import requests
import openai
import streamlit as st
import os

from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_image_url(query):
    """Returns the URL of an image from Unsplash"""
    ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

    url = 'https://api.unsplash.com/search/photos'
    headers = {'Authorization': f'Client-ID {ACCESS_KEY}'}
    params = {'query': query, 'page': 1, 'per_page': 1}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        image_url = [result['urls']['full'] for result in data['results']]
        return image_url
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def run_conversation(prompt):
    messages = [
        {"role": "user", "content": prompt}]
    functions = [
        # AIが、質問に対してこの関数を使うかどうか、決定する
        {
            "name": "get_image_url",
            "description": "Returns the URL of an image from Unsplash",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A query to search for",
                    },
                },
                "required": ["query"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        function_args = json.loads(
            response_message["function_call"]["arguments"])
        return function_args.get("query")
    else:
        return response_message


st.title("Unsplash Image Search")
st.markdown("This app uses OpenAI's API to search for images on Unsplash.")

prompt = st.text_input("What would you like to search for?")
if st.button("Search"):
    with st.spinner("Searching for images..."):
        query = run_conversation(prompt)
        image_url = get_image_url(query)
        if image_url:
            if len(image_url) == 1:
                # 配列に1つの要素がある場合の処理
                st.image(image_url[0])
            else:
                # 配列に複数の要素がある場合の処理
                for url in image_url:
                    st.image(url)
        else:
            st.markdown("Sorry, I couldn't find an image for that.")
