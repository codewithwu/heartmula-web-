"""测试标签 API"""

from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_get_tag_options_returns_chinese_and_english():
    """测试获取标签选项接口返回中英文类别和标签"""
    response = client.get("/api/v1/tags")
    assert response.status_code == 200

    data = response.json()
    assert "categories" in data
    categories = data["categories"]

    # 验证有 7 个类别
    assert len(categories) == 7

    # 验证每个类别都有中英文名称
    for category in categories:
        assert "name" in category
        assert "display_name" in category
        assert "tags" in category
        # 类别名称不应为空
        assert category["name"]
        assert category["display_name"]

        # 验证每个标签都有中英文
        for tag in category["tags"]:
            assert "value" in tag
            assert "name" in tag  # 英文名
            assert "display_name" in tag  # 中文名
            assert tag["name"]  # 英文名不应为空
            assert tag["display_name"]  # 中文名不应为空


def test_get_tag_options_genres_have_both_names():
    """测试 Genres 类别包含正确的英文和中文标签"""
    response = client.get("/api/v1/tags")
    data = response.json()

    genres_category = next(
        (c for c in data["categories"] if c["name"] == "Genres"), None
    )
    assert genres_category is not None
    assert genres_category["display_name"] == "流派"

    # 验证 pop 标签
    pop_tag = next((t for t in genres_category["tags"] if t["value"] == "pop"), None)
    assert pop_tag is not None
    assert pop_tag["name"] == "pop"
    assert pop_tag["display_name"] == "流行"


def test_get_tag_options_vocal_have_both_names():
    """测试 Vocal 类别包含正确的英文和中文标签"""
    response = client.get("/api/v1/tags")
    data = response.json()

    vocal_category = next((c for c in data["categories"] if c["name"] == "Vocal"), None)
    assert vocal_category is not None
    assert vocal_category["display_name"] == "人声"

    # 验证 male voice 标签
    male_tag = next(
        (t for t in vocal_category["tags"] if t["value"] == "male voice"), None
    )
    assert male_tag is not None
    assert male_tag["name"] == "male voice"
    assert male_tag["display_name"] == "男声"


def test_select_tags_with_chinese_names():
    """测试使用中文名选择标签也能返回正确的英文值"""
    response = client.post(
        "/api/v1/tags/select",
        json={"selections": {"Genres": "流行", "Mood/Emotion": "快乐"}},
    )
    assert response.status_code == 200
    data = response.json()
    # 应该返回英文值，而非中文
    assert "pop" in data["tags"] or "happy" in data["tags"]


def test_select_tags_with_english_names():
    """测试使用英文名选择标签"""
    response = client.post(
        "/api/v1/tags/select",
        json={"selections": {"Genres": "pop", "Mood/Emotion": "happy"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == "pop,happy"
