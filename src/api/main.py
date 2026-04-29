import os

from fastapi import FastAPI

from src.api.routers import transcribe

app = FastAPI(title="HeartMula 歌词转录 API", version="1.0.0")

app.include_router(transcribe.router)


@app.on_event("startup")
async def startup_event() -> None:
    """启动时打印服务信息"""
    port = os.getenv("PORT", "8000")
    print(f"HeartMula 歌词转录服务已启动: http://localhost:{port}/docs")
