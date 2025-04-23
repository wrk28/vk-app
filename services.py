from database import DB_Utils


class Data_Service:
    """Обеспечение совместной работы приложения с VK API и базой данных"""
    def __init__(self, token: str, db_utils: DB_Utils):
        self.token = token
        self.db_utils = db_utils

    def close(self):
        """Завершение работы с базой данных"""
        self.db_utils.close()

    def next_account(self, user_id: str) -> dict:
        return None

    def add_to_favourites(self, account: dict) -> bool:
        return None

    def show_favourites(self, user_id: str) -> list:
        return None

    def create_database(self):
        """Создать базу данных"""
        self.db_utils.create_database()

    def remove_database(self):
        """Удалить базу данных"""
        self.db_utils.remove_database()


