from fastapi import APIRouter, Query
from api.schemas.response import APIResponse
from services.file_service import search_files
from telegram.client import get_client
from utils.config_manager import load_config

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/")
async def list_files(
    query: str = "",
    tag: str = "",
    file_type: str = "",
    page: int = 1
):
    try:
        config = load_config()
        if not config or "api_id" not in config or "api_hash" not in config:
            return APIResponse(status="error", message="Telegram API credentials not configured.")
        client = get_client(config["api_id"], config["api_hash"])
        async with client:
            files = await search_files(
                client=client,
                query=query,
                tag=tag,
                file_type=file_type,
                page=page
            )
            return APIResponse(status="success", data=files)
    except Exception as e:
        return APIResponse(status="error", message=str(e))
