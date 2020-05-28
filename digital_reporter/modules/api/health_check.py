from flask import current_app, Blueprint

from digital_reporter.enumstore import APIRouteNames



health_blueprint = Blueprint("health", __name__)


@health_blueprint.route(APIRouteNames.HEALTH.value, methods=("GET",))
def health():
    sqlalchemy_engine = current_app.extensions["sqlalchemy"].db.get_engine()
    sqlalchemy_db_result = sqlalchemy_engine.execute("SELECT 1").first()[0]
    return {
        "status": "ok",
        "version": current_app.config["VERSION"],
        "database": "ok" if sqlalchemy_db_result == 1 else "unknown"
    }
