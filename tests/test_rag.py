from rag_pipeline.index import search

def test_search_returns_results():
    # Requires pre-indexed data
    results = search("test query", "journalist1", "./db/chromadb")
    assert isinstance(results, list)