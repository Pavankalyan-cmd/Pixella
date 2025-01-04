import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def get_gemini_response(input, image):
    """Get a response from the Gemini model based on the input and image."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        if input:
            response = model.generate_content([input, image])
        else:
            response = model.generate_content(image)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit App
def main():
    st.set_page_config(page_title='Pixella')
    st.header("Pixella")

    # Input prompt
    input_prompt = st.text_input('Input prompt:', key='input')

    # Image uploader
    upload_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'])
    image = None
    if upload_file is not None:
        image = Image.open(upload_file)
        st.image(image, caption='Uploaded image', use_column_width=True)

    # Submit button
    if st.button("Explain brief about image"):
        if image is not None:
            response = get_gemini_response(input_prompt, image)
            st.subheader('The response is')
            st.write(response)
        else:
            st.warning("Please upload an image first.")

if __name__ == "__main__":
    main()