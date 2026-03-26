import os
import tempfile
import aiofiles
from fastapi import APIRouter, Query, UploadFile, File, BackgroundTasks
from typing import List, Optional
from api.schemas.response import APIResponse
from api.schemas.file import TagRequest
from services.file_service import search_files, upload_file, download_file, delete_file
from utils.metadata_manager import add_tag, remove_tag
from telegram.client import get_client
from utils.config_manager import load_config
from utils.errors import TSGError

router = APIRouter(prefix="/files", tags=["files"])

def get_configured_client():
    config = load_config()
    if not config or "api_id" not in config or "api_hash" not in config:
        raise TSGError("Telegram API credentials not configured.")
    return get_client(config["api_id"], config["api_hash"])

@router.get("/")
async def list_files(
    query: str = "",
    tag: str = "",
    file_type: str = "",
    page: int = 1
):
    try:
        client = get_configured_client()
        async with client:
            files = await search_files(
                client=client,
                query=query,
                tag=tag,
                file_type=file_type,
                page=page
            )
            return APIResponse(status="success", data=files)
    except TSGError as e:
        return APIResponse(status="error", message=str(e))
    except Exception:
        return APIResponse(status="error", message="Internal server error")

@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    path: str = Query("/")
):
    temp_path = None
    try:
        # Save uploaded file temporarily
        fd, temp_path = tempfile.mkstemp(prefix="tsg_", suffix=f"_{file.filename}")
        os.close(fd)

        async with aiofiles.open(temp_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # 1MB chunks
                await out_file.write(content)

        client = get_configured_client()
        async with client:
            metadata = await upload_file(
                client=client,
                file_path=temp_path,
                log_cb=None,
                dest_path=path
            )

            return APIResponse(status="success", data={
                "id": metadata["id"],
                "name": metadata["name"],
                "size": metadata["size"],
                "path": metadata.get("path", path)
            })

    except TSGError as e:
        return APIResponse(status="error", message=str(e))
    except Exception:
        return APIResponse(status="error", message="Internal server error")
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

def cleanup_temp_dir(dir_path: str):
    if dir_path and os.path.exists(dir_path):
        import shutil
        shutil.rmtree(dir_path, ignore_errors=True)

@router.get("/download/{file_id}")
async def download(file_id: int, background_tasks: BackgroundTasks):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp(prefix="tsg_downloads_")

        client = get_configured_client()
        async with client:
            file_path = await download_file(
                client=client,
                file_id=file_id,
                output_dir=temp_dir,
                log_cb=None
            )

            if not file_path or not os.path.exists(file_path):
                raise TSGError("File not found or download failed")

            filename = os.path.basename(file_path)

            def iterfile():
                try:
                    with open(file_path, mode="rb") as file_like:
                        yield from file_like
                finally:
                    pass

            background_tasks.add_task(cleanup_temp_dir, temp_dir)

            from fastapi.responses import StreamingResponse
            return StreamingResponse(
                iterfile(),
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

    except TSGError as e:
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        return APIResponse(status="error", message=str(e))
    except Exception:
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        return APIResponse(status="error", message="Internal server error")

@router.delete("/")
async def delete_files_batch(ids: str = Query(...)):
    try:
        file_ids = [int(id.strip()) for id in ids.split(",")]
        client = get_configured_client()
        success = 0
        async with client:
            for file_id in file_ids:
                try:
                    await delete_file(client=client, file_id=file_id)
                    success += 1
                except TSGError:
                    pass
            return APIResponse(status="success", data={"deleted": success})
    except TSGError as e:
        return APIResponse(status="error", message=str(e))
    except Exception:
        return APIResponse(status="error", message="Internal server error")

@router.delete("/{file_id}")
async def delete_file_endpoint(file_id: int):
    try:
        client = get_configured_client()
        async with client:
            await delete_file(client=client, file_id=file_id)
            return APIResponse(status="success", data={"deleted": 1})
    except TSGError as e:
        return APIResponse(status="error", message=str(e))
    except Exception:
        return APIResponse(status="error", message="Internal server error")

@router.post("/tag")
async def tag_files(request: TagRequest):
    try:
        success = 0
        for file_id in request.file_ids:
            try:
                if request.action == "add":
                    add_tag(str(file_id), request.tag)
                    success += 1
                elif request.action == "remove":
                    remove_tag(str(file_id), request.tag)
                    success += 1
                else:
                    return APIResponse(status="error", message="Invalid action. Use 'add' or 'remove'.")
            except Exception:
                pass
        return APIResponse(status="success", data={"tagged": success})
    except TSGError as e:
        return APIResponse(status="error", message=str(e))
    except Exception:
        return APIResponse(status="error", message="Internal server error")
