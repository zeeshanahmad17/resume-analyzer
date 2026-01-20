from pymongo import MongoClient
from typing import List, Dict
from config import Config

class MongoVectorStore:

    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client.resume_analyzer
        self.collection = self.db.resume_chunks

    def add_chunks(self, resume_id: str, chunks: List[Dict], embeddings: List[List[float]]):
        documents = [
            {
                "resume_id": resume_id,
                "content": chunk["text"],
                "embedding": embedding,
                "metadata": {
                    "section": chunk["section"],
                    "chunk_id": chunk["chunk_id"],
                    "word_count": chunk["word_count"],
                }
            }
            for chunk, embedding in zip(chunks, embeddings)
        ]
        
        self.collection.delete_many({"resume_id": resume_id})

        result = self.collection.insert_many(documents)
        return len(result.inserted_ids)

    def search(self, query_embedding: List[float], resume_id: str, top_k: int = 5) -> List[Dict]:
        """Vector search with MongoDB filter (requires 10s index sync wait)"""
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 100,
                    "limit": top_k,
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
        
        try:
            results = list(self.collection.aggregate(pipeline))
                
        except Exception as e:
            print(f"[VectorStore] ERROR: {e}")
            return []

        return [
            {
                "text": doc["content"],
                "metadata": doc["metadata"],
                "score": doc["score"]
            }
            for doc in results
        ]

    def get_resume_chunks(self, resume_id: str) -> List[Dict]:
        chunks = list(self.collection.find(
            {"resume_id": resume_id},
            {"_id": 0, "content": 1, "metadata": 1}
        ))

        return chunks

    def delete_resume(self, resume_id: str):
        result = self.collection.delete_many({"resume_id": resume_id})
        return result.deleted_count

    def close(self):
        self.client.close()