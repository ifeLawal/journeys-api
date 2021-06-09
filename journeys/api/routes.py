from flask import Blueprint, render_template

from models import Movies, Pictures

data = Blueprint("data", __name__)


@data.route("/")
def index():
    """Function to test the functionality of the API"""
    return "Hello, world!"


@data.route("/create", methods=["POST"])
def add_user():
    pass


@data.route("/img/picture/<picture_id>", methods=["GET"])
def render_image_from_picture_id(picture_id):
    picture = Pictures.query.filter_by(id=picture_id).first_or_404()
    file_location = picture.file_location
    return render_template("image.html", file_location=file_location)


@data.route("/img/movie/<movie_name>", methods=["GET"])
def render_image_from_movie_name(movie_name):
    movie = Movies.query.filter(Movies.name.like(f"%{movie_name}%")).first_or_404()
    picture = Pictures.query.filter_by(movie_id=movie.id).first_or_404()
    file_location = picture.file_location
    return render_template("image.html", file_location=file_location)
