import streamlit as st
import os
from dotenv import load_dotenv

from modules.restaurant_fetcher import search_restaurant, RestaurantInfo
from modules.image_analyzer import analyze_food_photos
from modules.blog_generator import generate_blog_post, WRITING_STYLES

load_dotenv()

st.set_page_config(
    page_title="네이버 블로그 맛집 글 생성기",
    page_icon="🍽️",
    layout="wide",
)

st.title("🍽️ 네이버 블로그 맛집 글 자동 생성기")
st.caption("식당명 + 사진만 넣으면 SEO/GEO 최적화된 블로그 글이 완성됩니다")

# ── API 키 확인 ──────────────────────────────────────────────────────────────
gemini_key = os.getenv("GEMINI_API_KEY", "")

if not gemini_key:
    with st.expander("⚙️ Gemini API 키 설정", expanded=True):
        gemini_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            key="gemini_key_input",
            placeholder="AIzaSy...",
        )
        st.caption("무료 키 발급: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) (신용카드 불필요)")
    if not gemini_key:
        st.stop()

# 네이버/카카오 키 로드
naver_id = os.getenv("NAVER_CLIENT_ID", "")
naver_secret = os.getenv("NAVER_CLIENT_SECRET", "")
kakao_key = os.getenv("KAKAO_REST_API_KEY", "")
if naver_id:
    os.environ["NAVER_CLIENT_ID"] = naver_id
if naver_secret:
    os.environ["NAVER_CLIENT_SECRET"] = naver_secret
if kakao_key:
    os.environ["KAKAO_REST_API_KEY"] = kakao_key

# ── 1단계: 식당 검색 ─────────────────────────────────────────────────────────
st.header("1️⃣ 식당 검색")

col1, col2 = st.columns([3, 1])
with col1:
    restaurant_name_input = st.text_input(
        "식당명을 입력하세요",
        placeholder="예: 진미평양냉면 마포점",
    )
with col2:
    search_btn = st.button("🔍 검색", use_container_width=True)

selected_restaurant = None

if search_btn and restaurant_name_input:
    with st.spinner("식당 정보를 검색 중입니다..."):
        results = search_restaurant(restaurant_name_input)

    if results:
        st.success(f"{len(results)}개의 결과를 찾았습니다.")
        options = {
            f"{r.name} — {r.address} ({r.source.upper()})": r
            for r in results
        }
        st.session_state["search_results"] = options
    else:
        st.warning("검색 결과가 없습니다. 아래 직접 입력 옵션을 사용해주세요.")
        st.session_state["search_results"] = {}

if "search_results" in st.session_state and st.session_state["search_results"]:
    options = st.session_state["search_results"]
    chosen_label = st.radio("검색 결과", list(options.keys()), label_visibility="collapsed")
    if chosen_label:
        selected_restaurant = options[chosen_label]
        r = selected_restaurant
        with st.expander("📍 선택된 식당 정보", expanded=True):
            cols = st.columns(2)
            cols[0].markdown(f"**이름**: {r.name}")
            cols[0].markdown(f"**카테고리**: {r.category or '—'}")
            cols[0].markdown(f"**주소**: {r.address or '—'}")
            cols[1].markdown(f"**전화**: {r.phone or '—'}")
            if r.map_url:
                cols[1].markdown(f"**지도**: [바로가기]({r.map_url})")

with st.expander("✏️ 식당 정보 직접 입력 (검색 결과가 없을 때)"):
    manual_name = st.text_input("식당명", key="manual_name")
    manual_category = st.text_input("카테고리 (예: 한식 > 냉면)", key="manual_cat")
    manual_address = st.text_input("주소", key="manual_addr")
    manual_phone = st.text_input("전화번호", key="manual_phone")
    manual_map = st.text_input("지도 URL (선택)", key="manual_map")

    if manual_name:
        selected_restaurant = RestaurantInfo(
            name=manual_name,
            category=manual_category,
            address=manual_address,
            phone=manual_phone,
            description="",
            map_url=manual_map,
            source="manual",
            raw_data={},
        )
        st.success(f"'{manual_name}' 정보가 설정되었습니다.")

st.divider()

# ── 2단계: 사진 업로드 ────────────────────────────────────────────────────────
st.header("2️⃣ 사진 업로드")
uploaded_files = st.file_uploader(
    "방문 시 촬영한 사진을 업로드하세요 (최대 6장, 선택 사항)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
)

if uploaded_files:
    cols = st.columns(min(len(uploaded_files), 3))
    for i, f in enumerate(uploaded_files[:6]):
        cols[i % 3].image(f, caption=f.name, use_container_width=True)

st.divider()

# ── 3단계: 문체 선택 ──────────────────────────────────────────────────────────
st.header("3️⃣ 원하는 문체 선택")

style_choice = st.radio(
    "문체 스타일",
    list(WRITING_STYLES.keys()),
    horizontal=True,
)

custom_style = ""
if style_choice == "직접 입력":
    custom_style = st.text_area(
        "원하는 문체를 설명해주세요",
        placeholder="예: 30대 직장인 여성이 동료에게 추천하는 느낌으로, 가성비와 웨이팅 정보를 중요하게 다뤄주세요",
        height=100,
    )

final_style = custom_style if style_choice == "직접 입력" else WRITING_STYLES[style_choice]

st.divider()

# ── 4단계: 글 생성 ────────────────────────────────────────────────────────────
st.header("4️⃣ 블로그 글 생성")

generate_btn = st.button(
    "✨ 블로그 글 생성하기",
    type="primary",
    use_container_width=True,
    disabled=(selected_restaurant is None),
)

if selected_restaurant is None:
    st.caption("식당을 먼저 검색하거나 직접 입력해주세요.")

if generate_btn and selected_restaurant:
    photo_analysis = ""

    if uploaded_files:
        with st.spinner("📸 사진을 분석 중입니다..."):
            image_bytes_list = [f.read() for f in uploaded_files[:6]]
            try:
                photo_analysis = analyze_food_photos(image_bytes_list, gemini_key)
            except Exception as e:
                st.warning(f"사진 분석 중 오류: {e}")

    with st.spinner("✍️ SEO/GEO 최적화 블로그 글을 작성 중입니다... (10~30초 소요)"):
        try:
            blog_content = generate_blog_post(
                restaurant_info=selected_restaurant,
                photo_analysis=photo_analysis,
                writing_style=final_style,
                api_key=gemini_key,
            )
            st.session_state["blog_content"] = blog_content
        except Exception as e:
            st.error(f"글 생성 중 오류: {e}")

if "blog_content" in st.session_state:
    content = st.session_state["blog_content"]

    st.success("✅ 블로그 글이 완성되었습니다!")

    tab1, tab2 = st.tabs(["📄 미리보기", "📋 복사용 텍스트"])

    with tab1:
        st.markdown(content)

    with tab2:
        st.text_area(
            "아래 텍스트를 복사하여 네이버 블로그에 붙여넣으세요",
            value=content,
            height=600,
            key="copy_area",
        )
        st.caption("💡 네이버 블로그 편집기에 일반 텍스트로 붙여넣기 후 서식을 조정하세요.")

    if st.button("🔄 글 다시 생성하기"):
        del st.session_state["blog_content"]
        st.rerun()
