"""
Date: 05/08/2020
Author: adarshtri

This is the base parsing class. It's an abstract class. The class follows template
design pattern. The parse method calls all the chain of methods. Each abstract method(called inside parse() method
are implemented by the child classes.
"""

from digital_reporter.modules.parsers.constants import ParseConstants
from abc import ABC, abstractmethod
import feedparser
from digital_reporter.custom_exceptions import *
import time

from digital_reporter.modules.scraper.drivers import ChromeDriverManager
from digital_reporter.modules.scraper.base import Scapper
from digital_reporter.modules.scraper.models.scraper import dump_to_scraperdb
from digital_reporter.modules.db.managers.MySQL import MySQLManager
from digital_reporter.modules.utilities.configurations.configuration_manager import ConfigurationManager
from digital_reporter.modules.notifications.slack import SlackNotifier

class BaseParser(ABC):

    """
    Base parsing class.
    """

    def __init__(self, **kwargs):
        self._arguments = kwargs
        self._check_compulsory_parameters()
        self._source_id_scrapper_config_map = dict()

    def _check_compulsory_parameters(self):
        """
        Checks whether the compulsory parameters are present or not. If not raises exception.
        Also checks the type of received parameters. If incorrect assertion fails.
        :return: None
        """

        for param in ParseConstants.COMPULSORY_PARSER_PARAMETERS:
            if param not in self._arguments:
                raise MissingCompulsoryArguments(missing_argument=param)

            assert isinstance(self._arguments[param], ParseConstants.PARAMETER_TYPES[param]), \
                'Wrong type. Parameter \"{}\" should be of type \"{}\".'.format(param,
                                                                                ParseConstants.PARAMETER_TYPES[param])

    def parse(self):
        """
        The template function that defines the template for parsing any feed.
        :return: None
        """

        news_feed = self.get_news_feed_from_url()
        latest_feed, latest_time_recorded = self.get_latest_feed(news_feed)
        formatted_feed = self.get_formatted_feeds(latest_feed)
        link_details_for_scrapping = self.create_new_records_from_formatted_feeds(formatted_feed)
        self.scrap_links(link_details_for_scrapping)
        self.update_last_recorded_time(latest_time_recorded)

    def get_news_feed_from_url(self) -> dict:
        """
        Extract url from kwargs from init methods. Hits the url and returns the feed.
        :return: The feeds from the url.
        """

        all_feeds = {'entries': []}

        for url in self._arguments[ParseConstants.URL_KEY]:
            feed = feedparser.parse(url['url'])
            for entry in feed.entries:
                entry['source'] = url['url']
                self._source_id_scrapper_config_map[url['url']] = url['scrapper_config']
                all_feeds['entries'].append(entry)

        return all_feeds

    def get_latest_feed(self, feed):
        """
        Extracts time from kwargs. Compares feed with latest timestamp in record
        and filters old news feed.
        :param feed: News feed extracted from url
        :return: Filtered feeds.
        """
        latest_feed = []
        latest_published_time = self._arguments[ParseConstants.LATEST_PUBLISHED_TIME]
        next_latest_time = latest_published_time

        if feed:
            for entry in feed['entries']:
                try:
                    if time.mktime(entry.published_parsed) > latest_published_time:
                        latest_feed.append(entry)
                        if time.mktime(entry.published_parsed) > next_latest_time:
                            next_latest_time = time.mktime(
                                entry.published_parsed)
                except Exception as e:
                    print("Invalid entry in feed.")
        else:
            return [], next_latest_time
        return latest_feed, next_latest_time

    def scrap_links(self, link_config_map):
        """
        Each rss feed has set of links to be scrapped. This functions is passed a generator object with
        those links and the respective url to get scrapper config. Call the base scrapper and wait for
        the magic.
        :param link_config_map: Generator object, containing the link to be scrapped and the url of source
        to get the scrapper config.
        :return: Give me some time to decide. Update if you see anything getting returned and not mentioned
        here.
        """
        driver = ChromeDriverManager()
        config = ConfigurationManager.get_config()
        mysql_manager = MySQLManager(host=config.get_aws_rds_host(),
                                     port=config.get_aws_rds_port(),
                                     username=config.get_aws_rds_username(),
                                     pwd=config.get_aws_rds_password(),
                                     db_name=config.get_aws_rds_db_name())

        S = mysql_manager.get_session()
        s = S()

        for source_url, link, link_id in link_config_map:
            try:
                scrapper_config = self._source_id_scrapper_config_map[source_url]
                wait_driver = driver.get_waiter_driver(link['link'])
                scraper = Scapper(uri=link, config=scrapper_config, wait_driver=wait_driver, link_id=link_id)
                dump_to_scraperdb(data=scraper.get_data(), db_session=s)
            except Exception as e:
                print("Something went wrong with scraping rss links or dumping them to database.")


    @abstractmethod
    def get_formatted_feeds(self, latest_feed):
        """
        Each rss source can have different fields from the feed. This method brings all the feeds to
        single required format for backend.
        :param latest_feed: Latest feed from get_latest_feed method.
        :return: Formatted feed. Format can be anything. Might want to stick to one.
        """
        pass

    @abstractmethod
    def create_new_records_from_formatted_feeds(self, formatted_feed):
        """
        After getting the formatted feed write the data to the sink.
        :param formatted_feed: Formatted feed received from get_formatted_feeds method.
        :return: Could be write status. For now not decided.
        """
        pass

    @abstractmethod
    def update_last_recorded_time(self, latest_time_recorded):
        """
        After writing to sink our last date of feed will update to new value.
        Update that in your backend.
        :param latest_time_recorded: New latest time.
        :return: Could be update status. For now not decided.
        """
        pass

    @abstractmethod
    def check_child_class_parameters(self):
        """
        This is an abstract method. All the child class should implement this.
        This method helps in identifying class specific parameters.
        Can have implementation similar to compulsory checker of base parse class.
        :return: None
        """
        pass
