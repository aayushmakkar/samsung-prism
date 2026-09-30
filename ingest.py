import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


CORPUS_DIR = Path("data/corpus")
INDEX_PATH = Path("data/index.faiss")
CHUNKS_PATH = Path("data/chunks.json")

MODEL_NAME = "all-MiniLM-L6-v2"


def load_documents():
    documents = []

    for file in CORPUS_DIR.glob("*.txt"):
        text = file.read_text(encoding="utf-8")

        documents.append({
            "source": file.name,
            "text": text
        })

    return documents


def chunk_text(text, chunk_size=120, overlap=25):
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunks.append(" ".join(words[start:end]))

        if end == len(words):
            break

        start = end - overlap

    return chunks


def main():
    documents = load_documents()

    if not documents:
        raise RuntimeError("No documents found in data/corpus")

    chunks = []

    for document in documents:
        for chunk in chunk_text(document["text"]):
            chunks.append({
                "source": document["source"],
                "text": chunk
            })

    print(f"Loaded {len(documents)} document(s)")
    print(f"Created {len(chunks)} chunk(s)")

    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    embeddings = embeddings.astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(INDEX_PATH))

    CHUNKS_PATH.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("FAISS index created successfully.")
    print(f"Saved: {INDEX_PATH}")
    print(f"Saved: {CHUNKS_PATH}")


if __name__ == "__main__":
    main()