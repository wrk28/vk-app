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
        cls.ADDED_TO_FAVOURITES = content['added_to_favourites']
        cls.FAVOURITES = content['favourites']
        cls.NO_PHOTOS = content['no_photos']
        cls.START = content['start']
        cls.CHOOSE_NEXT_TO_START = content['choose_next_to_start']
        cls.ERROR_API_REQUEST = content['error_api_request']
        cls.BOT_SHOW_FAVOURITES = content['bot_command_show_favourites']


Content.initialize()