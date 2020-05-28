import os
import digital_reporter.modules.utilities.configurations.configuration_manager as cm


def set_conf_env_file(configuration_file: str) -> None:
    os.environ[cm.ConfigurationConstants.CONFIGURATION_FILE_ENV_VAR] = configuration_file


def get_conf_env_file() -> str:
    return os.environ[cm.ConfigurationConstants.CONFIGURATION_FILE_ENV_VAR]
