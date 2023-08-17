from dotenv import load_dotenv
import openai
import os
from pydub import AudioSegment
import tempfile


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def transcribe(audio_segment):
    # 一時的なファイルにエクスポート
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_segment.export(temp_file, format="wav")

    # ファイル名をtranscribe関数に渡す
    result = openai.Audio.transcribe(
        "whisper-1", temp_file)

    # 一時ファイルを削除
    os.unlink(temp_file.name)

    return result


audio_file = "audio/akusairon.mp3"

origin = AudioSegment.from_file(audio_file)
# PyDub handles time in milliseconds
two_minutes = 2 * 60 * 1000

data = []

for i in range(0, len(origin), two_minutes):
    transcript = transcribe(origin[i:i+two_minutes])
    data.append(transcript)

# 文章の結合
combined_text = "\n".join([item["text"] for item in data])

# .txtファイルとして書き出し
with open("docs/output.txt", "w", encoding="utf-8") as f:
    f.write(combined_text)

print("文章をoutput.txtファイルに書き出しました。")
