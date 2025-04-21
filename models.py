import sqlalchemy as sq
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
