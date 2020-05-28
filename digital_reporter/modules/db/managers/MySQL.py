from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MySQLManager(object):

    def __init__(self, host: str, port: str, username: str, pwd: str, db_name: str):
        self._host = host
        self._port = port
        self._username = username
        self._pwd = pwd
        self._db_name = db_name

        self._engine = None
        self._session = None

        self._set_engine()

    def _set_engine(self):

        self._engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".
                                     format(self._username, self._pwd, self._host, self._port, self._db_name))

    def get_engine(self):
        return self._engine

    def get_session(self):
        engine = self.get_engine()
        new_session = sessionmaker(bind=engine)
        return new_session
