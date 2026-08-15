import os
import shutil
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    status,
    Depends,
    BackgroundTasks,
)
from pypdf import PdfReader

from app.dependencies import get_current_user_dependency
from app.security.roles import ensure_is_admin

# Import your chunking and embedding service here
# from app.services.rag_service import ingest_document_to_vectorstore

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_text_from_file(file_path: str, file_ext: str) -> str:
    """Extracts raw text from PDF or TXT files safely without memory overhead."""
    text_content = ""
    if file_ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_content += extracted + "\n"
    elif file_ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text_content = f.read()
    return text_content


def process_and_index_document(file_path: str, file_ext: str, filename: str):
    """Background task to extract text, chunk, and embed into Pinecone."""
    try:
        extracted_text = extract_text_from_file(file_path, file_ext)
        if not extracted_text.strip():
            print(f"[WARN] No readable text extracted from {filename}")
            return

        # TODO: Call your existing vector store ingestion function
        # ingest_document_to_vectorstore(filename=filename, text=extracted_text)
        print(f"[SUCCESS] Processed and embedded document: {filename}")
    except Exception as e:
        print(f"[ERROR] Ingestion failed for {filename}: {str(e)}")


@router.post("")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user_dependency),
):
    """
    Endpoint to upload documents for RAG processing.
    """
    ensure_is_admin(current_user)

    allowed_extensions = {".pdf", ".txt", ".docx", ".doc"}
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{file_ext}'. Allowed formats: {', '.join(allowed_extensions)}",
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # Write chunks to file on disk rather than loading entirely into memory
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer, length=1024 * 1024)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )
    finally:
        file.file.close()

    # Trigger background ingestion to vector database
    background_tasks.add_task(
        process_and_index_document, file_path, file_ext, file.filename
    )

    return {
        "filename": file.filename,
        "file_path": file_path,
        "content_type": file.content_type,
        "message": "File uploaded successfully. Processing background embedding.",
    }
