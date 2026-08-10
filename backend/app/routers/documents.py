import os
import re
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document
from app.models.user import User
from app.security.jwt import get_current_user
from app.services.parser_service import parse_document
from app.services.embedding_service import embed_text
from app.ai.chunking import chunk_text
from app.ai.vector_store import upsert_document_vectors

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _sanitize_filename(filename: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", os.path.basename(filename))


@router.get("/")
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all uploaded documents."""
    return db.query(Document).order_by(Document.created_at.desc()).all()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload PDF or TXT files manually via Frontend."""
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only .pdf and .txt files are supported.",
        )

    safe_name = _sanitize_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    doc = Document(
        filename=safe_name,
        filepath=file_path,
        status="uploaded",
        uploaded_by_id=current_user.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    try:
        parsed_text = parse_document(file_path)
        doc.parsed_text = parsed_text
        doc.status = "parsed"
        db.commit()
        db.refresh(doc)

        # chunk -> embeddings -> upsert
        chunks = chunk_text(parsed_text)
        embeddings = [embed_text(c) for c in chunks]
        upsert_document_vectors(doc.id, doc.filename, chunks, embeddings)
    except Exception as exc:
        # mark failed and return error
        doc.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document processing failed: {str(exc)}",
        )

    return {"message": "File uploaded successfully", "document": doc}
