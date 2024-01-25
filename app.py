import os
import tempfile
from socket import gethostbyname, gethostname

import pymysql
from dotenv import load_dotenv
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError

from predict import KeeperVisionModel

load_dotenv()

KPModel = KeeperVisionModel()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

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
db.init_app(app)

with app.app_context():
    db.reflect()


class Player(db.Model):
    __table__ = db.metadata.tables["Player"]


class SessionStats(db.Model):
    __table__ = db.metadata.tables["SessionStats"]


class Session(db.Model):
    __table__ = db.metadata.tables["Session"]


# class Player(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.Text, nullable=False, unique=True)
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
#         primary_key=True
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


@app.route("/api/register", methods=["GET", "POST"])
def register_user():
    # check if user specified by 'username' exists
    if request.method == "GET":
        # parse request content
        content = request.json
        username = content["username"]
        # check if player exists
        player = db.session.execute(
            db.select(Player).filter_by(username=username)
        ).first()
        # generate response
        if not player:
            return ({"message": f"Player '{username}' does not exist."}, 404)
        return ({"id": player[0].id}, 200)

    # add user specified by 'username' and 'email' to db
    elif request.method == "POST":
        # parse request content
        content = request.json
        username = content["username"]
        email = content["email"]

        # add player to db
        try:
            player = Player(username=username, email=email)
            db.session.add(player)
            db.session.commit()
        except SQLAlchemyError as e:
            return ({"message": str(e.__dict__["orig"])}, 400)

        # generate response
        return ({"id": player.id}, 200)


@app.route("/api/session", methods=["GET", "POST"])
def session():
    if request.method == "GET":
        # parse request content
        content = request.json
        username = content["username"]

        # check if player exists
        player = db.session.execute(
            db.select(Player).filter_by(username=username)
        ).first()
        if not player:
            return ({"message": f"Player '{username}' does not exist."}, 404)

        player_id = player[0].id
        # get player_sessions exists
        player_sessions = db.select(Session).filter_by(player_id=player_id).subquery()

        # join session_stats with session
        session_stats = db.session.execute(
            db.select(player_sessions, SessionStats)
            .join(SessionStats)
            .order_by(-SessionStats.session_end)
        ).all()

        print(session_stats)

        return ({"session_stats": len(session_stats)}, 200)

    elif request.method == "POST":
        # extract input data
        # initial_image = request.files["initial_image"]
        # final_image = request.files["final_image"]
        content = request.json
        username = content["username"]
        stats = json.loads(content["session_stats"])

        # upload image to S3
        initial_image_url = "test1"
        final_image_url = "test2"

        # check if player exists
        player = db.session.execute(
            db.select(Player).filter_by(username=username)
        ).first()
        if not player:
            return ({"message": f"Player '{username}' does not exist."}, 404)

        # commit session stats
        session_stats = SessionStats()
        session_stats.session_start = stats.get("session_start")
        session_stats.session_end = stats.get("session_end")
        session_stats.initial_image = initial_image_url
        session_stats.final_image = final_image_url
        session_stats.f = stats.get("f")
        session_stats.b = stats.get("b")
        session_stats.l = stats.get("l")
        session_stats.r = stats.get("r")
        session_stats.fl = stats.get("fl")
        session_stats.fr = stats.get("fr")
        session_stats.bl = stats.get("bl")
        session_stats.br = stats.get("br")
        session_stats.s = stats.get("s")
        db.session.add(session_stats)
        db.session.commit()

        # commit the session
        session = Session(session_id=session_stats.id, player_id=player[0].id)
        db.session.add(session)
        db.session.commit()

        return ({"id": session.session_id}, 200)


if __name__ == "__main__":
    host = gethostname()
    addr = gethostbyname(host)
    app.run(debug=True, host=addr)
