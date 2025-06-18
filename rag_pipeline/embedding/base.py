class BaseEmbedder:
    def embed_text(self, text: str):
        raise NotImplementedError("Implement in subclass")