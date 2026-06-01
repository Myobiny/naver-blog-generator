# 🍽️ 네이버 블로그 맛집 글 자동 생성기

식당명과 사진만 넣으면 **SEO/GEO 최적화된 네이버 블로그 맛집 글**이 자동으로 완성됩니다.

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red) ![Claude](https://img.shields.io/badge/Claude-Sonnet_4.6-orange)

---

## 주요 기능

- **식당 정보 자동 수집** — 네이버 지도 · 카카오맵 API로 주소, 전화번호, 카테고리 자동 조회
- **사진 AI 분석** — Claude Vision이 음식 비주얼, 분위기, 플레이팅을 생생하게 묘사
- **SEO/GEO 최적화 글 생성** — 2026년 검색 전략 기반의 상위노출 요소 자동 포함
- **문체 선택** — 친근한 / 감성 에세이 / 정보 중심 / MZ 트렌디 / 직접 입력
- **원클릭 복사** — 생성된 글을 바로 네이버 블로그에 붙여넣기

---

## 생성 글에 포함되는 SEO/GEO 요소

| 요소 | 설명 |
|------|------|
| 핵심 키워드 | 식당명 + 지역명 + 음식 종류 자연스럽게 반복 |
| 롱테일 키워드 | 혼밥·데이트·가족 등 상황별 키워드 |
| FAQ 섹션 | AI 검색엔진 발췌용 Q&A 구조 |
| 시맨틱 SEO | 가격대·주차·웨이팅 등 관련 개념어 포함 |
| E-E-A-T | 직접 방문 경험 강조로 신뢰도 향상 |
| 해시태그 | 네이버 검색 최적화 해시태그 15-20개 |

---

## 사용 방법

1. 식당명 검색 또는 직접 입력
2. 방문 사진 업로드 (최대 6장)
3. 원하는 문체 선택
4. **글 생성하기** 클릭 → 30~60초 후 완성
5. 생성된 글 복사 → 네이버 블로그에 붙여넣기

---

## 로컬 실행

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. API 키 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어 키 입력:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
NAVER_CLIENT_ID=...          # 선택 (없으면 직접 입력 사용)
NAVER_CLIENT_SECRET=...      # 선택
KAKAO_REST_API_KEY=...       # 선택
```

### 3. 앱 실행

```bash
python3 -m streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

---

## Streamlit Cloud 배포

1. [share.streamlit.io](https://share.streamlit.io) → GitHub 로그인
2. **New app** → 이 리포지토리 선택, `app.py` 지정
3. **Advanced settings → Secrets** 에 아래 입력:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."

# 선택 사항
NAVER_CLIENT_ID = ""
NAVER_CLIENT_SECRET = ""
KAKAO_REST_API_KEY = ""
```

4. **Deploy** 클릭

---

## 필요한 API 키

| API | 발급처 | 필수 여부 | 비용 |
|-----|--------|----------|------|
| Anthropic (Claude) | [console.anthropic.com](https://console.anthropic.com) | **필수** | 글 1개당 약 15~45원 |
| 네이버 검색 API | [developers.naver.com](https://developers.naver.com) | 선택 | 무료 |
| 카카오 Local API | [developers.kakao.com](https://developers.kakao.com) | 선택 | 무료 |

> 네이버/카카오 API 키 없이도 **직접 입력** 옵션으로 식당 정보를 수동 입력하면 글 생성이 가능합니다.

---

## 프로젝트 구조

```
├── app.py                        # 메인 Streamlit 앱
├── requirements.txt
├── .env.example                  # API 키 템플릿
├── .streamlit/
│   └── config.toml               # 테마 설정
└── modules/
    ├── restaurant_fetcher.py     # 네이버/카카오 식당 검색
    ├── image_analyzer.py         # Claude Vision 사진 분석
    └── blog_generator.py         # SEO/GEO 블로그 글 생성
```
