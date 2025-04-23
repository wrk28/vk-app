import json


class Content:
    """Чтения файла с текстовым контентом для применения в коде приложения"""
    @classmethod
    def initialize(cls):

        with open('content.json', 'r') as f:
            content = json.load(f)
        cls.PROGRAM_STOPPED = content['program_stopped']
        cls.BOT_START_MESSAGE = content['bot_start_message']
        cls.BOT_COMMAND_NEXT = content['bot_command_next']
        cls.BOT_ADD_FAVOURITES = content['bot_command_add_favourites']
        cls.BOT_SHOW_FAVOURITES = content['bot_command_show_favourites']


Content.initialize()