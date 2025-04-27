from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from config import settings
from content import Content
from database import DB_Utils
from models import Base
from services import Data_Service
from messages import BotCommands, BotMessages


if __name__ == '__main__':

    db_utils = DB_Utils(base=Base, dsn=settings.dsn)
    
    data_service = Data_Service(group_token=settings.group_token, user_token=settings.user_token, db_utils=db_utils)

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
