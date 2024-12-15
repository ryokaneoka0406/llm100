# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import pyaudio
import sys
import traceback
import flet as ft
from google import genai

if sys.version_info < (3, 11, 0):
    import taskgroup, exceptiongroup
    asyncio.TaskGroup = taskgroup.TaskGroup
    asyncio.ExceptionGroup = exceptiongroup.ExceptionGroup

FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
CHUNK_SIZE = 512

MODEL = "models/gemini-2.0-flash-exp"

client = genai.Client(
    http_options={'api_version': 'v1alpha'})

CONFIG = {
    "generation_config": {
        "response_modalities": ["TEXT"]
    },
    "system_instruction": {
        "parts": [{
            "text": """
            You are an excellent stenographer.
            Please transcribe exactly what a user says. Ignore filler words etc.
            """
        }]
    }
}

class AudioLoop:
    def __init__(self, page: ft.Page):
        self.audio_out_queue = asyncio.Queue()
        self.session = None
        self.page = page
        self.transcription_text = ft.Text("")

    async def listen_audio(self):
        pya = pyaudio.PyAudio()
        mic_info = pya.get_default_input_device_info()
        stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )
        while True:
            data = await asyncio.to_thread(stream.read, CHUNK_SIZE)
            if self.session:
                self.audio_out_queue.put_nowait(data)
            else:
                break

    async def send_audio(self):
        while True:
            if not self.session:
                break
            chunk = await self.audio_out_queue.get()
            await self.session.send({"data": chunk, "mime_type": "audio/pcm"})

    async def receive_text(self):
        while True:
            if not self.session:
                break
            async for response in self.session.receive():
                server_content = response.server_content
                if server_content is not None:
                    model_turn = server_content.model_turn
                    if model_turn is not None:
                        for part in model_turn.parts:
                            if part.text is not None:
                                self.transcription_text.value += part.text.strip() + "\n"
                                self.page.update()

    async def start_streaming(self):
        async with (
            client.aio.live.connect(model=MODEL, config=CONFIG) as session,
            asyncio.TaskGroup() as tg,
        ):
            self.session = session
            self.listen_task = tg.create_task(self.listen_audio())
            self.send_task = tg.create_task(self.send_audio())
            self.receive_task = tg.create_task(self.receive_text())

            def check_error(task):
                if task.cancelled():
                    return
                if task.exception() is not None:
                    e = task.exception()
                    traceback.print_exception(None, e, e.__traceback__)

            for task in tg._tasks:
                task.add_done_callback(check_error)

    async def stop_streaming(self):
        self.session = None
        if hasattr(self, 'listen_task'):
            self.listen_task.cancel()
        if hasattr(self, 'send_task'):
            self.send_task.cancel()
        if hasattr(self, 'receive_task'):
            self.receive_task.cancel()

        self.transcription_text.value = ""
        self.page.update()

async def main(page: ft.Page):
    page.title = "Gemini Live Transcription"
    audio_loop = AudioLoop(page)

    async def start_button_click(e):
        start_button.disabled = True
        stop_button.disabled = False
        page.update()
        await audio_loop.start_streaming()

    async def stop_button_click(e):
        start_button.disabled = False
        stop_button.disabled = True
        page.update()
        await audio_loop.stop_streaming()

    start_button = ft.ElevatedButton("Start Streaming", on_click=start_button_click)
    stop_button = ft.ElevatedButton("Stop Streaming", on_click=stop_button_click, disabled=True)

    page.add(
        ft.Column([
            start_button,
            stop_button,
            audio_loop.transcription_text,
        ])
    )
    page.update()

ft.app(target=main)