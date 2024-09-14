import pyaudio
import wave
from faster_whisper import WhisperModel
import ollama
import pyttsx3

# Whisperモデルを初期化
model = WhisperModel("small", device="cpu", compute_type="int8")  # モデルサイズは必要に応じて変更

# PyAudio設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisperは16kHzが推奨
CHUNK = 1024
RECORD_SECONDS = 3  # 音声の録音時間（秒）
WAVE_OUTPUT_FILENAME = "output.wav"

def record_audio(filename, record_seconds):
    audio = pyaudio.PyAudio()

    # 録音開始
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Listening...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("done")

    # 録音を停止
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # WAVファイルとして保存
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename):
    segments, _ = model.transcribe(
        filename,
        vad_filter=True,
        without_timestamps=True
    )
    print("transcription:")
    transcription = ''
    for segment in segments:
        print(segment.text)
        transcription += segment.text
    return transcription

def text_to_speech(text):
    # pyttsx3のエンジンを初期化
    engine = pyttsx3.init()

    # 音声合成のために入力テキストをセット
    engine.say(text)

    # 音声合成を実行
    engine.runAndWait()

def main():
    while True:
        user_input = input("Press Enter to start conversation, type 'exit' to end:")
        if user_input.lower() == 'exit':
            break

        # 録音と文字起こしの実行
        record_audio(WAVE_OUTPUT_FILENAME, RECORD_SECONDS)
        transcription = transcribe_audio(WAVE_OUTPUT_FILENAME)

        # LLMに文字起こししたテキストを手渡し、レスポンスを取得
        print("Sending to LLM...")
        stream = ollama.chat(
            model='gemma2:9b',
            messages=[{'role': 'user', 'content': f""""
                      Please respond briefly to the following statement.
                       {transcription}
                        Please do not use pictograms, as your remarks will be output to speech."""}],
            stream=True,
        )

        response_text = ''
        print("Response from LLM:")
        for chunk in stream:
            content = chunk['message']['content']
            print(content, end='', flush=True)
            response_text += content

        print("\n")

        # レスポンスを音声出力
        text_to_speech(response_text)

if __name__ == "__main__":
    main()