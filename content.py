import json


class Content:
    """Чтения файла с текстовым контентом для применения в коде приложения"""
    @classmethod
    def initialize(cls):

        with open('content.json', 'r') as f:
            content = json.load(f)
        cls.PROGRAM_STOPPED = content['program_stopped']


Content.initialize()