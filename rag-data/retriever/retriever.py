import json 
import faiss
import numpy as np 
from embedder import Embedder
from pathlib import Path
from intent_router import get_intent_priority_sections

INDEX_PATH = Path("../embeddings/faiss_index/index.faiss")
METADATA_PATH = Path("../embeddings/faiss_index/metadata.json")