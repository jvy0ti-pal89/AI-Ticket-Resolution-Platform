from typing import List

from app.ai.vector_store import query_vectors


def find_relevant_chunks(embedding: List[float], top_k: int = 5) -> List[str]:
    """Query Pinecone for the most relevant document chunks."""
    try:
        response = query_vectors(embedding, top_k=top_k)
        matches = []
        if isinstance(response, dict):
            matches = response.get("matches") or []
        else:
            matches = getattr(response, "matches", []) or []

        chunks: List[str] = []
        for match in matches:
            metadata = (
                match.get("metadata")
                if isinstance(match, dict)
                else getattr(match, "metadata", None)
            )
            if metadata:
                chunk_text = metadata.get("chunk_text") or metadata.get("text_preview")
                if chunk_text:
                    chunks.append(chunk_text)
        return chunks
    except Exception:
        return []
