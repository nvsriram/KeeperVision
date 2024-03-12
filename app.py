import tempfile
from json import loads
from socket import gethostbyname, gethostname

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from config import app
from db import Player, Session, SessionStats, db
from predict import KPModel
from upload import get_object_name, handle_upload


@app.route("/api/game", methods=["POST"])
def game():
    assert request.method == "POST"

    # process image and get idx
    file = request.files["image"]

    img_bytes = file.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(img_bytes)
        temp_img_path = tmp_file.name

    score, _, _ = KPModel.get_prediction(temp_img_path, is_game=True)
    print("score:", score)

    return {"score": str(score)}, 200


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


@app.route("/api/register/<username>", methods=["GET", "POST"])
def register_user(username):
    # check if player specified by 'username' exists
    if request.method == "GET":
        # parse request
        if not username:
            return ({"message": "'username' missing from url"}, 400)

        # check if player exists
        player_id = Player.exists(username)
        if not player_id:
            return ({"message": f"Player '{username}' does not exist."}, 404)

        # generate response
        return ({"id": player_id}, 200)

    # add player specified by 'username' and 'email' to db
    elif request.method == "POST":
        # parse request content
        if not username:
            return ({"message": "'username' missing from url"}, 400)
        content = request.json
        email = content.get("email")
        if not email:
            return ({"message": "'email' key missing from body"}, 400)

        try:
            # create player
            player = Player.create(username=username, email=email)
        except SQLAlchemyError as e:
            return ({"message": str(e.__dict__["orig"])}, 400)

        # generate response
        return ({"id": player.id}, 200)


@app.route("/api/session/<username>", methods=["GET", "POST"])
def session(username):
    if request.method == "GET":
        # parse request
        if not username:
            return ({"message": "'username' missing from url"}, 400)

        # check if player exists
        player_id = Player.exists(username)
        if not player_id:
            return ({"message": f"Player '{username}' does not exist."}, 404)

        # get session_stats associated with player
        session_stats = Session.get_player_stats(player_id)

        # generate response
        return ({"player_id": player_id, "session_stats": session_stats}, 200)

    elif request.method == "POST":
        # extract input data
        if not username:
            return ({"message": "'username' missing from url"}, 400)
        initial_image = request.files["initial_image"]
        final_image = request.files["final_image"]
        content = request.form
        stats = content.get("session_stats")
        if not stats:
            return ({"message": "'session_stats' key missing from body"}, 400)
        stats = loads(stats)

        # check if player exists
        player_id = Player.exists(username)
        if not player_id:
            return ({"message": f"Player '{username}' does not exist."}, 404)

        try:
            # create session stats
            session_stats = SessionStats.create(
                session_start=stats.get("session_start"),
                session_end=stats.get("session_end"),
                f=stats.get("f"),
                b=stats.get("b"),
                l=stats.get("l"),
                r=stats.get("r"),
                fl=stats.get("fl"),
                fr=stats.get("fr"),
                bl=stats.get("bl"),
                br=stats.get("br"),
                s=stats.get("s"),
            )

            # handle S3 image upload and session stats url update
            initial_image_url = get_object_name(
                "initial", player_id=player_id, session_id=session_stats.id
            )
            initial_res, initial_msg = handle_upload(initial_image, initial_image_url)
            if not initial_res:
                return ({"message": initial_msg}, 400)
            session_stats.initial_image = initial_msg

            final_image_url = get_object_name(
                "final", player_id=player_id, session_id=session_stats.id
            )
            final_res, final_msg = handle_upload(final_image, final_image_url)
            if not final_res:
                return ({"message": final_msg}, 400)
            session_stats.final_image = final_msg

            db.session.commit()

            # create session
            session = Session.create(session_id=session_stats.id, player_id=player_id)
        except SQLAlchemyError as e:
            return ({"message": str(e.__dict__["orig"])}, 400)

        # generate response
        return ({"id": session.session_id}, 200)


if __name__ == "__main__":
    host = gethostname()
    addr = gethostbyname(host)
    app.run(debug=True, host=addr)
