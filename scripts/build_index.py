import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.retrieval.catalog_loader import CatalogLoader
from app.retrieval.vector_store import item_to_text

def main():
    print("Loading catalog...")
    catalog = CatalogLoader().load()
    
    # Filter out empty or pagination entries (e.g. purely numeric names like "2", "3")
    valid_items = []
    for item in catalog:
        name = item.get("name", "").strip()
        if not name or name.isdigit():
            continue
        valid_items.append(item)
        
    print(f"Loaded {len(valid_items)} valid catalog items out of {len(catalog)} total items.")
    
    if not valid_items:
        print("No valid items to index.")
        return
        
    print("Generating embeddings using all-MiniLM-L6-v2...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    texts = [item_to_text(item) for item in valid_items]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True).astype("float32")
    
    print("Normalizing embeddings...")
    faiss.normalize_L2(embeddings)
    
    print("Building FAISS IndexFlatIP...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    # Ensure directory exists
    os.makedirs("app/data", exist_ok=True)
    
    faiss.write_index(index, "app/data/faiss.index")
    print("Saved index to app/data/faiss.index")
    
    with open("app/data/faiss_metadata.json", "w", encoding="utf-8") as f:
        json.dump(valid_items, f, indent=2, ensure_ascii=False)
    print("Saved metadata to app/data/faiss_metadata.json")
    
    print("Index build completed successfully!")

if __name__ == "__main__":
    main()