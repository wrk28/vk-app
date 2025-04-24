import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User_VKinder(Base):
    __tablename__ = 'User'
    id_user = sq.Column(sq.String, primary_key=True)
    age = sq.Column(sq.Integer, nullable=True)
    sex = sq.Column(sq.Integer, nullable=True)
    city_id = sq.Column(sq.Integer, nullable=True)
    offset = sq.Column(sq.Integer, nullable=False, defeult=0)


class Requests(Base):
    __tablename__ = 'Requests'

    requests_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=False, nullable=False)
    surname = sq.Column(sq.String(length=80), unique=False, nullable=False)
    age = sq.Column(sq.Integer, unique=False, nullable=False)
    sex = sq.Column(sq.String(length=20), unique=False, nullable=False)
    city = sq.Column(sq.String(length=80), unique=False, nullable=False)
    link = sq.Column(sq.String(length=80), unique=False, nullable=False)

class User_requests(Base):
    __tablename__= 'User_requests'

    requests_user_id = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('User_VKinder'), nullable=False)
    requests_id = sq.Column(sq.Integer, sq.ForeignKey('Requests'), nullable=False)

    user = relationship(User_VKinder, backref='User_requests')
    req = relationship(Requests, backref= 'User_requests')


class Photos(Base):
    __tablename__ = 'Photos'

    photos_id= sq.Column(sq.Integer, primary_key=True)
    requests_id = sq.Column(sq.Integer, sq.ForeignKey('Requests'), nullable=False)
    photo_url = sq.Column(sq.String(length=80), unique=False, nullable=False)

    req = relationship(User_requests, backref='Photos')


