from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError

from journeys.api.schemas.comments import CommentSchema
from models import Comments

comments_namespace = Namespace("comments", description="Endpoint to retrieve Comments")


@comments_namespace.route("")
class CommentList(Resource):
    def get(self):
        comments = Comments.query.paginate(max_per_page=25)
        schema = CommentSchema(many=True)

        try:
            data = schema.dump(comments.items)
            return {"success": True, "data": data}
        except ValidationError as error:
            return {"success": False, "errors": error}, 400
