import streamlit as st
import json
import time

def get_bot_response(user_input):
    # Simulate bot response generation
    time.sleep(1)  # Simulate processing time
    response = f"You said: {user_input}"
    
    # Create a sample JSON response
    json_response = {
        "input": user_input,
        "response": response,
        "confidence": 0.95,
        "timestamp": time.time()
    }
    
    return json_response

st.title("Chatbot Interface with JSON Display")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get bot response
    response = get_bot_response(prompt)

    # Display JSON response
    with st.expander("View Intermediate JSON"):
        st.json(response)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response["response"])
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response["response"]})

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.experimental_rerun()