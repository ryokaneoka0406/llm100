# LLM100

## overview / 概要

- This project is for 100 prototypes on LLM/generative AI.
- LLM/生成 AI に関するプロトタイピングを 100 個行うプロジェクトです。

## policy / 方針

- Don't just follow the tutorial, add a little twist
- Use GUI as much as possible, not just the command line
- ただチュートリアルをなぞるだけではなく、ひと工夫入れる
- コマンドラインだけでなく、なるべく GUI を使用する

## projects / プロジェクト一覧

### [23. Fully Local PDF RAG with Gemma2:9b, e5-base-multilingual, and LlamaIndex / 完全ローカルで RAG システム構築](https://youtu.be/0fOak4whIfY)

- I have created a RAG system that runs completely locally using Gemma2:9b, e5-base-multilingual, and LlamaIndex.
- I am using [Cursor](https://www.cursor.com/) from this code. It's crazy crispy and comfortable to write.
- Gemma2:9b、e5-base-multilingual、 LlamaIndex を使って完全にローカルだけで動く RAG システムを作りました。NotebookLM みたいなのデスクトップアプリで作りたいんですよね。
- 今回のコードから [Cursor](https://www.cursor.com/) を利用しています。めちゃくちゃサクサク書けて快適。

### [22. faster-whisper, gemma2, pyttsx3 を使ってオフラインで AI と音声会話/ offline llm coversation](https://youtu.be/NOFeVt8obhs)

- I have created a demo of faster-whisper, gemma2, pyttsx3 fully offline and conversing with LLM by voice. The voice output is very robotic, so it might be better to use the normal text to speech API here.I tried gemma2 for the first time, and I think it is quite smart for local models. I'll do some more research.
- faster-whisper、gemma2、pyttsx3 を完全オフラインで LLM と音声で会話するデモを作りました。音声出力がめちゃくちゃロボットっぽいのでここは普通に Text to speech の API 使った方がいいかも。はじめて gemma2 を試してみましたが、ローカルモデルではかなり頭いい気がする。もうちょっと研究してみよう。

### [21. Twilio で GPT-4o-mini と電話できるようにした / Twilio to be able to call GPT-4o-mini.](https://youtu.be/_X3gcA83D7k)

- I have made it possible to call GPT-4o-mini using Twilio. Next to this, I want to use Text to speech to smooth out the conversation.
- Twilio を使って GPT-4o-mini と電話できるようにしました。この次は Text to speech を使って会話を滑らかにしたい。

### [20. Video frame search app with local&multimodal llms ( llava & multilingual-e5-base ) / ローカルで動く多様な LLM を使った動画フレーム検索アプリ](https://youtu.be/-zIGsKTnYkU)

- It enables video frame search using only locally running models.
- The app breaks down a video into frames, adds captions to them using llava, and then uses multilingual-e5-base for embedding, enabling video frame search. It works offline.
- I tried explain it in English for the first time✌️
- ローカルで動くモデルだけで動画のフレーム検索を実現しています。
- 動画をフレームにし、それに llava でキャプションをつけた後、multilingual-e5-base で embedding、動画のフレーム検索を実現しています。オフラインで動きます。
- 複雑なので英語での説明もしてみました。

### [19. Live caption images with Gemini-1.5-flash / gemini-1.5-flash で画像にライブキャプション](https://youtu.be/t6inXRibb5Y)

- I am fetching images from the browser every few seconds and having Gemini-1.5-flash describe the situation in those images.
- ブラウザで数秒ごとに画像を取得し、その状況を gemini-1.5-flash に説明させています。

### [18. Taking Screenshots and Summarizing Content with GPT-4o / スクリーンショットを撮って GPT-4o で内容を要約する](https://youtu.be/G_eTCKnjmjg)

- This demo showcases an app that lets you take screenshots and get instant summaries using GPT-4o
- このデモでは、スクリーンショットを撮って GPT-4 で即座に要約を得られるアプリを紹介します

### [17. job description Q&A with Claude3 Opus / 職務経歴書をもとにした Q&A を Claude3 を使って生成します](https://youtu.be/tLoBSaYEdMk)

- I created an app that uses Claude3 Opus to generate questions and answers based on a resume.
- 職務経歴書に基づいた質問と答えを Claude3 Opus を使って生成するアプリを作りました。

### [16. Quiz UI generator with GPT JSON mode/ JSON モードを使ってトピックから試験フォームを作る](https://youtu.be/jvMDWgCRHAI)

- Generates a Streamlit UI based on the input topic. An experiment that creates a form based on user input using GPT's JSON mode
- トピックを入れたら Streamlit の UI まで生成します。GPT の JSON モードを利用してユーザー入力を元にしたフォームを生成する実験。

### [15. Next.js + FastAPI でブラウザ録音 & 文字起こし / Browser Recording & Transcription with Next.js + FastAPI](https://youtu.be/oyNMrP8dlQI)

- It's been a while since I've posted! I was getting tired of Streamlit, so I created an app that allows you to record and transcribe directly in your browser using Next.js and FastAPI.
- 久々の投稿です！Streamlit に飽きてきたので Next.js と FastAPI を使ってブラウザで録音、そのまま文字起こしができるアプリを作りました。

### [14. Youtube Summarizer with LangChain / LangChain を使った Youtube 要約システム](https://youtu.be/WzCZrFN6Odo)

- I created a system to summarize YouTube using LangChain. Even long videos are supported.
- LangChain を使って YouTube を要約するシステムを作りました。長時間の動画でも対応しています。

#### Try it

https://ytsummarize.streamlit.app/

### [13. PaLM2 vs GPT-4](https://youtu.be/19dmKB3FwDw)

- This is a demonstration of having PaLM2 and GPT-4, Google's LLMs, consider the output with the same prompt and have GPT-4 decide which result is more appropriate. Perhaps because the judge is GPT-4, there is a slight bias...
- Google の LLM である PaLM2 と GPT-4 に同じプロンプトで出力を考えてもらい、GPT-4 にどちらの結果が適切か判断してもらうデモです。審判が GPT-4 だからか、若干偏りがあるような…

### [12. アイデアがうまくいくか判定してくれるツール/A tool that will give you the probability of success of your idea](https://youtu.be/NEzJrhU6qgE)

- When you submit an idea, this tool will give you a success probability and other ideas after considering the conditions for success and the risk of failure. This is a great tool to use when starting a new project.
- アイデアを投稿すると、成功の条件と失敗のリスクを考えた上で、成功確度と他の案を出してくれるツールです。新しいプロジェクトを始めるときにどうぞ。

#### Try it

https://idea-validator.streamlit.app/

### [11. CSV データを全自動で分析します/Fully automated analysis of CSV data](https://youtu.be/SZaMIx7XS1s)

- After uploading the CSV data and a description of the data, the analysis is fully automated; I used LangChain's SQL Chain and GPT-3.5 16k models. This app was submitted to the Streamlit LLM Hackathon.I have deployed it and you can try it from below.
- CSV データとデータについての説明をアップロードしたら、全自動で分析を行います。LangChain の SQL Chain と GPT-3.5 16k モデルを利用しました。このアプリは Streamlit LLM Hackathon に提出しました。デプロイしたので下から試せます。

#### Try it

https://csv-auto.streamlit.app/

### [10. CSV データアナリスト/CSV Data Analyst](https://youtu.be/DtKxA2OtzxE)

- The one that reads the headers and queries the table according to the questions when you upload the CSV.
- CSV をアップロードしたら、ヘッダーを読み込み、質問に応じてテーブルをクエリしてくれるやつです。

### [9. 日記から要点を抽出、ふさわしい挿絵を作成する / Making illustrations from the diary](https://youtu.be/AC4m5wvUJG0)

- When you put in your diary, it interprets the content and creates a suitable illustration.I used GPT-3.5 16k model & DALL-E.
- 日記を入れると、内容を解釈し、ふさわしい挿絵を作ってくれます。GPT-3.5 16k モデルと DALL-E を使用。

### [8. LangChain も VectorDB も使わず PDF ドキュメントで RAG してみる / RAG with PDF documents without LangChain or VectorDB](https://youtu.be/cTr3TV6M-NI)

- I wanted to understand how it works, so I implemented a RAG that can read a PDF URL and answer questions using only the ada model and GPT-4.
- 仕組みを理解したくて、ada モデルと GPT-4 だけで、PDF の URL を読み込んで質問に回答できる RAG を実装しました。

### [7. ada モデルで Embedding&異常検知 / Anomaly detection with ada model](https://youtu.be/uLXf6kepsmk)

- Embedding the text with ada model → dimensionality reduction → 2D plotting!I think it would be rather easy to make a model to find spam comments.
- ada モデルでテキストを Embedding→ 次元削減 →2D プロットすることで異常なコメントを見つけるよ！これならスパムコメントとか見つけるモデル割と簡単に作れそうな気がするなあ。

### [6. Whisper で文字起こし →LlamaIndex で要約 / Transcribing with Whisper and summarizing with LlamaIndex](https://youtu.be/bkMePaobmFE)

- I transcribed the text with Whisper and then summarized it with LlamaIndex. I have a feeling it returns results that look like that.
- Whisper で文字起こしした後に LlamaIndex で要約しました。それっぽい結果が返っている気はする

### [5. Whisper API で文字起こし + GPT-4 で箇条書きに整形 / Transcribing with Whisper API and formatting with GPT-4](https://youtu.be/gfVfh4rBvNk)

- I had a chat with my wife transcribed. Transcribed by Whisper API → formatted by GPT-4. It also supports sending prompts to Whisper API.
- 妻との雑談を文字起こししてもらった。Whisper API で文字起こし → GPT-4 による整形。さりげなく Whisper API へのプロンプト送信も対応している。

### [4. WhisperAPI で文字起こし（長時間録音対応）/ Transcribing with WhisperAPI (long audio support)](https://youtu.be/x2eYloHJNYM)

- It's a little more than a tutorial, but I have a system in place to split up the recording and transcribe it, even if it gets too long. I will join them together and make them look good after tomorrow.
- チュートリアルに毛が生えた程度だけど、一応録音が長くなっても分割して文字起こしする仕組みは作ってある。結合していい感じにするのは明日以降。

### [3. シチュエーションを投げ込むと英語の例文を生成 →Google Cloud Text to speech で読み上げ / Generating English sentences from situations and reading them out with Google Cloud Text to speech](https://youtu.be/BfPcyW8e3aw)

- Think of an example sentence for a situation → convert to JSON with function calling → convert to speech with Google Cloud Text to speech.
- シチュエーションに応じた例文を考える →function calling で JSON 化 →Google Cloud Text to speech で音声化するというもの。

### [2. OpenAI API の Function Calling を使って画像検索する / Searching images using OpenAI API's Function Calling](https://youtu.be/E0idcyjChPE)

- OpenAI's function calling should be combined with other APIs! So I combined it with image search.
- OpenAI の Function calling は他 API と組み合わせてナンボだろ！ということで画像検索と組み合わせてみた。

### [1. Llama2 をローカルで動かす / Running Llama2 locally](https://youtu.be/llqrpAyzHkY)

- Try "llama-cpp-python".
- 「llama-cpp-python」を試します。

## License

MIT

## copyright

Copyright (c) 2024 ryopenguin
