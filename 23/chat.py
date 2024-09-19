import sys
from setup import setup_index

def chat_with_model(query, index, llm):
    query_engine = index.as_query_engine(llm=llm, similarity_top_k=3)
    response = query_engine.query(query)
    return response.response  # Return only the response attribute

if __name__ == "__main__":
    import sys
    from setup import setup_index
    
    if len(sys.argv) < 2:
        print("Usage: python chat.py 'Your question here'")
    else:
        query = sys.argv[1]
        index, llm = setup_index()
        response = chat_with_model(query, index, llm)
        print(response)