from flask.globals import request
from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError
from werkzeug.datastructures import ImmutableMultiDict

from journeys.api.schemas.locations import LocationSchema
from models import Locations

locations_namespace = Namespace(
    "locations", description="Endpoint to retrieve Locations"
)


@locations_namespace.route("")
class LocationList(Resource):
    def get(self):
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
