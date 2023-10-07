import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or (
        f"sqlite:///{os.path.join(basedir, 'budget-db.sqlite')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = (
        os.getenv("SECRET_KEY") or b"LPhW~G@?b{*k'8;&MQbT=[~(M-VzDMKk.rP$kAnK"
    )
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "ptua6.real4dmin@gmail.com"
    MAIL_PASSWORD = "cubgxyscokadfxzj"

    def init_app(self):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or (
        f"sqlite:///{os.path.join(basedir, 'budget-db.sqlite')}"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
