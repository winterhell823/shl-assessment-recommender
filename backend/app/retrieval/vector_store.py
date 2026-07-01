import json
import os
import threading
from pathlib import Path
import numpy as np

# Keep memory usage low by only loading the embedding model when semantic search is actually needed.
_model = None
_faiss = None
_model_warmup_started = False


def get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as exc:
            print(f"Embedding model load failed: {exc}")
            _model = False
    return _model


def get_faiss():
    global _faiss
    if _faiss is None:
        try:
            import faiss
            _faiss = faiss
        except Exception as exc:
            print(f"FAISS import failed: {exc}")
            _faiss = False
    return _faiss


def warmup_model():
    global _model_warmup_started
    if _model_warmup_started or os.environ.get("SHL_DISABLE_WARMUP", "1") == "1":
        return
    _model_warmup_started = True
    try:
        model = get_model()
        if model is False:
            return
        model.encode(["warmup"], convert_to_numpy=True)
    except Exception:
        pass


class VectorStore:
    def __init__(self, index_path: str = "app/data/faiss.index", metadata_path: str = "app/data/faiss_metadata.json"):
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.index = None
        self.metadata = []
        self._load_store()
        if os.environ.get("SHL_DISABLE_WARMUP", "1") != "1":
            threading.Thread(target=warmup_model, daemon=True).start()

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

        model = get_model()
        if model is False:
            return []

        try:
            query_vector = model.encode([query], convert_to_numpy=True).astype("float32")

            faiss = get_faiss()
            if faiss is False:
                return []

            faiss.normalize_L2(query_vector)

            k = min(limit, len(self.metadata))
            distances, indices = self.index.search(query_vector, k)

            results = []
            for idx in indices[0]:
                if idx < 0 or idx >= len(self.metadata):
                    continue

                item = self.metadata[idx]
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
