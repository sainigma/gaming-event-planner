import os, json
from flask import Flask, render_template, request, jsonify, Response
from gateways.SQLiteGateway import SQLiteGateway
from controllers.GameDBController import GameDBController
from dotenv import load_dotenv

# for running on venv
if (os.path.basename(os.getcwd()) == 'backend'):
    os.chdir('./..')

load_dotenv()
gameDB = GameDBController()
gateway = SQLiteGateway(gameDB)

def tryLogin(username, password):
    if (len(username) < 3 or len(username) < 3):
        return None
    token = gateway.login(username, password)
    return token

app = Flask(__name__, static_url_path = "/", static_folder = "./../frontend/")

@app.route("/")
def index():
    return render_template("/index.html")

# TODO routet
# /api/vote
# /api/event
# /api/user
# /api/user/new
# /api/user/friends
# /api/comment
# /api/game
#

def headerVerified():
    return True

@app.route("/api/event/new", methods=['POST'])
def newEvent():
    if (not headerVerified()):
        return Response("", status = 301)
    req = request.json
    eventName = req["name"]
    eventGame = req["gameId"]
    print(eventName)
    print(eventGame)
    # Muista sanitointi
    return Response("", status = 400)

@app.route("/api/game/find/<string:title>")
def gamefind(title):
    result = gameDB.findGames(title)    
    print(result)
    if (len(result) > 0):
        return Response(json.dumps(result), status = 200, mimetype='application/json')
    return Response("", status = 400)

@app.route("/api/login", methods=['POST'])
def login():
    req = request.json

    if ("username" in req and "password" in req):
        # Muista sanitointi
        token = tryLogin(req["username"], req["password"])
        if (token != None):
            result = '{"bearer":"' + token + '"}'
            return Response(result, status = 200, mimetype='application/json')
        return Response("", status = 401)
    return Response("", status = 400)

if (__name__ == "__main__" ):
    app.run(debug=True)