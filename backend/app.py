from flask import Flask, render_template, jsonify

app = Flask(__name__, static_url_path="", static_folder="./../frontend/")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/login", methods=['POST'])
def login():
    data = request.form
    result = {
        "status":200,
        "verification":"adfsklhjadsfkj"
    }
    return jsonify(result)

app.run(debug=True)