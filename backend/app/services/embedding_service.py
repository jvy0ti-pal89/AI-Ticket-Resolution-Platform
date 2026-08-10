from app.ai.embeddings import create_embedding


def embed_text(text: str):
    """Return embedding vector for given text (list[float])."""
    return create_embedding(text)
