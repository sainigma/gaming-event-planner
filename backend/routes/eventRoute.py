import os, json, time, datetime
from flask import Flask, render_template, request, jsonify, Response
from app import app, gateway, appUtils
    
@app.route("/api/event/<int:eventId>")
def getEvent(eventId):
    event = gateway.getEvent(eventId)
    return Response(json.dumps(event), status = 200, mimetype='application/json')

@app.route("/api/event/invitations/<int:eventId>", methods=['POST'])
def parseInvitations(eventId):
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 301)

    req = request.json
    invitationStatus = req.get("status")
    if (appUtils.sanitize({invitationStatus, eventId})):
        gateway.parseInvitations(username, eventId, invitationStatus)
        return Response("", status = 200)
    return Response("", status = 400)    

@app.route("/api/event/new", methods=['POST'])
def newEvent():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 301)
    
    req = request.json
    eventName = req.get("name")
    gameId = req.get("gameId")
    groupId = req.get("groupId")
    ends = req.get("ends")

    etime = 0
    if (appUtils.sanitize({ends})):
        etime = appUtils.createDate(ends)

    if (appUtils.sanitize({eventName, gameId, groupId}) and etime != None):
        gateway.newEvent(eventName, gameId, username, groupId, etime)
        return Response("", status = 200)
    return Response("", status = 400)

@app.route("/api/event/update", methods=['POST'])
def updateEvent():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 301)
    
    req = request.json
    eventId = req.get('eventId')
    description = req.get('description')
    ends = req.get('date')
    optlower = req.get('optlower')
    optupper = req.get('optupper')

    etime = 0
    if (appUtils.sanitize({ends})):
        etime = appUtils.createDate(ends)

    if (appUtils.sanitize({description, optlower, optupper, eventId}) and etime != None):
        gateway.updateEvent(username, eventId, description, etime, optlower, optupper)
        return Response("", status = 200)
    return Response("", status = 400)

@app.route("/api/event/all")
def getEvents():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 400)
    events = gateway.getEvents(username)
    return Response(json.dumps(events), status = 200, mimetype='application/json')
