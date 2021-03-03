import os, json, time
from flask import Flask, render_template, request, jsonify, Response
from gateways.SQLiteGateway import SQLiteGateway
from controllers.GameDBController import GameDBController
from dotenv import load_dotenv

# for running on venv
if (os.path.basename(os.getcwd()) == 'backend'):
    os.chdir('./..')

load_dotenv()
gateway = SQLiteGateway()

os.environ['TZ'] = 'Europe/Helsinki'
time.tzset()

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
# /api/user/new

def containsEvil(content):
    # muista tehdä kunnon tarkistus
    if ';' in str(content):
        return True
    return False

def sanitize(params):
    for item in params:
        if (item == None or containsEvil(item)):
            return False
    return True

def getUsernameFromVerification(req):
    bearer = req.headers.get('Authorization')
    if (bearer == None):
        return None
    return gateway.verify(bearer)

@app.route("/api/comment/<int:eventId>")
def getComments(eventId):
    # muista lisätä käyttäjän tarkistus
    result = gateway.getComments('', eventId)
    return Response(json.dumps(result), status = 200, mimetype='application/json')

@app.route("/api/vote/date/union/<int:eventId>")
def getOverlappingDates(eventId):
    username = getUsernameFromVerification(request)
    if (not username):
        return Response("", status = 301)
    result = gateway.getOverlappingDates(username, eventId)
    return Response(json.dumps(result), status = 200, mimetype='application/json')

@app.route("/api/vote/date/", methods=['POST'])
def voteDate():
    username = getUsernameFromVerification(request)
    if (not username):
        return Response("", status = 301)
    
    req = request.json
    hours = []
    for i in range(0, 24):
        hour = req.get(str(i))
        if (hour != None):
            hours.append(i)
    eventId = req.get('eventId')
    date = req.get('date')
    # Tarkasta että date on muotoa yyyy-mm-dd
    if (sanitize(hours) and sanitize(eventId) and sanitize(date)):
        print(hours)
        gateway.voteDate(username, eventId, date, hours)
        return Response("", status = 200)
    return Response("", status = 400)

@app.route("/api/vote/date/<int:eventId>")
def getDateVotes(eventId):
    username = getUsernameFromVerification(request)
    if (not username):
        return Response("", status = 301)
    result = gateway.getEventDateVotes(username, eventId)
    return Response(json.dumps(result), status = 200, mimetype='application/json')

@app.route("/api/comment/new", methods=['POST'])
def addComment():
    username = getUsernameFromVerification(request)
    if (not username):
        return Response("", status = 301)
    req = request.json
    
    eventId = req.get("eventId")
    targetId = req.get("targetId")
    content = req.get("content")
    if (sanitize({eventId, targetId, content})):
        gateway.addComment(username, content, eventId, targetId)
        return Response("", status = 200)
    return Response("", status = 400)
    
@app.route("/api/event/<int:eventId>")
def getEvent(eventId):
    event = gateway.getEvent(eventId)
    return Response(json.dumps(event), status = 200, mimetype='application/json')

@app.route("/api/event/invitations/<int:eventId>", methods=['POST'])
def parseInvitations(eventId):
    username = getUsernameFromVerification(request)
    if (not username):
        return Response("", status = 301)

    req = request.json
    invitationStatus = req.get("status")
    if (sanitize({invitationStatus, eventId})):
        gateway.parseInvitations(username, eventId, invitationStatus)
        return Response("", status = 200)
    return Response("", status = 400)
    

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

@app.route("/api/game/<int:gameId>")
def getGame(gameId):
    result = gateway.getGame(gameId)
    if (len(result) > 0):
        return Response(json.dumps(result), status = 200, mimetype='application/json')
    return Response("", status = 400)

@app.route("/api/game/find/<string:title>")
def gamefind(title):
    result = gateway.findGames(title)    
    if (len(result) > 0):
        return Response(json.dumps(result), status = 200, mimetype='application/json')
    return Response("", status = 400)

@app.route("/api/user/invite/", methods=['POST'])
def inviteUserToEvent():
    username = getUsernameFromVerification(request)
    if (not username):
        return Response("", status = 400)
    req = request.json
    print(req)
    targetUser = req.get('targetuser')
    eventId = req.get('eventid')
    if (targetUser != None and eventId != None):
        gateway.inviteToEvent(username, targetUser, eventId)
        return Response("", status = 200)
    return Response("", status = 400)

@app.route("/api/user/find/", methods=['GET'])
def userfind():
    username = getUsernameFromVerification(request)
    if (not username):
        return Response("", status = 400)

    args = request.args.to_dict()
    if ('game' in args and 'event' in args):
        print(args)
    elif ('search' in args):
        searchstring = args['search']
        if (searchstring == '*'):
            searchstring = ''
        if (not containsEvil(searchstring)):
            result = gateway.searchUsers(searchstring, username)
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