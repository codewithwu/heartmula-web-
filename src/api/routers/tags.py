from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    TagCategory,
    TagItem,
    TagOptionsResponse,
    TagSelectionRequest,
    TagSelectionResponse,
)
from src.api.services.tags import (
    TAG_CATEGORY_DISPLAY_NAMES,
    get_all_tags,
    normalize_selections,
    validate_selection,
)

router = APIRouter(prefix="/api/v1", tags=["标签"])


@router.get("/tags", response_model=TagOptionsResponse)
async def get_tag_options() -> TagOptionsResponse:
    """获取所有标签选项（按类别）"""
    all_tags = get_all_tags()
    categories = [
        TagCategory(
            name=name,
            display_name=TAG_CATEGORY_DISPLAY_NAMES.get(name, name),
            tags=[
                TagItem(
                    value=t["value"], name=t["value"], display_name=t["display_name"]
                )
                for t in tag_list
            ],
        )
        for name, tag_list in all_tags.items()
    ]
    return TagOptionsResponse(categories=categories)


@router.post("/tags/select", response_model=TagSelectionResponse)
async def select_tags(request: TagSelectionRequest) -> TagSelectionResponse:
    """用户选择标签，返回逗号分隔的标签字符串"""
    is_valid, error_msg = validate_selection(request.selections)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # 将中文名转换为英文值
    normalized = normalize_selections(request.selections)
    all_tags = list(normalized.values())
    return TagSelectionResponse(tags=",".join(all_tags))
