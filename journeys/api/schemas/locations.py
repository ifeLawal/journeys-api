from models import Locations, ma


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Locations
