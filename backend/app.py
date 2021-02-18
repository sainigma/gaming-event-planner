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
# /api/event/all
# /api/user
# /api/user/new
# /api/user/friends
# /api/comment
# /api/game
#

def sanitize(params):
    def containsEvil(content):
        # tarkasta erikoismerkit
        return False

    for item in params:
        if (item == None or containsEvil(item)):
            return False
    return True

def getUsernameFromVerification(req):
    bearer = req.headers.get('Authorization')
    if (bearer == None):
        return None
    return gateway.verify(bearer)

@app.route("/api/event/<int:eventId>")
def getEvent(eventId):
    event = gateway.getEvent(eventId)
    return Response(json.dumps(event), status = 200, mimetype='application/json')

@app.route("/api/event/new", methods=['POST'])
def newEvent():
    username = getUsernameFromVerification(request)
    if (not username):
        return Response("", status = 301)
    
    req = request.json
    eventName = req.get("name")
    gameId = req.get("gameId")
    groupId = req.get("groupId")
    if (sanitize({eventName, gameId, groupId})):
        gateway.newEvent(eventName, gameId, username, groupId)
        return Response("", status = 200)
    return Response("", status = 400)

@app.route("/api/event/all")
def getEvents():
    username = getUsernameFromVerification(request)
    if (not username):
        return Response("", status = 400)
    events = gateway.getEvents(username)
    return Response(json.dumps(events), status = 200, mimetype='application/json')

@app.route("/api/game/find/<string:title>")
def gamefind(title):
    result = gameDB.findGames(title)    
    if (len(result) > 0):
        return Response(json.dumps(result), status = 200, mimetype='application/json')
    return Response("", status = 400)

@app.route("/api/login", methods=['POST'])
def login():
    username = getUsernameFromVerification(request)
    if (username != None):
        print(username + ' logged in')
        return Response("", status = 200)

    req = request.json
    username = req.get('username')
    password = req.get('password')

    if (sanitize({username, password})):
        token = tryLogin(req["username"], req["password"])
        if (token != None):
            result = '{"bearer":"' + token + '"}'
            return Response(result, status = 200, mimetype='application/json')
        return Response("", status = 401)
    return Response("", status = 400)

if (__name__ == "__main__" ):
    app.run(debug=True)