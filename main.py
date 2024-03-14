from dotenv import load_dotenv
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
API_KEY = os.getenv('OPENAI_API_KEY')

# Streamlit app
def main():
    st.title("Manual Test Generator")
    st.write("This bot takes a story, spec or user guide and generates manual test cases from it. To get started, add your document, modify the prompt (if needed) and hit go!")

    # API key input
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    if api_key:
        # Create an instance of the OpenAI LLM
        llm = OpenAI(openai_api_key=api_key, temperature=0.9)

        # File uploader
        uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True, type=["txt", "docx", "pdf"])

        if uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    # Read the contents of the file
                    file_contents = uploaded_file.read().decode("utf-8")

                    # Prompt
                    prompt = st.text_area("Prompt", value="You are an expert in developing test cases for the purposes of automating the Enterprise Justice Case Management System.  Your job is to create a detailed test case by interviewing me about the business process to be tested.  You will first prompt me to provide a document that describes the business process.  For each activity in the business process, you will help me generate a test case for that activity using a user manual that I will upload when you prompt me.   When all of the activities have a test case written, I will ask you to generate a detailed test case for the complete business process.  If you understand, say yes and prompt me to upload the Business Process documentation.", height=300)

                    # Create a PromptTemplate with the given prompt
                    prompt_template = PromptTemplate(input_variables=["file_contents"], template=prompt)

                    # Create an LLMChain with the specified prompt, llm, and memory
                    chain = LLMChain(prompt=prompt_template, llm=llm)

                    # Generate the manual test case
                    if st.button(f"Generate Test Case for {uploaded_file.name}"):
                        # Pass the file contents to the chain and get the response
                        response = chain.run(file_contents=file_contents)

                        # Display the response
                        st.subheader(f"Manual Test Case for {uploaded_file.name}")
                        st.text(response)
                except Exception as e:
                    st.error(f"Error processing file {uploaded_file.name}: {str(e)}")
    else:
        st.warning("Please enter your OpenAI API key to generate test cases.")

if __name__ == "__main__":
    main()
