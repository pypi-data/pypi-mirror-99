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
#  TODO:  add back in when artifactz is published to a repo
# from artifactz.artifact_registry import ArtifactRegistry
from providah.factories.package_factory import PackageFactory as pf

from servz.core.build_step import BuildStep


class PackagePublisher(BuildStep):

    def __init__(self, **kwargs):
        super().__init__()
        self._build_flows: list = list()

        artifactz_config = kwargs['artifactz']
        #  self.__artifact_registry: ArtifactRegistry = pf.create(key=artifactz_config['type'], configuration=artifactz_config['conf'])

    def build_part(self, **kwargs):

        raise NotImplementedError(f'Method not implemented for {type(self).__name__}.')

    def get_results(self):

        return {
            "package_publisher": self._build_flows
        }
