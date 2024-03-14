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

    # API key input
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    if api_key:
        # Create an instance of the OpenAI LLM
        llm = OpenAI(openai_api_key=api_key, temperature=0.9)

        # Create a ConversationBufferMemory object to store chat history
        memory = ConversationBufferMemory(input_key='human', memory_key='chat_history')

        # Create a PromptTemplate with the given prompt
        prompt = PromptTemplate(
            input_variables=['human', 'chat_history'],
            template='''You are an expert in developing test cases for the purposes of automating the Enterprise Justice Case Management System. Your job is to create a detailed test case by interviewing me about the business process to be tested. You will first prompt me to provide a document that describes the business process. For each activity in the business process, you will help me generate a test case for that activity using a user manual that I will upload when you prompt me. When all of the activities have a test case written, I will ask you to generate a detailed test case for the complete business process.

            Chat History:
            {chat_history}

            Human: {human}

            Assistant:'''
        )

        # Create an LLMChain with the specified prompt, llm, and memory
        chain = LLMChain(prompt=prompt, llm=llm, verbose=True, memory=memory)

        # Chat container
        chat_container = st.container()

        # User input
user_input = st.text_input("You:", key='user_input', value='')

if user_input:
    # Pass the user input to the chain and get the response
    response = chain.run(human=user_input)

    # Append the user input and assistant response to the chat container
    chat_container.text(f"You: {user_input}")
    chat_container.text(f"Assistant: {response}")

            # Clear the user input
            st.session_state.user_input = ""

        # File uploader
        uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

        if uploaded_files:
            for file in uploaded_files:
                # Read the contents of the file
                file_contents = file.read().decode("utf-8")

                # Pass the file contents to the chain and get the response
                response = chain.run(human=file_contents)

                # Display the response
                st.subheader(f"Test Case for {file.name}")
                st.text(response)

    else:
        st.warning("Please enter your OpenAI API key to generate test cases.")

if __name__ == "__main__":
    main()
