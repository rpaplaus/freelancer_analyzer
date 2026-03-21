from rag.vector_store import get_vector_store

def search_similar_jobs(query: str, k: int = 5):
    """Semantic search against the vector database."""
    try:
        vector_store = get_vector_store()
    except ValueError:
        return []
        
    results = vector_store.similarity_search_with_relevance_scores(query, k=k)
    
    formatted_results = []
    for doc, score in results:
        formatted_results.append({
            "Semantic Score": round(score, 3),
            "Title": doc.page_content.split('\n')[0].replace("Title: ", ""),
            "Budget Max": doc.metadata.get("budget_max"),
            "URL": doc.metadata.get("url")
        })
        
    return formatted_results
