# HeartMula

🎵 AI 音乐智能创作平台 - 基于 HeartMuLa 开源模型，通过歌词或标签即可创作专属音乐作品。

![HeartMula 首页](https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/ccv2%2F2026-04-30%2FMiniMax-M2.7%2F2033371718692643804%2F5c2b0cb17bd9d7d19425b55ed7f3125be2c2a99f1ee060dec6cd7defcc00d2fc..png?Expires=1777603917&OSSAccessKeyId=LTAI5tGLnRTkBjLuYPjNcKQ8&Signature=%2FBSe2HTcKORMIzToFvGuiWtQr0Q%3D)

## 功能特性

- **🎤 音频转歌词** - 上传音频文件，AI 自动识别并提取歌词内容
- **🎼 音乐生成** - 输入歌词或标签，AI 创作专属音乐作品
- **🎧 成品欣赏** - 体验 AI 创作的精彩音乐作品

## 技术栈

- **后端**: FastAPI + Python
- **前端**: 原生 HTML/CSS/JavaScript
- **AI 模型**: HeartMuLa 开源模型

## 项目结构

```
.
├── src/                    # 后端源代码
│   ├── api/                # API 路由
│   │   ├── main.py         # FastAPI 入口
│   │   └── routers/       # 各功能路由
│   ├── agents/             # AI Agent
│   └── utils/              # 工具函数
├── static/                 # 前端静态文件
│   ├── index.html          # 首页
│   ├── lyrics.html         # 音频转歌词页面
│   ├── generate.html       # 音乐生成页面
│   └── showcase.html       # 成品欣赏页面
├── example/                # 示例文件
│   ├── lyrics.txt          # 示例歌词
│   └── output.mp3          # 示例音乐
└── tests/                  # 测试文件
```

## 快速开始

### 环境要求

- Python 3.10+
- uv 包管理器

### 安装依赖

```bash
source .venv/bin/activate
uv sync
```

### 启动服务

```bash
uv run uvicorn src.api.main:app --host 0.0.0.0 --port 5000
```

服务启动后访问 http://localhost:5000/

## API 接口

### 音频转歌词

```
POST /api/transcribe
```

上传音频文件，获取歌词内容。

### 音乐生成

```
POST /api/generate
```

提交歌词和标签，生成音乐文件。

### 歌词格式校验

```
POST /api/validate-lyrics
```

校验歌词格式是否正确。

## 页面说明

| 页面 | 路径 | 说明 |
|------|------|------|
| 首页 | `/` | 功能入口 |
| 音频转歌词 | `/static/lyrics.html` | 上传音频提取歌词 |
| 音乐生成 | `/static/generate.html` | 输入歌词生成音乐 |
| 成品欣赏 | `/static/showcase.html` | 体验示例作品 |

## License

MIT