import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    # General config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rzQT29uwr7jrUWFC2KvnM363'
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    CONFIG_DIR = os.path.join(basedir, 'config')
    CONFIG_FILE = os.path.join(CONFIG_DIR, 'settings.ini')
    DATA_DIR = os.path.join(basedir, 'data')

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # DB config
    if config.read(CONFIG_FILE) and config.get('DB settings', 'type') == 'postgres':
        POSTGRES_URL = config.get('DB settings', 'url')
        POSTGRES_USER = config.get('DB settings', 'user')
        POSTGRES_PASSWORD = config.get('DB settings', 'password')
        POSTGRES_DB = config.get('DB settings', 'name')
        POSTGRES_PORT = config.get('DB settings', 'port')
        DB_URL = 'postgresql+psycopg2://{user}:{password}@{url}:{port}/{db}'.format(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            url=POSTGRES_URL,
            port=POSTGRES_PORT,
            db=POSTGRES_DB
        )
        SQLALCHEMY_DATABASE_URI = DB_URL
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DATA_DIR, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
