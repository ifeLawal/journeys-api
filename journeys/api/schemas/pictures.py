from models import Pictures, ma


class PictureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pictures
