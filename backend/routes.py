from flask import Blueprint, request, jsonify
from .retrieve import retrieve
from .generate import generate
from .ingest import run_ingest

bp = Blueprint("main", __name__)


@bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "question is required"}), 400

    chunks = retrieve(question)
    answer = generate(question, chunks)

    return jsonify({"answer": answer, "sources": [c["source"] for c in chunks]})


@bp.route("/ingest", methods=["POST"])
def ingest():
    run_ingest()
    return jsonify({"status": "done"})