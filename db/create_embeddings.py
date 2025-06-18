import os
import chromadb
from rag_pipeline.embedding.openai_embedder import OpenAIEmbedder

def create_embeddings(journalist_id, corpus_dir, chroma_path):
    embedder = OpenAIEmbedder()
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection(name=journalist_id)
    for fname in os.listdir(corpus_dir):
        with open(os.path.join(corpus_dir, fname)) as f:
            text = f.read()
        # For demo, treat each file as one chunk
        embedding = embedder.embed_text(text)
        collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[{"journalist_id": journalist_id, "filename": fname}]
        )

if __name__ == "__main__":
    base = "./db/journalists/corpus"
    chroma_path = "./db/chromadb"
    for journalist_id in os.listdir(base):
        corpus_dir = os.path.join(base, journalist_id)
        create_embeddings(journalist_id, corpus_dir, chroma_path)