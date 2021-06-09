from flask.globals import request
from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError
from werkzeug.datastructures import ImmutableMultiDict

from journeys.api.schemas.locations import LocationSchema
from journeys.api.utils.models import build_model_filters
from models import Locations

locations_namespace = Namespace(
    "locations", description="Endpoint to retrieve Locations"
)


@locations_namespace.route("")
class LocationList(Resource):
    def get(self):
        # q = query_args.pop("q", None)
        # field = str(query_args.pop("field", None))
        # filters = build_model_filters(model=locations, query=q, field=field)

        # locations = Locations.query.filter_by(**query_args).filter(*filters).all()
        address = request.args("address", "")
        args = []
        if address:
            for arg in request.args:
                if "name" not in arg:
                    filter = request.args.get(arg)
                    args.append((arg, filter))
            args = ImmutableMultiDict(args)
        else:
            args = request.args
        address = f"%{address}%"
        locations = (
            Locations.query.filter_by(**args)
            .filter(Locations.address.like(address))
            .paginate(max_per_page=25)
        )
        schema = LocationSchema(many=True)

        try:
            data = schema.dump(locations.items)
            return {"success": True, "data": data}
        except ValidationError as error:
            return {"success": False, "errors": error}, 400
