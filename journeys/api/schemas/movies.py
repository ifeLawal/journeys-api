from models import Movies, ma


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movies
