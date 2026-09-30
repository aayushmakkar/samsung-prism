class RetrievalController:

    def decide(self, text, has_previous_answer=False):
        text = text.strip()

        # Empty input
        if not text:
            return "WAIT", "empty input"

        # Conversational / closing input
        suppress_words = [
            "thanks",
            "thank you",
            "okay",
            "ok",
            "bye",
            "goodbye",
            "cool",
            "great"
        ]

        if text.lower() in suppress_words:
            return "SUPPRESS", "conversational input"

        words = text.split()

        # Very short request
        if len(words) < 3:
            return "WAIT", "request may be incomplete"

        # Clearly unfinished sentence
        dangling_words = [
            "about",
            "and",
            "or",
            "with",
            "for",
            "because"
        ]

        last_word = words[-1].lower().strip(".,?!")

        if last_word in dangling_words:
            return "WAIT", "sentence appears incomplete"

        # Enough information to retrieve
        return "RETRIEVE", "sufficient information"


if __name__ == "__main__":
    controller = RetrievalController()

    tests = [
        "Tell me about",
        "What is multi-intent decomposition?",
        "Thanks",
        "Explain FAISS retrieval"
    ]

    for text in tests:
        decision, reason = controller.decide(text)

        print(f"\nINPUT: {text}")
        print(f"DECISION: {decision}")
        print(f"REASON: {reason}")