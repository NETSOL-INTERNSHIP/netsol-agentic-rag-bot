# netsol-agentic-rag-bot

Agentic RAG (Retrieval-Augmented Generation) chatbot that indexes a corpus of text files, builds embeddings, and answers user questions by combining retrieved context with a configurable LLM provider.

**Quick Summary**
- **Backend:** Flask API that handles ingestion, retrieval and generation. See [run.py](run.py#L1) and [backend/__init__.py](backend/__init__.py#L1).
- **Frontend:** Vite + React app located in [frontend/package.json](frontend/package.json#L1) (dev server default port: 5173).
- **Data:** Plain-text documents stored in the `data/` folder and chunked into embeddings stored in [backend/vectorstore](backend/vectorstore).

**Default Ports**
- Backend API: `8090` (configured in [run.py](run.py#L1)).
- Frontend dev server: `5173` (Vite default, see [frontend/package.json](frontend/package.json#L1)).

**How it works (high level)**
- On startup `run.py` calls `run_ingest()` to create text chunks and embeddings if they don't already exist, then starts the Flask app on port 8090.
- The `/ingest` endpoint triggers the same ingestion flow manually.
- The `/chat` endpoint accepts a JSON payload with `question`, uses the sentence-transformers model to embed the query, finds the most similar stored chunks, and passes the concatenated context to a configured LLM to generate an answer.

Project layout and responsibilities
- **`run.py`**: Entrypoint. Creates the Flask app and calls ingestion on startup. [run.py](run.py#L1)
- **`requirements.txt`**: Python dependencies used by the backend (Flask, sentence-transformers, langchain adapters, numpy, etc.). [requirements.txt](requirements.txt#L1)

- **`backend/__init__.py`**: Creates and configures the Flask app and registers the blueprint. [backend/__init__.py](backend/__init__.py#L1)
- **`backend/config.py`**: Central configuration class. Loads `.env` (if present) and exposes constants such as `EMBEDDING_MODEL`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `DATA_DIR`, `VECTORSTORE_DIR`, `LLM_PROVIDER`, `LLM_MODEL` and API keys. Edit environment variables to change behavior. [backend/config.py](backend/config.py#L1)
- **`backend/ingest.py`**: Reads `.txt` files from `data/`, splits them into fixed-size overlapping chunks, computes embeddings (using `sentence-transformers`), and saves chunks + embeddings to `backend/vectorstore` via `store.py`. Called on startup and by the `/ingest` endpoint. [backend/ingest.py](backend/ingest.py#L1)
- **`backend/store.py`**: Disk persistence for `chunks.json` and `embeddings.npy`. `save_chunks()` and `load_chunks()` are the single source of truth for the local vectorstore. [backend/store.py](backend/store.py#L1)
- **`backend/retrieve.py`**: Loads saved chunks and embeddings into memory, encodes the user query, computes cosine similarities, and returns the top-K chunks. Uses the same embedding model for consistency. [backend/retrieve.py](backend/retrieve.py#L1)
- **`backend/generate.py`**: Builds a prompt by joining retrieved chunks into a `context` and calls the selected LLM via the `get_llm()` factory. Returns the model's answer. [backend/generate.py](backend/generate.py#L1)
- **`backend/llm.py`**: LLM provider factory. Supports `groq`, `openai`, `anthropic`, and `google` via langchain provider adapters. Set `LLM_PROVIDER` and provider-specific API keys in environment variables. [backend/llm.py](backend/llm.py#L1)
- **`backend/routes.py`**: Flask blueprint with two endpoints: `POST /chat` (accepts `{ "question": "..." }`) and `POST /ingest` (to force re-ingestion). [backend/routes.py](backend/routes.py#L1)

Data and vectorstore
- Text sources: all `.txt` files in the `data/` directory are chunked and embedded. Example files are present in the `data/` directory.
- Vectorstore files are saved to `backend/vectorstore/chunks.json` and `backend/vectorstore/embeddings.npy`. The repo already contains those files if ingestion has run.

Configuration and environment variables
- Create a `.env` at the project root to override defaults. The app reads `.env` via `backend/config.py`. Important variables:
	- `CHUNK_SIZE` (default 1000)
	- `CHUNK_OVERLAP` (default 275)
	- `LLM_PROVIDER` (groq|openai|anthropic|google)
	- `LLM_MODEL` (provider-specific model name)
	- `GROQ_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY` as needed

Run locally (backend)
1. Create a Python venv and install dependencies:
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
2. (Optional) Create `.env` with your API keys and config overrides.
3. Start the backend (calls ingestion on startup):
```bash
python run.py
```
The backend listens on `0.0.0.0:8090` by default.

Run frontend (dev)
```bash
cd frontend
npm install
npm run dev
```
Vite serves the frontend on port `5173` by default.

API
- `POST /chat` — body: `{ "question": "..." }` → returns `{ "answer": "...", "sources": [ ... ] }`.
- `POST /ingest` — triggers ingestion and persistence of chunks+embeddings.

Notes and tips
- Ingestion is idempotent: `ingest.run_ingest()` checks for existing `chunks.json` / `embeddings.npy` and skips if present.
- To re-run ingestion, delete `backend/vectorstore/*` or call `POST /ingest` after removing the files.
- The embedding model is currently set to `BAAI/bge-large-en-v1.5` in `backend/config.py`. Change it cautiously — embeddings must match between indexing and retrieval.

If you want, I can:
- add a sample `.env.example` with recommended variables
- add a tiny curl example for `/chat`
- wire the frontend to the backend's base URL and add a README section with common troubleshooting steps

