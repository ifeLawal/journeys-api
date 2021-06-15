from flask import Blueprint, render_template

from models import Movies, Pictures

data = Blueprint("data", __name__)


@data.route("/")
def index():
    """Function to show the endpoints of the API"""
    return """
            <div style="padding:10px 0px 0px 20px;">
            <h3>Journeys API is up and running!</h3>
            <b>Currently we only have the R of the CRUD ecosystem operational.</b>
            <br>Some JSON endpoints:
            <br>/movies, /comments, /locations, /covers,
            <br>/pictures, /img/picture/<picture_id>, /img/movie/<letters_in_movie_name>,
            </div>
            """


@data.route("/img/picture/<picture_id>", methods=["GET"])
def render_image_from_picture_id(picture_id):
    # Test for retreiving the images in the database
    picture = Pictures.query.filter_by(id=picture_id).first_or_404()
    file_location = picture.file_location
    return render_template("image.html", file_location=file_location)


@data.route("/img/movie/<movie_name>", methods=["GET"])
def render_image_from_movie_name(movie_name):
    # Test for retreiving the images in the database
    movie = Movies.query.filter(Movies.name.like(f"%{movie_name}%")).first_or_404()
    picture = Pictures.query.filter_by(movie_id=movie.id).first_or_404()
    file_location = picture.file_location
    return render_template("image.html", file_location=file_location)
