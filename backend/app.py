from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.model import predict_url

app = Flask(__name__)

# Allow Chrome extension
CORS(app, resources={r"/*": {"origins": "*"}})

# Handle preflight request (VERY IMPORTANT)
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

@app.route("/check", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    prediction, confidence = predict_url(url)

    return jsonify({
        "result": "phishing" if prediction == 1 else "safe",
        "confidence": confidence
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)