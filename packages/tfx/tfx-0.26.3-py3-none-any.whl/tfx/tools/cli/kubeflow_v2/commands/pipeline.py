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
"""Commands for pipeline group."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Text

import click
from tfx.tools.cli import labels
from tfx.tools.cli.cli_context import Context
from tfx.tools.cli.cli_context import pass_context
from tfx.tools.cli.kubeflow_v2 import labels as kubeflow_labels
from tfx.tools.cli.kubeflow_v2.handler import kubeflow_v2_handler
from tfx.utils import version_utils


_DEFAULT_TFX_IMAGE = 'gcr.io/tfx-oss-public/tfx:{}'.format(
    version_utils.get_image_version())


@click.group('pipeline')
def pipeline_group() -> None:
  pass


# TODO(b/149347293): Unify the CLI flags for different engines.
@pipeline_group.command('create', help='Create a pipeline')
@pass_context
@click.option(
    '--pipeline_path',
    '--pipeline-path',
    required=True,
    type=str,
    help='Path to Python DSL.')
@click.option(
    '--build_target_image',
    '--build-target-image',
    default=None,
    type=str,
    help='Target container image path. The target image will be built by this '
    'command to include local python codes to the TFX default image. By default, '
    'it uses docker daemon to build an image which will install the local '
    'python setup file onto TFX default image. You can place a setup.py file '
    'to control the python code to install the dependent packages. You can also '
    'customize the Skaffold building options by placing a build.yaml in the '
    'local directory. In addition, you can place a Dockerfile file to customize'
    'the docker building script.')
@click.option(
    '--build_base_image',
    '--build-base-image',
    default=None,
    type=str,
    help='Container image path to be used as the base image. If not specified, '
    'target image will be build based on the released TFX image.')
@click.option(
    '--skaffold_cmd',
    '--skaffold-cmd',
    default=None,
    type=str,
    help='Skaffold program command.')
def create_pipeline(ctx: Context, pipeline_path: Text, build_target_image: Text,
                    skaffold_cmd: Text, build_base_image: Text) -> None:
  """Command definition to create a pipeline."""
  click.echo('Creating pipeline')
  ctx.flags_dict[labels.ENGINE_FLAG] = kubeflow_labels.KUBEFLOW_V2_ENGINE
  ctx.flags_dict[labels.PIPELINE_DSL_PATH] = pipeline_path
  ctx.flags_dict[kubeflow_labels.TFX_IMAGE_ENV] = build_target_image
  ctx.flags_dict[labels.BASE_IMAGE] = build_base_image
  ctx.flags_dict[labels.SKAFFOLD_CMD] = skaffold_cmd
  kubeflow_v2_handler.KubeflowV2Handler(ctx.flags_dict).create_pipeline()


# TODO(b/149347293): Unify the CLI flags for different engines.
@pipeline_group.command('update', help='Update an existing pipeline.')
@pass_context
@click.option(
    '--pipeline_path',
    '--pipeline-path',
    required=True,
    type=str,
    help='Path to Python DSL file')
@click.option(
    '--skaffold_cmd',
    '--skaffold-cmd',
    default=None,
    type=str,
    help='Skaffold program command.')
def update_pipeline(ctx: Context, pipeline_path: Text,
                    skaffold_cmd: Text) -> None:
  """Command definition to update a pipeline."""
  click.echo('Updating pipeline')
  ctx.flags_dict[labels.ENGINE_FLAG] = kubeflow_labels.KUBEFLOW_V2_ENGINE
  ctx.flags_dict[labels.PIPELINE_DSL_PATH] = pipeline_path
  ctx.flags_dict[labels.SKAFFOLD_CMD] = skaffold_cmd
  kubeflow_v2_handler.KubeflowV2Handler(ctx.flags_dict).update_pipeline()


@pipeline_group.command('list', help='List all the pipelines')
@pass_context
def list_pipelines(ctx: Context) -> None:
  """Command definition to list pipelines."""
  click.echo('Listing all pipelines')
  ctx.flags_dict[labels.ENGINE_FLAG] = kubeflow_labels.KUBEFLOW_V2_ENGINE
  kubeflow_v2_handler.KubeflowV2Handler(ctx.flags_dict).list_pipelines()


@pipeline_group.command('delete', help='Delete a pipeline')
@pass_context
@click.option(
    '--pipeline_name',
    '--pipeline-name',
    required=True,
    type=str,
    help='Name of the pipeline')
def delete_pipeline(ctx: Context, pipeline_name: Text) -> None:
  """Command definition to delete a pipeline."""
  click.echo('Deleting pipeline')
  ctx.flags_dict[labels.ENGINE_FLAG] = kubeflow_labels.KUBEFLOW_V2_ENGINE
  ctx.flags_dict[labels.PIPELINE_NAME] = pipeline_name
  kubeflow_v2_handler.KubeflowV2Handler(ctx.flags_dict).delete_pipeline()


@pipeline_group.command('compile', help='Compile a pipeline.')
@pass_context
@click.option(
    '--pipeline_path',
    '--pipeline-path',
    required=True,
    type=str,
    help='Path to Python DSL file.')
@click.option(
    '--target_image',
    '--target-image',
    default=_DEFAULT_TFX_IMAGE,
    type=str,
    help='Target container image path. The target image will used as the '
    'container in the TFX pipeline execution. Default to the latest TFX '
    'image.')
@click.option(
    '--project_id',
    '--project-id',
    type=str,
    required=True,
    help='GCP project ID that will be used to invoke the service.')
def compile_pipeline(ctx: Context, pipeline_path: Text, target_image: Text,
                     project_id: Text) -> None:
  """Command definition to compile a pipeline."""
  click.echo('Compiling pipeline')
  ctx.flags_dict[labels.ENGINE_FLAG] = kubeflow_labels.KUBEFLOW_V2_ENGINE
  ctx.flags_dict[labels.PIPELINE_DSL_PATH] = pipeline_path
  ctx.flags_dict[kubeflow_labels.TFX_IMAGE_ENV] = target_image
  ctx.flags_dict[kubeflow_labels.GCP_PROJECT_ID_ENV] = project_id

  kubeflow_v2_handler.KubeflowV2Handler(ctx.flags_dict).compile_pipeline()
