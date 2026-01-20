from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config import Config
from werkzeug.utils import secure_filename
import os
import uuid
from services.document_parser import DocumentParser
from services.chunker import ResumeChunker
from services.embedding_service import EmbeddingService
from services.vector_store import MongoVectorStore
from services.analyzer import ResumeAnalyzer
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
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

doc_parser = DocumentParser()
chunker = ResumeChunker()
embedding_service = EmbeddingService()
vector_store = MongoVectorStore()
analyzer = ResumeAnalyzer()

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

        chunks = chunker.chunk_by_sections(text)

        print(f"Generating Embeddings for {len(chunks)} chunks")
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_service.embed_batch(chunk_texts)

        print(f"Adding Chunks to Vector Store")
        stored_count = vector_store.add_chunks(resume_id, chunks, embeddings)

        return jsonify({
            "resume_id": resume_id,
            "filename": filename,
            "file_type": file_extension,
            "status": "embedded",
            "char_count": len(text),
            "word_count": len(text.split()),
            "chunks_created": len(chunks),
            "chunks_stored": stored_count,
            "chunks": [
                {
                    "section": chunk["section"],
                    "chunk_id": chunk["chunk_id"],
                    "word_count": chunk["word_count"],
                    "text": chunk["text"][:20]
                }
                for chunk in chunks
            ],
            "text_preview": text[:300] + "..."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    data = request.json

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    resume_id = data.get("resume_id")
    job_description = data.get("job_description")

    if not resume_id or not job_description:
        return jsonify({"error": "Missing resume_id or job_description"}), 400

    try:
        print(f"\nAnalyzing resume: {resume_id}")
        jd_embedding = embedding_service.embed_query(job_description)

        relevant_chunks = vector_store.search(
            query_embedding=jd_embedding,
            resume_id=resume_id,
            top_k=6
        )

        if not relevant_chunks:
            return jsonify({"error": "Resume not found"}), 404
        
        analysis = analyzer.analyze(relevant_chunks, job_description)

        if "error" in analysis:
            return jsonify(analysis), 500
        
        return jsonify({
            "resume_id": resume_id,
            "analysis": analysis,
            "chunks_analyzed": len(relevant_chunks)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting AI resume analyzer API...")
    app.run(debug=True, port=5000)