import chromadb

def search(query: str, journalist_id: str, chroma_path: str, k=3):
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_collection(name=journalist_id)
    # Use OpenAI embeddings to embed the query
    from rag_pipeline.embedding.openai_embedder import OpenAIEmbedder
    embedder = OpenAIEmbedder()
    query_emb = embedder.embed_text(query)
    results = collection.query(query_embeddings=[query_emb], n_results=k)
    return [doc for doc in results['documents'][0]]