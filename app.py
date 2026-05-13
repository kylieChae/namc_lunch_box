import streamlit as st
import random
import time

# ─────────────────────────────────────────
# 🍽️ 음식점 목록 (여기에 추가/수정하세요!)
# ─────────────────────────────────────────
RESTAURANTS = [
    {"name": "새문순대국", "emoji": "🫕"},
    {"name": "고모네순대국", "emoji": "🍶"},
    {"name": "명문손칼국수", "emoji": "🍜"},
    {"name": "맘스터치", "emoji": "🍔"},
    {"name": "명인강메밀 푸른초장", "emoji": "🌿"},
    {"name": "1킬로치킨", "emoji": "🍗"},
    {"name": "곰소바돈까스", "emoji": "🍱"},
    {"name": "물뛴다", "emoji": "💧"},
    {"name": "르샤브샤브", "emoji": "🍲"},
    {"name": "메가폭탄김치찜", "emoji": "💣"},
    {"name": "국수나무", "emoji": "🌳"},
    {"name": "놀부부대찌개", "emoji": "🥘"},
    {"name": "세양원", "emoji": "🏮"},
    {"name": "오가삼계탕", "emoji": "🐔"},
    {"name": "온담", "emoji": "🔥"},
    {"name": "충정상회", "emoji": "🏪"},
    {"name": "버거킹", "emoji": "🍔"},
    {"name": "날아라분식", "emoji": "✈️"},
    {"name": "상아국시", "emoji": "🍝"},
    {"name": "권가네", "emoji": "👨‍🍳"},
    {"name": "돌된장", "emoji": "🪨"},
    {"name": "롯데리아", "emoji": "🍔"},
    {"name": "서브웨이", "emoji": "🍔"},
    {"name": "점심한식뷔페", "emoji": "🍽️"},
    {"name": "봄날의정원", "emoji": "🌸"},
    {"name": "모범떡볶이", "emoji": "🍢"},
    {"name": "백암순대국", "emoji": "🍶"}
]


LOADING_MESSAGES = [
    "신중하게 고르는 중...",
    "운명의 음식점을 찾는 중...",
    "칼퇴 기원 중...",
    "메뉴 셔플 중 🔀",
]

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="N신정 점메추",
    page_icon="🍽️",
    layout="centered",
)

# ─────────────────────────────────────────
# 커스텀 CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@700&family=Noto+Sans+KR:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.main { background-color: #FAFAF8; }

.title-wrap {
    text-align: center;
    margin-bottom: 2rem;
}

.app-title {
    font-family: 'Gaegu', cursive;
    font-size: 3rem;
    font-weight: 700;
    color: #1a1a1a;
    margin: 0;
    line-height: 1.1;
}

.app-subtitle {
    font-size: 0.95rem;
    color: #888;
    margin-top: 0.4rem;
}

.result-box {
    background: white;
    border: 1.5px solid #E8E5DF;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin: 1.5rem 0;
    min-height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    box-shadow: 0 2px 16px rgba(0,0,0,0.04);
}

.result-emoji {
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
    animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) both;
}

.result-name {
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a1a;
    animation: popIn 0.4s 0.08s cubic-bezier(0.175, 0.885, 0.32, 1.275) both;
}

.placeholder-text {
    font-size: 1rem;
    color: #bbb;
}

@keyframes popIn {
    from { transform: scale(0.5); opacity: 0; }
    to   { transform: scale(1);   opacity: 1; }
}

.tag-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 1rem;
}

.tag {
    background: #F3F0EB;
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.82rem;
    color: #666;
}

/* Streamlit 버튼 오버라이드 */
div.stButton {
    text-align: center;
}

div.stButton > button {
    background: #1a1a1a !important;
    color: white !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.75rem 2.5rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    transition: opacity 0.15s, transform 0.15s !important;
    letter-spacing: -0.3px;
}

div.stButton > button:hover {
    opacity: 0.85 !important;
    border: none !important;
}

footer, #MainMenu, header {visibility: hidden !important;}
[data-testid="stToolbar"] {display: none !important;}
div[data-testid="stBottom"] {display: none !important;}
            
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 앱 UI
# ─────────────────────────────────────────
st.markdown("""
<div class="title-wrap">
    <p class="app-title">🍽️ 오늘 뭐 먹지?</p>
    <p class="app-subtitle">버튼을 누르면 오늘의 점심을 골라드려요</p>
</div>
""", unsafe_allow_html=True)

# 결과 표시 영역
result_placeholder = st.empty()

# 초기 상태
if "picked" not in st.session_state:
    st.session_state.picked = None

if st.session_state.picked is None:
    result_placeholder.markdown("""
    <div class="result-box">
        <p class="placeholder-text">👆 버튼을 눌러서 오늘의 점심을 골라보세요!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    r = st.session_state.picked
    result_placeholder.markdown(f"""
    <div class="result-box">
        <div class="result-emoji">{r['emoji']}</div>
        <div class="result-name">{r['name']}</div>
    </div>
    """, unsafe_allow_html=True)

# 버튼
_, col, _ = st.columns([3, 4, 3])
with col:
    clicked = st.button("🎲 오늘의 점심 고르기", use_container_width=True)
if clicked:
    # 로딩 애니메이션
    with result_placeholder:
        for msg in LOADING_MESSAGES:
            result_placeholder.markdown(f"""
            <div class="result-box">
                <div style="font-size:2.5rem; margin-bottom:0.5rem">⏳</div>
                <p style="color:#888; font-size:0.95rem">{msg}</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.35)

    # 결과 선택
    pick = random.choice(RESTAURANTS)
    st.session_state.picked = pick
    st.rerun()

# 음식점 목록 태그
st.markdown('<div class="tag-wrap">', unsafe_allow_html=True)
tags_html = "".join([f'<span class="tag">{r["emoji"]} {r["name"]}</span>' for r in RESTAURANTS])
st.markdown(f'{tags_html}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
#st.caption("음식점을 추가/수정하려면 `app.py`의 RESTAURANTS 목록을 편집하세요 ✏️")
st.caption("음식점을 추가/수정하려면 IT개발실 숮과장에게 문의하세요. ✏️")
