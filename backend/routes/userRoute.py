import os, json, time, datetime
from flask import Flask, render_template, request, jsonify, Response
from app import app, gateway, appUtils

def tryLogin(username, password):
    if (len(username) < 3 or len(username) < 3):
        return None
    token = gateway.login(username, password)
    return token

@app.route("/api/user/invite/", methods=['POST'])
def inviteUserToEvent():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 400)
    req = request.json

    targetUser = req.get('targetuser')
    eventId = req.get('eventid')
    if (not appUtils.sanitize({targetUser, eventId})):
        return Response("", status = 400)

    if (targetUser != None and eventId != None):
        gateway.inviteToEvent(username, targetUser, eventId)
        return Response("", status = 200)
    return Response("", status = 400)

@app.route("/api/user/find/", methods=['GET'])
def userfind():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 400)

    args = request.args.to_dict()
    if ('game' in args and 'event' in args):
        print(args)
    elif ('search' in args):
        searchstring = args['search']
        if (searchstring == '*'):
            searchstring = ''
        if (not appUtils.containsEvil(searchstring)):
            result = gateway.searchUsers(searchstring, username)
            return Response(json.dumps(result), status = 200, mimetype='application/json') 
    return Response("", status = 400)

@app.route("/api/user/friend/request", methods=['POST'])
def friendRequest():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 400)

    req = request.json
    friend = req.get('friend')
    accepted = req.get('accepted')

    print('moi!:', req)

    if (appUtils.sanitize({friend, accepted})):
        if (len(friend) < 3):
            return Response("", status = 203)
        if (int(accepted) == 1):
            gateway.newRelation(username, friend, 1)
        #else:
        #   gateway.removeRelation(friend, username)
    return Response("", status = 200)

@app.route("/api/user/friend/request", methods=['GET'])
def getFriendRequests():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 400)

    result = gateway.getFriendRequests(username)
    if (len(result) == 0):
        return Response("", status = 204)
    return Response(json.dumps(result), status = 200, mimetype='application/json')

@app.route("/api/login", methods=['POST'])
def login():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (username != None):
        print(username + ' logged in')
        return Response("", status = 200)

    req = request.json
    username = req.get('username')
    password = req.get('password')

    if (username == None or password == None):
        return Response("", status = 401)

    if (appUtils.sanitize({username, password})):
        token = tryLogin(req["username"], req["password"])
        if (token != None):
            result = '{"bearer":"' + token + '"}'
            return Response(result, status = 200, mimetype='application/json')
        return Response("", status = 401)
    return Response("", status = 400)

@app.route("/api/login/new", methods=['POST'])
def newuser():
    req = request.json
    username = req.get('username')
    password = req.get('password')

    print(req)

    if (appUtils.sanitize({username, password})):
        token = gateway.newUser(username, password)
        if (token != None):
            result = '{"bearer":"' + token + '"}'
            return Response(result, status = 200, mimetype='application/json')
        return Response("", status = 401)
    return Response("", status = 400)
