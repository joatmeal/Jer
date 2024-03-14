from dotenv import load_dotenv
import os
import streamlit as st
from langchain.llms import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
API_KEY = os.getenv('OPENAI_API_KEY')

# Streamlit app
def main():
    st.title("OpenAI Haiku Generator")

    # API key input
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    # File uploader
    uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True)

    if api_key:
        # Create an instance of the OpenAI LLM
        llm = OpenAI(openai_api_key=api_key, temperature=0.9)

        # Generate haiku button
        if st.button("Generate Haiku"):
            if uploaded_files:
                # Process uploaded files
                for file in uploaded_files:
                    # Read the contents of the file
                    file_contents = file.read().decode("utf-8")

                    # Generate a haiku based on the file contents
                    haiku = llm(f"write a haiku about the following text: {file_contents}")

                    # Display the generated haiku
                    st.subheader(f"Generated Haiku for {file.name}")
                    st.text(haiku)
            else:
                st.warning("Please upload at least one file to generate haikus.")
    else:
        st.warning("Please enter your OpenAI API key to generate haikus.")

if __name__ == "__main__":
    main()
