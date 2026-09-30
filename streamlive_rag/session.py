from dataclasses import dataclass, field


@dataclass
class SessionState:
    session_id: str
    previous_answer: str = ""
    previous_intents: list = field(default_factory=list)
    previous_evidence: list = field(default_factory=list)
    details: list = field(default_factory=list)
    answer_version: int = 0

    def update(
        self,
        answer=None,
        intents=None,
        evidence=None,
        detail=None
    ):
        if answer is not None:
            self.previous_answer = answer
            self.answer_version += 1

        if intents is not None:
            self.previous_intents = intents

        if evidence is not None:
            self.previous_evidence = evidence

        if detail is not None:
            self.details.append(detail)

    def context(self):
        return {
            "session_id": self.session_id,
            "previous_answer": self.previous_answer,
            "previous_intents": self.previous_intents,
            "details": self.details,
            "answer_version": self.answer_version
        }


if __name__ == "__main__":
    session = SessionState(session_id="demo-session")

    session.update(
        answer="FAISS performs vector similarity search.",
        intents=["FAISS"],
        detail="User wants a simple explanation."
    )

    print("SESSION STATE:")
    print(session.context())

    session.update(
        detail="User also wants to know how FAISS is used in RAG."
    )

    print("\nUPDATED SESSION:")
    print(session.context())