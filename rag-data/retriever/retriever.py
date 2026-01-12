from pydoc import doc
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
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        doc = metadata[idx].copy()
        doc["score"] = float(score[0][i])
        results.append(doc)
    return results

def keyword_score(query, content):
    q_words = set(query.lower().split())
    c_words = set(content.lower().split())
    return len(q_words & c_words) / len(q_words | c_words) if q_words else 0

def score_document(query, intent, document):
    vector_score = document.get("score", 0.0)
    intent_score = 1.0 if document.get("category") == intent else 0.0
    keyword_sc = keyword_score(query, document.get("content", ""))
    
    final_score = (
        0.6 * vector_score +
        0.3 * intent_score +
        0.1 * keyword_sc
    )
    return final_score

def detect_intent(query):
    keywords = {
        "Power/Battery": ["baterai", "listrik", "mati", "daya", "charger"],
        "Screen/Display": ["layar", "monitor", "hitam", "resolusi", "pixel"],
        "Performance": ["lambat", "lemot", "kinerja", "hang", "freeze"],
        "Software/OS": ["sistem operasi", "windows", "macos", "linux", "update"],
        "Hardware": ["hardware", "komponen", "kerusakan fisik", "perangkat keras"]
    }
    
    query_lower = query.lower()
    for category, kws in keywords.items():
        for kw in kws:
            if kw in query_lower:
                return category
    return "General"

def retrieve_solutions(query, top_k=5):
    intent = detect_intent(query)
    raw_results = search_query(query, top_k=top_k)

    scored_results = []
    for doc in raw_results:
        doc["final_score"] = round(
            score_document(query, intent, doc), 3
        )
        scored_results.append(doc)

    scored_results.sort(
        key=lambda x: x["final_score"], reverse=True
    )

    return scored_results[:3]

if __name__ == "__main__":
    sample_query = "Layar laptop saya tiba-tiba menjadi hitam saat baru dinyalakan."

    answers = retrieve_solutions(sample_query)

    for i, res in enumerate(answers):
        print(f"\nResult {i+1}")
        print(f"Score: {res['final_score']}")
        print(json.dumps(res, indent=2, ensure_ascii=False))
        