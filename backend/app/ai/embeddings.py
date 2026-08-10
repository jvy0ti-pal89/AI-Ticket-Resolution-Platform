from typing import List
from sentence_transformers import SentenceTransformer

# Load model once at import time
_MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str) -> List[float]:
    """Create a dense embedding for the provided text using SentenceTransformer.

    Returns a list[float] representing the vector.
    """
    # SentenceTransformer returns a numpy array
    vec = _MODEL.encode(text, show_progress_bar=False)
    return vec.tolist()
