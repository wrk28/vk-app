from random import randint
from vk_api.vk_api import VkApiMethod
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from content import Content


class BotCommands:
    NEXT = Content.BOT_COMMAND_NEXT
    ADD_FAVOURITES = Content.BOT_ADD_FAVOURITES
    SHOW_FAVOURITES = Content.BOT_SHOW_FAVOURITES


class BotMessages:

    def __init__(self, bot_api: VkApiMethod, user_id: str) -> None:
        self.bot_api = bot_api
        self.user_id = user_id
        self.start_keyboard = VkKeyboard()
        self.start_keyboard.add_button(Content.START, VkKeyboardColor.PRIMARY)
        self.keyboard = VkKeyboard()
        self.keyboard.add_button(BotCommands.NEXT, VkKeyboardColor.PRIMARY)
        self.keyboard.add_button(BotCommands.ADD_FAVOURITES, VkKeyboardColor.SECONDARY)
        self.keyboard.add_button(BotCommands.SHOW_FAVOURITES, VkKeyboardColor.SECONDARY)
        
    def set_user_id(self, user_id: str) -> None:
        self.user_id = user_id
    
    def start_message(self, message: str) -> None:
        self.bot_api.messages.send(user_id=self.user_id, 
                          message=message, 
                          random_id=self._random_id(), 
                          keyboard=self.start_keyboard.get_keyboard())

    def message(self, message: str) -> None:
        self.bot_api.messages.send(user_id=self.user_id, 
                          message=message, 
                          random_id=self._random_id(), 
                          keyboard=self.keyboard.get_keyboard())

    def message_photos(self, message: str, photos: list) -> None:
        attachments = self._get_attachment_str(photos)
        if attachments:
            self.bot_api.messages.send(user_id=self.user_id,
                            message=message, 
                            random_id=self._random_id(), 
                            keyboard=self.keyboard.get_keyboard(),
                            attachment=attachments)
        else:
            self.message(message=f'{message}\n{Content.NO_PHOTOS}')

    def _random_id(self) -> int:
        return randint(1, 2**63-1)

    def _get_attachment_str(self, photos):
        attachment_list = []
        for item in photos:
            attachment = f'photo{item["owner_id"]}_{item["media_id"]}'
            if item['access_key']:
                attachment = f'{attachment}_{item["access_key"]}'
            attachment_list.append(attachment)
        attachments = ','.join(attachment_list)
        return attachments