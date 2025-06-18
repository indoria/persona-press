import os
from .embedding.openai_embedder import OpenAIEmbedder
from .chunking.fixed_length import chunk_text
import chromadb

def ingest_corpus(journalist_id, corpus_dir, chroma_path):
    embedder = OpenAIEmbedder()
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection(name=journalist_id)
    for fname in os.listdir(corpus_dir):
        with open(os.path.join(corpus_dir, fname)) as f:
            text = f.read()
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            embedding = embedder.embed_text(chunk)
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    "journalist_id": journalist_id,
                    "embedding_id": f"{journalist_id}_{fname}_{idx}",
                    "chunk_id": idx
                }]
            )