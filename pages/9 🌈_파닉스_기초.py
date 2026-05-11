import streamlit as st
from gtts import gTTS
import io
from pathlib import Path

# =========================
# 선생님이 수정할 부분
# =========================
YOUTUBE_VIDEOS = [
    {
        "title": "알파벳 기본 소리 배우기",
        "url": "https://www.youtube.com/watch?v=rTuoEBqjaVg"
    },
]

IMAGE_FILES = [
    {
        "caption": "파닉스 이미지 자료",
        "local": "pages/images/phonics.png",
        "url": "https://raw.githubusercontent.com/Alexwcjung/2026-highschool/main/pages/images/phonics.png"
    }
]

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="Phonics Concept",
    page_icon="🌈",
    layout="wide"
)

# =========================
# TTS 함수
# =========================
@st.cache_data
def make_tts_audio(text, lang="en", tld="com"):
    fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def audio_button(label, text, key):
    if st.button(label, key=key):
        audio_bytes = make_tts_audio(text)
        st.audio(audio_bytes, format="audio/mp3")


def repeat_sound(sound_text):
    return f"{sound_text}.   {sound_text}."


# =========================
# CSS 디자인
# =========================
st.markdown(
    """
    <style>
    .main {
        background-color: #fffdfb;
    }

    .hero-box {
        background: linear-gradient(135deg, #ffeef8 0%, #eef7ff 50%, #fff7df 100%);
        border-radius: 30px;
        padding: 32px 30px;
        margin-bottom: 26px;
        box-shadow: 0 10px 26px rgba(0,0,0,0.08);
        border: 1px solid #f3e8ff;
        text-align: center;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 900;
        color: #334155;
        margin-bottom: 10px;
    }

    .hero-sub {
        font-size: 18px;
        color: #64748b;
        line-height: 1.8;
        margin-bottom: 0;
    }

    .top-guide-box {
        background: linear-gradient(135deg, #fff9db 0%, #fff3c4 100%);
        border-radius: 22px;
        padding: 22px 24px;
        margin-bottom: 24px;
        border: 1px solid #fde68a;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    }

    .top-guide-title {
        font-size: 22px;
        font-weight: 900;
        color: #92400e;
        margin-bottom: 10px;
    }

    .top-guide-text {
        font-size: 16px;
        line-height: 1.8;
        color: #7c5a10;
    }

    .rule-box {
        background: linear-gradient(135deg, #f3f8ff 0%, #ffffff 100%);
        border-radius: 24px;
        padding: 22px 24px;
        margin-bottom: 22px;
        border: 1px solid #dbeafe;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    }

    .rule-title {
        font-size: 22px;
        font-weight: 900;
        color: #1d4ed8;
        margin-bottom: 10px;
    }

    .rule-text {
        font-size: 16px;
        color: #334155;
        line-height: 1.8;
    }

    .video-box {
        background: linear-gradient(135deg, #fff1f2 0%, #f5f3ff 50%, #eff6ff 100%);
        border-radius: 26px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid #fbcfe8;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    }

    .video-title {
        font-size: 26px;
        font-weight: 900;
        color: #be185d;
        margin-bottom: 8px;
    }

    .video-text {
        font-size: 16px;
        color: #475569;
        line-height: 1.8;
    }

    .image-box {
        background: linear-gradient(135deg, #ecfeff 0%, #f0fdf4 50%, #fff7ed 100%);
        border-radius: 26px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid #bae6fd;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    }

    .image-title {
        font-size: 26px;
        font-weight: 900;
        color: #047857;
        margin-bottom: 8px;
    }

    .image-text {
        font-size: 16px;
        color: #475569;
        line-height: 1.8;
    }

    .phonics-card {
        background: linear-gradient(135deg, #ffffff 0%, #fcfcff 100%);
        border-radius: 22px;
        padding: 18px 18px 14px 18px;
        margin-bottom: 16px;
        border: 1px solid #ede9fe;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    }

    .label-small {
        display: inline-block;
        background: #fce7f3;
        color: #be185d;
        font-size: 12px;
        font-weight: 800;
        padding: 5px 10px;
        border-radius: 999px;
        margin-bottom: 8px;
    }

    .pattern-box {
        font-size: 34px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 4px;
    }

    .concept-box {
        font-size: 16px;
        font-weight: 700;
        color: #475569;
        line-height: 1.6;
    }

    .sound-box {
        font-size: 16px;
        font-weight: 800;
        color: #1f2937;
        line-height: 1.7;
    }

    .word-box {
        font-size: 24px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 6px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 900;
        color: #334155;
        margin-bottom: 4px;
    }

    .section-caption {
        font-size: 15px;
        color: #64748b;
        margin-bottom: 14px;
    }

    button[data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 800;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 800;
        border: 1px solid #d1d5db;
        padding: 0.42rem 0.95rem;
    }

    .stButton > button:hover {
        border-color: #8b5cf6;
        color: #8b5cf6;
    }

    div[data-testid="stAudio"] {
        margin-top: 4px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 상단 제목
# =========================
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🌈🐰 Alex의 Phonics Garden 🧸✨</div>
        <div class="hero-sub">
            자음 소리, 짧은 모음, 긴 모음, 모음 예외, 자음 예외를<br>
            귀엽고 쉽게 듣고 익혀 보는 파닉스 기초 학습 공간입니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# 상단 공통 안내 박스
# =========================

def show_rule(title, lines):
    html = f"<div class='rule-box'><div class='rule-title'>{title}</div><div class='rule-text'>"
    for line in lines:
        html += f"• {line}<br>"
    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


def show_fixed_image(image_info, idx):
    caption = image_info.get("caption", f"파닉스 이미지 자료 {idx}")
    local_path = image_info.get("local", "")
    url = image_info.get("url", "")

    if local_path and Path(local_path).exists():
        st.image(local_path, caption=caption, use_container_width=True)
    elif url:
        st.image(url, caption=caption, use_container_width=True)
    else:
        st.warning(f"이미지 자료 {idx}를 불러올 수 없습니다.")


# =========================
# 데이터
# =========================
consonant_sounds = [
    {"pattern": "B b", "letter_name": "bee", "concept": "Consonant sound", "sound_name": "/b/ (브에 가까운 소리)", "sound_audio": repeat_sound("buh"), "word": "bat", "word_audio": "bat"},
    {"pattern": "C c", "letter_name": "see", "concept": "Consonant sound", "sound_name": "/k/ (크에 가까운 소리)", "sound_audio": repeat_sound("kuh"), "word": "cat", "word_audio": "cat"},
    {"pattern": "D d", "letter_name": "dee", "concept": "Consonant sound", "sound_name": "/d/ (드에 가까운 소리)", "sound_audio": repeat_sound("duh"), "word": "dog", "word_audio": "dog"},
    {"pattern": "F f", "letter_name": "eff", "concept": "Consonant sound", "sound_name": "/f/ (입술을 가볍게 물고 내는 프 소리)", "sound_audio": repeat_sound("fff"), "word": "fish", "word_audio": "fish"},
    {"pattern": "G g", "letter_name": "gee", "concept": "Consonant sound", "sound_name": "/g/ (그에 가까운 소리)", "sound_audio": repeat_sound("guh"), "word": "goat", "word_audio": "goat"},
    {"pattern": "H h", "letter_name": "aitch", "concept": "Consonant sound", "sound_name": "/h/ (ㅎ에 가까운 숨소리)", "sound_audio": repeat_sound("huh"), "word": "hat", "word_audio": "hat"},
    {"pattern": "J j", "letter_name": "jay", "concept": "Consonant sound", "sound_name": "/dʒ/ (즈와 쥬 사이 소리)", "sound_audio": repeat_sound("juh"), "word": "jam", "word_audio": "jam"},
    {"pattern": "K k", "letter_name": "kay", "concept": "Consonant sound", "sound_name": "/k/ (크에 가까운 소리)", "sound_audio": repeat_sound("kuh"), "word": "kite", "word_audio": "kite"},
    {"pattern": "L l", "letter_name": "el", "concept": "Consonant sound", "sound_name": "/l/ (혀끝을 윗잇몸에 대는 ㄹ 소리)", "sound_audio": repeat_sound("lll"), "word": "lion", "word_audio": "lion"},
    {"pattern": "M m", "letter_name": "em", "concept": "Consonant sound", "sound_name": "/m/ (음에 가까운 소리)", "sound_audio": repeat_sound("mmm"), "word": "moon", "word_audio": "moon"},
    {"pattern": "N n", "letter_name": "en", "concept": "Consonant sound", "sound_name": "/n/ (느에 가까운 소리)", "sound_audio": repeat_sound("nnn"), "word": "nest", "word_audio": "nest"},
    {"pattern": "P p", "letter_name": "pee", "concept": "Consonant sound", "sound_name": "/p/ (프에 가까운 소리)", "sound_audio": repeat_sound("puh"), "word": "pig", "word_audio": "pig"},
    {"pattern": "Q q", "letter_name": "cue", "concept": "Usually /kw/", "sound_name": "/kw/ (크우에 가까운 소리)", "sound_audio": repeat_sound("kwuh"), "word": "queen", "word_audio": "queen"},
    {"pattern": "R r", "letter_name": "ar", "concept": "Consonant sound", "sound_name": "/r/ (혀를 말아 내는 r 소리)", "sound_audio": repeat_sound("ruh"), "word": "red", "word_audio": "red"},
    {"pattern": "S s", "letter_name": "ess", "concept": "Consonant sound", "sound_name": "/s/ (스에 가까운 소리)", "sound_audio": repeat_sound("sss"), "word": "sun", "word_audio": "sun"},
    {"pattern": "T t", "letter_name": "tee", "concept": "Consonant sound", "sound_name": "/t/ (트에 가까운 소리)", "sound_audio": repeat_sound("tuh"), "word": "top", "word_audio": "top"},
    {"pattern": "V v", "letter_name": "vee", "concept": "Consonant sound", "sound_name": "/v/ (입술을 가볍게 물고 내는 브 소리)", "sound_audio": repeat_sound("vvv"), "word": "van", "word_audio": "van"},
    {"pattern": "W w", "letter_name": "double you", "concept": "Consonant sound", "sound_name": "/w/ (우에서 시작하는 w 소리)", "sound_audio": repeat_sound("wuh"), "word": "window", "word_audio": "window"},
    {"pattern": "X x", "letter_name": "ex", "concept": "Often /ks/", "sound_name": "/ks/ (크스에 가까운 소리)", "sound_audio": repeat_sound("ks"), "word": "fox", "word_audio": "fox"},
    {"pattern": "Y y", "letter_name": "why", "concept": "Consonant sound", "sound_name": "/y/ (이에서 시작하는 y 소리)", "sound_audio": repeat_sound("yuh"), "word": "yes", "word_audio": "yes"},
    {"pattern": "Z z", "letter_name": "zee", "concept": "Consonant sound", "sound_name": "/z/ (즈에 가까운 소리)", "sound_audio": repeat_sound("zzz"), "word": "zebra", "word_audio": "zebra"},
]

short_vowels = [
    {"pattern": "A a", "letter_name": "ay", "concept": "짧은 모음", "sound_name": "Short a /æ/ (애에 가까운 소리)", "sound_audio": repeat_sound("a"), "word": "apple", "word_audio": "apple"},
    {"pattern": "E e", "letter_name": "ee", "concept": "짧은 모음", "sound_name": "Short e /e/ (에에 가까운 소리)", "sound_audio": repeat_sound("eh"), "word": "egg", "word_audio": "egg"},
    {"pattern": "I i", "letter_name": "eye", "concept": "짧은 모음", "sound_name": "Short i /ɪ/ (이와 에 사이의 짧은 소리)", "sound_audio": repeat_sound("ih"), "word": "igloo", "word_audio": "igloo"},
    {"pattern": "O o", "letter_name": "oh", "concept": "짧은 모음", "sound_name": "Short o /ɑ/ (아에 가까운 소리)", "sound_audio": repeat_sound("ah"), "word": "octopus", "word_audio": "octopus"},
    {"pattern": "U u", "letter_name": "you", "concept": "짧은 모음", "sound_name": "Short u /ʌ/ (짧은 어에 가까운 소리)", "sound_audio": repeat_sound("uh"), "word": "umbrella", "word_audio": "umbrella"},
]

long_vowels = [
    {"pattern": "A a", "concept": "긴 모음", "sound_name": "Long a /eɪ/ (에이 소리)", "sound_audio": "cake. name. make.", "word": "cake", "word_audio": "cake"},    
    {"pattern": "E e", "concept": "긴 모음", "sound_name": "Long e /iː/ (긴 이 소리)", "sound_audio": repeat_sound("ee"), "word": "tree", "word_audio": "tree"},
    {"pattern": "I i", "concept": "긴 모음", "sound_name": "Long i /aɪ/ (아이 소리)", "sound_audio": repeat_sound("eye"), "word": "bike", "word_audio": "bike"},
    {"pattern": "O o", "concept": "긴 모음", "sound_name": "Long o /oʊ/ (오우에 가까운 소리)", "sound_audio": repeat_sound("oh"), "word": "rope", "word_audio": "rope"},
    {"pattern": "U u", "concept": "긴 모음", "sound_name": "Long u /juː/ (유에 가까운 소리)", "sound_audio": repeat_sound("you"), "word": "cube", "word_audio": "cube"},
]

# =========================
# 모음 예외: 비슷한 소리는 묶음
# =========================
vowel_exceptions = [
    {
        "pattern": "al / ar / a",
        "concept": "A 예외 묶음",
        "sound_name": "ball, car, father처럼 A가 기본 short a와 다르게 남",
        "sound_audio": repeat_sound("ah"),
        "word": "ball / car / father",
        "word_audio": "ball. car. father."
    },
    {
        "pattern": "unstressed a",
        "concept": "약한 a",
        "sound_name": "about, ago처럼 a가 약한 /ə/ 소리로 남",
        "sound_audio": repeat_sound("uh"),
        "word": "about / ago",
        "word_audio": "about. ago."
    },
    {
        "pattern": "o",
        "concept": "O 예외 묶음",
        "sound_name": "love, come, son처럼 o가 /ʌ/ 소리로 남",
        "sound_audio": repeat_sound("uh"),
        "word": "love / come / son",
        "word_audio": "love. come. son."
    },
    {
        "pattern": "o",
        "concept": "O 예외 묶음",
        "sound_name": "do, to처럼 o가 긴 /uː/ 소리로 남",
        "sound_audio": repeat_sound("oo"),
        "word": "do / to",
        "word_audio": "do. to."
    },
    {
        "pattern": "oo",
        "concept": "OO 소리 비교",
        "sound_name": "book은 짧은 /ʊ/, moon은 긴 /uː/ 소리로 남",
        "sound_audio": "book. moon.",
        "word": "book / moon",
        "word_audio": "book. moon."
    },
    {
        "pattern": "ea",
        "concept": "EA 예외",
        "sound_name": "bread처럼 ea가 /e/ 소리로 나는 경우가 있음",
        "sound_audio": repeat_sound("eh"),
        "word": "bread",
        "word_audio": "bread"
    },
    {
        "pattern": "ou",
        "concept": "OU 예외",
        "sound_name": "country처럼 ou가 /ʌ/ 소리로 나는 경우가 있음",
        "sound_audio": repeat_sound("uh"),
        "word": "country",
        "word_audio": "country"
    },
]

blends = [
    {"pattern": "bl", "concept": "Consonant blend", "sound_name": "bl (블에 가까운 연결 소리)", "sound_audio": repeat_sound("bl"), "word": "black", "word_audio": "black"},
    {"pattern": "br", "concept": "Consonant blend", "sound_name": "br (브르에 가까운 연결 소리)", "sound_audio": repeat_sound("br"), "word": "brown", "word_audio": "brown"},
    {"pattern": "cl", "concept": "Consonant blend", "sound_name": "cl (클에 가까운 연결 소리)", "sound_audio": repeat_sound("cl"), "word": "clock", "word_audio": "clock"},
    {"pattern": "cr", "concept": "Consonant blend", "sound_name": "cr (크르에 가까운 연결 소리)", "sound_audio": repeat_sound("cr"), "word": "crab", "word_audio": "crab"},
    {"pattern": "dr", "concept": "Consonant blend", "sound_name": "dr (드르에 가까운 연결 소리)", "sound_audio": repeat_sound("dr"), "word": "drum", "word_audio": "drum"},
    {"pattern": "fl", "concept": "Consonant blend", "sound_name": "fl (플에 가까운 연결 소리)", "sound_audio": repeat_sound("fl"), "word": "flag", "word_audio": "flag"},
    {"pattern": "fr", "concept": "Consonant blend", "sound_name": "fr (프르에 가까운 연결 소리)", "sound_audio": repeat_sound("fr"), "word": "frog", "word_audio": "frog"},
    {"pattern": "gl", "concept": "Consonant blend", "sound_name": "gl (글에 가까운 연결 소리)", "sound_audio": repeat_sound("gl"), "word": "glass", "word_audio": "glass"},
    {"pattern": "gr", "concept": "Consonant blend", "sound_name": "gr (그르에 가까운 연결 소리)", "sound_audio": repeat_sound("gr"), "word": "green", "word_audio": "green"},
    {"pattern": "pl", "concept": "Consonant blend", "sound_name": "pl (플에 가까운 연결 소리)", "sound_audio": repeat_sound("pl"), "word": "plane", "word_audio": "plane"},
    {"pattern": "pr", "concept": "Consonant blend", "sound_name": "pr (프르에 가까운 연결 소리)", "sound_audio": repeat_sound("pr"), "word": "present", "word_audio": "present"},
    {"pattern": "sk", "concept": "Consonant blend", "sound_name": "sk (스크에 가까운 연결 소리)", "sound_audio": repeat_sound("sk"), "word": "skate", "word_audio": "skate"},
    {"pattern": "sl", "concept": "Consonant blend", "sound_name": "sl (슬에 가까운 연결 소리)", "sound_audio": repeat_sound("sl"), "word": "sleep", "word_audio": "sleep"},
    {"pattern": "sm", "concept": "Consonant blend", "sound_name": "sm (슴에 가까운 연결 소리)", "sound_audio": repeat_sound("sm"), "word": "smile", "word_audio": "smile"},
    {"pattern": "sn", "concept": "Consonant blend", "sound_name": "sn (슨에 가까운 연결 소리)", "sound_audio": repeat_sound("sn"), "word": "snake", "word_audio": "snake"},
    {"pattern": "sp", "concept": "Consonant blend", "sound_name": "sp (스프에 가까운 연결 소리)", "sound_audio": repeat_sound("sp"), "word": "spoon", "word_audio": "spoon"},
    {"pattern": "st", "concept": "Consonant blend", "sound_name": "st (스트에 가까운 연결 소리)", "sound_audio": repeat_sound("st"), "word": "star", "word_audio": "star"},
    {"pattern": "tr", "concept": "Consonant blend", "sound_name": "tr (트르에 가까운 연결 소리)", "sound_audio": repeat_sound("tr"), "word": "tree", "word_audio": "tree"},
]

digraphs = [
    {"pattern": "ch", "concept": "Consonant digraph", "sound_name": "/tʃ/ (치에 가까운 소리)", "sound_audio": repeat_sound("ch"), "word": "chair", "word_audio": "chair"},
    {"pattern": "sh", "concept": "Consonant digraph", "sound_name": "/ʃ/ (쉬에 가까운 소리)", "sound_audio": repeat_sound("sh"), "word": "ship", "word_audio": "ship"},
    {"pattern": "th", "concept": "Voiceless th", "sound_name": "/θ/ (혀를 살짝 내밀고 내는 스 소리)", "sound_audio": repeat_sound("th"), "word": "three", "word_audio": "three"},
    {"pattern": "th", "concept": "Voiced th", "sound_name": "/ð/ (혀를 살짝 내밀고 내는 드 소리)", "sound_audio": repeat_sound("th"), "word": "this", "word_audio": "this"},
    {"pattern": "wh", "concept": "Consonant digraph", "sound_name": "/w/ (우에서 시작하는 w 소리)", "sound_audio": repeat_sound("wuh"), "word": "whale", "word_audio": "whale"},
    {"pattern": "ph", "concept": "Consonant digraph", "sound_name": "/f/ (입술을 가볍게 물고 내는 프 소리)", "sound_audio": repeat_sound("fff"), "word": "phone", "word_audio": "phone"},
    {"pattern": "ck", "concept": "Consonant digraph", "sound_name": "/k/ (크에 가까운 소리)", "sound_audio": repeat_sound("kuh"), "word": "duck", "word_audio": "duck"},
]

vowel_teams = [
    {"pattern": "ai", "concept": "Usually middle", "sound_name": "/eɪ/ (에이에 가까운 소리)", "sound_audio": repeat_sound("ay"), "word": "rain", "word_audio": "rain"},
    {"pattern": "ay", "concept": "Usually end", "sound_name": "/eɪ/ (에이에 가까운 소리)", "sound_audio": repeat_sound("ay"), "word": "day", "word_audio": "day"},
    {"pattern": "ee", "concept": "Long e", "sound_name": "/iː/ (긴 이 소리)", "sound_audio": repeat_sound("ee"), "word": "see", "word_audio": "see"},
    {"pattern": "ea", "concept": "Usually long e", "sound_name": "/iː/ (긴 이 소리)", "sound_audio": repeat_sound("ee"), "word": "eat", "word_audio": "eat"},
    {"pattern": "oa", "concept": "Usually middle", "sound_name": "/oʊ/ (오우에 가까운 소리)", "sound_audio": repeat_sound("oh"), "word": "boat", "word_audio": "boat"},
    {"pattern": "ow", "concept": "Often end", "sound_name": "/oʊ/ (오우에 가까운 소리)", "sound_audio": repeat_sound("oh"), "word": "snow", "word_audio": "snow"},
    {"pattern": "ow", "concept": "Another sound", "sound_name": "/aʊ/ (아우에 가까운 소리)", "sound_audio": repeat_sound("ow"), "word": "cow", "word_audio": "cow"},
    {"pattern": "ou", "concept": "Often /aʊ/", "sound_name": "/aʊ/ (아우에 가까운 소리)", "sound_audio": repeat_sound("ow"), "word": "house", "word_audio": "house"},
    {"pattern": "oi", "concept": "Usually middle", "sound_name": "/ɔɪ/ (오이에 가까운 소리)", "sound_audio": repeat_sound("oy"), "word": "coin", "word_audio": "coin"},
    {"pattern": "oy", "concept": "Usually end", "sound_name": "/ɔɪ/ (오이에 가까운 소리)", "sound_audio": repeat_sound("oy"), "word": "boy", "word_audio": "boy"},
]

r_controlled = [
    {"pattern": "ar", "concept": "R-controlled vowel", "sound_name": "/ɑːr/ (아르에 가까운 소리)", "sound_audio": repeat_sound("ar"), "word": "car", "word_audio": "car"},
    {"pattern": "er", "concept": "R-controlled vowel", "sound_name": "/ɜːr/ (얼에 가까운 소리)", "sound_audio": repeat_sound("er"), "word": "her", "word_audio": "her"},
    {"pattern": "ir", "concept": "R-controlled vowel", "sound_name": "/ɜːr/ (얼에 가까운 소리)", "sound_audio": repeat_sound("er"), "word": "bird", "word_audio": "bird"},
    {"pattern": "or", "concept": "R-controlled vowel", "sound_name": "/ɔːr/ (오르에 가까운 소리)", "sound_audio": repeat_sound("or"), "word": "corn", "word_audio": "corn"},
    {"pattern": "ur", "concept": "R-controlled vowel", "sound_name": "/ɜːr/ (얼에 가까운 소리)", "sound_audio": repeat_sound("er"), "word": "turn", "word_audio": "turn"},
]

silent_e = [
    {"pattern": "a_e", "concept": "Silent e", "sound_name": "Long a /eɪ/ (에이에 가까운 소리)", "sound_audio": repeat_sound("ay"), "word": "cake", "word_audio": "cake"},
    {"pattern": "i_e", "concept": "Silent e", "sound_name": "Long i /aɪ/ (아이 소리)", "sound_audio": repeat_sound("eye"), "word": "bike", "word_audio": "bike"},
    {"pattern": "o_e", "concept": "Silent e", "sound_name": "Long o /oʊ/ (오우에 가까운 소리)", "sound_audio": repeat_sound("oh"), "word": "home", "word_audio": "home"},
    {"pattern": "u_e", "concept": "Silent e", "sound_name": "Long u /juː/ (유에 가까운 소리)", "sound_audio": repeat_sound("you"), "word": "cube", "word_audio": "cube"},
]

consonant_exceptions = [
    {"pattern": "c + e", "concept": "Soft C", "sound_name": "c가 /s/ 소리로 남", "sound_audio": repeat_sound("sss"), "word": "cent", "word_audio": "cent"},
    {"pattern": "c + i", "concept": "Soft C", "sound_name": "c가 /s/ 소리로 남", "sound_audio": repeat_sound("sss"), "word": "city", "word_audio": "city"},
    {"pattern": "c + y", "concept": "Soft C", "sound_name": "c가 /s/ 소리로 남", "sound_audio": repeat_sound("sss"), "word": "cycle", "word_audio": "cycle"},
    {"pattern": "g + e", "concept": "Soft G", "sound_name": "g가 /dʒ/ 소리로 나는 경우가 있음", "sound_audio": repeat_sound("juh"), "word": "gem", "word_audio": "gem"},
    {"pattern": "g + i", "concept": "Soft G", "sound_name": "g가 /dʒ/ 소리로 나는 경우가 있음", "sound_audio": repeat_sound("juh"), "word": "giant", "word_audio": "giant"},
    {"pattern": "g + y", "concept": "Soft G", "sound_name": "g가 /dʒ/ 소리로 나는 경우가 있음", "sound_audio": repeat_sound("juh"), "word": "gym", "word_audio": "gym"},
    {"pattern": "kn", "concept": "Silent k", "sound_name": "k는 소리 나지 않고 n만 남", "sound_audio": repeat_sound("nnn"), "word": "knee", "word_audio": "knee"},
    {"pattern": "wr", "concept": "Silent w", "sound_name": "w는 소리 나지 않고 r만 남", "sound_audio": repeat_sound("ruh"), "word": "write", "word_audio": "write"},
    {"pattern": "mb", "concept": "Silent b", "sound_name": "단어 끝 mb에서 b는 소리 나지 않음", "sound_audio": repeat_sound("mmm"), "word": "lamb", "word_audio": "lamb"},
    {"pattern": "x", "concept": "x as /gz/", "sound_name": "x가 /gz/ 소리로 나는 경우", "sound_audio": repeat_sound("gz"), "word": "exam", "word_audio": "exam"},
]


# =========================
# 카드 출력 함수
# =========================
def show_cards(data, title, show_letter_name=False):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-caption'>버튼을 눌러 이름, 실제 소리, 예시 단어를 들어 보세요.</div>", unsafe_allow_html=True)

    for idx, item in enumerate(data):
        st.markdown('<div class="phonics-card">', unsafe_allow_html=True)

        if show_letter_name:
            col1, col2, col3, col4, col5 = st.columns([1.1, 1.3, 1.5, 1.9, 1.7])
        else:
            col1, col2, col3, col4 = st.columns([1.1, 1.6, 2.1, 1.7])

        with col1:
            st.markdown("<div class='label-small'>글자 / 패턴</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='pattern-box'>{item['pattern']}</div>", unsafe_allow_html=True)

        if show_letter_name:
            with col2:
                st.markdown("<div class='label-small'>알파벳 이름</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='concept-box'>{item['letter_name']}</div>", unsafe_allow_html=True)
                audio_button("🔊 이름 듣기", item["letter_name"], key=f"name_{title}_{idx}_{item['pattern']}_{item['word']}")

            with col3:
                st.markdown("<div class='label-small'>조건 / 개념</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='concept-box'>{item['concept']}</div>", unsafe_allow_html=True)

            with col4:
                st.markdown("<div class='label-small'>실제 소리</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='sound-box'>{item['sound_name']}</div>", unsafe_allow_html=True)
                audio_button("🔊 실제 소리 듣기", item["sound_audio"], key=f"sound_{title}_{idx}_{item['pattern']}_{item['word']}")

            with col5:
                st.markdown("<div class='label-small'>예시 단어</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='word-box'>{item['word']}</div>", unsafe_allow_html=True)
                audio_button("🔊 단어 듣기", item["word_audio"], key=f"word_{title}_{idx}_{item['pattern']}_{item['word']}")

        else:
            with col2:
                st.markdown("<div class='label-small'>조건 / 개념</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='concept-box'>{item['concept']}</div>", unsafe_allow_html=True)

            with col3:
                st.markdown("<div class='label-small'>실제 소리</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='sound-box'>{item['sound_name']}</div>", unsafe_allow_html=True)
                audio_button("🔊 실제 소리 듣기", item["sound_audio"], key=f"sound_{title}_{idx}_{item['pattern']}_{item['word']}")

            with col4:
                st.markdown("<div class='label-small'>예시 단어</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='word-box'>{item['word']}</div>", unsafe_allow_html=True)
                audio_button("🔊 단어 듣기", item["word_audio"], key=f"word_{title}_{idx}_{item['pattern']}_{item['word']}")

        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 탭 구성
# =========================
tabs = st.tabs([
    "🎬 YouTube 영상",
    "🖼️ 이미지 자료",
    "① 자음 소리",
    "② 짧은 모음",
    "③ 긴 모음",
    "④ 모음 예외",
    "⑤ 자음 이어 읽기",
    "⑥ 두 글자 한 소리",
    "⑦ 모음 두 글자 소리",
    "⑧ r이 붙은 모음",
    "⑨ 소리 안 나는 e",
    "⑩ 자음 예외"
])

# =========================
# 0. YouTube 영상 탭
# =========================
with tabs[0]:
    st.markdown(
        """
        <div class="video-box">
            <div class="video-title">🎬 파닉스 영상으로 먼저 배우기</div>
            <div class="video-text">
                선생님이 선택한 YouTube 파닉스 영상을 보고 알파벳 소리와 파닉스의 기본 개념을 익혀 봅니다.<br>
                영상을 본 뒤 이미지 자료를 보고, 그다음 자음과 모음 소리를 차례대로 연습합니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    for idx, video in enumerate(YOUTUBE_VIDEOS, start=1):
        title = video.get("title", f"영상 {idx}")
        url = video.get("url", "")

        if url:
            st.markdown(f"### 🎬 {idx}. {title}")
            st.video(url)
            st.markdown("---")

    st.markdown(
        """
        <div class="top-guide-box">
            <div class="top-guide-title">🌱 영상 시청 후 활동</div>
            <div class="top-guide-text">
                • 영상에서 들은 알파벳 소리를 따라 말해 봅니다.<br>
                • 알파벳 이름과 실제 소리가 어떻게 다른지 생각해 봅니다.<br>
                • 다음 탭으로 이동해 <b>이미지 자료</b>를 확인합니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# 1. 이미지 자료 탭
# =========================
with tabs[1]:
    st.markdown(
        """
        <div class="image-box">
            <div class="image-title">🖼️ 파닉스 이미지 자료 보기</div>
            <div class="image-text">
                선생님이 GitHub에 올린 파닉스 이미지 자료를 보여주는 공간입니다.<br>
                알파벳 표, 발음표, 단어 카드, 활동지 이미지를 넣어 수업에 활용할 수 있습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if IMAGE_FILES:
        for idx, image_info in enumerate(IMAGE_FILES, start=1):
            show_fixed_image(image_info, idx)
    else:
        st.info("아직 등록된 이미지가 없습니다.")

# =========================
# 2. 자음 소리
# =========================
with tabs[2]:
    show_rule(
        "자음 소리 Consonant Sounds",
        [
            "알파벳 이름과 실제 자음 소리는 다릅니다.",
            "예를 들어 B의 이름은 bee이지만, 실제 소리는 /b/입니다.",
            "표의 한글 소리 힌트는 정확한 발음값이 아니라 학생들이 소리를 떠올리기 위한 참고용입니다.",
            "정확한 발음은 반드시 실제 소리 듣기 버튼으로 확인하도록 지도하면 좋습니다."
        ]
    )
    show_cards(consonant_sounds, "① 자음 소리", show_letter_name=True)

# =========================
# 3. 짧은 모음
# =========================
with tabs[3]:
    show_rule(
        "짧은 모음 Short Vowels 규칙",
        [
            "짧은 모음은 짧게 나는 모음 소리입니다.",
            "보통 모음이 자음 사이에 끼어 있는 CVC 단어에서 많이 나타납니다.",
            "예: cat, bed, sit, hot, cup",
            "발음기호 옆의 한글 소리 힌트는 정확한 발음값이 아니라 소리를 떠올리기 위한 참고용입니다.",
            "실제 소리 버튼은 short a라고 읽지 않고, 실제 영어 소리만 두 번 들려줍니다."
        ]
    )
    show_cards(short_vowels, "② 짧은 모음 Short Vowels", show_letter_name=True)

# =========================
# 4. 긴 모음
# =========================
with tabs[4]:
    show_rule(
        "긴 모음 Long Vowels 규칙",
        [
            "긴 모음은 보통 알파벳 이름과 비슷하게 나는 소리입니다.",
            "모음 뒤에 자음이 오고, 단어 끝에 e가 붙으면 앞의 모음이 긴 모음이 되는 경우가 많습니다.",
            "예: cap → cape, kit → kite, hop → hope",
            "두 모음이 함께 나올 때 첫 번째 모음이 긴 모음으로 나는 경우도 많습니다.",
            "예: rain, boat, see",
            "한글 소리 힌트는 참고용이며, 정확한 발음은 실제 소리 듣기 버튼으로 확인합니다."
        ]
    )
    show_cards(long_vowels, "③ 긴 모음 Long Vowels")

# =========================
# 5. 모음 예외
# =========================
with tabs[5]:
    show_rule(
        "모음 예외 소리 규칙",
        [
            "영어 모음은 항상 짧은 모음이나 긴 모음으로만 읽히지 않습니다.",
            "비슷한 예외 소리는 한 줄로 묶어서 익히면 더 쉽습니다.",
            "al, ar, father 계열은 A가 기본 short a와 다르게 나는 경우입니다. 예: ball, car, father",
            "강세가 약한 a는 /ə/처럼 약하게 나는 경우가 많습니다. 예: about, ago",
            "o는 love, come, son처럼 /ʌ/ 소리로 나는 경우가 있습니다.",
            "o는 do, to처럼 긴 /uː/ 소리로 나는 경우도 있습니다.",
            "oo는 book처럼 짧은 /ʊ/ 소리도 나고, moon처럼 긴 /uː/ 소리도 납니다.",
            "ea는 bread처럼 /e/로 나는 예외가 있습니다.",
            "ou는 country처럼 /ʌ/로 나는 예외가 있습니다.",
            "한글 소리 힌트는 참고용이며, 정확한 발음은 실제 소리 듣기 버튼으로 확인합니다."
        ]
    )
    show_cards(vowel_exceptions, "④ 모음 예외 소리")

# =========================
# 6. 자음 이어 읽기
# =========================
with tabs[6]:
    show_rule(
        "자음 이어 읽기 Consonant Blends",
        [
            "Blends는 두 자음이 이어져 나지만, 각각의 소리가 어느 정도 살아 있습니다.",
            "예: bl은 /b/와 /l/ 소리가 이어집니다.",
            "black, brown, frog, star처럼 단어의 앞부분에서 자주 나옵니다.",
            "한글 소리 힌트는 참고용이며, 실제 연결 소리는 버튼으로 확인합니다."
        ]
    )
    show_cards(blends, "⑤ 자음 이어 읽기")

# =========================
# 7. 두 글자 한 소리
# =========================
with tabs[7]:
    show_rule(
        "두 글자 한 소리 Consonant Digraphs",
        [
            "Digraphs는 두 글자가 만나 하나의 새로운 소리를 만드는 경우입니다.",
            "ch, sh, th, ph, ck 등이 대표적입니다.",
            "예: ch는 chair, sh는 ship, ph는 phone에서 하나의 소리처럼 납니다.",
            "th는 three의 /θ/ 소리와 this의 /ð/ 소리가 다를 수 있습니다.",
            "한글 소리 힌트는 참고용이며, 정확한 발음은 실제 소리 듣기 버튼으로 확인합니다."
        ]
    )
    show_cards(digraphs, "⑥ 두 글자 한 소리")

# =========================
# 8. 모음 두 글자 소리
# =========================
with tabs[8]:
    show_rule(
        "모음 두 글자 소리 Vowel Teams",
        [
            "Vowel Teams는 두 모음 글자가 함께 하나의 모음 소리를 만드는 경우입니다.",
            "ai와 ay는 보통 /eɪ/ 소리가 납니다. ai는 단어 중간, ay는 단어 끝에 많이 옵니다.",
            "예: rain, day",
            "oa와 ow는 보통 /oʊ/ 소리가 납니다. 예: boat, snow",
            "ow와 ou는 /aʊ/ 소리도 납니다. 예: cow, house",
            "oi와 oy는 /ɔɪ/ 소리가 납니다. oi는 단어 중간, oy는 단어 끝에 많이 옵니다.",
            "예: coin, boy",
            "한글 소리 힌트는 참고용이며, 정확한 발음은 실제 소리 듣기 버튼으로 확인합니다."
        ]
    )
    show_cards(vowel_teams, "⑦ 모음 두 글자 소리")

# =========================
# 9. r이 붙은 모음
# =========================
with tabs[9]:
    show_rule(
        "r이 붙은 모음 R-Controlled Vowels",
        [
            "모음 뒤에 r이 오면 r의 영향을 받아 모음 소리가 바뀝니다.",
            "ar은 car처럼 /ɑːr/ 소리가 납니다.",
            "er, ir, ur은 her, bird, turn처럼 비슷한 /ɜːr/ 소리로 나는 경우가 많습니다.",
            "or은 corn처럼 /ɔːr/ 소리가 납니다.",
            "한글 소리 힌트는 참고용이며, 정확한 발음은 실제 소리 듣기 버튼으로 확인합니다."
        ]
    )
    show_cards(r_controlled, "⑧ r이 붙은 모음")

# =========================
# 10. 소리 안 나는 e
# =========================
with tabs[10]:
    show_rule(
        "소리 안 나는 e Silent e",
        [
            "단어 끝의 e는 직접 소리 나지 않는 경우가 많습니다.",
            "하지만 앞의 모음을 긴 모음으로 바꾸는 역할을 합니다.",
            "예: cap은 짧은 a, cape는 긴 a입니다.",
            "kit → kite, hop → hope, cub → cube처럼 소리가 달라집니다.",
            "그래서 silent e는 magic e라고도 부릅니다.",
            "한글 소리 힌트는 참고용이며, 정확한 발음은 실제 소리 듣기 버튼으로 확인합니다."
        ]
    )
    show_cards(silent_e, "⑨ 소리 안 나는 e")

# =========================
# 11. 자음 예외
# =========================
with tabs[11]:
    show_rule(
        "자음 예외 소리 규칙",
        [
            "영어 자음은 항상 기본 소리로만 읽히지 않습니다.",
            "c는 보통 /k/ 소리가 나지만, 뒤에 e, i, y가 오면 /s/ 소리가 나는 경우가 많습니다.",
            "예: cent, city, cycle",
            "g는 보통 /g/ 소리가 나지만, 뒤에 e, i, y가 오면 /dʒ/ 소리가 나는 경우가 있습니다.",
            "예: gem, giant, gym",
            "kn, wr, mb처럼 어떤 글자는 보이지만 소리 나지 않는 경우도 있습니다.",
            "예: knee, write, lamb",
            "x는 fox처럼 /ks/로 나기도 하지만, exam처럼 /gz/로 나는 경우도 있습니다.",
            "한글 소리 힌트는 참고용이며, 정확한 발음은 실제 소리 듣기 버튼으로 확인합니다."
        ]
    )
    show_cards(consonant_exceptions, "⑩ 자음 예외 소리")
