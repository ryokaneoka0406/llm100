from openai import OpenAI
import streamlit as st
import pyautogui
import io
import base64
import os
from dotenv import load_dotenv

# st.sidebar.title("Settings")
# api_key = st.sidebar.text_input("API Key", type="password")

load_dotenv()

# スクリーンショットを取得する関数
def take_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

# 画像をBase64形式にエンコードする関数
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# 画像のURLをAPIに送信する関数
def send_image_url(image_url):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": """
                 The image being sent is a screenshot that shows a web browser or an e-book.
                 Read the text in the image on the right side of the screen and summarize its content.
                 """},
                {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                },
                },
            ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

# Streamlitアプリの定義
st.title("Screenshot Sender")

if st.button("Take Screenshot and Send"):
    screenshot = take_screenshot()
    st.image(screenshot, caption="Screenshot", use_column_width=True)
    base64_image = encode_image(screenshot)
    response = send_image_url(f"data:image/png;base64,{base64_image}")
    st.success(response)