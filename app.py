from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config

app = Flask(__name__)
CORS(app)

try:
    Config.validate()
    print("Configuration validated successfully")
except ValueError as e:
    print(f"Configuration error: {e}")
    exit(1)

@app.route('/')
def index():
    return jsonify({
        "status": "AI resume analyzer API running",
        "version": "1.0.0",
        "endpoints": [
            "/api/upload-resume",
            "/api/analyze",
            "/api/quota-status"
        ]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    print("Starting AI resume analyzer API...")
    app.run(debug=True, port=5000)