# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Portable library for output artifacts resolution including caching decision."""

import collections
import datetime
import os
from typing import Dict, List, Optional, Text

from absl import logging
from tfx import types
from tfx.dsl.io import fileio
from tfx.proto.orchestration import pipeline_pb2
from tfx.types import artifact_utils
from tfx.types.value_artifact import ValueArtifact

_SYSTEM = '.system'
_EXECUTOR_EXECUTION = 'executor_execution'
_DRIVER_EXECUTION = 'driver_execution'
_STATEFUL_WORKING_DIR = 'stateful_working_dir'
_DRIVER_OUTPUT_FILE = 'driver_output.pb'
_EXECUTOR_OUTPUT_FILE = 'executor_output.pb'
_VALUE_ARTIFACT_FILE_NAME = 'value'


def make_output_dirs(output_dict: Dict[Text, List[types.Artifact]]) -> None:
  """Make dirs for output artifacts' URI."""
  for _, artifact_list in output_dict.items():
    for artifact in artifact_list:
      if isinstance(artifact, ValueArtifact):
        # If it is a ValueArtifact, create a file.
        artifact_dir = os.path.dirname(artifact.uri)
        fileio.makedirs(artifact_dir)
        with fileio.open(artifact.uri, 'w') as f:
          # Because fileio.open won't create an empty file, we write an
          # empty string to it to force the creation.
          f.write('')
      else:
        # Otherwise create a dir.
        fileio.makedirs(artifact.uri)


def remove_output_dirs(output_dict: Dict[Text, List[types.Artifact]]) -> None:
  """Remove dirs of output artifacts' URI."""
  for _, artifact_list in output_dict.items():
    for artifact in artifact_list:
      if fileio.isdir(artifact.uri):
        fileio.rmtree(artifact.uri)
      else:
        fileio.remove(artifact.uri)


def remove_stateful_working_dir(stateful_working_dir: Text) -> None:
  """Remove stateful_working_dir."""
  # Clean up stateful working dir
  # Note that:
  # stateful_working_dir = os.path.join(
  #    self._node_dir,
  #    _SYSTEM,
  #    _STATEFUL_WORKING_DIR, <-- we want to clean from this level down.
  #    dir_suffix)
  stateful_working_dir = os.path.abspath(
      os.path.join(stateful_working_dir, os.pardir))
  try:
    fileio.rmtree(stateful_working_dir)
  except Exception as e:  # pylint: disable=broad-except
    if 'NotFoundError' in str(type(e)):
      # TODO(b/175244977): This is a workaround to avoid introducing
      # tensorflow dependency. Change this except block to use a generic
      # NotFoundError once it is Defined in fileio.
      logging.warning(
          'stateful_working_dir %s is not found, not going to delete it.',
          stateful_working_dir)
    else:
      raise


