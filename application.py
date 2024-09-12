from flask import Flask, request, jsonify, render_template

application = Flask(__name__)
app = application

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug="True")