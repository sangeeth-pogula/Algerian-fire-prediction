from flask import Flask, request, jsonify, render_template

application = Flask(__name__)
app = application

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    pass

if __name__ == "__main__":
    app.run(debug="True")