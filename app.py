import os
import tempfile
from socket import gethostbyname, gethostname

import pymysql
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, desc

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


with app.app_context():
    players = db.session.execute(db.select(Player)).scalars
    print(players)


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


@app.route("/api/register", methods=["POST"])
def register_user():
    assert request.method == "POST"

    username = request.body["username"]
    email = request.body["email"]

    # handle player already exists case
    # check if autoincrement pk works
    player = Player(username=username, email=email)
    # player.username = username
    # player.email = email
    db.session.add(player)
    db.session.commit()


@app.route("/api/session", methods=["GET", "POST"])
def session():
    if request.method == "GET":
        username = request.body["username"]

        player_id = db.get_or_404(db.select(Player).filter_by(username=username)).id
        player_sessions = db.select(Session).filter_by(player_id=player_id)

        # join session_stats with session
        session_stats = db.first_or_404(
            db.select(player_sessions, SessionStats)
            .join(SessionStats)
            .order_by(-SessionStats.session_end)
            # ).order_by(desc(SessionStats.session_end))
        )

        return (session_stats, 200)

    elif request.method == "POST":
        # extract input data
        initial_image = request.files["initial_image"]
        final_image = request.files["final_image"]
        stats = request.body["session_stats"]
        username = request.body["username"]

        # upload image to S3
        initial_image_url = ""
        final_image_url = ""

        # check if player exists
        player = db.get_or_404(db.select(Player).filter_by(username=username))

        # commit session stats
        session_stats = SessionStats()
        session_stats.session_start = stats.session_start
        session_stats.session_end = stats.session_end
        session_stats.initial_image = stats.initial_image
        session_stats.final_image = stats.final_image
        session_stats.f = stats.f
        session_stats.b = stats.b
        session_stats.l = stats.l
        session_stats.r = stats.r
        session_stats.fl = stats.fl
        session_stats.fr = stats.fr
        session_stats.bl = stats.bl
        session_stats.br = stats.br
        session_stats.s = stats.s
        db.session.add(session_stats)
        db.session.commit()

        # get session_id

        # commit the session
        session = Session()
        session.player_id = player.id
        session.session_id = session_stats.id
        db.session.add(session)
        db.session.commit()

        return ({"session_id": session.id}, 200)


if __name__ == "__main__":
    host = gethostname()
    addr = gethostbyname(host)
    app.run(debug=True, host=addr)
