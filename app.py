import streamlit as st
from google import genai

# -------------------------
# Setup
# -------------------------

# Read API key from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]

# Create client
client = genai.Client(api_key=api_key)

# Choose model
model = "gemini-2.5-flash-lite"


# -------------------------
# YOUR STREAM FUNCTION
# -------------------------

def stream_chat(prompt, system=None):

    params = {
        "model": model,
        "contents": prompt
    }

    # Add system prompt if provided
    if system:
        params["config"] = {
            "system_instruction": system
        }

    # Stream response
    response = client.models.generate_content_stream(**params)

    # Yield chunks instead of print
    for chunk in response:
        if chunk.text:
            yield chunk.text


# -------------------------
# UI
# -------------------------

st.title("My Gemini Chatbot")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask something...")

if user_input:

    # Show user message
    st.chat_message("user").markdown(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Assistant message container
    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        full_response = ""

        # Use YOUR function
        for chunk in stream_chat(
            user_input,
            system="you're a scientist"
        ):
            full_response += chunk
            response_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })
