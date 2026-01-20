from pymongo import MongoClient
from dotenv import load_dotenv
import os
from services.embedding_service import EmbeddingService

load_dotenv()

# Connect
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.resume_analyzer
collection = db.resume_chunks

# Generate a test query embedding
embedding_service = EmbeddingService()
job_desc = "Full Stack Developer"
query_embedding = embedding_service.embed_query(job_desc)

print(f"Query embedding generated: {len(query_embedding)} dimensions")

# Test the exact pipeline
resume_id = "b14a7edf-f394-407e-aa6f-3d69b66ef869"

pipeline = [
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": query_embedding,
            "numCandidates": 100,
            "limit": 5,
            "filter": {
                "resume_id": resume_id
            }
        }
    },
    {
        "$project": {
            "content": 1,
            "metadata": 1,
            "score": {
                "$meta": "vectorSearchScore"
            }
        }
    }
]

print(f"\nSearching for resume: {resume_id}")
print("Running vector search...")

try:
    results = list(collection.aggregate(pipeline))
    print(f"\n✅ Found {len(results)} results!")
    
    if results:
        for i, doc in enumerate(results, 1):
            print(f"\n  Result {i}:")
            print(f"    Section: {doc.get('metadata', {}).get('section', 'Unknown')}")
            print(f"    Score: {doc.get('score', 'N/A')}")
            print(f"    Text: {doc.get('content', '')[:50]}...")
    else:
        print("\n❌ No results returned by vector search!")
        print("\nDebug: Testing without filter...")
        pipeline_no_filter = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 100,
                    "limit": 5
                }
            },
            {
                "$project": {
                    "content": 1,
                    "metadata": 1,
                    "resume_id": 1,
                    "score": {
                        "$meta": "vectorSearchScore"
                    }
                }
            }
        ]
        results_no_filter = list(collection.aggregate(pipeline_no_filter))
        print(f"Without filter: Found {len(results_no_filter)} results")
        if results_no_filter:
            print("Resume IDs found:")
            for doc in results_no_filter[:3]:
                print(f"  - {doc.get('resume_id', 'Unknown')}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
