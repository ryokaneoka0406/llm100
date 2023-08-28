import openai
import os

import json

openai.api_key = os.environ['OAI_API_KEY']

# 入力用の文章をロード
with open('docs.json') as f:
    docs = json.load(f)

index = []
for doc in docs:
    # ここでベクトル化を行う
    # openai.embeddings_utils.embeddings_utilsを使うともっとシンプルにかけます
    res = openai.Embedding.create(
        model='text-embedding-ada-002',
        input=doc['body']
    )

    # ベクトルをデータベースに追加
    index.append({
        'title': doc['title'],
        'body': doc['body'],
        'embedding': res['data'][0]['embedding']
    })

with open('index.json', 'w') as f:
    json.dump(index, f)