from flask_restx import Namespace, Resource
from marshmallow.exceptions import ValidationError

from journeys.api.schemas.comments import CommentSchema
from journeys.api.utils.models import build_model_filters
from models import Comments

comments_namespace = Namespace("comments", description="Endpoint to retrieve Comments")


@comments_namespace.route("")
class CommentList(Resource):
    def get(self):
        # q = query_args.pop("q", None)
        # field = str(query_args.pop("field", None))
        # filters = build_model_filters(model=comments, query=q, field=field)

        # comments = Comments.query.filter_by(**query_args).filter(*filters).all()
        comments = Comments.query.paginate(max_per_page=25)
        schema = CommentSchema(many=True)

        try:
            data = schema.dump(comments.items)
            return {"success": True, "data": data}
        except ValidationError as error:
            return {"success": False, "errors": error}, 400
