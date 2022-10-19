import os
from pydantic import BaseSettings
from decouple import config

class Settings(BaseSettings):

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    DATABASE_URI = config("DATABASE_URI")
    # DATABASE_URI = "mysql+pymysql://root:12345678@localhost:3307/fastapiauth"
    # DATABASE_URI = 'sqlite:///sqlite.db'
    SECRET_KEY = config("SECRET")

    ALGORITHM = config("ALGORITHM")


settings = Settings()