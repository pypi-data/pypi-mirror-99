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
import uuid
from typing import List
from jinja2 import Template
from servz.core.orchestration_artifact_builder.orchestration_artifact_builder import OrchestrationArtifactBuilder
from servz.utils.parsers.project_config import ProjectConfig


class PrefectArtifactBuilder(OrchestrationArtifactBuilder):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.__manifest_templates = {
            'prefect_flow_template': os.path.join(ProjectConfig.package_root(), 'templates/prefect_templates',
                                                'prefect_flow_template'),
            'prefect_class_template': os.path.join(ProjectConfig.package_root(), 'templates/prefect_templates',
                                                  'prefect_class_template'),
            'prefect_edge_template': os.path.join(ProjectConfig.package_root(), 'templates/prefect_templates',
                                                  'prefect_edge_template'),
            'prefect_instance_template': os.path.join(ProjectConfig.package_root(), 'templates/prefect_templates',
                                                  'prefect_instance_template')

        }

        self.__namespace = kwargs.get('namespace')

    def _compile_workflow(self, pipe: dict) -> dict:

        classes: list = list()
        instances: list = list()
        edges: list = list()
        for task in pipe['workflow']:
            classes.append(self.__append_class(task))
            instances.append(self.__append_instance(task))
            edges.append(self.__append_edge(task))

        success = self.__build_prefect_flow(pipe=pipe, classes=classes, instances=instances, edges=edges)

        return {
            'success': success,
        }

    def __append_class(self, task):

        with open(self.__manifest_templates['prefect_class_template'], 'r') as f:
            class_temp = f.read()

        script = task.get("predict").replace("\\", "\\\\")

        class_template = Template(class_temp, autoescape=True)
        task_str = class_template.render(
            # TODO: replace this with camel case at some point
            class_name=task.get("stage_name").lower().replace(" ", "_"),
            command=f'{task.get("type")} {script.lower()}'
        )

        return task_str

    def __append_instance(self, task):
        with open(self.__manifest_templates['prefect_instance_template'], 'r') as f:
            instance_temp = f.read()

        node = task.get("stage_name").lower().replace(" ", "_")

        instance_template = Template(instance_temp, autoescape=True)
        task_str = instance_template.render(
            node=node,
            # TODO: replace this with camel case at some point
            instance=node.title()
        )

        return task_str

    def __append_edge(self, task):
        with open(self.__manifest_templates['prefect_edge_template'], 'r') as f:
            edge_temp = f.read()

        edge_str = ""
        deps = task.get('dependencies')
        if len(deps) == 0:
            return edge_str
        b = task["stage_name"].lower().replace(" ", "_")

        for dep in deps:
            edge_template = Template(edge_temp, autoescape=True)
            temp_str = instance_template.render(
                a=dep.lower().replace(" ", "_"),
                b=b
            )
            edge_str = f'{edge_str}\n{temp_str}'

        return edge_str

    def __build_prefect_flow(self, pipe: dict, classes: list, instances: list, edges: list):
        pipeline_name = pipe['name'].lower().replace(" ", "_")

        with open(self.__manifest_templates['prefect_flow_template'], 'r') as f:
            dag_temp = f.read()

        dag_template = Template(dag_temp, autoescape=True)

        airflow_str = dag_template.render(
            classes=''.join(classes),
            instances=''.join(instances),
            edges=''.join(edges),
        )

        pipeline_name = pipeline_name + '_prefect_' + uuid.uuid4().hex + '.py'
        # TODO This shouldn't be hard-coded and should be by 'run'
        with open(pipeline_name, 'w') as stream:
            stream.write(airflow_str)

        pipe['artifact_name'] = pipeline_name

        return True
