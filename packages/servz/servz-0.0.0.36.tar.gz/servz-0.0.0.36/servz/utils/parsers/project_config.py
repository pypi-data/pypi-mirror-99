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
import platform
import os
from pathlib import Path


class ProjectConfig:
    @classmethod
    def home(cls):
        if not os.getenv('SERVZ'):
            if platform.system().lower() != 'windows':
                os.environ['SERVZ'] = os.getenv('HOME')
            else:
                os.environ['SERVZ'] = os.getenv('USERPROFILE')
        return os.getenv('SERVZ')

    @classmethod
    def env_var(cls):
        return os.getenv('SERVZ')

    @classmethod
    def config_path(cls):
        return os.path.join(cls.home(), f'.{__name__.split(".")[0]}/configuration.yml')

    @classmethod
    def env_path(cls):
        return os.path.join(cls.home(), f'.{__name__.split(".")[0]}/command_config.yml')

    @classmethod
    def package_root(cls):
        return Path(__file__).parent.parent.parent
