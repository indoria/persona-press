import re

def chunk_text(text, max_sentences=5):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunks.append(" ".join(sentences[i:i+max_sentences]))
    return chunks