import configparser
import os

class Config:

    def __init__(self, path=None):

        if path:
            settingspath = path
        else:
            settingspath = os.path.join(os.getcwd(), 'config.ini')
        config = configparser.ConfigParser()
        config.read(settingspath)

        self.token = config.get('VK_API', 'token')

        driver = config.get('DATABASE', 'driver')
        user = config.get('DATABASE', 'user')
        password = config.get('DATABASE', 'password')
        host = config.get('DATABASE', 'host')
        port = config.get('DATABASE', 'port')
        database_name = config.get('DATABASE', 'database_name')
        self.dsn = f'{driver}://{user}:{password}@{host}:{port}/{database_name}'

        self.auto_create = config.get('DATABASE', 'auto_create').lower().strip() in ('true', 't', '1', 'yes', 'y')
        self.auto_remove = config.get('DATABASE', 'auto_remove').lower().strip() in ('true', 't', '1', 'yes', 'y')


settings = Config()
