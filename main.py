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
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "pdf"])

        if uploaded_file is not None:
            # Read the contents of the file
            file_contents = uploaded_file.read().decode("utf-8")

            # Prompt
            prompt = st.text_area("Prompt", value="Read through the attached Quick Reference Guide word document closely, summarizing the key steps of the business process. Then, write out a detailed manual test case that covers each of the steps, inputs, and expected outputs of the business process. The test case should be written clearly enough that someone unfamiliar with the process could execute it successfully. Make sure to include:\n\nA descriptive test case name\nAny prerequisite steps\nTest data to use\nStep-by-step actions to take\nInputs and data to use at each step\nExpected system responses and outputs at each step\nAny cleanup steps to reset the state for the next test run\n\nThe test case should cover the normal successful path through the business process.\n\nIn summary, please read through the attached Quick Reference Guide and write a comprehensive manual test case that covers the end-to-end business process flow and key validation points, written clearly enough for someone new to follow and execute.", height=300)

            # Create a PromptTemplate with the given prompt
            prompt_template = PromptTemplate(input_variables=["file_contents"], template=prompt)

            # Create an LLMChain with the specified prompt, llm, and memory
            chain = LLMChain(prompt=prompt_template, llm=llm)

            # Generate the manual test case
            if st.button("Submit"):
                # Pass the file contents to the chain and get the response
                response = chain.run(file_contents=file_contents)

                # Display the response
                st.subheader(f"Manual Test Case for {uploaded_file.name}")
                st.text(response)
    else:
        st.warning("Please enter your OpenAI API key to generate test cases.")

if __name__ == "__main__":
    main()
