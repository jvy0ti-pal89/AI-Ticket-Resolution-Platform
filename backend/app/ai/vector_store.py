from typing import List, Dict, Any
from app.config import settings
import pinecone


def _init_pinecone():
    if hasattr(_init_pinecone, "initted") and _init_pinecone.initted:
        return
    api_key = settings.pinecone_api_key
    env = settings.pinecone_environment
    host = settings.pinecone_host
    if api_key and env:
        pinecone.init(api_key=api_key, environment=env)
    elif api_key and host:
        pinecone.init(api_key=api_key, host=host)
    else:
        raise RuntimeError("Pinecone API key or host not configured in settings")
    _init_pinecone.initted = True


def _get_index(index_name: str, dimension: int = 384):
    _init_pinecone()
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=dimension, metric="cosine")
    return pinecone.Index(index_name)


def upsert_document_vectors(
    document_id: int, filename: str, chunks: List[str], embeddings: List[List[float]]
):
    """Upsert document chunks and embeddings into Pinecone with metadata.

    Each vector id will be: "{document_id}_{chunk_idx}"
    Metadata includes: document_id, filename, chunk_index, text_preview
    """
    index_name = settings.pinecone_index_name or "ai-ticket-platform"
    index = _get_index(index_name, dimension=len(embeddings[0]) if embeddings else 384)

    to_upsert = []
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        vid = f"{document_id}_{i}"
        metadata: Dict[str, Any] = {
            "document_id": document_id,
            "filename": filename,
            "chunk_index": i,
            "text_preview": chunk[:250],
            "chunk_text": chunk,
        }
        to_upsert.append((vid, emb, metadata))

    # upsert in batches
    batch_size = 100
    for i in range(0, len(to_upsert), batch_size):
        batch = to_upsert[i : i + batch_size]
        index.upsert(vectors=batch)


def query_vectors(embedding: List[float], top_k: int = 5):
    index_name = settings.pinecone_index_name or "ai-ticket-platform"
    index = _get_index(index_name, dimension=len(embedding))
    res = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return res
