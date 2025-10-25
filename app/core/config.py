from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

print("BASE_DIR",BASE_DIR)

IMAGES_DIR = BASE_DIR / "images"
OUTPUT_DIR = BASE_DIR / "after_convert"

MAP_SIZE = 256
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"]
MAX_FILE_SIZE_MB = 5
MODEL_PATH = BASE_DIR / "models" / "model.h5"

# ensure directories exist
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
