from dotenv import load_dotenv
import os
import streamlit as st
from langchain.llms import OpenAI

load_dotenv()  # take environment variables from .env.
API_KEY = os.environ['OPENAI_API_KEY']

llm = OpenAI(openai_api_key=API_KEY, temperature=0.9)
haiku = llm("write a haiku about my father Mark")
print(haiku)