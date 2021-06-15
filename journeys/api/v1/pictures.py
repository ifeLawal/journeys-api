from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError

from journeys.api.schemas.pictures import PictureSchema
from models import Pictures

pictures_namespace = Namespace("pictures", description="Endpoint to retrieve Pictures")


@pictures_namespace.route("")
class PictureList(Resource):
    def get(self):
        pictures = Pictures.query.paginate(max_per_page=25)
        schema = PictureSchema(many=True)

        try:
            data = schema.dump(pictures.items)
            return {"success": True, "data": data}
        except ValidationError as error:
            return {"success": False, "errors": error}, 400
