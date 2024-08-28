from flask import Blueprint, render_template, request, redirect, url_for, current_app
from favourites import favourite_songs
from werkzeug.utils import secure_filename
import os

my_view = Blueprint("my_view", __name__)

form_open = False

@my_view.route("/")
def index():
    return render_template("index.html")

@my_view.route("/page2", methods=["GET", "POST"])
def page2():
    return render_template("page2.html", favourite_songs = favourite_songs, form_open = form_open)

@my_view.route("/addBand", methods=["GET", "POST"])
def addBand():
    global form_open
    if request.method == "POST":
        file = request.files['add_img']
        filename = None
        if file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        form_open = False
        favourite_songs.append({ 
            "artist": request.form["add_artist"],
            "album": request.form["add_album"],
            "song": request.form["add_song"],
            "rating": request.form["add_rating"],
            "image": filename
        })
    return render_template("page2.html", favourite_songs = favourite_songs, form_open = form_open)

@my_view.route("/filterBands", methods=["GET", "POST"])
def filterBands():
    global favourite_songs
    filter_bands = []
    if request.method == "POST":
        filter_num = request.form["added_rating"]
        if filter_num == "All":
            filter_bands = favourite_songs
        else:
            filter_bands = [song for song in favourite_songs if song["rating"] == filter_num]
    return render_template("page2.html", favourite_songs = filter_bands)

@my_view.route("/openForm")
def openForm():
    global form_open
    form_open = True
    return redirect(url_for("my_view.page2"))

@my_view.route("/delete", methods=["POST"])
def delete():
    global favourite_songs
    song_to_delete = request.form.get("song")
    favourite_songs = [i for i in favourite_songs if i["song"] != song_to_delete]
    return redirect(url_for("my_view.page2"))