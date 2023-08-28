import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

# PDFをアップロードして、chunk、それについて質問できるシステムを作る
# VectorDBはあえて使わない