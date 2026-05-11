import streamlit as st
from gtts import gTTS
import io
import random
import base64
import uuid
import re
import json
import html
import streamlit.components.v1 as components

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="Daily English 400",
    page_icon="🌱",
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
        background: linear-gradient(135deg, #dcfce7 0%, #e0f2fe 50%, #fef3c7 100%);
        border-radius: 26px;
        padding: 28px 30px;
        margin-bottom: 28px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.8);
    }

    .hero-title {
        font-size: 27px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 10px;
    }

    .hero-text {
        font-size: 14px;
        color: #374151;
        line-height: 1.8;
    }

    .theme-header {
        background: linear-gradient(135deg, #22c55e 0%, #0ea5e9 50%, #8b5cf6 100%);
        color: white;
        padding: 22px 26px;
        border-radius: 24px;
        margin-bottom: 22px;
        box-shadow: 0 8px 20px rgba(34,197,94,0.25);
    }

    .theme-title {
        font-size: 27px;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .theme-desc {
        font-size: 15px;
        opacity: 0.95;
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
        font-size: 16px;
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
        border: 1px solid #dcfce7;
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
        color: #166534;
        background: #dcfce7;
        border-radius: 999px;
        padding: 5px 9px;
        text-align: center;
    }

    .word-text {
        min-width: 170px;
        font-size: 25px;
        font-weight: 900;
        color: #111827;
    }

    .meaning-text {
        font-size: 19px;
        font-weight: 800;
        color: #374151;
        margin-left: 8px;
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
        border: 1px solid #dbeafe;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    }

    .quiz-number {
        display: inline-block;
        background: #dbeafe;
        color: #1d4ed8;
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


    .cassette-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 50%, #fff7ed 100%);
        border: 1px solid #bbf7d0;
        border-radius: 24px;
        padding: 22px 24px;
        margin: 18px 0 18px 0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }

    .cassette-title {
        font-size: 25px;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 8px;
    }

    .cassette-text {
        font-size: 15px;
        color: #475569;
        line-height: 1.7;
        margin-bottom: 14px;
    }

    div[data-testid="stRadio"] > label {
        font-weight: 800;
        color: #374151;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 800;
        border: 1px solid #d1d5db;
        padding: 0.45rem 1rem;
    }

    .stButton > button:hover {
        border-color: #22c55e;
        color: #22c55e;
    }


    /* 카테고리 탭 크게 보이게 */
    div[data-testid="stTabs"] button[role="tab"] {
        min-height: 58px !important;
        padding: 10px 16px !important;
        border-radius: 18px 18px 0 0 !important;
    }

    div[data-testid="stTabs"] button[role="tab"] p {
        font-size: 21px !important;
        font-weight: 900 !important;
        line-height: 1.3 !important;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #dcfce7, #dbeafe, #fef3c7) !important;
        border-radius: 18px 18px 0 0 !important;
    }

    .theme-header {
        padding: 30px 34px !important;
        border-radius: 30px !important;
    }

    .theme-title {
        font-size: 38px !important;
        line-height: 1.2 !important;
    }

    .theme-desc {
        font-size: 18px !important;
        font-weight: 800 !important;
    }

    @media (max-width: 520px) {
        div[data-testid="stTabs"] button[role="tab"] {
            min-height: 50px !important;
            padding: 8px 11px !important;
        }
        div[data-testid="stTabs"] button[role="tab"] p {
            font-size: 17px !important;
        }
        .theme-title {
            font-size: 30px !important;
        }
        .theme-desc {
            font-size: 15px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 상단 제목
# =========================
st.markdown("<div class='main-title'>🌱 Daily English 400</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>기초 일상대화에 필요한 단어와 문장을 듣고, 읽고, 퀴즈로 익혀 봅시다.</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🌟 오늘의 학습 방식</div>
        <div class="hero-text">
        </div>
    </div>
    """,
    unsafe_allow_html=True
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


def remove_speaker_label(sentence):
    return re.sub(r"^[A-Z]:\s*", "", sentence).strip()


def make_dialogue_tts_text(dialogue):
    return " ".join([remove_speaker_label(item["en"]) for item in dialogue])


def get_word_emoji(word):
    """단어별로 최대한 어울리는 이모지를 붙입니다."""
    emoji_map = {
        # 학교생활
        "subject": "📚", "math": "➗", "science": "🔬", "history": "🏛️", "music": "🎵",
        "art": "🎨", "P.E.": "🏃", "club": "👥", "schedule": "🗓️", "semester": "🏫",
        "assignment": "📝", "project": "📁", "presentation": "🗣️", "report": "📄", "textbook": "📘",
        "workbook": "📗", "library": "📚", "cafeteria": "🍽️", "hallway": "🚶", "attendance": "✅",

        # 교실 활동
        "copy": "✍️", "repeat": "🔁", "underline": "〽️", "circle": "⭕", "choose": "☝️",
        "check": "✅", "match": "🧩", "complete": "🏁", "fill": "🖊️", "spell": "🔤",
        "pronounce": "🗣️", "review": "🔎", "explain": "💬", "describe": "🖼️", "compare": "⚖️",
        "discuss": "🗨️", "present": "📢", "take notes": "📝", "turn in": "📥", "hand out": "📤",

        # 집과 생활
        "living room": "🛋️", "bedroom": "🛏️", "kitchen": "🍳", "balcony": "🌇", "floor": "🧱",
        "wall": "🧱", "roof": "🏠", "garden": "🌷", "yard": "🌳", "sofa": "🛋️",
        "television": "📺", "refrigerator": "🧊", "microwave": "♨️", "blanket": "🛌", "pillow": "🛏️",
        "towel": "🧺", "soap": "🧼", "mirror": "🪞", "closet": "🚪", "trash": "🗑️",

        # 하루 일과
        "routine": "🔄", "wake up": "⏰", "get up": "🌅", "brush": "🪥", "shower": "🚿",
        "dress": "👕", "leave": "🚪", "arrive": "📍", "return": "↩️", "finish": "🏁",
        "relax": "😌", "weekday": "📅", "weekend": "🎉", "usually": "🔁", "often": "🔂",
        "sometimes": "🤔", "always": "♾️", "never": "🚫", "habit": "🔁", "lifestyle": "🌿",

        # 취미와 여가
        "hobby": "🎯", "movie": "🎬", "drama": "📺", "song": "🎵", "concert": "🎤",
        "dance": "💃", "drawing": "✏️", "painting": "🖌️", "comic": "💬", "novel": "📖",
        "photography": "📷", "cooking": "🍳", "baking": "🍞", "camping": "⛺", "hiking": "🥾",
        "fishing": "🎣", "free time": "🕒", "favorite": "⭐", "popular": "🔥", "relaxing": "😌",

        # 운동과 활동
        "soccer": "⚽", "baseball": "⚾", "basketball": "🏀", "volleyball": "🏐", "tennis": "🎾",
        "badminton": "🏸", "swimming": "🏊", "cycling": "🚴", "skating": "⛸️", "boxing": "🥊",
        "taekwondo": "🥋", "yoga": "🧘", "fitness": "💪", "field": "🏟️", "court": "🎾",
        "stadium": "🏟️", "coach": "📣", "match": "🏆", "competition": "🏁", "medal": "🏅",

        # 날씨와 계절
        "season": "🍂", "spring": "🌸", "summer": "☀️", "fall": "🍁", "winter": "❄️",
        "cloudy": "☁️", "rainy": "🌧️", "snowy": "🌨️", "windy": "🌬️", "stormy": "⛈️",
        "foggy": "🌫️", "dry": "🏜️", "wet": "💦", "humid": "💧", "temperature": "🌡️",
        "degree": "🌡️", "forecast": "📡", "umbrella": "☂️", "raincoat": "🧥", "rainbow": "🌈",

        # 자연과 환경
        "nature": "🌿", "environment": "🌎", "plant": "🌱", "forest": "🌲", "lake": "🏞️",
        "ocean": "🌊", "island": "🏝️", "desert": "🏜️", "farm": "🚜", "village": "🏘️",
        "leaf": "🍃", "root": "🌱", "stone": "🪨", "sand": "🏖️", "soil": "🌱",
        "plastic": "🥤", "recycle": "♻️", "protect": "🛡️", "pollution": "🏭",

        # 식당과 주문
        "restaurant": "🍽️", "menu": "📋", "seat": "💺", "waiter": "🤵", "waitress": "🤵‍♀️",
        "order": "🛎️", "dish": "🍛", "meal": "🍽️", "soup": "🍲", "salad": "🥗",
        "steak": "🥩", "pizza": "🍕", "pasta": "🍝", "burger": "🍔", "sandwich": "🥪",
        "dessert": "🍰", "spicy": "🌶️", "sweet": "🍬", "bill": "🧾", "receipt": "🧾",

        # 쇼핑과 가격
        "shop": "🏪", "market": "🛒", "mall": "🏬", "supermarket": "🛒", "cashier": "💁",
        "customer": "🧑", "price": "💰", "sale": "🏷️", "discount": "🔻", "coupon": "🎟️",
        "change": "💵", "coin": "🪙", "expensive": "💸", "cheap": "👍", "size": "📏",
        "color": "🎨", "brand": "🏷️", "exchange": "🔄", "refund": "↩️",

        # 옷과 외모
        "T-shirt": "👕", "pants": "👖", "jeans": "👖", "shorts": "🩳", "skirt": "👗",
        "dress": "👗", "jacket": "🧥", "coat": "🧥", "sweater": "🧶", "hoodie": "🧥",
        "uniform": "🎽", "socks": "🧦", "sneakers": "👟", "boots": "🥾", "sandals": "🩴",
        "scarf": "🧣", "gloves": "🧤", "belt": "👖", "glasses": "👓", "comfortable": "😌",

        # 교통과 길 찾기
        "bus stop": "🚏", "subway": "🚇", "airport": "✈️", "terminal": "🚌", "platform": "🚉",
        "route": "🗺️", "direction": "➡️", "straight": "⬆️", "corner": "↪️", "block": "🏙️",
        "traffic": "🚦", "crosswalk": "🚸", "sidewalk": "🚶", "bridge": "🌉", "tunnel": "🚇",
        "entrance": "🚪", "exit": "🚪", "transfer": "🔁", "lost": "😵", "guide": "🧭",

        # 여행과 숙박
        "travel": "✈️", "trip": "🧳", "vacation": "🏖️", "tourist": "📸", "passport": "🛂",
        "flight": "🛫", "hotel": "🏨", "motel": "🏩", "hostel": "🛏️", "reservation": "📅",
        "check in": "🔑", "check out": "👋", "luggage": "🧳", "suitcase": "🧳", "backpack": "🎒",
        "souvenir": "🎁", "museum": "🏛️", "famous": "⭐", "local": "📍",

        # 친구 관계
        "friendship": "🤝", "best friend": "👯", "teammate": "👥", "partner": "🤝", "message": "💬",
        "call": "📞", "chat": "💬", "invite": "✉️", "visit": "🏠", "meet": "🤝",
        "hang out": "🎉", "laugh": "😂", "share": "🤲", "trust": "🤝", "promise": "🤞",
        "secret": "🤫", "joke": "😄", "together": "👥", "alone": "🚶", "forgive": "🫶",

        # 감정 표현 확장
        "excited": "🤩", "nervous": "😬", "bored": "🥱", "surprised": "😲", "confused": "😕",
        "embarrassed": "😳", "proud": "😊", "disappointed": "😞", "lonely": "🥲", "relaxed": "😌",
        "calm": "🧘", "upset": "😟", "interested": "🧐", "satisfied": "😌", "thankful": "🙏",
        "hopeful": "🌟", "mood": "🙂", "stress": "😣", "confidence": "💪", "courage": "🦁",

        # 생각과 의견
        "think": "💭", "believe": "🙏", "guess": "🤔", "remember": "🧠", "forget": "💨",
        "mean": "💡", "agree": "👍", "disagree": "👎", "opinion": "💬", "idea": "💡",
        "reason": "❓", "example": "🔎", "fact": "✅", "choice": "☝️", "decision": "✅",
        "advice": "💡", "suggestion": "💬", "possible": "✅", "impossible": "🚫", "confusing": "😵",

        # 계획과 약속
        "plan": "📝", "appointment": "📅", "meeting": "👥", "date": "📆", "event": "🎪",
        "party": "🎉", "festival": "🎊", "deadline": "⏳", "calendar": "📅", "next week": "➡️",
        "join": "🙋", "prepare": "🎒", "decide": "✅", "cancel": "❌", "on time": "⏰",
        "available": "🟢", "reminder": "🔔",

        # 건강한 생활
        "health": "🩺", "body": "🧍", "eye": "👁️", "ear": "👂", "nose": "👃",
        "mouth": "👄", "tooth": "🦷", "hand": "✋", "arm": "💪", "leg": "🦵",
        "foot": "🦶", "stomach": "🤰", "back": "🔙", "heart": "❤️", "clinic": "🏥",
        "vitamin": "💊", "diet": "🥗", "cough": "😷", "flu": "🤒", "breathe": "🌬️",

        # 미디어와 스마트폰
        "smartphone": "📱", "screen": "🖥️", "app": "📲", "website": "🌐", "internet": "🌐",
        "Wi-Fi": "📶", "password": "🔐", "text": "💬", "video call": "📹", "gallery": "🖼️",
        "news": "📰", "channel": "📺", "post": "📝", "comment": "💬", "upload": "⬆️",
        "download": "⬇️", "search": "🔎", "click": "🖱️", "battery": "🔋", "notification": "🔔",

        # 직업과 미래
        "job": "💼", "work": "💼", "company": "🏢", "office": "🏢", "factory": "🏭",
        "engineer": "🛠️", "mechanic": "🔧", "chef": "👨‍🍳", "firefighter": "🚒", "farmer": "🚜",
        "designer": "🎨", "singer": "🎤", "actor": "🎭", "athlete": "🏃", "dream": "🌈",
        "future": "🔮", "goal": "🎯", "skill": "🛠️", "interview": "🎙️", "experience": "🌱",
    }
    return emoji_map.get(word, "🌱")


# =========================
# 단어용 HTML 오디오 플레이어
# =========================
def html_word_audio_player(label, text, repeat_count=20, pause_ms=1500, height=48):
    audio_bytes = make_tts_audio(text)
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    play_btn_id = f"play_btn_{uuid.uuid4().hex}"
    stop_btn_id = f"stop_btn_{uuid.uuid4().hex}"
    status_id = f"status_{uuid.uuid4().hex}"
    player_id = f"player_{uuid.uuid4().hex}"

    safe_label = json.dumps(label)
    safe_text = json.dumps(text)
    safe_player_id = json.dumps(player_id)
    safe_src = json.dumps(f"data:audio/mp3;base64,{audio_base64}")

    components.html(
        f"""
        <div style="font-family: Arial, sans-serif; display:flex; align-items:center; gap:6px; height:42px;">
            <button id="{play_btn_id}" style="
                background: linear-gradient(135deg, #dcfce7, #dbeafe);
                border: 1px solid #bbf7d0;
                border-radius: 999px;
                padding: 6px 10px;
                font-weight: 800;
                font-size: 13px;
                color: #374151;
                cursor: pointer;
                box-shadow: 0 2px 5px rgba(0,0,0,0.06);
                white-space: nowrap;
            ">
                {label}
            </button>

            <button id="{stop_btn_id}" style="
                background: #fff7ed;
                border: 1px solid #fed7aa;
                border-radius: 999px;
                padding: 6px 10px;
                font-weight: 800;
                font-size: 13px;
                color: #9a3412;
                cursor: pointer;
                box-shadow: 0 2px 5px rgba(0,0,0,0.04);
                white-space: nowrap;
            ">
                ⏹ 중지
            </button>

            <span id="{status_id}" style="
                font-size: 12px;
                color: #075985;
                font-weight: 700;
                white-space: nowrap;
            "></span>

            <script>
            const playBtn = document.getElementById("{play_btn_id}");
            const stopBtn = document.getElementById("{stop_btn_id}");
            const status = document.getElementById("{status_id}");

            const maxCount = {repeat_count};
            const pauseMs = {pause_ms};
            const labelText = {safe_label};
            const wordText = {safe_text};
            const playerId = {safe_player_id};
            const audioSrc = {safe_src};

            const channel = new BroadcastChannel("daily_english_audio_channel");

            // 중요: Streamlit components.html()은 작은 iframe 안에서 실행됩니다.
            // window.parent에 오디오를 만들면 탭/화면 전환 때 iframe이 사라지면서 소리가 끊길 수 있습니다.
            // 그래서 가능한 한 가장 바깥 브라우저 창(window.top)에 공용 오디오를 만들어 유지합니다.
            let parentWin = window;
            try {{
                parentWin = window.top || window.parent || window;
            }} catch (e) {{
                parentWin = window.parent || window;
            }}

            // 가장 바깥 화면에 공용 단어 오디오 플레이어를 1개만 만듭니다.
            // Streamlit 탭/카테고리 화면을 바꿔도 이 공용 오디오는 최대한 유지됩니다.
            if (!parentWin.__dailyEnglishWordPlayer) {{
                const sharedAudio = new parentWin.Audio();

                parentWin.__dailyEnglishWordPlayer = {{
                    audio: sharedAudio,
                    timer: null,
                    token: 0,
                    count: 0,
                    maxCount: 0,
                    pauseMs: 0,
                    currentPlayerId: null,
                    labelText: "▶️ 발음",
                    updateStatus: null,
                    updateButton: null,

                    safeStatus(message) {{
                        try {{
                            if (typeof this.updateStatus === "function") this.updateStatus(message);
                        }} catch (e) {{}}
                    }},

                    safeButton(text, disabled) {{
                        try {{
                            if (typeof this.updateButton === "function") this.updateButton(text, disabled);
                        }} catch (e) {{}}
                    }},

                    clearTimer() {{
                        if (this.timer) {{
                            parentWin.clearTimeout(this.timer);
                            this.timer = null;
                        }}
                    }},

                    stop(showMessage = false, requestedPlayerId = null) {{
                        if (requestedPlayerId && this.currentPlayerId && requestedPlayerId !== this.currentPlayerId) return;

                        this.token += 1;
                        this.clearTimer();
                        this.audio.pause();
                        this.audio.currentTime = 0;
                        this.count = 0;
                        this.safeButton(this.labelText, false);
                        this.safeStatus(showMessage ? "중지됨" : "");
                        this.currentPlayerId = null;
                    }},

                    play(options) {{
                        this.stop(false);

                        this.token += 1;
                        const myToken = this.token;

                        this.currentPlayerId = options.playerId;
                        this.labelText = options.labelText;
                        this.maxCount = options.maxCount;
                        this.pauseMs = options.pauseMs;
                        this.updateStatus = options.updateStatus;
                        this.updateButton = options.updateButton;
                        this.count = 0;

                        this.audio.src = options.src;
                        this.safeButton("재생중", true);
                        this.safeStatus("시작");

                        const playOnce = () => {{
                            if (myToken !== this.token) return;

                            if (this.count >= this.maxCount) {{
                                this.safeStatus("완료");
                                this.safeButton(this.labelText, false);
                                this.currentPlayerId = null;
                                return;
                            }}

                            this.audio.currentTime = 0;
                            this.audio.play().then(() => {{
                                if (myToken !== this.token) return;
                                this.count += 1;
                                this.safeStatus(this.count + "/" + this.maxCount);
                            }}).catch((error) => {{
                                this.safeStatus("다시 클릭");
                                this.safeButton(this.labelText, false);
                            }});
                        }};

                        this.audio.onended = () => {{
                            if (myToken !== this.token) return;

                            if (this.count < this.maxCount) {{
                                this.timer = parentWin.setTimeout(playOnce, this.pauseMs);
                            }} else {{
                                this.safeStatus("완료");
                                this.safeButton(this.labelText, false);
                                this.currentPlayerId = null;
                            }}
                        }};

                        playOnce();
                    }}
                }};
            }}

            const sharedPlayer = parentWin.__dailyEnglishWordPlayer;

            function setLocalButton(text, disabled) {{
                playBtn.innerText = text;
                playBtn.disabled = disabled;
            }}

            function setLocalStatus(message) {{
                status.innerText = message;
            }}

            function resetLocalUi(message = "") {{
                setLocalButton(labelText, false);
                setLocalStatus(message);
            }}

            channel.onmessage = function(event) {{
                if (!event.data) return;

                // 다른 단어/카세트를 새로 누르면 현재 단어 발음은 멈춥니다.
                // 단, 탭이나 페이지 이동만으로는 STOP_ALL을 받더라도 단어 발음을 끊지 않습니다.
                if (event.data.type === "STOP_OTHERS" && event.data.playerId !== playerId) {{
                    if (sharedPlayer.currentPlayerId === playerId) {{
                        sharedPlayer.stop(false, playerId);
                    }}
                    resetLocalUi("");
                }}
            }};

            playBtn.addEventListener("click", function() {{
                channel.postMessage({{
                    type: "STOP_OTHERS",
                    playerId: playerId
                }});

                sharedPlayer.play({{
                    src: audioSrc,
                    playerId: playerId,
                    labelText: labelText,
                    wordText: wordText,
                    maxCount: maxCount,
                    pauseMs: pauseMs,
                    updateStatus: setLocalStatus,
                    updateButton: setLocalButton
                }});
            }});

            stopBtn.addEventListener("click", function() {{
                sharedPlayer.stop(true, playerId);
                resetLocalUi("중지됨");
            }});
            </script>
        </div>
        """,
        height=height
    )

def audio_button(label, text, key=None):
    html_word_audio_player(
        label=label,
        text=text,
        repeat_count=20,
        pause_ms=1500,
        height=48
    )


# =========================
# 대화용 HTML 오디오 플레이어
# =========================
def html_dialogue_audio_player(label, dialogue_lines, line_pause_ms=1400, height=105):
    audio_data_list = []

    for line in dialogue_lines:
        clean_text = remove_speaker_label(line["en"])
        audio_bytes = make_tts_audio(clean_text)
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        audio_data_list.append({
            "text": clean_text,
            "src": f"data:audio/mp3;base64,{audio_base64}"
        })

    audio_json = json.dumps(audio_data_list)
    safe_label = json.dumps(label)

    audio_id = f"dialogue_audio_{uuid.uuid4().hex}"
    play_btn_id = f"dialogue_play_{uuid.uuid4().hex}"
    stop_btn_id = f"dialogue_stop_{uuid.uuid4().hex}"
    status_id = f"dialogue_status_{uuid.uuid4().hex}"
    player_id = f"dialogue_player_{uuid.uuid4().hex}"
    safe_player_id = json.dumps(player_id)

    components.html(
        f"""
        <div style="font-family: Arial, sans-serif;">
            <audio id="{audio_id}"></audio>

            <button id="{play_btn_id}" style="
                background: linear-gradient(135deg, #fef3c7, #dbeafe);
                border: 1px solid #fde68a;
                border-radius: 999px;
                padding: 9px 15px;
                font-weight: 800;
                font-size: 14px;
                color: #374151;
                cursor: pointer;
                box-shadow: 0 3px 8px rgba(0,0,0,0.08);
                margin-right: 6px;
            ">
                {label}
            </button>

            <button id="{stop_btn_id}" style="
                background: #fff7ed;
                border: 1px solid #fed7aa;
                border-radius: 999px;
                padding: 9px 15px;
                font-weight: 800;
                font-size: 14px;
                color: #9a3412;
                cursor: pointer;
                box-shadow: 0 3px 8px rgba(0,0,0,0.05);
            ">
                ⏹ 중지
            </button>

            <div id="{status_id}" style="
                margin-top: 8px;
                font-size: 13px;
                color: #075985;
                font-weight: 700;
            "></div>

            <script>
            const audio = document.getElementById("{audio_id}");
            const playBtn = document.getElementById("{play_btn_id}");
            const stopBtn = document.getElementById("{stop_btn_id}");
            const status = document.getElementById("{status_id}");

            const dialogueAudios = {audio_json};
            const linePauseMs = {line_pause_ms};
            const labelText = {safe_label};
            const playerId = {safe_player_id};

            let index = 0;
            let timer = null;
            let isStopped = false;

            const channel = new BroadcastChannel("daily_english_audio_channel");

            function stopThisAudio(showMessage = false) {{
                isStopped = true;

                if (timer) {{
                    clearTimeout(timer);
                    timer = null;
                }}

                audio.pause();
                audio.currentTime = 0;
                index = 0;

                playBtn.disabled = false;
                playBtn.innerText = labelText;

                if (showMessage) {{
                    status.innerText = "⏹ 대화 듣기를 중지했습니다.";
                }} else {{
                    status.innerText = "";
                }}
            }}

            channel.onmessage = function(event) {{
                if (!event.data) return;

                if (event.data.type === "STOP_OTHERS" && event.data.playerId !== playerId) {{
                    stopThisAudio(false);
                }}
            }};

            function playCurrentLine() {{
                if (isStopped) return;

                if (index >= dialogueAudios.length) {{
                    status.innerText = "✅ 대화 재생 완료";
                    playBtn.disabled = false;
                    playBtn.innerText = labelText;
                    return;
                }}

                audio.src = dialogueAudios[index].src;
                audio.currentTime = 0;

                audio.play().then(() => {{
                    status.innerText = "🔊 대화 재생 중: " + (index + 1) + " / " + dialogueAudios.length;
                }}).catch((error) => {{
                    status.innerText = "⚠️ 소리 재생이 차단되었습니다. 버튼을 다시 눌러 주세요.";
                    playBtn.disabled = false;
                    playBtn.innerText = labelText;
                }});
            }}

            audio.addEventListener("ended", function() {{
                if (isStopped) return;

                index += 1;

                if (index < dialogueAudios.length) {{
                    timer = setTimeout(playCurrentLine, linePauseMs);
                }} else {{
                    status.innerText = "✅ 대화 재생 완료";
                    playBtn.disabled = false;
                    playBtn.innerText = labelText;
                }}
            }});

            playBtn.addEventListener("click", function() {{
                channel.postMessage({{
                    type: "STOP_OTHERS",
                    playerId: playerId
                }});

                stopThisAudio(false);

                isStopped = false;
                index = 0;
                playBtn.disabled = true;
                playBtn.innerText = "재생 중...";
                status.innerText = "🔊 대화 듣기를 시작합니다.";
                playCurrentLine();
            }});

            stopBtn.addEventListener("click", function() {{
                stopThisAudio(true);
            }});
            </script>
        </div>
        """,
        height=height
    )


# =========================
# Daily English 400 테마별 단어
# =========================
word_themes = {
    "🏫 학교생활": [
        {"word": "subject", "meaning": "과목"},
        {"word": "math", "meaning": "수학"},
        {"word": "science", "meaning": "과학"},
        {"word": "history", "meaning": "역사"},
        {"word": "music", "meaning": "음악"},
        {"word": "art", "meaning": "미술"},
        {"word": "P.E.", "meaning": "체육"},
        {"word": "club", "meaning": "동아리"},
        {"word": "schedule", "meaning": "일정표"},
        {"word": "semester", "meaning": "학기"},
        {"word": "assignment", "meaning": "과제"},
        {"word": "project", "meaning": "프로젝트"},
        {"word": "presentation", "meaning": "발표"},
        {"word": "report", "meaning": "보고서"},
        {"word": "textbook", "meaning": "교과서"},
        {"word": "workbook", "meaning": "문제집"},
        {"word": "library", "meaning": "도서관"},
        {"word": "cafeteria", "meaning": "급식소, 식당"},
        {"word": "hallway", "meaning": "복도"},
        {"word": "attendance", "meaning": "출석"},
    ],

    "✏️ 교실 활동": [
        {"word": "copy", "meaning": "베껴 쓰다"},
        {"word": "repeat", "meaning": "반복하다"},
        {"word": "underline", "meaning": "밑줄 치다"},
        {"word": "circle", "meaning": "동그라미 치다"},
        {"word": "choose", "meaning": "고르다"},
        {"word": "check", "meaning": "확인하다"},
        {"word": "match", "meaning": "연결하다, 맞추다"},
        {"word": "complete", "meaning": "완성하다"},
        {"word": "fill", "meaning": "채우다"},
        {"word": "spell", "meaning": "철자를 말하다"},
        {"word": "pronounce", "meaning": "발음하다"},
        {"word": "review", "meaning": "복습하다"},
        {"word": "explain", "meaning": "설명하다"},
        {"word": "describe", "meaning": "묘사하다"},
        {"word": "compare", "meaning": "비교하다"},
        {"word": "discuss", "meaning": "토론하다"},
        {"word": "present", "meaning": "발표하다"},
        {"word": "take notes", "meaning": "필기하다"},
        {"word": "turn in", "meaning": "제출하다"},
        {"word": "hand out", "meaning": "나누어 주다"},
    ],

    "🏠 집과 생활": [
        {"word": "living room", "meaning": "거실"},
        {"word": "bedroom", "meaning": "침실"},
        {"word": "kitchen", "meaning": "부엌"},
        {"word": "balcony", "meaning": "발코니"},
        {"word": "floor", "meaning": "바닥, 층"},
        {"word": "wall", "meaning": "벽"},
        {"word": "roof", "meaning": "지붕"},
        {"word": "garden", "meaning": "정원"},
        {"word": "yard", "meaning": "마당"},
        {"word": "sofa", "meaning": "소파"},
        {"word": "television", "meaning": "텔레비전"},
        {"word": "refrigerator", "meaning": "냉장고"},
        {"word": "microwave", "meaning": "전자레인지"},
        {"word": "blanket", "meaning": "담요"},
        {"word": "pillow", "meaning": "베개"},
        {"word": "towel", "meaning": "수건"},
        {"word": "soap", "meaning": "비누"},
        {"word": "mirror", "meaning": "거울"},
        {"word": "closet", "meaning": "옷장"},
        {"word": "trash", "meaning": "쓰레기"},
    ],

    "🌅 하루 일과": [
        {"word": "routine", "meaning": "일과"},
        {"word": "wake up", "meaning": "잠에서 깨다"},
        {"word": "get up", "meaning": "일어나다"},
        {"word": "brush", "meaning": "닦다"},
        {"word": "shower", "meaning": "샤워하다"},
        {"word": "dress", "meaning": "옷을 입다"},
        {"word": "leave", "meaning": "떠나다"},
        {"word": "arrive", "meaning": "도착하다"},
        {"word": "return", "meaning": "돌아오다"},
        {"word": "finish", "meaning": "끝내다"},
        {"word": "relax", "meaning": "쉬다"},
        {"word": "weekday", "meaning": "평일"},
        {"word": "weekend", "meaning": "주말"},
        {"word": "usually", "meaning": "보통"},
        {"word": "often", "meaning": "자주"},
        {"word": "sometimes", "meaning": "가끔"},
        {"word": "always", "meaning": "항상"},
        {"word": "never", "meaning": "절대 ~않다"},
        {"word": "habit", "meaning": "습관"},
        {"word": "lifestyle", "meaning": "생활 방식"},
    ],

    "🎮 취미와 여가": [
        {"word": "hobby", "meaning": "취미"},
        {"word": "movie", "meaning": "영화"},
        {"word": "drama", "meaning": "드라마"},
        {"word": "song", "meaning": "노래"},
        {"word": "concert", "meaning": "콘서트"},
        {"word": "dance", "meaning": "춤"},
        {"word": "drawing", "meaning": "그림 그리기"},
        {"word": "painting", "meaning": "그림, 회화"},
        {"word": "comic", "meaning": "만화"},
        {"word": "novel", "meaning": "소설"},
        {"word": "photography", "meaning": "사진 촬영"},
        {"word": "cooking", "meaning": "요리"},
        {"word": "baking", "meaning": "빵 굽기"},
        {"word": "camping", "meaning": "캠핑"},
        {"word": "hiking", "meaning": "하이킹"},
        {"word": "fishing", "meaning": "낚시"},
        {"word": "free time", "meaning": "여가 시간"},
        {"word": "favorite", "meaning": "가장 좋아하는"},
        {"word": "popular", "meaning": "인기 있는"},
        {"word": "relaxing", "meaning": "편안한"},
    ],

    "⚽ 운동과 활동": [
        {"word": "soccer", "meaning": "축구"},
        {"word": "baseball", "meaning": "야구"},
        {"word": "basketball", "meaning": "농구"},
        {"word": "volleyball", "meaning": "배구"},
        {"word": "tennis", "meaning": "테니스"},
        {"word": "badminton", "meaning": "배드민턴"},
        {"word": "swimming", "meaning": "수영"},
        {"word": "cycling", "meaning": "자전거 타기"},
        {"word": "skating", "meaning": "스케이트 타기"},
        {"word": "boxing", "meaning": "복싱"},
        {"word": "taekwondo", "meaning": "태권도"},
        {"word": "yoga", "meaning": "요가"},
        {"word": "fitness", "meaning": "체력 운동"},
        {"word": "field", "meaning": "경기장, 들판"},
        {"word": "court", "meaning": "코트"},
        {"word": "stadium", "meaning": "경기장"},
        {"word": "coach", "meaning": "코치"},
        {"word": "match", "meaning": "경기"},
        {"word": "competition", "meaning": "대회"},
        {"word": "medal", "meaning": "메달"},
    ],

    "🌦️ 날씨와 계절": [
        {"word": "season", "meaning": "계절"},
        {"word": "spring", "meaning": "봄"},
        {"word": "summer", "meaning": "여름"},
        {"word": "fall", "meaning": "가을"},
        {"word": "winter", "meaning": "겨울"},
        {"word": "cloudy", "meaning": "흐린"},
        {"word": "rainy", "meaning": "비 오는"},
        {"word": "snowy", "meaning": "눈 오는"},
        {"word": "windy", "meaning": "바람 부는"},
        {"word": "stormy", "meaning": "폭풍우 치는"},
        {"word": "foggy", "meaning": "안개 낀"},
        {"word": "dry", "meaning": "건조한"},
        {"word": "wet", "meaning": "젖은"},
        {"word": "humid", "meaning": "습한"},
        {"word": "temperature", "meaning": "온도"},
        {"word": "degree", "meaning": "도"},
        {"word": "forecast", "meaning": "일기예보"},
        {"word": "umbrella", "meaning": "우산"},
        {"word": "raincoat", "meaning": "비옷"},
        {"word": "rainbow", "meaning": "무지개"},
    ],

    "🌳 자연과 환경": [
        {"word": "nature", "meaning": "자연"},
        {"word": "environment", "meaning": "환경"},
        {"word": "plant", "meaning": "식물"},
        {"word": "forest", "meaning": "숲"},
        {"word": "lake", "meaning": "호수"},
        {"word": "ocean", "meaning": "대양"},
        {"word": "island", "meaning": "섬"},
        {"word": "desert", "meaning": "사막"},
        {"word": "field", "meaning": "들판"},
        {"word": "farm", "meaning": "농장"},
        {"word": "village", "meaning": "마을"},
        {"word": "leaf", "meaning": "잎"},
        {"word": "root", "meaning": "뿌리"},
        {"word": "stone", "meaning": "돌"},
        {"word": "sand", "meaning": "모래"},
        {"word": "soil", "meaning": "흙"},
        {"word": "plastic", "meaning": "플라스틱"},
        {"word": "recycle", "meaning": "재활용하다"},
        {"word": "protect", "meaning": "보호하다"},
        {"word": "pollution", "meaning": "오염"},
    ],

    "🍽️ 식당과 주문": [
        {"word": "restaurant", "meaning": "식당"},
        {"word": "menu", "meaning": "메뉴"},
        {"word": "seat", "meaning": "자리"},
        {"word": "waiter", "meaning": "남자 종업원"},
        {"word": "waitress", "meaning": "여자 종업원"},
        {"word": "order", "meaning": "주문하다"},
        {"word": "dish", "meaning": "요리, 접시"},
        {"word": "meal", "meaning": "식사"},
        {"word": "soup", "meaning": "수프"},
        {"word": "salad", "meaning": "샐러드"},
        {"word": "steak", "meaning": "스테이크"},
        {"word": "pizza", "meaning": "피자"},
        {"word": "pasta", "meaning": "파스타"},
        {"word": "burger", "meaning": "버거"},
        {"word": "sandwich", "meaning": "샌드위치"},
        {"word": "dessert", "meaning": "디저트"},
        {"word": "spicy", "meaning": "매운"},
        {"word": "sweet", "meaning": "단"},
        {"word": "bill", "meaning": "계산서"},
        {"word": "receipt", "meaning": "영수증"},
    ],

    "🛍️ 쇼핑과 가격": [
        {"word": "shop", "meaning": "가게"},
        {"word": "market", "meaning": "시장"},
        {"word": "mall", "meaning": "쇼핑몰"},
        {"word": "supermarket", "meaning": "슈퍼마켓"},
        {"word": "cashier", "meaning": "계산원"},
        {"word": "customer", "meaning": "손님"},
        {"word": "price", "meaning": "가격"},
        {"word": "sale", "meaning": "할인 판매"},
        {"word": "discount", "meaning": "할인"},
        {"word": "coupon", "meaning": "쿠폰"},
        {"word": "change", "meaning": "거스름돈"},
        {"word": "coin", "meaning": "동전"},
        {"word": "bill", "meaning": "지폐, 계산서"},
        {"word": "expensive", "meaning": "비싼"},
        {"word": "cheap", "meaning": "싼"},
        {"word": "size", "meaning": "크기"},
        {"word": "color", "meaning": "색깔"},
        {"word": "brand", "meaning": "상표"},
        {"word": "exchange", "meaning": "교환하다"},
        {"word": "refund", "meaning": "환불"},
    ],

    "👕 옷과 외모": [
        {"word": "T-shirt", "meaning": "티셔츠"},
        {"word": "pants", "meaning": "바지"},
        {"word": "jeans", "meaning": "청바지"},
        {"word": "shorts", "meaning": "반바지"},
        {"word": "skirt", "meaning": "치마"},
        {"word": "dress", "meaning": "드레스, 원피스"},
        {"word": "jacket", "meaning": "재킷"},
        {"word": "coat", "meaning": "코트"},
        {"word": "sweater", "meaning": "스웨터"},
        {"word": "hoodie", "meaning": "후드티"},
        {"word": "uniform", "meaning": "교복, 제복"},
        {"word": "socks", "meaning": "양말"},
        {"word": "sneakers", "meaning": "운동화"},
        {"word": "boots", "meaning": "부츠"},
        {"word": "sandals", "meaning": "샌들"},
        {"word": "scarf", "meaning": "목도리"},
        {"word": "gloves", "meaning": "장갑"},
        {"word": "belt", "meaning": "벨트"},
        {"word": "glasses", "meaning": "안경"},
        {"word": "comfortable", "meaning": "편안한"},
    ],

    "🚇 교통과 길 찾기": [
        {"word": "bus stop", "meaning": "버스 정류장"},
        {"word": "subway", "meaning": "지하철"},
        {"word": "airport", "meaning": "공항"},
        {"word": "terminal", "meaning": "터미널"},
        {"word": "platform", "meaning": "승강장"},
        {"word": "route", "meaning": "경로"},
        {"word": "direction", "meaning": "방향"},
        {"word": "straight", "meaning": "똑바로"},
        {"word": "corner", "meaning": "모퉁이"},
        {"word": "block", "meaning": "구역, 블록"},
        {"word": "traffic", "meaning": "교통"},
        {"word": "crosswalk", "meaning": "횡단보도"},
        {"word": "sidewalk", "meaning": "인도"},
        {"word": "bridge", "meaning": "다리"},
        {"word": "tunnel", "meaning": "터널"},
        {"word": "entrance", "meaning": "입구"},
        {"word": "exit", "meaning": "출구"},
        {"word": "transfer", "meaning": "갈아타다"},
        {"word": "lost", "meaning": "길을 잃은"},
        {"word": "guide", "meaning": "안내하다, 안내자"},
    ],

    "🧳 여행과 숙박": [
        {"word": "travel", "meaning": "여행하다"},
        {"word": "trip", "meaning": "여행"},
        {"word": "vacation", "meaning": "방학, 휴가"},
        {"word": "tourist", "meaning": "관광객"},
        {"word": "guide", "meaning": "안내자"},
        {"word": "passport", "meaning": "여권"},
        {"word": "flight", "meaning": "항공편"},
        {"word": "hotel", "meaning": "호텔"},
        {"word": "motel", "meaning": "모텔"},
        {"word": "hostel", "meaning": "호스텔"},
        {"word": "reservation", "meaning": "예약"},
        {"word": "check in", "meaning": "체크인하다"},
        {"word": "check out", "meaning": "체크아웃하다"},
        {"word": "luggage", "meaning": "짐"},
        {"word": "suitcase", "meaning": "여행 가방"},
        {"word": "backpack", "meaning": "배낭"},
        {"word": "souvenir", "meaning": "기념품"},
        {"word": "museum", "meaning": "박물관"},
        {"word": "famous", "meaning": "유명한"},
        {"word": "local", "meaning": "현지의"},
    ],

    "👥 친구 관계": [
        {"word": "friendship", "meaning": "우정"},
        {"word": "best friend", "meaning": "가장 친한 친구"},
        {"word": "teammate", "meaning": "팀 동료"},
        {"word": "partner", "meaning": "짝, 파트너"},
        {"word": "message", "meaning": "메시지"},
        {"word": "call", "meaning": "전화하다"},
        {"word": "chat", "meaning": "채팅하다"},
        {"word": "invite", "meaning": "초대하다"},
        {"word": "visit", "meaning": "방문하다"},
        {"word": "meet", "meaning": "만나다"},
        {"word": "hang out", "meaning": "어울려 놀다"},
        {"word": "laugh", "meaning": "웃다"},
        {"word": "share", "meaning": "나누다, 공유하다"},
        {"word": "trust", "meaning": "믿다"},
        {"word": "promise", "meaning": "약속"},
        {"word": "secret", "meaning": "비밀"},
        {"word": "joke", "meaning": "농담"},
        {"word": "together", "meaning": "함께"},
        {"word": "alone", "meaning": "혼자"},
        {"word": "forgive", "meaning": "용서하다"},
    ],

    "😊 감정 표현 확장": [
        {"word": "excited", "meaning": "신난"},
        {"word": "nervous", "meaning": "긴장한"},
        {"word": "bored", "meaning": "지루한"},
        {"word": "surprised", "meaning": "놀란"},
        {"word": "confused", "meaning": "혼란스러운"},
        {"word": "embarrassed", "meaning": "당황한"},
        {"word": "proud", "meaning": "자랑스러운"},
        {"word": "disappointed", "meaning": "실망한"},
        {"word": "lonely", "meaning": "외로운"},
        {"word": "relaxed", "meaning": "편안한"},
        {"word": "calm", "meaning": "차분한"},
        {"word": "upset", "meaning": "속상한"},
        {"word": "interested", "meaning": "관심 있는"},
        {"word": "satisfied", "meaning": "만족한"},
        {"word": "thankful", "meaning": "감사하는"},
        {"word": "hopeful", "meaning": "희망적인"},
        {"word": "mood", "meaning": "기분"},
        {"word": "stress", "meaning": "스트레스"},
        {"word": "confidence", "meaning": "자신감"},
        {"word": "courage", "meaning": "용기"},
    ],

    "💭 생각과 의견": [
        {"word": "think", "meaning": "생각하다"},
        {"word": "believe", "meaning": "믿다"},
        {"word": "guess", "meaning": "추측하다"},
        {"word": "remember", "meaning": "기억하다"},
        {"word": "forget", "meaning": "잊다"},
        {"word": "mean", "meaning": "의미하다"},
        {"word": "agree", "meaning": "동의하다"},
        {"word": "disagree", "meaning": "동의하지 않다"},
        {"word": "opinion", "meaning": "의견"},
        {"word": "idea", "meaning": "생각, 아이디어"},
        {"word": "reason", "meaning": "이유"},
        {"word": "example", "meaning": "예시"},
        {"word": "fact", "meaning": "사실"},
        {"word": "choice", "meaning": "선택"},
        {"word": "decision", "meaning": "결정"},
        {"word": "advice", "meaning": "조언"},
        {"word": "suggestion", "meaning": "제안"},
        {"word": "possible", "meaning": "가능한"},
        {"word": "impossible", "meaning": "불가능한"},
        {"word": "confusing", "meaning": "혼란스러운"},
    ],

    "📅 계획과 약속": [
        {"word": "plan", "meaning": "계획"},
        {"word": "appointment", "meaning": "약속, 예약"},
        {"word": "promise", "meaning": "약속"},
        {"word": "meeting", "meaning": "모임, 회의"},
        {"word": "date", "meaning": "날짜, 데이트"},
        {"word": "event", "meaning": "행사"},
        {"word": "party", "meaning": "파티"},
        {"word": "festival", "meaning": "축제"},
        {"word": "deadline", "meaning": "마감일"},
        {"word": "calendar", "meaning": "달력"},
        {"word": "next week", "meaning": "다음 주"},
        {"word": "message", "meaning": "메시지"},
        {"word": "join", "meaning": "참여하다"},
        {"word": "prepare", "meaning": "준비하다"},
        {"word": "decide", "meaning": "결정하다"},
        {"word": "change", "meaning": "바꾸다"},
        {"word": "cancel", "meaning": "취소하다"},
        {"word": "on time", "meaning": "시간 맞춰"},
        {"word": "available", "meaning": "시간이 되는, 이용 가능한"},
        {"word": "reminder", "meaning": "알림"},
    ],

    "🩺 건강한 생활": [
        {"word": "health", "meaning": "건강"},
        {"word": "body", "meaning": "몸"},
        {"word": "eye", "meaning": "눈"},
        {"word": "ear", "meaning": "귀"},
        {"word": "nose", "meaning": "코"},
        {"word": "mouth", "meaning": "입"},
        {"word": "tooth", "meaning": "이"},
        {"word": "hand", "meaning": "손"},
        {"word": "arm", "meaning": "팔"},
        {"word": "leg", "meaning": "다리"},
        {"word": "foot", "meaning": "발"},
        {"word": "stomach", "meaning": "배, 위"},
        {"word": "back", "meaning": "등, 허리"},
        {"word": "heart", "meaning": "심장"},
        {"word": "clinic", "meaning": "의원, 진료소"},
        {"word": "vitamin", "meaning": "비타민"},
        {"word": "diet", "meaning": "식단"},
        {"word": "cough", "meaning": "기침"},
        {"word": "flu", "meaning": "독감"},
        {"word": "breathe", "meaning": "숨 쉬다"},
    ],

    "📱 미디어와 스마트폰": [
        {"word": "smartphone", "meaning": "스마트폰"},
        {"word": "screen", "meaning": "화면"},
        {"word": "app", "meaning": "앱"},
        {"word": "website", "meaning": "웹사이트"},
        {"word": "internet", "meaning": "인터넷"},
        {"word": "Wi-Fi", "meaning": "와이파이"},
        {"word": "password", "meaning": "비밀번호"},
        {"word": "text", "meaning": "문자 메시지"},
        {"word": "video call", "meaning": "영상 통화"},
        {"word": "gallery", "meaning": "사진첩"},
        {"word": "news", "meaning": "뉴스"},
        {"word": "channel", "meaning": "채널"},
        {"word": "post", "meaning": "게시물"},
        {"word": "comment", "meaning": "댓글"},
        {"word": "upload", "meaning": "업로드하다"},
        {"word": "download", "meaning": "다운로드하다"},
        {"word": "search", "meaning": "검색하다"},
        {"word": "click", "meaning": "클릭하다"},
        {"word": "battery", "meaning": "배터리"},
        {"word": "notification", "meaning": "알림"},
    ],

    "🌈 직업과 미래": [
        {"word": "job", "meaning": "직업"},
        {"word": "work", "meaning": "일하다"},
        {"word": "company", "meaning": "회사"},
        {"word": "office", "meaning": "사무실"},
        {"word": "factory", "meaning": "공장"},
        {"word": "engineer", "meaning": "기술자, 엔지니어"},
        {"word": "mechanic", "meaning": "정비사"},
        {"word": "chef", "meaning": "요리사"},
        {"word": "firefighter", "meaning": "소방관"},
        {"word": "farmer", "meaning": "농부"},
        {"word": "designer", "meaning": "디자이너"},
        {"word": "singer", "meaning": "가수"},
        {"word": "actor", "meaning": "배우"},
        {"word": "athlete", "meaning": "운동선수"},
        {"word": "dream", "meaning": "꿈"},
        {"word": "future", "meaning": "미래"},
        {"word": "goal", "meaning": "목표"},
        {"word": "skill", "meaning": "기술, 능력"},
        {"word": "interview", "meaning": "면접"},
        {"word": "experience", "meaning": "경험"},
    ],
}

# =========================
# 오늘의 일상 대화
# =========================
theme_dialogues = {
    "🏫 학교생활": [
        {"en": "A: What is your favorite subject?", "ko": "A: 네가 가장 좋아하는 과목은 뭐니?"},
        {"en": "B: My favorite subject is science.", "ko": "B: 내가 가장 좋아하는 과목은 과학이야."},
        {"en": "A: Do you have homework today?", "ko": "A: 오늘 숙제 있니?"},
        {"en": "B: Yes, I have a report.", "ko": "B: 응, 보고서가 있어."},
        {"en": "A: When is the presentation?", "ko": "A: 발표는 언제니?"},
        {"en": "B: It is next week.", "ko": "B: 다음 주야."},
    ],

    "✏️ 교실 활동": [
        {"en": "A: Please underline this word.", "ko": "A: 이 단어에 밑줄을 그어 주세요."},
        {"en": "B: Okay. I will underline it.", "ko": "B: 좋아요. 밑줄 칠게요."},
        {"en": "A: Can you repeat the sentence?", "ko": "A: 문장을 반복해 줄 수 있니?"},
        {"en": "B: Yes, I can repeat it.", "ko": "B: 네, 반복할 수 있어요."},
        {"en": "A: Please turn in your paper.", "ko": "A: 종이를 제출해 주세요."},
        {"en": "B: Sure. Here it is.", "ko": "B: 네. 여기 있어요."},
    ],

    "🏠 집과 생활": [
        {"en": "A: Where is your room?", "ko": "A: 네 방은 어디에 있니?"},
        {"en": "B: It is next to the living room.", "ko": "B: 거실 옆에 있어."},
        {"en": "A: Is your room clean?", "ko": "A: 네 방은 깨끗하니?"},
        {"en": "B: No, it is a little messy.", "ko": "B: 아니, 조금 지저분해."},
        {"en": "A: Can you clean it?", "ko": "A: 청소할 수 있니?"},
        {"en": "B: Yes, I can clean it today.", "ko": "B: 응, 오늘 청소할 수 있어."},
    ],

    "🌅 하루 일과": [
        {"en": "A: What time do you get up?", "ko": "A: 너는 몇 시에 일어나니?"},
        {"en": "B: I usually get up at seven.", "ko": "B: 나는 보통 7시에 일어나."},
        {"en": "A: What do you do after school?", "ko": "A: 방과 후에 무엇을 하니?"},
        {"en": "B: I relax and watch videos.", "ko": "B: 쉬면서 영상을 봐."},
        {"en": "A: Do you sleep early?", "ko": "A: 너는 일찍 자니?"},
        {"en": "B: No, I sometimes sleep late.", "ko": "B: 아니, 가끔 늦게 자."},
    ],

    "🎮 취미와 여가": [
        {"en": "A: What is your hobby?", "ko": "A: 네 취미는 뭐니?"},
        {"en": "B: My hobby is watching movies.", "ko": "B: 내 취미는 영화 보기야."},
        {"en": "A: Do you like music?", "ko": "A: 음악 좋아하니?"},
        {"en": "B: Yes, I like pop songs.", "ko": "B: 응, 나는 팝송을 좋아해."},
        {"en": "A: What do you do in your free time?", "ko": "A: 여가 시간에 무엇을 하니?"},
        {"en": "B: I play games and read comics.", "ko": "B: 게임하고 만화를 읽어."},
    ],

    "⚽ 운동과 활동": [
        {"en": "A: What sport do you like?", "ko": "A: 어떤 운동을 좋아하니?"},
        {"en": "B: I like tennis.", "ko": "B: 나는 테니스를 좋아해."},
        {"en": "A: Do you practice often?", "ko": "A: 자주 연습하니?"},
        {"en": "B: Yes, I practice after school.", "ko": "B: 응, 방과 후에 연습해."},
        {"en": "A: Did your team win?", "ko": "A: 너희 팀이 이겼니?"},
        {"en": "B: Yes, we won the match.", "ko": "B: 응, 우리는 경기에서 이겼어."},
    ],

    "🌦️ 날씨와 계절": [
        {"en": "A: How is the weather today?", "ko": "A: 오늘 날씨가 어때?"},
        {"en": "B: It is cloudy and windy.", "ko": "B: 흐리고 바람이 불어."},
        {"en": "A: Do you like winter?", "ko": "A: 겨울을 좋아하니?"},
        {"en": "B: No, I like spring.", "ko": "B: 아니, 나는 봄을 좋아해."},
        {"en": "A: Do you need an umbrella?", "ko": "A: 우산이 필요하니?"},
        {"en": "B: Yes, it may rain.", "ko": "B: 응, 비가 올지도 몰라."},
    ],

    "🌳 자연과 환경": [
        {"en": "A: Do you like nature?", "ko": "A: 자연을 좋아하니?"},
        {"en": "B: Yes, I like forests and lakes.", "ko": "B: 응, 나는 숲과 호수를 좋아해."},
        {"en": "A: What can we do for the environment?", "ko": "A: 환경을 위해 무엇을 할 수 있을까?"},
        {"en": "B: We can recycle plastic.", "ko": "B: 플라스틱을 재활용할 수 있어."},
        {"en": "A: Is pollution a problem?", "ko": "A: 오염은 문제니?"},
        {"en": "B: Yes, it is a big problem.", "ko": "B: 응, 큰 문제야."},
    ],

    "🍽️ 식당과 주문": [
        {"en": "A: Are you ready to order?", "ko": "A: 주문할 준비가 되셨나요?"},
        {"en": "B: Yes, I want pasta.", "ko": "B: 네, 파스타 주세요."},
        {"en": "A: Do you want a drink?", "ko": "A: 음료도 원하시나요?"},
        {"en": "B: Yes, I want juice.", "ko": "B: 네, 주스 주세요."},
        {"en": "A: How is the food?", "ko": "A: 음식은 어때요?"},
        {"en": "B: It is delicious.", "ko": "B: 맛있어요."},
    ],

    "🛍️ 쇼핑과 가격": [
        {"en": "A: Can I help you?", "ko": "A: 도와드릴까요?"},
        {"en": "B: Yes, I am looking for a bag.", "ko": "B: 네, 가방을 찾고 있어요."},
        {"en": "A: What color do you want?", "ko": "A: 어떤 색을 원하세요?"},
        {"en": "B: I want a black one.", "ko": "B: 검은색을 원해요."},
        {"en": "A: It is on sale today.", "ko": "A: 오늘 할인 중이에요."},
        {"en": "B: Great. I will buy it.", "ko": "B: 좋아요. 살게요."},
    ],

    "👕 옷과 외모": [
        {"en": "A: Do you like this jacket?", "ko": "A: 이 재킷 마음에 드니?"},
        {"en": "B: Yes, it looks comfortable.", "ko": "B: 응, 편해 보여."},
        {"en": "A: What size do you need?", "ko": "A: 어떤 사이즈가 필요하니?"},
        {"en": "B: I need a medium size.", "ko": "B: 중간 사이즈가 필요해."},
        {"en": "A: Are these sneakers new?", "ko": "A: 이 운동화는 새거니?"},
        {"en": "B: Yes, they are new.", "ko": "B: 응, 새거야."},
    ],

    "🚇 교통과 길 찾기": [
        {"en": "A: Where is the bus stop?", "ko": "A: 버스 정류장이 어디에 있나요?"},
        {"en": "B: Go straight and turn left.", "ko": "B: 똑바로 가서 왼쪽으로 도세요."},
        {"en": "A: Is the subway station far?", "ko": "A: 지하철역은 먼가요?"},
        {"en": "B: No, it is near here.", "ko": "B: 아니요, 여기 근처에 있어요."},
        {"en": "A: I think I am lost.", "ko": "A: 길을 잃은 것 같아요."},
        {"en": "B: I can help you.", "ko": "B: 제가 도와드릴 수 있어요."},
    ],

    "🧳 여행과 숙박": [
        {"en": "A: Do you have a reservation?", "ko": "A: 예약하셨나요?"},
        {"en": "B: Yes, I have a hotel reservation.", "ko": "B: 네, 호텔 예약이 있어요."},
        {"en": "A: May I see your passport?", "ko": "A: 여권을 볼 수 있을까요?"},
        {"en": "B: Sure. Here it is.", "ko": "B: 물론이죠. 여기 있어요."},
        {"en": "A: What time is check out?", "ko": "A: 체크아웃은 몇 시인가요?"},
        {"en": "B: It is at eleven.", "ko": "B: 11시입니다."},
    ],

    "👥 친구 관계": [
        {"en": "A: Do you want to hang out this weekend?", "ko": "A: 이번 주말에 같이 놀래?"},
        {"en": "B: Yes, that sounds fun.", "ko": "B: 응, 재미있겠다."},
        {"en": "A: Can I invite my friend?", "ko": "A: 내 친구도 초대해도 돼?"},
        {"en": "B: Sure. We can meet together.", "ko": "B: 물론이지. 같이 만날 수 있어."},
        {"en": "A: Thank you for helping me.", "ko": "A: 도와줘서 고마워."},
        {"en": "B: No problem. We are friends.", "ko": "B: 괜찮아. 우리는 친구잖아."},
    ],

    "😊 감정 표현 확장": [
        {"en": "A: You look nervous.", "ko": "A: 너 긴장해 보여."},
        {"en": "B: Yes, I have a presentation.", "ko": "B: 응, 발표가 있어."},
        {"en": "A: Don't worry. You can do it.", "ko": "A: 걱정하지 마. 너는 할 수 있어."},
        {"en": "B: Thank you. I feel better.", "ko": "B: 고마워. 기분이 나아졌어."},
        {"en": "A: Are you proud of yourself?", "ko": "A: 너 자신이 자랑스럽니?"},
        {"en": "B: Yes, I am proud.", "ko": "B: 응, 자랑스러워."},
    ],

    "💭 생각과 의견": [
        {"en": "A: What do you think about this idea?", "ko": "A: 이 생각에 대해 어떻게 생각하니?"},
        {"en": "B: I think it is useful.", "ko": "B: 유용하다고 생각해."},
        {"en": "A: Do you agree with me?", "ko": "A: 내 말에 동의하니?"},
        {"en": "B: Yes, I agree.", "ko": "B: 응, 동의해."},
        {"en": "A: Can you give me a reason?", "ko": "A: 이유를 말해 줄 수 있니?"},
        {"en": "B: Sure. It is simple and clear.", "ko": "B: 물론이지. 간단하고 명확해."},
    ],

    "📅 계획과 약속": [
        {"en": "A: Do you have plans this weekend?", "ko": "A: 이번 주말에 계획 있니?"},
        {"en": "B: Yes, I have a meeting.", "ko": "B: 응, 모임이 있어."},
        {"en": "A: Are you available tomorrow?", "ko": "A: 내일 시간 돼?"},
        {"en": "B: Yes, I am free in the afternoon.", "ko": "B: 응, 오후에 시간이 있어."},
        {"en": "A: Can we change the time?", "ko": "A: 시간을 바꿀 수 있을까?"},
        {"en": "B: Sure. No problem.", "ko": "B: 물론이지. 문제없어."},
    ],

    "🩺 건강한 생활": [
        {"en": "A: You look tired.", "ko": "A: 너 피곤해 보여."},
        {"en": "B: Yes, I did not sleep well.", "ko": "B: 응, 잠을 잘 못 잤어."},
        {"en": "A: You should rest.", "ko": "A: 쉬는 게 좋겠어."},
        {"en": "B: I know. I need more sleep.", "ko": "B: 알아. 잠이 더 필요해."},
        {"en": "A: Do you exercise often?", "ko": "A: 자주 운동하니?"},
        {"en": "B: Sometimes. I want to be healthy.", "ko": "B: 가끔. 건강해지고 싶어."},
    ],

    "📱 미디어와 스마트폰": [
        {"en": "A: What app do you use often?", "ko": "A: 어떤 앱을 자주 사용하니?"},
        {"en": "B: I often use a video app.", "ko": "B: 나는 영상 앱을 자주 사용해."},
        {"en": "A: Can you send me the link?", "ko": "A: 링크를 보내줄 수 있니?"},
        {"en": "B: Sure. I will send it now.", "ko": "B: 물론이지. 지금 보낼게."},
        {"en": "A: Is your battery low?", "ko": "A: 배터리가 부족하니?"},
        {"en": "B: Yes, I need to charge my phone.", "ko": "B: 응, 휴대폰을 충전해야 해."},
    ],

    "🌈 직업과 미래": [
        {"en": "A: What is your dream job?", "ko": "A: 네 꿈의 직업은 뭐니?"},
        {"en": "B: I want to be an engineer.", "ko": "B: 나는 엔지니어가 되고 싶어."},
        {"en": "A: What skill do you need?", "ko": "A: 어떤 기술이 필요하니?"},
        {"en": "B: I need computer skills.", "ko": "B: 컴퓨터 기술이 필요해."},
        {"en": "A: Do you have a goal?", "ko": "A: 목표가 있니?"},
        {"en": "B: Yes, I want to get a good job.", "ko": "B: 응, 좋은 직업을 얻고 싶어."},
    ],
}


# =========================
# 맨 앞 탭 전용 전체 카세트 듣기
# 브라우저 음성 엔진 사용: gTTS 긴 텍스트 오류 방지
# =========================
def flatten_all_words():
    all_items = []
    number = 1

    for theme_name, theme_words in word_themes.items():
        for item in theme_words:
            word = item["word"]
            all_items.append({
                "number": number,
                "theme": theme_name,
                "word": word,
                "meaning": item["meaning"],
                "emoji": get_word_emoji(word),
                "script": word
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
            "script": word
        })

    return theme_items

def make_daily_example(word, meaning="", theme=""):
    """
    전체 카세트에서 단어 뒤에 붙일 짧은 일상회화 문장입니다.
    너무 어색한 I like closet 같은 문장을 피하기 위해 자주 쓰는 단어는 따로 예문을 지정합니다.
    """
    examples = {
        "subject": "What is your favorite subject?",
        "math": "I have math today.",
        "science": "Science is interesting.",
        "history": "I study history at school.",
        "music": "I like listening to music.",
        "art": "Art class is fun.",
        "P.E.": "We have P.E. on Friday.",
        "club": "I joined a school club.",
        "schedule": "Let me check my schedule.",
        "semester": "This semester is busy.",
        "assignment": "I have an assignment today.",
        "project": "We are working on a project.",
        "presentation": "I have a presentation tomorrow.",
        "report": "I need to write a report.",
        "textbook": "Open your textbook.",
        "workbook": "Please finish your workbook.",
        "library": "I study in the library.",
        "cafeteria": "Let's meet at the cafeteria.",
        "hallway": "Do not run in the hallway.",
        "attendance": "The teacher checks attendance.",

        "copy": "Please copy this sentence.",
        "repeat": "Can you repeat that?",
        "underline": "Underline the important word.",
        "circle": "Circle the correct answer.",
        "choose": "Choose the best answer.",
        "check": "Please check your answer.",
        "match": "Match the word and picture.",
        "complete": "Complete the sentence.",
        "fill": "Fill in the blank.",
        "spell": "How do you spell your name?",
        "pronounce": "Please pronounce this word.",
        "review": "Let's review the lesson.",
        "explain": "Can you explain it again?",
        "describe": "Describe the picture.",
        "compare": "Compare the two answers.",
        "discuss": "Let's discuss this topic.",
        "present": "Please present your idea.",
        "take notes": "Take notes while you listen.",
        "turn in": "Turn in your paper.",
        "hand out": "Please hand out the worksheets.",

        "living room": "My family talks in the living room.",
        "bedroom": "My bedroom is small but cozy.",
        "kitchen": "My mom is in the kitchen.",
        "balcony": "I can see the street from the balcony.",
        "floor": "The floor is clean.",
        "wall": "There is a picture on the wall.",
        "roof": "The roof is red.",
        "garden": "There are flowers in the garden.",
        "yard": "The dog is in the yard.",
        "sofa": "I sit on the sofa.",
        "television": "I watch television at night.",
        "refrigerator": "The milk is in the refrigerator.",
        "microwave": "Please use the microwave.",
        "blanket": "I need a warm blanket.",
        "pillow": "This pillow is soft.",
        "towel": "I need a clean towel.",
        "soap": "Please wash your hands with soap.",
        "mirror": "I look in the mirror.",
        "closet": "My clothes are in the closet.",
        "trash": "Please take out the trash.",

        "routine": "This is my morning routine.",
        "wake up": "I wake up at seven.",
        "get up": "I get up early.",
        "brush": "I brush my teeth.",
        "shower": "I take a shower.",
        "dress": "I dress quickly in the morning.",
        "leave": "I leave home at eight.",
        "arrive": "I arrive at school on time.",
        "return": "I return home after school.",
        "finish": "I finish my homework.",
        "relax": "I relax after dinner.",
        "weekday": "I go to school on weekdays.",
        "weekend": "I sleep late on the weekend.",
        "usually": "I usually eat breakfast.",
        "often": "I often watch videos.",
        "sometimes": "I sometimes play soccer.",
        "always": "I always bring my phone.",
        "never": "I never skip breakfast.",
        "habit": "This is a good habit.",
        "lifestyle": "I want a healthy lifestyle.",

        "hobby": "My hobby is watching movies.",
        "movie": "Let's watch a movie.",
        "drama": "This drama is popular.",
        "song": "I like this song.",
        "concert": "I want to go to a concert.",
        "dance": "She likes to dance.",
        "drawing": "I enjoy drawing.",
        "painting": "This painting is beautiful.",
        "comic": "I read comics in my free time.",
        "novel": "This novel is interesting.",
        "photography": "I like photography.",
        "cooking": "Cooking is fun.",
        "baking": "My sister likes baking.",
        "camping": "We go camping in summer.",
        "hiking": "I go hiking with my friends.",
        "fishing": "My father likes fishing.",
        "free time": "What do you do in your free time?",
        "favorite": "This is my favorite song.",
        "popular": "This game is popular.",
        "relaxing": "This music is relaxing.",

        "soccer": "I play soccer after school.",
        "baseball": "Baseball is popular in Korea.",
        "basketball": "Let's play basketball.",
        "volleyball": "We play volleyball in P.E.",
        "tennis": "I like playing tennis.",
        "badminton": "Badminton is fun.",
        "swimming": "Swimming is good exercise.",
        "cycling": "Cycling is my favorite sport.",
        "skating": "Skating looks difficult.",
        "boxing": "Boxing is very hard.",
        "taekwondo": "Taekwondo is a Korean martial art.",
        "yoga": "Yoga helps me relax.",
        "fitness": "Fitness is important.",
        "field": "The players are on the field.",
        "court": "They are on the tennis court.",
        "stadium": "The stadium is crowded.",
        "coach": "The coach is kind.",
        "competition": "I joined a competition.",
        "medal": "She won a medal.",

        "season": "What is your favorite season?",
        "spring": "Spring is warm.",
        "summer": "Summer is hot.",
        "fall": "Fall is cool.",
        "winter": "Winter is cold.",
        "cloudy": "It is cloudy today.",
        "rainy": "It is rainy outside.",
        "snowy": "It is snowy in winter.",
        "windy": "It is windy today.",
        "stormy": "The weather is stormy.",
        "foggy": "It is foggy this morning.",
        "dry": "The air is dry.",
        "wet": "My shoes are wet.",
        "humid": "It is humid today.",
        "temperature": "The temperature is high.",
        "degree": "It is thirty degrees.",
        "forecast": "Check the weather forecast.",
        "umbrella": "I need an umbrella.",
        "raincoat": "Wear a raincoat.",
        "rainbow": "Look at the rainbow.",

        "nature": "I love nature.",
        "environment": "We should protect the environment.",
        "plant": "This plant needs water.",
        "forest": "The forest is quiet.",
        "lake": "The lake is beautiful.",
        "ocean": "The ocean is blue.",
        "island": "Jeju is a beautiful island.",
        "desert": "The desert is very hot.",
        "farm": "My uncle has a farm.",
        "village": "This village is quiet.",
        "leaf": "A leaf is falling.",
        "root": "The root is under the ground.",
        "stone": "There is a stone on the road.",
        "sand": "The sand is hot.",
        "soil": "Plants grow in soil.",
        "plastic": "Do not throw away plastic.",
        "recycle": "We should recycle bottles.",
        "protect": "We should protect nature.",
        "pollution": "Pollution is a serious problem.",

        "restaurant": "Let's go to a restaurant.",
        "menu": "Can I see the menu?",
        "seat": "Is this seat taken?",
        "waiter": "The waiter is friendly.",
        "waitress": "The waitress brought water.",
        "order": "I want to order pizza.",
        "dish": "This dish is delicious.",
        "meal": "Enjoy your meal.",
        "soup": "This soup is hot.",
        "salad": "I want a salad.",
        "steak": "The steak smells good.",
        "pizza": "I like pizza.",
        "pasta": "I want pasta.",
        "burger": "This burger is big.",
        "sandwich": "I made a sandwich.",
        "dessert": "Do you want dessert?",
        "spicy": "This food is spicy.",
        "sweet": "This cake is sweet.",
        "bill": "Can I have the bill?",
        "receipt": "Can I get a receipt?",

        "shop": "Let's go to the shop.",
        "market": "I bought fruit at the market.",
        "mall": "The mall is crowded.",
        "supermarket": "I go to the supermarket.",
        "cashier": "Pay the cashier.",
        "customer": "The customer is waiting.",
        "price": "What is the price?",
        "sale": "This shirt is on sale.",
        "discount": "Can I get a discount?",
        "coupon": "I have a coupon.",
        "change": "Here is your change.",
        "coin": "I found a coin.",
        "expensive": "This bag is expensive.",
        "cheap": "This pen is cheap.",
        "size": "What size do you need?",
        "color": "What color do you like?",
        "brand": "This brand is famous.",
        "exchange": "Can I exchange this?",
        "refund": "Can I get a refund?",

        "T-shirt": "I wear a T-shirt.",
        "pants": "These pants are comfortable.",
        "jeans": "I like these jeans.",
        "shorts": "I wear shorts in summer.",
        "skirt": "This skirt is pretty.",
        "dress": "She wears a dress.",
        "jacket": "I need a jacket.",
        "coat": "Wear a coat in winter.",
        "sweater": "This sweater is warm.",
        "hoodie": "I like this hoodie.",
        "uniform": "Students wear uniforms.",
        "socks": "I need clean socks.",
        "sneakers": "These sneakers are new.",
        "boots": "I wear boots in winter.",
        "sandals": "I wear sandals in summer.",
        "scarf": "This scarf is warm.",
        "gloves": "I need gloves.",
        "belt": "He wears a belt.",
        "glasses": "She wears glasses.",
        "comfortable": "These shoes are comfortable.",

        "bus stop": "Where is the bus stop?",
        "subway": "I take the subway.",
        "airport": "I go to the airport.",
        "terminal": "The bus terminal is near here.",
        "platform": "Wait on the platform.",
        "route": "This is the bus route.",
        "direction": "Which direction should I go?",
        "straight": "Go straight.",
        "corner": "Turn at the corner.",
        "block": "Walk two blocks.",
        "traffic": "There is heavy traffic.",
        "crosswalk": "Use the crosswalk.",
        "sidewalk": "Walk on the sidewalk.",
        "bridge": "Cross the bridge.",
        "tunnel": "Go through the tunnel.",
        "entrance": "Where is the entrance?",
        "exit": "Where is the exit?",
        "transfer": "I need to transfer.",
        "lost": "I think I am lost.",
        "guide": "The guide is helpful.",

        "travel": "I want to travel.",
        "trip": "Have a nice trip.",
        "vacation": "I need a vacation.",
        "tourist": "Many tourists visit Seoul.",
        "passport": "I need my passport.",
        "flight": "My flight is at three.",
        "hotel": "I booked a hotel.",
        "motel": "We stayed at a motel.",
        "hostel": "A hostel is cheaper.",
        "reservation": "I have a reservation.",
        "check in": "I want to check in.",
        "check out": "What time is check out?",
        "luggage": "My luggage is heavy.",
        "suitcase": "This suitcase is big.",
        "backpack": "I carry a backpack.",
        "souvenir": "I bought a souvenir.",
        "museum": "Let's visit the museum.",
        "famous": "This place is famous.",
        "local": "Try the local food.",

        "friendship": "Friendship is important.",
        "best friend": "He is my best friend.",
        "teammate": "She is my teammate.",
        "partner": "Work with your partner.",
        "message": "Send me a message.",
        "call": "Can I call you?",
        "chat": "Let's chat later.",
        "invite": "I want to invite you.",
        "visit": "Please visit my house.",
        "meet": "Nice to meet you.",
        "hang out": "Let's hang out after school.",
        "laugh": "We laugh together.",
        "share": "Please share your idea.",
        "trust": "I trust my friend.",
        "promise": "I made a promise.",
        "secret": "Can you keep a secret?",
        "joke": "That joke is funny.",
        "together": "Let's study together.",
        "alone": "I am alone at home.",
        "forgive": "Please forgive me.",

        "excited": "I am excited.",
        "nervous": "I am nervous.",
        "bored": "I am bored.",
        "surprised": "I am surprised.",
        "confused": "I am confused.",
        "embarrassed": "I am embarrassed.",
        "proud": "I am proud of you.",
        "disappointed": "I am disappointed.",
        "lonely": "I feel lonely.",
        "relaxed": "I feel relaxed.",
        "calm": "Stay calm.",
        "upset": "I am upset.",
        "interested": "I am interested in music.",
        "satisfied": "I am satisfied.",
        "thankful": "I am thankful.",
        "hopeful": "I feel hopeful.",
        "mood": "I am in a good mood.",
        "stress": "I have a lot of stress.",
        "confidence": "Confidence is important.",
        "courage": "You have courage.",

        "think": "What do you think?",
        "believe": "I believe you.",
        "guess": "Can you guess?",
        "remember": "I remember your name.",
        "forget": "Do not forget your homework.",
        "mean": "What does this mean?",
        "agree": "I agree with you.",
        "disagree": "I disagree with him.",
        "opinion": "What is your opinion?",
        "idea": "That is a good idea.",
        "reason": "What is the reason?",
        "example": "Give me an example.",
        "fact": "That is a fact.",
        "choice": "This is your choice.",
        "decision": "I made a decision.",
        "advice": "I need your advice.",
        "suggestion": "Thank you for your suggestion.",
        "possible": "It is possible.",
        "impossible": "It is impossible.",
        "confusing": "This question is confusing.",

        "plan": "What is your plan?",
        "appointment": "I have an appointment.",
        "meeting": "I have a meeting.",
        "date": "What is the date today?",
        "event": "This event is fun.",
        "party": "I am going to a party.",
        "festival": "The festival starts today.",
        "deadline": "The deadline is tomorrow.",
        "calendar": "Check your calendar.",
        "next week": "See you next week.",
        "join": "Can I join you?",
        "prepare": "I need to prepare.",
        "decide": "Please decide now.",
        "cancel": "I need to cancel it.",
        "on time": "Please come on time.",
        "available": "Are you available today?",
        "reminder": "Set a reminder.",

        "health": "Health is important.",
        "body": "My body feels tired.",
        "eye": "My eye hurts.",
        "ear": "My ear hurts.",
        "nose": "My nose is runny.",
        "mouth": "Open your mouth.",
        "tooth": "My tooth hurts.",
        "hand": "Raise your hand.",
        "arm": "My arm hurts.",
        "leg": "My leg hurts.",
        "foot": "My foot hurts.",
        "stomach": "My stomach hurts.",
        "back": "My back hurts.",
        "heart": "My heart is beating fast.",
        "clinic": "I went to the clinic.",
        "vitamin": "I take vitamins.",
        "diet": "I need a healthy diet.",
        "cough": "I have a cough.",
        "flu": "I have the flu.",
        "breathe": "Breathe slowly.",

        "smartphone": "I use my smartphone.",
        "screen": "The screen is bright.",
        "app": "Open the app.",
        "website": "Visit the website.",
        "internet": "The internet is slow.",
        "Wi-Fi": "Do you have Wi-Fi?",
        "password": "What is the password?",
        "text": "Send me a text.",
        "video call": "Let's have a video call.",
        "gallery": "Check your gallery.",
        "news": "I watch the news.",
        "channel": "Change the channel.",
        "post": "I wrote a post.",
        "comment": "Leave a comment.",
        "upload": "Upload the photo.",
        "download": "Download the file.",
        "search": "Search for the word.",
        "click": "Click the button.",
        "battery": "My battery is low.",
        "notification": "I got a notification.",

        "job": "I want a good job.",
        "work": "I work hard.",
        "company": "He works at a company.",
        "office": "She works in an office.",
        "factory": "My father works in a factory.",
        "engineer": "I want to be an engineer.",
        "mechanic": "A mechanic fixes cars.",
        "chef": "The chef cooks well.",
        "firefighter": "A firefighter helps people.",
        "farmer": "A farmer grows food.",
        "designer": "She is a designer.",
        "singer": "He is a singer.",
        "actor": "She is an actor.",
        "athlete": "He is an athlete.",
        "dream": "What is your dream?",
        "future": "Think about your future.",
        "goal": "My goal is clear.",
        "skill": "This skill is useful.",
        "interview": "I have an interview.",
        "experience": "This is a good experience.",
    }

    if word in examples:
        return examples[word]

    if "집" in theme:
        return f"I use the {word} at home."
    if "학교" in theme or "교실" in theme:
        return f"We use {word} in class."
    if "식당" in theme or "쇼핑" in theme:
        return f"I need {word}, please."
    if "교통" in theme or "여행" in theme:
        return f"I need help with {word}."
    if "감정" in theme:
        return f"I feel {word} today."
    if "운동" in theme:
        return f"I like {word}."
    if "건강" in theme:
        return f"My {word} is important."

    return f"I use the word {word} in daily English."


def make_daily_example_ko(word, meaning="", theme=""):
    """
    전체 카세트 목록에서 예시 문장의 한국어 뜻을 보여 주기 위한 함수입니다.
    주요 단어는 자연스러운 한국어 번역을 따로 지정하고,
    없는 경우에는 단어 뜻을 활용한 안내 문장을 보여 줍니다.
    """
    examples_ko = {
        # 학교생활
        "subject": "네가 가장 좋아하는 과목은 뭐니?",
        "math": "나는 오늘 수학 수업이 있어.",
        "science": "과학은 흥미로워.",
        "history": "나는 학교에서 역사를 공부해.",
        "music": "나는 음악 듣는 것을 좋아해.",
        "art": "미술 수업은 재미있어.",
        "P.E.": "우리는 금요일에 체육 수업이 있어.",
        "club": "나는 학교 동아리에 가입했어.",
        "schedule": "내 일정을 확인해 볼게.",
        "semester": "이번 학기는 바빠.",
        "assignment": "나는 오늘 과제가 있어.",
        "project": "우리는 프로젝트를 하고 있어.",
        "presentation": "나는 내일 발표가 있어.",
        "report": "나는 보고서를 써야 해.",
        "textbook": "교과서를 펴세요.",
        "workbook": "문제집을 끝내 주세요.",
        "library": "나는 도서관에서 공부해.",
        "cafeteria": "급식소에서 만나자.",
        "hallway": "복도에서 뛰지 마세요.",
        "attendance": "선생님께서 출석을 확인하신다.",

        # 교실 활동
        "copy": "이 문장을 베껴 쓰세요.",
        "repeat": "다시 말해 줄 수 있니?",
        "underline": "중요한 단어에 밑줄을 그으세요.",
        "circle": "정답에 동그라미 치세요.",
        "choose": "가장 좋은 답을 고르세요.",
        "check": "네 답을 확인해 보세요.",
        "match": "단어와 그림을 연결하세요.",
        "complete": "문장을 완성하세요.",
        "fill": "빈칸을 채우세요.",
        "spell": "네 이름 철자를 어떻게 쓰니?",
        "pronounce": "이 단어를 발음해 보세요.",
        "review": "수업 내용을 복습합시다.",
        "explain": "다시 설명해 줄 수 있니?",
        "describe": "그림을 묘사해 보세요.",
        "compare": "두 답을 비교해 보세요.",
        "discuss": "이 주제에 대해 토론해 봅시다.",
        "present": "네 생각을 발표해 보세요.",
        "take notes": "들으면서 필기하세요.",
        "turn in": "종이를 제출하세요.",
        "hand out": "학습지를 나누어 주세요.",

        # 집과 생활
        "living room": "우리 가족은 거실에서 이야기를 나눈다.",
        "bedroom": "내 침실은 작지만 아늑해.",
        "kitchen": "엄마는 부엌에 계셔.",
        "balcony": "나는 발코니에서 거리를 볼 수 있어.",
        "floor": "바닥이 깨끗해.",
        "wall": "벽에 그림이 있어.",
        "roof": "지붕은 빨간색이야.",
        "garden": "정원에 꽃들이 있어.",
        "yard": "개가 마당에 있어.",
        "sofa": "나는 소파에 앉아.",
        "television": "나는 밤에 텔레비전을 봐.",
        "refrigerator": "우유는 냉장고 안에 있어.",
        "microwave": "전자레인지를 사용하세요.",
        "blanket": "나는 따뜻한 담요가 필요해.",
        "pillow": "이 베개는 부드러워.",
        "towel": "나는 깨끗한 수건이 필요해.",
        "soap": "비누로 손을 씻으세요.",
        "mirror": "나는 거울을 봐.",
        "closet": "내 옷은 옷장 안에 있어.",
        "trash": "쓰레기를 내다 버려 주세요.",

        # 하루 일과
        "routine": "이것은 나의 아침 일과야.",
        "wake up": "나는 7시에 잠에서 깨.",
        "get up": "나는 일찍 일어나.",
        "brush": "나는 이를 닦아.",
        "shower": "나는 샤워를 해.",
        "dress": "나는 아침에 빨리 옷을 입어.",
        "leave": "나는 8시에 집을 떠나.",
        "arrive": "나는 학교에 제시간에 도착해.",
        "return": "나는 방과 후에 집으로 돌아와.",
        "finish": "나는 숙제를 끝내.",
        "relax": "나는 저녁 식사 후에 쉬어.",
        "weekday": "나는 평일에 학교에 가.",
        "weekend": "나는 주말에 늦게 자.",
        "usually": "나는 보통 아침을 먹어.",
        "often": "나는 자주 영상을 봐.",
        "sometimes": "나는 가끔 축구를 해.",
        "always": "나는 항상 휴대폰을 가져와.",
        "never": "나는 절대 아침을 거르지 않아.",
        "habit": "이것은 좋은 습관이야.",
        "lifestyle": "나는 건강한 생활 방식을 원해.",

        # 취미와 여가
        "hobby": "내 취미는 영화 보기야.",
        "movie": "영화 보자.",
        "drama": "이 드라마는 인기가 있어.",
        "song": "나는 이 노래를 좋아해.",
        "concert": "나는 콘서트에 가고 싶어.",
        "dance": "그녀는 춤추는 것을 좋아해.",
        "drawing": "나는 그림 그리기를 즐겨.",
        "painting": "이 그림은 아름다워.",
        "comic": "나는 여가 시간에 만화를 읽어.",
        "novel": "이 소설은 흥미로워.",
        "photography": "나는 사진 촬영을 좋아해.",
        "cooking": "요리는 재미있어.",
        "baking": "내 여동생은 빵 굽기를 좋아해.",
        "camping": "우리는 여름에 캠핑을 가.",
        "hiking": "나는 친구들과 하이킹을 가.",
        "fishing": "아버지는 낚시를 좋아하셔.",
        "free time": "너는 여가 시간에 무엇을 하니?",
        "favorite": "이것은 내가 가장 좋아하는 노래야.",
        "popular": "이 게임은 인기가 있어.",
        "relaxing": "이 음악은 편안해.",

        # 운동과 활동
        "soccer": "나는 방과 후에 축구를 해.",
        "baseball": "야구는 한국에서 인기가 있어.",
        "basketball": "농구하자.",
        "volleyball": "우리는 체육 시간에 배구를 해.",
        "tennis": "나는 테니스 치는 것을 좋아해.",
        "badminton": "배드민턴은 재미있어.",
        "swimming": "수영은 좋은 운동이야.",
        "cycling": "자전거 타기는 내가 가장 좋아하는 운동이야.",
        "skating": "스케이트 타기는 어려워 보여.",
        "boxing": "복싱은 매우 힘들어.",
        "taekwondo": "태권도는 한국 무술이야.",
        "yoga": "요가는 내가 쉬는 데 도움이 돼.",
        "fitness": "체력 운동은 중요해.",
        "field": "선수들이 경기장에 있어.",
        "court": "그들은 테니스 코트에 있어.",
        "stadium": "경기장이 붐벼.",
        "coach": "코치는 친절해.",
        "competition": "나는 대회에 참가했어.",
        "medal": "그녀는 메달을 땄어.",

        # 날씨와 계절
        "season": "네가 가장 좋아하는 계절은 뭐니?",
        "spring": "봄은 따뜻해.",
        "summer": "여름은 더워.",
        "fall": "가을은 시원해.",
        "winter": "겨울은 추워.",
        "cloudy": "오늘은 흐려.",
        "rainy": "밖에 비가 와.",
        "snowy": "겨울에는 눈이 와.",
        "windy": "오늘은 바람이 불어.",
        "stormy": "날씨가 폭풍우 쳐.",
        "foggy": "오늘 아침은 안개가 꼈어.",
        "dry": "공기가 건조해.",
        "wet": "내 신발이 젖었어.",
        "humid": "오늘은 습해.",
        "temperature": "기온이 높아.",
        "degree": "30도야.",
        "forecast": "일기예보를 확인해.",
        "umbrella": "나는 우산이 필요해.",
        "raincoat": "비옷을 입어.",
        "rainbow": "무지개를 봐.",

        # 자연과 환경
        "nature": "나는 자연을 사랑해.",
        "environment": "우리는 환경을 보호해야 해.",
        "plant": "이 식물은 물이 필요해.",
        "forest": "숲은 조용해.",
        "lake": "호수는 아름다워.",
        "ocean": "바다는 파래.",
        "island": "제주는 아름다운 섬이야.",
        "desert": "사막은 매우 더워.",
        "farm": "우리 삼촌은 농장을 가지고 있어.",
        "village": "이 마을은 조용해.",
        "leaf": "잎이 떨어지고 있어.",
        "root": "뿌리는 땅 아래에 있어.",
        "stone": "도로 위에 돌이 있어.",
        "sand": "모래가 뜨거워.",
        "soil": "식물은 흙에서 자라.",
        "plastic": "플라스틱을 버리지 마세요.",
        "recycle": "우리는 병을 재활용해야 해.",
        "protect": "우리는 자연을 보호해야 해.",
        "pollution": "오염은 심각한 문제야.",

        # 식당과 주문
        "restaurant": "식당에 가자.",
        "menu": "메뉴를 볼 수 있을까요?",
        "seat": "이 자리 사용 중인가요?",
        "waiter": "남자 종업원이 친절해.",
        "waitress": "여자 종업원이 물을 가져왔어.",
        "order": "나는 피자를 주문하고 싶어.",
        "dish": "이 요리는 맛있어.",
        "meal": "맛있게 드세요.",
        "soup": "이 수프는 뜨거워.",
        "salad": "나는 샐러드를 원해.",
        "steak": "스테이크 냄새가 좋아.",
        "pizza": "나는 피자를 좋아해.",
        "pasta": "나는 파스타를 원해.",
        "burger": "이 버거는 커.",
        "sandwich": "나는 샌드위치를 만들었어.",
        "dessert": "디저트 먹을래?",
        "spicy": "이 음식은 매워.",
        "sweet": "이 케이크는 달아.",
        "bill": "계산서를 받을 수 있을까요?",
        "receipt": "영수증을 받을 수 있을까요?",

        # 쇼핑과 가격
        "shop": "가게에 가자.",
        "market": "나는 시장에서 과일을 샀어.",
        "mall": "쇼핑몰이 붐벼.",
        "supermarket": "나는 슈퍼마켓에 가.",
        "cashier": "계산원에게 계산하세요.",
        "customer": "손님이 기다리고 있어.",
        "price": "가격이 얼마인가요?",
        "sale": "이 셔츠는 할인 중이야.",
        "discount": "할인 받을 수 있을까요?",
        "coupon": "나는 쿠폰이 있어.",
        "change": "여기 거스름돈입니다.",
        "coin": "나는 동전을 찾았어.",
        "expensive": "이 가방은 비싸.",
        "cheap": "이 펜은 싸.",
        "size": "어떤 사이즈가 필요하세요?",
        "color": "무슨 색을 좋아하세요?",
        "brand": "이 브랜드는 유명해.",
        "exchange": "이것을 교환할 수 있을까요?",
        "refund": "환불 받을 수 있을까요?",

        # 옷과 외모
        "T-shirt": "나는 티셔츠를 입어.",
        "pants": "이 바지는 편안해.",
        "jeans": "나는 이 청바지를 좋아해.",
        "shorts": "나는 여름에 반바지를 입어.",
        "skirt": "이 치마는 예뻐.",
        "dress": "그녀는 원피스를 입어.",
        "jacket": "나는 재킷이 필요해.",
        "coat": "겨울에는 코트를 입어.",
        "sweater": "이 스웨터는 따뜻해.",
        "hoodie": "나는 이 후드티를 좋아해.",
        "uniform": "학생들은 교복을 입어.",
        "socks": "나는 깨끗한 양말이 필요해.",
        "sneakers": "이 운동화는 새거야.",
        "boots": "나는 겨울에 부츠를 신어.",
        "sandals": "나는 여름에 샌들을 신어.",
        "scarf": "이 목도리는 따뜻해.",
        "gloves": "나는 장갑이 필요해.",
        "belt": "그는 벨트를 착용해.",
        "glasses": "그녀는 안경을 써.",
        "comfortable": "이 신발은 편안해.",

        # 교통과 길 찾기
        "bus stop": "버스 정류장이 어디에 있나요?",
        "subway": "나는 지하철을 타.",
        "airport": "나는 공항에 가.",
        "terminal": "버스 터미널은 여기 근처에 있어.",
        "platform": "승강장에서 기다리세요.",
        "route": "이것은 버스 경로야.",
        "direction": "어느 방향으로 가야 하나요?",
        "straight": "똑바로 가세요.",
        "corner": "모퉁이에서 도세요.",
        "block": "두 블록 걸어가세요.",
        "traffic": "교통이 매우 혼잡해.",
        "crosswalk": "횡단보도를 이용하세요.",
        "sidewalk": "인도로 걸으세요.",
        "bridge": "다리를 건너세요.",
        "tunnel": "터널을 지나가세요.",
        "entrance": "입구가 어디인가요?",
        "exit": "출구가 어디인가요?",
        "transfer": "나는 갈아타야 해.",
        "lost": "나는 길을 잃은 것 같아.",
        "guide": "안내자가 도움이 돼.",

        # 여행과 숙박
        "travel": "나는 여행하고 싶어.",
        "trip": "좋은 여행 되세요.",
        "vacation": "나는 휴가가 필요해.",
        "tourist": "많은 관광객들이 서울을 방문해.",
        "passport": "나는 여권이 필요해.",
        "flight": "내 항공편은 3시야.",
        "hotel": "나는 호텔을 예약했어.",
        "motel": "우리는 모텔에 묵었어.",
        "hostel": "호스텔은 더 저렴해.",
        "reservation": "나는 예약이 있어.",
        "check in": "체크인하고 싶어요.",
        "check out": "체크아웃 시간이 언제인가요?",
        "luggage": "내 짐은 무거워.",
        "suitcase": "이 여행 가방은 커.",
        "backpack": "나는 배낭을 메고 다녀.",
        "souvenir": "나는 기념품을 샀어.",
        "museum": "박물관에 가자.",
        "famous": "이곳은 유명해.",
        "local": "현지 음식을 먹어 봐.",

        # 친구 관계
        "friendship": "우정은 중요해.",
        "best friend": "그는 내 가장 친한 친구야.",
        "teammate": "그녀는 내 팀 동료야.",
        "partner": "짝과 함께 활동하세요.",
        "message": "나에게 메시지를 보내.",
        "call": "너에게 전화해도 될까?",
        "chat": "나중에 채팅하자.",
        "invite": "나는 너를 초대하고 싶어.",
        "visit": "우리 집에 방문해 주세요.",
        "meet": "만나서 반가워.",
        "hang out": "방과 후에 같이 놀자.",
        "laugh": "우리는 함께 웃어.",
        "share": "네 생각을 나눠 주세요.",
        "trust": "나는 내 친구를 믿어.",
        "promise": "나는 약속을 했어.",
        "secret": "비밀을 지켜 줄 수 있니?",
        "joke": "그 농담은 웃겨.",
        "together": "함께 공부하자.",
        "alone": "나는 집에 혼자 있어.",
        "forgive": "나를 용서해 주세요.",

        # 감정 표현
        "excited": "나는 신이 났어.",
        "nervous": "나는 긴장돼.",
        "bored": "나는 지루해.",
        "surprised": "나는 놀랐어.",
        "confused": "나는 혼란스러워.",
        "embarrassed": "나는 당황했어.",
        "proud": "나는 네가 자랑스러워.",
        "disappointed": "나는 실망했어.",
        "lonely": "나는 외로워.",
        "relaxed": "나는 편안해.",
        "calm": "침착해.",
        "upset": "나는 속상해.",
        "interested": "나는 음악에 관심이 있어.",
        "satisfied": "나는 만족해.",
        "thankful": "나는 감사해.",
        "hopeful": "나는 희망적이야.",
        "mood": "나는 기분이 좋아.",
        "stress": "나는 스트레스가 많아.",
        "confidence": "자신감은 중요해.",
        "courage": "너는 용기가 있어.",

        # 생각과 의견
        "think": "너는 어떻게 생각해?",
        "believe": "나는 너를 믿어.",
        "guess": "추측해 볼 수 있니?",
        "remember": "나는 네 이름을 기억해.",
        "forget": "숙제를 잊지 마.",
        "mean": "이것은 무슨 뜻이야?",
        "agree": "나는 너에게 동의해.",
        "disagree": "나는 그에게 동의하지 않아.",
        "opinion": "네 의견은 뭐야?",
        "idea": "그것은 좋은 생각이야.",
        "reason": "이유가 뭐야?",
        "example": "예를 들어 줘.",
        "fact": "그것은 사실이야.",
        "choice": "이것은 너의 선택이야.",
        "decision": "나는 결정을 내렸어.",
        "advice": "나는 네 조언이 필요해.",
        "suggestion": "네 제안 고마워.",
        "possible": "그것은 가능해.",
        "impossible": "그것은 불가능해.",
        "confusing": "이 문제는 혼란스러워.",

        # 계획과 약속
        "plan": "네 계획은 뭐야?",
        "appointment": "나는 약속이 있어.",
        "meeting": "나는 회의가 있어.",
        "date": "오늘 날짜가 뭐야?",
        "event": "이 행사는 재미있어.",
        "party": "나는 파티에 갈 거야.",
        "festival": "축제가 오늘 시작해.",
        "deadline": "마감일은 내일이야.",
        "calendar": "달력을 확인해.",
        "next week": "다음 주에 보자.",
        "join": "나도 함께해도 될까?",
        "prepare": "나는 준비해야 해.",
        "decide": "지금 결정해 주세요.",
        "cancel": "나는 그것을 취소해야 해.",
        "on time": "제시간에 와 주세요.",
        "available": "오늘 시간 돼?",
        "reminder": "알림을 설정해.",

        # 건강한 생활
        "health": "건강은 중요해.",
        "body": "내 몸이 피곤해.",
        "eye": "내 눈이 아파.",
        "ear": "내 귀가 아파.",
        "nose": "내 코가 막혔어.",
        "mouth": "입을 벌리세요.",
        "tooth": "내 이가 아파.",
        "hand": "손을 드세요.",
        "arm": "내 팔이 아파.",
        "leg": "내 다리가 아파.",
        "foot": "내 발이 아파.",
        "stomach": "내 배가 아파.",
        "back": "내 등이 아파.",
        "heart": "내 심장이 빨리 뛰어.",
        "clinic": "나는 의원에 갔어.",
        "vitamin": "나는 비타민을 먹어.",
        "diet": "나는 건강한 식단이 필요해.",
        "cough": "나는 기침이 나.",
        "flu": "나는 독감에 걸렸어.",
        "breathe": "천천히 숨 쉬어.",

        # 미디어와 스마트폰
        "smartphone": "나는 스마트폰을 사용해.",
        "screen": "화면이 밝아.",
        "app": "앱을 열어.",
        "website": "웹사이트를 방문해.",
        "internet": "인터넷이 느려.",
        "Wi-Fi": "와이파이가 있나요?",
        "password": "비밀번호가 뭐예요?",
        "text": "나에게 문자 보내.",
        "video call": "영상 통화를 하자.",
        "gallery": "사진첩을 확인해.",
        "news": "나는 뉴스를 봐.",
        "channel": "채널을 바꿔.",
        "post": "나는 게시물을 썼어.",
        "comment": "댓글을 남겨.",
        "upload": "사진을 업로드해.",
        "download": "파일을 다운로드해.",
        "search": "그 단어를 검색해.",
        "click": "버튼을 클릭해.",
        "battery": "내 배터리가 부족해.",
        "notification": "나는 알림을 받았어.",

        # 직업과 미래
        "job": "나는 좋은 직업을 원해.",
        "work": "나는 열심히 일해.",
        "company": "그는 회사에서 일해.",
        "office": "그녀는 사무실에서 일해.",
        "factory": "아버지는 공장에서 일하셔.",
        "engineer": "나는 엔지니어가 되고 싶어.",
        "mechanic": "정비사는 자동차를 고친다.",
        "chef": "요리사는 요리를 잘해.",
        "firefighter": "소방관은 사람들을 도와.",
        "farmer": "농부는 음식을 기른다.",
        "designer": "그녀는 디자이너야.",
        "singer": "그는 가수야.",
        "actor": "그녀는 배우야.",
        "athlete": "그는 운동선수야.",
        "dream": "네 꿈은 뭐야?",
        "future": "너의 미래에 대해 생각해.",
        "goal": "내 목표는 분명해.",
        "skill": "이 기술은 유용해.",
        "interview": "나는 면접이 있어.",
        "experience": "이것은 좋은 경험이야.",
    }

    return examples_ko.get(
        word,
        f"이 문장은 '{meaning}'이라는 뜻의 단어를 사용한 일상 영어 문장입니다."
    )

def browser_easy_cassette_player(all_items, title="📼 단어 카세트", intro="재생 버튼을 누르면 단어가 차례대로 재생됩니다.", height=600, word_repeat_each=1):
    """
    보기 편한 카세트 플레이어.
    - 큰 재생 버튼
    - 현재 단어/뜻 크게 표시
    - 속도/반복 횟수 선택
    - 현재 단어 다시 듣기
    - 모바일에서도 버튼이 잘리지 않도록 반응형 처리
    """

    player_id = f"easy_cassette_{uuid.uuid4().hex}"
    play_btn_id = f"play_{uuid.uuid4().hex}"
    pause_btn_id = f"pause_{uuid.uuid4().hex}"
    replay_btn_id = f"replay_{uuid.uuid4().hex}"
    prev_btn_id = f"prev_{uuid.uuid4().hex}"
    next_btn_id = f"next_{uuid.uuid4().hex}"
    stop_btn_id = f"stop_{uuid.uuid4().hex}"
    progress_id = f"progress_{uuid.uuid4().hex}"
    visual_bar_id = f"bar_{uuid.uuid4().hex}"
    percent_id = f"percent_{uuid.uuid4().hex}"
    status_id = f"status_{uuid.uuid4().hex}"
    word_id = f"word_{uuid.uuid4().hex}"
    meaning_id = f"meaning_{uuid.uuid4().hex}"
    count_id = f"count_{uuid.uuid4().hex}"
    theme_id = f"theme_{uuid.uuid4().hex}"
    speed_select_id = f"speed_{uuid.uuid4().hex}"
    repeat_select_id = f"repeat_{uuid.uuid4().hex}"
    wrap_id = f"wrap_{uuid.uuid4().hex}"

    cassette_json = json.dumps(all_items, ensure_ascii=False)
    safe_player_id = json.dumps(player_id)
    safe_title = html.escape(title)
    safe_intro = html.escape(intro)
    max_index = max(len(all_items) - 1, 0)
    word_repeat_each = max(1, int(word_repeat_each))

    components.html(
        f"""
        <style>
            .easy-cassette-wrap {{
                font-family: Arial, sans-serif;
                width: 100%;
                max-width: 100%;
                box-sizing: border-box;
                overflow: hidden;
                border-radius: 20px;
                padding: 14px;
                background: linear-gradient(135deg, #eff6ff 0%, #fff7ed 48%, #fdf2f8 100%);
                border: 1px solid #bae6fd;
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
            }}
            .easy-cassette-top {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
                flex-wrap: wrap;
                margin-bottom: 12px;
            }}
            .easy-cassette-title {{
                font-size: 16px;
                font-weight: 900;
                color: #0f172a;
                line-height: 1.25;
            }}
            .easy-cassette-small {{
                font-size: 13px;
                font-weight: 900;
                color: #475569;
                background: rgba(255,255,255,0.75);
                border: 1px solid #dbeafe;
                border-radius: 999px;
                padding: 7px 12px;
            }}
            .easy-now-card {{
                background: rgba(255,255,255,0.86);
                border: 1px solid #dbeafe;
                border-radius: 24px;
                padding: 18px 18px;
                margin: 12px 0;
                box-sizing: border-box;
            }}
            .easy-theme {{
                display: inline-block;
                font-size: 13px;
                font-weight: 900;
                color: #7c3aed;
                background: #f3e8ff;
                border-radius: 999px;
                padding: 6px 11px;
                margin-bottom: 9px;
            }}
            .easy-word {{
                font-size: clamp(28px, 7vw, 48px);
                font-weight: 900;
                color: #111827;
                line-height: 1.05;
                word-break: break-word;
                letter-spacing: -1px;
            }}
            .easy-meaning {{
                margin-top: 8px;
                font-size: clamp(16px, 4vw, 22px);
                font-weight: 900;
                color: #334155;
                line-height: 1.25;
                word-break: keep-all;
            }}
            .easy-progress-box {{
                background: rgba(255,255,255,0.76);
                border: 1px solid #dbeafe;
                border-radius: 20px;
                padding: 13px 14px;
                margin: 12px 0;
            }}
            .easy-bar-bg {{
                width: 100%;
                height: 10px;
                background: #e2e8f0;
                border-radius: 999px;
                overflow: hidden;
                margin: 8px 0 9px 0;
            }}
            .easy-bar-fill {{
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, #38bdf8, #8b5cf6, #ec4899);
                border-radius: 999px;
            }}
            .easy-range {{
                width: 100%;
                height: 34px;
                accent-color: #8b5cf6;
                cursor: pointer;
            }}
            .easy-control-grid {{
                display: grid;
                grid-template-columns: 1.25fr 1fr 1fr;
                gap: 9px;
                margin-top: 12px;
            }}
            .easy-sub-grid {{
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 8px;
                margin-top: 8px;
            }}
            .easy-btn {{
                width: 100%;
                min-height: 42px;
                border-radius: 18px;
                border: 1px solid #cbd5e1;
                font-size: 14px;
                font-weight: 900;
                cursor: pointer;
                box-sizing: border-box;
                white-space: nowrap;
                box-shadow: 0 3px 9px rgba(15,23,42,0.07);
            }}
            .easy-btn-main {{
                min-height: 46px;
                font-size: 16px;
                background: linear-gradient(135deg, #dbeafe, #fce7f3);
                border-color: #c4b5fd;
                color: #111827;
            }}
            .easy-select-row {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 9px;
                margin-top: 10px;
            }}
            .easy-select-box {{
                background: rgba(255,255,255,0.84);
                border: 1px solid #dbeafe;
                border-radius: 18px;
                padding: 10px 12px;
                box-sizing: border-box;
            }}
            .easy-label {{
                font-size: 12px;
                font-weight: 900;
                color: #64748b;
                margin-bottom: 5px;
            }}
            .easy-select {{
                width: 100%;
                border: 0;
                background: transparent;
                font-size: 14px;
                font-weight: 900;
                color: #0f172a;
                outline: none;
            }}
            .easy-status {{
                margin-top: 10px;
                font-size: 14px;
                font-weight: 900;
                color: #075985;
                min-height: 20px;
                line-height: 1.35;
            }}
            @media (max-width: 520px) {{
                .easy-cassette-wrap {{ padding: 10px 8px; border-radius: 16px; }}
                .easy-cassette-title {{ font-size: 16px; }}
                .easy-cassette-small {{ font-size: 12px; padding: 6px 9px; }}
                .easy-now-card {{ padding: 10px 10px; border-radius: 14px; }}
                .easy-control-grid {{ grid-template-columns: 1fr; gap: 7px; }}
                .easy-sub-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; }}
                .easy-btn {{ min-height: 36px; font-size: 11px; border-radius: 12px; padding: 5px 2px; }}
                .easy-btn-main {{ min-height: 40px; font-size: 13px; }}
                .easy-select-row {{ grid-template-columns: 1fr 1fr; gap: 7px; }}
                .easy-select {{ font-size: 12px; }}
            }}
        </style>

        <div id="{wrap_id}" class="easy-cassette-wrap">
            <div class="easy-cassette-top">
                <div class="easy-cassette-title">{safe_title}</div>
                <div id="{count_id}" class="easy-cassette-small">1 / {len(all_items)}</div>
            </div>

            <div style="font-size:14px; font-weight:800; color:#475569; line-height:1.5; margin-bottom:8px;">
                {safe_intro}
            </div>

            <div class="easy-now-card">
                <div id="{theme_id}" class="easy-theme">Theme</div>
                <div id="{word_id}" class="easy-word">Ready</div>
                <div id="{meaning_id}" class="easy-meaning">재생 버튼을 눌러 주세요.</div>
            </div>

            <div class="easy-progress-box">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:4px;">
                    <span style="font-size:13px; font-weight:900; color:#075985;">🎚️ 단어 위치</span>
                    <span id="{percent_id}" style="font-size:13px; font-weight:900; color:#7c3aed;">0%</span>
                </div>
                <div class="easy-bar-bg"><div id="{visual_bar_id}" class="easy-bar-fill"></div></div>
                <input id="{progress_id}" class="easy-range" type="range" min="0" max="{max_index}" value="0" step="1">
            </div>

            <div class="easy-control-grid">
                <button id="{play_btn_id}" class="easy-btn easy-btn-main">▶️ 듣기</button>
                <button id="{pause_btn_id}" class="easy-btn" style="background:#ecfeff; border-color:#67e8f9; color:#155e75;">⏸ 잠깐 멈춤</button>
                <button id="{replay_btn_id}" class="easy-btn" style="background:#fef3c7; border-color:#fde68a; color:#92400e;">🔁 현재 단어</button>
            </div>

            <div class="easy-sub-grid">
                <button id="{prev_btn_id}" class="easy-btn" style="background:#f8fafc; color:#334155;">⏮ 이전</button>
                <button id="{stop_btn_id}" class="easy-btn" style="background:#fff7ed; border-color:#fed7aa; color:#9a3412;">⏹ 처음</button>
                <button id="{next_btn_id}" class="easy-btn" style="background:#f8fafc; color:#334155;">다음 ⏭</button>
            </div>

            <div class="easy-select-row">
                <div class="easy-select-box">
                    <div class="easy-label">속도</div>
                    <select id="{speed_select_id}" class="easy-select">
                        <option value="0.55">천천히</option>
                        <option value="0.75" selected>보통</option>
                        <option value="0.95">조금 빠르게</option>
                        <option value="1.15">빠르게</option>
                    </select>
                </div>
                <div class="easy-select-box">
                    <div class="easy-label">전체 반복</div>
                    <select id="{repeat_select_id}" class="easy-select">
                        <option value="1">1번</option>
                        <option value="2">2번</option>
                        <option value="3" selected>3번</option>
                    </select>
                </div>
            </div>

            <div id="{status_id}" class="easy-status"></div>

            <script>
            (function() {{
                const cassetteItems = {cassette_json};
                const playBtn = document.getElementById("{play_btn_id}");
                const pauseBtn = document.getElementById("{pause_btn_id}");
                const replayBtn = document.getElementById("{replay_btn_id}");
                const prevBtn = document.getElementById("{prev_btn_id}");
                const nextBtn = document.getElementById("{next_btn_id}");
                const stopBtn = document.getElementById("{stop_btn_id}");
                const progress = document.getElementById("{progress_id}");
                const visualBar = document.getElementById("{visual_bar_id}");
                const percentBox = document.getElementById("{percent_id}");
                const status = document.getElementById("{status_id}");
                const wordBox = document.getElementById("{word_id}");
                const meaningBox = document.getElementById("{meaning_id}");
                const countBox = document.getElementById("{count_id}");
                const themeBox = document.getElementById("{theme_id}");
                const speedSelect = document.getElementById("{speed_select_id}");
                const repeatSelect = document.getElementById("{repeat_select_id}");
                const wrap = document.getElementById("{wrap_id}");
                const playerId = {safe_player_id};
                const channel = new BroadcastChannel("daily_english_audio_channel");

                let index = 0;
                let isPlaying = false;
                let isPaused = false;
                let playToken = 0;
                let repeatRound = 1;
                const wordRepeatEach = {word_repeat_each};
                let safetyTimer = null;
                let jumpTimer = null;

                function escapeHtml(text) {{
                    const div = document.createElement("div");
                    div.innerText = text || "";
                    return div.innerHTML;
                }}

                function getEmoji(word) {{
                    const emojiMap = {{
                        "I":"🙋","you":"👉","he":"👦","she":"👧","we":"👥","they":"👥","friend":"🤝","teacher":"👩‍🏫","student":"🧑‍🎓",
                        "go":"➡️","come":"⬅️","walk":"🚶","run":"🏃","sit":"🪑","stand":"🧍","stop":"🛑","start":"▶️","open":"📂","close":"📕",
                        "eat":"🍽️","drink":"🥤","sleep":"😴","study":"📚","read":"📖","write":"✏️","listen":"👂","speak":"🗣️","help":"🆘",
                        "happy":"😊","sad":"😢","angry":"😠","tired":"🥱","hungry":"😋","thirsty":"🥤","sick":"🤒","okay":"👌","fine":"🙂",
                        "food":"🍽️","water":"💧","rice":"🍚","bread":"🍞","milk":"🥛","juice":"🧃","coffee":"☕","tea":"🍵",
                        "home":"🏠","school":"🏫","bathroom":"🚻","hospital":"🏥","store":"🏪","bus":"🚌","car":"🚗","taxi":"🚕","train":"🚆","bike":"🚲",
                        "time":"⏰","now":"🕒","today":"📅","tomorrow":"➡️📅","yesterday":"⬅️📅","nine":"9️⃣","ten":"🔟",
                        "bag":"🎒","phone":"📱","book":"📘","money":"💵","card":"💳","ticket":"🎫",
                        "please":"🙏","sorry":"🙇","excuse me":"🙋","again":"🔁","slowly":"🐢","question":"❓","answer":"✅"
                    }};
                    return emojiMap[word] || "🌱";
                }}

                function getEnglishVoice() {{
                    const voices = window.speechSynthesis.getVoices();
                    const preferredNames = ["Samantha", "Google US English", "Microsoft Jenny", "Microsoft Aria", "Microsoft Zira", "Karen", "Moira", "Tessa", "Fiona", "Victoria"];
                    for (const name of preferredNames) {{
                        const found = voices.find(v => v.name && v.name.toLowerCase().includes(name.toLowerCase()) && v.lang && v.lang.toLowerCase().startsWith("en"));
                        if (found) return found;
                    }}
                    return voices.find(v => v.lang && v.lang.toLowerCase().startsWith("en")) || null;
                }}

                function updateDisplay() {{
                    const item = cassetteItems[index];
                    if (!item) return;
                    const max = Math.max(cassetteItems.length - 1, 1);
                    const pct = Math.round((index / max) * 100);
                    progress.value = index;
                    visualBar.style.width = pct + "%";
                    percentBox.innerText = pct + "%";
                    countBox.innerText = (index + 1) + " / " + cassetteItems.length;
                    themeBox.innerText = item.theme || "Theme";
                    wordBox.innerText = item.word + " " + (item.emoji || getEmoji(item.word));
                    meaningBox.innerHTML = escapeHtml(item.meaning);
                    status.innerText = "현재 위치: " + (index + 1) + "번 · 반복 " + repeatRound + "/" + repeatSelect.value;
                }}

                function clearTimers() {{
                    if (safetyTimer) {{ clearTimeout(safetyTimer); safetyTimer = null; }}
                    if (jumpTimer) {{ clearTimeout(jumpTimer); jumpTimer = null; }}
                }}

                function stopTape(resetIndex = false, showMessage = false) {{
                    playToken += 1;
                    clearTimers();
                    window.speechSynthesis.cancel();
                    isPlaying = false;
                    isPaused = false;
                    repeatRound = 1;
                    playBtn.innerText = "▶️ 듣기";
                    pauseBtn.innerText = "⏸ 잠깐 멈춤";
                    if (resetIndex) index = 0;
                    updateDisplay();
                    if (showMessage) status.innerText = "처음으로 돌아갔습니다.";
                }}

                channel.onmessage = function(event) {{
                    if (!event.data) return;

                    // 다른 카테고리/다른 카세트가 시작되거나,
                    // 탭/챕터 이동 신호가 오면 현재 듣기를 자동으로 중지합니다.
                    if (event.data.type === "STOP_ALL") {{
                        stopTape(false, false);
                    }}

                    if (event.data.type === "STOP_OTHERS" && event.data.playerId !== playerId) {{
                        stopTape(false, false);
                    }}
                }};

                function broadcastStopAll() {{
                    try {{
                        channel.postMessage({{ type: "STOP_ALL", playerId: playerId }});
                    }} catch (e) {{}}
                }}

                // Streamlit 페이지 이동, 새로고침, 브라우저 탭 이동 시 자동 중지
                window.addEventListener("pagehide", function() {{ stopTape(false, false); }});
                window.addEventListener("beforeunload", function() {{ stopTape(false, false); }});
                document.addEventListener("visibilitychange", function() {{
                    if (document.hidden) stopTape(false, false);
                }});

                // 카세트 영역이 화면에서 사라지면 자동 중지
                if ("IntersectionObserver" in window && wrap) {{
                    const observer = new IntersectionObserver(function(entries) {{
                        entries.forEach(function(entry) {{
                            if (!entry.isIntersecting && (isPlaying || isPaused || window.speechSynthesis.speaking)) {{
                                stopTape(false, false);
                            }}
                        }});
                    }}, {{ threshold: 0.05 }});
                    observer.observe(wrap);
                }}

                // Streamlit의 상단 탭이나 왼쪽 페이지 메뉴를 누르면 모든 카세트 중지
                try {{
                    const parentDoc = window.parent && window.parent.document;
                    if (parentDoc && !window.parent.__survivalCassetteAutoStopBound) {{
                        window.parent.__survivalCassetteAutoStopBound = true;
                        parentDoc.addEventListener("click", function(e) {{
                            const target = e.target;
                            if (!target) return;
                            const clickedTab = target.closest('[role="tab"]');
                            const clickedSidebarLink = target.closest('section[data-testid="stSidebar"] a');
                            const clickedPageLink = target.closest('a[href]');
                            if (clickedTab || clickedSidebarLink || clickedPageLink) {{
                                setTimeout(broadcastStopAll, 10);
                            }}
                        }}, true);
                    }}
                }} catch (e) {{}}

                function speakItem(item, onDone, token) {{
                    if (!item || token !== playToken) return;
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(item.script || item.word);
                    utterance.lang = "en-US";
                    utterance.rate = parseFloat(speedSelect.value || "0.75");
                    utterance.pitch = 1.05;
                    const voice = getEnglishVoice();
                    if (voice) utterance.voice = voice;

                    let done = false;
                    function finish() {{
                        if (done) return;
                        done = true;
                        if (token !== playToken) return;
                        onDone();
                    }}
                    utterance.onend = finish;
                    utterance.onerror = finish;
                    window.speechSynthesis.speak(utterance);

                    const estimatedMs = Math.max(1600, (item.script || item.word || "word").length * 160 / Math.max(parseFloat(speedSelect.value || "0.75"), 0.4));
                    safetyTimer = setTimeout(finish, estimatedMs);
                }}

                function speakCurrent(token = playToken, wordRepeatCount = 1) {{
                    if (!isPlaying || isPaused || token !== playToken) return;
                    const item = cassetteItems[index];
                    if (!item) return;
                    updateDisplay();

                    if (wordRepeatEach > 1) {{
                        status.innerText = "현재 위치: " + (index + 1) + "번 · 단어 " + wordRepeatCount + "/" + wordRepeatEach + "회 · 전체 반복 " + repeatRound + "/" + repeatSelect.value;
                    }}

                    speakItem(item, function() {{
                        if (!isPlaying || isPaused || token !== playToken) return;

                        if (wordRepeatCount < wordRepeatEach) {{
                            jumpTimer = setTimeout(function() {{ speakCurrent(token, wordRepeatCount + 1); }}, 650);
                            return;
                        }}

                        index += 1;
                        if (index >= cassetteItems.length) {{
                            const maxRepeat = parseInt(repeatSelect.value || "1");
                            if (repeatRound < maxRepeat) {{
                                repeatRound += 1;
                                index = 0;
                                updateDisplay();
                                jumpTimer = setTimeout(function() {{ speakCurrent(token, 1); }}, 600);
                                return;
                            }}
                            stopTape(false, false);
                            index = cassetteItems.length - 1;
                            updateDisplay();
                            status.innerText = "카세트 듣기 완료!";
                            return;
                        }}
                        updateDisplay();
                        jumpTimer = setTimeout(function() {{ speakCurrent(token, 1); }}, 500);
                    }}, token);
                }}

                function startFromCurrent() {{
                    channel.postMessage({{ type: "STOP_OTHERS", playerId: playerId }});
                    playToken += 1;
                    clearTimers();
                    window.speechSynthesis.cancel();
                    isPlaying = true;
                    isPaused = false;
                    playBtn.innerText = "재생 중...";
                    pauseBtn.innerText = "⏸ 잠깐 멈춤";
                    const token = playToken;
                    speakCurrent(token);
                }}

                function jumpTo(newIndex, keepPlaying = true) {{
                    index = Math.max(0, Math.min(cassetteItems.length - 1, newIndex));
                    repeatRound = 1;
                    playToken += 1;
                    clearTimers();
                    window.speechSynthesis.cancel();
                    updateDisplay();
                    if (isPlaying && keepPlaying) {{
                        const token = playToken;
                        jumpTimer = setTimeout(function() {{ speakCurrent(token); }}, 300);
                    }}
                }}

                playBtn.addEventListener("click", function() {{
                    if (isPaused) {{
                        window.speechSynthesis.resume();
                        isPaused = false;
                        isPlaying = true;
                        playBtn.innerText = "재생 중...";
                        pauseBtn.innerText = "⏸ 잠깐 멈춤";
                        status.innerText = "이어 듣는 중";
                        return;
                    }}
                    startFromCurrent();
                }});

                pauseBtn.addEventListener("click", function() {{
                    if (isPlaying && !isPaused && window.speechSynthesis.speaking) {{
                        window.speechSynthesis.pause();
                        isPaused = true;
                        playBtn.innerText = "▶️ 이어 듣기";
                        pauseBtn.innerText = "멈춤 중";
                        status.innerText = "잠깐 멈춤";
                    }}
                }});

                replayBtn.addEventListener("click", function() {{
                    channel.postMessage({{ type: "STOP_OTHERS", playerId: playerId }});
                    playToken += 1;
                    clearTimers();
                    window.speechSynthesis.cancel();
                    isPlaying = false;
                    isPaused = false;
                    playBtn.innerText = "▶️ 듣기";
                    pauseBtn.innerText = "⏸ 잠깐 멈춤";
                    updateDisplay();
                    const token = playToken;
                    status.innerText = "현재 단어 다시 듣기";
                    speakItem(cassetteItems[index], function() {{
                        if (token === playToken) status.innerText = "현재 단어 듣기 완료";
                    }}, token);
                }});

                prevBtn.addEventListener("click", function() {{ jumpTo(index - 1, true); }});
                nextBtn.addEventListener("click", function() {{ jumpTo(index + 1, true); }});
                stopBtn.addEventListener("click", function() {{ stopTape(true, true); }});

                progress.addEventListener("input", function() {{
                    index = parseInt(progress.value);
                    updateDisplay();
                }});
                progress.addEventListener("change", function() {{
                    jumpTo(parseInt(progress.value), true);
                }});
                speedSelect.addEventListener("change", function() {{
                    status.innerText = "속도 변경: " + speedSelect.options[speedSelect.selectedIndex].text;
                }});
                repeatSelect.addEventListener("change", function() {{
                    repeatRound = 1;
                    status.innerText = "반복 횟수 변경: " + repeatSelect.value + "번";
                    updateDisplay();
                }});

                if (typeof speechSynthesis !== "undefined") {{
                    speechSynthesis.onvoiceschanged = function() {{ getEnglishVoice(); }};
                }}

                updateDisplay();
            }})();
            </script>
        </div>
        """,
        height=height
    )


def browser_daily_cassette_player(all_items, height=620):
    browser_easy_cassette_player(
        all_items,
        title="📼 전체 단어 카세트 듣기",
        intro="전체 단어를 차례대로 듣습니다. 한 단어를 2번씩 들려준 뒤 다음 단어로 넘어갑니다.",
        height=height,
        word_repeat_each=2
    )


def browser_theme_cassette_player(theme_items, theme_name, height=580):
    browser_easy_cassette_player(
        theme_items,
        title=f"📼 {theme_name} 단어 카세트 듣기",
        intro="이 테마 단어를 차례대로 듣습니다. 한 단어를 2번씩 들려준 뒤 다음 단어로 넘어갑니다.",
        height=height,
        word_repeat_each=2
    )




def show_all_cassette_tab():
    st.markdown("## 🎧 전체 단어만 카세트 듣기")

    all_items = flatten_all_words()
    browser_daily_cassette_player(all_items, height=640)

    with st.expander("📜 전체 카세트 단어 목록 보기"):
        st.write("카세트에서 실제로 들려주는 단어와 뜻을 확인할 수 있습니다.")

        for item in all_items:
            st.markdown(
                f"""
                <div style="
                    background:white;
                    border:1px solid #dcfce7;
                    border-radius:16px;
                    padding:12px 14px;
                    margin-bottom:8px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.035);
                ">
                    <div style="font-size:18px; font-weight:900; color:#111827;">
                        {item['number']}. {item['word']} {item.get('emoji', '🌱')}
                    </div>
                    <div style="font-size:15px; font-weight:800; color:#374151; margin-top:4px;">
                        단어 뜻: {item['meaning']}
                    </div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:4px;">
                        {item['theme']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


def show_cassette_player(theme_words, theme_name):
    st.markdown("### 🎧 이 테마 단어만 카세트 듣기")

    theme_items = make_theme_cassette_items(theme_words, theme_name)

    browser_theme_cassette_player(
        theme_items,
        theme_name,
        height=620
    )

# =========================
# 전체 뜻 목록 만들기
# =========================
all_words = []
for theme_words in word_themes.values():
    all_words.extend(theme_words)

all_meanings = [item["meaning"] for item in all_words]


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

    for idx, item in enumerate(theme_words):
        correct = item["meaning"]
        distractors = [m for m in all_meanings if m != correct]
        random.seed(f"{theme_name}_{item['word']}_{idx}")

        if len(distractors) >= 3:
            wrong_options = random.sample(distractors, 3)
        else:
            wrong_options = distractors

        options = [correct] + wrong_options

        quiz_items.append({
            "word": item["word"],
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
# 오늘의 일상 대화 보여주기
# =========================
def show_dialogue(theme_name):
    dialogue = theme_dialogues.get(theme_name, [])

    if not dialogue:
        return

    st.markdown('<div class="dialogue-box">', unsafe_allow_html=True)
    st.markdown('<div class="dialogue-title">💬 오늘의 일상 대화</div>', unsafe_allow_html=True)

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

    dialogue_text = make_dialogue_tts_text(dialogue)
    dialogue_audio_bytes = make_tts_audio(dialogue_text)

    safe_file_name = re.sub(r"[^a-zA-Z0-9가-힣_]+", "_", theme_name)

    st.download_button(
        label="⬇️ 대화 듣기 파일 다운로드",
        data=dialogue_audio_bytes,
        file_name=f"{safe_file_name}_dialogue.mp3",
        mime="audio/mp3",
        key=f"{theme_name}_dialogue_download"
    )


# =========================
# 단어 익히기
# =========================
def show_word_cards(theme_words, theme_name):
    st.markdown("### 🌱 핵심 단어 익히기")
    st.write("기초 일상대화에 꼭 필요한 단어를 듣고 익혀 보세요.")

    for idx, item in enumerate(theme_words):
        st.markdown('<div class="word-card">', unsafe_allow_html=True)

        # 기존 크기감은 유지하면서: 영어 → 한국어 → 이모지 → 듣기/중지 순서
        col1, col2, col3, col4 = st.columns([1.25, 1.05, 0.35, 1.65])

        with col1:
            st.markdown(
                f"""
                <div class="word-row">
                    <div class="word-number">{idx + 1}</div>
                    <div class="word-text">{item['word']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div class='meaning-text'>{item['meaning']}</div>",
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"<div class='emoji-text'>{get_word_emoji(item['word'])}</div>",
                unsafe_allow_html=True
            )

        with col4:
            audio_button(
                "🔊 듣기",
                item["word"],
                key=f"{theme_name}_learn_audio_{idx}"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('---')
    show_cassette_player(theme_words, theme_name)


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
        st.write("영어 단어를 보고 알맞은 뜻을 고르세요.")

        for i, q in enumerate(quiz_items):
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)

            st.markdown(f"<div class='quiz-number'>🌟 Question {i + 1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='quiz-word'>{q['word']}</div>", unsafe_allow_html=True)

            audio_button(
                "🔊 듣기",
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
            st.success("🌈 완벽합니다! 이 테마의 일상 단어를 모두 잘 기억하고 있습니다.")

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
                    "🔊 듣기",
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
                    "🔊 듣기",
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
# 탭 구성
# =========================
# 전체 카세트 듣기는 제일 마지막 탭에 배치
tab_names = list(word_themes.keys()) + ["🎧 전체 카세트 듣기"]
tabs = st.tabs(tab_names)

for tab, theme_name in zip(tabs[:-1], word_themes.keys()):
    with tab:
        theme_words = word_themes[theme_name]

        st.markdown(
            f"""
            <div class="theme-header">
                <div class="theme-title">{theme_name}</div>
                <div class="theme-desc">이 테마에는 {len(theme_words)}개의 일상 단어가 있습니다. 핵심 단어를 듣고 익혀 봅시다.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        mode = st.radio(
            "학습 모드를 선택하세요.",
            ["🌱 핵심 단어 익히기", "🧸 퀴즈 풀기"],
            key=f"{theme_name}_mode",
            horizontal=True
        )

        if mode == "🌱 핵심 단어 익히기":
            show_word_cards(theme_words, theme_name)
        else:
            show_quiz(theme_words, theme_name)

with tabs[-1]:
    show_all_cassette_tab()
