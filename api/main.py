from fastapi import FastAPI
from api.routes import auth, files, folders

app = FastAPI(title="TSG-CLI API", version="1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(folders.router)
