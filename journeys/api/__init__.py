from flask import Blueprint
from flask_restx import Api

from journeys.api.v1.comments import comments_namespace
from journeys.api.v1.covers import covers_namespace
from journeys.api.v1.locations import locations_namespace
from journeys.api.v1.movies import movies_namespace
from journeys.api.v1.pictures import pictures_namespace

# https://stackoverflow.com/questions/24757922/correct-way-to-display-image-through-restapi

api = Blueprint("api", __name__)
journeys_api = Api(api)

journeys_api.add_namespace(ns=movies_namespace, path="/movies")
journeys_api.add_namespace(ns=comments_namespace, path="/comments")
journeys_api.add_namespace(ns=covers_namespace, path="/covers")
journeys_api.add_namespace(ns=pictures_namespace, path="/pictures")
journeys_api.add_namespace(ns=locations_namespace, path="/locations")
