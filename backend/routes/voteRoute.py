import os, json, time, datetime
from flask import Flask, render_template, request, jsonify, Response
from app import app, gateway, appUtils

@app.route("/api/vote/date/union/<int:eventId>")
def getOverlappingDates(eventId):
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 301)
    result = gateway.getOverlappingDates(username, eventId)
    return Response(json.dumps(result), status = 200, mimetype='application/json')

@app.route("/api/vote/date/", methods=['POST'])
def voteDate():
    username = appUtils.getUsernameFromVerification(request, gateway)
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

    etime = None
    if (appUtils.sanitize(date)):
        etime = appUtils.createDate(date)

    if (appUtils.sanitize(hours) and appUtils.sanitize(eventId) and etime != None):
        gateway.voteDate(username, eventId, date, hours)
        return Response("", status = 200)
    return Response("", status = 400)

@app.route("/api/vote/date/<int:eventId>")
def getDateVotes(eventId):
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 301)
    result = gateway.getEventDateVotes(username, eventId)
    return Response(json.dumps(result), status = 200, mimetype='application/json')
