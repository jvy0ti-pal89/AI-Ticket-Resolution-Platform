from typing import Dict, List

from app.ai.embeddings import create_embedding
from app.ai.llm import generate_structured_response
from app.ai.retriever import find_relevant_chunks


def create_ticket_resolution(title: str, description: str) -> Dict[str, str]:
    """Create a grounded ticket enrichment result using RAG."""
    text = f"{title}\n{description}"
    embedding = create_embedding(text)
    chunks = find_relevant_chunks(embedding)
    result = generate_structured_response(title, description, chunks)
    return result
