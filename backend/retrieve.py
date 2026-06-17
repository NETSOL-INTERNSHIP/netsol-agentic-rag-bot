import chromadb
from sentence_transformers import SentenceTransformer

from .config import Config

_collection = None
_model = None


def _get_resources():
    global _collection, _model
    if _collection is None:
        _model = SentenceTransformer(Config.EMBEDDING_MODEL)
        client = chromadb.PersistentClient(path=Config.CHROMA_DIR)
        _collection = client.get_collection(name="rag_documents")
    return _collection, _model


def retrieve(question, top_k=None):
    collection, model = _get_resources()
    top_k = top_k or Config.TOP_K

    # Manually embed the question
    query_embedding = model.encode([question], normalize_embeddings=True).tolist()

    # Query ChromaDB
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    # Format results
    formatted_results = []
    for i in range(len(results['ids'][0])):
        formatted_results.append({
            "text": results['documents'][0][i],
            "source": results['metadatas'][0][i]['source'],
            "score": 1 - results['distances'][0][i] 
        })

    return formatted_results