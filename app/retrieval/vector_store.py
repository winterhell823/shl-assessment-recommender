import json
import os
from pathlib import Path
import numpy as np

# Lazy imports to make server startup fast if vector store is not initialized or used
_model = None
_faiss = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_faiss():
    global _faiss
    if _faiss is None:
        import faiss
        _faiss = faiss
    return _faiss


class VectorStore:
    def __init__(self, index_path: str = "app/data/faiss.index", metadata_path: str = "app/data/faiss_metadata.json"):
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.index = None
        self.metadata = []
        self._load_store()

    def _load_store(self):
        if not self.index_path.exists() or not self.metadata_path.exists():
            print("Vector store files not found. Semantic search is disabled.")
            return

        try:
            faiss = get_faiss()
            self.index = faiss.read_index(str(self.index_path))
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
            print(f"Loaded FAISS index with {len(self.metadata)} items.")
        except Exception as e:
            print(f"Error loading vector store: {e}")
            self.index = None
            self.metadata = []

    def search(self, query: str, limit: int = 10) -> list[dict]:
        if self.index is None or not self.metadata or not query.strip():
            return []

        try:
            model = get_model()
            # Encode query
            query_vector = model.encode([query], convert_to_numpy=True).astype("float32")
            
            # Normalize vector for Cosine Similarity (since we use IndexFlatIP)
            faiss = get_faiss()
            faiss.normalize_L2(query_vector)

            # Search FAISS index
            k = min(limit, len(self.metadata))
            distances, indices = self.index.search(query_vector, k)

            results = []
            for idx in indices[0]:
                if idx < 0 or idx >= len(self.metadata):
                    continue
                
                item = self.metadata[idx]
                
                # Standardize url/link field
                if "link" in item and "url" not in item:
                    item["url"] = item["link"]
                
                results.append(item)

            return results
        except Exception as e:
            print(f"Error during vector search: {e}")
            return []


def item_to_text(item: dict) -> str:
    parts = []
    
    # Text fields
    for field in ["name", "description", "test_type", "remote", "adaptive"]:
        val = item.get(field)
        if val:
            parts.append(str(val))
            
    # List or text fields
    for field in ["skills", "keywords", "keys", "job_levels", "duration"]:
        val = item.get(field)
        if isinstance(val, list):
            parts.extend([str(x) for x in val if x])
        elif val:
            parts.append(str(val))
            
    return " ".join(parts).strip()
