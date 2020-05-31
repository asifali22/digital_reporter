import os
import typing as t
import logging
import pickle
import json

import requests
from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger(__name__)


def load_from_file(filepath, mode='r'):
    with open(filepath, mode) as fin:
        content = fin.read()
    return content


class Config:
    DEBUG = True
    TESTING = True

    LOG_FORMAT_DEFAULT = os.environ.get(
        "LOG_FORMAT_DEFAULT",
        "[%(levelname)s]|%(name)s|%(asctime)s|%(module)s|%(funcName)s|%(lineno)d|%(message)s",
    )

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    VERSION = load_from_file('VERSION', 'r')

    # logging configuration
    logging.basicConfig(level=LOG_LEVEL,
                        format=LOG_FORMAT_DEFAULT)

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

    DRIVER_PATH = os.environ.get("DRIVER_PATH", "/usr/local/bin/chromedriver")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=chrome_options)

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    cron_db_engine = sessionmaker(bind=engine)()


class TestConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


CONFIGS = {"test": TestConfig, "staging": StagingConfig,
           "production": ProductionConfig}


current_config: Config = CONFIGS[os.environ.get("ENV", "test")]
