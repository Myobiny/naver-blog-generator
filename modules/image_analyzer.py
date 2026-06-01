import base64
import anthropic
from PIL import Image
import io


def _encode_image(image_bytes: bytes) -> tuple[str, str]:
    """이미지를 base64로 인코딩하고 미디어 타입을 반환합니다."""
    img = Image.open(io.BytesIO(image_bytes))
    fmt = img.format or "JPEG"
    media_map = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp", "GIF": "image/gif"}
    media_type = media_map.get(fmt.upper(), "image/jpeg")

    buf = io.BytesIO()
    img.save(buf, format=fmt)
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    return encoded, media_type


def analyze_food_photos(image_files: list[bytes], client: anthropic.Anthropic) -> str:
    """음식 사진들을 분석하여 상세한 설명을 반환합니다."""
    if not image_files:
        return ""

    content = []
    for img_bytes in image_files[:6]:  # 최대 6장
        encoded, media_type = _encode_image(img_bytes)
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": encoded,
            },
        })

    content.append({
        "type": "text",
        "text": (
            "위 사진들은 맛집 방문 시 촬영한 사진들입니다. 각 사진에서 다음 정보를 한국어로 분석해주세요:\n"
            "1. 음식 종류 및 메뉴명 (추정)\n"
            "2. 음식의 비주얼 특징 (색감, 플레이팅, 신선도, 양 등)\n"
            "3. 분위기 및 인테리어 특징 (해당되는 경우)\n"
            "4. 인상적인 요소나 특별한 점\n"
            "5. 사진 전반적인 분위기 (아늑한, 트렌디한, 캐주얼한 등)\n\n"
            "블로그 글 작성에 활용할 수 있도록 구체적이고 생생하게 묘사해주세요."
        ),
    })

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": content}],
    )
    return response.content[0].text
