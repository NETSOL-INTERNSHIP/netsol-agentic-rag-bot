import os
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from .config import Config


def split_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def run_ingest():
    # 1. Initialize ChromaDB client
    client = chromadb.PersistentClient(path=Config.CHROMA_DIR)
    
    # 2. Initialize the collection WITHOUT the embedding function
    # We will manually handle embeddings for speed and batching control
    collection = client.get_or_create_collection(
        name="rag_documents",
        metadata={"hnsw:space": "cosine"}
    )

    # 3. Skip if already ingested
    if collection.count() > 0:
        print(f"Found {collection.count()} chunks in ChromaDB. Skipping ingestion.")
        return

    print(f"Loading model: {Config.EMBEDDING_MODEL}")
    model = SentenceTransformer(Config.EMBEDDING_MODEL)
    
    os.makedirs(Config.DATA_DIR, exist_ok=True)

    # 4. Read files
    ids = []
    documents = []
    metadatas = []

    for filename in os.listdir(Config.DATA_DIR):
        if not filename.endswith(".txt"):
            continue
            
        filepath = os.path.join(Config.DATA_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        file_chunks = split_text(text, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)

        for i, chunk in enumerate(file_chunks):
            chunk_id = f"{filename}_chunk_{i}"
            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append({"source": filename, "chunk_index": i})

    if not documents:
        print(f"WARNING: No .txt files found in {Config.DATA_DIR}")
        return

    print(f"Created {len(documents)} chunks. Creating embeddings (this will take a minute)...")

    # 5. FAST EMBEDDING: Use model.encode with batching
    embeddings = model.encode(documents, batch_size=64, show_progress_bar=True, normalize_embeddings=True)

    print("Adding to ChromaDB in batches...")

    # 6. FAST INSERT: Add to ChromaDB in batches of 500
    batch_size = 500
    for i in tqdm(range(0, len(ids), batch_size), desc="Inserting into DB"):
        batch_ids = ids[i : i + batch_size]
        batch_docs = documents[i : i + batch_size]
        batch_metas = metadatas[i : i + batch_size]
        batch_embs = embeddings[i : i + batch_size].tolist() # ChromaDB expects lists, not numpy arrays

        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            metadatas=batch_metas,
            embeddings=batch_embs
        )

    print(f"Successfully saved {collection.count()} chunks to ChromaDB.")