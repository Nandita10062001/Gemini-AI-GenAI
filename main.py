import os
import streamlit as st
from streamlit_option_menu import option_menu 
from gemini_utility import (load_gemini_pro_model, 
                            load_gemini_flash_model, 
                            embedding_model_response,
                            gemini_pro_response)
from PIL import Image

working_directory = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:

    selected = option_menu(
        "Gemini AI",
        ["Chatbot", 
         "Image Captioning", 
         "Embed Text", 
         "Ask me anything!"],
        menu_icon = 'robot', 
        icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
        default_index =0)

#function to translate role between gemini pro and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if selected == "Chatbot":

    model = load_gemini_pro_model()

    # Initialize chat session in streamlit if not already present

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    
    st.title("🤖 Chatbot")

    # Display Chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)


    # Input for user's message
    user_prompt = st.chat_input("Ask Gemini Pro....")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)


        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        #display response on streamlit webpage

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


if selected == "Image Captioning":
    
    st.title("📷 Image Caption Generator")

    uploadedImage = st.file_uploader("Upload an image....", type=['jpg','jpeg','png'])

    if st.button("Generate Caption"):

        image = Image.open(uploadedImage)

        col1,col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800,500), Image.Resampling.LANCZOS)
            st.image(resized_image)

        default_prompt = "Write a caption for this image"

        caption = load_gemini_flash_model(default_prompt, image)

        with col2:
            st.info(caption)

if selected == "Embed Text":
    st.title("🔡 Embed Text")

    input_text = st.text_area(label="", placeholder="Enter the text you want to embed...")
    
    if st.button("Get Embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)

if selected == "Ask me anything!":
    st.title("❓Ask Me Anything!")
    user_prompt = st.text_area(label="", placeholder="Ask Gemini....")

    if st.button("Get Response"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)
