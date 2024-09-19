from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.file import PDFReader

def setup_index(file_path):
    llm = Ollama(model="gemma2:9b", request_timeout=30.0)
    embed_model = HuggingFaceEmbedding(
        model_name="intfloat/multilingual-e5-base",
        cache_folder="embed_model"
    )

    pdf_reader = PDFReader()
    documents = pdf_reader.load_data(file_path)
 
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    return index, llm

if __name__ == "__main__":
    # Specify the path to your test file
    test_file_path = "path/to/your/test/file.pdf"
    index, llm = setup_index(test_file_path)
    print("Index and LLM setup complete.")