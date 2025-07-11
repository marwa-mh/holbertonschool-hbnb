import os
from dotenv import load_dotenv


load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False

class DevelopmentConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}