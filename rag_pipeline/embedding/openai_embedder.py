import openai
from .base import BaseEmbedder

class OpenAIEmbedder(BaseEmbedder):
    def embed_text(self, text: str):
        response = openai.Embedding.create(
            input=[text], model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']