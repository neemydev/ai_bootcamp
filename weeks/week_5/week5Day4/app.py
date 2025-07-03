from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import joblib

app = Flask(__name__)
run_with_ngrok(app)
model = joblib.load('model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = data['features']
    pred = model.predict([features])[0]
    return jsonify({'prediction': int(pred)})

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run()
