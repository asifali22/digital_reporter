import typing

from digital_reporter.modules.db.models import Scraper
from digital_reporter.modules.db.managers.MySQL import MySQLManager
from digital_reporter.modules.utilities.configurations.configuration_manager import ConfigurationManager

if typing.TYPE_CHECKING:
    from digital_reporter.modules.utilities.configurations.configuration_manager import Configuration


def dump_to_scraperdb(data, db_session):

    config: "Configuration" = ConfigurationManager.get_config()

    assert data["headline"] is not None
    f = Scraper(rss_feed_id=data["rss_feed_id"],
                uri=data["uri"]["link"],
                headline=data["headline"],
                story_kicker=data["story_kicker"],
                article=data["article"])
    try:
        db_session.add(f)
        db_session.flush()
        db_session.commit()
    except:
        db_session.rollback()
    finally:
        db_session.close()
