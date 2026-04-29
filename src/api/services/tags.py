"""标签枚举定义"""

from dataclasses import dataclass


@dataclass
class TagItem:
    """标签项"""

    value: str
    display_name: str


# 流派
GENRES_TAGS = [
    TagItem("pop", "流行"),
    TagItem("rock", "摇滚"),
    TagItem("jazz", "爵士"),
    TagItem("classical", "古典"),
    TagItem("electronic", "电子"),
    TagItem("blues", "蓝调"),
    TagItem("country", "乡村"),
    TagItem("metal", "金属"),
    TagItem("funk", "放克"),
    TagItem("reggae", "雷鬼"),
    TagItem("hip-hop", "嘻哈"),
    TagItem("rap", "说唱"),
    TagItem("indie", "独立"),
    TagItem("folk", "民谣"),
    TagItem("soul", "灵魂乐"),
    TagItem("r&b", "节奏布鲁斯"),
    TagItem("latin", "拉丁"),
    TagItem("dance", "舞曲"),
    TagItem("disco", "迪斯科"),
    TagItem("techno", "Techno"),
    TagItem("house", "浩室"),
    TagItem("ambient", "氛围"),
]

# 乐器
INSTRUMENTS_TAGS = [
    TagItem("piano", "钢琴"),
    TagItem("guitar", "吉他"),
    TagItem("bass", "贝斯"),
    TagItem("drum", "鼓"),
    TagItem("violin", "小提琴"),
    TagItem("saxophone", "萨克斯"),
    TagItem("trumpet", "小号"),
    TagItem("flute", "长笛"),
    TagItem("organ", "风琴"),
    TagItem("synthesizer", "合成器"),
    TagItem("acoustic", "原声"),
    TagItem("electric", "电声"),
    TagItem("keyboard", "键盘"),
    TagItem("cello", "大提琴"),
    TagItem("harp", "竖琴"),
    TagItem("banjo", "班卓琴"),
    TagItem("harmonica", "口琴"),
    TagItem("ukulele", "尤克里里"),
    TagItem("accordion", "手风琴"),
    TagItem("clarinet", "单簧管"),
]

# 情绪
MOOD_EMOTION_TAGS = [
    TagItem("happy", "快乐"),
    TagItem("sad", "悲伤"),
    TagItem("romantic", "浪漫"),
    TagItem("energetic", "活力"),
    TagItem("calm", "平静"),
    TagItem("peaceful", "安宁"),
    TagItem("melancholic", "忧郁"),
    TagItem("upbeat", "轻快"),
    TagItem("chill", "放松"),
    TagItem("dark", "暗黑"),
    TagItem("bright", "明亮"),
    TagItem("dreamy", "梦幻"),
    TagItem("aggressive", "激烈"),
    TagItem("gentle", "温柔"),
    TagItem("intense", "强烈"),
    TagItem("relaxing", "舒缓"),
    TagItem("cheerful", "欢快"),
    TagItem("nostalgic", "怀旧"),
    TagItem("dramatic", "戏剧"),
    TagItem("playful", "俏皮"),
]

# 节奏
TEMPO_RHYTHM_TAGS = [
    TagItem("fast", "快"),
    TagItem("slow", "慢"),
    TagItem("medium", "中速"),
    TagItem("upbeat", "快节奏"),
    TagItem("downtempo", "慢节奏"),
    TagItem("steady", "稳健"),
    TagItem("syncopated", "切分"),
    TagItem("groove", "律动"),
    TagItem("driving", "驱动"),
    TagItem("flowing", "流畅"),
    TagItem("bouncy", "弹跳"),
    TagItem("rhythmic", "有节奏"),
]

# 风格
STYLE_ATMOSPHERE_TAGS = [
    TagItem("acoustic", "原声"),
    TagItem("electronic", "电子"),
    TagItem("orchestral", "管弦"),
    TagItem("minimal", "极简"),
    TagItem("ambient", "氛围"),
    TagItem("atmospheric", "大气"),
    TagItem("cinematic", "电影"),
    TagItem("experimental", "实验"),
    TagItem("traditional", "传统"),
    TagItem("modern", "现代"),
    TagItem("vintage", "复古"),
    TagItem("lo-fi", "低保真"),
    TagItem("hi-fi", "高保真"),
    TagItem("raw", "原始"),
    TagItem("polished", "精致"),
    TagItem("live", "现场"),
    TagItem("studio", "录音室"),
]

# 场合
OCCASION_THEME_TAGS = [
    TagItem("wedding", "婚礼"),
    TagItem("party", "派对"),
    TagItem("dance", "舞蹈"),
    TagItem("meditation", "冥想"),
    TagItem("workout", "健身"),
    TagItem("sleep", "睡眠"),
    TagItem("focus", "专注"),
    TagItem("celebration", "庆典"),
    TagItem("romance", "浪漫"),
    TagItem("adventure", "冒险"),
    TagItem("nature", "自然"),
    TagItem("urban", "城市"),
    TagItem("fantasy", "奇幻"),
]

# 人声
VOCAL_TAGS = [
    TagItem("male voice", "男声"),
    TagItem("female voice", "女声"),
    TagItem("choir", "合唱"),
    TagItem("acappella", "无伴奏"),
    TagItem("vocal harmony", "和声"),
    TagItem("rap", "说唱"),
    TagItem("singing", "演唱"),
]


# 所有标签类别映射
TAG_CATEGORIES: dict[str, list[TagItem]] = {
    "Genres": GENRES_TAGS,
    "Instruments": INSTRUMENTS_TAGS,
    "Mood/Emotion": MOOD_EMOTION_TAGS,
    "Tempo/Rhythm": TEMPO_RHYTHM_TAGS,
    "Style/Atmosphere": STYLE_ATMOSPHERE_TAGS,
    "Occasion/Theme": OCCASION_THEME_TAGS,
    "Vocal": VOCAL_TAGS,
}

# 标签类别中文名
TAG_CATEGORY_DISPLAY_NAMES: dict[str, str] = {
    "Genres": "流派",
    "Instruments": "乐器",
    "Mood/Emotion": "情绪",
    "Tempo/Rhythm": "节奏",
    "Style/Atmosphere": "风格",
    "Occasion/Theme": "场合",
    "Vocal": "人声",
}


def get_all_tags() -> dict[str, list[dict]]:
    """获取所有标签，按类别分组（用于 API 响应）"""
    return {
        name: [
            {"value": tag.value, "display_name": tag.display_name} for tag in tag_list
        ]
        for name, tag_list in TAG_CATEGORIES.items()
    }


def validate_selection(selections: dict[str, str]) -> tuple[bool, str | None]:
    """验证标签选择是否合法，支持英文值或中文名"""
    for category, tag_value in selections.items():
        if category not in TAG_CATEGORIES:
            return False, f"未知类别: {category}"
        valid_values = [tag.value for tag in TAG_CATEGORIES[category]]
        valid_display_names = [tag.display_name for tag in TAG_CATEGORIES[category]]
        if tag_value not in valid_values and tag_value not in valid_display_names:
            return False, f"标签 '{tag_value}' 不属于类别 '{category}'"
    return True, None


def normalize_selections(selections: dict[str, str]) -> dict[str, str]:
    """将选择中的中文名转换为英文值"""
    result = {}
    for category, tag_value in selections.items():
        if category not in TAG_CATEGORIES:
            result[category] = tag_value
            continue
        # 如果是中文名，转换为英文值
        for tag in TAG_CATEGORIES[category]:
            if tag_value == tag.display_name:
                result[category] = tag.value
                break
        else:
            result[category] = tag_value
    return result
