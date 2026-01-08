import faiss
import json
import numpy as np
from embedder import Embedder
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.path.join(BASE_DIR, "..", "embeddings", "faiss_index")

INDEX_PATH = os.path.join(INDEX_DIR, "computer_service.index")
META_PATH = os.path.join(INDEX_DIR, "computer_service_metadata.json")

def load_faiss_index():
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

def search_query(query, top_k=3):
    embedder = Embedder()
    index, metadata = load_faiss_index()
    
    query_embedding = embedder.get_embedding(query)
    query_embedding = np.expand_dims(query_embedding, axis=0)
    
    score, indices = index.search(query_embedding,top_k)
    
    results = []
    for i in indices[0]:
        results.append(metadata[i])
        
    return results


if __name__ == "__main__":
    sample_query = "Layar laptop saya tiba-tiba menjadi hitam saat baru dinyalakan."
    results = search_query(sample_query, top_k=3)
    
    filtered_results = []
    for res in results:
        if res["category"] == "Power/Battery":
            filtered_results.append(res)

    for i, res in enumerate(filtered_results):
        print(f"Result {i+1}:")
        print(json.dumps(res, indent=2, ensure_ascii=False))
        print()
        