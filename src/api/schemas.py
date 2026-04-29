from pydantic import BaseModel


class TranscribeResponse(BaseModel):
    """转录响应模型"""

    lyrics: str


class TranscribeRequest(BaseModel):
    """转录请求模型"""

    role: str = "default"
    llm_provider: str = "longcat"


class TagItem(BaseModel):
    """标签项模型"""

    value: str
    name: str  # 英文名
    display_name: str  # 中文名


class TagCategory(BaseModel):
    """标签类别模型"""

    name: str
    display_name: str
    tags: list[TagItem]


class TagOptionsResponse(BaseModel):
    """标签选项响应"""

    categories: list[TagCategory]


class TagSelectionRequest(BaseModel):
    """用户标签选择请求"""

    selections: dict[str, str]  # category -> tag


class TagSelectionResponse(BaseModel):
    """用户标签选择响应"""

    tags: str  # 逗号分隔的标签字符串，用于生成接口


class GenerationRequest(BaseModel):
    """音乐生成请求模型"""

    lyrics: str
    tags: str


class GenerationResponse(BaseModel):
    """音乐生成响应模型"""

    audio_path: str


class LyricsCheckRequest(BaseModel):
    """歌词格式校验请求模型"""

    lyrics: str
    role: str = "generate"
    llm_provider: str = "longcat"


class LyricsCheckResponse(BaseModel):
    """歌词格式校验响应模型"""

    is_valid: bool
