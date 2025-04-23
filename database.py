import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Base
from config import settings


class DB_Utils:

    def __init__(self, base, dsn):
        self.base = base
        self.engine = sq.create_engine(dsn)
        self.Session = sessionmaker()
        self.session = None

    def _start_session(self):
        self.session = self.Session()

    def _close_session(self):
        if self.session:
            self.session.close()
        self.session = None

    def get_offset(self, user_id: str) -> int:
        # Ищет в базе пользователя с user_id, если не находит, то создаёт и устанавливает значения поля offset
        # равным 0, если находит, то увеличивает значение offset на 1. В обоих случаях возвращает offset до увеличения
        return None

    def create_database(self):
        self.base.metadata.create_all(self.engine)

    def remove_database(self):
        self.base.metadata.drop_all(self.engine)

    def close(self):
        self._close_session()


db_utils = DB_Utils(base=Base, dsn=settings.dsn)