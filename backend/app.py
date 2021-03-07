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
    debug = True
    if (os.getenv('DEBUG') and os.getenv('DEBUG') == 0):
        debug = False
    app.run(debug=debug)

from routes import userRoute, gameRoute, eventRoute, commentRoute, voteRoute, groupRoute