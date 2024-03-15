from dotenv import load_dotenv
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
API_KEY = os.getenv('OPENAI_API_KEY')

# Streamlit app
def main():
    st.title("Manual Test Generator")

    # API key input 
    st.header("OpenAI API Key")
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    if api_key:
        # Create an instance of the OpenAI LLM
        llm = OpenAI(openai_api_key=api_key, temperature=0.9)
        
        # Create a ConversationBufferMemory object to store chat history
        memory = ConversationBufferMemory(input_key='human', memory_key='chat_history')
        
        # Create a PromptTemplate with the given prompt
        prompt = PromptTemplate(
            input_variables=['human', 'chat_history'],  
            template='''You are an AI assistant created by OpenAI. Your role is to assist in developing test cases for the purposes of automating the Enterprise Justice Case Management System. The user will provide a document describing the business process and a user manual. For each activity in the business process, help the user generate a test case using the provided user manual. When all activities have a test case, generate a detailed test case for the complete business process.

Chat History:
{chat_history}
