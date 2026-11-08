import requests
import streamlit as st

from chatbot import MODELS, OLLAMA_URL, SYSTEM_PROMPT

st.set_page_config(
    page_title="Anzma AI Insight",
    page_icon="🤖",
    layout="centered"
)

st.title("Anzma AI Insight")
st.caption("Local bilingual AI assistant | Powered by Ollama")

with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Choose AI model",
        list(MODELS.values()),
        index=1
    )
    st.caption("All responses are generated locally.")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask in Arabic or English...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + st.session_state.messages

    with st.chat_message("assistant"):
        with st.spinner("Generating response locally..."):
            try:
                payload = {
                    "model": model,
                    "messages": conversation,
                    "stream": False,
                    "options": {"num_ctx": 2048}
                }

                response = requests.post(
                    OLLAMA_URL,
                    json=payload,
                    timeout=300
                )
                response.raise_for_status()

                answer = response.json()["message"]["content"]
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to Ollama. "
                    "Please start the local Ollama server."
                )
            except requests.exceptions.Timeout:
                st.error("The model took too long to respond.")
            except (requests.exceptions.RequestException, KeyError, ValueError) as error:
                st.error(f"Request failed: {error}")
