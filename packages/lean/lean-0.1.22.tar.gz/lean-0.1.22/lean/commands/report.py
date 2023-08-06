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

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import click
from docker.types import Mount

from lean.click import LeanCommand, PathParameter
from lean.constants import ENGINE_IMAGE, PROJECT_CONFIG_FILE_NAME
from lean.container import container


def _find_project_directory(backtest_file: Path) -> Optional[Path]:
    """Returns the project directory, or None if backtest_file is not stored in a project directory.

    :param backtest_file: the path to the JSON file containing the backtest results
    :return: the path to the project directory, or None if backtest_file is stored outside a project directory
    """
    current_directory = backtest_file.parent

    # Loop until we find the root directory ("/")
    while current_directory != current_directory.parent:
        if (current_directory / PROJECT_CONFIG_FILE_NAME).is_file():
            return current_directory

        current_directory = current_directory.parent

    return None


@click.command(cls=LeanCommand, requires_lean_config=True)
@click.option("--backtest-data-source-file",
              type=PathParameter(exists=True, file_okay=True, dir_okay=False),
              required=True,
              help="Path to the JSON file containing the backtest results")
@click.option("--live-data-source-file",
              type=PathParameter(exists=True, file_okay=True, dir_okay=False),
              help="Path to the JSON file containing the live trading results")
@click.option("--report-destination",
              type=PathParameter(exists=False, file_okay=True, dir_okay=False),
              default=lambda: Path.cwd() / "report.html",
              help="Path where the generated report is stored as HTML (defaults to ./report.html)")
@click.option("--strategy-name",
              type=str,
              help="Name of the strategy, will appear at the top-right corner of each page")
@click.option("--strategy-version",
              type=str,
              help="Version number of the strategy, will appear next to the project name")
@click.option("--strategy-description",
              type=str,
              help="Description of the strategy, will appear under the 'Strategy Description' section")
@click.option("--overwrite",
              is_flag=True,
              default=False,
              help="Overwrite --report-destination if it already contains a file")
@click.option("--update",
              is_flag=True,
              default=False,
              help="Pull the selected LEAN engine version before running the report creator")
@click.option("--version",
              type=str,
              default="latest",
              help="The LEAN engine version to run (defaults to the latest installed version)")
def report(backtest_data_source_file: Path,
           live_data_source_file: Optional[Path],
           report_destination: Path,
           strategy_name: Optional[str],
           strategy_version: Optional[str],
           strategy_description: Optional[str],
           overwrite: bool,
           update: bool,
           version: str) -> None:
    """Generate a report of a backtest.

    This runs the LEAN Report Creator in Docker to generate a polished, professional-grade report of a backtest.

    The name, description, and version are optional and will be blank if not given.

    If the given backtest data source file is stored in a project directory (or one of its subdirectories, like the
    default <project>/backtests/<timestamp>), the default name is the name of the project directory and the default
    description is the description stored in the project's config.json file.
    """
    if report_destination.exists() and not overwrite:
        raise RuntimeError(f"{report_destination} already exists, use --overwrite to overwrite it")

    project_directory = _find_project_directory(backtest_data_source_file)

    if project_directory is not None:
        if strategy_name is None:
            strategy_name = project_directory.name

        if strategy_description is None:
            project_config_manager = container.project_config_manager()
            project_config = project_config_manager.get_project_config(project_directory)
            strategy_description = project_config.get("description", "")

    # The configuration given to the report creator
    # See https://github.com/QuantConnect/Lean/blob/master/Report/config.example.json
    report_config = {
        "data-folder": "/Lean/Data",
        "strategy-name": strategy_name or "",
        "strategy-version": strategy_version or "",
        "strategy-description": strategy_description or "",
        "live-data-source-file": "live-data-source-file.json" if live_data_source_file is not None else "",
        "backtest-data-source-file": "backtest-data-source-file.json",
        "report-destination": "/Results/report.html",

        "environment": "report",

        "log-handler": "QuantConnect.Logging.CompositeLogHandler",
        "messaging-handler": "QuantConnect.Messaging.Messaging",
        "job-queue-handler": "QuantConnect.Queues.JobQueue",
        "api-handler": "QuantConnect.Api.Api",
        "map-file-provider": "QuantConnect.Data.Auxiliary.LocalDiskMapFileProvider",
        "factor-file-provider": "QuantConnect.Data.Auxiliary.LocalDiskFactorFileProvider",
        "data-provider": "QuantConnect.Lean.Engine.DataFeeds.DefaultDataProvider",
        "alpha-handler": "QuantConnect.Lean.Engine.Alphas.DefaultAlphaHandler",
        "data-channel-provider": "DataChannelProvider",

        "environments": {
            "report": {
                "live-mode": False,

                "setup-handler": "QuantConnect.Lean.Engine.Setup.ConsoleSetupHandler",
                "result-handler": "QuantConnect.Lean.Engine.Results.BacktestingResultHandler",
                "data-feed-handler": "QuantConnect.Lean.Engine.DataFeeds.FileSystemDataFeed",
                "real-time-handler": "QuantConnect.Lean.Engine.RealTime.BacktestingRealTimeHandler",
                "history-provider": "QuantConnect.Lean.Engine.HistoricalData.SubscriptionDataReaderHistoryProvider",
                "transaction-handler": "QuantConnect.Lean.Engine.TransactionHandlers.BacktestingTransactionHandler"
            }
        }
    }

    output_dir = Path(tempfile.mkdtemp())

    config_path = output_dir / "config.json"
    with config_path.open("w+", encoding="utf-8") as file:
        json.dump(report_config, file)

    lean_config_manager = container.lean_config_manager()
    data_dir = lean_config_manager.get_data_directory()

    run_options: Dict[str, Any] = {
        "working_dir": "/Lean/Report/bin/Debug",
        "entrypoint": ["mono", "QuantConnect.Report.exe"],
        "mounts": [
            Mount(target="/Lean/Report/bin/Debug/config.json",
                  source=str(config_path),
                  type="bind",
                  read_only=True),
            Mount(target="/Lean/Report/bin/Debug/backtest-data-source-file.json",
                  source=str(backtest_data_source_file),
                  type="bind",
                  read_only=True)
        ],
        "volumes": {
            str(data_dir): {
                "bind": "/Lean/Data",
                "mode": "ro"
            },
            str(output_dir): {
                "bind": "/Results",
                "mode": "rw"
            }
        }
    }

    if live_data_source_file is not None:
        run_options["mounts"].append(Mount(target="/Lean/Report/bin/Debug/live-data-source-file.json",
                                           source=str(live_data_source_file),
                                           type="bind",
                                           read_only=True))

    docker_manager = container.docker_manager()

    if version != "latest":
        if not docker_manager.tag_exists(ENGINE_IMAGE, version):
            raise RuntimeError("The specified version does not exist")

    if update:
        docker_manager.pull_image(ENGINE_IMAGE, version)

    success = docker_manager.run_image(ENGINE_IMAGE, version, **run_options)
    if not success:
        raise RuntimeError("Something went wrong while running the LEAN Report Creator")

    report_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_dir / "report.html", report_destination)

    logger = container.logger()
    logger.info(f"Successfully generated report to '{report_destination}'")

    if version == "latest" and not update:
        update_manager = container.update_manager()
        update_manager.warn_if_docker_image_outdated(ENGINE_IMAGE)
