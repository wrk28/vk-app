import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    user_id = sq.Column(sq.BigInteger, primary_key=True)
    age = sq.Column(sq.Integer)
    sex = sq.Column(sq.Integer)
    city_id = sq.Column(sq.Integer)
    offset = sq.Column(sq.Integer, nullable=False, default=0)


class Requests(Base):
    __tablename__ = 'Requests'

    requests_id = sq.Column(sq.BigInteger, primary_key=True)
    first_name = sq.Column(sq.String(length=80))
    last_name = sq.Column(sq.String(length=80))
    age = sq.Column(sq.Integer)
    sex = sq.Column(sq.Integer)
    city_id = sq.Column(sq.Integer)
    link = sq.Column(sq.String(length=160))


class User_requests(Base):
    __tablename__= 'User_requests'
    
    user_id = sq.Column(sq.BigInteger, sq.ForeignKey('User.user_id'), primary_key=True)
    requests_id = sq.Column(sq.BigInteger, sq.ForeignKey('Requests.requests_id'), primary_key=True)
    number = sq.Column(sq.BigInteger, default=0)
    favorite_list = sq.Column(sq.Integer, default=0)

    User = relationship(User, backref='User_requests')
    Requests = relationship(Requests, backref= 'User_requests')


class Photos(Base):
    __tablename__ = 'Photos'

    photos_id= sq.Column(sq.Integer, primary_key=True)
    requests_id = sq.Column(sq.Integer, sq.ForeignKey('Requests.requests_id'), nullable=False)
    photo_url = sq.Column(sq.String(length=1000), nullable=False)

    Requests = relationship(Requests, backref='Photos')