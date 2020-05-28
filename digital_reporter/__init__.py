import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlalchemy

from config import CONFIGS, current_config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None, config=CONFIGS):
    if not config_name:
        config_name = os.environ.get("ENV", "test")

    assert config_name in config.keys(
    ), f"'{config_name}' must be one of {config!r}"

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # initialize flask extensions
    db.init_app(app)
    # jwt.init_app(app)
    migrate.init_app(app, db)

    # Imports for migration
    from digital_reporter.modules.db.models import (RSSSource, RSSFeed, RSSFeedLink, RSSLastTime, ScrapperConfiguration, Scraper)

    # register API routes
    from digital_reporter.modules.api.health_check import health_blueprint

    app.register_blueprint(health_blueprint)

    return app
