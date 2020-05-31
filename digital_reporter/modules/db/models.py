from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, VARCHAR, DECIMAL
import datetime
import sqlalchemy.dialects.mysql as mysql_t
from sqlalchemy.sql.functions import current_timestamp
from digital_reporter import db


class RSSSource(db.Model):
    __tablename__ = 'rss_source'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    scrapper_config_id = db.Column(BigInteger, ForeignKey(
        'scrapper_config.id', ondelete='CASCADE', onupdate='CASCADE'
    ), nullable=True)
    url = db.Column(VARCHAR(3000), unique=True)
    created_at = db.Column(mysql_t.TIMESTAMP(
        fsp=6), nullable=False, server_default=current_timestamp(6))


class RSSFeed(db.Model):
    __tablename__ = 'rss_feed'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    source_url = db.Column(VARCHAR(3000), ForeignKey(
        'rss_source.url', onupdate='CASCADE', ondelete='CASCADE'))
    link = db.Column(mysql_t.MEDIUMTEXT())
    title = db.Column(mysql_t.MEDIUMTEXT())
    summary = db.Column(mysql_t.LONGTEXT())
    published_string = db.Column(mysql_t.MEDIUMTEXT())
    published_at = db.Column(DateTime, default=None)
    created_at = db.Column(mysql_t.TIMESTAMP(
        fsp=6), nullable=False, server_default=current_timestamp(6))


class RSSFeedLink(db.Model):
    __tablename__ = 'rss_feeds_link'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    rss_feed_id = db.Column(BigInteger, ForeignKey(
        'rss_feed.id', onupdate='CASCADE', ondelete='CASCADE'))
    rss_feed_link = db.Column(mysql_t.MEDIUMTEXT(), nullable=False)
    created_at = db.Column(mysql_t.TIMESTAMP(
        fsp=6), nullable=False, server_default=current_timestamp(6))


class RSSLastTime(db.Model):
    __tablename__ = 'rss_last_time'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    last_time = db.Column(DECIMAL)
    created_at = db.Column(mysql_t.TIMESTAMP(
        fsp=6), nullable=False, server_default=current_timestamp(6))


class ScrapperConfiguration(db.Model):
    __tablename__ = 'scrapper_config'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    scrapper_name = db.Column(mysql_t.TEXT(), nullable=False)
    headline = db.Column(mysql_t.MEDIUMTEXT(), nullable=True)
    date_time = db.Column(mysql_t.TEXT(), nullable=True)
    article = db.Column(mysql_t.LONGTEXT(), nullable=True)
    story_kicker = db.Column(mysql_t.MEDIUMTEXT(), nullable=True)
    created_at = db.Column(mysql_t.TIMESTAMP(
        fsp=6), nullable=False, server_default=current_timestamp(6))


class Scraper(db.Model):
    __tablename__ = 'rss_feed_scrapped'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    # not sure if required now the below field
    # scraper_name = db.Column(mysql_t.TEXT(), nullable=False)
    rss_feed_id = db.Column(BigInteger, ForeignKey(
        'rss_feed.id', onupdate='CASCADE', ondelete='CASCADE'))
    uri = db.Column(mysql_t.MEDIUMTEXT(), nullable=False)
    headline = db.Column(mysql_t.MEDIUMTEXT(), nullable=False)
    story_kicker = db.Column(mysql_t.MEDIUMTEXT())
    article = db.Column(mysql_t.LONGTEXT())
    created_at = db.Column(mysql_t.TIMESTAMP(
        fsp=6), nullable=False, server_default=current_timestamp(6))
    # not that important in the context
    # updated_at = db.Column(mysql_t.TIMESTAMP(fsp=6), nullable=False,
    #                     server_default=current_timestamp(6), server_onupdate=current_timestamp(6))

    def __repr__(self):
        return {
            'id': self.id,
            'rss_feed_id': self.rss_feed_id,
            'uri': self.uri,
            'headline': self.headline,
            'story_kicker': self.story_kicker,
            'article': self.article,
            'created_at': self.created_at
        }
