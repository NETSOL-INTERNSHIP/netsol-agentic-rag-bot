import numpy as np
from sentence_transformers import SentenceTransformer

from .config import Config
from .store import load_chunks

# Loaded once at module level
_model = None
_chunks = None
_embeddings = None


def _ensure_loaded():
    global _model, _chunks, _embeddings

    if _chunks is not None:
        return

    _chunks, _embeddings = load_chunks()
    if _chunks is None:
        raise RuntimeError("No chunks found. Run /ingest first.")

    print(f"Loaded {_len()} chunks into memory.")

    if _model is None:
        _model = SentenceTransformer(Config.EMBEDDING_MODEL)


def _len():
    return len(_chunks)


def retrieve(question, top_k=None):
    _ensure_loaded()
    top_k = top_k or Config.TOP_K

    # Embed the question
    query_embedding = _model.encode([question])

    # Cosine similarity
    scores = np.dot(_embeddings, query_embedding.T).flatten()
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "text": _chunks[idx]["text"],
            "source": _chunks[idx]["source"],
            "score": float(scores[idx])
        })

    return results