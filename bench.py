from streamlive_rag.pipeline import StreamingRAG


def run_test(rag, text, expected):
    result = rag.feed(text)

    actual = result["decision"]

    passed = actual == expected

    print(f"INPUT:    {text}")
    print(f"EXPECTED: {expected}")
    print(f"ACTUAL:   {actual}")
    print(f"RESULT:   {'PASS' if passed else 'FAIL'}")
    print("-" * 60)

    return passed


def main():
    rag = StreamingRAG()

    tests = [
        ("Tell me about", "WAIT"),
        ("Explain FAISS and multi-intent decomposition", "RETRIEVE"),
        ("Thanks", "SUPPRESS"),
        ("Explain FAISS retrieval", "RETRIEVE"),
    ]

    passed = 0

    for text, expected in tests:
        if run_test(rag, text, expected):
            passed += 1

    accuracy = (passed / len(tests)) * 100

    print()
    print("=" * 60)
    print(f"BENCHMARK RESULT: {passed}/{len(tests)} passed")
    print(f"CONTROLLER ACCURACY: {accuracy:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()