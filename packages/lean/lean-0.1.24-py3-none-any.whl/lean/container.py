# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from lean.components.api.api_client import APIClient
from lean.components.cloud.cloud_project_manager import CloudProjectManager
from lean.components.cloud.cloud_runner import CloudRunner
from lean.components.cloud.data_downloader import DataDownloader
from lean.components.cloud.pull_manager import PullManager
from lean.components.cloud.push_manager import PushManager
from lean.components.config.cli_config_manager import CLIConfigManager
from lean.components.config.lean_config_manager import LeanConfigManager
from lean.components.config.optimizer_config_manager import OptimizerConfigManager
from lean.components.config.project_config_manager import ProjectConfigManager
from lean.components.config.storage import Storage
from lean.components.docker.csharp_compiler import CSharpCompiler
from lean.components.docker.docker_manager import DockerManager
from lean.components.docker.lean_runner import LeanRunner
from lean.components.util.logger import Logger
from lean.components.util.market_hours_database import MarketHoursDatabase
from lean.components.util.name_generator import NameGenerator
from lean.components.util.project_manager import ProjectManager
from lean.components.util.task_manager import TaskManager
from lean.components.util.update_manager import UpdateManager
from lean.constants import CACHE_PATH, CREDENTIALS_CONFIG_PATH, GENERAL_CONFIG_PATH


class Container(DeclarativeContainer):
    """The Container class contains providers for all reusable components used by the CLI."""
    logger = Singleton(Logger)

    task_manager = Singleton(TaskManager, logger=logger)
    name_generator = Singleton(NameGenerator)

    general_storage = Singleton(Storage, file=GENERAL_CONFIG_PATH)
    credentials_storage = Singleton(Storage, file=CREDENTIALS_CONFIG_PATH)
    cache_storage = Singleton(Storage, file=CACHE_PATH)

    project_config_manager = Singleton(ProjectConfigManager)
    cli_config_manager = Singleton(CLIConfigManager,
                                   general_storage=general_storage,
                                   credentials_storage=credentials_storage)
    lean_config_manager = Singleton(LeanConfigManager,
                                    cli_config_manager=cli_config_manager,
                                    project_config_manager=project_config_manager)

    project_manager = Singleton(ProjectManager, project_config_manager=project_config_manager)

    market_hours_database = Singleton(MarketHoursDatabase, lean_config_manager=lean_config_manager)

    api_client = Factory(APIClient,
                         logger=logger,
                         user_id=cli_config_manager.provided.user_id.get_value()(),
                         api_token=cli_config_manager.provided.api_token.get_value()())

    cloud_runner = Singleton(CloudRunner, logger=logger, api_client=api_client, task_manager=task_manager)
    pull_manager = Singleton(PullManager,
                             logger=logger,
                             api_client=api_client,
                             project_manager=project_manager,
                             project_config_manager=project_config_manager)
    push_manager = Singleton(PushManager,
                             logger=logger,
                             api_client=api_client,
                             project_manager=project_manager,
                             project_config_manager=project_config_manager)
    data_downloader = Singleton(DataDownloader,
                                logger=logger,
                                api_client=api_client,
                                lean_config_manager=lean_config_manager,
                                market_hours_database=market_hours_database)
    cloud_project_manager = Singleton(CloudProjectManager,
                                      api_client=api_client,
                                      project_config_manager=project_config_manager,
                                      pull_manager=pull_manager,
                                      push_manager=push_manager)

    docker_manager = Singleton(DockerManager, logger=logger)

    csharp_compiler = Singleton(CSharpCompiler, logger=logger, docker_manager=docker_manager)
    lean_runner = Singleton(LeanRunner,
                            logger=logger,
                            csharp_compiler=csharp_compiler,
                            lean_config_manager=lean_config_manager,
                            docker_manager=docker_manager)

    update_manager = Singleton(UpdateManager, logger=logger, cache_storage=cache_storage, docker_manager=docker_manager)

    optimizer_config_manager = Singleton(OptimizerConfigManager, logger=logger)


container = Container()
