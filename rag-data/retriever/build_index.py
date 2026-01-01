import os
import json
import faiss
import numpy as np
from embedder import Embedder

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNK_DIR = os.path.join(BASE_DIR, "..", "chunks")
INDEX_DIR = os.path.join(BASE_DIR, "..", "embeddings", "faiss_index")

os.makedirs(INDEX_DIR, exist_ok=True)

# ---------------- LOAD CHUNKS ----------------
def load_chunks(chunk_dir):
    contents = []
    metadata = []

    if not os.path.exists(chunk_dir):
        raise FileNotFoundError(f"Chunk directory not found: {chunk_dir}")

    for root, _, files in os.walk(chunk_dir):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    if not isinstance(data, list):
                        continue

                    for chunk in data:
                        if "content" in chunk:
                            contents.append(chunk["content"])
                            metadata.append(chunk)

    if not contents:
        raise ValueError("No valid chunks found")

    return contents, metadata

# ---------------- BUILD INDEX ----------------
def build_faiss_index():
    print("🔄 Loading chunks...")
    texts, metadata = load_chunks(CHUNK_DIR)
    print(f"✅ Loaded {len(texts)} chunks")

    print("🔄 Generating embeddings...")
    embedder = Embedder()
    embeddings = embedder.get_embedding(texts)

    print("✅ Embedding shape:", embeddings.shape)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    # Save index
    index_path = os.path.join(INDEX_DIR, "computer_service.index")
    faiss.write_index(index, index_path)

    # Save metadata
    metadata_path = os.path.join(INDEX_DIR, "computer_service_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("🎉 FAISS index successfully built")
    print(f"📦 Index saved to: {index_path}")
    print(f"🧾 Metadata saved to: {metadata_path}")

# ---------------- RUN ----------------
if __name__ == "__main__":
    build_faiss_index()
