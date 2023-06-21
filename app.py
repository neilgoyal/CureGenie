import os
import tempfile
import streamlit as st
import json
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from pdf_parser import parse_pdf
from meal_planner import start_chat, load_config, pretty_print_json

# Load image (can be .jpg, .png, etc.)
image = './logo.png'

# Display image with a caption
st.image(image, width=200)

# Sidebar contents
with st.sidebar:
    st.title('Meal and Workout Planner')
    st.markdown('''
    ## About
    This app uses OpenAI's GPT-4 to suggest meal and workout plans tailored to your needs.
    Contributors @ A.I. Cal Hackathon 2023:
    - Neil
    - Cesar
    - Christopher
    - Andrew
    ''')
    add_vertical_space(5)
    st.write('Main Branch with [Neil](https://github.com/neilgoyal)')

load_dotenv('/home/ubuntu/App/.env')

def main():
    st.markdown("## All information provided does not constitute professional medical advice.")

    # Load configuration variables
    openai_api_key, completion_model = load_config()

    # Upload a PDF file containing bloodwork (optional)
    bloodwork_pdf = st.file_uploader("Upload your bloodwork (PDF, optional)", type='pdf')

    # Parse the PDF if provided
    bloodwork = None
    if bloodwork_pdf is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tfile:
            tfile.write(bloodwork_pdf.read())
            bloodwork = parse_pdf(tfile.name)
        os.unlink(tfile.name)  # Delete the temporary file

    # Input for the number of days and user's needs
    user_input = st.text_input("Please enter the number of days for the meal and workout plan along with your needs:")

    if st.button("Generate Plan"):
        if user_input:
            try:
                meal_suggestions, final_response = start_chat(openai_api_key, completion_model, user_input, bloodwork)
                st.json(meal_suggestions) # Display Meal Plan JSON
                st.write(final_response)  # Display the final response in the Streamlit app
            except Exception as e:
                st.write(f"An error occurred: {e}")
        else:
            st.write("Please enter the number of days and your needs to generate your meal and workout plans: ")

if __name__ == '__main__':
    main()

