import os

from fastapi import FastAPI

from src.api.routers import generate, tags, transcribe

app = FastAPI(title="HeartMula 歌词转录 API", version="1.0.0")

app.include_router(transcribe.router)
app.include_router(generate.router)
app.include_router(tags.router)


@app.on_event("startup")
async def startup_event() -> None:
    """启动时打印服务信息"""
    port = os.getenv("PORT", "8000")
    print(f"HeartMula 服务已启动: http://localhost:{port}/docs")
