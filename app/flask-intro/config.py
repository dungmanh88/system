### default config
import os
class BaseConfig(object):
    DEBUG = False
    ### Using os.urandom(24) to generate secret_key 
    SECRET_KEY = '\x1f\x94;u\x87\xa1\xeep\x1f\xccI\xfb\xfb\xc5\xc8\xc5G\x11U\xf4q\xb5T\xed'
    ### Please export DATABASE_URL is sqlite:///posts.db
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
#    SQLALCHEMY_DATABASE_URI = "sqlite:///posts.db"

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
