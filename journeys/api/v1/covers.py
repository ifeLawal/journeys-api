from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError

from journeys.api.schemas.covers import CoverSchema
from models import Covers

covers_namespace = Namespace("covers", description="Endpoint to retrieve Covers")


@covers_namespace.route("")
class PictureList(Resource):
    def get(self):
        covers = Covers.query.paginate(max_per_page=25)
        schema = CoverSchema(many=True)

        try:
            data = schema.dump(covers.items)
            return {"success": True, "data": data}
        except ValidationError as error:
            return {"success": False, "errors": error}, 400
