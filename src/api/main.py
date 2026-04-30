import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.api.routers import generate, tags, transcribe

app = FastAPI(title="HeartMula 歌词转录 API", version="1.0.0")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")
# 挂载 example 目录
app.mount("/example", StaticFiles(directory="example"), name="example")


@app.get("/")
async def root() -> FileResponse:
    """返回首页"""
    return FileResponse("static/index.html")


app.include_router(transcribe.router)
app.include_router(generate.router)
app.include_router(tags.router)


@app.on_event("startup")
async def startup_event() -> None:
    """启动时打印服务信息"""
    port = os.getenv("PORT", "8000")
    print(f"HeartMula 服务已启动: http://localhost:{port}/docs")
