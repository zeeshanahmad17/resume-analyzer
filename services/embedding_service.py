import google.generativeai as genai
import hashlib
from typing import List
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

class EmbeddingService:
    def __init__(self):
        self.model_name = "models/text-embedding-004"
        self.dimensions = 768
        self.cache = {}

    def embed_text(self, text: str) -> List[float]:
        cache_key = self._get_cache_key(text)
        if cache_key in self.cache:
            print(f"Using cached embedding for {text[:50]}")
            return self.cache[cache_key]

        try:
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            embedding = result['embedding']

            self.cache[cache_key] = embedding
            print(f"Generated embedding for {text[:50]} with length {len(embedding)}")
            return embedding

        except Exception as e:
            print(f"Failed to generate embedding for {text[:50]}: {e}")
            raise ValueError(f"Failed to generate embedding: {str(e)}")

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = []

        for text in texts:
            embeddings.append(self.embed_text(text))

        return embeddings

    def embed_query(self, query: str) -> List[float]:
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"
            )
            embedding = result['embedding']

            return embedding
        
        except Exception as e:
            print(f"Failed to generate embedding for {query[:50]}: {e}")
            raise ValueError(f"Failed to generate embedding: {str(e)}")

    def get_dimensions(self) -> int:
        return self.dimensions

    def _get_cache_key(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()