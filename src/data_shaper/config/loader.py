"""Configuration loader for YAML files."""

import os
from pathlib import Path
import re
from typing import Any, Dict
import yaml
from dotenv import load_dotenv
from data_shaper.utils.exceptions import ConfigurationError
from data_shaper.utils.logger import get_logger


logger = get_logger(__name__)


class ConfigLoader:
    """Load and validate dataset configurations from YAML files."""

    def __init__(self, config_path: str):
        """
        Initialize the config loader.

        Args:
            config_path: Path to YAML file containing data processing configuration.
        """
        self.config_path = Path(config_path)
        load_dotenv()

    def _resolve_env_vars(self, data: Any) -> Any:
        """
        Recursively resolve environment variable placeholders in config.

        Supports ${VAR_NAME} syntax.

        Args:
            data: Configuration data (dict, list, or string)

        Returns:
            Data with environment variables resolved
        """
        if isinstance(data, dict):
            return {key: self._resolve_env_vars(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._resolve_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Replace ${VAR_NAME} with environment variable value
            def replace_env_var(match: re.Match) -> str:
                var_name = match.group(1)
                value = os.getenv(var_name)
                if value is None:
                    logger.warning(f"Environment variable {var_name} not found")
                    return match.group(0)
                return value

            return re.sub(r"\$\{([^}]+)\}", replace_env_var, data)
        else:
            return data

    def load_config(self) -> Dict[str, Any]:
        """
        Load a configuration from YAML.

        Returns:
            Validated configuration

        Raises:
            ConfigurationError: If config file not found or invalid
        """
        if not self.config_path.is_file():
            raise ConfigurationError(f"Config file not found: {self.config_path}")

        try:
            with open(self.config_path, "r") as f:
                raw_config = yaml.safe_load(f)

            if not raw_config:
                raise ConfigurationError(
                    f"Empty configuration file: {self.config_path}"
                )

            # Resolve environment variables
            config = self._resolve_env_vars(raw_config)

            logger.info(f"Loaded configuration for: {config['name']}")
            return config

        except yaml.YAMLError as e:
            raise ConfigurationError(f"Failed to parse YAML: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load config: {e}")
