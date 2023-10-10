import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = os.environ.get("APP_NAME", "Budget App")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or (
        f"sqlite:///{os.path.join(basedir, 'budget-db.sqlite')}"
    )

    # The Flask-SQLAlchemy documentation also suggests to set this key to False
    # to use less memory unless signals for object changes are needed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    SECRET_KEY = (
        os.getenv("SECRET_KEY") or b"LPhW~G@?b{*k'8;&MQbT=[~(M-VzDMKk.rP$kAnK"
    )
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in [
        "true",
        "on",
        "1",
    ]
    MAIL_USERNAME = os.environ.get(
        "MAIL_USERNAME", "ptua6.real4dmin@gmail.com"
    )
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "cubgxyscokadfxzj")
    MAIL_SUBJECT_PREFIX = f"[{APP_NAME}]"
    MAIL_SENDER_EMAIL = os.environ.get(
        "MAIL_SENDER_EMAIL", "ptua6.real4dmin@gmail"
    )
    MAIL_SENDER = f"{APP_NAME} HQ <{MAIL_SENDER_EMAIL}>"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        f"sqlite:///{os.path.join(basedir, 'budget-db.sqlite')}"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
