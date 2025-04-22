from config import settings
from content import Content
from database import db_utils
from services import Data_Service
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint

def random_id():
    return randint(1, 2**63-1)

if __name__ == '__main__':
    
    data_service = Data_Service(token=settings.token, db_utils=db_utils)

    try:
        if settings.auto_remove:
            data_service.remove_database()
            
        if settings.auto_create:
            data_service.create_database()

        vk_session = VkApi(token=settings.token)
        poll = VkLongPoll(vk_session)
        bot = vk_session.get_api()

        for event in poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    if request == '1':
                        bot.messages.send(user_id=event.user_id, message='2', random_id=random_id())

    except Exception as e:
        print(Content.PROGRAM_STOPPED.format(error=e))
    finally:
        data_service.close()
