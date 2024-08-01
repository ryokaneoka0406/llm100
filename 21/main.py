import os
import base64

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OpenAI APIキーの設定
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def generate_json_schema(infomation):
    json_schema = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional programmer."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""
                                Define and return a JSON schema from the following information.
                                Return only the information from the JSON schema.

                                # information
                                {information}
                                """
                            },
                        ]
                    }
                ],
                max_tokens=300
            )
    return json_schema.choices[0].message.content


st.title("画像情報抽出アプリ")
information = st.text_area("画像から抽出したい情報を入力してください", """
例：
- タイトル（文字）
- 説明（文字）
- カテゴリ（文字）
- 人数（数値）
""")

uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="アップロードされた画像", use_column_width=True)

    if st.button("分析開始"):
        with st.spinner("画像を分析中..."):
            json_format = generate_json_schema(information)
            base64_image = encode_image(uploaded_file)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "You are a useful data converter."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""
                                Extract the information shown in the attached image into the following JSON format.
                                Leave any information that cannot be read from the image blank.
                                Only return the specified JSON format.

                                # JSON Format
                                {json_format}
                                """
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )

            result = response.choices[0].message.content
            st.json(result)
else:
    st.warning("画像をアップロードしてください。")