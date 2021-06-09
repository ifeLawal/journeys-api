import logging
import os
import shutil
from pathlib import Path

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import MetaData

from connecting import get_engine

Base = declarative_base()
db = SQLAlchemy()
ma = Marshmallow()


class Movies(Base, db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    year = Column(String(128))
    summary = Column(Text, default="This movie summary is not available")

    locations = relationship("Locations", back_populates="movies")
    covers = relationship("Covers", back_populates="movies")

    def __repr__(self):
        return f"Movies(id={self.id!r}, name={self.name!r}, year={self.year!r})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Locations(Base, db.Model):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    address = Column(String(128), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"))

    movies = relationship("Movies", back_populates="locations")
    pictures = relationship("Pictures", back_populates="locations")
    comments = relationship("Comments", back_populates="locations")

    def __repr__(self):
        return f"Locations(id={self.id!r}, address={self.address!r}, movie_id={self.movie_id!r})"


class Pictures(Base, db.Model):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True)
    file_location = Column(Text, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    movie_id = Column(Integer)

    locations = relationship("Locations", back_populates="pictures")

    # def __repr__(self):
    #     return f"User(id={self.id!r}, name={self.email_address!r}, fullname={self.user_id!r}"


class Comments(Base, db.Model):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    comment = Column(Text)
    location_id = Column(Integer, ForeignKey("locations.id"))
    movie_id = Column(Integer)

    locations = relationship("Locations", back_populates="comments")

    # def __repr__(self):
    #     return f"User(id={self.id!r}, name={self.email_address!r}, fullname={self.user_id!r}"


class Covers(Base, db.Model):
    __tablename__ = "covers"

    id = Column(Integer, primary_key=True)
    file_location = Column(Text, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"))

    movies = relationship("Movies", back_populates="covers")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.email_address!r}, fullname={self.user_id!r}"


def create_all_tables(engine_name):
    engine = get_engine(name=engine_name)
    Base.metadata.create_all(engine)


def drop_table_with_name(engine_name, table_name):
    engine = get_engine(name=engine_name)
    metadata = MetaData(engine)
    table = Table(table_name, metadata, autoload=True)
    if table is not None:
        logging.info(f"Deleting {table_name} table")
        Base.metadata.drop_all(bind=engine, tables=[table], checkfirst=True)
    # Base.metadata.drop_all(bind=engine, tables=[Covers.__table__])


def drop_all(engine_name):
    engine = get_engine(name=engine_name)
    path = Path(os.path.dirname(__file__))
    project_path = path.parent.absolute()
    shutil.rmtree(os.path.join(project_path, "scraper/files"))
    Base.metadata.drop_all(engine)
