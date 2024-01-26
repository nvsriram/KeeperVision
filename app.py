import tempfile
from json import loads
from socket import gethostbyname, gethostname

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from config import app
from db import Player, Session, SessionStats, db
from predict import KPModel


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
    # check if player specified by 'username' exists
    if request.method == "GET":
        # parse request content
        content = request.json
        username = content["username"]
        
        # check if player exists
        player_id = Player.exists(username)
        if not player_id:
            return ({"message": f"Player '{username}' does not exist."}, 404)
        
        # generate response
        return ({"id": player_id}, 200)

    # add player specified by 'username' and 'email' to db
    elif request.method == "POST":
        # parse request content
        content = request.json
        username = content["username"]
        email = content["email"]

        # add player to db
        try:
            player_id = Player.create(username=username, email=email)
            # db.session.add(player)
            # db.session.commit()
        except SQLAlchemyError as e:
            return ({"message": str(e.__dict__["orig"])}, 400)

        # generate response
        return ({"id": player_id}, 200)


@app.route("/api/session", methods=["GET", "POST"])
def session():
    if request.method == "GET":
        # parse request content
        content = request.json
        username = content["username"]

        # check if player exists
        player_id = Player.exists(username)
        if not player_id:
            return ({"message": f"Player '{username}' does not exist."}, 404)

        # get session_stats associated with player
        # player_sessions = db.select(Session).filter_by(player_id=player_id).subquery()
        # session_stats = db.session.execute(
        #     db.select(player_sessions, SessionStats)
        #     .join(SessionStats)
        #     .order_by(-SessionStats.session_end)
        # ).all()
        session_stats = Session.get_player_stats(player_id)

        # generate response
        return ({"session_stats": session_stats}, 200)

    elif request.method == "POST":
        # extract input data
        # initial_image = request.files["initial_image"]
        # final_image = request.files["final_image"]
        content = request.json
        username = content["username"]
        stats = loads(content["session_stats"])

        # upload image to S3
        initial_image_url = "test1"
        final_image_url = "test2"

        # check if player exists
        player_id = Player.exists(username)
        if not player_id:
            return ({"message": f"Player '{username}' does not exist."}, 404)

        # commit session stats
        session_stats_id = SessionStats.create(
            session_start= stats.get("session_start"),
            session_end = stats.get("session_end"),
            initial_image = initial_image_url,
            final_image = final_image_url,
            f = stats.get("f"),
            b = stats.get("b"),
            l = stats.get("l"),
            r = stats.get("r"),
            fl = stats.get("fl"),
            fr = stats.get("fr"),
            bl = stats.get("bl"),
            br = stats.get("br"),
            s = stats.get("s")
        )

        # commit the session
        session_id = Session.create(session_id=session_stats_id, player_id=player_id)

        return ({"id": session_id}, 200)


if __name__ == "__main__":
    host = gethostname()
    addr = gethostbyname(host)
    app.run(debug=True, host=addr)
