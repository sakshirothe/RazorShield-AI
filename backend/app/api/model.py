import os
import json
from fastapi import APIRouter, HTTPException
from backend.app.core.config import settings

router = APIRouter(prefix="/api/model", tags=["Model Health"])

@router.get("/metrics")
def get_model_metrics():
    eval_path = settings.EVALUATION_PATH
    meta_path = settings.METADATA_PATH

    if not os.path.exists(eval_path):
        raise HTTPException(
            status_code=404,
            detail="Model evaluation report not found. Please run evaluation first."
        )

    with open(eval_path, "r") as f:
        eval_data = json.load(f)

    meta_data = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            meta_data = json.load(f)

    return {
        "status": "HEALTHY",
        "metadata": meta_data,
        "evaluation": eval_data
    }
