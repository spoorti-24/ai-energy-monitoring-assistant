from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health Check Endpoint")
def get_health():
    """
    Basic application health check.
    Returns:
        dict: {"status": "ok"}
    """
    return {"status": "ok"}
