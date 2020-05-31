import argparse
import os

from config import current_config
from digital_reporter.modules.parsers.default_parser import DefaultParser
import digital_reporter.modules.db.models as models


sqlalchemy_engine = current_config.cron_db_engine

def main():

    last_time_row = sqlalchemy_engine.query(models.RSSLastTime).order_by(
        models.RSSLastTime.id.desc()).first()

    rss_urls = sqlalchemy_engine.query(models.RSSSource)
    urls = []
    for rss_url in rss_urls:
        scrapper_config_id = rss_url.scrapper_config_id
        scrapper_config_model_object = sqlalchemy_engine.query(models.ScrapperConfiguration).filter(
            models.ScrapperConfiguration.id == scrapper_config_id).first()
        entry = {
            'url': rss_url.url,
            'scrapper_config': scrapper_config_model_object.__dict__,
            'id': rss_url.id
        }
        urls.append(entry)

    if last_time_row:
        default_parser = DefaultParser(url=urls,
                                   latest_published_time=last_time_row.last_time,
                                   custom_parser_params={})
    else:
        default_parser = DefaultParser(url=urls,
                                   latest_published_time=0.0,
                                   custom_parser_params={})
    
    default_parser.parse()


if __name__ == "__main__":
    main()
