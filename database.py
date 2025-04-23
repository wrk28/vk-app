import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Base
from config import settings
import models as m

class DB_Utils:

    def __init__(self, base, dsn) -> None:
        self.base = base
        self.engine = sq.create_engine(dsn)
        self.Session = sessionmaker()
        self.session = None

    def _start_session(self) -> None:
        self.session = self.Session()

    def _close_session(self) -> None:
        if self.session:
            self.session.close()
        self.session = None

    def get_offset(self, user_id: str) -> int:
        # Ищет в базе пользователя с user_id, если не находит, то создаёт и устанавливает значения поля offset
        # равным 0, если находит, то увеличивает значение offset на 1. В обоих случаях возвращает offset до увеличения
        return None
    
    def check_user(self, user_id: str) -> bool:
        pass

    def create_database(self) -> None:
        self.base.metadata.create_all(self.engine)

    def remove_database(self) -> None:
        self.base.metadata.drop_all(self.engine)

    def close(self) -> None:
        self._close_session()

    def add_user(self, user_info: dict) -> None:
        '''
        Функция добавляет пользователя в базу данных.
        В данном случае user_vkinder - это пользователь, который ищет пару.
        Для простоты будем называть его "пользователь"
        :param id_user: id пользовател
        :param name: имя пользователя.
        :param surname: имя пользователя.
        :param sex: пол пользователя. 1 - женский, 2 - мужской
        :param age: возраст пользователя
        :param city: город пользователя
        '''

        # with self.session as session:
        #     user_find = session.query(m.User_VKinder.id_user).all()
        #     if id_user not in [user[0] for user in user_find]:
        #         user = m.User_VKinder(id_user=id_user, name=name, surname=surname, age=age,
        #                               sex=sex,  city=city)
        #         session.add(user)
        #         session.commit()

    def add_requests(self, user_id, requests_id, name, surname, age, sex, city, link):
        '''
        Функция добавляет запрос в базу данных.
        В данном случае requests - это предложенный пользователю человек из поиска.
        Для простоты будем называть его "запросом"
        :param user_id: id пользователя
        :param requests_id: id предложения
        :param name: имя предложения
        :param surname: фамилия предложения
        :param sex: пол предложения. 1 - женский, 2 - мужской
        :param age: возраст предложения
        :param city: город предложения
        :param link: ссылка на пользователя по запросу
        '''
        with self.session as session:
            requests_find = session.query(m.Requests.requests_id).all()
            if requests_id not in [req[0] for req in requests_find]:
                request = m.Requests(requests_id=requests_id, name=name,
                                      surname=surname, age=age, sex=sex, city=city, link=link)
                session.add(request)
            user_request_find = session.query(m.User_requests.requests_user_id).\
                filter(m.User_requests.user_id == user_id).\
                filter(m.User_requests.requests_id == requests_id).all()
            if len(user_request_find) == 0:
                user_request = m.User_requests(user_id=user_id, requests_id=requests_id)
                session.add(user_request)
            session.commit()

    def add_favorite(self, user_id, requests_id):
        '''
        Функция добавляет запрос пользователя в избранное,
        если пользователь хочет сохранить запрос.
        0 - предложение неактуально, 1 - предложение включено (включается) в избранное
        :param user_id: id пользователя
        :param requests_id: id предложения
        '''
        with self.session as session:
            session.query(m.User_requests). \
                filter(m.User_requests.requests_id == requests_id). \
                filter(m.User_requests.user_id == user_id). \
                update({'favorite_list': 1})
            session.commit()

    def add_photo(self, requests_id, photo_url):
        '''
        Функция сохраняет в БД ссылки на фотографии предложения
        :param requests_id: id запроса
        :param photo_url: ссылки на фотографии
        '''
        with self.session as session:
            for url in photo_url:
                photo = m.Photos(requests_id=requests_id, photo_url=url)
                session.add(photo)
            session.commit()


db_utils = DB_Utils(base=Base, dsn=settings.dsn)