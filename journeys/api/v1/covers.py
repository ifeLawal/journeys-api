from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError

from journeys.api.schemas.covers import CoverSchema
from journeys.api.utils.models import build_model_filters
from models import Covers

covers_namespace = Namespace("covers", description="Endpoint to retrieve Covers")


@covers_namespace.route("")
class PictureList(Resource):
    def get(self):
        # q = query_args.pop("q", None)
        # field = str(query_args.pop("field", None))
        # filters = build_model_filters(model=covers, query=q, field=field)

        # covers = Covers.query.filter_by(**query_args).filter(*filters).all()
        covers = Covers.query.paginate(max_per_page=25)
        schema = CoverSchema(many=True)

        try:
            data = schema.dump(covers.items)
            return {"success": True, "data": data}
        except ValidationError as error:
            return {"success": False, "errors": error}, 400
