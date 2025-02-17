from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from flask_cors import CORS

# Load the trained model and scaler
model = joblib.load("boston_house_price_model.pkl")
scaler = joblib.load("scaler.pkl")

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route("/")
def home():
    return "Boston House Price Prediction API"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get data from Ionic frontend
        data = request.json
        features = data["features"]  # Expecting an array of feature values

        # Convert to numpy array and reshape
        features = np.array(features).reshape(1, -1)

        # Scale the input
        features_scaled = scaler.transform(features)

        # Make a prediction
        prediction = model.predict(features_scaled)

        return jsonify({"predicted_price": prediction[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
