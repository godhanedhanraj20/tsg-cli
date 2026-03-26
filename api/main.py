from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.routes import auth, files, folders

@asynccontextmanager
async def lifespan(app: FastAPI):
    from api.client_manager import get_shared_client
    try:
        await get_shared_client()
    except Exception:
        # Ignore startup failures to allow health check to pass without config
        pass

    yield

    from api.client_manager import _client
    if _client and getattr(_client, "is_connected", False):
        try:
            await _client.stop()
        except Exception:
            pass

app = FastAPI(title="TSG-CLI API", version="1.0", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(folders.router)
