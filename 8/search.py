import openai
from openai.embeddings_utils import cosine_similarity
import os

import json

openai.api_key = os.environ['OAI_API_KEY']

# データベースの読み込み
with open('index.json') as f:
    INDEX = json.load(f)

# これが検索用の文字列
QUERY = 'なんか甘くてオレンジのやつ'

# 検索用の文字列をベクトル化
query = openai.Embedding.create(
    model='text-embedding-ada-002',
    input=QUERY
)

query = query['data'][0]['embedding']

# 総当りで類似度を計算
results = map(
        lambda i: {
            'title': i['title'],
            'body': i['body'],
            # ここでクエリと各文章のコサイン類似度を計算
            'similarity': cosine_similarity(i['embedding'], query)
            },
        INDEX
)
# コサイン類似度で降順（大きい順）にソート
results = sorted(results, key=lambda i: i['similarity'], reverse=True)

# 以下で結果を表示
print(f"Query: {QUERY}")
print("Rank: Title Similarity")
for i, result in enumerate(results):
    print(f'{i+1}: {result["title"]} {result["similarity"]}')

print("====Best Doc====")
print(f'title: {results[0]["title"]}')
print(f'body: {results[0]["body"]}')

print("====Worst Doc====")
print(f'title: {results[-1]["title"]}')
print(f'body: {results[-1]["body"]}')