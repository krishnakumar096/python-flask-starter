import os
import psycopg2
import socket
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

basedir = os.path.abspath(os.path.dirname(__file__))

class DbConfig:
    db_host = os.getenv('POSTGRES_HOST') or 'localhost'
    db_user = os.getenv('POSTGRES_USER') or 'postgres'
    db_password = os.getenv('POSTGRES_PASSWORD') or 'root@123'
    db_port = os.getenv('POSTGRES_PORT') or '5432'
    db_name = os.getenv('POSTGRES_NAME') or 'postgres'
    postgres_local_base = 'postgresql+psycopg2://'+db_user+':'+db_password+'@'+db_host+':'+db_port+'/'+db_name


class PythonConfig:
    flask_port = os.getenv('SERVER_PORT') or "5000"
    project_name = "python-flask-starter"
    

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')


class DevelopmentConfig(Config):
    # for postgres uncomment this line
    SQLALCHEMY_DATABASE_URI = DbConfig.postgres_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = DbConfig.postgres_local_base
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DbConfig.postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    uat=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY