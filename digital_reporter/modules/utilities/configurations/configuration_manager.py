import configparser
from digital_reporter.custom_exceptions import *
import os


class ConfigurationConstants:

    CONFIGURATION_FILE_ENV_VAR = "feedparse_config_file"

    # sections
    AWS_RDS_SECTION = "AWS_RDS"
    SCRAPER_INDIA_TODAY = "SCRAPER_INDIA_TODAY"
    SCRAPER_HINDUSTAN_TIMES = "SCRAPER_HINDUSTAN_TIMES"
    SCRAPER_ZEENEWS = "SCRAPER_ZEENEWS"
    SCRAPER_ABP = "SCRAPER_ABP"

    # aws rds section configurations
    AWS_RDS_HOST = "host"
    AWS_RDS_PORT = "port"
    AWS_RDS_USERNAME = "username"
    AWS_RDS_PASSWORD = "password"
    AWS_RDS_DB_NAME = "db_name"

    SECTIONS_REQURIED = [AWS_RDS_SECTION,
                         SCRAPER_INDIA_TODAY, SCRAPER_HINDUSTAN_TIMES, SCRAPER_ZEENEWS, SCRAPER_ABP]

    SCRAPERS = [SCRAPER_INDIA_TODAY, SCRAPER_HINDUSTAN_TIMES,
                SCRAPER_ZEENEWS, SCRAPER_ABP]


class Configuration(object):

    def __init__(self, configuration_file):
        self._configuration_file = configuration_file
        self._config = None

        self._set_config()
        self._check_sections()

    def _set_config(self):

        try:
            self._config = configparser.ConfigParser()
            self._config._interpolation = configparser.ExtendedInterpolation()
            self._config.read(self._configuration_file)

        except FileNotFoundError:
            print("Configuration file provided not found.")
            exit(1)

    def _check_sections(self):
        for section in ConfigurationConstants.SECTIONS_REQURIED:
            if section not in self._config.sections():
                raise MissingConfigurationSection(missing_section=section)

    def get_aws_rds_host(self):
        return self._config.get(ConfigurationConstants.AWS_RDS_SECTION, ConfigurationConstants.AWS_RDS_HOST)

    def get_aws_rds_port(self):
        return self._config.get(ConfigurationConstants.AWS_RDS_SECTION, ConfigurationConstants.AWS_RDS_PORT)

    def get_aws_rds_username(self):
        return self._config.get(ConfigurationConstants.AWS_RDS_SECTION, ConfigurationConstants.AWS_RDS_USERNAME)

    def get_aws_rds_password(self):
        return self._config.get(ConfigurationConstants.AWS_RDS_SECTION, ConfigurationConstants.AWS_RDS_PASSWORD)

    def get_aws_rds_db_name(self):
        return self._config.get(ConfigurationConstants.AWS_RDS_SECTION, ConfigurationConstants.AWS_RDS_DB_NAME)

    def get_scraper_configs(self):
        scraper_config = dict()
        for section in ConfigurationConstants.SCRAPERS:
            scraper_config[section] = dict(self._config.items(section))
        return scraper_config


class ConfigurationManager(object):

    config = None

    @staticmethod
    def get_config():

        if ConfigurationManager.config is None:
            if ConfigurationConstants.CONFIGURATION_FILE_ENV_VAR not in os.environ:
                print("Configuration file not found.")
            else:
                ConfigurationManager.config = Configuration(configuration_file=os.environ[
                    ConfigurationConstants.CONFIGURATION_FILE_ENV_VAR
                ])

        return ConfigurationManager.config
