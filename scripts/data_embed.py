import os
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer

# =========================
# Paths do projeto
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_DIR = os.path.join(BASE_DIR, "data", "chunks")

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_VERSION = "v1"

EMBEDDINGS_DIR = os.path.join(
    BASE_DIR,
    "data",
    "embeddings",
    f"{MODEL_NAME}_{EMBEDDING_VERSION}"
)

os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

# =========================
# Modelo de embedding (local)
# =========================

model = SentenceTransformer(MODEL_NAME)

# =========================
# IO helpers
# =========================

def load_chunks():
    for file in os.listdir(CHUNKS_DIR):
        if file.endswith(".json"):
            with open(os.path.join(CHUNKS_DIR, file), "r", encoding="utf-8") as f:
                yield json.load(f)


def embedding_exists(chunk_id: str) -> bool:
    path = os.path.join(EMBEDDINGS_DIR, f"{chunk_id}.json")
    return os.path.exists(path)


def save_embedding(record: dict):
    path = os.path.join(EMBEDDINGS_DIR, f"{record['chunk_id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

# =========================
# Pipeline principal
# =========================

def main():
    for chunk in load_chunks():
        chunk_id = chunk["chunk_id"]

        # Idempotência: não gerar duas vezes
        if embedding_exists(chunk_id):
            continue

        # Embedding local (zero custo)
        embedding_vector = model.encode(chunk["text"]).tolist()

        record = {
            "chunk_id": chunk_id,
            "doc_id": chunk["doc_id"],
            "chunk_index": chunk["chunk_index"],

            "embedding": embedding_vector,

            "embedding_model": MODEL_NAME,
            "embedding_version": EMBEDDING_VERSION,
            "embedding_dim": len(embedding_vector),
            "created_at": datetime.utcnow().isoformat()
        }

        save_embedding(record)

    print("Embedding generation (local) completed.")


if __name__ == "__main__":
    main()