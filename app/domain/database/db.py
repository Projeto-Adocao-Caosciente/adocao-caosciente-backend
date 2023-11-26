from pymongo import MongoClient
from app.config.settings import settings

env = settings.ENVIRONMENT
DATABASE_URL = settings.DATABASE_URL if env != "test" else settings.DATABASE_URL_TEST
DATABASE_NAME = settings.DATABASE_NAME if env != "test" else settings.DATABASE_NAME_TEST

class Database:
    def __init__(self):
        self.client = MongoClient(DATABASE_URL)
        self.db = self.client.get_database(DATABASE_NAME)
        self.session = self.client.start_session()
    
    def get_database(self):
        # TODO: Tornar singleton
        return self.db
