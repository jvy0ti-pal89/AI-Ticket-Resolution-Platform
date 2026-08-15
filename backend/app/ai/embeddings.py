from typing import List
from sentence_transformers import SentenceTransformer

_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str) -> List[float]:
    """Create a 384-dimensional embedding."""
    if not text or not text.strip():
        return []

    vec = _MODEL.encode(text, show_progress_bar=False)
    return vec.tolist()