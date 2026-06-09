
import streamlit as st
from urllib.parse import quote
import requests
import hashlib
import random
import re
import html
import base64
import json
import uuid
import streamlit.components.v1 as components

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="Survival English 160",
    page_icon="🛟",
    layout="wide"
)

# =========================
# CSS 디자인
# =========================
st.markdown(
    """
    <style>
    .main-title {
        font-size: 44px;
        font-weight: 900;
        color: #1f2937;
        margin-bottom: 4px;
    }

    .sub-title {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 24px;
    }

    .hero-box {
        background: linear-gradient(135deg, #ecfeff 0%, #fef3c7 50%, #fce7f3 100%);
        border-radius: 22px;
        padding: 18px 22px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        border: 1px solid rgba(255,255,255,0.8);
    }

    .hero-title {
        font-size: 27px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 10px;
    }

    .hero-text {
        font-size: 16px;
        color: #374151;
        line-height: 1.8;
    }

    .theme-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 50%, #ec4899 100%);
        color: white;
        padding: 30px 32px;
        border-radius: 28px;
        margin-bottom: 26px;
        box-shadow: 0 10px 24px rgba(14,165,233,0.28);
    }

    .theme-title {
        font-size: 40px;
        font-weight: 1000;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
        line-height: 1.15;
    }

    .theme-desc {
        font-size: 19px;
        font-weight: 800;
        opacity: 0.98;
        line-height: 1.55;
    }

    .dialogue-box {
        background: #fefce8;
        border: 1px solid #fde68a;
        border-radius: 24px;
        padding: 20px 22px;
        margin-bottom: 24px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }

    .dialogue-title {
        font-size: 24px;
        font-weight: 900;
        color: #854d0e;
        margin-bottom: 14px;
    }

    .dialogue-line {
        font-size: 18px;
        font-weight: 900;
        color: #111827;
        margin-top: 10px;
    }

    .dialogue-meaning {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 5px;
    }

    .word-card {
        background: white;
        border-radius: 18px;
        padding: 10px 14px;
        margin-bottom: 8px;
        border: 1px solid #e0f2fe;
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
        color: #0369a1;
        background: #e0f2fe;
        border-radius: 999px;
        padding: 5px 9px;
        text-align: center;
    }

    .word-text {
        min-width: 170px;
        font-size: 25px;
        font-weight: 900;
        color: #111827;
        white-space: nowrap;
    }

    .meaning-text {
        font-size: 19px;
        font-weight: 800;
        color: #374151;
        margin-left: 8px;
        white-space: nowrap;
        line-height: 42px;
    }

    .emoji-text {
        font-size: 25px;
        line-height: 1;
        text-align: center;
        padding-top: 2px;
    }

    .quiz-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 22px 24px;
        margin-bottom: 18px;
        border: 1px solid #e9d5ff;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    }

    .quiz-number {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        padding: 6px 12px;
        border-radius: 999px;
        font-weight: 900;
        font-size: 13px;
        margin-bottom: 10px;
    }

    .quiz-word {
        font-size: 34px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 8px;
    }

    .score-box {
        background: linear-gradient(135deg, #dcfce7 0%, #dbeafe 50%, #fce7f3 100%);
        border-radius: 24px;
        padding: 24px 26px;
        margin: 20px 0;
        border: 1px solid #bbf7d0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }

    .score-title {
        font-size: 27px;
        font-weight: 900;
        color: #14532d;
    }

    .wrong-box {
        background: #fff7ed;
        border-left: 6px solid #fb923c;
        border-radius: 18px;
        padding: 16px 18px;
        margin: 18px 0;
        color: #7c2d12;
        font-weight: 700;
    }

    .answer-box {
        background: #f8fafc;
        border-radius: 20px;
        padding: 18px 20px;
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 800;
        border: 1px solid #d1d5db;
        padding: 0.45rem 1rem;
    }

    .stButton > button:hover {
        border-color: #0ea5e9;
        color: #0ea5e9;
    }


    /* 카테고리 탭 글자 크게 */
    div[data-baseweb="tab-list"] {
        gap: 10px;
        flex-wrap: wrap;
    }

    button[data-baseweb="tab"] {
        min-height: 58px;
        padding: 12px 18px;
        border-radius: 18px 18px 0 0;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        margin-right: 4px;
    }

    button[data-baseweb="tab"] p {
        font-size: 21px !important;
        font-weight: 1000 !important;
        color: #111827 !important;
        line-height: 1.25 !important;
        white-space: nowrap;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #dbeafe, #fce7f3);
        border-bottom: 4px solid #8b5cf6;
    }

    /* 학습 모드 선택 글자도 조금 크게 */
    div[role="radiogroup"] label p {
        font-size: 18px !important;
        font-weight: 900 !important;
    }

    @media (max-width: 600px) {
        .main-title {
            font-size: 34px;
        }

        .theme-header {
            padding: 24px 22px;
            border-radius: 24px;
        }

        .theme-title {
            font-size: 33px;
        }

        .theme-desc {
            font-size: 16px;
        }

        button[data-baseweb="tab"] {
            min-height: 52px;
            padding: 10px 14px;
        }

        button[data-baseweb="tab"] p {
            font-size: 18px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 상단 제목
# =========================
st.markdown("<div class='main-title'>🛟 Survival English 160</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>생존 회화에 꼭 필요한 문장과 단어를 듣고, 따라 하고, 퀴즈로 익혀 봅시다.</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-text" style="font-size:18px; font-weight:900; color:#374151;">
            이 단어 160개만 외우면 미국에서 생존이 가능합니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# TTS 함수 - 일상 400과 같은 requests 방식
# =========================
def make_google_tts_url(text, lang="en"):
    clean_text = str(text).strip()
    if not clean_text:
        clean_text = "Hello"
    encoded = quote(clean_text)
    return f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={encoded}"


@st.cache_data(show_spinner=False)
def get_tts_mp3_bytes(text, lang="en"):
    """Google TTS mp3를 requests로 직접 받아와 st.audio에서 재생합니다."""
    clean_text = str(text).strip()
    if not clean_text:
        clean_text = "Hello"

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


def make_tts_audio(text, lang="en", tld="com"):
    """기존 코드 호환용 함수입니다."""
    return get_tts_mp3_bytes(text, lang=lang)


def remove_speaker_label(sentence):
    return re.sub(r"^[A-Z]:\s*", "", sentence).strip()


def make_dialogue_tts_text(dialogue):
    return " ".join([remove_speaker_label(item["en"]) for item in dialogue])


def instant_audio_button(label, text, key=None, height=46):
    """
    화면에 st.audio 플레이어를 띄우지 않고, 버튼을 누르면 바로 소리만 재생합니다.
    Google TTS mp3는 requests로 받아와 base64로 넣기 때문에 gTTS 파일 생성보다 오류가 적고,
    브라우저 자동재생 제한도 사용자 클릭 안에서 처리됩니다.
    """
    text = str(text).strip()
    if not text:
        return

    if key is None:
        key = "instant_audio_" + hashlib.md5((label + "::" + text).encode("utf-8")).hexdigest()

    safe_id = re.sub(r"[^a-zA-Z0-9_]", "_", str(key))

    try:
        audio_bytes = get_tts_mp3_bytes(text, lang="en")
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        button_html = f"""
        <button id="btn_{safe_id}" style="
            width:100%;
            min-height:38px;
            border-radius:999px;
            border:1px solid #d1d5db;
            background:#ffffff;
            color:#111827;
            font-size:15px;
            font-weight:900;
            cursor:pointer;
            box-shadow:0 2px 6px rgba(15,23,42,0.06);
        ">{html.escape(label)}</button>

        <script>
        const btn_{safe_id} = document.getElementById("btn_{safe_id}");
        const audio_{safe_id} = new Audio("data:audio/mp3;base64,{audio_b64}");
        audio_{safe_id}.preload = "auto";

        btn_{safe_id}.addEventListener("click", function() {{
            audio_{safe_id}.pause();
            audio_{safe_id}.currentTime = 0;
            audio_{safe_id}.play().then(function() {{
                btn_{safe_id}.innerText = "🔊 재생 중";
            }}).catch(function() {{
                btn_{safe_id}.innerText = "다시 누르기";
            }});
        }});

        audio_{safe_id}.addEventListener("ended", function() {{
            btn_{safe_id}.innerText = "{html.escape(label)}";
        }});
        </script>
        """
        components.html(button_html, height=height, scrolling=False)

    except Exception as e:
        st.error("음성 파일을 만들지 못했습니다. requirements.txt에 requests가 있는지 확인해 주세요.")
        st.caption(f"오류 내용: {e}")
        st.link_button("🔊 새 창에서 듣기", make_google_tts_url(text, lang="en"), use_container_width=True)


def play_audio_block(text, label="🔊 듣기", show_link=True, key=None):
    # st.audio 플레이어를 띄우지 않고, 클릭 즉시 재생합니다.
    instant_audio_button(label, text, key=key, height=48)


def direct_audio_player(text, show_link=True):
    # 단어 카드용: 오디오 플레이어 없이 바로 재생 버튼만 보여줍니다.
    instant_audio_button("🔊 듣기", text, height=48)


# =========================
# 생존 회화 160 테마별 단어
# =========================
word_themes = {
    "🧍 나와 사람": [
        {"word": "I", "meaning": "나"},
        {"word": "you", "meaning": "너, 당신"},
        {"word": "he", "meaning": "그"},
        {"word": "she", "meaning": "그녀"},
        {"word": "we", "meaning": "우리"},
        {"word": "they", "meaning": "그들"},
        {"word": "friend", "meaning": "친구"},
        {"word": "teacher", "meaning": "선생님"},
        {"word": "student", "meaning": "학생"},
        {"word": "classmate", "meaning": "반 친구"},
        {"word": "family", "meaning": "가족"},
        {"word": "father", "meaning": "아버지"},
        {"word": "mother", "meaning": "어머니"},
        {"word": "brother", "meaning": "형제, 남자 형제"},
        {"word": "sister", "meaning": "자매, 여자 형제"},
        {"word": "name", "meaning": "이름"},
        {"word": "person", "meaning": "사람"},
        {"word": "man", "meaning": "남자"},
        {"word": "woman", "meaning": "여자"},
        {"word": "child", "meaning": "아이"},
    ],
    "🏃 기본 동작": [
        {"word": "go", "meaning": "가다"},
        {"word": "come", "meaning": "오다"},
        {"word": "walk", "meaning": "걷다"},
        {"word": "run", "meaning": "달리다"},
        {"word": "sit", "meaning": "앉다"},
        {"word": "stand", "meaning": "서다"},
        {"word": "stop", "meaning": "멈추다"},
        {"word": "start", "meaning": "시작하다"},
        {"word": "open", "meaning": "열다"},
        {"word": "close", "meaning": "닫다"},
        {"word": "eat", "meaning": "먹다"},
        {"word": "drink", "meaning": "마시다"},
        {"word": "sleep", "meaning": "자다"},
        {"word": "study", "meaning": "공부하다"},
        {"word": "read", "meaning": "읽다"},
        {"word": "write", "meaning": "쓰다"},
        {"word": "listen", "meaning": "듣다"},
        {"word": "speak", "meaning": "말하다"},
        {"word": "help", "meaning": "돕다"},
        {"word": "wait", "meaning": "기다리다"},
    ],
    "💖 감정·몸 상태": [
        {"word": "happy", "meaning": "행복한"},
        {"word": "sad", "meaning": "슬픈"},
        {"word": "angry", "meaning": "화난"},
        {"word": "tired", "meaning": "피곤한"},
        {"word": "hungry", "meaning": "배고픈"},
        {"word": "thirsty", "meaning": "목마른"},
        {"word": "sick", "meaning": "아픈"},
        {"word": "okay", "meaning": "괜찮은"},
        {"word": "fine", "meaning": "괜찮은"},
        {"word": "cold", "meaning": "추운, 차가운"},
        {"word": "hot", "meaning": "더운, 뜨거운"},
        {"word": "pain", "meaning": "통증"},
        {"word": "headache", "meaning": "두통"},
        {"word": "stomachache", "meaning": "복통"},
        {"word": "fever", "meaning": "열"},
        {"word": "hurt", "meaning": "아프다, 다치다"},
        {"word": "good", "meaning": "좋은"},
        {"word": "bad", "meaning": "나쁜"},
        {"word": "worried", "meaning": "걱정하는"},
        {"word": "scared", "meaning": "무서워하는"},
    ],
    "🍎 음식·물": [
        {"word": "food", "meaning": "음식"},
        {"word": "water", "meaning": "물"},
        {"word": "rice", "meaning": "밥, 쌀"},
        {"word": "bread", "meaning": "빵"},
        {"word": "milk", "meaning": "우유"},
        {"word": "juice", "meaning": "주스"},
        {"word": "coffee", "meaning": "커피"},
        {"word": "tea", "meaning": "차"},
        {"word": "apple", "meaning": "사과"},
        {"word": "banana", "meaning": "바나나"},
        {"word": "egg", "meaning": "달걀"},
        {"word": "meat", "meaning": "고기"},
        {"word": "chicken", "meaning": "닭고기, 닭"},
        {"word": "fish", "meaning": "생선, 물고기"},
        {"word": "breakfast", "meaning": "아침 식사"},
        {"word": "lunch", "meaning": "점심 식사"},
        {"word": "dinner", "meaning": "저녁 식사"},
        {"word": "snack", "meaning": "간식"},
        {"word": "medicine", "meaning": "약"},
        {"word": "hospital", "meaning": "병원"},
    ],
    "🚗 장소·이동": [
        {"word": "home", "meaning": "집"},
        {"word": "school", "meaning": "학교"},
        {"word": "classroom", "meaning": "교실"},
        {"word": "bathroom", "meaning": "화장실"},
        {"word": "hospital", "meaning": "병원"},
        {"word": "store", "meaning": "가게"},
        {"word": "station", "meaning": "역"},
        {"word": "bus", "meaning": "버스"},
        {"word": "car", "meaning": "자동차"},
        {"word": "taxi", "meaning": "택시"},
        {"word": "train", "meaning": "기차"},
        {"word": "bike", "meaning": "자전거"},
        {"word": "road", "meaning": "도로"},
        {"word": "street", "meaning": "거리"},
        {"word": "here", "meaning": "여기"},
        {"word": "there", "meaning": "거기"},
        {"word": "near", "meaning": "가까운"},
        {"word": "far", "meaning": "먼"},
        {"word": "left", "meaning": "왼쪽"},
        {"word": "right", "meaning": "오른쪽, 맞는"},
    ],
    "⏰ 시간·숫자": [
        {"word": "time", "meaning": "시간"},
        {"word": "now", "meaning": "지금"},
        {"word": "today", "meaning": "오늘"},
        {"word": "tomorrow", "meaning": "내일"},
        {"word": "yesterday", "meaning": "어제"},
        {"word": "morning", "meaning": "아침"},
        {"word": "afternoon", "meaning": "오후"},
        {"word": "evening", "meaning": "저녁"},
        {"word": "night", "meaning": "밤"},
        {"word": "nine", "meaning": "아홉"},
        {"word": "late", "meaning": "늦은"},
        {"word": "one", "meaning": "하나"},
        {"word": "two", "meaning": "둘"},
        {"word": "three", "meaning": "셋"},
        {"word": "four", "meaning": "넷"},
        {"word": "five", "meaning": "다섯"},
        {"word": "six", "meaning": "여섯"},
        {"word": "seven", "meaning": "일곱"},
        {"word": "eight", "meaning": "여덟"},
        {"word": "ten", "meaning": "열"},
    ],
    "🎒 물건·돈": [
        {"word": "bag", "meaning": "가방"},
        {"word": "phone", "meaning": "전화기"},
        {"word": "book", "meaning": "책"},
        {"word": "notebook", "meaning": "공책"},
        {"word": "pen", "meaning": "펜"},
        {"word": "pencil", "meaning": "연필"},
        {"word": "desk", "meaning": "책상"},
        {"word": "chair", "meaning": "의자"},
        {"word": "door", "meaning": "문"},
        {"word": "window", "meaning": "창문"},
        {"word": "key", "meaning": "열쇠"},
        {"word": "money", "meaning": "돈"},
        {"word": "card", "meaning": "카드"},
        {"word": "ticket", "meaning": "표, 티켓"},
        {"word": "clothes", "meaning": "옷"},
        {"word": "shoes", "meaning": "신발"},
        {"word": "hat", "meaning": "모자"},
        {"word": "watch", "meaning": "시계"},
        {"word": "cup", "meaning": "컵"},
        {"word": "bottle", "meaning": "병"},
    ],
    "🆘 도움 요청": [
        {"word": "help", "meaning": "도움, 돕다"},
        {"word": "please", "meaning": "부디, 제발"},
        {"word": "sorry", "meaning": "미안합니다"},
        {"word": "excuse me", "meaning": "실례합니다"},
        {"word": "again", "meaning": "다시"},
        {"word": "slowly", "meaning": "천천히"},
        {"word": "understand", "meaning": "이해하다"},
        {"word": "question", "meaning": "질문"},
        {"word": "problem", "meaning": "문제"},
        {"word": "need", "meaning": "필요하다"},
        {"word": "want", "meaning": "원하다"},
        {"word": "know", "meaning": "알다"},
        {"word": "say", "meaning": "말하다"},
        {"word": "tell", "meaning": "말하다, 알려주다"},
        {"word": "ask", "meaning": "묻다"},
        {"word": "answer", "meaning": "대답, 답"},
        {"word": "repeat", "meaning": "반복하다"},
        {"word": "speak", "meaning": "말하다"},
        {"word": "look", "meaning": "보다"},
        {"word": "listen", "meaning": "듣다"},
    ],
}


# =========================
# 뜻 표시 함수
# =========================
def get_display_meaning(word, korean_meaning):
    """한국어 뜻만 보여줍니다."""
    return korean_meaning


# =========================
# 단어별 예문
# =========================
CASSETTE_EXAMPLES = {
    "I": "I am a student.", "you": "You are my friend.", "he": "He is my friend.", "she": "She is a student.",
    "we": "We are happy.", "they": "They are students.", "friend": "He is my friend.", "teacher": "She is my teacher.",
    "student": "I am a student.", "classmate": "He is my classmate.", "family": "This is my family.",
    "father": "He is my father.", "mother": "She is my mother.", "brother": "He is my brother.",
    "sister": "She is my sister.", "name": "My name is Alex.", "person": "He is a good person.",
    "man": "He is a man.", "woman": "She is a woman.", "child": "He is a child.",

    "go": "I go to school.", "come": "Please come here.", "walk": "I walk to school.", "run": "I can run.",
    "sit": "Please sit down.", "stand": "Please stand up.", "stop": "Please stop.", "start": "Let's start.",
    "open": "Open the door.", "close": "Close the door.", "eat": "I eat lunch.", "drink": "I drink water.",
    "sleep": "I sleep at night.", "study": "I study English.", "read": "I read a book.", "write": "I write my name.",
    "listen": "Listen carefully.", "speak": "Please speak slowly.", "help": "Can you help me?", "wait": "Please wait.",

    "happy": "I am happy.", "sad": "I am sad.", "angry": "I am angry.", "tired": "I am tired.",
    "hungry": "I am hungry.", "thirsty": "I am thirsty.", "sick": "I am sick.", "okay": "I am okay.",
    "fine": "I am fine.", "cold": "I am cold.", "hot": "It is hot.", "pain": "I have pain.",
    "headache": "I have a headache.", "stomachache": "I have a stomachache.", "fever": "I have a fever.",
    "hurt": "My leg hurts.", "good": "It is good.", "bad": "It is bad.", "worried": "I am worried.",
    "scared": "I am scared.",

    "food": "I need food.", "water": "I need water.", "rice": "I eat rice.", "bread": "I eat bread.",
    "milk": "I drink milk.", "juice": "I drink juice.", "coffee": "I drink coffee.", "tea": "I drink tea.",
    "apple": "I like apples.", "banana": "I like bananas.", "egg": "I eat an egg.", "meat": "I eat meat.",
    "chicken": "I like chicken.", "fish": "I eat fish.", "breakfast": "I eat breakfast.", "lunch": "I eat lunch.",
    "dinner": "I eat dinner.", "snack": "I want a snack.", "medicine": "I need medicine.", "hospital": "I need a hospital.",

    "home": "I go home.", "school": "I go to school.", "classroom": "This is my classroom.",
    "bathroom": "Where is the bathroom?", "store": "I go to the store.", "station": "Where is the station?",
    "bus": "I take a bus.", "car": "This is my car.", "taxi": "I need a taxi.", "train": "I take a train.",
    "bike": "I ride a bike.", "road": "This road is long.", "street": "This street is busy.",
    "here": "Come here.", "there": "Go there.", "near": "It is near here.", "far": "It is far.",
    "left": "Turn left.", "right": "Turn right.",

    "time": "What time is it?", "now": "I am here now.", "today": "Today is Monday.",
    "tomorrow": "See you tomorrow.", "yesterday": "I studied yesterday.", "morning": "Good morning.",
    "afternoon": "Good afternoon.", "evening": "Good evening.", "night": "Good night.",
    "early": "It is early.", "late": "It is late.", "one": "I have one book.", "two": "I have two books.",
    "three": "I have three books.", "four": "I have four books.", "five": "I have five books.",
    "six": "I have six books.", "seven": "I have seven books.", "eight": "I have eight books.",
    "nine": "I have nine books.", "ten": "I have ten books.",

    "bag": "This is my bag.", "phone": "This is my phone.", "book": "This is my book.",
    "notebook": "This is my notebook.", "pen": "I have a pen.", "pencil": "I have a pencil.",
    "desk": "This is my desk.", "chair": "This is my chair.", "door": "Open the door.",
    "window": "Close the window.", "key": "I need a key.", "money": "I need money.",
    "card": "I have a card.", "ticket": "I need a ticket.", "clothes": "These are my clothes.",
    "shoes": "These are my shoes.", "hat": "This is my hat.", "watch": "This is my watch.",
    "cup": "This is my cup.", "bottle": "This is my bottle.",

    "please": "Please help me.", "sorry": "I am sorry.", "excuse me": "Excuse me.",
    "again": "Please say it again.", "slowly": "Please speak slowly.", "understand": "I understand.",
    "question": "I have a question.", "problem": "I have a problem.", "need": "I need help.",
    "want": "I want water.", "know": "I know.", "say": "Please say it again.",
    "tell": "Please tell me.", "ask": "Can I ask you?", "answer": "This is the answer.",
    "repeat": "Please repeat.", "look": "Look at this.",
}

CASSETTE_EXAMPLES_KO = {
    "I": "나는 학생입니다.", "you": "너는 나의 친구입니다.", "he": "그는 나의 친구입니다.", "she": "그녀는 학생입니다.",
    "we": "우리는 행복합니다.", "they": "그들은 학생들입니다.", "friend": "그는 나의 친구입니다.", "teacher": "그녀는 나의 선생님입니다.",
    "student": "나는 학생입니다.", "classmate": "그는 나의 반 친구입니다.", "family": "이것은 나의 가족입니다.",
    "father": "그는 나의 아버지입니다.", "mother": "그녀는 나의 어머니입니다.", "brother": "그는 나의 남자 형제입니다.",
    "sister": "그녀는 나의 여자 형제입니다.", "name": "내 이름은 Alex입니다.", "person": "그는 좋은 사람입니다.",
    "man": "그는 남자입니다.", "woman": "그녀는 여자입니다.", "child": "그는 아이입니다.",

    "go": "나는 학교에 갑니다.", "come": "이리 와 주세요.", "walk": "나는 걸어서 학교에 갑니다.", "run": "나는 달릴 수 있습니다.",
    "sit": "앉아 주세요.", "stand": "일어나 주세요.", "stop": "멈춰 주세요.", "start": "시작합시다.",
    "open": "문을 여세요.", "close": "문을 닫으세요.", "eat": "나는 점심을 먹습니다.", "drink": "나는 물을 마십니다.",
    "sleep": "나는 밤에 잡니다.", "study": "나는 영어를 공부합니다.", "read": "나는 책을 읽습니다.", "write": "나는 내 이름을 씁니다.",
    "listen": "주의 깊게 들으세요.", "speak": "천천히 말해 주세요.", "help": "나를 도와줄 수 있나요?", "wait": "기다려 주세요.",

    "happy": "나는 행복합니다.", "sad": "나는 슬픕니다.", "angry": "나는 화가 났습니다.", "tired": "나는 피곤합니다.",
    "hungry": "나는 배고픕니다.", "thirsty": "나는 목마릅니다.", "sick": "나는 아픕니다.", "okay": "나는 괜찮습니다.",
    "fine": "나는 괜찮습니다.", "cold": "나는 춥습니다.", "hot": "날씨가 덥습니다.", "pain": "나는 통증이 있습니다.",
    "headache": "나는 두통이 있습니다.", "stomachache": "나는 복통이 있습니다.", "fever": "나는 열이 있습니다.",
    "hurt": "내 다리가 아픕니다.", "good": "그것은 좋습니다.", "bad": "그것은 나쁩니다.", "worried": "나는 걱정됩니다.",
    "scared": "나는 무섭습니다.",

    "food": "나는 음식이 필요합니다.", "water": "나는 물이 필요합니다.", "rice": "나는 밥을 먹습니다.", "bread": "나는 빵을 먹습니다.",
    "milk": "나는 우유를 마십니다.", "juice": "나는 주스를 마십니다.", "coffee": "나는 커피를 마십니다.", "tea": "나는 차를 마십니다.",
    "apple": "나는 사과를 좋아합니다.", "banana": "나는 바나나를 좋아합니다.", "egg": "나는 달걀 하나를 먹습니다.",
    "meat": "나는 고기를 먹습니다.", "chicken": "나는 닭고기를 좋아합니다.", "fish": "나는 생선을 먹습니다.",
    "breakfast": "나는 아침 식사를 먹습니다.", "lunch": "나는 점심을 먹습니다.", "dinner": "나는 저녁을 먹습니다.",
    "snack": "나는 간식을 원합니다.", "medicine": "나는 약이 필요합니다.", "hospital": "나는 병원이 필요합니다.",

    "home": "나는 집에 갑니다.", "school": "나는 학교에 갑니다.", "classroom": "여기는 나의 교실입니다.",
    "bathroom": "화장실이 어디에 있나요?", "store": "나는 가게에 갑니다.", "station": "역은 어디에 있나요?",
    "bus": "나는 버스를 탑니다.", "car": "이것은 나의 차입니다.", "taxi": "나는 택시가 필요합니다.",
    "train": "나는 기차를 탑니다.", "bike": "나는 자전거를 탑니다.", "road": "이 도로는 깁니다.",
    "street": "이 거리는 붐빕니다.", "here": "여기로 오세요.", "there": "그곳으로 가세요.",
    "near": "그것은 여기 근처에 있습니다.", "far": "그것은 멉니다.", "left": "왼쪽으로 도세요.", "right": "오른쪽으로 도세요.",

    "time": "지금 몇 시인가요?", "now": "나는 지금 여기에 있습니다.", "today": "오늘은 월요일입니다.",
    "tomorrow": "내일 봅시다.", "yesterday": "나는 어제 공부했습니다.", "morning": "좋은 아침입니다.",
    "afternoon": "좋은 오후입니다.", "evening": "좋은 저녁입니다.", "night": "안녕히 주무세요.",
    "early": "이릅니다.", "late": "늦었습니다.", "one": "나는 책 한 권이 있습니다.",
    "two": "나는 책 두 권이 있습니다.", "three": "나는 책 세 권이 있습니다.", "four": "나는 책 네 권이 있습니다.",
    "five": "나는 책 다섯 권이 있습니다.", "six": "나는 책 여섯 권이 있습니다.", "seven": "나는 책 일곱 권이 있습니다.",
    "eight": "나는 책 여덟 권이 있습니다.", "nine": "나는 책 아홉 권이 있습니다.", "ten": "나는 책 열 권이 있습니다.",

    "bag": "이것은 나의 가방입니다.", "phone": "이것은 나의 전화기입니다.", "book": "이것은 나의 책입니다.",
    "notebook": "이것은 나의 공책입니다.", "pen": "나는 펜이 있습니다.", "pencil": "나는 연필이 있습니다.",
    "desk": "이것은 나의 책상입니다.", "chair": "이것은 나의 의자입니다.", "door": "문을 여세요.",
    "window": "창문을 닫으세요.", "key": "나는 열쇠가 필요합니다.", "money": "나는 돈이 필요합니다.",
    "card": "나는 카드가 있습니다.", "ticket": "나는 표가 필요합니다.", "clothes": "이것들은 나의 옷입니다.",
    "shoes": "이것들은 나의 신발입니다.", "hat": "이것은 나의 모자입니다.", "watch": "이것은 나의 시계입니다.",
    "cup": "이것은 나의 컵입니다.", "bottle": "이것은 나의 병입니다.",

    "please": "제발 나를 도와주세요.", "sorry": "미안합니다.", "excuse me": "실례합니다.",
    "again": "다시 말해 주세요.", "slowly": "천천히 말해 주세요.", "understand": "나는 이해합니다.",
    "question": "나는 질문이 있습니다.", "problem": "나는 문제가 있습니다.", "need": "나는 도움이 필요합니다.",
    "want": "나는 물을 원합니다.", "know": "나는 압니다.", "say": "다시 말해 주세요.",
    "tell": "나에게 말해 주세요.", "ask": "질문해도 될까요?", "answer": "이것이 답입니다.",
    "repeat": "반복해 주세요.", "look": "이것을 보세요.",
}

# =========================
# 단어별 이모지
# =========================
WORD_EMOJIS = {
    "I": "🙋", "you": "👉", "he": "👦", "she": "👧", "we": "👥", "they": "👥",
    "friend": "🤝", "teacher": "👩‍🏫", "student": "🧑‍🎓", "classmate": "👫", "family": "👨‍👩‍👧",
    "father": "👨", "mother": "👩", "brother": "👦", "sister": "👧", "name": "🏷️",
    "person": "🧍", "man": "👨", "woman": "👩", "child": "🧒",
    "go": "➡️", "come": "⬅️", "walk": "🚶", "run": "🏃", "sit": "🪑", "stand": "🧍",
    "stop": "🛑", "start": "▶️", "open": "📂", "close": "📕", "eat": "🍽️", "drink": "🥤",
    "sleep": "😴", "study": "📚", "read": "📖", "write": "✏️", "listen": "👂", "speak": "🗣️",
    "help": "🆘", "wait": "⏳",
    "happy": "😊", "sad": "😢", "angry": "😠", "tired": "🥱", "hungry": "😋", "thirsty": "🥤",
    "sick": "🤒", "okay": "👌", "fine": "🙂", "cold": "🥶", "hot": "🥵", "pain": "🤕",
    "headache": "🤯", "stomachache": "🤢", "fever": "🌡️", "hurt": "🩹", "good": "👍", "bad": "👎",
    "worried": "😟", "scared": "😨",
    "food": "🍽️", "water": "💧", "rice": "🍚", "bread": "🍞", "milk": "🥛", "juice": "🧃",
    "coffee": "☕", "tea": "🍵", "apple": "🍎", "banana": "🍌", "egg": "🥚", "meat": "🥩",
    "chicken": "🍗", "fish": "🐟", "breakfast": "🍳", "lunch": "🍱", "dinner": "🍽️", "snack": "🍪",
    "medicine": "💊", "hospital": "🏥",
    "home": "🏠", "school": "🏫", "classroom": "🧑‍🏫", "bathroom": "🚻", "store": "🏪", "station": "🚉",
    "bus": "🚌", "car": "🚗", "taxi": "🚕", "train": "🚆", "bike": "🚲", "road": "🛣️",
    "street": "🏙️", "here": "📍", "there": "📌", "near": "↔️", "far": "🌁", "left": "⬅️", "right": "➡️",
    "time": "⏰", "now": "🕒", "today": "📅", "tomorrow": "➡️📅", "yesterday": "⬅️📅",
    "morning": "🌅", "afternoon": "☀️", "evening": "🌆", "night": "🌙", "early": "🐓", "late": "🌃",
    "one": "1️⃣", "two": "2️⃣", "three": "3️⃣", "four": "4️⃣", "five": "5️⃣", "six": "6️⃣",
    "seven": "7️⃣", "eight": "8️⃣", "nine": "9️⃣", "ten": "🔟",
    "bag": "🎒", "phone": "📱", "book": "📘", "notebook": "📓", "pen": "🖊️", "pencil": "✏️",
    "desk": "🪑", "chair": "🪑", "door": "🚪", "window": "🪟", "key": "🔑", "money": "💵",
    "card": "💳", "ticket": "🎫", "clothes": "👕", "shoes": "👟", "hat": "🧢", "watch": "⌚",
    "cup": "☕", "bottle": "🍼",
    "please": "🙏", "sorry": "🙇", "excuse me": "🙋", "again": "🔁", "slowly": "🐢",
    "understand": "💡", "question": "❓", "problem": "⚠️", "need": "📌", "want": "✨",
    "know": "🧠", "say": "💬", "tell": "📣", "ask": "❔", "answer": "✅",
    "repeat": "🔁", "look": "👀",
}


def get_word_emoji(word):
    return WORD_EMOJIS.get(word, "🌱")


# =========================
# 단어·대화 오디오 - 일상 400과 같은 안전한 st.audio 방식
# =========================
def audio_button(label, text, key=None):
    # 단어별 듣기: 화면에 플레이어가 뜨지 않고 버튼 클릭 즉시 재생됩니다.
    instant_audio_button(label, text, key=key, height=48)


def html_dialogue_audio_player(label, dialogue_lines, line_pause_ms=1400, height=105):
    # 대화 듣기도 같은 방식으로, 플레이어 없이 버튼 클릭 즉시 재생합니다.
    dialogue_text = make_dialogue_tts_text(dialogue_lines)
    instant_audio_button(
        label,
        dialogue_text,
        key="dialogue_" + hashlib.md5(dialogue_text.encode("utf-8")).hexdigest(),
        height=50
    )


# =========================
# 오늘의 생존 대화
# =========================
theme_dialogues = {
    "🧍 나와 사람": [
        {"en": "A: Hello. What is your name?", "ko": "A: 안녕. 네 이름은 뭐니?"},
        {"en": "B: My name is Alex.", "ko": "B: 내 이름은 Alex야."},
        {"en": "A: Are you a student?", "ko": "A: 너는 학생이니?"},
        {"en": "B: Yes, I am a student.", "ko": "B: 응, 나는 학생이야."},
        {"en": "A: Is he your friend?", "ko": "A: 그는 네 친구니?"},
        {"en": "B: Yes, he is my friend.", "ko": "B: 응, 그는 내 친구야."},
    ],
    "🏃 기본 동작": [
        {"en": "A: Can you come here?", "ko": "A: 여기로 올 수 있니?"},
        {"en": "B: Yes, I can come.", "ko": "B: 응, 갈 수 있어."},
        {"en": "A: Please sit down.", "ko": "A: 앉아 주세요."},
        {"en": "B: Okay. I will sit down.", "ko": "B: 좋아요. 앉을게요."},
        {"en": "A: Can you help me?", "ko": "A: 나를 도와줄 수 있니?"},
        {"en": "B: Yes, I can help you.", "ko": "B: 응, 도와줄 수 있어."},
    ],
    "💖 감정·몸 상태": [
        {"en": "A: Are you okay?", "ko": "A: 너 괜찮니?"},
        {"en": "B: No, I am tired.", "ko": "B: 아니, 나는 피곤해."},
        {"en": "A: Are you hungry?", "ko": "A: 너 배고프니?"},
        {"en": "B: Yes, I am hungry.", "ko": "B: 응, 나는 배고파."},
        {"en": "A: Are you sick?", "ko": "A: 너 아프니?"},
        {"en": "B: Yes, I am sick.", "ko": "B: 응, 나는 아파."},
    ],
    "🍎 음식·물": [
        {"en": "A: Are you thirsty?", "ko": "A: 너 목마르니?"},
        {"en": "B: Yes, I need water.", "ko": "B: 응, 나는 물이 필요해."},
        {"en": "A: Do you want food?", "ko": "A: 음식이 필요하니?"},
        {"en": "B: Yes, I want food.", "ko": "B: 응, 나는 음식이 필요해."},
        {"en": "A: Do you like apples?", "ko": "A: 너는 사과를 좋아하니?"},
        {"en": "B: Yes, I like apples.", "ko": "B: 응, 나는 사과를 좋아해."},
    ],
    "🚗 장소·이동": [
        {"en": "A: Where is the bathroom?", "ko": "A: 화장실은 어디에 있나요?"},
        {"en": "B: It is near here.", "ko": "B: 여기 근처에 있어요."},
        {"en": "A: I want to go home.", "ko": "A: 나는 집에 가고 싶어요."},
        {"en": "B: You can go by bus.", "ko": "B: 버스로 갈 수 있어요."},
        {"en": "A: Where is the station?", "ko": "A: 역은 어디에 있나요?"},
        {"en": "B: It is not far.", "ko": "B: 멀지 않아요."},
    ],
    "⏰ 시간·숫자": [
        {"en": "A: What time is it?", "ko": "A: 지금 몇 시니?"},
        {"en": "B: It is three.", "ko": "B: 3시야."},
        {"en": "A: Is it morning?", "ko": "A: 아침이니?"},
        {"en": "B: No, it is afternoon.", "ko": "B: 아니, 오후야."},
        {"en": "A: Do you study today?", "ko": "A: 너는 오늘 공부하니?"},
        {"en": "B: Yes, I study today.", "ko": "B: 응, 나는 오늘 공부해."},
    ],
    "🎒 물건·돈": [
        {"en": "A: Where is my phone?", "ko": "A: 내 전화기는 어디에 있니?"},
        {"en": "B: It is in your bag.", "ko": "B: 네 가방 안에 있어."},
        {"en": "A: Do you have money?", "ko": "A: 너 돈 있니?"},
        {"en": "B: No, I do not have money.", "ko": "B: 아니, 돈이 없어."},
        {"en": "A: Is this your book?", "ko": "A: 이것은 네 책이니?"},
        {"en": "B: Yes, it is my book.", "ko": "B: 응, 그것은 내 책이야."},
    ],
    "🆘 도움 요청": [
        {"en": "A: Excuse me.", "ko": "A: 실례합니다."},
        {"en": "B: Yes?", "ko": "B: 네?"},
        {"en": "A: I don't understand.", "ko": "A: 이해하지 못했어요."},
        {"en": "B: Okay. I will say it again.", "ko": "B: 알겠어요. 다시 말할게요."},
        {"en": "A: Please speak slowly.", "ko": "A: 천천히 말해 주세요."},
        {"en": "B: Sure. I can help you.", "ko": "B: 물론이죠. 도와줄 수 있어요."},
    ],
}



# =========================
# 복습 희망 저장 기능
# =========================
if "unknown_words" not in st.session_state:
    st.session_state.unknown_words = []

if "unknown_word_info" not in st.session_state:
    st.session_state.unknown_word_info = {}


def add_unknown_word(word, meaning, theme_name):
    if word not in st.session_state.unknown_words:
        st.session_state.unknown_words.append(word)

    st.session_state.unknown_word_info[word] = {
        "meaning": meaning,
        "theme": theme_name,
    }


def remove_unknown_word(word):
    if word in st.session_state.unknown_words:
        st.session_state.unknown_words.remove(word)

    if word in st.session_state.unknown_word_info:
        del st.session_state.unknown_word_info[word]



def clear_review_checkbox_keys():
    """
    복습 희망 전체 삭제 후에도 체크박스 key 상태가 남아 있으면
    다시 체크해도 목록에 들어가지 않는 문제가 생깁니다.
    따라서 전체 삭제 시 체크박스 key까지 함께 삭제합니다.
    """
    keys_to_delete = [
        key for key in list(st.session_state.keys())
        if "_unknown_" in str(key)
    ]

    for key in keys_to_delete:
        del st.session_state[key]


def toggle_unknown_word(word, meaning, theme_name):
    if word in st.session_state.unknown_words:
        remove_unknown_word(word)
    else:
        add_unknown_word(word, meaning, theme_name)


# =========================
# 카세트 듣기 - 일상 400과 같은 단어별 mp3 순차 재생 방식
# =========================
def get_example_sentence(word):
    return CASSETTE_EXAMPLES.get(word, f"This is {word}.")


def get_example_sentence_ko(word):
    return CASSETTE_EXAMPLES_KO.get(word, "이 단어를 사용한 생존 영어 문장입니다.")


def flatten_survival_words():
    all_items = []
    number = 1
    for theme_name, theme_words in word_themes.items():
        for item in theme_words:
            word = item["word"]
            all_items.append({
                "number": number,
                "theme": theme_name,
                "word": word,
                "meaning": get_display_meaning(word, item["meaning"]),
                "emoji": get_word_emoji(word),
            })
            number += 1
    return all_items


def make_theme_cassette_items(theme_words, theme_name):
    theme_items = []
    for idx, item in enumerate(theme_words, start=1):
        word = item["word"]
        theme_items.append({
            "number": idx,
            "theme": theme_name,
            "word": word,
            "meaning": item["meaning"],
            "emoji": get_word_emoji(word),
        })
    return theme_items


def make_cassette_text(items, repeat_word=2):
    parts = []
    for item in items:
        word = item["word"]
        parts.append(". ".join([word] * repeat_word) + ".")
    return " ".join(parts)


def js_cassette_visual_player(items, audio_payloads, title="📼 단어 카세트", height=560):
    """
    일상 400과 같은 형태의 카세트입니다.
    남기는 기능:
    - 재생/멈춤 버튼 1개
    - 이전
    - 다음
    - 속도 선택
    - 전체 반복 선택
    """
    player_id = "survival_cassette_" + uuid.uuid4().hex

    visual_items = []
    for idx, (item, audio_b64) in enumerate(zip(items, audio_payloads), start=1):
        visual_items.append({
            "number": item.get("number", idx),
            "theme": str(item.get("theme", "")),
            "word": str(item.get("word", "")),
            "meaning": str(item.get("meaning", "")),
            "emoji": get_word_emoji(item.get("word", "")),
            "src": "data:audio/mp3;base64," + audio_b64,
        })

    items_json = json.dumps(visual_items, ensure_ascii=False)

    components.html(
        f"""
        <div id="{player_id}" style="
            font-family: Arial, sans-serif;
            width:100%;
            box-sizing:border-box;
            border-radius:28px;
            padding:14px;
            background:linear-gradient(135deg,#f0fdf4 0%,#eff6ff 48%,#fff7ed 100%);
            border:1px solid #bbf7d0;
            box-shadow:0 8px 22px rgba(15,23,42,0.10);
            overflow:hidden;
        ">
            <div style="display:flex; justify-content:flex-end; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
                <div id="count_{player_id}" style="font-size:13px; font-weight:900; color:#475569; background:rgba(255,255,255,.8); border:1px solid #dcfce7; border-radius:999px; padding:7px 12px;">1 / {len(visual_items)}</div>
            </div>

            <audio id="audio_{player_id}" preload="auto" style="width:100%; margin:6px 0 14px 0;"></audio>

            <div style="display:grid; grid-template-columns:1fr; gap:12px;">
                <div style="
                    background:rgba(255,255,255,0.88);
                    border:1px solid #dcfce7;
                    border-radius:26px;
                    padding:16px 14px;
                    text-align:center;
                ">
                    <div id="theme_{player_id}" style="display:inline-block; font-size:13px; font-weight:900; color:#15803d; background:#dcfce7; border-radius:999px; padding:6px 12px; margin-bottom:10px;">Theme</div>
                    <div id="emoji_{player_id}" style="font-size:46px; line-height:1.05; margin:2px 0;">🛟</div>
                    <div id="word_{player_id}" style="font-size:clamp(36px,7.8vw,62px); font-weight:1000; color:#111827; line-height:1.05; word-break:break-word; letter-spacing:-1px;">Ready</div>
                    <div id="meaning_{player_id}" style="font-size:clamp(20px,4.4vw,30px); font-weight:900; color:#334155; margin-top:10px; word-break:keep-all;">재생 버튼을 눌러 주세요.</div>
                    <div style="width:100%; height:14px; background:#e2e8f0; border-radius:999px; overflow:hidden; margin-top:12px;">
                        <div id="bar_{player_id}" style="height:100%; width:0%; background:linear-gradient(90deg,#22c55e,#0ea5e9,#8b5cf6); border-radius:999px;"></div>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns:1fr; gap:8px;">
                    <button id="play_{player_id}" style="min-height:38px; border-radius:13px; border:1px solid #86efac; background:linear-gradient(135deg,#dcfce7,#dbeafe); font-size:13px; font-weight:900; cursor:pointer; box-shadow:0 3px 9px rgba(15,23,42,0.08);">▶️ 재생</button>
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                    <button id="prev_{player_id}" style="min-height:38px; border-radius:13px; border:1px solid #cbd5e1; background:#f8fafc; color:#334155; font-size:13px; font-weight:900; cursor:pointer;">⏮ 이전</button>
                    <button id="next_{player_id}" style="min-height:38px; border-radius:13px; border:1px solid #cbd5e1; background:#f8fafc; color:#334155; font-size:13px; font-weight:900; cursor:pointer;">다음 ⏭</button>
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                    <div style="background:rgba(255,255,255,0.88); border:1px solid #dcfce7; border-radius:16px; padding:9px 11px;">
                        <div style="font-size:12px; font-weight:900; color:#64748b; margin-bottom:4px;">속도</div>
                        <select id="speed_{player_id}" style="width:100%; border:0; background:transparent; font-size:14px; font-weight:900; color:#0f172a; outline:none;">
                            <option value="0.75">천천히</option>
                            <option value="1" selected>보통</option>
                            <option value="1.15">조금 빠르게</option>
                            <option value="1.3">빠르게</option>
                        </select>
                    </div>
                    <div style="background:rgba(255,255,255,0.88); border:1px solid #dcfce7; border-radius:16px; padding:9px 11px;">
                        <div style="font-size:12px; font-weight:900; color:#64748b; margin-bottom:4px;">전체 반복</div>
                        <select id="loop_{player_id}" style="width:100%; border:0; background:transparent; font-size:14px; font-weight:900; color:#0f172a; outline:none;">
                            <option value="1" selected>1번</option>
                            <option value="2">2번</option>
                            <option value="3">3번</option>
                        </select>
                    </div>
                </div>

                <div id="status_{player_id}" style="font-size:14px; font-weight:900; color:#075985; min-height:22px;">준비 완료</div>
            </div>
        </div>

        <script>
        const items_{player_id} = {items_json};
        const audio_{player_id} = document.getElementById("audio_{player_id}");
        const wordEl_{player_id} = document.getElementById("word_{player_id}");
        const meaningEl_{player_id} = document.getElementById("meaning_{player_id}");
        const emojiEl_{player_id} = document.getElementById("emoji_{player_id}");
        const themeEl_{player_id} = document.getElementById("theme_{player_id}");
        const countEl_{player_id} = document.getElementById("count_{player_id}");
        const barEl_{player_id} = document.getElementById("bar_{player_id}");
        const statusEl_{player_id} = document.getElementById("status_{player_id}");
        const playBtn_{player_id} = document.getElementById("play_{player_id}");
        const prevBtn_{player_id} = document.getElementById("prev_{player_id}");
        const nextBtn_{player_id} = document.getElementById("next_{player_id}");
        const speedSelect_{player_id} = document.getElementById("speed_{player_id}");
        const loopSelect_{player_id} = document.getElementById("loop_{player_id}");

        let currentIndex_{player_id} = 0;
        let currentLoop_{player_id} = 1;
        let isPlayingList_{player_id} = false;
        let isFinished_{player_id} = false;

        function setCurrent_{player_id}(idx) {{
            if (!items_{player_id}.length) return;
            idx = Math.max(0, Math.min(idx, items_{player_id}.length - 1));
            currentIndex_{player_id} = idx;
            const it = items_{player_id}[idx];

            wordEl_{player_id}.textContent = it.word;
            meaningEl_{player_id}.textContent = it.meaning;
            emojiEl_{player_id}.textContent = it.emoji;
            themeEl_{player_id}.textContent = it.theme || "Survival English";
            countEl_{player_id}.textContent = (idx + 1) + " / " + items_{player_id}.length + " · " + currentLoop_{player_id} + "회차";

            const percent = items_{player_id}.length <= 1 ? 100 : (idx / (items_{player_id}.length - 1)) * 100;
            barEl_{player_id}.style.width = percent + "%";
        }}

        function loadCurrent_{player_id}() {{
            const it = items_{player_id}[currentIndex_{player_id}];
            setCurrent_{player_id}(currentIndex_{player_id});
            if (audio_{player_id}.src !== it.src) {{
                audio_{player_id}.src = it.src;
                audio_{player_id}.load();
            }}
            audio_{player_id}.playbackRate = parseFloat(speedSelect_{player_id}.value || "1");
        }}

        function playCurrent_{player_id}() {{
            if (!items_{player_id}.length) return;
            isPlayingList_{player_id} = true;
            isFinished_{player_id} = false;
            loadCurrent_{player_id}();
            playBtn_{player_id}.textContent = "⏸ 멈춤";
            statusEl_{player_id}.textContent = "현재 단어: " + items_{player_id}[currentIndex_{player_id}].word;
            audio_{player_id}.play().catch(() => {{
                statusEl_{player_id}.textContent = "브라우저가 자동 재생을 막았습니다. 재생 버튼을 한 번 더 눌러 주세요.";
                playBtn_{player_id}.textContent = "▶️ 재생";
            }});
        }}

        function pauseCurrent_{player_id}() {{
            isPlayingList_{player_id} = false;
            audio_{player_id}.pause();
            playBtn_{player_id}.textContent = "▶️ 이어 듣기";
            statusEl_{player_id}.textContent = "일시정지";
        }}

        function moveTo_{player_id}(idx, autoPlay=false) {{
            isPlayingList_{player_id} = autoPlay;
            isFinished_{player_id} = false;
            audio_{player_id}.pause();
            currentIndex_{player_id} = Math.max(0, Math.min(idx, items_{player_id}.length - 1));
            loadCurrent_{player_id}();
            if (autoPlay) {{
                playCurrent_{player_id}();
            }} else {{
                playBtn_{player_id}.textContent = "▶️ 재생";
                statusEl_{player_id}.textContent = "선택된 단어: " + items_{player_id}[currentIndex_{player_id}].word;
            }}
        }}

        loadCurrent_{player_id}();

        speedSelect_{player_id}.addEventListener("change", function() {{
            audio_{player_id}.playbackRate = parseFloat(speedSelect_{player_id}.value || "1");
        }});

        playBtn_{player_id}.addEventListener("click", function() {{
            if (isPlayingList_{player_id}) {{
                pauseCurrent_{player_id}();
            }} else {{
                if (isFinished_{player_id}) {{
                    currentIndex_{player_id} = 0;
                    currentLoop_{player_id} = 1;
                    isFinished_{player_id} = false;
                }}
                playCurrent_{player_id}();
            }}
        }});

        prevBtn_{player_id}.addEventListener("click", function() {{
            moveTo_{player_id}(currentIndex_{player_id} - 1, false);
        }});

        nextBtn_{player_id}.addEventListener("click", function() {{
            moveTo_{player_id}(currentIndex_{player_id} + 1, false);
        }});

        audio_{player_id}.addEventListener("ended", function() {{
            if (!isPlayingList_{player_id}) return;
            const maxLoop = parseInt(loopSelect_{player_id}.value || "1");
            if (currentIndex_{player_id} < items_{player_id}.length - 1) {{
                currentIndex_{player_id} += 1;
                playCurrent_{player_id}();
            }} else if (currentLoop_{player_id} < maxLoop) {{
                currentLoop_{player_id} += 1;
                currentIndex_{player_id} = 0;
                playCurrent_{player_id}();
            }} else {{
                isPlayingList_{player_id} = false;
                isFinished_{player_id} = true;
                playBtn_{player_id}.textContent = "▶️ 처음부터 다시";
                statusEl_{player_id}.textContent = "✅ 카세트 재생 완료";
                barEl_{player_id}.style.width = "100%";
            }}
        }});
        </script>
        """,
        height=height,
        scrolling=True
    )


def show_cassette_audio(items, title):
    repeat_word = st.selectbox(
        "단어 반복 횟수",
        [1, 2, 3],
        index=1,
        key=f"repeat_{title}"
    )

    # 버튼을 누른 뒤 카세트를 생성하는 방식이 아니라,
    # 테마 화면에 들어오면 바로 카세트가 보이도록 합니다.
    cassette_title = "🎧 전체 단어 듣기" if title == "전체 단어" else "🎧 테마별 전체 단어 듣기"
    st.markdown(
        f"<div style='font-size:20px; font-weight:1000; color:#0f172a; margin:8px 0 10px 0;'>{cassette_title}</div>",
        unsafe_allow_html=True
    )

    try:
        with st.spinner("단어별 카세트 음성을 준비하는 중입니다. 처음 한 번은 조금 걸릴 수 있습니다."):
            audio_payloads = []
            for item in items:
                word = str(item["word"]).strip()
                tts_text = ". ".join([word] * repeat_word) + "."
                audio_bytes = get_tts_mp3_bytes(tts_text, lang="en")
                audio_payloads.append(base64.b64encode(audio_bytes).decode("utf-8"))

        js_cassette_visual_player(
            items=items,
            audio_payloads=audio_payloads,
            title=cassette_title,
            height=560
        )
    except Exception as e:
        st.error("카세트 음성을 만들지 못했습니다. requirements.txt에 requests가 있는지 확인해 주세요.")
        st.caption(f"오류 내용: {e}")


def show_all_cassette_tab():
    all_items = flatten_survival_words()
    show_cassette_audio(all_items, "전체 단어")


def show_cassette_player(theme_words, theme_name):
    theme_items = make_theme_cassette_items(theme_words, theme_name)
    show_cassette_audio(theme_items, theme_name)


# =========================
# 전체 뜻 목록 만들기
# =========================
all_words = []
for theme_words in word_themes.values():
    all_words.extend(theme_words)


def get_all_display_meanings():
    return [
        get_display_meaning(item["word"], item["meaning"])
        for item in all_words
    ]


# =========================
# 보기 고정 랜덤 섞기
# =========================
def get_shuffled_options(theme_name, index, options):
    key = f"{theme_name}_options_{index}"

    if key not in st.session_state:
        shuffled = options[:]
        random.seed(f"{theme_name}_{index}")
        random.shuffle(shuffled)
        st.session_state[key] = shuffled

    return st.session_state[key]


# =========================
# 퀴즈 문항 만들기
# =========================
def make_quiz_items(theme_words, theme_name):
    quiz_items = []
    display_meanings = get_all_display_meanings()

    for idx, item in enumerate(theme_words):
        word = item["word"]
        correct = get_display_meaning(word, item["meaning"])
        distractors = [m for m in display_meanings if m != correct]
        random.seed(f"{theme_name}_{word}_{idx}")
        wrong_options = random.sample(distractors, 3)

        options = [correct] + wrong_options

        quiz_items.append({
            "word": word,
            "answer": correct,
            "options": options
        })

    return quiz_items


# =========================
# 상태 초기화
# =========================
def init_state(theme_name):
    if f"{theme_name}_submitted1" not in st.session_state:
        st.session_state[f"{theme_name}_submitted1"] = False

    if f"{theme_name}_submitted2" not in st.session_state:
        st.session_state[f"{theme_name}_submitted2"] = False

    if f"{theme_name}_wrong" not in st.session_state:
        st.session_state[f"{theme_name}_wrong"] = []


def reset_theme(theme_name):
    keys_to_delete = []

    for key in st.session_state.keys():
        if key.startswith(theme_name):
            keys_to_delete.append(key)

    for key in keys_to_delete:
        del st.session_state[key]


# =========================
# 오늘의 생존 대화 보여주기
# =========================
def show_dialogue(theme_name):
    dialogue = theme_dialogues.get(theme_name, [])

    if not dialogue:
        return

    st.markdown('<div class="dialogue-box">', unsafe_allow_html=True)
    st.markdown('<div class="dialogue-title">💬 오늘의 생존 대화</div>', unsafe_allow_html=True)

    for line in dialogue:
        st.markdown(
            f"<div class='dialogue-line'>{line['en']}</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='dialogue-meaning'>{line['ko']}</div>",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    html_dialogue_audio_player(
        label="🔊 대화 듣기",
        dialogue_lines=dialogue,
        line_pause_ms=1400,
        height=105
    )



# =========================
# 단어 익히기
# =========================
def show_word_cards(theme_words, theme_name):
    for idx, item in enumerate(theme_words):
        word = item["word"]
        meaning = get_display_meaning(word, item["meaning"])
        checked = word in st.session_state.unknown_words
        checkbox_key = f"{theme_name}_unknown_{idx}_{word}"

        st.markdown('<div class="word-card">', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns([1.25, 1.05, 0.35, 1.65, 1.25])

        with col1:
            st.markdown(
                f"""
                <div class="word-row">
                    <div class="word-number">{idx + 1}</div>
                    <div class="word-text">{word}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div class='meaning-text'>{meaning}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div class='emoji-text'>{get_word_emoji(word)}</div>",
                unsafe_allow_html=True
            )

        with col4:
            audio_button(
                "🔊 듣기",
                word,
                key=f"{theme_name}_learn_audio_{idx}"
            )

        with col5:
            review_checked = st.checkbox(
                "복습 희망",
                value=checked,
                key=checkbox_key
            )

            # 체크박스 화면 상태와 실제 복습 희망 목록을 매번 동기화합니다.
            # 이렇게 해야 전체 삭제 후 다시 체크해도 바로 목록에 들어갑니다.
            if review_checked and word not in st.session_state.unknown_words:
                add_unknown_word(word, meaning, theme_name)
            elif not review_checked and word in st.session_state.unknown_words:
                remove_unknown_word(word)

        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 퀴즈 풀기
# =========================
def show_quiz(theme_words, theme_name):
    init_state(theme_name)

    quiz_items = make_quiz_items(theme_words, theme_name)

    submitted1_key = f"{theme_name}_submitted1"
    submitted2_key = f"{theme_name}_submitted2"
    wrong_key = f"{theme_name}_wrong"

    if not st.session_state[submitted1_key]:
        st.markdown("### 🧸 1차 퀴즈")
        st.write("영어 단어를 보고 선택한 언어의 알맞은 뜻을 고르세요.")

        for i, q in enumerate(quiz_items):
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)

            st.markdown(f"<div class='quiz-number'>🌟 Question {i + 1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='quiz-word'>{q['word']}</div>", unsafe_allow_html=True)

            audio_button(
                "🔊 발음 듣기",
                q["word"],
                key=f"{theme_name}_quiz_audio1_{i}"
            )

            options = get_shuffled_options(theme_name, i, q["options"])

            st.radio(
                "뜻을 고르세요.",
                options,
                key=f"{theme_name}_q1_{i}"
            )

            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("✅ 1차 제출하기", key=f"{theme_name}_submit1"):
            wrong = []

            for i, q in enumerate(quiz_items):
                user_answer = st.session_state.get(f"{theme_name}_q1_{i}")

                if user_answer != q["answer"]:
                    wrong.append(i)

            st.session_state[wrong_key] = wrong
            st.session_state[submitted1_key] = True
            st.rerun()

    elif st.session_state[submitted1_key] and not st.session_state[submitted2_key]:
        wrong = st.session_state[wrong_key]
        score = len(quiz_items) - len(wrong)

        st.markdown(
            f"""
            <div class="score-box">
                <div class="score-title">🎉 1차 결과: {score} / {len(quiz_items)}점</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if len(wrong) == 0:
            st.balloons()
            st.success("🌈 완벽합니다! 이 테마의 생존 단어를 모두 잘 기억하고 있습니다.")

            if st.button("🔄 다시 풀기", key=f"{theme_name}_reset_all_correct"):
                reset_theme(theme_name)
                st.rerun()

        else:
            st.markdown(
                f"""
                <div class="wrong-box">
                    🍊 틀린 단어 {len(wrong)}개를 다시 풀어 봅시다.
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### 🔁 2차 퀴즈: 틀린 단어만 다시 풀기")

            for i in wrong:
                q = quiz_items[i]

                st.markdown('<div class="quiz-card">', unsafe_allow_html=True)

                st.markdown(f"<div class='quiz-number'>🌟 Retry {i + 1}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='quiz-word'>{q['word']}</div>", unsafe_allow_html=True)

                audio_button(
                    "🔊 발음 다시 듣기",
                    q["word"],
                    key=f"{theme_name}_quiz_audio2_{i}"
                )

                options = get_shuffled_options(theme_name, i, q["options"])

                st.radio(
                    "뜻을 다시 고르세요.",
                    options,
                    key=f"{theme_name}_q2_{i}"
                )

                st.markdown('</div>', unsafe_allow_html=True)

            if st.button("✅ 2차 제출하기", key=f"{theme_name}_submit2"):
                st.session_state[submitted2_key] = True
                st.rerun()

    else:
        wrong = st.session_state[wrong_key]
        second_wrong = []

        for i in wrong:
            q = quiz_items[i]
            user_answer = st.session_state.get(f"{theme_name}_q2_{i}")

            if user_answer != q["answer"]:
                second_wrong.append(i)

        final_score = len(quiz_items) - len(second_wrong)

        st.markdown(
            f"""
            <div class="score-box">
                <div class="score-title">🏆 최종 결과: {final_score} / {len(quiz_items)}점</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if len(second_wrong) == 0:
            st.balloons()
            st.success("💖 좋습니다! 틀렸던 단어까지 모두 다시 확인했습니다.")
        else:
            st.warning("🍊 아래 단어들은 다시 복습하면 좋습니다.")

        st.markdown("### ✅ 정답 확인")

        if len(wrong) == 0:
            st.info("틀린 문제가 없습니다.")
        else:
            for i in wrong:
                q = quiz_items[i]
                user1 = st.session_state.get(f"{theme_name}_q1_{i}")
                user2 = st.session_state.get(f"{theme_name}_q2_{i}")

                st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                st.markdown(f"### 🌱 {q['word']}")

                audio_button(
                    "🔊 발음 다시 듣기",
                    q["word"],
                    key=f"{theme_name}_answer_audio_{i}"
                )

                st.write(f"1차 선택: {user1}")
                st.write(f"2차 선택: {user2}")
                st.success(f"정답: {q['answer']}")
                st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔄 다시 풀기", key=f"{theme_name}_reset"):
            reset_theme(theme_name)
            st.rerun()



# =========================
# 복습 희망 단어 모음 탭
# =========================
def show_unknown_words_tab():
    st.markdown(
        """
        <div class="theme-header">
            <div class="theme-title">⭐ 복습 희망</div>
            <div class="theme-desc">각 탭에서 복습하고 싶은 단어만 모아서 다시 들을 수 있습니다.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    unknown_words = st.session_state.unknown_words
    unknown_info = st.session_state.unknown_word_info

    if not unknown_words:
        st.info("아직 체크한 단어가 없습니다. 각 단어 옆의 '복습 희망'을 체크해 보세요.")
        return

    st.success(f"총 {len(unknown_words)}개의 단어를 체크했습니다.")

    # 마지막 탭에서도 같은 방식의 전체 카세트 듣기 제공
    unknown_items = []
    for idx, word in enumerate(unknown_words, start=1):
        info = unknown_info.get(word, {})
        unknown_items.append({
            "number": idx,
            "theme": info.get("theme", "복습 희망"),
            "word": word,
            "meaning": get_display_meaning(word, info.get("meaning", "")),
            "emoji": get_word_emoji(word),
        })

    show_cassette_audio(unknown_items, "복습 희망")

    st.markdown("### 📌 체크한 단어 목록")

    for idx, word in enumerate(unknown_words):
        info = unknown_info.get(word, {})
        meaning = get_display_meaning(word, info.get("meaning", ""))
        theme_name = info.get("theme", "")

        st.markdown('<div class="word-card">', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns([1.25, 1.05, 0.35, 1.65, 1.25])

        with col1:
            st.markdown(
                f"""
                <div class="word-row">
                    <div class="word-number">{idx + 1}</div>
                    <div class="word-text">{word}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div class='meaning-text'>{meaning}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div class='emoji-text'>{get_word_emoji(word)}</div>",
                unsafe_allow_html=True
            )

        with col4:
            audio_button(
                "🔊 듣기",
                word,
                key=f"unknown_word_audio_{idx}_{word}"
            )

        with col5:
            if st.button("삭제", key=f"delete_unknown_{idx}_{word}", use_container_width=True):
                remove_unknown_word(word)

                # 해당 단어의 체크박스 상태도 함께 지웁니다.
                keys_to_delete = [
                    key for key in list(st.session_state.keys())
                    if "_unknown_" in str(key) and str(key).endswith(f"_{word}")
                ]
                for key in keys_to_delete:
                    del st.session_state[key]

                st.rerun()

        st.caption(f"분류: {theme_name}")

        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️ 복습 희망 전체 삭제", key="clear_all_unknown_words", use_container_width=True):
        st.session_state.unknown_words = []
        st.session_state.unknown_word_info = {}
        st.rerun()


# =========================
# 탭 구성
# =========================
# 전체 카세트 듣기는 제일 마지막 탭에 배치
tab_names = list(word_themes.keys()) + ["🎧 전체 단어 듣기", "⭐ 복습 희망"]
tabs = st.tabs(tab_names)

for tab, theme_name in zip(tabs[:-2], word_themes.keys()):
    with tab:
        theme_words = word_themes[theme_name]

        st.markdown(
            f"""
            <div class="theme-header">
                <div class="theme-title">{theme_name}</div>
                <div class="theme-desc">{len(theme_words)}개의 생존 단어를 듣고 익혀 봅시다.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        show_cassette_player(theme_words, theme_name)
        show_word_cards(theme_words, theme_name)

# 기존 전체 카세트 듣기 탭은 그대로 유지
with tabs[-2]:
    show_all_cassette_tab()

# 복습 희망 단어 탭은 전체 카세트 오른쪽에 따로 추가
with tabs[-1]:
    show_unknown_words_tab()
