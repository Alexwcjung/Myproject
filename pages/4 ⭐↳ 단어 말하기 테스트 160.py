import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="생존 단어 카드 말하기 게임",
    page_icon="🃏",
    layout="wide"
)

# =========================================================
# 생존 단어 160개
# =========================================================
WORD_THEMES = {
    "🧍 나와 사람": [
        {"word": "I", "meaning": "나", "emoji": "🙋"},
        {"word": "you", "meaning": "너, 당신", "emoji": "👉"},
        {"word": "he", "meaning": "그", "emoji": "👦"},
        {"word": "she", "meaning": "그녀", "emoji": "👧"},
        {"word": "we", "meaning": "우리", "emoji": "👥"},
        {"word": "they", "meaning": "그들", "emoji": "👥"},
        {"word": "friend", "meaning": "친구", "emoji": "🤝"},
        {"word": "teacher", "meaning": "선생님", "emoji": "👩‍🏫"},
        {"word": "student", "meaning": "학생", "emoji": "🧑‍🎓"},
        {"word": "classmate", "meaning": "반 친구", "emoji": "👫"},
        {"word": "family", "meaning": "가족", "emoji": "👨‍👩‍👧"},
        {"word": "father", "meaning": "아버지", "emoji": "👨"},
        {"word": "mother", "meaning": "어머니", "emoji": "👩"},
        {"word": "brother", "meaning": "형제, 남자 형제", "emoji": "👦"},
        {"word": "sister", "meaning": "자매, 여자 형제", "emoji": "👧"},
        {"word": "name", "meaning": "이름", "emoji": "🏷️"},
        {"word": "person", "meaning": "사람", "emoji": "🧍"},
        {"word": "man", "meaning": "남자", "emoji": "👨"},
        {"word": "woman", "meaning": "여자", "emoji": "👩"},
        {"word": "child", "meaning": "아이", "emoji": "🧒"},
    ],
    "🏃 기본 동작": [
        {"word": "go", "meaning": "가다", "emoji": "➡️"},
        {"word": "come", "meaning": "오다", "emoji": "⬅️"},
        {"word": "walk", "meaning": "걷다", "emoji": "🚶"},
        {"word": "run", "meaning": "달리다", "emoji": "🏃"},
        {"word": "sit", "meaning": "앉다", "emoji": "🪑"},
        {"word": "stand", "meaning": "서다", "emoji": "🧍"},
        {"word": "stop", "meaning": "멈추다", "emoji": "🛑"},
        {"word": "start", "meaning": "시작하다", "emoji": "▶️"},
        {"word": "open", "meaning": "열다", "emoji": "📂"},
        {"word": "close", "meaning": "닫다", "emoji": "📕"},
        {"word": "eat", "meaning": "먹다", "emoji": "🍽️"},
        {"word": "drink", "meaning": "마시다", "emoji": "🥤"},
        {"word": "sleep", "meaning": "자다", "emoji": "😴"},
        {"word": "study", "meaning": "공부하다", "emoji": "📚"},
        {"word": "read", "meaning": "읽다", "emoji": "📖"},
        {"word": "write", "meaning": "쓰다", "emoji": "✏️"},
        {"word": "listen", "meaning": "듣다", "emoji": "👂"},
        {"word": "speak", "meaning": "말하다", "emoji": "🗣️"},
        {"word": "help", "meaning": "돕다", "emoji": "🆘"},
        {"word": "wait", "meaning": "기다리다", "emoji": "⏳"},
    ],
    "💖 감정·몸 상태": [
        {"word": "happy", "meaning": "행복한", "emoji": "😊"},
        {"word": "sad", "meaning": "슬픈", "emoji": "😢"},
        {"word": "angry", "meaning": "화난", "emoji": "😠"},
        {"word": "tired", "meaning": "피곤한", "emoji": "🥱"},
        {"word": "hungry", "meaning": "배고픈", "emoji": "😋"},
        {"word": "thirsty", "meaning": "목마른", "emoji": "🥤"},
        {"word": "sick", "meaning": "아픈", "emoji": "🤒"},
        {"word": "okay", "meaning": "괜찮은", "emoji": "👌"},
        {"word": "fine", "meaning": "괜찮은", "emoji": "🙂"},
        {"word": "cold", "meaning": "추운, 차가운", "emoji": "🥶"},
        {"word": "hot", "meaning": "더운, 뜨거운", "emoji": "🥵"},
        {"word": "pain", "meaning": "통증", "emoji": "🤕"},
        {"word": "headache", "meaning": "두통", "emoji": "🤯"},
        {"word": "stomachache", "meaning": "복통", "emoji": "🤢"},
        {"word": "fever", "meaning": "열", "emoji": "🌡️"},
        {"word": "hurt", "meaning": "아프다, 다치다", "emoji": "🩹"},
        {"word": "good", "meaning": "좋은", "emoji": "👍"},
        {"word": "bad", "meaning": "나쁜", "emoji": "👎"},
        {"word": "worried", "meaning": "걱정하는", "emoji": "😟"},
        {"word": "scared", "meaning": "무서워하는", "emoji": "😨"},
    ],
    "🍎 음식·물": [
        {"word": "food", "meaning": "음식", "emoji": "🍽️"},
        {"word": "water", "meaning": "물", "emoji": "💧"},
        {"word": "rice", "meaning": "밥, 쌀", "emoji": "🍚"},
        {"word": "bread", "meaning": "빵", "emoji": "🍞"},
        {"word": "milk", "meaning": "우유", "emoji": "🥛"},
        {"word": "juice", "meaning": "주스", "emoji": "🧃"},
        {"word": "coffee", "meaning": "커피", "emoji": "☕"},
        {"word": "tea", "meaning": "차", "emoji": "🍵"},
        {"word": "apple", "meaning": "사과", "emoji": "🍎"},
        {"word": "banana", "meaning": "바나나", "emoji": "🍌"},
        {"word": "egg", "meaning": "달걀", "emoji": "🥚"},
        {"word": "meat", "meaning": "고기", "emoji": "🥩"},
        {"word": "chicken", "meaning": "닭고기, 닭", "emoji": "🍗"},
        {"word": "fish", "meaning": "생선, 물고기", "emoji": "🐟"},
        {"word": "breakfast", "meaning": "아침 식사", "emoji": "🍳"},
        {"word": "lunch", "meaning": "점심 식사", "emoji": "🍱"},
        {"word": "dinner", "meaning": "저녁 식사", "emoji": "🍽️"},
        {"word": "snack", "meaning": "간식", "emoji": "🍪"},
        {"word": "medicine", "meaning": "약", "emoji": "💊"},
        {"word": "hospital", "meaning": "병원", "emoji": "🏥"},
    ],
    "🚗 장소·이동": [
        {"word": "home", "meaning": "집", "emoji": "🏠"},
        {"word": "school", "meaning": "학교", "emoji": "🏫"},
        {"word": "classroom", "meaning": "교실", "emoji": "🧑‍🏫"},
        {"word": "bathroom", "meaning": "화장실", "emoji": "🚻"},
        {"word": "hospital", "meaning": "병원", "emoji": "🏥"},
        {"word": "store", "meaning": "가게", "emoji": "🏪"},
        {"word": "station", "meaning": "역", "emoji": "🚉"},
        {"word": "bus", "meaning": "버스", "emoji": "🚌"},
        {"word": "car", "meaning": "자동차", "emoji": "🚗"},
        {"word": "taxi", "meaning": "택시", "emoji": "🚕"},
        {"word": "train", "meaning": "기차", "emoji": "🚆"},
        {"word": "bike", "meaning": "자전거", "emoji": "🚲"},
        {"word": "road", "meaning": "도로", "emoji": "🛣️"},
        {"word": "street", "meaning": "거리", "emoji": "🏙️"},
        {"word": "here", "meaning": "여기", "emoji": "📍"},
        {"word": "there", "meaning": "거기", "emoji": "📌"},
        {"word": "near", "meaning": "가까운", "emoji": "↔️"},
        {"word": "far", "meaning": "먼", "emoji": "🌁"},
        {"word": "left", "meaning": "왼쪽", "emoji": "⬅️"},
        {"word": "right", "meaning": "오른쪽, 맞는", "emoji": "➡️"},
    ],
    "⏰ 시간·숫자": [
        {"word": "time", "meaning": "시간", "emoji": "⏰"},
        {"word": "now", "meaning": "지금", "emoji": "🕒"},
        {"word": "today", "meaning": "오늘", "emoji": "📅"},
        {"word": "tomorrow", "meaning": "내일", "emoji": "➡️📅"},
        {"word": "yesterday", "meaning": "어제", "emoji": "⬅️📅"},
        {"word": "morning", "meaning": "아침", "emoji": "🌅"},
        {"word": "afternoon", "meaning": "오후", "emoji": "☀️"},
        {"word": "evening", "meaning": "저녁", "emoji": "🌆"},
        {"word": "night", "meaning": "밤", "emoji": "🌙"},
        {"word": "early", "meaning": "이른", "emoji": "🐓"},
        {"word": "late", "meaning": "늦은", "emoji": "🌃"},
        {"word": "one", "meaning": "하나", "emoji": "1️⃣"},
        {"word": "two", "meaning": "둘", "emoji": "2️⃣"},
        {"word": "three", "meaning": "셋", "emoji": "3️⃣"},
        {"word": "four", "meaning": "넷", "emoji": "4️⃣"},
        {"word": "five", "meaning": "다섯", "emoji": "5️⃣"},
        {"word": "six", "meaning": "여섯", "emoji": "6️⃣"},
        {"word": "seven", "meaning": "일곱", "emoji": "7️⃣"},
        {"word": "eight", "meaning": "여덟", "emoji": "8️⃣"},
        {"word": "ten", "meaning": "열", "emoji": "🔟"},
    ],
    "🎒 물건·돈": [
        {"word": "bag", "meaning": "가방", "emoji": "🎒"},
        {"word": "phone", "meaning": "전화기", "emoji": "📱"},
        {"word": "book", "meaning": "책", "emoji": "📘"},
        {"word": "notebook", "meaning": "공책", "emoji": "📓"},
        {"word": "pen", "meaning": "펜", "emoji": "🖊️"},
        {"word": "pencil", "meaning": "연필", "emoji": "✏️"},
        {"word": "desk", "meaning": "책상", "emoji": "🪑"},
        {"word": "chair", "meaning": "의자", "emoji": "🪑"},
        {"word": "door", "meaning": "문", "emoji": "🚪"},
        {"word": "window", "meaning": "창문", "emoji": "🪟"},
        {"word": "key", "meaning": "열쇠", "emoji": "🔑"},
        {"word": "money", "meaning": "돈", "emoji": "💵"},
        {"word": "card", "meaning": "카드", "emoji": "💳"},
        {"word": "ticket", "meaning": "표, 티켓", "emoji": "🎫"},
        {"word": "clothes", "meaning": "옷", "emoji": "👕"},
        {"word": "shoes", "meaning": "신발", "emoji": "👟"},
        {"word": "hat", "meaning": "모자", "emoji": "🧢"},
        {"word": "watch", "meaning": "시계", "emoji": "⌚"},
        {"word": "cup", "meaning": "컵", "emoji": "☕"},
        {"word": "bottle", "meaning": "병", "emoji": "🍼"},
    ],
    "🆘 도움 요청": [
        {"word": "help", "meaning": "도움, 돕다", "emoji": "🆘"},
        {"word": "please", "meaning": "부디, 제발", "emoji": "🙏"},
        {"word": "sorry", "meaning": "미안합니다", "emoji": "🙇"},
        {"word": "excuse me", "meaning": "실례합니다", "emoji": "🙋"},
        {"word": "again", "meaning": "다시", "emoji": "🔁"},
        {"word": "slowly", "meaning": "천천히", "emoji": "🐢"},
        {"word": "understand", "meaning": "이해하다", "emoji": "💡"},
        {"word": "question", "meaning": "질문", "emoji": "❓"},
        {"word": "problem", "meaning": "문제", "emoji": "⚠️"},
        {"word": "need", "meaning": "필요하다", "emoji": "📌"},
        {"word": "want", "meaning": "원하다", "emoji": "✨"},
        {"word": "know", "meaning": "알다", "emoji": "🧠"},
        {"word": "say", "meaning": "말하다", "emoji": "💬"},
        {"word": "tell", "meaning": "말하다, 알려주다", "emoji": "📣"},
        {"word": "ask", "meaning": "묻다", "emoji": "❔"},
        {"word": "answer", "meaning": "대답, 답", "emoji": "✅"},
        {"word": "repeat", "meaning": "반복하다", "emoji": "🔁"},
        {"word": "speak", "meaning": "말하다", "emoji": "🗣️"},
        {"word": "look", "meaning": "보다", "emoji": "👀"},
        {"word": "listen", "meaning": "듣다", "emoji": "👂"},
    ],
}

