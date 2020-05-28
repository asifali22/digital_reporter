import argparse
from digital_reporter.modules.utilities.configurations.configuration_manager import ConfigurationConstants, ConfigurationManager
import os


def get_configuration_parameters():

    parser = argparse.ArgumentParser()

    parser.add_argument('--config',
                        required=True,
                        help="Configuration file for running parser.",
                        dest="config",
                        type=str)

    parameters = parser.parse_args()
    return parameters.config


# def main():
#     configuration_file = get_configuration_parameters()
#     os.environ[ConfigurationConstants.CONFIGURATION_FILE_ENV_VAR] = configuration_file
#     config = ConfigurationManager.get_config()

#     from digital_reporter.modules.parsers.default_parser import DefaultParser
#     import digital_reporter.modules.db.models as models
#     from digital_reporter.modules.db.managers.MySQL import MySQLManager

#     mysql_manager = MySQLManager(host=config.get_aws_rds_host(),
#                                  port=config.get_aws_rds_port(),
#                                  username=config.get_aws_rds_username(),
#                                  pwd=config.get_aws_rds_password(),
#                                  db_name=config.get_aws_rds_db_name())

#     S = mysql_manager.get_session()
#     s = S()
#     last_time_row = s.query(models.RSSLastTime).order_by(
#         models.RSSLastTime.id.desc()).first()
#     rss_urls = s.query(models.RSSSource)
#     urls = []
#     for rss_url in rss_urls:
#         scrapper_config_id = rss_url.scrapper_config_id
#         scrapper_config_model_object = s.query(models.ScrapperConfiguration).filter(
#             models.ScrapperConfiguration.id == scrapper_config_id).first()
#         entry = {
#             'url': rss_url.url,
#             'scrapper_config': scrapper_config_model_object.__dict__,
#             'id': rss_url.id
#         }
#         urls.append(entry)
#     s.close()

#     default_parser = DefaultParser(url=urls,
#                                    latest_published_time=last_time_row.last_time,
#                                    custom_parser_params={})
#     default_parser.parse()

def main():
    print("Cron executed")
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get('https://www.indiatoday.in/india/story/18-day-old-baby-defeats-coronavirus-in-mumbai-1682866-2020-05-28')
    waitdriver = WebDriverWait(driver, 5)
    text = waitdriver.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).get_attribute("textContent")
    print(text)
    driver.quit()

if __name__ == "__main__":
    main()
