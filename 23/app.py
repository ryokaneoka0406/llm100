import streamlit as st
from setup import setup_index
from chat import chat_with_model
import tempfile
import os

st.title("Fully local PDF RAG with gemma2:9b, e5-base-multilingual and LlamaIndex")

# Initialize session state
if 'index' not in st.session_state:
    st.session_state.index = None
if 'llm' not in st.session_state:
    st.session_state.llm = None
if 'file_processed' not in st.session_state:
    st.session_state.file_processed = False

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None and not st.session_state.file_processed:
    if st.button("Process File"):
        with st.spinner("Processing file..."):
            # Save as a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            # Create index
            st.session_state.index, st.session_state.llm = setup_index(tmp_file_path)

            # Delete temporary file
            os.unlink(tmp_file_path)

            st.session_state.file_processed = True
            st.success("File processing completed!")

if st.session_state.file_processed:
    st.subheader("Ask a question")
    query = st.text_input("Enter your question")

    if query:
        if st.button("Submit"):
            with st.spinner("Generating answer..."):
                response_text = chat_with_model(query, st.session_state.index, st.session_state.llm)
                st.write("Answer:", response_text)

st.sidebar.markdown("""
## How to use
1. Upload a PDF file.
2. Click the "Process File" button and wait for processing to complete.
3. Enter your question and click the "Submit" button to see the answer.
""")

# Button for processing a new file
if st.session_state.file_processed:
    if st.sidebar.button("Process a new file"):
        st.session_state.file_processed = False
        st.session_state.index = None
        st.session_state.llm = None
        st.experimental_rerun()