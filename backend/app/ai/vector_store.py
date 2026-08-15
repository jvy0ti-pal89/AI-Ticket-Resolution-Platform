from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from app.config import settings

_pc_client = None


def _get_pinecone_client() -> Pinecone:
    global _pc_client

    if _pc_client is None:
        api_key = getattr(settings, "pinecone_api_key", None)

        if not api_key:
            raise RuntimeError(
                "Pinecone API key is missing."
            )

        _pc_client = Pinecone(api_key=api_key)

    return _pc_client


def _get_index(index_name: str, dimension: int = 384):
    pc = _get_pinecone_client()

    existing_indexes = [idx.name for idx in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=getattr(settings, "pinecone_cloud", "aws"),
                region=getattr(settings, "pinecone_region", "us-east-1"),
            ),
        )

    return pc.Index(index_name)


def upsert_document_vectors(
    document_id: int,
    filename: str,
    chunks: List[str],
    embeddings: List[List[float]],
):
    """Upsert document chunks and embeddings into Pinecone."""

    if not embeddings:
        return

    index_name = (
        getattr(settings, "pinecone_index_name", None)
        or "ai-ticket-platform"
    )

    index = _get_index(
        index_name,
        dimension=len(embeddings[0]),
    )

    to_upsert = []

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        vector_id = f"{document_id}_{i}"

        metadata: Dict[str, Any] = {
            "document_id": document_id,
            "filename": filename,
            "chunk_index": i,
            "text_preview": chunk[:250],
            "chunk_text": chunk,
        }

        to_upsert.append((vector_id, emb, metadata))

    batch_size = 100

    for i in range(0, len(to_upsert), batch_size):
        batch = to_upsert[i:i + batch_size]
        index.upsert(vectors=batch)


def query_vectors(
    embedding: List[float],
    top_k: int = 5,
):
    """Query Pinecone for the most relevant document chunks."""

    index_name = (
        getattr(settings, "pinecone_index_name", None)
        or "ai-ticket-platform"
    )

    index = _get_index(
        index_name,
        dimension=len(embedding),
    )

    return index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True,
    )