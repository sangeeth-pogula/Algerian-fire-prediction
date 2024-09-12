from flask import Flask, request, jsonify, render_template
from dependencies import *

application = Flask(__name__)
app = application

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON data from request
        data = request.get_json()
        if not data:
            logging.warning("No data received in POST request.")
            return jsonify({'error': 'No data received'}), 400

        # Convert data to DataFrame
        df = pd.DataFrame([data])
        prediction = predict_FWI(df)
        
        # Return the prediction as JSON
        return jsonify({'prediction': prediction})
    except Exception as e:
        logging.error(f"Error in /predict endpoint: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

if __name__ == "__main__":
    app.run(debug="True")