import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends

from app.dependencies import get_current_user_dependency
from app.security.roles import ensure_is_admin

router = APIRouter(prefix="/upload", tags=["Upload"])

# Directory where uploaded files will be temporarily stored
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("")
async def upload_document(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user_dependency),
):
    ensure_is_admin(current_user)
    """
    Endpoint to upload documents (PDF, TXT, DOCX) for processing.
    """
    allowed_extensions = {".pdf", ".txt", ".docx", ".doc"}
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{file_ext}'. Allowed formats: {', '.join(allowed_extensions)}",
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}",
        )
    finally:
        file.file.close()

    return {
        "filename": file.filename,
        "file_path": file_path,
        "content_type": file.content_type,
        "message": "File uploaded successfully",
    }
