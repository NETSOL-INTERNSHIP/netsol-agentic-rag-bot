import os
from sentence_transformers import SentenceTransformer

from .config import Config
from .store import save_chunks, load_chunks


def split_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def run_ingest():
    # Skip if already ingested
    chunks, embeddings = load_chunks()
    if chunks is not None:
        print("Found existing chunks. Skipping ingestion.")
        return

    # Load embedding model
    print(f"Loading model: {Config.EMBEDDING_MODEL}")
    model = SentenceTransformer(Config.EMBEDDING_MODEL)

    # Ensure the data folder exists
    os.makedirs(Config.DATA_DIR, exist_ok=True)

    # Read only .txt files
    all_chunks = []
    for filename in os.listdir(Config.DATA_DIR):
        if not filename.endswith(".txt"):
            continue
            
        filepath = os.path.join(Config.DATA_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        file_chunks = split_text(text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)

        for i, chunk in enumerate(file_chunks):
            all_chunks.append({
                "text": chunk,
                "source": filename,
                "chunk_id": i
            })

    if not all_chunks:
        print(f"WARNING: No .txt files found in {Config.DATA_DIR}")
        return

    print(f"Created {len(all_chunks)} chunks")

    # Create embeddings (one-time cost)
    print("Creating embeddings...")
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    # Save to disk
    save_chunks(all_chunks, embeddings)
    print(f"Saved {len(all_chunks)} chunks and embeddings to disk.")