import typing
from datetime import datetime
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException



class Scapper:

    def __init__(self, uri, config, wait_driver, link_id):

        self.uri = uri
        self.wait_driver = wait_driver
        self._headline = None
        self._story_kicker = None
        self._article = []
        self._config = dict()
        #self.scraper_name = scraper_name
        self.response = dict()
        self._config = config
        self.scraper_name = config["scrapper_name"]
        self.link_id = link_id

        self.with_rss_uri()  # fix for indiatoday - later will have diferent class for each scraper

        # self.load_config(scraper_name=self.scraper_name)

    @property
    def headline(self):
        return self._headline

    @property
    def story_kicker(self):
        return self._story_kicker

    @property
    def article(self):
        return self._article

    @headline.setter
    def headline(self, headline_text):
        self._headline = headline_text

    @story_kicker.setter
    def story_kicker(self, story_kicker_text):
        self._story_kicker = story_kicker_text

    @article.setter
    def article(self, article_data):
        self._article = article_data

    def post_process(self, data):
        data["scraper_name"] = self.scraper_name
        return data

    def get_data(self):
        if self.response == dict():
            self.set_data()
            self.response = self.post_process(data=self.response)
            self.response["rss_feed_id"] = self.link_id
            return self.response
        else:
            return self.response

    def set_data(self) -> str:
        config = self._config
        _map = {
            "headline": self.headline,
            "story_kicker": self.story_kicker,
            "article": self.article
        }
        _field_map = {
            "CSS_SELECTOR": By.CSS_SELECTOR,
            "TAG_NAME": By.TAG_NAME
        }
        response = dict(uri=self.uri)
        for kind in _map.keys():
            try:
                if kind is "article":
                    by, attribute_name, child_tag = config[kind].split(",")
                    element = self.wait_driver.until(
                        EC.presence_of_element_located((_field_map[by], attribute_name)))
                    if child_tag != "":
                        childs = element.find_elements_by_tag_name(child_tag)
                        article = [child.get_attribute("textContent").strip() for child in childs if len(
                            child.get_attribute("textContent").strip())]
                        article = "\n\n".join(
                            article) if article is not None else None
                        _map[kind] = article
                        response[kind] = _map[kind]
                    else:
                        article = element.text
                        _map[kind] = "".join(
                            article) if article is not None else None
                        response[kind] = _map[kind]
                else:
                    by, attribute_name = config[kind].split(",")
                    element = self.wait_driver.until(
                        EC.presence_of_element_located((_field_map[by], attribute_name)))
                    _map[kind] = element.get_attribute("textContent")
                    response[kind] = _map[kind]
            except TimeoutException as exec:
                response[kind] = None
        self.response = response
        return self

    @staticmethod
    def format_datetime(date_string: str, format="%B %d, %Y %H:%M %Z") -> datetime:
        if not date_string:
            return None

        def format_date(f_date, d_string):
            if f_date[0] == ":":
                d_string = d_string[1:].strip()
            else:
                d_string = d_string.strip()
            local_datetime = datetime.strptime(
                d_string, format)
            local_datetime_timestamp = float(local_datetime.strftime("%s"))
            UTC_datetime = datetime.utcfromtimestamp(local_datetime_timestamp)
            return UTC_datetime

        index = None
        formatted_date = date_string.lower()
        try:
            index = formatted_date.index("updated")
        except ValueError as e:
            formatted_date = formatted_date.strip()
            if len(formatted_date):
                date_string = date_string.strip()
                return format_date(formatted_date, date_string)
        else:
            index = index + len("updated")
            formatted_date = formatted_date[index:]
            date_string = date_string[index:]
            return format_date(formatted_date, date_string)

    def with_rss_uri(self, part_of_uri="?utm_source=rss"):
        index = None
        try:
            index = self.uri.index(part_of_uri)
        except ValueError as e:
            # part of uri not present
            return self
        else:
            self.uri = self.uri[:index]
        return self

    def __repr__(self):
        return '<{class_name}(scraper_name={scraper_name}, uri={uri})>'.format(
            class_name=self.__class__.__name__,
            scraper_name=self.scraper_name,
            uri=self.uri
        )
