import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class AnswerGenerator:

    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])

    def generate(self, question, evidence, session_context=None):

        evidence_text = ""

        for i, item in enumerate(evidence, 1):
            evidence_text += (
                f"[E{i}] {item['text']}\n"
            )

        previous_answer = ""

        if session_context:
            previous_answer = session_context.get(
                "previous_answer", ""
            )

        prompt = f"""
Answer the user's question using ONLY the provided evidence.

Rules:
1. Do not invent facts.
2. Cite evidence using [E1], [E2], etc.
3. If the evidence does not contain the answer, say:
   "Not found in the provided corpus."
4. If a previous answer exists and the user provides additional
   information, refine the answer instead of ignoring the previous answer.
5. Keep the answer concise and clear.

USER QUESTION:
{question}

PREVIOUS ANSWER:
{previous_answer}

EVIDENCE:
{evidence_text}
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a grounded RAG answer generator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    from streamlive_rag.streamlive_rag.retriever import Retriever

    retriever = Retriever()
    generator = AnswerGenerator()

    question = "What is FAISS used for?"

    evidence = retriever.search(question, k=3)

    answer = generator.generate(
        question,
        evidence
    )

    print("\nANSWER:")
    print(answer)