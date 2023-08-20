import streamlit as st
from dotenv import load_dotenv
import openai
import os
from pydub import AudioSegment
import tempfile

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def transcribe(audio_segment, prompt="Transcribe the audio file"):
    # 一時的なファイルにエクスポート
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_segment.export(temp_file, format="wav")

    # ファイル名をtranscribe関数に渡す
    result = openai.Audio.transcribe(
        "whisper-1", temp_file, propmpt=prompt)

    # 一時ファイルを削除
    os.unlink(temp_file.name)

    return result


def to_markdown(transcription):
    """文字起こしをマークダウン箇条書きに変換する関数"""
    prompt = f"""
    Below is the text of the audio transcription.
    Convert it to a markdown bulleted text in Japanese, formatting the parts that are difficult to make sense of.

    Transcription:
    {transcription}
    """

    res = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are an astute editor."},
            {"role": "user", "content": prompt},
        ]
    )
    return res['choices'][0]['message']['content']


st.title("Audio Transcription")

uploaded_file_long = st.file_uploader("Upload a file", type=[
                                      "mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "web"], key="long_file")
prompt = st.text_area(
    "What is this file about?", key="prompt")

if uploaded_file_long is not None:
    if st.button("Transcribe", key="long_transcribe"):
        with st.spinner("Preparing..."):
            origin = AudioSegment.from_file(uploaded_file_long)
            # PyDub handles time in milliseconds
            two_minutes = 2 * 60 * 1000

        data = []

        for i in range(0, len(origin), two_minutes):
            with st.spinner("Transcribing..."):
                transcript = transcribe(origin[i:i+two_minutes], prompt)
                text = to_markdown(transcript["text"])
                st.write(text)
                data.append(text)

        st.markdown("---")
        st.markdown("## Merged Text")
        st.markdown("\n".join(data))
