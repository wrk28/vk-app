import sqlalchemy
from sqlalchemy.orm import sessionmaker
import models as m
import configparser

class Load_db:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        login = config['authorization db']['login_db']
        password = config['authorization db']['password_db']
        name_db = config['authorization db']['name_db']
        self.engine = sqlalchemy.create_engine(f'postgresql://{login}:{password}'
                                               f'@localhost:5432/{name_db}')
        m.create_tables(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_user_vkinder(self, id_user, name, surname, age, sex, city):
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
        with self.session as session:
            user_find = session.query(m.User_VKinder.id_user).all()
            if id_user not in [user[0] for user in user_find]:
                user = m.User_VKinder(id_user=id_user, name=name, surname=surname, age=age,
                                      sex=sex,  city=city)
                session.add(user)
                session.commit()

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



# class DB_Utils:
#
#     def __init__(self, base, dsn):
#         self.base = base
#         self.engine = sq.create_engine(dsn)
#         self.Session = sessionmaker()
#         self.session = None
#
#     def _start_session(self):
#         self.session = self.Session()
#
#     def _close_session(self):
#         if self.session:
#             self.session.close()
#         self.session = None
#
#     def create_database(self):
#         self.base.metadata.create_all(self.engine)
#
#     def remove_database(self):
#         self.base.metadata.drop_all(self.engine)
#
#     def close(self):
#         self._close_session()
#
#
# db_utils = DB_Utils(base=Base, dsn=settings.dsn)