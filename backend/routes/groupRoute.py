import os, json, time, datetime
from flask import Flask, render_template, request, jsonify, Response
from app import app, gateway, appUtils

@app.route("/api/group/request", methods=['POST'])
def joinGroup():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 400)
    req = request.json

    targetGroup = req.get('group')
    if (not appUtils.sanitize({targetGroup})):
        return Response("", status = 400)

    if (targetGroup != None):
        result = gateway.joinGroup(username, targetGroup)
        if (result):
            return Response("", status = 201)
        return Response("", status = 200)
    return Response("", status = 400)

@app.route("/api/group/request", methods=['GET'])
def getRequests():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 400)
    
    requests = gateway.getGroupRequests(username)
    return Response(json.dumps(requests), status = 200, mimetype='application/json')

@app.route("/api/group/parserequest", methods=['POST'])
def parseRequest():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 400)
    req = request.json

    targetuser = req.get('user')
    targetgroup = req.get('group')
    accepted = req.get('accepted')

    if (appUtils.sanitize({targetuser, targetgroup, accepted})):
        if (int(accepted) == 1):
            gateway.addToGroup(username, targetuser, targetgroup)
            return Response("", status = 200)
        else:
            print('not accepted')
    return Response("", status = 400)

@app.route("/api/group/all")
def getGroups():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 400)

    groups = gateway.getGroups(username)
    return Response(json.dumps(groups), status = 200, mimetype='application/json')