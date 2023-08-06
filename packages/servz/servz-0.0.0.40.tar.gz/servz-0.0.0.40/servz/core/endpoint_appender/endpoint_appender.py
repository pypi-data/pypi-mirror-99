# Copyright © 2020 Hashmap, Inc
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
from servz.core.build_step import BuildStep


class EndpointAppender(BuildStep):

    def __init__(self, **kwargs):
        super().__init__()
        self._endpoints: list = list()

    def build_part(self, **kwargs):
        pipelines = kwargs.get('pipelines')
        self._build_runner_script(pipe=pipelines)
        self._build_artifact_bundle(pipe=pipelines)
        self._build_endpoint(pipe=pipelines)

    def get_results(self):

        return {
            "endpoint_appender": self._endpoints
        }

    def _build_runner_script(self, pipe):

        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def _build_artifact_bundle(self, pipe):

        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def _build_endpoint(self, pipe):

        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')