from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from io import StringIO
import streamlit as st
from dotenv import load_dotenv
import os  # ✅ Added to access environment variables
import time
import base64

load_dotenv()

st.title("Let's do code review for your java code")
st.header("Please upload your .java file here:")

# ✅ NEW: Input field to accept API key from user
user_api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Function to download text content as a file
def text_downloader(raw_text):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    b64 = base64.b64encode(raw_text.encode()).decode()
    new_filename = f"code_review_analysis_file_{timestr}_.txt"
    st.markdown("#### Download File ✅###")
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href, unsafe_allow_html=True)

data = st.file_uploader("Upload java file", type=".java")

# ✅ MODIFIED: Only proceed if both file and API key are provided
if data and user_api_key:
    stringio = StringIO(data.getvalue().decode("utf-8"))
    fetched_data = stringio.read()
    st.write(fetched_data)

    # ✅ MODIFIED: Use the API key from input instead of default
    chat = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.9,
        openai_api_key=user_api_key
    )

    systemMessage = SystemMessage(content="You are a code review assistant. Provide detailed suggestions to improve the given java code along by mentioning the existing code line by line with proper indent")
    humanMessage = HumanMessage(content=fetched_data)
    finalResponse = chat.invoke([systemMessage, humanMessage])

    st.markdown(finalResponse.content)
    text_downloader(finalResponse.content)

# ✅ NEW: Warn the user if they didn't enter the API key
elif data and not user_api_key:
    st.warning("⚠️ Please enter your OpenAI API key to proceed.")