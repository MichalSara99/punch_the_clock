import os
import pymysql
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or  '09091988'
    LANGUAGES = ['en','cs']
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT',587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS','true').lower() in ['true','on','1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'Punch.The.Clock.Team@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Einstein1988++'
    PTC_MAIL_SUBJECT_PREFIX = '[Punch The Clock]'
    PTC_MAIL_SENDER = 'Punch The Clock Admin <Punch.The.Clock.Team@gmail.com>'
    PTC_ADMIN = os.environ.get('PTC_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass



class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql+pymysql://root:Einstein1988++@127.0.0.1:3306/ptc?charset=utf8mb4'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://saramich$ptc?charset=utf8mb4'

config = {
'development': DevConfig,
'production': ProdConfig,
'default': DevConfig
}
