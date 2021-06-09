# https://docs.sqlalchemy.org/en/14/tutorial/engine.html
# import sqlalchemy
# sqlalchemy(__name__)
import os

from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))
db_type = "sqlite"
db_api = "pysqlite"
name = "ontheset"
db_location = os.path.join(basedir, f"{name}.db")
DATABASE = f"{db_type}+{db_api}:///{db_location}"
# {
#     "drivername": "sqlite",
#     # 'host': 'localhost',
#     # 'port': '5432',
#     # 'username': 'YOUR_USERNAME',
#     # 'password': 'YOUR_PASSWORD',
#     "database": "/path/to/your_db.sqlite",
# }


def get_engine(name):
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_type = "sqlite"
    db_api = "pysqlite"
    db_location = os.path.join(basedir, f"{name}.db")
    engine = create_engine(
        f"{db_type}+{db_api}:///{db_location}", echo=True, future=True
    )
    # engine = create_engine(URL(**DATABASE))
    return engine
