import os, sys
from flask import Flask, render_template
from utils import appUtils


appUtils.init()
gateway = appUtils.initGateway()
app = Flask(__name__, static_url_path = "/", static_folder = "./../frontend/")

if (not gateway):
    sys.exit()


@app.route("/")
def index():
    return render_template("/index.html")

if (__name__ == "__main__" ):
    debug = os.getenv('DEBUG')
    if (debug):
        app.run(debug=True)
    else:
        app.run(debug=False)

from routes import userRoute, gameRoute, eventRoute, commentRoute, voteRoute