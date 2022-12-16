import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    DB_SERVER = os.getenv('DB_SERVER')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    @property
    def DATABASE_URI(self):
        return f'postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}'
