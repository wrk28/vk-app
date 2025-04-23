from database import DB_Utils
import requests
from datetime import datetime


class Data_Service:
    """Обеспечение совместной работы приложения с VK API и базой данных"""
    def __init__(self, token: str, db_utils: DB_Utils):
        self.token = token
        self.version = '5.131'
        self.db_utils = db_utils

    def close(self):
        """Завершение работы с базой данных"""
        self.db_utils.close()

    def next_account(self, user_id: str) -> dict:
        user_info = self._user_info(user_id)
        offset = self.db_utils.get_offset(user_info['user_id'])
        account = self._fetch_account(user_info=user_info, offset=offset)
        return account

    def add_to_favourites(self, account: dict) -> bool:
        return None

    def show_favourites(self, user_id: str) -> list:
        return None
    
    def _fetch_account(self, user_info: dict, offsett: int) -> dict:
        pass
    
    def _user_info(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {"access_token": self.token, "v": self.version, "user_ids": user_id, "fields": "bdate,city,sex"}
        response = requests.get(url=url, params=params).json()['response'][0]

        self.id = response.get('id')
        self.city_id = response.get('city').get('id')
        self.sex = response.get('sex')
        bday = response.get('bday')
        if bday:
            current_time = datetime.now()
            self.age = current_time.year - bday.year - ((current_time.month, current_time.day) < (bday.month, bday.day))
        else:
            self.age = None

        return {"user_id": self.id, "city_id": self.city_id, "sex": self.sex, "age": self.age}

    def create_database(self):
        """Создать базу данных"""
        self.db_utils.create_database()

    def remove_database(self):
        """Удалить базу данных"""
        self.db_utils.remove_database()


