from flask import render_template
from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError

from journeys.api.schemas.pictures import PictureSchema
from journeys.api.utils.models import build_model_filters
from models import Pictures

pictures_namespace = Namespace("pictures", description="Endpoint to retrieve Pictures")


@pictures_namespace.route("")
class PictureList(Resource):
    def get(self):
        # q = query_args.pop("q", None)
        # field = str(query_args.pop("field", None))
        # filters = build_model_filters(model=pictures, query=q, field=field)

        # pictures = Pictures.query.filter_by(**query_args).filter(*filters).all()
        pictures = Pictures.query.paginate(max_per_page=25)
        schema = PictureSchema(many=True)

        try:
            data = schema.dump(pictures.items)
            return {"success": True, "data": data}
        except ValidationError as error:
            return {"success": False, "errors": error}, 400
