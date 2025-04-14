import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

st.set_page_config(page_title="EduDetect - Chatbot", layout="wide")

# Add sidebar
st.sidebar.header("Chatbot")
st.sidebar.write("EduDetect AI Chatbot")

# Main content
st.title("AI Chatbot")

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
  # Add user message to chat history
  st.session_state.messages.append({"role": "user", "content": prompt})
  
  # Display user message
  with st.chat_message("user"):
    st.markdown(prompt)
  
  # Display assistant response in chat message container
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    
    # Create Groq API request
    chat_completion = client.chat.completions.create(
      model="llama-3.3-70b-versatile",
      messages=[
        {"role": m["role"], "content": m["content"]} 
        for m in st.session_state.messages
      ],
      temperature=0.7,
      max_completion_tokens=4096,
      stream=True,
    )
    
    # Stream the response
    for chunk in chat_completion:
      content = chunk.choices[0].delta.content or ""
      full_response += content
      message_placeholder.markdown(full_response + "▌")
    
    message_placeholder.markdown(full_response)
  
  # Add assistant response to chat history
  st.session_state.messages.append({"role": "assistant", "content": full_response})