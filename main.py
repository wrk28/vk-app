from random import randint
from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import settings
from content import Content
from database import DB_Utils
from models import Base
from services import Data_Service


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
    

if __name__ == '__main__':

    db_utils = DB_Utils(base=Base, 
                        dsn=settings.dsn)
    
    data_service = Data_Service(group_token=settings.group_token, 
                                user_token=settings.user_token, 
                                db_utils=db_utils)

    try:
        if settings.auto_remove:
            data_service.remove_database()
            
        if settings.auto_create:
            data_service.create_database()

        vk_session = VkApi(token=settings.group_token)
        poll = VkLongPoll(vk_session)
        bot_api = vk_session.get_api()
        bot = BotMessages(bot_api=bot_api, user_id=None)

        for event in poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    new_user = data_service.check_user(user_id=event.user_id)
                    bot.set_user_id(user_id=event.user_id)

                    if new_user:
                        bot.start_message(Content.BOT_START_MESSAGE)

                    elif request == BotCommands.NEXT:
                        account, photos = data_service.next_account(user_id=bot.user_id)
                        message = f'- {account.get("first_name")} {account.get("last_name")}\n- {account.get("link")}'
                        bot.message_photos(message=message, photos=photos)

                    elif request == BotCommands.ADD_FAVOURITES:
                        name = data_service.add_to_favourites(user_id=event.user_id)
                        bot.message(Content.ADDED_TO_FAVOURITES.format(name=name))

                    elif request == BotCommands.SHOW_FAVOURITES:
                        bot.message(Content.FAVOURITES)
                        favourites = data_service.get_favourites(user_id=bot.user_id)
                        for item in favourites:
                            account = item['account']
                            photos = item['photos']
                            message = f'-{account.get("first_name")} {account.get("last_name")}\n- {account.get("link")}'
                            bot.message_photos(message=message, photos=photos)

                    else:
                        bot.message(Content.CHOOSE_NEXT_TO_START)

    except Exception as e:
        print(Content.PROGRAM_STOPPED.format(error=e))
    finally:
        data_service.close()
