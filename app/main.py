from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes.upload_routes import router as upload_router
from app.core.config import OUTPUT_DIR

app = FastAPI(title="Malware Detection API")


origins = [

    '*'
    ]

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/after_convert", StaticFiles(directory=OUTPUT_DIR) , name="static")

app.include_router(upload_router)

@app.get("/")
def root():
    return {"message": "Malware Detection API is running"}
