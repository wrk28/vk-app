from config import settings
from content import Content
from models import Base
from database import DB_Utils
from services import Data_Service


if __name__ == '__main__':
    
    db_utils = DB_Utils(base=Base, dsn=settings.dsn)
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
