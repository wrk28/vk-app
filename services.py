import requests
from datetime import datetime
from database import DB_Utils
from content import Content


class Data_Service:

    def __init__(self, group_token: str, user_token:str, db_utils: DB_Utils):
        self.group_token = group_token
        self.user_token = user_token
        self.version = '5.199'
        self.db_utils = db_utils

    def close(self):
        self.db_utils.close()


    def next_account(self, user_id: str) -> dict:
        user_info = self._user_info(user_id)
        account = self._fetch_account(user_info=user_info)
        photos = self._fetch_photos(owner_id = account.get('id'))
        return account, photos


    def add_to_favourites(self, user_id: str) -> str:
        requests_id = self.db_utils.get_last_requests_id(user_id=user_id)
        self.db_utils.add_favorite(user_id=user_id, requests_id=requests_id)
        name = self.db_utils.get_requests_name(requests_id=requests_id)
        return f'{name[0]} {name[1]}'
    

    def get_favourites(self, user_id: str) -> tuple:
        requests = self.db_utils.get_favourites(user_id=user_id)
        favourites = []
        for item in requests:
            photos = self.db_utils.get_requests_photos(request_id=item['id'])
            favourites.append({"account": item, "photos": photos})
        return favourites
    

    def check_user(self, user_id: str) -> bool:
        found = self.db_utils.check_user(user_id=user_id)
        if not found:
            user_info = self._user_info(user_id=user_id)
            self.db_utils.add_user(user_info=user_info)
        return not found
    

    def _fetch_account(self, user_info: dict) -> dict:
        url = r'https://api.vk.com/method/users.search'
        search_params = self._get_search_params(user_info)
        params = {"v": self.version, "access_token": self.user_token, **search_params}
        response = requests.get(url=url, params=params)
        if 'error' in response.json():
            raise Exception(Content.ERROR_API_REQUEST)
        items = response.json()['response']['items'][0]
        account = self._get_account_info(items)
        self.db_utils.add_requests(user_id=user_info['user_id'], account=account)
        return account


    def _get_search_params(self, user_info: dict) -> dict:
        offset = self.db_utils.get_offset(user_info.get('user_id'))
        age_from = user_info['age'] - 5 if user_info['age'] else None
        age_to = user_info['age'] + 5 if user_info['age'] else None
        params = {
            "city_id": user_info['city_id'],
            "age_from": age_from,
            "age_to": age_to,
            "sex": user_info['sex'],
            "count": 1,
            "offset": offset
        }
        return params
    

    def _get_account_info(self, items: dict) -> dict:
        keys = {"id", "first_name", "last_name", "sex", "city_id", "age"}
        account = {key: items[key] for key in keys if key in items}
        account['link'] = f'https://vk.com/id{account.get("id")}'
        return account
    

    def _fetch_photos(self, owner_id: str) -> list:
        url = r'https://api.vk.com/method/photos.get'
        params = {"access_token": self.user_token, "v": self.version, "owner_id": owner_id, "album_id": "profile", "extended": 1}
        response = requests.get(url=url, params=params).json()
        photos_info = []
        if 'error' not in response:
            items = response['response']['items']
            photos_info = self._get_photos_info(items)
            self.db_utils.add_photos(requests_id=owner_id, photos=photos_info)
        return photos_info


    def _get_photos_info(self, items: list) -> list:
        sorted_photos = sorted(items, key=lambda item: (item.get('likes', {}).get('count', 0) if 'likes' in item else 0), reverse=True)
        photos = sorted_photos[:3]
        photos_info = []
        for photo in photos:
            sizes = photo['sizes']
            max_size = max(sizes, key=lambda x: x['height'] * x['width'])['url']
            photos_info.append({"media_id": photo.get('id'), "owner_id": photo.get('owner_id'), "access_key": photo.get('access_key'), "url": max_size}) 
        return photos_info
        
    
    def _user_info(self, user_id: str) -> dict:
        url = r'https://api.vk.com/method/users.get'
        params = {"access_token": self.group_token, "v": self.version, "user_ids": user_id, "fields": "bdate,city,sex"}
        response = requests.get(url=url, params=params)
        if 'error' in response.json():
            raise Exception(Content.ERROR_API_REQUEST)
        item = response.json()['response'][0]
        return self._get_user_info(item)


    def _get_user_info(self, item: dict) -> dict:
        user_id = item.get('id')
        city_id = item.get('city').get('id')
        sex = item.get('sex')
        bday = item.get('bday')
        if bday:
            current_time = datetime.now()
            age = current_time.year - bday.year - ((current_time.month, current_time.day) < (bday.month, bday.day))
        else:
            age = None
        return {"user_id": user_id, "city_id": city_id, "sex": sex, "age": age}


    def create_database(self) -> None:
        self.db_utils.create_database()


    def remove_database(self) -> None:
        self.db_utils.remove_database()
