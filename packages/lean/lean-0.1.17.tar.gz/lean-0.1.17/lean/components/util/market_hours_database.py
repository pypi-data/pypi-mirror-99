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
from typing import Dict

from lean.components.config.lean_config_manager import LeanConfigManager
from lean.models.api import QCSecurityType
from lean.models.data import MarketHoursDatabaseEntry


class MarketHoursDatabase:
    """The MarketHoursDatabase class handles access to the market-hours-database.json file."""

    def __init__(self, lean_config_manager: LeanConfigManager) -> None:
        """Creates a new MarketHoursDatabase instance.

        :param lean_config_manager: the LeanConfigManager instance that is used when retrieving the data directory
        """
        self._lean_config_manager = lean_config_manager

    def get_entry(self, security_type: QCSecurityType, market: str, ticker: str) -> MarketHoursDatabaseEntry:
        """Reads the market hours database and returns the entry for the given data.

        An error is raised if the market hours database does not contain an entry matching the given data.

        :param security_type: the security type of the data
        :param market: the market of the data
        :param ticker: the ticker of the data
        :return: the market hours database entry for the data
        """
        entries = self._get_all_entries()

        keys_to_check = [f"{security_type.value}-{market}-{ticker.upper()}", f"{security_type.value}-{market}-[*]"]

        for key in keys_to_check:
            if key in entries:
                return entries[key]

        raise ValueError(f"Could not find entry in market hours database, checked following keys: {keys_to_check}")

    def _get_all_entries(self) -> Dict[str, MarketHoursDatabaseEntry]:
        """Reads the market hours database and returns all parsed entries by name.

        :return: a dict containing all market hours database entries by name
        """
        data_dir = self._lean_config_manager.get_data_directory()
        market_hours_database_path = data_dir / "market-hours" / "market-hours-database.json"

        market_hours_database = json.loads(market_hours_database_path.read_text(encoding="utf-8"))

        return {key: MarketHoursDatabaseEntry(**value) for key, value in market_hours_database["entries"].items()}
