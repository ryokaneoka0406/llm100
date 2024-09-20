# Fully Local PDF RAG with Gemma2:9b, E5-base-multilingual, and LlamaIndex

This project implements a Retrieval-Augmented Generation (RAG) system for PDF documents using Gemma2:9b as the language model, e5-base-multilingual for embeddings, and LlamaIndex for document indexing and querying. The entire system runs locally, ensuring privacy and offline functionality.

## Prerequisites

- Python 3.10
- Pipenv
- Ollama (with gemma2:9b model installed)

## Setup

1. Clone this repository

2. Install dependencies using Pipenv:

   ```
   pipenv install
   ```

3. Activate the virtual environment:

   ```
   pipenv shell
   ```

4. Ensure Ollama is installed and the gemma2:9b model is available:
   ```
   ollama pull gemma2:9b
   ```

## Usage

1. Run the Streamlit app:

   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).

3. Follow the on-screen instructions to upload a PDF, process it, and ask questions about its content.

## Project Structure

- `app.py`: Main Streamlit application
- `setup.py`: Configuration for index creation and LLM setup
- `chat.py`: Handles the question-answering functionality

## How It Works

1. The user uploads a PDF file through the Streamlit interface.
2. The PDF is processed and indexed using LlamaIndex and the e5-base-multilingual embedding model.
3. Users can then ask questions about the PDF content.
4. The system uses the Gemma2:9b model (via Ollama) to generate responses based on the relevant parts of the indexed document.

## License

MIT License

Copyright (c) 2024 Ryo Kaneoka