class OutputsResolver:
  """This class has methods to handle launcher output related logic."""

  def __init__(self,
               pipeline_node: pipeline_pb2.PipelineNode,
               pipeline_info: pipeline_pb2.PipelineInfo,
               pipeline_runtime_spec: pipeline_pb2.PipelineRuntimeSpec,
               execution_mode: 'pipeline_pb2.Pipeline.ExecutionMode' = (
                   pipeline_pb2.Pipeline.SYNC)):
    self._pipeline_node = pipeline_node
    self._pipeline_info = pipeline_info
    self._pipeline_root = (
        pipeline_runtime_spec.pipeline_root.field_value.string_value)
    self._pipeline_run_id = (
        pipeline_runtime_spec.pipeline_run_id.field_value.string_value)
    self._execution_mode = execution_mode
    self._node_dir = os.path.join(self._pipeline_root,
                                  pipeline_node.node_info.id)

  def generate_output_artifacts(
      self, execution_id: int) -> Dict[Text, List[types.Artifact]]:
    """Generates output artifacts given execution_id."""
    output_artifacts = collections.defaultdict(list)
    for key, output_spec in self._pipeline_node.outputs.outputs.items():
      artifact = artifact_utils.deserialize_artifact(
          output_spec.artifact_spec.type)
      artifact.uri = os.path.join(self._node_dir, key, str(execution_id))
      if isinstance(artifact, ValueArtifact):
        artifact.uri = os.path.join(artifact.uri, _VALUE_ARTIFACT_FILE_NAME)
      # artifact.name will contain the set of information to track its creation
      # and is guaranteed to be idempotent across retires of a node.
      artifact_name = f'{self._pipeline_info.id}'
      if self._execution_mode == pipeline_pb2.Pipeline.SYNC:
        artifact_name = f'{artifact_name}:{self._pipeline_run_id}'
      # The index of this artifact, since we only has one artifact per output
      # for now, it is always 0.
      # TODO(b/162331170): Update the "0" to the actual index.
      artifact_name = (
          f'{artifact_name}:{self._pipeline_node.node_info.id}:{key}:0')
      artifact.name = artifact_name
      logging.debug('Creating output artifact uri %s as directory',
                    artifact.uri)
      output_artifacts[key].append(artifact)

    return output_artifacts

  def get_executor_output_uri(self, execution_id: int) -> Text:
    """Generates executor output uri given execution_id."""
    execution_dir = os.path.join(self._node_dir, _SYSTEM, _EXECUTOR_EXECUTION,
                                 str(execution_id))
    fileio.makedirs(execution_dir)
    return os.path.join(execution_dir, _EXECUTOR_OUTPUT_FILE)

  def get_driver_output_uri(self) -> Text:
    driver_output_dir = os.path.join(
        self._node_dir, _SYSTEM, _DRIVER_EXECUTION,
        str(int(datetime.datetime.now().timestamp() * 1000000)))
    fileio.makedirs(driver_output_dir)
    return os.path.join(driver_output_dir, _DRIVER_OUTPUT_FILE)

  def get_stateful_working_directory(
      self, execution_id: Optional[int] = None) -> Text:
    """Generates stateful working directory given (optional) execution id.

    Args:
      execution_id: An optional execution id which will be used as part of the
        stateful working dir path if provided. The stateful working dir path
        will be <node_dir>/.system/stateful_working_dir/<execution_id>. If
        execution_id is not provided, for backward compatibility purposes,
        <pipeline_run_id> is used instead of <execution_id> but an error is
        raised if the execution_mode is not SYNC (since ASYNC pipelines have
        no pipeline_run_id).

    Returns:
      Path to stateful working directory.

    Raises:
      ValueError: If execution_id is not provided and execution_mode of the
        pipeline is not SYNC.
    """
    if (execution_id is None and
        self._execution_mode != pipeline_pb2.Pipeline.SYNC):
      raise ValueError(
          'Cannot create stateful working dir if execution id is `None` and '
          'the execution mode of the pipeline is not `SYNC`.')

    if execution_id is None:
      dir_suffix = self._pipeline_run_id
    else:
      dir_suffix = str(execution_id)

    # TODO(b/150979622): We should introduce an id that is not changed across
    # retries of the same component run to provide better isolation between
    # "retry" and "new execution". When it is available, introduce it into
    # stateful working directory.
    # NOTE: If this directory structure is changed, please update
    # the remove_stateful_working_dir function in this file accordingly.
    stateful_working_dir = os.path.join(self._node_dir, _SYSTEM,
                                        _STATEFUL_WORKING_DIR,
                                        dir_suffix)
    try:
      fileio.makedirs(stateful_working_dir)
    except Exception:  # pylint: disable=broad-except
      logging.exception('Failed to make stateful working dir: %s',
                        stateful_working_dir)
      raise
    return stateful_working_dir

  def make_tmp_dir(self, execution_id: int) -> Text:
    """Generates a temporary directory."""
    result = os.path.join(self._node_dir, _SYSTEM, _EXECUTOR_EXECUTION,
                          str(execution_id), '.temp', '')
    fileio.makedirs(result)
    return result
