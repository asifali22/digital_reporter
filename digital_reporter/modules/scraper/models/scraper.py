import typing

from digital_reporter.modules.db.models import Scraper
from config import current_config

sqlalchemy_engine = current_config.cron_db_engine

def dump_to_scraperdb(data, db_session=sqlalchemy_engine):

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
