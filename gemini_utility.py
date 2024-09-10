import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

working_directory = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-1.5-pro")
    return gemini_pro_model

def load_gemini_flash_model(prompt, image):
    gemini_flash_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gemini_flash_model.generate_content([prompt, image])
    result = response.text
    return result

def embedding_model_response(input_text):
    embedding_model = "models/text-embedding-004"
    embedding = genai.embed_content(model=embedding_model, 
                                    content=input_text, 
                                    task_type="retrieval_document")
    return embedding

def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-1.5-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result
