import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "RazorShield AI"
    APP_VERSION: str = "1.0.0"
    TAGLINE: str = "Cost-Sensitive AI Risk Manager for RTO & Return Abuse"
    BUILDATHON_TRACK: str = "Razorpay AI Buildathon — AI Risk Manager"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/razorshield.db")

    LOW_RISK_THRESHOLD: int = int(os.getenv("LOW_RISK_THRESHOLD", 30))
    MEDIUM_RISK_THRESHOLD: int = int(os.getenv("MEDIUM_RISK_THRESHOLD", 70))

    DEFAULT_AVG_RTO_LOSS: float = float(os.getenv("DEFAULT_AVG_RTO_LOSS", 2400.0))
    DEFAULT_VERIFICATION_COST: float = float(os.getenv("DEFAULT_VERIFICATION_COST", 25.0))
    DEFAULT_MANUAL_REVIEW_COST: float = float(os.getenv("DEFAULT_MANUAL_REVIEW_COST", 65.0))
    DEFAULT_FALSE_POSITIVE_COST: float = float(os.getenv("DEFAULT_FALSE_POSITIVE_COST", 220.0))
    DEFAULT_FALSE_NEGATIVE_COST: float = float(os.getenv("DEFAULT_FALSE_NEGATIVE_COST", 2400.0))

    MODEL_PATH: str = os.getenv("MODEL_PATH", "ml/models/model.pkl")
    EVALUATION_PATH: str = os.getenv("EVALUATION_PATH", "ml/models/evaluation.json")
    METADATA_PATH: str = os.getenv("METADATA_PATH", "ml/models/metadata.json")

    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]

settings = Settings()
