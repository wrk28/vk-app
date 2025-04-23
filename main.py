from config import settings
from content import Content
from database import db_utils
from services import Data_Service
from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randint


class BotCommands:
    NEXT = Content.BOT_COMMAND_NEXT
    ADD_FAVOURITES = Content.BOT_ADD_FAVOURITES
    SHOW_FAVOURITES = Content.BOT_SHOW_FAVOURITES


class BotMessages:

    def __init__(self, bot_api: VkApiMethod, user_id: str):
        self.bot_api = bot_api
        self.user_id = user_id

        self.keyboard = VkKeyboard()
        self.keyboard.add_button(BotCommands.NEXT, VkKeyboardColor.PRIMARY)
        self.keyboard.add_button(BotCommands.ADD_FAVOURITES, VkKeyboardColor.SECONDARY)
        self.keyboard.add_button(BotCommands.SHOW_FAVOURITES, VkKeyboardColor.SECONDARY)

    def _random_id(self) -> int:
        return randint(1, 2**63-1)

    def messsage(self, message: str):
        self.bot_api.messages.send(user_id=self.user_id, 
                          message=message, 
                          random_id=self._random_id(), 
                          keyboard=self.keyboard.get_keyboard())

    def message_photo(self):
        pass
    

if __name__ == '__main__':
    
    data_service = Data_Service(token=settings.token, db_utils=db_utils)

    try:
        if settings.auto_remove:
            data_service.remove_database()
            
        if settings.auto_create:
            data_service.create_database()

        vk_session = VkApi(token=settings.token)
        poll = VkLongPoll(vk_session)
        bot_api = vk_session.get_api()

        for event in poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    bot = BotMessages(bot_api=bot_api, user_id=event.user_id)

                    if request == BotCommands.NEXT:
                        bot.messsage('Выбрано "Следующий"')
                        account = data_service.next_account(user_id=bot.user_id)
                        print(account)

                    elif request == BotCommands.ADD_FAVOURITES:
                        bot.messsage('Выбрано "В избранное"')
                        current_account = {}
                        data_service.add_to_favourites(account=current_account)

                    elif request == BotCommands.SHOW_FAVOURITES:
                        bot.messsage('Выбрано "Показать избранное"')
                        data_service.show_favourites(user=bot.bot_api)

                    else:
                        bot.messsage('Выберите "Следующий" для начала поиска')

    except Exception as e:
        print(Content.PROGRAM_STOPPED.format(error=e))
    finally:
        data_service.close()
