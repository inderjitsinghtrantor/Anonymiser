import streamlit as st
import json
import time
import updated_run as urun

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

st.title("Chatbot PII anonymiser with intermediat JSON Display")

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
    # response = get_bot_response(prompt)  # TODO use your function
    masked_response_dict, response = urun.secure_request(prompt)
    print(f"##### masked response dict: {masked_response_dict}\nresponse: {response}")

    # Display JSON response
    with st.expander("View Intermediate JSON"):
        st.json(masked_response_dict) # TODO your intermediate json

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response) # TODO response from the function
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()