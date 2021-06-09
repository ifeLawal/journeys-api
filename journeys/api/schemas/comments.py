from models import Comments, ma


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comments
