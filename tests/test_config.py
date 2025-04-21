import config

class TestConfig:

    def test_settingspath_default(self):
        settings = config.Config()
        assert settings.dsn == 'postgresql+pg8000://<user>:<password>@localhost:5432/<database_name>'
        assert settings.token == '<Your token>'

    def test_settingspath_specified(self):
        settings = config.Config('./config.ini')
        assert settings.dsn == 'postgresql+pg8000://<user>:<password>@localhost:5432/<database_name>'
        assert settings.token == '<Your token>'