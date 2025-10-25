import magic
import os
import uuid
from fastapi import HTTPException
from app.core.config import ALLOWED_IMAGE_TYPES, MAX_FILE_SIZE_MB, IMAGES_DIR

class FileService:
    """handles validation and saving of uploaded files."""

    def __init__(self):
        self.max_size = MAX_FILE_SIZE_MB * 1024 * 1024

    async def validate_and_save(self, upload_file) -> dict:
        """validate mime type and size, then save file and return info."""
        # peek to check type
        file_content = await upload_file.read(1024)
        file_type = magic.from_buffer(file_content, mime=True)

        if file_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file_type}")

        # check file size
        await upload_file.seek(0)
        content = await upload_file.read()
        size_bytes = len(content)
        if size_bytes > self.max_size:
            raise HTTPException(status_code=400, detail="File too large")

        # create unique filename
        unique_id = str(uuid.uuid4())
        ext = upload_file.filename.split(".")[-1]
        filename = f"{unique_id}.{ext}"
        save_path = os.path.join(IMAGES_DIR, filename)

        # save file
        with open(save_path, "wb") as f:
            f.write(content)

        return {
            "path": save_path,
            "filename": filename,
            "base_name": unique_id,
            "content_type": file_type,
            "size_kb": size_bytes / 1024,
        }
