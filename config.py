import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'hart to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = "[Flasky]"
    FLASKY_MAIL_SENDER = "413180794@qq.com"
    FLASK_ADMIN = "413180794@qq.com"


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "413180794@qq.com"
    MAIL_PASSWORD = "zcjxxxdcdfzsbijc"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or 'sqlite:///' + os.path.join(basedir,
                                                                                                'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or 'sqlite:///' + os.path.join(basedir,
                                                                                                'data-test.sqlite')


class ProductConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or 'sqlite:///' + os.path.join(basedir,
                                                                                                'data.sqlite')
config = {
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "production":ProductConfig,
    "default":DevelopmentConfig
}
