from flask import request
from flask_restx import Namespace, Resource, reqparse
from marshmallow.exceptions import ValidationError
from werkzeug.datastructures import ImmutableMultiDict

from journeys.api.schemas.movies import MovieSchema
from models import Movies

parser = reqparse.RequestParser()
parser.add_argument("rate", type=int, help="Rate cannot be converted")
parser.add_argument("name")

movies_namespace = Namespace("movies", description="Endpoint to retrieve Movies")


@movies_namespace.route("")
class MovieList(Resource):
    def get(self):
        # TODO Make the filter like into a generic function for use in locations and comments
        name = request.args.get("name", "")
        args = []
        if name:
            for arg in request.args:
                if "name" not in arg:
                    filter = request.args.get(arg)
                    args.append((arg, filter))
            args = ImmutableMultiDict(args)
        else:
            args = request.args
        name = f"%{name}%"
        movies = (
            Movies.query.filter_by(**args)
            .filter(Movies.name.like(name))
            .paginate(max_per_page=25)
        )
        schema = MovieSchema(many=True)

        try:
            data = schema.dump(movies.items)
            return {"success": True, "data": data}
        except ValidationError as error:
            return {"success": False, "errors": error}, 400
