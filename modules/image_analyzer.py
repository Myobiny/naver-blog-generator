from google import genai
from google.genai import types
from PIL import Image
import io


def analyze_food_photos(image_files: list, api_key: str) -> str:
    """음식 사진들을 분석하여 상세한 설명을 반환합니다."""
    if not image_files:
        return ""

    client = genai.Client(api_key=api_key)

    parts = []
    for img_bytes in image_files[:6]:
        img = Image.open(io.BytesIO(img_bytes))
        buf = io.BytesIO()
        fmt = img.format or "JPEG"
        img.save(buf, format=fmt)
        mime = "image/jpeg" if fmt.upper() in ("JPEG", "JPG") else f"image/{fmt.lower()}"
        parts.append(types.Part.from_bytes(data=buf.getvalue(), mime_type=mime))

    parts.append(types.Part.from_text(text=(
        "위 사진들은 맛집 방문 시 촬영한 사진들입니다. 각 사진에서 다음 정보를 한국어로 분석해주세요:\n"
        "1. 음식 종류 및 메뉴명 (추정)\n"
        "2. 음식의 비주얼 특징 (색감, 플레이팅, 신선도, 양 등)\n"
        "3. 분위기 및 인테리어 특징 (해당되는 경우)\n"
        "4. 인상적인 요소나 특별한 점\n"
        "5. 사진 전반적인 분위기 (아늑한, 트렌디한, 캐주얼한 등)\n\n"
        "블로그 글 작성에 활용할 수 있도록 구체적이고 생생하게 묘사해주세요."
    )))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=parts,
    )
    return response.text
