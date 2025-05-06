import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')  # Updated model
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"

# Function to prepare uploaded image for Gemini
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Streamlit UI setup
st.set_page_config(page_title="Gemini Health App")
st.header("🥗 Gemini Health App – Calorie Estimator")

uploaded_file = st.file_uploader("📷 Upload a food image", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Prompt
input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food items with calories intake
in the below format:

1. Item 1 - number of calories  
2. Item 2 - number of calories  
...  

Finally, you can also mention whether the food is healthy or not.
"""

# Submit button
if st.button("Tell me the total calories"):
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("📋 Analysis Result:")
        st.write(response)
    else:
        st.error("⚠️ Please upload an image before clicking the button.")
