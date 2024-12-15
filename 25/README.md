# Gemini Live Transcription App

This application is a real-time transcription app using the Gemini model, based on code published by Google.
[Google Gemini Live API Starter](https://github.com/google-gemini/cookbook/blob/main/gemini-2/live_api_starter.py)

## Overview

- Real-time text conversion from microphone input
- High-accuracy transcription using Gemini API
- Simple GUI interface using Flet

## Requirements

- Python 3.10
- Python packages:
  - google-cloud-aiplatform
  - google-generativeai
  - pyaudio
  - flet
  - taskgroup
  - exceptiongroup

## Setup

1. Clone the repository

```
git clone [repository-url]
```

2. Install dependencies

```
pipenv install
```

3. Configure environment

- Create a project in Google Cloud Platform
- Enable Gemini API
- Obtain and properly configure API key

## Usage

1. Launch the application

```
python app.py
```

2. When the GUI window opens, click "Start Streaming" to begin recording
3. Click "Stop Streaming" to end recording

## License

This project is based on code provided by Google LLC and is licensed under the Apache License 2.0.

```
Copyright 2023 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Disclaimer

- This application is intended for educational and research purposes
- Use of Google Cloud Platform APIs is subject to separate terms of service
- Please verify appropriate licensing for commercial use

## Acknowledgments

This project was developed based on code and Gemini API provided by Google LLC.
