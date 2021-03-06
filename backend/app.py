import os, json, time, datetime
from flask import Flask, render_template, request, jsonify, Response
from gateways.SQLiteGateway import SQLiteGateway
from utils import appUtils

appUtils.init()
gateway = SQLiteGateway()
app = Flask(__name__, static_url_path = "/", static_folder = "./../frontend/")

@app.route("/")
def index():
    return render_template("/index.html")

if (__name__ == "__main__" ):
    app.run(debug=True)

from routes import userRoute, gameRoute, eventRoute, commentRoute, voteRoute