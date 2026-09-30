import time

import streamlit as st

from streamlive_rag.pipeline import StreamingRAG


st.set_page_config(
    page_title="Streaming Live RAG",
    page_icon="🔎",
    layout="wide"
)


st.title("🔎 Streaming Live RAG")
st.caption(
    "Samsung PRISM Y2026 | Theme 04"
)


if "rag" not in st.session_state:
    st.session_state.rag = StreamingRAG()

if "transcript" not in st.session_state:
    st.session_state.transcript = []

if "results" not in st.session_state:
    st.session_state.results = []


st.sidebar.header("Demo Controls")

delay = st.sidebar.slider(
    "Streaming delay",
    0.1,
    2.0,
    0.5
)


user_input = st.text_input(
    "Enter transcript chunk",
    placeholder="e.g. Explain FAISS and multi-intent decomposition"
)


col1, col2 = st.columns(2)

with col1:
    if st.button("Send Chunk"):
        if user_input.strip():

            result = st.session_state.rag.feed(
                user_input
            )

            st.session_state.transcript.append(
                user_input
            )

            st.session_state.results.append(
                result
            )

with col2:
    if st.button("Reset Session"):
        st.session_state.rag = StreamingRAG()
        st.session_state.transcript = []
        st.session_state.results = []
        st.rerun()


st.divider()


left, right = st.columns(2)


with left:

    st.subheader("Live Transcript")

    if st.session_state.transcript:

        for text in st.session_state.transcript:
            st.write("🎙️", text)

    else:
        st.info("No transcript chunks yet.")


with right:

    st.subheader("Retrieval Controller")

    if st.session_state.results:

        latest = st.session_state.results[-1]

        decision = latest.get(
            "decision",
            "WAIT"
        )

        if decision == "RETRIEVE":
            st.success("RETRIEVE")

        elif decision == "WAIT":
            st.warning("WAIT")

        else:
            st.info("SUPPRESS")

        st.write(
            "Reason:",
            latest.get("reason", "")
        )


st.divider()


st.subheader("Grounded Answer")

if st.session_state.results:

    latest = st.session_state.results[-1]

    if "answer" in latest:
        st.write(latest["answer"])
    else:
        st.info(
            "No answer generated for this chunk."
        )

else:
    st.info(
        "Send a transcript chunk to begin."
    )


st.divider()


st.subheader("Query Decomposition")

if st.session_state.results:

    latest = st.session_state.results[-1]

    intents = latest.get(
        "intents",
        []
    )

    if intents:

        for i, intent in enumerate(
            intents,
            1
        ):
            st.write(
                f"**Query {i}:** {intent}"
            )

    else:
        st.info("No retrieval queries.")


st.divider()


st.subheader("Telemetry")

events = st.session_state.rag.telemetry.get_events()

if events:

    for event in reversed(events[-10:]):
        st.json(event)

else:
    st.info("No telemetry events yet.")