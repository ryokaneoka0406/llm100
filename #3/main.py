from dotenv import load_dotenv

import openai
import streamlit as st
from google.cloud import texttospeech
from pydub import AudioSegment

import os
import json
import pprint


load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_texts(situation):
    prompt = f"""
    You are an English teacher.
    You are asked to create 10 example sentences in English that can be used in the following situation.

    ## Situation
    {situation}

    ## Conditions
    - Output must be in the following format
    ```
    Japanese example sentence 1\n
    English example sentence 1\n
    Japanese example sentence 2\n
    English example sentence 2\n
    ...
    Japanese example sentence 10\n
    English example sentence 10\n
    ````
    - Do not output any sentences other than the above example sentences. For example, a response such as "I understand" is also unnecessary.

    ## Example output
    こんにちは！\n
    Hello!\n
    さようなら！\n
    Goodbye!\n
    会えて嬉しいです！\n
    Nice to meet you!
    """
    res = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are an English teacher."},
            {"role": "user", "content": prompt},
        ]
    )
    return res['choices'][0]['message']['content']


def text_to_sentences_json(texts):
    content = f"""
    Generate an audio file that reads the following texts

    ## Texts
    {texts}
    """
    functions = [
        # AIが、質問に対してこの関数を使うかどうか、決定する
        {
            "name": "generate_and_combine_audio",
            "description": "Generate audio files from given English and Japanese sentences",
            "parameters": {
                "type": "object",
                "properties": {
                    "sentences": {
                        "type": "array",
                        "description": "List of Japanese and English sentences",
                        "items": {
                            "type": "object",
                            "description": "Japanese and English sentence",
                            "properties": {
                                "japanese": {"type": "string"},
                                "english": {"type": "string"},
                            }
                        }
                    },
                },
                "required": ["sentences"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ],
        functions=functions,
        function_call={"name": "generate_and_combine_audio", }
    )
    try:
        result = json.loads(
            response.choices[0].message.function_call.arguments)
        return result
    except:
        print("error")
        pprint(response.choices[0].message.function_call.arguments)


def ssml_to_audio(ssml_text, langage_code, outfile):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=langage_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(outfile, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file ' + outfile)


def text_to_ssml(input_text):
    return "<speak>{}</speak>".format(
        input_text.replace("\n", "<break time='10s'/>")
    )


def generate_and_combine_audio(sentences):
    # 日本語と英語の音声ファイルを一時的に保存するためのリスト
    temp_files = []

    for i, sentence in enumerate(sentences):
        japanese_ssml = text_to_ssml(sentence["japanese"])
        english_ssml = text_to_ssml(sentence["english"])

        # 一時的なファイル名を作成
        japanese_file = f"temp_japanese_{str(i)}.mp3"
        english_file = f"temp_english_{str(i)}.mp3"

        ssml_to_audio(japanese_ssml, "ja-JP", japanese_file)
        ssml_to_audio(english_ssml, "en-US", english_file)

        temp_files.append(japanese_file)
        temp_files.append(english_file)

    # pydubを使用して全てのファイルを結合
    combined_audio = AudioSegment.empty()
    for f in temp_files:
        combined_audio += AudioSegment.from_mp3(f)

    # 最終的なファイルとして保存
    combined_audio.export("combined_output.mp3", format="mp3")

    # 一時ファイルの削除
    for f in temp_files:
        os.remove(f)


st.title("Text to Speech")
st.header("Generatate English sentences from your situation")

st.subheader("Situation")
situation = st.text_area(
    "Enter text to describe your situation", key="input_text")

if st.button("Generate"):
    with st.spinner("Generating..."):
        texts = generate_texts(situation)
        st.write(texts)

        data = text_to_sentences_json(texts)
        st.write("Converted!")
        st.write(data)

        generate_and_combine_audio(data["sentences"])
        st.write("Generated!")
        st.audio("combined_output.mp3")
