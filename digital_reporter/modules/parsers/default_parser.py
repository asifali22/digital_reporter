import time


from digital_reporter.modules.parsers.base_parser import BaseParser
from digital_reporter.modules.parsers.constants import ParseConstants
from digital_reporter.custom_exceptions import *
from digital_reporter.modules.db.models import *
from config import current_config

sqlalchemy_engine = current_config.cron_db_engine

class DefaultParser(BaseParser):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._output_file = None
        self._last_time_file = None

        self.check_child_class_parameters()

    def get_formatted_feeds(self, feeds):

        json_feeds = []

        for feed in feeds:
            current_feed = {}

            if "source" in feed:
                current_feed["source_url"] = feed["source"]

            if "title" in feed:
                current_feed["title"] = feed["title"]

            if "link" in feed:
                current_feed["link"] = feed["link"]

            if "links" in feed:
                link_list = []
                for link in feed["links"]:
                    if "href" in link:
                        current_link = dict()
                        current_link["link"] = link["href"]
                        link_list.append(current_link)

                if link_list:
                    current_feed["links"] = link_list

            if "summary" in feed:
                current_feed["summary"] = feed["summary"]

            if "published" in feed:
                current_feed["published"] = feed["published"]

            if "published_parsed" in feed:
                current_feed["published_parsed"] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', feed["published_parsed"])

            json_feeds.append(current_feed)

        return json_feeds

    def create_new_records_from_formatted_feeds(self, formatted_feed):


        for i, feed in enumerate(formatted_feed):
            f = RSSFeed(source_url=feed["source_url"],
                        title=feed["title"],
                        summary=feed["summary"],
                        link=feed["link"],
                        published_string=feed["published"],
                        published_at=feed["published_parsed"])
            sqlalchemy_engine.add(f)
            sqlalchemy_engine.flush()
            sqlalchemy_engine.refresh(f)

            try:
                foreign_key = f.id
                link_to_be_forwarded_for_scrapping = []
                for link in feed["links"]:
                    l = RSSFeedLink(rss_feed_id=foreign_key,
                                    rss_feed_link=link["link"])
                    sqlalchemy_engine.add(l)
                    sqlalchemy_engine.flush()
                    sqlalchemy_engine.refresh(l)
                    link_to_be_forwarded_for_scrapping.append((feed["source_url"], link, l.id))
                sqlalchemy_engine.commit()
                for link_details in link_to_be_forwarded_for_scrapping:
                    yield link_details
            except:
                sqlalchemy_engine.rollback()
            finally:
                sqlalchemy_engine.close()

    def update_last_recorded_time(self, latest_time_recorded):
        if latest_time_recorded != self._arguments[ParseConstants.LATEST_PUBLISHED_TIME]:
            last_time = RSSLastTime(last_time=latest_time_recorded)
           
            sqlalchemy_engine.add(last_time)
            sqlalchemy_engine.commit()
            sqlalchemy_engine.close()

    def check_child_class_parameters(self):
        for param in ParseConstants.DEFAULT_PARSER_PROPERTIES:
            if param not in self._arguments[ParseConstants.CUSTOM_PARSER_PROPERTIES]:
                raise MissingDefaultParserArguments(missing_argument=param)
