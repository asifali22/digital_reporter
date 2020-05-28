from digital_reporter.modules.db.managers.MySQL import MySQLManager
import argparse
from digital_reporter.modules.utilities.configurations.configuration_manager import ConfigurationManager, Configuration
import digital_reporter.modules.utilities.configurations.set_conf_env as sce


def get_params():

    parser = argparse.ArgumentParser()

    parser.add_argument('--config',
                        dest='config',
                        required=True,
                        type=str)

    parser.add_argument('--url',
                        dest='url',
                        required=True,
                        type=str)

    arg_params = parser.parse_args()
    url, config = arg_params.url, arg_params.config
    sce.set_conf_env_file(config)
    config = ConfigurationManager.get_config()
    return url, config


def get_db_session(config: Configuration):

    db_manager = MySQLManager(host=config.get_aws_rds_host(),
                              port=config.get_aws_rds_port(),
                              username=config.get_aws_rds_username(),
                              pwd=config.get_aws_rds_password(),
                              db_name=config.get_aws_rds_db_name())

    Session = db_manager.get_session()
    session = Session()
    return session


def main():
    url, config = get_params()
    session = get_db_session(config)

    from digital_reporter.modules.db.models import RSSSource

    rss_source = RSSSource(url=url)
    session.add(rss_source)
    session.commit()


if __name__ == "__main__":
    main()