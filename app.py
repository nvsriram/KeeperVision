from flask import Flask, request
from socket import gethostname
from predict import predict

app = Flask(__name__)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    assert request.method == "POST"

    # process image and get idx
    image = request.files["image"]
    idx, x, y = predict(image)

    return (
        {
            "idx": idx,
            "x": x,  # < 0 => left; > 0 => right
            "y": y,  # < 0 => back; > 0 => front
        },
        200,
    )


if __name__ == "__main__":
    app.run(debug=True, host=gethostname())
