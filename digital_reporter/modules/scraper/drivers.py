from digital_reporter.modules.utilities.designs.singleton import singleton
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


@singleton
class ChromeDriverManager(object):

    def __init__(self):

        # part of dummy config

        class CurrentConfig:
            driver = webdriver.Chrome(executable_path="chromedriver_mac64/chromedriver")

        self.driver = CurrentConfig.driver

    def get_waiter_driver(self, uri):

        """
        returns wait driver for the uri
        :param uri: uri
        :return: WaitDriver
        """

        self.driver.get(uri)
        wait_driver = WebDriverWait(self.driver, 10)
        return wait_driver

x = ChromeDriverManager()
