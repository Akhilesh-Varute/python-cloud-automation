# api_transform.py
from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List
import logging

app = FastAPI(title="API Transformer", version="1.0.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_transform")


class TransformIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    score: float = Field(..., ge=0, le=100)


class TransformOut(BaseModel):
    name_upper: str
    passed: bool
    score: float
    message: Optional[str] = None


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/demo", response_model=List[TransformOut])
async def demo():
    # Simple demo data to show output shape and example responses
    sample = [
        {"name_upper": "SAM", "passed": True, "score": 72, "message": "Congrats"},
        {
            "name_upper": "RIA",
            "passed": False,
            "score": 34,
            "message": "Needs improvement",
        },
    ]
    return sample


@app.post("/transform", response_model=TransformOut)
async def transform(
    payload: TransformIn,
    request: Request,
    threshold: Optional[float] = Query(
        40.0, ge=0, le=100, description="Pass threshold (default 40)"
    ),
):
    """
    POST /transform
    Body: {"name": str, "score": float}
    Query param: ?threshold=50
    """
    # Log request info (client IP + payload)
    client_ip = request.client.host if request.client else "unknown"
    logger.info(
        "Request from %s body=%s threshold=%s", client_ip, payload.json(), threshold
    )

    # Business rule: reject absurdly long names (example custom error)
    if len(payload.name.strip()) > 50:
        raise HTTPException(status_code=400, detail="Name too long (max 50 characters)")

    # Transform logic
    name_upper = payload.name.strip().upper()
    passed = payload.score >= threshold
    message = "Congrats" if passed else "Needs improvement"

    return TransformOut(
        name_upper=name_upper,
        passed=passed,
        score=payload.score,
        message=message,
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning("Validation error: %s", exc)
    # Keep the default 422 semantics but ensure logging
    raise HTTPException(status_code=422, detail=exc.errors())
