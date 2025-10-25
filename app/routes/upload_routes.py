from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os

from app.services.file_service import FileService
from app.services.image_service import BinaryVisualizer
from app.services.model_service import MalwareDetectionModel

router = APIRouter(prefix="/upload-image", tags=["File Upload"])

file_service = FileService()
visualizer = BinaryVisualizer()
model_service = MalwareDetectionModel()


@router.post("/")
async def upload_and_analyze(file: UploadFile = File(...)):
    """
    upload a file, validate it, convert it to binary visualization,
    classify with ML model, and return results in the same format
    as the original code.
    """
    try:
        # step 1: Validate and save uploaded file
        save_info = await file_service.validate_and_save(file)
        saved_path = save_info["path"]
        file_type = save_info["content_type"]
        file_size = save_info["size_kb"]
        filename = file.filename
        base_name = save_info["base_name"]

        # step 2: generate visualization image
        converted_path = visualizer.generate_visualization(saved_path, base_name)
        saved_as = os.path.basename(converted_path)

        # step 3: predict using model
        result = model_service.predict_image(converted_path)

        # step 4: build response 
        return JSONResponse(
            status_code=200,
            content={
                "prediction": str(result["prediction"]),
                "predicted_class_name": result["predicted_class_name"],
                "filename": filename,
                "saved_as": saved_as,
                "path": saved_path,
                "content_type": file_type,
                "size": f"{file_size:.2f} KB",
                "message": "Image uploaded successfully",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
