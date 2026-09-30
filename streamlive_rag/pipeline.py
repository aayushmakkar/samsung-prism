import time

from .controller import RetrievalController
from .decomposer import MultiIntentDecomposer
from .retriever import Retriever
from .fusion import EvidenceFusion
from .session import SessionState
from .generator import AnswerGenerator
from .telemetry import Telemetry


class StreamingRAG:

    def __init__(self):
        self.controller = RetrievalController()
        self.decomposer = MultiIntentDecomposer()
        self.retriever = Retriever()
        self.fusion = EvidenceFusion(self.retriever)
        self.generator = AnswerGenerator()
        self.telemetry = Telemetry()

        self.session = SessionState(
            session_id="demo-session"
        )

    def feed(self, text):

        start_time = time.time()

        # 1. Controller
        decision, reason = self.controller.decide(
            text,
            has_previous_answer=bool(
                self.session.previous_answer
            )
        )

        self.telemetry.log(
            "controller_decision",
            text=text,
            decision=decision,
            reason=reason
        )

        # WAIT
        if decision == "WAIT":
            return {
                "decision": "WAIT",
                "reason": reason,
                "intents": [],
                "evidence": []
            }

        # SUPPRESS
        if decision == "SUPPRESS":
            return {
                "decision": "SUPPRESS",
                "reason": reason,
                "intents": [],
                "evidence": []
            }

        # 2. Decompose
        intents = self.decomposer.decompose(text)

        self.telemetry.log(
            "query_decomposition",
            queries=intents
        )

        # 3. Retrieve + fuse
        evidence = self.fusion.search(
            intents,
            k=3
        )

        self.telemetry.log(
            "retrieval",
            queries=intents,
            result_count=len(evidence),
            latency_ms=round(
                (time.time() - start_time) * 1000,
                2
            )
        )

        # 4. Generate grounded answer
        answer = self.generator.generate(
            text,
            evidence,
            self.session.context()
        )

        # 5. Update session
        self.session.update(
            answer=answer,
            intents=intents,
            evidence=evidence
        )

        self.telemetry.log(
            "answer_generated",
            answer_version=self.session.answer_version
        )

        return {
            "decision": "RETRIEVE",
            "reason": reason,
            "intents": intents,
            "evidence": evidence,
            "answer": answer
        }


if __name__ == "__main__":

    rag = StreamingRAG()

    tests = [
        "Tell me about",
        "Explain FAISS and multi-intent decomposition",
        "Thanks"
    ]

    for text in tests:

        print("\n" + "=" * 60)
        print("USER:", text)

        result = rag.feed(text)

        print("DECISION:", result["decision"])

        if result["intents"]:
            print("INTENTS:")

            for intent in result["intents"]:
                print("-", intent)

        if "answer" in result:
            print("\nANSWER:")
            print(result["answer"])