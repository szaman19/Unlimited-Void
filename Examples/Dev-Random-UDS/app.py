from flask import Flask, request, Response


app = Flask(__name__)


@app.route("/data", methods=["GET"])
def get_data():
    num_bytes = request.args.get("num_bytes", default=1024, type=int)
    with open("/dev/random", "rb") as f:
        binary_data = f.read(num_bytes)
    return Response(binary_data, mimetype="application/octet-stream")
