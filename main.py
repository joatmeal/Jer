from dotenv import load_dotenv
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

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

        # Chat container
        chat_container = st.container()

        # User input
        user_input = st.text_input("You:", key='user_input', value='')

        if user_input:
            # Append the user input to the chat history
            memory.save_context({'human': user_input}, {'ai': ''})

            # Generate the AI response
            ai_response = llm.predict(
                prompt=f"{memory.load_memory_variables({})}Human: {user_input}\nAssistant:",
                stop=["Human:"]
            )

            # Append the AI response to the chat history
            memory.save_context({'human': user_input}, {'ai': ai_response})

            # Append the user input and AI response to the chat container
            chat_container.text(f"You: {user_input}")
            chat_container.text(f"Assistant: {ai_response}")

        # File uploader
        uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

        if uploaded_files:
            for file in uploaded_files:
                # Read the contents of the file
                file_contents = file.read().decode("utf-8")

                # Append the file contents to the chat history
                memory.save_context({'human': file_contents}, {'ai': ''})

                # Generate the AI response based on the file contents
                ai_response = llm.predict(
                    prompt=f"{memory.load_memory_variables({})}Human: {file_contents}\nAssistant:",
                    stop=["Human:"]
                )

                # Append the AI response to the chat history
                memory.save_context({'human': file_contents}, {'ai': ai_response})

                # Display the AI response
                st.subheader(f"Test Case for {file.name}")
                st.text(ai_response)

    else:
        st.warning("Please enter your OpenAI API key to generate test cases.")

if __name__ == "__main__":
    main()
