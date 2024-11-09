# © 2024 Seb Garrioch. All rights reserved.
# Published under the MIT License.
import json

from pathlib import Path
from typing import Optional


class ConfigManager:
    """Manages the configuration files for the project."""

    __auth_path: Optional[Path]
    __config_path: Path

    def __init__(self, config_path: str, auth_path: str = None):
        """Initializes the ConfigManager object.
        :param config_path: The path to the config.json file containing the configuration settings.
        :param auth_path: The path to the auth.json file containing the authentication settings.
        """
        self.__config_path = Path(config_path)
        if auth_path:
            self.__auth_path = Path(auth_path)
        else:
            self.__auth_path = None

    def load_config(self) -> dict:
        """Loads the configuration settings from the config.json file.
        :return: The configuration settings as a dictionary.
        """
        try:
            if not self.__config_path.exists():
                raise FileNotFoundError(f"Config file not found at {self.__config_path}")
            with open(self.__config_path) as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading config file: {e}")
            raise
