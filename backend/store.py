import json
import numpy as np
import os

from .config import Config


def save_chunks(chunks, embeddings):
    """Save chunks and embeddings to disk."""
    os.makedirs(Config.VECTORSTORE_DIR, exist_ok=True)

    chunks_path = os.path.join(Config.VECTORSTORE_DIR, "chunks.json")
    embeddings_path = os.path.join(Config.VECTORSTORE_DIR, "embeddings.npy")

    with open(chunks_path, "w") as f:
        json.dump(chunks, f)

    np.save(embeddings_path, np.array(embeddings))


def load_chunks():
    """Load chunks and embeddings from disk. Returns None if not found."""
    chunks_path = os.path.join(Config.VECTORSTORE_DIR, "chunks.json")
    embeddings_path = os.path.join(Config.VECTORSTORE_DIR, "embeddings.npy")

    if not os.path.exists(chunks_path) or not os.path.exists(embeddings_path):
        return None, None

    with open(chunks_path, "r") as f:
        chunks = json.load(f)

    embeddings = np.load(embeddings_path)

    return chunks, embeddings