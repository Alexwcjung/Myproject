import streamlit as st
from urllib.parse import quote
import requests
import hashlib
import re
import html

# =====================================================
# 자동차과 실무 영어
# 탭 순서: 정밀기계 → 용접 → 자동차수리 → 전기·전자 → 복습 희망
# =====================================================

st.set_page_config(
    page_title="자동차과 실무 영어",
    page_icon="🚗",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown(
    """
    <style>
    .main-title {
        font-size: 44px;
        font-weight: 1000;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .sub-title {
        font-size: 17px;
        color: #475569;
        margin-bottom: 24px;
        font-weight: 750;
    }

    .hero-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #eff6ff 45%, #fef3c7 100%);
        border: 1.5px solid #bfdbfe;
        border-radius: 28px;
        padding: 28px 30px;
        margin-bottom: 28px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }

    .hero-title {
        font-size: 30px;
        font-weight: 1000;
        color: #0f172a;
        margin-bottom: 10px;
    }

    .hero-text {
        font-size: 16px;
        color: #334155;
        line-height: 1.8;
        font-weight: 750;
    }

    .theme-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 55%, #7c3aed 100%);
        color: white;
        padding: 30px 34px;
        border-radius: 30px;
        margin-bottom: 22px;
        box-shadow: 0 8px 20px rgba(37,99,235,0.22);
    }

    .theme-title {
        font-size: 38px;
        font-weight: 1000;
        margin-bottom: 6px;
        line-height: 1.2;
    }

    .theme-desc {
        font-size: 18px;
        opacity: 0.96;
        font-weight: 850;
    }

    .cassette-box {
        background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 52%, #fff7ed 100%);
        border: 1.5px solid #bfdbfe;
        border-radius: 28px;
        padding: 28px 30px;
        margin: 22px 0;
        box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    }

    .cassette-title {
        font-size: 34px;
        font-weight: 1000;
        color: #0f172a;
        line-height: 1.25;
        letter-spacing: -0.5px;
    }

    .word-card {
        background: white;
        border-radius: 18px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border: 1px solid #dbeafe;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }

    .word-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .word-number {
        min-width: 38px;
        font-size: 13px;
        font-weight: 900;
        color: #1d4ed8;
        background: #dbeafe;
        border-radius: 999px;
        padding: 5px 9px;
        text-align: center;
    }

    .word-text {
        min-width: 200px;
        font-size: 24px;
        font-weight: 1000;
        color: #111827;
    }

    .meaning-text {
        font-size: 18px;
        font-weight: 850;
        color: #374151;
        margin-left: 8px;
    }

    .emoji-text {
        font-size: 25px;
        line-height: 1;
        text-align: center;
        padding-top: 2px;
    }

    .dialogue-box {
        background: #fefce8;
        border: 1.5px solid #fde68a;
        border-radius: 24px;
        padding: 20px 22px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }

    .dialogue-title {
        font-size: 17px;
        font-weight: 1000;
        color: #854d0e;
        margin-bottom: 14px;
    }

    .dialogue-line {
        font-size: 18px;
        font-weight: 1000;
        color: #111827;
        margin-top: 10px;
    }

    .dialogue-meaning {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 5px;
        font-weight: 750;
    }

    .expression-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 16px 18px;
        margin-bottom: 12px;
    }

    .expression-en {
        font-size: 22px;
        font-weight: 1000;
        color: #0f172a;
        margin-bottom: 5px;
    }

    .expression-ko {
        font-size: 16px;
        font-weight: 750;
        color: #475569;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 1000;
        border: 1px solid #bfdbfe;
        padding: 0.9rem 1.2rem;
        min-height: 62px;
        font-size: 21px;
        box-shadow: 0 6px 16px rgba(37,99,235,0.12);
    }

    .stButton > button:hover {
        border-color: #2563eb;
        color: #2563eb;
    }

    div[data-testid="stTabs"] button[role="tab"] {
        min-height: 58px !important;
        padding: 10px 16px !important;
        border-radius: 18px 18px 0 0 !important;
    }

    div[data-testid="stTabs"] button[role="tab"] p {
        font-size: 20px !important;
        font-weight: 1000 !important;
        line-height: 1.3 !important;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #dbeafe, #e0f2fe, #fef3c7) !important;
        border-radius: 18px 18px 0 0 !important;
    }

    @media (max-width: 520px) {
        .main-title { font-size: 34px !important; }
        .theme-title { font-size: 30px !important; }
        .theme-desc { font-size: 15px !important; }
        .cassette-title { font-size: 28px !important; }
        .word-text { font-size: 20px !important; min-width: 120px !important; }
        .meaning-text { font-size: 16px !important; }
        div[data-testid="stTabs"] button[role="tab"] p { font-size: 16px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 제목
# =========================
st.markdown("<div class='main-title'>🚗 자동차과 실무 영어</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>정밀기계 · 용접 · 자동차수리 · 전기전자 현장에서 필요한 영어 단어와 표현을 듣고 익힙니다.</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🔧 자동차과 학생을 위한 현장 중심 영어</div>
        <div class="hero-text">
            자동차 관련 전공 수업과 현장 실습에서 자주 만나는 단어를
            <b>정밀기계, 용접, 자동차수리, 전기·전자</b> 순서로 정리했습니다.
            각 탭에서 전체 듣기, 단어별 듣기, 복습 희망 체크를 할 수 있습니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# TTS
# =========================
def make_google_tts_url(text, lang="en"):
    clean_text = str(text).strip() or "Hello"
    encoded = quote(clean_text)
    return f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={encoded}"


@st.cache_data(show_spinner=False)
def get_tts_mp3_bytes(text, lang="en"):
    clean_text = str(text).strip() or "Hello"
    url = make_google_tts_url(clean_text, lang=lang)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://translate.google.com/",
    }
    response = requests.get(url, headers=headers, timeout=12)
    response.raise_for_status()
    audio_bytes = response.content
    if not audio_bytes or len(audio_bytes) < 500:
        raise ValueError("음성 파일이 비어 있습니다.")
    return audio_bytes


def direct_audio_player(text, show_link=True):
    text = str(text).strip()
    if not text:
        return
    try:
        audio_bytes = get_tts_mp3_bytes(text, lang="en")
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error("음성 파일을 만들지 못했습니다.")
        st.caption(f"오류 내용: {e}")
        if show_link:
            st.link_button("🔊 새 창에서 듣기", make_google_tts_url(text, lang="en"), use_container_width=True)


def play_audio_block(text, label="🔊 듣기", key=None):
    text = str(text).strip()
    if not text:
        return
    if key is None:
        key = "audio_" + hashlib.md5((label + "::" + text).encode("utf-8")).hexdigest()

    if st.button(label, key=key, use_container_width=True):
        direct_audio_player(text)


def remove_speaker_label(sentence):
    return re.sub(r"^[A-Z]:\s*", "", sentence).strip()


def make_dialogue_tts_text(dialogue):
    return " ".join([remove_speaker_label(item["en"]) for item in dialogue])


def get_word_emoji(word):
    emoji_map = {
        "lathe": "⚙️", "milling machine": "⚙️", "caliper": "📏", "micrometer": "📐",
        "tolerance": "🎯", "welding": "🔥", "arc welding": "⚡", "welding mask": "🥽",
        "spark": "✨", "engine": "⚙️", "brake": "🛑", "battery": "🔋", "sensor": "📡",
        "circuit": "🔌", "wire": "〰️", "fuse": "🔲", "voltage": "⚡", "current": "⚡",
        "diagnostic scanner": "🔍", "oil": "🛢️", "tire": "🛞", "wrench": "🔧",
    }
    return emoji_map.get(word, "🚗")


# =========================
# 복습 희망
# =========================
if "unknown_words" not in st.session_state:
    st.session_state.unknown_words = []

if "unknown_word_info" not in st.session_state:
    st.session_state.unknown_word_info = {}


def make_review_id(theme_name, word):
    return f"{theme_name}||{word}"


def add_unknown_word(word, meaning, theme_name):
    review_id = make_review_id(theme_name, word)
    if review_id not in st.session_state.unknown_words:
        st.session_state.unknown_words.append(review_id)
    st.session_state.unknown_word_info[review_id] = {
        "word": word,
        "meaning": meaning,
        "theme": theme_name,
    }


def remove_unknown_word(review_id):
    if review_id in st.session_state.unknown_words:
        st.session_state.unknown_words.remove(review_id)
    if review_id in st.session_state.unknown_word_info:
        del st.session_state.unknown_word_info[review_id]


def clear_review_checkbox_keys():
    for key in [key for key in list(st.session_state.keys()) if "_unknown_" in str(key)]:
        del st.session_state[key]


# =========================
# 단어 자료
# =========================
word_themes = {
    "⚙️ 정밀기계": [
        {"word": "precision machine", "meaning": "정밀 기계"},
        {"word": "lathe", "meaning": "선반"},
        {"word": "milling machine", "meaning": "밀링 머신"},
        {"word": "drilling machine", "meaning": "드릴링 머신"},
        {"word": "grinder", "meaning": "연삭기"},
        {"word": "CNC machine", "meaning": "CNC 기계"},
        {"word": "cutting tool", "meaning": "절삭 공구"},
        {"word": "workpiece", "meaning": "가공물"},
        {"word": "chuck", "meaning": "척, 고정 장치"},
        {"word": "spindle", "meaning": "주축"},
        {"word": "feed rate", "meaning": "이송 속도"},
        {"word": "cutting speed", "meaning": "절삭 속도"},
        {"word": "surface finish", "meaning": "표면 거칠기, 표면 마감"},
        {"word": "tolerance", "meaning": "공차"},
        {"word": "dimension", "meaning": "치수"},
        {"word": "diameter", "meaning": "직경"},
        {"word": "depth", "meaning": "깊이"},
        {"word": "thread", "meaning": "나사산"},
        {"word": "groove", "meaning": "홈"},
        {"word": "burr", "meaning": "버, 날카로운 찌꺼기"},
        {"word": "deburring", "meaning": "버 제거"},
        {"word": "caliper", "meaning": "버니어 캘리퍼스"},
        {"word": "micrometer", "meaning": "마이크로미터"},
        {"word": "gauge", "meaning": "게이지"},
        {"word": "blueprint", "meaning": "도면"},
        {"word": "measure", "meaning": "측정하다"},
        {"word": "machine", "meaning": "가공하다"},
        {"word": "adjust", "meaning": "조정하다"},
        {"word": "align", "meaning": "정렬하다"},
        {"word": "inspect", "meaning": "검사하다"},
    ],
    "🔥 용접": [
        {"word": "welding", "meaning": "용접"},
        {"word": "welder", "meaning": "용접공, 용접기"},
        {"word": "arc welding", "meaning": "아크 용접"},
        {"word": "gas welding", "meaning": "가스 용접"},
        {"word": "spot welding", "meaning": "점용접"},
        {"word": "MIG welding", "meaning": "MIG 용접"},
        {"word": "TIG welding", "meaning": "TIG 용접"},
        {"word": "electrode", "meaning": "전극봉"},
        {"word": "welding rod", "meaning": "용접봉"},
        {"word": "filler metal", "meaning": "용가재"},
        {"word": "base metal", "meaning": "모재"},
        {"word": "weld bead", "meaning": "용접 비드"},
        {"word": "joint", "meaning": "이음부"},
        {"word": "seam", "meaning": "이음선"},
        {"word": "torch", "meaning": "토치"},
        {"word": "shielding gas", "meaning": "보호 가스"},
        {"word": "spark", "meaning": "불꽃"},
        {"word": "slag", "meaning": "슬래그"},
        {"word": "spatter", "meaning": "스패터, 튄 금속"},
        {"word": "welding mask", "meaning": "용접면"},
        {"word": "welding gloves", "meaning": "용접 장갑"},
        {"word": "apron", "meaning": "앞치마"},
        {"word": "grind", "meaning": "갈다, 연마하다"},
        {"word": "clamp", "meaning": "클램프"},
        {"word": "cutting torch", "meaning": "절단 토치"},
        {"word": "heat", "meaning": "가열하다"},
        {"word": "melt", "meaning": "녹이다"},
        {"word": "cool down", "meaning": "식히다"},
        {"word": "crack", "meaning": "균열"},
        {"word": "burn mark", "meaning": "그을린 자국"},
    ],
    "🔧 자동차수리": [
        {"word": "auto repair", "meaning": "자동차 수리"},
        {"word": "mechanic", "meaning": "정비사"},
        {"word": "repair shop", "meaning": "정비소"},
        {"word": "inspection", "meaning": "점검"},
        {"word": "maintenance", "meaning": "정비, 유지관리"},
        {"word": "engine", "meaning": "엔진"},
        {"word": "transmission", "meaning": "변속기"},
        {"word": "brake", "meaning": "브레이크"},
        {"word": "brake pad", "meaning": "브레이크 패드"},
        {"word": "tire", "meaning": "타이어"},
        {"word": "wheel", "meaning": "휠"},
        {"word": "suspension", "meaning": "서스펜션"},
        {"word": "shock absorber", "meaning": "쇼크 업소버"},
        {"word": "radiator", "meaning": "라디에이터"},
        {"word": "coolant", "meaning": "냉각수"},
        {"word": "engine oil", "meaning": "엔진 오일"},
        {"word": "oil filter", "meaning": "오일 필터"},
        {"word": "air filter", "meaning": "에어 필터"},
        {"word": "spark plug", "meaning": "점화 플러그"},
        {"word": "belt", "meaning": "벨트"},
        {"word": "hose", "meaning": "호스"},
        {"word": "muffler", "meaning": "소음기"},
        {"word": "exhaust pipe", "meaning": "배기관"},
        {"word": "jack", "meaning": "잭"},
        {"word": "wrench", "meaning": "렌치"},
        {"word": "screwdriver", "meaning": "드라이버"},
        {"word": "replace", "meaning": "교체하다"},
        {"word": "tighten", "meaning": "조이다"},
        {"word": "loosen", "meaning": "풀다"},
        {"word": "test drive", "meaning": "시운전"},
    ],
    "🔋 전기·전자": [
        {"word": "electricity", "meaning": "전기"},
        {"word": "electronics", "meaning": "전자"},
        {"word": "battery", "meaning": "배터리"},
        {"word": "alternator", "meaning": "발전기"},
        {"word": "starter motor", "meaning": "시동 모터"},
        {"word": "motor", "meaning": "모터"},
        {"word": "generator", "meaning": "발전기"},
        {"word": "circuit", "meaning": "회로"},
        {"word": "wire", "meaning": "전선"},
        {"word": "connector", "meaning": "커넥터"},
        {"word": "terminal", "meaning": "단자"},
        {"word": "fuse", "meaning": "퓨즈"},
        {"word": "relay", "meaning": "릴레이"},
        {"word": "switch", "meaning": "스위치"},
        {"word": "sensor", "meaning": "센서"},
        {"word": "ECU", "meaning": "전자제어장치"},
        {"word": "voltage", "meaning": "전압"},
        {"word": "current", "meaning": "전류"},
        {"word": "resistance", "meaning": "저항"},
        {"word": "ground", "meaning": "접지"},
        {"word": "short circuit", "meaning": "합선"},
        {"word": "open circuit", "meaning": "단선"},
        {"word": "multimeter", "meaning": "멀티미터"},
        {"word": "diagnostic scanner", "meaning": "진단 스캐너"},
        {"word": "OBD port", "meaning": "차량 진단 포트"},
        {"word": "warning light", "meaning": "경고등"},
        {"word": "check engine light", "meaning": "엔진 경고등"},
        {"word": "electric vehicle", "meaning": "전기차"},
        {"word": "charging port", "meaning": "충전구"},
        {"word": "inverter", "meaning": "인버터"},
    ],
}

# =========================
# 대화 자료
# =========================
theme_dialogues = {
    "⚙️ 정밀기계": [
        {"en": "A: Please check the blueprint first.", "ko": "A: 먼저 도면을 확인해 주세요."},
        {"en": "B: Okay. I will check the dimensions.", "ko": "B: 네. 치수를 확인하겠습니다."},
        {"en": "A: Use the caliper to measure the diameter.", "ko": "A: 캘리퍼스로 직경을 측정하세요."},
        {"en": "B: The diameter is within tolerance.", "ko": "B: 직경은 공차 범위 안에 있습니다."},
        {"en": "A: Remove the burr after machining.", "ko": "A: 가공 후 버를 제거하세요."},
        {"en": "B: I will deburr the workpiece.", "ko": "B: 가공물의 버를 제거하겠습니다."},
    ],
    "🔥 용접": [
        {"en": "A: Put on your welding mask.", "ko": "A: 용접면을 착용하세요."},
        {"en": "B: Yes, safety comes first.", "ko": "B: 네, 안전이 먼저입니다."},
        {"en": "A: Clamp the base metal tightly.", "ko": "A: 모재를 단단히 고정하세요."},
        {"en": "B: The joint is ready for welding.", "ko": "B: 이음부가 용접 준비되었습니다."},
        {"en": "A: Check the weld bead after cooling.", "ko": "A: 식은 후 용접 비드를 확인하세요."},
        {"en": "B: I can see some spatter here.", "ko": "B: 여기 스패터가 조금 보입니다."},
    ],
    "🔧 자동차수리": [
        {"en": "A: What seems to be the problem?", "ko": "A: 어떤 문제가 있는 것 같나요?"},
        {"en": "B: The brake makes a noise.", "ko": "B: 브레이크에서 소리가 납니다."},
        {"en": "A: We need to inspect the brake pads.", "ko": "A: 브레이크 패드를 점검해야 합니다."},
        {"en": "B: Should we replace them?", "ko": "B: 그것들을 교체해야 하나요?"},
        {"en": "A: Yes, the brake pads are worn out.", "ko": "A: 네, 브레이크 패드가 마모되었습니다."},
        {"en": "B: I will replace the brake pads.", "ko": "B: 브레이크 패드를 교체하겠습니다."},
    ],
    "🔋 전기·전자": [
        {"en": "A: The warning light is on.", "ko": "A: 경고등이 켜져 있습니다."},
        {"en": "B: I will connect the diagnostic scanner.", "ko": "B: 진단 스캐너를 연결하겠습니다."},
        {"en": "A: Check the battery voltage.", "ko": "A: 배터리 전압을 확인하세요."},
        {"en": "B: The voltage is too low.", "ko": "B: 전압이 너무 낮습니다."},
        {"en": "A: There may be a short circuit.", "ko": "A: 합선이 있을 수 있습니다."},
        {"en": "B: I will check the fuse and wires.", "ko": "B: 퓨즈와 전선을 확인하겠습니다."},
    ],
}

# =========================
# 표현 자료
# =========================
theme_expressions = {
    "⚙️ 정밀기계": [
        {"en": "Measure the diameter.", "ko": "직경을 측정하세요."},
        {"en": "Check the tolerance.", "ko": "공차를 확인하세요."},
        {"en": "The surface finish is smooth.", "ko": "표면 마감이 매끄럽습니다."},
        {"en": "Remove the burr.", "ko": "버를 제거하세요."},
        {"en": "Align the workpiece.", "ko": "가공물을 정렬하세요."},
    ],
    "🔥 용접": [
        {"en": "Wear your welding mask.", "ko": "용접면을 착용하세요."},
        {"en": "Clamp the metal tightly.", "ko": "금속을 단단히 고정하세요."},
        {"en": "Watch out for sparks.", "ko": "불꽃을 조심하세요."},
        {"en": "Check the weld bead.", "ko": "용접 비드를 확인하세요."},
        {"en": "Let it cool down.", "ko": "식히세요."},
    ],
    "🔧 자동차수리": [
        {"en": "Inspect the engine.", "ko": "엔진을 점검하세요."},
        {"en": "Replace the oil filter.", "ko": "오일 필터를 교체하세요."},
        {"en": "Tighten the bolts.", "ko": "볼트를 조이세요."},
        {"en": "The tire pressure is low.", "ko": "타이어 공기압이 낮습니다."},
        {"en": "Let's take a test drive.", "ko": "시운전을 해 봅시다."},
    ],
    "🔋 전기·전자": [
        {"en": "Check the battery voltage.", "ko": "배터리 전압을 확인하세요."},
        {"en": "There is a short circuit.", "ko": "합선이 있습니다."},
        {"en": "The fuse is blown.", "ko": "퓨즈가 나갔습니다."},
        {"en": "Connect the diagnostic scanner.", "ko": "진단 스캐너를 연결하세요."},
        {"en": "Reset the error code.", "ko": "오류 코드를 초기화하세요."},
    ],
}

# =========================
# 화면 함수
# =========================
def show_cassette_audio(items, title):
    st.markdown(
        f"""
        <div class="cassette-box">
            <div class="cassette-title">🎧 {title} 전체 듣기</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    text = ". ".join([f"{item['word']}. {item['meaning']}." for item in items])
    play_audio_block(text, label="🎧 전체 듣기", key=f"cassette_{title}")


def show_dialogue(theme_name):
    dialogue = theme_dialogues.get(theme_name, [])
    if not dialogue:
        return

    st.markdown('<div class="dialogue-box">', unsafe_allow_html=True)
    st.markdown('<div class="dialogue-title">💬 현장 대화</div>', unsafe_allow_html=True)

    for item in dialogue:
        st.markdown(f"<div class='dialogue-line'>{html.escape(item['en'])}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='dialogue-meaning'>{html.escape(item['ko'])}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    dialogue_text = make_dialogue_tts_text(dialogue)
    play_audio_block(dialogue_text, label="🎧 대화 전체 듣기", key=f"dialogue_{theme_name}")


def show_expressions(theme_name):
    expressions = theme_expressions.get(theme_name, [])
    if not expressions:
        return

    st.markdown("### 🧾 현장 표현")
    for idx, item in enumerate(expressions):
        st.markdown(
            f"""
            <div class="expression-card">
                <div class="expression-en">{idx + 1}. {html.escape(item['en'])}</div>
                <div class="expression-ko">{html.escape(item['ko'])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        direct_audio_player(item["en"])


def show_word_cards(theme_words, theme_name):
    st.markdown("### 📚 핵심 단어")

    for idx, item in enumerate(theme_words):
        word = item["word"]
        meaning = item["meaning"]
        review_id = make_review_id(theme_name, word)
        checked = review_id in st.session_state.unknown_words
        checkbox_key = f"{theme_name}_unknown_{idx}_{word}"

        st.markdown('<div class="word-card">', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns([1.45, 1.15, 0.35, 1.45, 1.2])

        with col1:
            st.markdown(
                f"""
                <div class="word-row">
                    <div class="word-number">{idx + 1}</div>
                    <div class="word-text">{html.escape(word)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(f"<div class='meaning-text'>{html.escape(meaning)}</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='emoji-text'>{get_word_emoji(word)}</div>", unsafe_allow_html=True)

        with col4:
            direct_audio_player(word)

        with col5:
            review_checked = st.checkbox(
                "복습 희망",
                value=checked,
                key=checkbox_key
            )

            if review_checked and review_id not in st.session_state.unknown_words:
                add_unknown_word(word, meaning, theme_name)
            elif not review_checked and review_id in st.session_state.unknown_words:
                remove_unknown_word(review_id)

        st.markdown("</div>", unsafe_allow_html=True)


def show_theme_tab(theme_name, theme_words):
    st.markdown(
        f"""
        <div class="theme-header">
            <div class="theme-title">{theme_name}</div>
            <div class="theme-desc">자동차과 실습과 현장에서 필요한 단어와 표현을 익혀 봅시다.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    show_cassette_audio(theme_words, theme_name)
    show_dialogue(theme_name)
    show_expressions(theme_name)
    show_word_cards(theme_words, theme_name)


def show_review_tab():
    st.markdown(
        """
        <div class="theme-header">
            <div class="theme-title">⭐ 복습 희망</div>
            <div class="theme-desc">각 탭에서 체크한 단어만 모아 다시 듣고 복습합니다.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    unknown_ids = st.session_state.unknown_words
    unknown_info = st.session_state.unknown_word_info

    if not unknown_ids:
        st.info("아직 체크한 단어가 없습니다. 각 단어 옆의 '복습 희망'을 체크해 보세요.")
        return

    st.success(f"총 {len(unknown_ids)}개의 단어를 체크했습니다.")

    unknown_items = []
    for idx, review_id in enumerate(unknown_ids, start=1):
        info = unknown_info.get(review_id, {})
        word = info.get("word", review_id.split("||")[-1])
        unknown_items.append({
            "word": word,
            "meaning": info.get("meaning", ""),
            "theme": info.get("theme", "복습 희망"),
        })

    show_cassette_audio(unknown_items, "복습 희망")

    st.markdown("### 📌 체크한 단어 목록")

    for idx, review_id in enumerate(list(unknown_ids)):
        info = unknown_info.get(review_id, {})
        word = info.get("word", review_id.split("||")[-1])
        meaning = info.get("meaning", "")
        theme_name = info.get("theme", "")

        st.markdown('<div class="word-card">', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns([1.45, 1.15, 0.35, 1.45, 1.2])

        with col1:
            st.markdown(
                f"""
                <div class="word-row">
                    <div class="word-number">{idx + 1}</div>
                    <div class="word-text">{html.escape(word)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(f"<div class='meaning-text'>{html.escape(meaning)}</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='emoji-text'>{get_word_emoji(word)}</div>", unsafe_allow_html=True)

        with col4:
            direct_audio_player(word)

        with col5:
            if st.button("삭제", key=f"delete_unknown_{idx}_{review_id}", use_container_width=True):
                remove_unknown_word(review_id)
                st.rerun()

        st.caption(f"분류: {theme_name}")

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🗑️ 복습 희망 전체 삭제", key="clear_all_unknown_words", use_container_width=True):
        st.session_state.unknown_words = []
        st.session_state.unknown_word_info = {}
        clear_review_checkbox_keys()
        st.rerun()


# =========================
# 탭 구성
# =========================
tab_names = list(word_themes.keys()) + ["⭐ 복습 희망"]
tabs = st.tabs(tab_names)

for tab, theme_name in zip(tabs[:-1], word_themes.keys()):
    with tab:
        show_theme_tab(theme_name, word_themes[theme_name])

with tabs[-1]:
    show_review_tab()
