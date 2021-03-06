import os, json, time, datetime
from flask import Flask, render_template, request, jsonify, Response
from app import app, gateway, appUtils

@app.route("/api/comment/<int:eventId>")
def getComments(eventId):
    # muista lisätä käyttäjän tarkistus
    result = gateway.getComments('', eventId)
    return Response(json.dumps(result), status = 200, mimetype='application/json')

@app.route("/api/comment/new", methods=['POST'])
def addComment():
    username = appUtils.getUsernameFromVerification(request, gateway)
    if (not username):
        return Response("", status = 301)
    req = request.json
    
    eventId = req.get("eventId")
    targetId = req.get("targetId")
    content = req.get("content")
    if (appUtils.sanitize({eventId, targetId, content})):
        gateway.addComment(username, content, eventId, targetId)
        return Response("", status = 200)
    return Response("", status = 400)