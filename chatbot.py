# My own AI chatbot
# Setup:
#   pip install streamlit anthropic
#   Get an API key from https://console.anthropic.com
#   Mac/Linux:  export ANTHROPIC_API_KEY="your-key-here"
#   Windows:    set ANTHROPIC_API_KEY=your-key-here
# Run:
#   streamlit run chatbot.py

import streamlit as st
import anthropic

MODEL = "claude-sonnet-5-5"
SYSTEM_PROMPT = "You are a friendly, helpful assistant. Keep answers clear and concise."

st.set_page_config(page_title="My Chatbot", page_icon="💬")
st.title("💬 My Chatbot")

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from your environment

# Chat history survives between messages in this browser session
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    if st.button("New chat"):
        st.session_state.messages = []
        st.rerun()

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle a new message
if prompt := st.chat_input("Ask me anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        reply = ""
        try:
            # Stream the answer word by word, like ChatGPT
            with client.messages.stream(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages,
            ) as stream:
                for text in stream.text_stream:
                    reply += text
                    placeholder.markdown(reply + "▌")
            placeholder.markdown(reply)
        except anthropic.AuthenticationError:
            reply = "API key missing or wrong. Set ANTHROPIC_API_KEY and restart."
            placeholder.error(reply)
        except Exception as e:
            reply = f"Something went wrong: {e}"
            placeholder.error(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
