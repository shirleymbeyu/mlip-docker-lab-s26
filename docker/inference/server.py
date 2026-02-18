from flask import Flask, request, jsonify
import numpy as np
import joblib
import os
from datetime import datetime

app = Flask(__name__)

MODEL_PATH = "/app/models/wine_model.pkl"
LOG_PATH = "/app/logs/predictions.log"

model = None

# DONE: Load the trained model from the shared volume
try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")
except Exception as e:
    print(f"Warning: Could not load model from {MODEL_PATH}: {e}")
    model = None

# Wine feature names for reference (13 features):
# alcohol, malic_acid, ash, alcalinity_of_ash, magnesium, total_phenols,
# flavanoids, nonflavanoid_phenols, proanthocyanins, color_intensity,
# hue, od280/od315_of_diluted_wines, proline

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # DONE: Get the input array from the request JSON body
        data = request.get_json()
        features = data["input"]

        # DONE: Convert to numpy array, reshape for single prediction, and predict
        prediction = model.predict(np.array(features).reshape(1, -1))

        # Map prediction to wine class name
        wine_classes = {0: "class_0", 1: "class_1", 2: "class_2"}
        result = wine_classes.get(int(prediction[0]), "unknown")

        # DONE: Log the prediction to the bind-mounted log file
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} | input: {features} | prediction: {result}\n")
        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/')
def hello():
    return 'Welcome to the Wine Classifier - MLIP S26 Docker Lab'

@app.route('/health')
def health():
    global model
    model_exists = os.path.exists(MODEL_PATH)
    return jsonify({
        "status": "healthy" if model_exists else "model not found",
        "model_loaded": model is not None
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
