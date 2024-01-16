import os
import tempfile
from socket import gethostbyname, gethostname

import pymysql
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from predict import KeeperVisionModel

KPModel = KeeperVisionModel()

app = Flask(__name__)


def get_database_uri():
    # ensure .env is setup properly
    username = os.getenv("DATABASE_USERNAME")
    if not username:
        raise RuntimeError(f"DATABASE_USERNAME is not set")
    password = os.getenv("DATABASE_PASSWORD")
    if not password:
        raise RuntimeError(f"DATABASE_PASSWORD is not set")
    host = os.getenv("DATABASE_HOST")
    if not host:
        raise RuntimeError(f"DATABASE_HOST is not set")
    dbname = os.getenv("DATABASE_NAME")
    if not dbname:
        raise RuntimeError(f"DATABASE_NAME is not set")

    return f"mysql+pymysql://{username}:{password}@{host}/{dbname}?charset=utf8mb4"


app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


# class Player(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.Text, nullable=False)
#     username = db.Column(db.Text)


# class SessionStats(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     session_start = db.Column(db.DateTime)
#     session_end = db.Column(db.DateTime)
#     initial_image = db.Column(db.Text)
#     final_image = db.Column(db.Text)
#     f = db.Column(db.Integer)
#     b = db.Column(db.Integer)
#     l = db.Column(db.Integer)
#     r = db.Column(db.Integer)
#     fl = db.Column(db.Integer)
#     fr = db.Column(db.Integer)
#     bl = db.Column(db.Integer)
#     br = db.Column(db.Integer)
#     s = db.Column(db.Integer)


# class Session(db.Model):
#     session_id = db.Column(db.ForeignKey(SessionStats.id), primary_key=True)
#     player_id = db.Column(
#         db.ForeignKey(Player.id),
#     )


@app.route("/api/predict", methods=["POST"])
def predict():
    assert request.method == "POST"

    # process image and get idx
    file = request.files["image"]

    img_bytes = file.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(img_bytes)
        temp_img_path = tmp_file.name

    idx, x, y = KPModel.get_prediction(temp_img_path)

    return (
        {
            "idx": idx,
            "x": x,  # < 0 => left; > 0 => right
            "y": y,  # < 0 => back; > 0 => front
        },
        200,
    )


@app.route("/api/session", methods=["GET", "POST"])
def session():
    if request.method == "GET":
        db.session.query()
    elif request.method == "POST":
        pass


if __name__ == "__main__":
    host = gethostname()
    addr = gethostbyname(host)
    app.run(debug=True, host=addr)
