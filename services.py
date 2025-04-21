from database import DB_Utils


class Data_Service:
    """Обеспечение совместной работы приложения с VK API и базой данных"""
    def __init__(self, token: str, db_utils: DB_Utils):
        self.token = token
        self.db_utils = db_utils

    def close(self):
        """Завершение работы с базой данных"""
        self.db_utils.close()


