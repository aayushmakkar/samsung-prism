import json
import time
from pathlib import Path


TELEMETRY_FILE = Path("telemetry.jsonl")


class Telemetry:

    def __init__(self):
        self.events = []

    def log(self, event, **data):
        record = {
            "timestamp": time.time(),
            "event": event,
            **data
        }

        self.events.append(record)

        with open(
            TELEMETRY_FILE,
            "a",
            encoding="utf-8"
        ) as f:
            f.write(json.dumps(record) + "\n")

    def get_events(self):
        return self.events

    def clear(self):
        self.events = []

        if TELEMETRY_FILE.exists():
            TELEMETRY_FILE.unlink()


if __name__ == "__main__":
    telemetry = Telemetry()

    telemetry.log(
        "controller_decision",
        decision="RETRIEVE",
        reason="sufficient information"
    )

    telemetry.log(
        "retrieval",
        query="What is FAISS?",
        results=3
    )

    telemetry.log(
        "answer_generated",
        citations=["E1"]
    )

    print("Telemetry events:")

    for event in telemetry.get_events():
        print(event)