from flask import Flask, request, jsonify, render_template

application = Flask(__name__)
app = application

@app.route("/", methods=["GET"])
def index():
    return "<h1>Hello World</h1>"

if __name__ == "__main__":
    app.run(debug="True")