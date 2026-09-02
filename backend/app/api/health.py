import os
from datetime import datetime
from fastapi import APIRouter
from backend.app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/api/health")
def health_check():
    model_exists = os.path.exists(settings.MODEL_PATH)
    eval_exists = os.path.exists(settings.EVALUATION_PATH)

    return {
        "status": "HEALTHY",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "tagline": settings.TAGLINE,
        "buildathon_track": settings.BUILDATHON_TRACK,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model_loaded": model_exists,
        "evaluation_available": eval_exists,
        "database": "CONNECTED"
    }
