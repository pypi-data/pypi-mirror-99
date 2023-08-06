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
"""Base class to define how to operator an executor."""
import sys
from typing import Dict, List, Optional, cast

import tensorflow as tf
from tfx import types
from tfx.dsl.components.base import base_executor
from tfx.dsl.io import fileio
from tfx.orchestration.portable import base_executor_operator
from tfx.orchestration.portable import data_types
from tfx.proto.orchestration import executable_spec_pb2
from tfx.proto.orchestration import execution_result_pb2
from tfx.types.value_artifact import ValueArtifact
from tfx.utils import import_utils

from google.protobuf import message

_STATEFUL_WORKING_DIR = 'stateful_working_dir'


def _populate_output_artifact(
    executor_output: execution_result_pb2.ExecutorOutput,
    output_dict: Dict[str, List[types.Artifact]]):
  """Populate output_dict to executor_output."""
  for key, artifact_list in output_dict.items():
    artifacts = execution_result_pb2.ExecutorOutput.ArtifactList()
    for artifact in artifact_list:
      artifacts.artifacts.append(artifact.mlmd_artifact)
    executor_output.output_artifacts[key].CopyFrom(artifacts)


class PythonExecutorOperator(base_executor_operator.BaseExecutorOperator):
  """PythonExecutorOperator handles python class based executor's init and execution.

  Attributes:
    extra_flags: Extra flags that will pass to Python executors. It come from
      two sources in the order:
      1. The `extra_flags` set in the executor spec.
      2. The flags passed in when starting the program by users or by other
         systems.
      The interpretation of these flags relying on the executor implementation.
  """

  SUPPORTED_EXECUTOR_SPEC_TYPE = [executable_spec_pb2.PythonClassExecutableSpec]
  SUPPORTED_PLATFORM_CONFIG_TYPE = []

  def __init__(self,
               executor_spec: message.Message,
               platform_config: Optional[message.Message] = None):
    """Initialize an PythonExecutorOperator.

    Args:
      executor_spec: The specification of how to initialize the executor.
      platform_config: The specification of how to allocate resource for the
        executor.
    """
    # Python executors run locally, so platform_config is not used.
    del platform_config
    super().__init__(executor_spec)
    python_class_executor_spec = cast(
        executable_spec_pb2.PythonClassExecutableSpec, self._executor_spec)
    self._executor_cls = import_utils.import_class_by_path(
        python_class_executor_spec.class_path)
    self.extra_flags = []
    self.extra_flags.extend(python_class_executor_spec.extra_flags)
    self.extra_flags.extend(sys.argv[1:])

  def run_executor(
      self, execution_info: data_types.ExecutionInfo
  ) -> execution_result_pb2.ExecutorOutput:
    """Invokers executors given input from the Launcher.

    Args:
      execution_info: A wrapper of the details of this execution.

    Returns:
      The output from executor.
    """
    # TODO(b/156000550): We should not specialize `Context` to embed beam
    # pipeline args. Instead, the `Context` should consists of generic purpose
    # `extra_flags` which can be interpreted differently by different
    # implementations of executors.
    context = base_executor.BaseExecutor.Context(
        beam_pipeline_args=self.extra_flags,
        tmp_dir=execution_info.tmp_dir,
        unique_id=str(execution_info.execution_id),
        executor_output_uri=execution_info.execution_output_uri,
        stateful_working_dir=execution_info.stateful_working_dir)
    executor = self._executor_cls(context=context)

    for _, artifact_list in execution_info.input_dict.items():
      for artifact in artifact_list:
        if isinstance(artifact, ValueArtifact):
          # Read ValueArtifact into memory.
          artifact.read()

    result = executor.Do(execution_info.input_dict, execution_info.output_dict,
                         execution_info.exec_properties)
    if not result:
      # If result is not returned from the Do function, then try to
      # read if from the executor_output_uri.
      try:
        with fileio.open(execution_info.execution_output_uri, 'rb') as f:
          result = execution_result_pb2.ExecutorOutput.FromString(
              f.read())
      except tf.errors.NotFoundError:
        # Old style TFX executor doesn't return executor_output, but modify
        # output_dict and exec_properties in place. For backward compatibility,
        # we use their executor_output and exec_properties to construct
        # ExecutorOutput.
        result = execution_result_pb2.ExecutorOutput()
        _populate_output_artifact(result, execution_info.output_dict)
    return result
