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
        
        prompt = PromptTemplate(
    input_variables=['human', 'chat_history', 'context'],  
    template='''You are an AI assistant created by OpenAI. Your role is to assist in developing test cases for the purposes of automating the Enterprise Justice Case Management System. The user will provide a request or prompt, along with any relevant files as context. Generate a response based on the user's request and the provided context.

Context:
{context}

Chat History:
{chat_history}
