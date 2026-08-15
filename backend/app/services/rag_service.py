from typing import Dict, List

from app.ai.embeddings import create_embedding
from app.ai.llm import generate_structured_response
from app.ai.retriever import find_relevant_chunks


def create_ticket_resolution(title: str, description: str) -> Dict[str, str]:
    """Create a grounded ticket enrichment result using RAG."""
    # Combine title and description for higher retrieval quality
    query_text = f"{title} {description}"

    # 1. Generate query embedding
    embedding = create_embedding(query_text)

    # 2. Retrieve top matching chunks from Pinecone
    chunks: List[str] = find_relevant_chunks(embedding, top_k=3) if embedding else []

    # Debug logging (optional)
    print(f"\n[RAG SERVICE] Retrieved {len(chunks)} chunks for query: '{title}'")

    # 3. Pass ticket details and retrieved context to Groq/LLM
    result = generate_structured_response(title, description, chunks)
    return result
