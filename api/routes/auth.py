from fastapi import APIRouter, Depends
from api.schemas.response import APIResponse
from api.dependencies import verify_token, rate_limit

router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(verify_token), Depends(rate_limit)])

@router.get("/status")
async def status():
    try:
        # call service layer
        return APIResponse(status="success", data={"logged_in": True})
    except Exception as e:
        return APIResponse(status="error", message=str(e))
