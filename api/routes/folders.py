from fastapi import APIRouter
from api.schemas.response import APIResponse
from utils.path_utils import normalize_path
from utils.metadata_manager import load_metadata, save_metadata

router = APIRouter(prefix="/folders", tags=["folders"])

@router.get("/")
async def list_folder(path: str = "/"):
    try:
        path = normalize_path(path)
        metadata_dict = load_metadata()
        metadata = list(metadata_dict.values())

        files = [f for f in metadata if f.get("path", "/").startswith(path)]

        folders = set()
        for f in files:
            sub = f["path"][len(path):].split("/")[0]
            if sub:
                folders.add(sub + "/")

        return APIResponse(
            status="success",
            data={
                "folders": sorted(list(folders)),
                "files": files
            }
        )
    except Exception as e:
        return APIResponse(status="error", message=str(e))

@router.post("/mkdir")
async def mkdir(path: str):
    try:
        path = normalize_path(path)
        return APIResponse(status="success", message=f"Folder ready: {path}")
    except Exception as e:
        return APIResponse(status="error", message=str(e))

@router.post("/move")
async def move(file_ids: list[int], path: str):
    try:
        path = normalize_path(path)
        metadata_dict = load_metadata()
        success = 0

        for f_id in file_ids:
            if str(f_id) in metadata_dict:
                metadata_dict[str(f_id)]["path"] = path
                success += 1

        save_metadata(metadata_dict)

        return APIResponse(
            status="success",
            data={"moved": success}
        )
    except Exception as e:
        return APIResponse(status="error", message=str(e))
