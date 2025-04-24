import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User_VKinder(Base):
    __tablename__ = 'User_VKinder'

    id_user = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=False)
    age = sq.Column(sq.Integer, unique=False)
    sex = sq.Column(sq.String(length=20), unique=False)
    city = sq.Column(sq.String(length=80), unique=False)


class Requests(Base):
    __tablename__ = 'Requests'

    requests_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=False)
    surname = sq.Column(sq.String(length=80), unique=False)
    age = sq.Column(sq.Integer, unique=False)
    sex = sq.Column(sq.String(length=20), unique=False)
    city = sq.Column(sq.String(length=80), unique=False)
    link = sq.Column(sq.String(length=80), unique=False)

class User_requests(Base):
    __tablename__= 'User_requests'

    requests_user_id = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('User_VKinder'))
    requests_id = sq.Column(sq.Integer, sq.ForeignKey('Requests'))
    favorite_list = sq.Column(sq.Integer, unique=False, default=0)
    black_list = sq.Column(sq.Integer, unique=False, default=0)

    user = relationship(User_VKinder, backref='User_requests')
    req = relationship(Requests, backref= 'User_requests')


class Photos(Base):
    __tablename__ = 'Photos'

    photos_id= sq.Column(sq.Integer, primary_key=True)
    requests_id = sq.Column(sq.Integer, sq.ForeignKey('Requests'), nullable=False)
    photo_url = sq.Column(sq.String(length=80), unique=False, nullable=False)

    req = relationship(User_requests, backref='Photos')