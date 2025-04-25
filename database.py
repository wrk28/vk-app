import sqlalchemy as sq
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from models import User, Requests, User_requests, Photos
import models as m


class DB_Utils:

    def __init__(self, base, dsn) -> None:
        self.base = base
        self.engine = sq.create_engine(dsn)
        self.Session = sessionmaker(bind=self.engine)


    def close(self):
        self.Session.close_all()


    def get_offset(self, user_id: str) -> int:
        with self.Session() as session:
            result = session.query(User.offset).filter(User.user_id == user_id).one_or_none()[0]
            session.execute(sq.update(User).where(User.user_id==user_id).values(offset=User.offset+1))
            session.commit()
        return result
    

    def get_last_requests_id(self, user_id: str) -> int:
        with self.Session() as session:
            offset = session.query(User.offset).filter(User.user_id == user_id).one_or_none()[0]
            requests_id = session.query(User_requests.requests_id).\
                filter(User_requests.user_id == user_id, User_requests.number == offset).one_or_none()[0]
        return requests_id
    

    def get_requests_name(self, requests_id: str) -> tuple:
        with self.Session() as session:
            name = session.query(Requests.first_name, Requests.last_name).\
                filter(Requests.requests_id == requests_id).one_or_none()
        return name
    

    def check_user(self, user_id: str) -> bool:
        with self.Session() as session:
            result = session.query(User).filter(User.user_id == user_id).one_or_none()
        return True if result else False


    def add_user(self, user_info: dict) -> None:
        user_id = user_info['user_id']
        city_id = user_info['city_id']
        sex = user_info['sex']
        age = user_info['age']
        with self.Session() as session:
            new_user = User(user_id=user_id, city_id=city_id, sex=sex, age=age)
            session.add(new_user)
            session.commit()


    def get_favourites(self, user_id: str) -> list:
        with self.Session() as session:
            result = session.query(Requests.requests_id, 
                                   Requests.first_name, 
                                   Requests.last_name, 
                                   Requests.link). \
                join(User_requests, User_requests.requests_id==Requests.requests_id).\
                    filter(User_requests.user_id==user_id, User_requests.favorite_list==1).all()
        favourites = []
        for item in result:
            favourites.append(dict(zip(["id", "first_name", "last_name", "link"], item)))
        return favourites


    def create_database(self) -> None:
        self.base.metadata.create_all(self.engine)


    def remove_database(self) -> None:
        self.base.metadata.drop_all(self.engine)


    def add_requests(self, user_id: str, account: dict):
        requests_id = account.get('id')
        first_name = account.get('first_name')
        last_name = account.get('last_name')
        sex = account.get('sex')
        age = account.get('age')
        city_id = account.get('city_id')
        link = f'https://vk.com/id{account.get("id")}'
        
        with self.Session() as session:
            result = session.query(m.Requests.requests_id).filter(Requests.requests_id==requests_id).all()
            if not result:
                new_requests = m.Requests(requests_id=requests_id, 
                                          first_name=first_name, 
                                          last_name=last_name, 
                                          sex=sex, 
                                          age=age, 
                                          city_id=city_id, 
                                          link=link)
                session.add(new_requests)
                session.commit()
            self.add_user_requests(user_id=user_id, requests_id=requests_id)


    def add_user_requests(self, user_id: str, requests_id: str) -> None:
        with self.Session() as session:
            result = session.query(m.User_requests.requests_id).filter(User_requests.user_id == user_id, 
                                                                       User_requests.requests_id==requests_id).one_or_none()
            if not result:
                count = session.query(func.count(User_requests.user_id)).filter(User_requests.user_id==user_id).scalar() + 1
                new_user_requests = m.User_requests(user_id=user_id, requests_id=requests_id, number=count)
                session.add(new_user_requests)
                session.commit()


    def add_favorite(self, user_id, requests_id):
        with self.Session() as session:
            session.execute(sq.update(m.User_requests). \
                            where(m.User_requests.user_id == user_id, m.User_requests.requests_id == requests_id). \
                                values(favorite_list = 1))
            session.commit()


    def add_photos(self, requests_id: str, photos: list):
        with self.Session() as session:
            for photo in photos:
                photo = m.Photos(requests_id=requests_id, 
                                 owner_id=photo.get('owner_id'),
                                 media_id=photo.get('media_id'),
                                 access_key=photo.get('access_key'),
                                 photo_url=photo.get('url'))
                session.add(photo)
                session.commit()
    

    def get_requests_photos(self, request_id: str) -> list:
        with self.Session() as session:
            result = session.query(Photos.owner_id, Photos.media_id, Photos.access_key). \
                    filter(Photos.requests_id==request_id).all()
        photos = []
        for item in result:
            photos.append(dict(zip(["owner_id", "media_id", "access_key"], item)))
        return photos