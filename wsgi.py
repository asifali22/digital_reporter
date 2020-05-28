import os

from digital_reporter import create_app

application = app = create_app(os.environ.get("ENV", "test"))
