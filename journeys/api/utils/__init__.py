from flask import current_app as app
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import create_database as create_database_util
from sqlalchemy_utils import database_exists as database_exists_util
from sqlalchemy_utils import drop_database as drop_database_util


def create_database():
    url = make_url(app.config["SQLALCHEMY_DATABASE_URI"])
    if not database_exists_util(url):
        create_database_util(url)
    return url


def drop_database():
    url = make_url(app.config["SQLALCHEMY_DATABASE_URI"])
    drop_database_util(url)
