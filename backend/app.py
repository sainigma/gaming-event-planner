from flask import Flask, render_template, request, jsonify, Response
from gateways.SQLiteGateway import SQLiteGateway
from controllers.GameDBController import GameDBController
from dotenv import load_dotenv

load_dotenv()
gameDB = GameDBController()
gateway = SQLiteGateway(gameDB)


def tryLogin(username, password):
    if (len(username) < 3 or len(username) < 3):
        return -1
    return 'afdsjlkasjfldsaf'

app = Flask(__name__, static_url_path="", static_folder="./../frontend/")

@app.route("/")
def index():
    return render_template("index.html")

# /api/vote
# /api/new/event
# /api/new/user
# /api/comment
#

@app.route("/api/login", methods=['POST'])
def login():
    req = request.json

    if ("username" in req and "password" in req):
        verification = tryLogin(req["username"], req["password"])
        if (verification != -1):
            result = "{'verification':'adfsklhjadsfkj'}"
            return Response(result, status = 200, mimetype='application/json')
        return Response("", status = 401)
    return Response("", status = 400)

if (__name__ == "__main__" ):
    app.run(debug=True)