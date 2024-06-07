
import streamlit as st
import google.generativeai as genai

headers = {
    'authorization' : st.secrets['API_KEY'],
    'content-type': 'application/json'
}
genai.configure(api_key=headers['authorization'])

generation_config = {
  "temperature": 0.55,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config, 
)
chat = model.start_chat(history=[])

def get_response(user_input):
    response = chat.send_message(user_input)
    return response.text

def main():
    st.set_page_config(layout="centered")
    st.title("KuniKo GPT ")

    # # Sidebar for image upload
    # st.sidebar.title("Menu")
    # image_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    # if image_file is not None:
    #     st.sidebar.image(image_file, caption="Uploaded Image", use_column_width=True)

    st.write("Ask me anything!")

    # Initialize session state for chat history
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Chat history container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.history:
            st.write(message)

    # Text input at the bottom
    user_input = st.text_input("You:", key="input", placeholder="Type your message here...")

    col1, col2 = st.columns([1, 5])
    
    with col1:
        send_button = st.button("Send")
    
    with col2:
        clear_button = st.button("Clear Chat")

    if send_button and user_input:
        response = get_response(user_input)
        st.session_state.history.append(f"You: {user_input}")
        st.session_state.history.append(f"Bot: {response}")
        st.experimental_rerun()  # To refresh the page and display the new message

    if clear_button:
        st.session_state.history = []
        st.experimental_rerun()  # To refresh the page and clear the chat

if __name__ == "__main__":
    main()

