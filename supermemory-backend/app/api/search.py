from fastapi import APIRouter

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/ping")
async def ping():
    return {"msg": "search ok"}
