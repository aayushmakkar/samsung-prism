import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class MultiIntentDecomposer:

    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])

    def decompose(self, text):
        prompt = f"""
You are a query decomposition system.

Break the user's request into separate retrieval queries.

Rules:
1. Return only valid JSON.
2. Use this exact format:
{{"queries": ["query 1", "query 2"]}}
3. If the request contains only one intent, return one query.
4. Do not answer the question.
5. Preserve the meaning of the user's request.

User request:
{text}
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You decompose complex requests into retrieval queries."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0
        )

        content = response.choices[0].message.content

        try:
            data = json.loads(content)
            queries = data.get("queries", [])

            if isinstance(queries, list) and queries:
                return queries

        except json.JSONDecodeError:
            pass

        return [text]


if __name__ == "__main__":
    decomposer = MultiIntentDecomposer()

    tests = [
        "What is FAISS?",
        "Explain FAISS and also explain multi-intent decomposition"
    ]

    for text in tests:
        print(f"\nINPUT: {text}")

        queries = decomposer.decompose(text)

        print("QUERIES:")

        for i, query in enumerate(queries, 1):
            print(f"{i}. {query}")