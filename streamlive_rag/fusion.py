class EvidenceFusion:

    def __init__(self, retriever):
        self.retriever = retriever

    def search(self, queries, k=3):
        all_results = []

        for query in queries:
            results = self.retriever.search(query, k=k)

            for result in results:
                result["query"] = query
                all_results.append(result)

        # Remove duplicate chunks
        unique = {}

        for result in all_results:
            key = result["text"]

            if key not in unique:
                unique[key] = result
            else:
                # Keep the stronger score
                if result["score"] > unique[key]["score"]:
                    unique[key] = result

        # Sort by relevance
        fused_results = sorted(
            unique.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        return fused_results


if __name__ == "__main__":
    from streamlive_rag.streamlive_rag.retriever import Retriever

    retriever = Retriever()
    fusion = EvidenceFusion(retriever)

    queries = [
        "FAISS vector similarity search",
        "multi-intent decomposition"
    ]

    results = fusion.search(queries)

    for i, result in enumerate(results, 1):
        print(f"\n[E{i}]")
        print("QUERY:", result["query"])
        print("SCORE:", result["score"])
        print("SOURCE:", result["source"])
        print("TEXT:", result["text"])