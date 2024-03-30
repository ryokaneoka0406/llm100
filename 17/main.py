import os

from dotenv import load_dotenv
import anthropic
import streamlit as st
from PyPDF2 import PdfReader

load_dotenv()

# helper function to extract text from pdf
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# streamlit app
st.title("Job description Q&A with Claude3 Opus")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("YOUR Claude API Key", type="password")
client = anthropic.Anthropic(
    api_key=api_key,
)

# Extract text from uploaded pdf
uploaded_file = st.file_uploader("Upload your job description(pdf)", type="pdf")
if uploaded_file is not None:
        # PDFファイルからテキストを抽出
        job_description = extract_text_from_pdf(uploaded_file)

if st.button("Generate Q&A"):
    with st.spinner("Generating Q&A..."):
        # prompt
        PROMPT = f"""
        You are an excellent career change agent.

        From now on, I would like you to support my job search activities.

        Below is my resume.

        <JobDescription>
        {job_description}
        </JobDescription>

        Please prepare 5 questions and expected answers related to my resume. Follow the output format specified in <example>.
        (output only the markdown, without including the <example> tags)

        <example>
        - Q1. You mentioned "introducing OKRs", but what specifically did you do?
        - A1. I conducted a pilot project within my own product team, created documentation, and shared insights with the product team. 
        </example>
        """

        # generate Q&A
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": PROMPT},
            ]
        )

        st.write(message.content[0].text)