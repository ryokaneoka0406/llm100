import os
import json

import openai
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def create_sql(header_json, question):
    """
    データとデータの内容を読み込み、質問文のリストを生成する関数

    header_json:
        JSON
    question:
        str
    return:
        str
    """

    prompt = f"""
    You are a data analyst.You will now receives a JSON object below.
    This indicates the table name its column names.
    Return SQL to answer the given question. table name is "data".

    JSON:
    {header_json}

    Question:
    {question}

    SQL:
    """

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an excellent data analyst."},
            {"role": "user", "content": prompt},
        ]
    )

    return res['choices'][0]['message']['content']


st.title('AI CSV Analyst')
st.subheader('I read CSV header and answer question')
st.sidebar.title('Upload CSV')
uploaded_file = st.sidebar.file_uploader('Choose a file', type='csv')


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader('header')
    st.table(df.head(1))


question = st.text_input('Question')
if st.button('Answer'):
    header_json = json.dumps(df.head(1).to_json())
    sql = create_sql(header_json, question)

    db = df.to_sql('data', 'sqlite:///data.db', if_exists='replace')
    st.subheader('Answer')

    df_answer = pd.read_sql(sql, 'sqlite:///data.db')
    st.table(df_answer)
    st.write(sql)
