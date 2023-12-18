import base64
import os
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import aiofiles

load_dotenv()

app = FastAPI()
origins = [
    "http://localhost:3000",  # Reactの開発サーバーのURLを許可する
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.post("/transcribe/")
async def transcribe_audio(audio: UploadFile = File(...)):
    # 一時的なファイル名を生成
    temp_file = f"temp_{audio.filename}"

    try:
        # save temp file
        async with aiofiles.open(temp_file, 'wb') as out_file:
            content = await audio.read()
            await out_file.write(content)

        # whisperで文字起こし
        with open(temp_file, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return {"transcription": transcript.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 一時ファイルを削除
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Uvicorn でサーバを起動する場合
# uvicorn main:app --reload
