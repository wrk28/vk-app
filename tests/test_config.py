import config

class TestConfig:

    def test_settingspath_default(self):
        settings = config.Config()
        assert settings.dsn is not None
        assert settings.user_token is not None
        assert settings.group_token is not None

    def test_settingspath_specified(self):
        settings = config.Config('./config.ini')
        assert settings.dsn is not None
        assert settings.user_token is not None
        assert settings.group_token is not None