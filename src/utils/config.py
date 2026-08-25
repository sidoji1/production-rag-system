from pathlib import Path

import yaml


class Config:
    """
    Loads and provides access to application configuration.
    """

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        with open(
            self.config_path,
            "r",
            encoding="utf-8",
        ) as file:
            self.data = yaml.safe_load(file)

    def get(self, *keys):
        """
        Retrieve a nested configuration value.

        Example:
            config.get("embedding", "model")
        """
        value = self.data

        for key in keys:
            if key not in value:
                raise KeyError(
                    f"Configuration key not found: {' -> '.join(keys)}"
                )

            value = value[key]

        return value