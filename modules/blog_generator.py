from google import genai
from .restaurant_fetcher import RestaurantInfo


WRITING_STYLES = {
    "친근하고 솔직한": "친한 친구에게 맛집을 소개하듯 친근하고 솔직하게, 이모티콘 적절히 사용",
    "감성적인 에세이": "감성적이고 문학적인 문체로, 분위기와 감정을 풍부하게 묘사",
    "정보 중심 리뷰": "객관적이고 체계적으로 정보를 전달하는 전문 리뷰어 스타일",
    "MZ 트렌디": "MZ세대 감성으로 짧고 임팩트 있는 문장, 유행어 적절히 포함",
    "직접 입력": "",
}


def _build_restaurant_context(info: RestaurantInfo) -> str:
    parts = [f"- 식당명: {info.name}"]
    if info.category:
        parts.append(f"- 카테고리: {info.category}")
    if info.address:
        parts.append(f"- 주소: {info.address}")
    if info.phone:
        parts.append(f"- 전화번호: {info.phone}")
    if info.map_url:
        parts.append(f"- 지도 링크: {info.map_url}")
    return "\n".join(parts)


def generate_blog_post(
    restaurant_info: RestaurantInfo,
    photo_analysis: str,
    writing_style: str,
    api_key: str,
) -> str:
    client = genai.Client(api_key=api_key)

    restaurant_ctx = _build_restaurant_context(restaurant_info)
    address_parts = restaurant_info.address.split() if restaurant_info.address else []
    location_keywords = " ".join(address_parts[:3]) if address_parts else "맛집"

    prompt = f"""당신은 2026년 현재 네이버 블로그 SEO/GEO 최적화 전문가이자 맛집 블로거입니다.

## 식당 기본 정보
{restaurant_ctx}

## 사진 분석 결과
{photo_analysis if photo_analysis else "사진 없음"}

## 요청 문체 스타일
{writing_style}

## 작성 조건

### SEO/GEO 최적화 (2026년 기준)
- **핵심 키워드**: 식당명, 지역명, 음식 종류를 자연스럽게 반복 삽입 (키워드 밀도 2-3%)
- **롱테일 키워드**: "{location_keywords} 맛집", "{restaurant_info.category} 맛집 추천", "혼밥/데이트/가족 맛집" 등 상황별 키워드 포함
- **GEO(Generative Engine Optimization)**: AI 검색엔진이 발췌하기 좋은 명확한 Q&A 형식 섹션 포함
- **시맨틱 SEO**: 관련 개념어(분위기, 가격대, 주차, 웨이팅 등) 자연스럽게 포함
- **E-E-A-T**: 직접 방문 경험을 강조하여 신뢰도 높임

### 블로그 구조 (필수 포함)
1. **제목**: 클릭을 유도하는 핵심 키워드 포함 제목 (25자 내외)
2. **도입부**: 공감을 이끄는 방문 동기나 상황 묘사 (2-3문장)
3. **식당 기본 정보**: 위치, 영업시간(알면), 주차, 예약 여부
4. **메뉴 및 음식 리뷰**: 사진 분석 기반 생생한 음식 묘사 (메인 섹션)
5. **분위기/인테리어**: 공간감과 감성 묘사
6. **총평 및 추천 포인트**: 어떤 상황에 추천하는지 명시
7. **FAQ 섹션**: AI 검색 발췌용 Q&A 3-4개 (예: Q. 주차 가능한가요? A. ...)
8. **해시태그**: 네이버 검색 최적화 해시태그 15-20개

### 금지 사항
- 과장되거나 허위 사실 금지
- 모든 문장이 긍정적일 필요 없음 (단점도 솔직하게)

지금 바로 완성된 블로그 포스팅 전문을 작성해주세요. 마크다운 형식으로 작성하고, 실제 네이버 블로그에 바로 붙여넣을 수 있는 수준으로 완성도 높게 작성해주세요."""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text
