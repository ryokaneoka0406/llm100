import os

from dotenv import load_dotenv
import openai
import streamlit as st

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def create_caption(sentence):
    prompt = f"""
    The following text is the user's diary. Please summarize the scenes from this diary in a caption.
    An illustrator will be asked to draw an illustration based on this caption.
    Therefore, make sure that the caption represents the content of the user's diary in a straightforward manner.

    Sentense:
    {sentence}

    Example:
        - sentence: I went to the park with my friends but it suddenly started raining.
        - caption: Two people running in the park in the rain.

    Caption:
    """
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {"role": "system", "content": "You are an excellent caption editor."},
            {"role": "user", "content": prompt},
        ]
    )
    return res['choices'][0]['message']['content']


def draw_illustration(caption):
    response = openai.Image.create(
        prompt=caption,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url


st.header('Making illustrations from the diary')
st.subheader('Input what happened today')

sentence = st.text_area('Sentence', height=100)
if sentence:
    with st.spinner('Loading...'):
        caption = create_caption(sentence)
        print(caption)
        image_url = draw_illustration(caption)

    st.image(image_url)
