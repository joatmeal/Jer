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

    if api_key:
        # Create an instance of the OpenAI LLM
        llm = OpenAI(openai_api_key=api_key, temperature=0.9)

        # Generate haiku button
        if st.button("Generate poem"):
            # Generate a haiku
            haiku = llm("write a poem about my wife Mariah")

            # Display the generated haiku
            st.subheader("Generated Haiku")
            st.text(haiku)
    else:
        st.warning("Please enter your OpenAI API key to generate a haiku.")

if __name__ == "__main__":
    main()
