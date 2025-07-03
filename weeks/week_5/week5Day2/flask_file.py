import flask
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pickle
import os
import model_creator
# Create Flask app
app = Flask(__name__)

# Load model for prediction
def load_model():
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# Define prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from POST request
    data = request.get_json()

    # Check if data is in correct format
    if not data or 'features' not in data:
        return jsonify({'error': 'No valid features provided'}), 400

    # Convert data to numpy array for prediction
    try:
        features = np.array(data['features']).reshape(1, -1)
        model = load_model()
        prediction = model.predict(features).tolist()
        prediction_proba = model.predict_proba(features).tolist()

        return jsonify({
            'prediction': prediction,
            'probability': prediction_proba
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)