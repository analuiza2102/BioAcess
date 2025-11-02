from fastapi import APIRouter

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/ping")
def ping():
    return {"pong": True}
