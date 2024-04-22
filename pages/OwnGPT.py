import streamlit as st
import ollama
import time
import textwrap

# Initialize the session state variables if not already present
if 'messages' not in st.session_state:
    st.session_state.messages = []

def send_to_model():
    with st.spinner("One moment please..."):
        # Filter messages to ensure they only contain valid fields and correct roles
        formatted_messages = [{'role': msg['role'], 'content': msg.get('content', '')} for msg in st.session_state.messages if 'content' in msg and msg['role'] in ['user', 'assistant']]
        
        # Call to ollama model
        result = ollama.chat(model="llama3", messages=formatted_messages)
        
        if result and 'message' in result:
            response = result['message']['content']
            # Create a placeholder for the assistant's response to initiate the display
            response_placeholder = st.empty()
            current_text = ""  # Initialize an empty string to accumulate characters
            for char in response:
                current_text += char  # Append each character to the accumulator string
                wrapped_text = '\n'.join(textwrap.wrap(current_text, width=8))
                response_placeholder.text(current_text)  # Update the placeholder with the accumulated text
                time.sleep(0.05)  # Adjust sleep time to control the speed of the 'typing'
            # Once complete, append the full response to the session state
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Trigger a rerun to update the conversation display
        st.experimental_rerun()


# Display the chat messages
if 'messages' in st.session_state:
    for message in st.session_state.messages:
        with st.container():
            if message['role'] == 'user':
                if 'content' in message:
                    st.info(message['content'])  # User's messages in one style
                if 'image' in message:
                    st.image(message['image'])  # Display user's uploaded image
            elif message['role'] == 'assistant':
                st.success(message['content'])  # Assistant's responses in another style

# Form for input and submission
with st.form(key='chat_form'):
    prompt = st.text_input("Ask anything", key="chat_input")
    uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    submit_button = st.form_submit_button("Send")

if submit_button:
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
    if uploaded_file is not None:
        # If the model cannot handle images, you might store image locally or handle differently
        # Currently, adding image information as a placeholder
        st.session_state.messages.append({"role": "user", "content": "[User uploaded an image]", "image": uploaded_file.getvalue()})
    
    if prompt or uploaded_file:
        send_to_model()
    
    # Clear the input field by resetting the key in session state to trigger UI refresh
    del st.session_state['chat_input']  # Deleting the key to reset the form input
