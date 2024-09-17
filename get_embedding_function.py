from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

def get_embedding_function():
    model_id = 'sentence-transformers/all-MiniLM-L6-v2'
    model_kwargs = {'device': 'cpu'}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs=model_kwargs
    )
    # embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings