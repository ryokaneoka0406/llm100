from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import BytesIO
from urllib.request import urlopen
import os
import openai
import streamlit as st
from dotenv import load_dotenv
from openai.embeddings_utils import cosine_similarity


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def pdf_to_text(pdf_file):
    """Convert pdf file to text"""
    resource_manager = PDFResourceManager()
    fake_file_handle = BytesIO()
    converter = TextConverter(
        resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    for page in PDFPage.get_pages(pdf_file, caching=True, check_extractable=True):
        page_interpreter.process_page(page)

    text = fake_file_handle.getvalue().decode('utf-8')
    converter.close()
    fake_file_handle.close()
    return text


def get_embedding(text, model="text-embedding-ada-002"):
    """Get embedding for text"""
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def text_to_embeddings_json(text):
    """Split text into 1000 character chunks and return a list of"""
    split_texts = []
    for i in range(0, len(text), 1000):
        split_texts.append(
            {
                'text': text[i:i + 1000],
                'embedding': get_embedding(text[i:i + 1000])
            }
        )
    return split_texts


def generate_answer_from_chunk(context, question):
    """Generate answer from chunk"""

    prompt = f"""
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer in Japanese:
    """
    res = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a knowledgeable university professor"},
            {"role": "user", "content": prompt},
        ]
    )
    return res['choices'][0]['message']['content']


st.header("RAG without LangChain and VectorDB")
pdf_url = st.text_input("Enter URL of PDF file", key="url")
quesiton = st.text_input("Enter question", key="question")

if st.button("process"):
    with st.spinner("Embedding..."):
        try:
            with urlopen(pdf_url) as response:
                output = pdf_to_text(BytesIO(response.read()))
                index = text_to_embeddings_json(output)
        except Exception as e:
            st.write(f"Error: {e}")

    with st.spinner("Generate Answer..."):
        query = get_embedding(quesiton)
        results = map(
            lambda i: {
                'text': i['text'],
                # calculate cosine similarity
                'similarity': cosine_similarity(i['embedding'], query)
            },
            index
        )

        # sort by similarity
        results = sorted(results, key=lambda i: i['similarity'], reverse=True)
        answer = generate_answer_from_chunk(results[0]['text'], quesiton)

        st.subheader("Question")
        st.write(quesiton)
        st.subheader("Answer")
        st.write(answer)
        st.subheader("Source")
        st.write(results[0]['text'])
