from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.resume_analyzer

# Check for the specific resume
resume_id = "b14a7edf-f394-407e-aa6f-3d69b66ef869"
chunks = list(db.resume_chunks.find({'resume_id': resume_id}))

print(f"Checking resume: {resume_id}")
print(f"Found {len(chunks)} chunks in MongoDB")

if chunks:
    print("\nChunk details:")
    for i, chunk in enumerate(chunks, 1):
        print(f"  {i}. Section: {chunk.get('metadata', {}).get('section', 'Unknown')}")
        print(f"     Has embedding: {'embedding' in chunk}")
        print(f"     Embedding length: {len(chunk.get('embedding', []))}")
else:
    print("\n❌ NO DATA FOUND! The resume was not stored in MongoDB.")
    print("\nAll resumes in database:")
    all_docs = list(db.resume_chunks.find({}, {'resume_id': 1, '_id': 0}).limit(5))
    for doc in all_docs:
        print(f"  - {doc.get('resume_id', 'Unknown')}")