# =========================================================
# 상단 디자인
# =========================================================
st.markdown(
    """
    <style>
    .main-title-box {
        background: linear-gradient(135deg, #eff6ff 0%, #fff7ed 50%, #fdf2f8 100%);
        border: 1.5px solid #dbeafe;
        border-radius: 30px;
        padding: 28px 30px;
        margin-bottom: 22px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.07);
    }

    .main-title-box h1 {
        margin: 0 0 10px 0;
        color: #0f172a;
        font-size: 38px;
        font-weight: 900;
    }

    .main-title-box p {
        margin: 0;
        color: #475569;
        font-size: 18px;
        line-height: 1.7;
        font-weight: 700;
    }

    @media (max-width: 768px) {
        .main-title-box {
            padding: 20px 18px;
            border-radius: 22px;
        }

        .main-title-box h1 {
            font-size: 27px;
        }

        .main-title-box p {
            font-size: 15px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-title-box">
        <h1>🃏 생존 단어 카드 말하기 게임</h1>
        <p>한국말 뜻을 보고 영어 단어를 말해 보세요.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 말하기 카드 게임 컴포넌트
# =========================================================
def word_card_speaking_game(word_themes):
    items = []
    for cat, words in word_themes.items():
        for item in words:
            new_item = dict(item)
            new_item["cat"] = cat
            items.append(new_item)

    items_json = json.dumps(items, ensure_ascii=False)

    html = r"""
    <div id="word-card-app" style="
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 50%, #fdf2f8 100%);
        border: 1.5px solid #dbeafe;
        border-radius: 30px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        max-width: 100%;
        overflow-x: hidden;
        box-sizing: border-box;
    ">
        <style>
            #word-card-app * {
                box-sizing: border-box;
            }

            #word-card-app button {
                -webkit-tap-highlight-color: transparent;
                touch-action: manipulation;
            }

            #word-card-app select {
                max-width: 100%;
            }

            #cardBox {
                position: relative;
                transform-style: preserve-3d;
                perspective: 1200px;
                transform-origin: left center;
            }

            #cardBox::after {
                content: "";
                position: absolute;
                inset: 0;
                border-radius: 32px;
                pointer-events: none;
                background: linear-gradient(90deg, rgba(255,255,255,0.15), rgba(15,23,42,0.10));
                opacity: 0;
            }

            .page-flip-card {
                animation: pageFlip 0.62s ease-in-out;
            }

            .page-flip-card::after {
                animation: pageShadow 0.62s ease-in-out;
            }

            @keyframes pageFlip {
                0% {
                    transform: rotateY(0deg) translateX(0);
                    opacity: 1;
                }
                35% {
                    transform: rotateY(-18deg) translateX(-6px);
                    opacity: 0.92;
                }
                70% {
                    transform: rotateY(7deg) translateX(3px);
                    opacity: 1;
                }
                100% {
                    transform: rotateY(0deg) translateX(0);
                    opacity: 1;
                }
            }

            @keyframes pageShadow {
                0% {
                    opacity: 0;
                }
                35% {
                    opacity: 1;
                }
                100% {
                    opacity: 0;
                }
            }

            @media (max-width: 768px) {
                #word-card-app {
                    padding: 14px !important;
                    border-radius: 22px !important;
                }

                #categorySelect {
                    width: 100%;
                    font-size: 14px !important;
                }

                #topControlBox {
                    gap: 8px !important;
                }

                #topControlBox button {
                    flex: 1 1 45%;
                    font-size: 14px !important;
                    padding: 10px 10px !important;
                }

                #cardBox {
                    padding: 18px 14px !important;
                    border-radius: 24px !important;
                }

                #emojiBox {
                    font-size: 72px !important;
                }

                #meaningBox {
                    font-size: 32px !important;
                    line-height: 1.25 !important;
                }

                #answerBox {
                    font-size: 27px !important;
                    padding: 14px 12px !important;
                    word-break: break-word;
                }

                #buttonBox button {
                    flex: 1 1 100%;
                    font-size: 16px !important;
                    padding: 13px 12px !important;
                }

                #transcriptBox {
                    font-size: 19px !important;
                }

                #resultBox {
                    font-size: 17px !important;
                }
            }
        </style>

        <div id="topControlBox" style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:18px;">
            <label style="font-weight:900; color:#334155;">단어 테마 선택</label>
            <select id="categorySelect" style="
                padding: 10px 14px;
                border-radius: 999px;
                border: 1.5px solid #bae6fd;
                font-size: 15px;
                font-weight: 800;
                color: #0f172a;
                background: white;
            "></select>

            <button id="randomBtn" style="
                border: 1.5px solid #c7d2fe;
                background: white;
                color: #3730a3;
                border-radius: 999px;
                padding: 10px 15px;
                font-weight: 900;
                cursor: pointer;
            ">🎲 섞어서 풀기</button>

            <button id="resetBtn" style="
                border: 1.5px solid #fed7aa;
                background: #fff7ed;
                color: #9a3412;
                border-radius: 999px;
                padding: 10px 15px;
                font-weight: 900;
                cursor: pointer;
            ">🔄 다시 시작</button>
        </div>

        <div id="gameArea">
            <div style="display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <div id="categoryLabel" style="
                    display:inline-block;
                    background:#eef6ff;
                    color:#1d4ed8;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1px solid #bfdbfe;
                "></div>

                <div id="scoreLabel" style="
                    display:inline-block;
                    background:#f0fdf4;
                    color:#166534;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1px solid #bbf7d0;
                ">정답 0 / 0 · 못 말한 단어 0</div>
            </div>

            <div id="cardBox" style="
                background:white;
                border-radius:32px;
                padding:30px 24px;
                border:1.5px solid #e0f2fe;
                box-shadow:0 8px 24px rgba(0,0,0,0.07);
                text-align:center;
                margin-bottom:18px;
            ">
                <div id="emojiBox" style="
                    font-size: 96px;
                    line-height: 1.1;
                    margin-bottom: 14px;
                ">🃏</div>

                <div style="
                    display:inline-block;
                    background:#fef3c7;
                    color:#92400e;
                    border:1.5px solid #fde68a;
                    border-radius:999px;
                    padding:7px 14px;
                    font-size:14px;
                    font-weight:900;
                    margin-bottom:14px;
                ">한국말 뜻</div>

                <div id="meaningBox" style="
                    font-size: 44px;
                    font-weight: 900;
                    color: #111827;
                    line-height: 1.35;
                    margin-bottom: 16px;
                ">뜻</div>

                <div id="answerBox" style="
                    display:none;
                    background:#ecfdf5;
                    border:1.5px solid #bbf7d0;
                    color:#166534;
                    border-radius:20px;
                    padding:16px 18px;
                    font-size:34px;
                    font-weight:900;
                    margin-top:18px;
                ">answer</div>

                <div id="hintBox" style="
                    display:none;
                    background:#fff7ed;
                    border:1.5px solid #fed7aa;
                    color:#9a3412;
                    border-radius:20px;
                    padding:14px 16px;
                    font-size:30px;
                    font-weight:900;
                    margin-top:14px;
                ">hint</div>
            </div>

            <div id="buttonBox" style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:16px;">
                <button id="micBtn" style="
                    border:1.5px solid #fecaca;
                    background:#fff1f2;
                    color:#be123c;
                    border-radius:999px;
                    padding:13px 20px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:17px;
                ">🎙️ 말하기</button>

                <button id="answerBtn" style="
                    border:1.5px solid #bfdbfe;
                    background:#eff6ff;
                    color:#1d4ed8;
                    border-radius:999px;
                    padding:13px 20px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:17px;
                ">🔊 정답 듣기/보기</button>

                <button id="hintBtn" style="
                    border:1.5px solid #fed7aa;
                    background:#fff7ed;
                    color:#9a3412;
                    border-radius:999px;
                    padding:13px 20px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:17px;
                ">💡 힌트 보기</button>

                <button id="skipBtn" style="
                    border:1.5px solid #c7d2fe;
                    background:#eef2ff;
                    color:#3730a3;
                    border-radius:999px;
                    padding:13px 20px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:17px;
                ">➡️ 다음 단어</button>
            </div>

            <div style="
                background:#f8fafc;
                border:1.5px solid #e2e8f0;
                border-radius:18px;
                padding:14px 16px;
                margin-bottom:14px;
                min-height:54px;
            ">
                <div style="font-size:13px; color:#64748b; font-weight:900; margin-bottom:5px;">인식된 단어</div>
                <div id="transcriptBox" style="font-size:22px; font-weight:900; color:#334155;"></div>
            </div>

            <div id="resultBox" style="
                background:#f1f5f9;
                border:1.5px solid #e2e8f0;
                border-radius:18px;
                padding:14px 16px;
                font-size:20px;
                font-weight:900;
                color:#334155;
            ">
                마이크 버튼을 누르고 영어 단어 한 단어를 말해 보세요.
            </div>
        </div>

        <div id="finishBox" style="
            display:none;
            background:white;
            border-radius:30px;
            padding:30px 24px;
            border:1.5px solid #bbf7d0;
            box-shadow:0 8px 24px rgba(0,0,0,0.07);
            text-align:center;
            margin-top:16px;
        ">
            <div style="font-size:64px; margin-bottom:10px;">🎉</div>
            <div style="
                font-size:34px;
                font-weight:900;
                color:#14532d;
                margin-bottom:10px;
            ">테마 완료!</div>
            <div id="finishScore" style="
                font-size:24px;
                font-weight:900;
                color:#166534;
                margin-bottom:18px;
            ">정답 0 / 0 · 못 말한 단어 0</div>
            <button id="finishRetryBtn" style="
                border:1.5px solid #a7f3d0;
                background:#ecfdf5;
                color:#047857;
                border-radius:999px;
                padding:13px 22px;
                font-weight:900;
                cursor:pointer;
                font-size:17px;
            ">🔁 다시 풀기</button>
        </div>
    </div>

    <script>
    const ITEMS = __ITEMS_JSON__;

    let currentList = [];
    let currentIndex = 0;
    let currentItem = null;
    let correctMap = {};
    let missedMap = {};
    let finished = false;

    const categorySelect = document.getElementById("categorySelect");
    const randomBtn = document.getElementById("randomBtn");
    const resetBtn = document.getElementById("resetBtn");

    const gameArea = document.getElementById("gameArea");
    const finishBox = document.getElementById("finishBox");
    const finishScore = document.getElementById("finishScore");
    const finishRetryBtn = document.getElementById("finishRetryBtn");

    const categoryLabel = document.getElementById("categoryLabel");
    const scoreLabel = document.getElementById("scoreLabel");
    const cardBox = document.getElementById("cardBox");
    const emojiBox = document.getElementById("emojiBox");
    const meaningBox = document.getElementById("meaningBox");
    const answerBox = document.getElementById("answerBox");
    const hintBox = document.getElementById("hintBox");

    const micBtn = document.getElementById("micBtn");
    const answerBtn = document.getElementById("answerBtn");
    const hintBtn = document.getElementById("hintBtn");
    const skipBtn = document.getElementById("skipBtn");

    const transcriptBox = document.getElementById("transcriptBox");
    const resultBox = document.getElementById("resultBox");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    function uniqueCategories() {
        const cats = ["전체"];
        ITEMS.forEach(item => {
            if (!cats.includes(item.cat)) cats.push(item.cat);
        });
        return cats;
    }

    function initCategories() {
        const cats = uniqueCategories();
        categorySelect.innerHTML = "";
        cats.forEach(cat => {
            const option = document.createElement("option");
            option.value = cat;
            option.innerText = cat;
            categorySelect.appendChild(option);
        });
    }

    function getFilteredItems() {
        const selected = categorySelect.value;
        if (selected === "전체") return ITEMS.slice();
        return ITEMS.filter(item => item.cat === selected);
    }

    function getItemKey(item) {
        return item.cat + "||" + item.meaning + "||" + item.word;
    }

    function shuffleArray(arr) {
        const copied = arr.slice();
        for (let i = copied.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copied[i], copied[j]] = [copied[j], copied[i]];
        }
        return copied;
    }

    function normalizeText(text) {
        return String(text || "")
            .toLowerCase()
            .replace(/[.,!?;:'"’‘“”]/g, "")
            .replace(/\s+/g, " ")
            .trim();
    }

    function isCorrectSpeech(spoken, answer) {
        const s = normalizeText(spoken);
        const a = normalizeText(answer);

        if (!s || !a) return false;

        if (s === a) return true;

        // 음성 인식이 앞뒤에 짧은 말을 붙이는 경우 허용
        // 예: "the word water" / "water please"
        const words = s.split(" ").filter(Boolean);
        if (!a.includes(" ") && words.includes(a)) return true;

        // excuse me처럼 두 단어 단어도 처리
        if (a.includes(" ")) {
            return s.includes(a);
        }

        return false;
    }

    function countCorrectInCurrentTheme() {
        const list = getFilteredItems();
        let count = 0;

        list.forEach(item => {
            if (correctMap[getItemKey(item)]) count += 1;
        });

        return count;
    }

    function countMissedInCurrentTheme() {
        const list = getFilteredItems();
        let count = 0;

        list.forEach(item => {
            if (missedMap[getItemKey(item)]) count += 1;
        });

        return count;
    }

    function updateScore() {
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentTheme();
        const missedCount = countMissedInCurrentTheme();
        scoreLabel.innerText = "정답 " + correctCount + " / " + list.length + " · 못 말한 단어 " + missedCount;
    }

    function speak(text) {
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        utterance.rate = 0.82;
        utterance.pitch = 1.05;

        const voices = window.speechSynthesis.getVoices();
        const preferred = voices.find(v =>
            v.lang && v.lang.toLowerCase().startsWith("en") &&
            /(samantha|jenny|aria|zira|google us english|karen|victoria|female)/i.test(v.name)
        );
        if (preferred) utterance.voice = preferred;

        window.speechSynthesis.speak(utterance);
    }

    function showGameArea() {
        gameArea.style.display = "block";
        finishBox.style.display = "none";
        finished = false;
    }

    function showFinishScreen() {
        finished = true;
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentTheme();
        const missedCount = countMissedInCurrentTheme();

        finishScore.innerText = "정답 " + correctCount + " / " + list.length + " · 못 말한 단어 " + missedCount;

        gameArea.style.display = "none";
        finishBox.style.display = "block";
    }

    function loadQuestion(index = 0) {
        if (currentList.length === 0) {
            currentList = getFilteredItems();
        }

        if (index >= currentList.length) {
            showFinishScreen();
            return;
        }

        if (index < 0) index = 0;

        showGameArea();

        currentIndex = index;
        currentItem = currentList[currentIndex];

        categoryLabel.innerText = currentItem.cat + " · " + (currentIndex + 1) + " / " + currentList.length;
        emojiBox.innerText = currentItem.emoji || "🃏";
        meaningBox.innerText = currentItem.meaning;

        answerBox.style.display = "none";
        answerBox.innerText = "정답: " + currentItem.word;

        hintBox.style.display = "none";
        hintBox.innerText = "";

        transcriptBox.innerText = "";
        resultBox.innerText = "";
        resultBox.style.background = "#f1f5f9";
        resultBox.style.borderColor = "#e2e8f0";
        resultBox.style.color = "#334155";

        cardBox.classList.remove("page-flip-card");
        void cardBox.offsetWidth;
        cardBox.classList.add("page-flip-card");

        updateScore();
    }

    function goNextCard() {
        if (currentIndex + 1 >= currentList.length) {
            showFinishScreen();
        } else {
            loadQuestion(currentIndex + 1);
        }
    }

    function checkSpeech(spokenText) {
        if (!currentItem) return;

        if (isCorrectSpeech(spokenText, currentItem.word)) {
            correctMap[getItemKey(currentItem)] = true;
            delete missedMap[getItemKey(currentItem)];
            updateScore();

            resultBox.innerHTML =
                "✅ 정답입니다!<br>" +
                "<span style='font-size:17px;'>잘 말했어요: " + currentItem.word + "</span>";

            resultBox.style.background = "#ecfdf5";
            resultBox.style.borderColor = "#bbf7d0";
            resultBox.style.color = "#166534";

            speak(currentItem.word);

            setTimeout(function() {
                goNextCard();
            }, 650);
        } else {
            resultBox.innerHTML =
                "🍊 다시 말해 보세요.<br>" +
                "<span style='font-size:17px;'>한국말 뜻을 보고 영어 단어 한 단어만 말하면 됩니다.</span>";

            resultBox.style.background = "#fff7ed";
            resultBox.style.borderColor = "#fed7aa";
            resultBox.style.color = "#9a3412";
        }
    }

    function startRecognition() {
        if (!SpeechRecognition) {
            resultBox.innerText = "이 브라우저에서는 음성 인식을 사용할 수 없습니다. Chrome에서 실행해 보세요.";
            resultBox.style.background = "#fef2f2";
            resultBox.style.borderColor = "#fecaca";
            resultBox.style.color = "#991b1b";
            return;
        }

        if (finished) return;

        window.speechSynthesis.cancel();

        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = false;
        recognition.continuous = false;
        recognition.maxAlternatives = 3;

        micBtn.innerText = "🎙️ 듣는 중...";
        resultBox.innerText = "말해 보세요.";
        resultBox.style.background = "#eff6ff";
        resultBox.style.borderColor = "#bfdbfe";
        resultBox.style.color = "#1d4ed8";

        recognition.onresult = function(event) {
            let bestTranscript = "";

            for (let i = 0; i < event.results[0].length; i++) {
                const transcript = event.results[0][i].transcript;
                if (i === 0) bestTranscript = transcript;

                if (isCorrectSpeech(transcript, currentItem.word)) {
                    bestTranscript = transcript;
                    break;
                }
            }

            transcriptBox.innerText = bestTranscript;
            checkSpeech(bestTranscript);
        };

        recognition.onerror = function(event) {
            resultBox.innerText = "다시 눌러 주세요.";
            resultBox.style.background = "#fef2f2";
            resultBox.style.borderColor = "#fecaca";
            resultBox.style.color = "#991b1b";
            micBtn.innerText = "🎙️ 말하기";
        };

        recognition.onend = function() {
            micBtn.innerText = "🎙️ 말하기";
        };

        recognition.start();
    }

    function resetCurrentTheme() {
        const list = getFilteredItems();

        list.forEach(item => {
            delete correctMap[getItemKey(item)];
            delete missedMap[getItemKey(item)];
        });

        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    }

    categorySelect.addEventListener("change", function() {
        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    });

    randomBtn.addEventListener("click", function() {
        currentList = shuffleArray(getFilteredItems());
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    });

    resetBtn.addEventListener("click", resetCurrentTheme);
    finishRetryBtn.addEventListener("click", resetCurrentTheme);

    micBtn.addEventListener("click", startRecognition);

    answerBtn.addEventListener("click", function() {
        if (!currentItem) return;
        answerBox.style.display = "block";
        answerBox.innerText = "정답: " + currentItem.word;
        speak(currentItem.word);
    });

    hintBtn.addEventListener("click", function() {
        if (!currentItem) return;

        const cleanWord = String(currentItem.word || "").trim();
        const noSpaceWord = cleanWord.replace(/\s+/g, "");
        const firstTwo = noSpaceWord.length <= 2 ? noSpaceWord : noSpaceWord.slice(0, 2);

        hintBox.style.display = "block";
        hintBox.innerText = "힌트: " + firstTwo + "...";
    });

    skipBtn.addEventListener("click", function() {
        if (currentItem && !correctMap[getItemKey(currentItem)]) {
            missedMap[getItemKey(currentItem)] = true;
            updateScore();
        }
        goNextCard();
    });

    initCategories();
    currentList = getFilteredItems();
    loadQuestion(0);
    updateScore();
    </script>
    """

    html = html.replace("__ITEMS_JSON__", items_json)

    components.html(html, height=800, scrolling=True)


word_card_speaking_game(WORD_THEMES)
