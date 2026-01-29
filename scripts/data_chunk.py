import os
import json
import hashlib

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDARDIZED_DIR = os.path.join(BASE_DIR, "data", "standardized")
CHUNKS_DIR = os.path.join(BASE_DIR, "data", "chunks")

os.makedirs(CHUNKS_DIR, exist_ok=True)

# Chunking parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
STEP = CHUNK_SIZE - CHUNK_OVERLAP


def generate_chunk_id(doc_id: str, chunk_index: int) -> str:
    raw = f"{doc_id}_{chunk_index}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def chunk_text(text: str):
    """
    Deterministic character-based chunking with overlap.
    """
    chunks = []
    start = 0
    index = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]

        if chunk.strip():
            chunks.append((index, chunk))

        start += STEP
        index += 1

    return chunks


# Metrics
metrics = {
    "documents_processed": 0,
    "documents_skipped": 0,
    "chunks_created": 0
}


for filename in os.listdir(STANDARDIZED_DIR):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(STANDARDIZED_DIR, filename)

    with open(file_path, "r", encoding="utf-8") as f:
        doc = json.load(f)

    content = doc.get("content_raw_text")
    doc_id = doc.get("doc_id")

    if not content or not doc_id:
        metrics["documents_skipped"] += 1
        continue

    metrics["documents_processed"] += 1

    chunks = chunk_text(content)

    for chunk_index, chunk_text_value in chunks:
        chunk_id = generate_chunk_id(doc_id, chunk_index)
        output_path = os.path.join(CHUNKS_DIR, f"{chunk_id}.json")

        if os.path.exists(output_path):
            raise RuntimeError(f"Chunk already exists: {output_path}")

        chunk_record = {
            "chunk_id": chunk_id,
            "doc_id": doc_id,
            "chunk_index": chunk_index,
            "text": chunk_text_value,
            "source": doc.get("source"),
            "url": doc.get("url"),
            "title": doc.get("title"),
            "published_at": doc.get("published_at"),
            "language": doc.get("language")
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunk_record, f, ensure_ascii=False, indent=2)

        metrics["chunks_created"] += 1


print("\n===== Chunking Report =====")
print(f"Documents processed: {metrics['documents_processed']}")
print(f"Documents skipped:   {metrics['documents_skipped']}")
print(f"Chunks created:      {metrics['chunks_created']}")
print("===========================\n")