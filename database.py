import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import User
import models as m

class DB_Utils:

    def __init__(self, base, dsn) -> None:
        self.base = base
        self.engine = sq.create_engine(dsn)
        self.Session = sessionmaker(bind=self.engine)
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
        self._start_session()
        result = self.session.query(User).filter(User.user_id == user_id).one_or_none()
        self._close_session()
        return True if result else False

    def add_user(self, user_info: dict) -> None:
        '''
        Функция добавляет пользователя в базу данных.
        '''
        user_id = user_info['user_id']
        city_id = user_info['city_id']
        sex = user_info['sex']
        age = user_info['age']
        self._start_session()
        new_user = User(user_id=user_id, city_id=city_id, sex=sex, age=age)
        self.session.add(new_user)
        self.session.commit()
        self._close_session()


    def get_favourites(self, user_id: str) -> list:
        pass

    def create_database(self) -> None:
        self.base.metadata.create_all(self.engine)

    def remove_database(self) -> None:
        self.base.metadata.drop_all(self.engine)

    def close(self) -> None:
        self._close_session()


    def add_requests(self, user_id, account):
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
        # with self.session as session:
        #     requests_find = session.query(m.Requests.requests_id).all()
        #     if requests_id not in [req[0] for req in requests_find]:
        #         request = m.Requests(requests_id=requests_id, name=name,
        #                               surname=surname, age=age, sex=sex, city=city, link=link)
        #         session.add(request)
        #     user_request_find = session.query(m.User_requests.requests_user_id).\
        #         filter(m.User_requests.user_id == user_id).\
        #         filter(m.User_requests.requests_id == requests_id).all()
        #     if len(user_request_find) == 0:
        #         user_request = m.User_requests(user_id=user_id, requests_id=requests_id)
        #         session.add(user_request)
        #     session.commit()

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