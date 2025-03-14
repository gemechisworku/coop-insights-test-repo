import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://localhost:8000/process_query/"

# Streamlit UI
st.title("Chat with Coop Insights")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask something...")
if user_input:
    # Display user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Call FastAPI backend
    response = requests.get(API_URL, params={"user_prompt": user_input})
    response_json = response.json()
    if isinstance(response_json, list):
        bot_reply = response_json[0]  # Get the first item if it's a list
    else:
        bot_reply = response_json.get("response", response_json)

    
    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    
    # Store bot response in session state
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
