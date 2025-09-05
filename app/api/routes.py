from fastapi import APIRouter

router = APIRouter()

@router.get("/hc")
def healthyCheck():
    return {
        "message" : "test OK"
    }