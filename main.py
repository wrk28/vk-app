from config import settings
from content import Content
from database import db_utils
from services import Data_Service


if __name__ == '__main__':
    
    data_service = Data_Service(token=settings.token, db_utils=db_utils)

    try:

        if settings.auto_remove:
            data_service.remove_database()
            
        if settings.auto_create:
            data_service.create_database()

    except Exception as e:
        print(Content.PROGRAM_STOPPED.format(error=e))
    finally:
        data_service.close()
