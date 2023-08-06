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
import os

import traceback

from servz.core.packager.packager import Packager
from servz.utils.exceptions.packager_error import PackagerError
from servz.utils.parsers.config_parser import ConfigParser
from servz.utils.parsers.cmd_config_parser import CmdConfigParser


class PrefectFilePackager(Packager):

    # ---------------------------------------- #
    # ------------- Construction ------------- #
    # ---------------------------------------- #

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__root_path: str = os.path.abspath(kwargs.get('project_path'))
        self.__workflows_path: str = os.path.join(kwargs.get('project_path'), 'workflows')

        self._workflows: list = list()
        self._pacified_tasks: list = list()
        self._file_list = []
        config_parser = ConfigParser()
        config_parser.parse()
        __cmd_config_obj = CmdConfigParser()
        __cmd_config_obj.parse()
        self.__cmd_config = __cmd_config_obj.configuration()

    def build_part(self, **kwargs):

        try:
            print("____-->>   build_part  prefect pkg ", kwargs)
            if 'pipelines' not in kwargs.keys():
                error_message = f"In {__name__}.build_part 'pipelines' was not found in build_part. " \
                                f"The parameters passed were: {' - '.join(kwargs.keys())}."
                raise ValueError(error_message)

            self._build(pipelines=kwargs.get("pipelines"))

        except:
            self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')

    def _build(self, pipelines: list) -> None:
        self._workflows = []
        for pipeline in pipelines:
            updated_pipes: list = list()
            while len(pipeline['workflow']) > 0:
                for pipe in pipeline['workflow']:
                    _res = self.__build_file(pipe=pipe)
                    if _res['successful']:
                        # Update dependencies pacified
                        self._pacified_tasks.append(pipe['stage_name'])
                        # Make a copy of the new pipes
                        updated_pipes.append(pipe)
                        # Remove old pipe
                        pipeline['workflow'].remove(pipe)

            self._build_flows.append(
                {
                    'name': pipeline['name'],
                    'workflow': self._file_list
                }
            )

    def __build_file(self, pipe: dict) -> dict:
        if pipe.get("cmd_type"):
            pipe.update(self.__cmd_config[pipe["cmd_type"]])

        if os.path.exists(self.__root_path):
            for root, dirs, files in os.walk(self.__root_path):
                for file in files:
                    selected_file = os.path.join(root, file)
                    self._file_list.append(selected_file)

            self._logger.info('file built.')
            try:

                return dict(
                    successful=True

                )

            except:
                self.__handle_exception(f'The following error has occurred{traceback.format_exc()}')
        else:
            self.__handle_exception(f"file {self.__root_path} do not exist.")

    def __handle_exception(self, message: str) -> None:
        message = f'In {__name__}: {message}'
        self._logger.error(message)
        raise (PackagerError(message))

    def __are_dependencies_pacified(self, dependencies: list) -> bool:
        return len([1 for dependency in dependencies if dependency in self._pacified_tasks]) == len(dependencies)
