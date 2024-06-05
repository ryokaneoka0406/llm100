# README

This guide will help you set up and run a Streamlit application that processes a video to extract frames, generate captions and embeddings, and then allows users to search for specific scenes based on a query.

## Prerequisites

- Python 3.10

## steps

1. Install dependencies using pipenv:

```sh
pipenv install
```

And then, run `pipenv shell`.

2. Pull llava

```sh
ollama pull llava
```

3. Download the embedding-e5-base model:

run `download_model.py`

```sh
python download_model.py
```

4. Run streamlit app

```sh
streamlit run app.py
```

5. Upload a movie you like & query scenes

However long movies may take so long hours to process, I recommend the one that is a few minute.
