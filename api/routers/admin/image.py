import shutil
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from schemas import admin

router = APIRouter(prefix="/image", tags=["Admin | Image"])

UPLOAD_DIR = Path("static/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post(path="/upload")
async def upload(
    file: Annotated[UploadFile, File(description="Image file")],
) -> admin.ImageResponseSchema:
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not an image",
        )

    file_extension = Path(file.filename).suffix if file.filename else ".jpg"
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    try:
        with (UPLOAD_DIR / unique_filename).open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save image: {str(e)}",
        ) from e
    finally:
        file.file.close()

    return admin.ImageResponseSchema(url=f"/static/images/{unique_filename}")
