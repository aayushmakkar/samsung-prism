import json
import faiss
from sentence_transformers import SentenceTransformer


INDEX_PATH = "data/index.faiss"
CHUNKS_PATH = "data/chunks.json"
MODEL_NAME = "all-MiniLM-L6-v2"


class Retriever:

    def __init__(self):
        self.index = faiss.read_index(INDEX_PATH)

        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        self.model = SentenceTransformer(MODEL_NAME)

    def search(self, query, k=3):
        embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype("float32")

        scores, indices = self.index.search(embedding, k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            results.append({
                "score": float(score),
                "source": self.chunks[index]["source"],
                "text": self.chunks[index]["text"]
            })

        return results


if __name__ == "__main__":
    retriever = Retriever()

    results = retriever.search(
        "What is multi-intent decomposition?"
    )

    for result in results:
        print("\nSCORE:", result["score"])
        print("SOURCE:", result["source"])
        print("TEXT:", result["text"])