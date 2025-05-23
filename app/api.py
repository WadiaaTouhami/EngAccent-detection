# Force HF Hub to copy instead of symlinking on Windows
import os

os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from .pipeline import AccentDetectionPipeline


class ProcessRequest(BaseModel):
    video_url: HttpUrl


app = FastAPI(
    title="Accent Detection API",
    version="1.0",
    description="AI-powered accent detection from video URLs",
)

# Add CORS middleware for frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pipeline once at startup
print("Initializing Accent Detection Pipeline...")
pipeline = AccentDetectionPipeline()
print("✓ Pipeline ready!")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Accent Detection API is running",
        "status": "healthy",
        "version": "1.0",
    }


@app.post("/process")
async def process_video(req: ProcessRequest):
    """Endpoint to process a video URL and return accent detection results"""
    try:
        result = pipeline.process(str(req.video_url))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check for deployment"""
    return {"status": "healthy"}
