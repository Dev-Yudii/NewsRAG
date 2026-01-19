import os
import json
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_FOLDER = os.path.join(BASE_DIR, "data", "raw")
STANDARDIZED_FOLDER = os.path.join(BASE_DIR, "data", "standardized")

os.makedirs(STANDARDIZED_FOLDER, exist_ok=True)


def safe_filename_from_url(url: str) -> str:
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return f"{url_hash}.json"


files = os.listdir(RAW_FOLDER)
json_files = [f for f in files if f.endswith(".json")]

for filename in json_files:
    raw_path = os.path.join(RAW_FOLDER, filename)

    try:
        with open(raw_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON malformado: {raw_path}") from e

    required_keys = {"title", "url", "source", "date", "context"}
    if not required_keys.issubset(data.keys()):
        raise RuntimeError(f"Schema inválido em {raw_path}: {data.keys()}")

    record = {
        "doc_id": data["url"],
        "source": data["source"],
        "url": data["url"],
        "title": data["title"],
        "published_at": data["date"],
        "language": None,
        "section": None,
        "content_raw_text": data["context"],
    }

    output_filename = safe_filename_from_url(record["url"])
    output_path = os.path.join(STANDARDIZED_FOLDER, output_filename)

    if os.path.exists(output_path):
        raise RuntimeError(f"The standardized file already exists: {output_path}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

print("Data standardization successfully.")