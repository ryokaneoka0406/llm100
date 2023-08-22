from dotenv import load_dotenv
import os
import streamlit as st

import openai
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
import plotly.express as px

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


# データ読み込み
df = pd.read_csv("data/movie_survey.csv")

st.title("Anomaly detection with ada model")
st.subheader("dataset")
st.table(df.head())
st.markdown("""
- 映画についてのアンケートデータ
- 10%の確率で、政治的なネガティブなトピックが混入するようにした

- Sample survey data about the movie
- 10% chance of negative political topics to be mixed in
""")

# ベクトル化
st.subheader("Embedding and visualize in 2D")
if st.button("process"):
    with st.spinner("Embedding..."):
        df["embedding"] = df["answer_japanese"].apply(get_embedding)
        st.table(df.head())

    with st.spinner("Processing..."):
        matrix = np.array(df['embedding'].to_list())
        tsne = TSNE(n_components=2, perplexity=15, random_state=42,
                    init='random', learning_rate=200)
        vis_dims = tsne.fit_transform(matrix)

        df["x"] = vis_dims[:, 0]
        df["y"] = vis_dims[:, 1]

        fig = px.scatter(df, x="x", y="y", color="topic",
                         title="Annomaly Detection with Embedding")
        st.plotly_chart(fig, use_container_width=True)
