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
"""Kubeflow pipelines V2 specific flags."""

KUBEFLOW_V2_ENGINE = 'kubeflow_v2'
JOB_NAME = 'job_name'
# Environment variable for the default TFX image.
TFX_IMAGE_ENV = 'TFX_IMAGE'
# API key used to authenticate services on GCP.
API_KEY_ENV = 'API_KEY'
# GCP project ID used.
GCP_PROJECT_ID_ENV = 'GCP_PROJECT_ID'
# Flag used to indicate whether an actual execution is intended.
RUN_FLAG_ENV = 'run'
