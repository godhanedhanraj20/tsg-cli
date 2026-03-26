from fastapi import APIRouter
from api.schemas.response import APIResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/status")
async def status():
    try:
        # call service layer
        return APIResponse(status="success", data={"logged_in": True})
    except Exception as e:
        return APIResponse(status="error", message=str(e))
