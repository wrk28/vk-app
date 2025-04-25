from database import DB_Utils
import requests
from datetime import datetime


class Data_Service:
    """Обеспечение совместной работы приложения с VK API и базой данных"""
    def __init__(self, group_token: str, user_token:str, db_utils: DB_Utils):
        self.group_token = group_token
        self.user_token = user_token
        self.version = '5.199'
        self.db_utils = db_utils

    def close(self):
        """Завершение работы с базой данных"""
        self.db_utils.close()


    def next_account(self, user_id: str) -> dict:
        user_info = self._user_info(user_id)
        offset = self.db_utils.get_offset(user_id)
        account = self._fetch_account(user_info=user_info, offset=offset)
        photos = self._fetch_photos(owner_id = account.get('id'))
        return account, photos


    def add_to_favourites(self, user_id: str) -> str:
        requests_id = self.db_utils.get_last_requests_id(user_id=user_id)
        self.db_utils.add_favorite(user_id=user_id, requests_id=requests_id)
        name = self.db_utils.get_requests_name(requests_id=requests_id)
        return f'{name[0]} {name[1]}'
    

    def get_favourites(self, user_id: str) -> list:
        favourites = self.db_utils.get_favourites(user_id=user_id)
        return favourites
    

    def check_user(self, user_id: str):
        user_exists = self.db_utils.check_user(user_id=user_id)
        if not user_exists:
            user_info = self._user_info(user_id=user_id)
            self.db_utils.add_user(user_info=user_info)
    

    def _fetch_account(self, user_info: dict, offset: int) -> dict:
        url = r'https://api.vk.com/method/users.search'
        age_from = user_info['age'] - 5 if user_info['age'] else None
        age_to = user_info['age'] + 5 if user_info['age'] else None
        params = {
            "city_id": user_info['city_id'],
            "age_from": age_from,
            "age_to": age_to,
            "sex": user_info['sex'],
            "count": 1,
            "offset": offset,
            "v": self.version,
            "access_token": self.user_token
        }
        response = requests.get(url=url, params=params)
        items = response.json()['response']['items'][0]
        keys = {"id", "first_name", "last_name", "sex", "city_id", "age"}
        account = {key: items[key] for key in keys if key in items}
        account['link'] = f'https://vk.com/id{account.get("id")}'
        self.db_utils.add_requests(user_id=user_info['user_id'], account=account)
        return account
    

    def _fetch_photos(self, owner_id: str):
        url = r'https://api.vk.com/method/photos.get'
        params = {"access_token": self.user_token, "v": self.version, "owner_id": owner_id, "album_id": "profile", "extended": 1}
        items = requests.get(url=url, params=params).json()['response']['items']
        sorted_photos = sorted(items, key=lambda item: (item.get('likes', {}).get('count', 0) if 'likes' in item else 0), reverse=True)
        top_photos = sorted_photos[:3]
        photo_urls = self._get_photo_links(top_photos)
        for photo in photo_urls:
            self.db_utils.add_photo(requests_id=owner_id, photo_url=photo)
        return photo_urls


    def _get_photo_links(self, photos: list) -> list:
        photo_urls = []
        for photo in photos:
            sizes = photo['sizes']
            max_size = max(sizes, key=lambda x: x['height'] * x['width'])['url']
            photo_urls.append(max_size) 
        return photo_urls
        
    
    def _user_info(self, user_id):
        url = r'https://api.vk.com/method/users.get'
        params = {"access_token": self.group_token, "v": self.version, "user_ids": user_id, "fields": "bdate,city,sex"}
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


