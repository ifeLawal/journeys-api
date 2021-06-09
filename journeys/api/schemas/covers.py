from models import Covers, ma


class CoverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Covers
