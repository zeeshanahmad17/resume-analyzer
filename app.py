from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from werkzeug.utils import secure_filename
import os
import uuid
from services.document_parser import DocumentParser

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

doc_parser = DocumentParser()

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Check against Config.ALLOWED_EXTENSIONS
    file_extension = file.filename.lower().split('.')[-1]
    if file_extension not in Config.ALLOWED_EXTENSIONS:
        return jsonify({
            "error": f"Invalid file format. Allowed formats: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        }), 400

    try:
        filename = secure_filename(file.filename)
        resume_id = str(uuid.uuid4())
        filepath = os.path.join(UPLOAD_FOLDER, f'{resume_id}_{filename}')
        file.save(filepath)

        # Validate Document
        if not doc_parser.validate_file(filepath):
            os.remove(filepath)
            return jsonify({"error": "Invalid file"}), 400
        
        text = doc_parser.extract_content(filepath)

        if not text or len(text) < 50:
            return jsonify({"error": "Could not extract text from file"}), 400

        return jsonify({
            "resume_id": resume_id,
            "filename": filename,
            "status": "text_extracted",
            "char_count": len(text),
            "word_count": len(text.split()),
            "text_preview": text[:300] + "..."
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting AI resume analyzer API...")
    app.run(debug=True, port=5000)