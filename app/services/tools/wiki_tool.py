import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from langchain.tools import tool

ef = ONNXMiniLM_L6_V2(preferred_providers=["CoreMLExecutionProvider"])

chroma_client = chromadb.PersistentClient(path="./db")
collection = chroma_client.get_or_create_collection(name="articles", embedding_function=ef)


@tool
def search_pages_vector(query: str):
    """Search the vector database and return multiple relevant wiki pages.
    Args:
        query: User question or search phrase.
    Returns:
        List of content from matching articles
    """
    if not query.strip():

        return {"error": "Query cannot be empty"}
    try:
        result = collection.query(
            query_texts=query,
            n_results=10,
        )
        return result["documents"][0]
    except Exception as e:
        return {"error": f"Vector search failed: {e}"}
