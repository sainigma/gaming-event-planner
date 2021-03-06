import os, json, time, datetime
from flask import Flask, render_template, request, jsonify, Response
from app import app, gateway, appUtils

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