from fastapi import FastAPI
from api.routes import auth, files, folders

app = FastAPI(title="TSG-CLI API", version="1.0")

@app.on_event("startup")
async def startup():
    from api.client_manager import get_shared_client
    try:
        await get_shared_client()
    except Exception:
        # Ignore startup failures to allow health check to pass without config
        pass

@app.on_event("shutdown")
async def shutdown():
    from api.client_manager import _client
    if _client and getattr(_client, "is_connected", False):
        try:
            await _client.stop()
        except Exception:
            pass

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(folders.router)
