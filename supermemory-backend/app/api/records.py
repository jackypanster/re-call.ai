from fastapi import APIRouter

router = APIRouter(prefix="/records", tags=["records"])

@router.get("/ping")
async def ping():
    return {"msg": "records ok"}
