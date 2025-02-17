from flask import Flask, request, jsonify, render_template
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
    return render_template("index.html")  # Serve the HTML page

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data from HTML
        features = [float(request.form[f"feature{i}"]) for i in range(13)]

        # Convert to numpy array and reshape
        features = np.array(features).reshape(1, -1)

        # Scale the input
        features_scaled = scaler.transform(features)

        # Make a prediction
        prediction = model.predict(features_scaled)

        return jsonify({"predicted_price": round(prediction[0], 2)})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
