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
        <p>한국말 뜻을 보고 영어 단어를 말해 보세요. 발음 시험이 아니라 단어를 알고 있는지 확인하는 활동입니다.</p>
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
            #word-card-app * { box-sizing: border-box; }
            #word-card-app button {
                -webkit-tap-highlight-color: transparent;
                touch-action: manipulation;
            }
            #word-card-app select { max-width: 100%; }

            #cardBox {
                position: relative;
                overflow: hidden;
                transform-origin: center center;
                will-change: transform, opacity, filter;
            }

            #cardBox::before {
                content: "다음 단어";
                position: absolute;
                top: 18px;
                left: 50%;
                transform: translateX(-50%) translateY(-16px) scale(0.88);
                background: linear-gradient(135deg, #2563eb, #7c3aed);
                color: white;
                border: 3px solid rgba(255,255,255,0.92);
                border-radius: 999px;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: 900;
                letter-spacing: -0.2px;
                box-shadow: 0 12px 26px rgba(37,99,235,0.24);
                opacity: 0;
                z-index: 8;
                pointer-events: none;
                white-space: nowrap;
            }

            #cardBox::after {
                content: "";
                position: absolute;
                inset: 0;
                pointer-events: none;
                background: linear-gradient(90deg,
                    rgba(219,234,254,0) 0%,
                    rgba(219,234,254,0.88) 34%,
                    rgba(237,233,254,0.92) 50%,
                    rgba(254,243,199,0.88) 66%,
                    rgba(219,234,254,0) 100%);
                transform: translateX(-115%);
                opacity: 0;
                z-index: 7;
            }

            .next-card-animate {
                animation: nextCardSlide 0.58s cubic-bezier(.2,.8,.2,1);
            }
            .next-card-animate::before {
                animation: nextBadgePop 0.58s cubic-bezier(.2,.8,.2,1);
            }
            .next-card-animate::after {
                animation: nextLightSweep 0.58s ease-out;
            }

            @keyframes nextCardSlide {
                0% { opacity: 0; transform: translateX(46px) scale(0.965); filter: blur(3px) brightness(1.05); }
                55% { opacity: 1; transform: translateX(-7px) scale(1.012); filter: blur(0) brightness(1.03); }
                100% { opacity: 1; transform: translateX(0) scale(1); filter: blur(0) brightness(1); }
            }

            @keyframes nextBadgePop {
                0% { opacity: 0; transform: translateX(-50%) translateY(-18px) scale(0.86); }
                20% { opacity: 1; transform: translateX(-50%) translateY(0) scale(1.04); }
                62% { opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }
                100% { opacity: 0; transform: translateX(-50%) translateY(-8px) scale(0.96); }
            }

            @keyframes nextLightSweep {
                0% { opacity: 0; transform: translateX(-115%); }
                20% { opacity: 1; }
                100% { opacity: 0; transform: translateX(115%); }
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
                #emojiBox { font-size: 72px !important; }
                #meaningBox {
                    font-size: 32px !important;
                    line-height: 1.25 !important;
                }
                #answerBox {
                    font-size: 27px !important;
                    padding: 14px 12px !important;
                    word-break: break-word;
                }
                #micBtn {
                    min-height: 54px !important;
                    font-size: 17px !important;
                    padding: 13px 12px !important;
                    border-radius: 999px !important;
                }
                #transcriptMiniBox {
                    min-height: 62px !important;
                    padding: 10px 12px !important;
                    border-radius: 18px !important;
                }
                #transcriptMiniLabel {
                    font-size: 12px !important;
                    margin-bottom: 4px !important;
                }
                #transcriptBox {
                    font-size: 19px !important;
                    line-height: 1.25 !important;
                }
                #smallButtonRow {
                    gap: 6px !important;
                }
                #smallButtonRow button {
                    min-height: 42px !important;
                    font-size: 12px !important;
                    padding: 8px 4px !important;
                    border-radius: 15px !important;
                    letter-spacing: -0.5px;
                }
                #resultBox { font-size: 17px !important; }
            }
        </style>

        <div id="topControlBox" style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:18px;">
            <label style="font-weight:900; color:#334155;">단어 범위 선택</label>
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
            ">🎲 이 범위 섞기</button>

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
            <div style="display:flex; justify-content:flex-end; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <div id="scoreLabel" style="
                    display:inline-block;
                    background:#f0fdf4;
                    color:#166534;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1px solid #bbf7d0;
                ">정답 0 / 0 · 연습 필요 단어 0</div>
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
                <div id="emojiBox" style="font-size: 96px; line-height: 1.1; margin-bottom: 14px;">🃏</div>

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

            <div id="buttonBox" style="
                display:flex;
                flex-direction:column;
                gap:10px;
                align-items:stretch;
                margin-bottom:16px;
                width:100%;
            ">
                <button id="micBtn" style="
                    width:100%;
                    border:1.5px solid #fecaca;
                    background:#fff1f2;
                    color:#be123c;
                    border-radius:999px;
                    padding:14px 18px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:19px;
                    min-height:58px;
                    white-space:nowrap;
                    box-shadow:0 3px 9px rgba(0,0,0,0.05);
                ">🎙️ 말하기</button>

                <div id="transcriptMiniBox" style="
                    width:100%;
                    background:#f8fafc;
                    border:1.5px solid #e2e8f0;
                    border-radius:20px;
                    padding:12px 14px;
                    min-height:68px;
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    overflow:hidden;
                ">
                    <div id="transcriptMiniLabel" style="font-size:13px; color:#64748b; font-weight:900; margin-bottom:5px; white-space:nowrap;">인식된 단어</div>
                    <div id="transcriptBox" style="font-size:22px; font-weight:900; color:#334155; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;"></div>
                </div>

                <div id="smallButtonRow" style="
                    display:grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap:8px;
                    width:100%;
                ">
                    <button id="hintBtn" style="
                        border:1.5px solid #fed7aa;
                        background:#fff7ed;
                        color:#9a3412;
                        border-radius:999px;
                        padding:10px 8px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:14px;
                        min-height:46px;
                        white-space:nowrap;
                    ">💡 힌트</button>

                    <button id="answerBtn" style="
                        border:1.5px solid #bfdbfe;
                        background:#eff6ff;
                        color:#1d4ed8;
                        border-radius:999px;
                        padding:10px 8px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:14px;
                        min-height:46px;
                        white-space:nowrap;
                    ">👀 정답+🔊</button>

                    <button id="skipBtn" style="
                        border:1.5px solid #c7d2fe;
                        background:#eef2ff;
                        color:#3730a3;
                        border-radius:999px;
                        padding:10px 8px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:14px;
                        min-height:46px;
                        white-space:nowrap;
                    ">➡️ 다음</button>
                </div>
            </div>

            <div id="resultBox" style="
                background:#f1f5f9;
                border:1.5px solid #e2e8f0;
                border-radius:18px;
                padding:14px 16px;
                font-size:20px;
                font-weight:900;
                color:#334155;
            "></div>
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
            ">범위 완료!</div>
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
    let isListening = false;
    let micSafetyTimer = null;
    let recognitionRunId = 0;

    function resetMicButton() {
        isListening = false;
        if (micSafetyTimer) {
            clearTimeout(micSafetyTimer);
            micSafetyTimer = null;
        }
        micBtn.disabled = false;
        micBtn.style.opacity = "1";
        micBtn.style.cursor = "pointer";
        micBtn.innerText = "🎙️ 말하기";
    }

    function cleanupRecognition() {
        recognitionRunId += 1;
        if (micSafetyTimer) {
            clearTimeout(micSafetyTimer);
            micSafetyTimer = null;
        }
        if (recognition) {
            try { recognition.onresult = null; } catch (e) {}
            try { recognition.onerror = null; } catch (e) {}
            try { recognition.onend = null; } catch (e) {}
            try { recognition.abort(); } catch (e) {}
            try { recognition.stop(); } catch (e) {}
            recognition = null;
        }
        resetMicButton();
    }

    function escapeHtml(text) {
        return String(text || "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function uniqueCategories() {
        return ["1~50", "51~100", "101~160"];
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
        const selected = categorySelect.value || "1~50";
        if (selected === "1~50") return ITEMS.slice(0, 50);
        if (selected === "51~100") return ITEMS.slice(50, 100);
        if (selected === "101~160") return ITEMS.slice(100, 160);
        return ITEMS.slice(0, 50);
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

    function hasKorean(text) {
        return /[ㄱ-ㅎㅏ-ㅣ가-힣]/.test(String(text || ""));
    }

    function hasEnglishLetters(text) {
        return /[a-zA-Z]/.test(String(text || ""));
    }

    function isKoreanOnlyWithoutEnglishClue(text) {
        const raw = String(text || "").trim();
        if (!raw) return false;
        return hasKorean(raw) && !hasEnglishLetters(raw);
    }

    function normalizeText(text) {
        return String(text || "")
            .toLowerCase()
            .replace(/\bi'm\b/g, "i am")
            .replace(/\bim\b/g, "i am")
            .replace(/\byou're\b/g, "you are")
            .replace(/\bhe's\b/g, "he is")
            .replace(/\bshe's\b/g, "she is")
            .replace(/\bit's\b/g, "it is")
            .replace(/\bwe're\b/g, "we are")
            .replace(/\bthey're\b/g, "they are")
            .replace(/\bdon't\b/g, "do not")
            .replace(/\bdoesn't\b/g, "do not")
            .replace(/\bdidn't\b/g, "do not")
            .replace(/\bcan't\b/g, "cannot")
            .replace(/\bcant\b/g, "cannot")
            .replace(/\bi'll\b/g, "i will")
            .replace(/\byou'll\b/g, "you will")
            .replace(/\bhe'll\b/g, "he will")
            .replace(/\bshe'll\b/g, "she will")
            .replace(/\bok\b/g, "okay")
            .replace(/\bo k\b/g, "okay")
            .replace(/\bt shirt\b/g, "tshirt")
            .replace(/\btee shirt\b/g, "tshirt")
            .replace(/\bwi fi\b/g, "wifi")
            .replace(/\bwi-fi\b/g, "wifi")
            .replace(/[.,!?;:'"’‘“”]/g, "")
            .replace(/-/g, " ")
            .replace(/\s+/g, " ")
            .trim();
    }

    const KNOWN_ANSWER_WORDS = ITEMS.map(item =>
        normalizeText(item.word).replace(/\s+/g, "")
    );

    function wordsOnly(text) {
        return normalizeText(text)
            .split(" ")
            .filter(function(w) {
                return w.length > 0;
            });
    }

    function editDistance(a, b) {
        a = String(a || "");
        b = String(b || "");
        const dp = [];
        for (let i = 0; i <= a.length; i++) {
            dp[i] = [];
            for (let j = 0; j <= b.length; j++) dp[i][j] = 0;
        }
        for (let i = 0; i <= a.length; i++) dp[i][0] = i;
        for (let j = 0; j <= b.length; j++) dp[0][j] = j;

        for (let i = 1; i <= a.length; i++) {
            for (let j = 1; j <= b.length; j++) {
                const cost = a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1;
                dp[i][j] = Math.min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost
                );
            }
        }
        return dp[a.length][b.length];
    }

    function wordSimilarity(a, b) {
        a = String(a || "");
        b = String(b || "");
        if (!a || !b) return 0;
        if (a === b) return 1;
        const dist = editDistance(a, b);
        const maxLen = Math.max(a.length, b.length);
        return 1 - (dist / maxLen);
    }

    function soundKey(text) {
        return normalizeText(text)
            .replace(/[^a-z]/g, "")
            .replace(/tion/g, "shun")
            .replace(/sion/g, "shun")
            .replace(/ch/g, "j")
            .replace(/sh/g, "s")
            .replace(/th/g, "d")
            .replace(/ph/g, "f")
            .replace(/gh/g, "g")
            .replace(/ck/g, "k")
            .replace(/qu/g, "kw")
            .replace(/x/g, "ks")
            .replace(/c/g, "k")
            .replace(/q/g, "k")
            .replace(/z/g, "s")
            .replace(/v/g, "b")
            .replace(/f/g, "p")
            .replace(/r/g, "l")
            .replace(/j/g, "g")
            .replace(/w/g, "u")
            .replace(/ee/g, "i")
            .replace(/ea/g, "i")
            .replace(/ie/g, "i")
            .replace(/ei/g, "i")
            .replace(/oo/g, "u")
            .replace(/ou/g, "u")
            .replace(/ow/g, "o")
            .replace(/oa/g, "o")
            .replace(/ai/g, "e")
            .replace(/ay/g, "e")
            .replace(/[aeiouy]/g, "")
            .replace(/(.)\1+/g, "$1");
    }

    function vowelLooseKey(text) {
        return normalizeText(text)
            .replace(/[^a-z]/g, "")
            .replace(/ee/g, "i")
            .replace(/ea/g, "i")
            .replace(/ie/g, "i")
            .replace(/ei/g, "i")
            .replace(/oo/g, "u")
            .replace(/ou/g, "u")
            .replace(/ow/g, "o")
            .replace(/oa/g, "o")
            .replace(/ai/g, "e")
            .replace(/ay/g, "e")
            .replace(/[aeiouy]+/g, "v")
            .replace(/(.)\1+/g, "$1");
    }

    function aliasMatch(spokenWord, answerWord) {
        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        const aliases = {
            "i": ["i", "eye", "hi", "ai", "a"],
            "you": ["you", "u", "yew", "yo", "ya", "your", "yu"],
            "he": ["he", "hi", "hey", "hee"],
            "she": ["she", "see", "sea", "shi", "seat", "sheet"],
            "we": ["we", "wee", "wi", "me", "be"],
            "they": ["they", "day", "dey", "the", "there", "their", "that"],
            "one": ["one", "won", "wan"],
            "two": ["two", "to", "too", "tu"],
            "three": ["three", "tree", "free", "sree"],
            "four": ["four", "for", "fore"],
            "five": ["five", "fife", "pipe"],
            "six": ["six", "sex", "sick", "sicks"],
            "seven": ["seven", "seben", "sevn"],
            "eight": ["eight", "ate", "eit"],
            "ten": ["ten", "tin"],
            "here": ["here", "hear", "hir"],
            "there": ["there", "their", "der", "dare"],
            "right": ["right", "write", "light", "rite"],
            "wait": ["wait", "weight", "wet"],
            "know": ["know", "no", "now"],
            "night": ["night", "knight", "nite"],
            "okay": ["okay", "ok", "kay", "okey"],
            "phone": ["phone", "fone", "pon"],
            "coffee": ["coffee", "coffe", "copy"],
            "please": ["please", "plz", "plis", "place"],
            "go": ["go", "goal", "고"],
            "come": ["come", "com", "gum"],
            "run": ["run", "ran", "learn"],
            "sit": ["sit", "seat", "set"],
            "stand": ["stand", "stan", "stend"],
            "stop": ["stop", "stap", "stub"],
            "start": ["start", "stard", "stut"],
            "open": ["open", "opin", "oben"],
            "close": ["close", "clothes", "cloze", "closed"],
            "eat": ["eat", "it", "e"],
            "drink": ["drink", "dring", "drank"],
            "sleep": ["sleep", "slip", "sleap"],
            "read": ["read", "reed", "rid"],
            "write": ["write", "right", "light"],
            "help": ["help", "hell", "halp"],
            "friend": ["friend", "freind", "frend"],
            "teacher": ["teacher", "techer", "ticher"],
            "student": ["student", "studen", "studant"],
            "classmate": ["classmate", "classmate", "classmate", "classmate", "classmate", "classmate", "classmate", "classmate", "classmate", "class mate"],
            "family": ["family", "famly", "femily"],
            "father": ["father", "fader", "pader"],
            "mother": ["mother", "mader", "moder"],
            "brother": ["brother", "brader", "broder"],
            "sister": ["sister", "seester", "sistar"],
            "person": ["person", "parson"],
            "woman": ["woman", "women", "wuman"],
            "walk": ["walk", "work", "wok"],
            "study": ["study", "stady", "steady"],
            "listen": ["listen", "lisen", "lesson"],
            "speak": ["speak", "speek", "spik"],
            "happy": ["happy", "happi"],
            "sad": ["sad", "set"],
            "angry": ["angry", "angri", "hungry"],
            "tired": ["tired", "tyred", "tire"],
            "hungry": ["hungry", "hangry", "angry"],
            "thirsty": ["thirsty", "thirsti", "firsty"],
            "stomachache": ["stomachache", "stomach ache", "stomachegg"],
            "headache": ["headache", "head ache", "hedache"],
            "breakfast": ["breakfast", "brekfast", "break first"],
            "medicine": ["medicine", "medisin", "medicen"],
            "hospital": ["hospital", "hospitel", "hostpital"],
            "bathroom": ["bathroom", "bath room", "batroom"],
            "station": ["station", "stashion", "staytion"],
            "bottle": ["bottle", "bottel", "battle"],
            "question": ["question", "kwestion", "queshon"],
            "understand": ["understand", "understend", "understanded"],
            "answer": ["answer", "anser", "andser"],
            "again": ["again", "agen", "agein"],
            "slowly": ["slowly", "slowli", "slowy"],
            "water": ["water", "wader", "워터"],
            "school": ["school", "skool", "스쿨"],
            "home": ["home", "holm"],
            "food": ["food", "fud", "put"],
            "rice": ["rice", "rise", "lice"],
            "bread": ["bread", "bred"],
            "milk": ["milk", "melk"],
            "juice": ["juice", "juse"],
            "apple": ["apple", "appel"],
            "banana": ["banana", "bananna"],
            "chicken": ["chicken", "chiken"],
            "classroom": ["classroom", "class room"],
            "store": ["store", "stole"],
            "train": ["train", "trane"],
            "bike": ["bike", "back", "baik"],
            "road": ["road", "load"],
            "street": ["street", "strit"],
            "left": ["left", "lift"],
            "morning": ["morning", "mornin"],
            "afternoon": ["afternoon", "after noon"],
            "evening": ["evening", "evning"],
            "money": ["money", "moni"],
            "ticket": ["ticket", "tiket"],
            "clothes": ["clothes", "close", "cloths"],
            "shoes": ["shoes", "shoe"],
            "repeat": ["repeat", "repeet"],
            "look": ["look", "luk"],
            "ask": ["ask", "axe"],
            "tell": ["tell", "tel"],
            "say": ["say", "sei"],
            "want": ["want", "wanna", "won"],
            "need": ["need", "nid"],
            "problem": ["problem", "problum"],
            "sorry": ["sorry", "sori"],
            "child": ["child", "chaild"],
            "man": ["man", "men"],
            "hot": ["hot", "hut"],
            "cold": ["cold", "called"],
            "good": ["good", "gud"],
            "bad": ["bad", "bed"]
        };

        if (!aliases[aw]) return false;
        return aliases[aw].includes(sw);
    }

    function clearlyWrongPronoun(spokenWord, answerWord) {
        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");
        const pronouns = ["i", "you", "he", "she", "we", "they"];
        if (!pronouns.includes(aw)) return false;
        if (!pronouns.includes(sw)) return false;
        return sw !== aw;
    }

    function prefixOverlap(a, b) {
        a = String(a || "");
        b = String(b || "");
        let n = Math.min(a.length, b.length);
        let count = 0;
        for (let i = 0; i < n; i++) {
            if (a.charAt(i) === b.charAt(i)) count += 1;
            else break;
        }
        return count;
    }

    function hasSharedBigram(a, b) {
        a = String(a || "");
        b = String(b || "");
        if (a.length < 2 || b.length < 2) return false;
        for (let i = 0; i < a.length - 1; i++) {
            if (b.includes(a.slice(i, i + 2))) return true;
        }
        return false;
    }

    function isClearlyDifferentKnownWord(sw, aw) {
        if (!KNOWN_ANSWER_WORDS.includes(sw)) return false;
        if (sw === aw) return false;
        if (aliasMatch(sw, aw)) return false;

        const sim = wordSimilarity(sw, aw);
        const soundSim = wordSimilarity(soundKey(sw), soundKey(aw));
        const sameFirst = sw.charAt(0) === aw.charAt(0);
        const sameLast = sw.charAt(sw.length - 1) === aw.charAt(aw.length - 1);

        // 생존 단어 목록 안의 다른 단어라도, bike/back처럼 ASR 오인식 가능성이 있으면 막지 않습니다.
        // 다만 water → student처럼 완전히 다른 생존 단어는 오답 처리합니다.
        return !(sameFirst || sameLast || sim >= 0.45 || soundSim >= 0.36 || hasSharedBigram(sw, aw));
    }

    function isUnderstandableWord(spokenWord, answerWord) {
        if (!spokenWord || !answerWord) return false;

        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        if (!sw || !aw) return false;
        if (sw === aw) return true;
        if (aliasMatch(sw, aw)) return true;

        // 한국어만 인식된 경우는 기본적으로 오답 처리합니다.
        // 다만 브라우저가 영어 발음을 한글 소리로 잡는 일부 경우(예: go→고, water→워터, school→스쿨)는
        // 위의 aliasMatch에서 먼저 통과되므로 너무 인색하게 막지 않습니다.
        if (isKoreanOnlyWithoutEnglishClue(spokenWord)) return false;

        // I / you / he / she / we / they는 의미가 크게 바뀌므로 대명사끼리 다르면 오답
        if (clearlyWrongPronoun(sw, aw)) return false;

        // 아예 다른 생존 단어를 말한 경우는 오답
        if (isClearlyDifferentKnownWord(sw, aw)) return false;

        const dist = editDistance(sw, aw);
        const sim = wordSimilarity(sw, aw);

        const soundSw = soundKey(sw);
        const soundAw = soundKey(aw);
        const soundDist = editDistance(soundSw, soundAw);
        const soundSim = wordSimilarity(soundSw, soundAw);

        const vowelSw = vowelLooseKey(sw);
        const vowelAw = vowelLooseKey(aw);
        const vowelSim = wordSimilarity(vowelSw, vowelAw);

        const sameFirst = sw.charAt(0) === aw.charAt(0);
        const sameLast = sw.charAt(sw.length - 1) === aw.charAt(aw.length - 1);
        const sameFirstTwo = sw.slice(0, 2) === aw.slice(0, 2);
        const sameFirstThree = sw.slice(0, 3) === aw.slice(0, 3);
        const sameLastTwo = sw.slice(-2) === aw.slice(-2);

        const soundSameFirst = soundSw && soundAw && soundSw.charAt(0) === soundAw.charAt(0);
        const soundSameLast = soundSw && soundAw && soundSw.charAt(soundSw.length - 1) === soundAw.charAt(soundAw.length - 1);
        const overlap = prefixOverlap(sw, aw);

        const hasAnyClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            soundSameFirst ||
            soundSameLast ||
            overlap >= 1 ||
            hasSharedBigram(sw, aw) ||
            soundSim >= 0.25 ||
            vowelSim >= 0.30 ||
            sim >= 0.30;

        if (!hasAnyClue) return false;

        // 한 단어 인식에서 브라우저가 앞뒤에 붙이거나 일부만 잡은 경우 허용
        if (aw.length >= 4 && sw.length >= 2 && (aw.includes(sw) || sw.includes(aw))) return true;

        // 자음 뼈대가 같거나 거의 같으면 단어를 안 것으로 처리
        if (soundSw && soundAw && soundSw === soundAw) return true;
        if (soundSw && soundAw && soundDist <= 2 && soundSim >= 0.25) return true;

        // 1~2글자 단어: alias 중심이지만 너무 딱딱하지 않게 처리
        if (aw.length <= 2) {
            return sim >= 0.55 || soundSim >= 0.35 || sameFirst || sameLast;
        }

        // 3~4글자 단어: 가장 관대하게 처리
        // 목적은 발음 평가가 아니라 단어 인지 확인
        if (aw.length <= 4) {
            return (
                dist <= 2 ||
                sim >= 0.32 ||
                soundSim >= 0.24 ||
                vowelSim >= 0.28 ||
                sameFirst ||
                sameLast ||
                soundSameFirst ||
                soundSameLast ||
                hasSharedBigram(sw, aw)
            );
        }

        // 5~6글자 단어
        if (aw.length <= 6) {
            return (
                dist <= 4 ||
                sim >= 0.34 ||
                soundSim >= 0.25 ||
                vowelSim >= 0.30 ||
                sameFirst ||
                sameFirstTwo ||
                sameLast ||
                sameLastTwo ||
                hasSharedBigram(sw, aw)
            );
        }

        // 7글자 이상 긴 단어
        return (
            dist <= 6 ||
            sim >= 0.30 ||
            soundSim >= 0.22 ||
            vowelSim >= 0.25 ||
            sameFirst ||
            sameFirstTwo ||
            sameFirstThree ||
            sameLast ||
            sameLastTwo ||
            hasSharedBigram(sw, aw)
        );
    }

    function isCorrectSpeech(spoken, answer) {
        const s = normalizeText(spoken);
        const a = normalizeText(answer);

        if (!s || !a) return false;
        if (s === a) return true;

        const spokenWords = wordsOnly(s);
        const answerWords = wordsOnly(a);

        if (spokenWords.length === 0 || answerWords.length === 0) return false;

        if (answerWords.length === 1) {
            const target = answerWords[0];

            // 전체 인식 문장이 비슷하면 정답
            if (isUnderstandableWord(s, target)) return true;

            // 인식 후보 단어 중 하나라도 정답과 비슷하면 정답
            for (const sw of spokenWords) {
                if (isUnderstandableWord(sw, target)) return true;
            }

            // "bath room", "class room"처럼 분리되거나 붙는 경우 대비
            const joinedSpoken = spokenWords.join("");
            if (isUnderstandableWord(joinedSpoken, target)) return true;

            // 앞뒤에 please, uh, a, the 같은 말이 붙어도 핵심 단어만 맞으면 통과
            const fillerRemoved = spokenWords.filter(w =>
                !["a", "an", "the", "uh", "um", "please", "yes", "no"].includes(w)
            );
            if (fillerRemoved.length > 0) {
                const joinedClean = fillerRemoved.join("");
                if (isUnderstandableWord(joinedClean, target)) return true;
                for (const w of fillerRemoved) {
                    if (isUnderstandableWord(w, target)) return true;
                }
            }

            return false;
        }

        if (s.includes(a)) return true;

        // 두 단어 이상 표현: 순서대로 핵심 단어가 비슷하게 잡히면 정답
        let pos = 0;
        for (const sw of spokenWords) {
            const target = answerWords[pos];
            if (!target) break;

            if (isUnderstandableWord(sw, target)) {
                pos += 1;
            }
            if (pos >= answerWords.length) break;
        }

        // excuse me처럼 짧은 두 단어 표현은 붙어서 인식되는 경우도 허용
        if (pos < answerWords.length) {
            const joinedSpoken = spokenWords.join("");
            const joinedAnswer = answerWords.join("");
            if (isUnderstandableWord(joinedSpoken, joinedAnswer)) return true;
        }

        return pos >= answerWords.length;
    }

    function transcriptScore(transcript, answer) {
        const spokenWords = wordsOnly(transcript);
        const answerWords = wordsOnly(answer);
        if (spokenWords.length === 0 || answerWords.length === 0) return 0;

        let best = 0;

        for (const sw of spokenWords) {
            for (const aw of answerWords) {
                const swNorm = normalizeText(sw).replace(/\s+/g, "");
                const awNorm = normalizeText(aw).replace(/\s+/g, "");
                const soundSw = soundKey(swNorm);
                const soundAw = soundKey(awNorm);
                const vowelSw = vowelLooseKey(swNorm);
                const vowelAw = vowelLooseKey(awNorm);

                if (isUnderstandableWord(sw, aw)) {
                    best = Math.max(best, 1);
                } else {
                    best = Math.max(
                        best,
                        wordSimilarity(swNorm, awNorm),
                        wordSimilarity(soundSw, soundAw) * 0.95,
                        wordSimilarity(vowelSw, vowelAw) * 0.88
                    );
                }
            }
        }

        const s = normalizeText(transcript);
        const a = normalizeText(answer);
        if (s.includes(a) || a.includes(s)) best += 0.2;

        return best;
    }

    function pickBestTranscriptFromEvent(event, answer) {
        let bestTranscript = "";
        let bestScore = -1;
        let anyFinal = false;

        for (let i = 0; i < event.results.length; i++) {
            if (event.results[i].isFinal) anyFinal = true;

            for (let j = 0; j < event.results[i].length; j++) {
                const candidate = event.results[i][j].transcript.trim();
                if (!candidate) continue;

                if (!bestTranscript) bestTranscript = candidate;

                // 정답 판정이 되는 후보가 있으면 final을 기다리지 않고 바로 선택
                if (isCorrectSpeech(candidate, answer)) {
                    return {
                        transcript: candidate,
                        hasFinal: anyFinal,
                        isCorrectCandidate: true
                    };
                }

                const score = transcriptScore(candidate, answer);
                if (score > bestScore) {
                    bestScore = score;
                    bestTranscript = candidate;
                }
            }
        }

        return {
            transcript: bestTranscript,
            hasFinal: anyFinal,
            isCorrectCandidate: false
        };
    }

    function countCorrectInCurrentRange() {
        const list = getFilteredItems();
        let count = 0;
        list.forEach(item => {
            if (correctMap[getItemKey(item)]) count += 1;
        });
        return count;
    }

    function countMissedInCurrentRange() {
        const list = getFilteredItems();
        let count = 0;
        list.forEach(item => {
            if (missedMap[getItemKey(item)]) count += 1;
        });
        return count;
    }

    function updateScore() {
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentRange();
        const missedCount = countMissedInCurrentRange();
        scoreLabel.innerText = "정답 " + correctCount + " / " + list.length + " · 연습 필요 단어 " + missedCount;
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
        cleanupRecognition();
        finished = true;
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentRange();
        const missedCount = countMissedInCurrentRange();

        finishScore.innerText = "정답 " + correctCount + " / " + list.length + " · 연습 필요 단어 " + missedCount;

        gameArea.style.display = "none";
        finishBox.style.display = "block";
    }

    function loadQuestion(index = 0) {
        if (currentList.length === 0) currentList = getFilteredItems();

        if (index >= currentList.length) {
            showFinishScreen();
            return;
        }

        if (index < 0) index = 0;

        showGameArea();
        cleanupRecognition();

        currentIndex = index;
        currentItem = currentList[currentIndex];

        emojiBox.innerText = currentItem.emoji || "🃏";
        meaningBox.innerText = currentItem.meaning;

        answerBox.style.display = "none";
        answerBox.style.background = "#ecfdf5";
        answerBox.style.borderColor = "#bbf7d0";
        answerBox.style.color = "#166534";
        answerBox.innerText = "정답: " + currentItem.word;

        hintBox.style.display = "none";
        hintBox.innerText = "";

        transcriptBox.innerText = "";
        resultBox.innerText = "";
        resultBox.style.display = "none";
        resultBox.style.background = "#fff7ed";
        resultBox.style.borderColor = "#fed7aa";
        resultBox.style.color = "#92400e";

        cardBox.classList.remove("next-card-animate");
        void cardBox.offsetWidth;
        cardBox.classList.add("next-card-animate");

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

            answerBox.style.display = "none";
            transcriptBox.innerHTML =
                "<span style='color:#334155;'>" + escapeHtml(currentItem.word) + "</span>" +
                " <span style='display:inline-block; margin-left:8px; padding:4px 9px; border-radius:999px; background:#dcfce7; color:#166534; border:1px solid #bbf7d0; font-size:0.82em; font-weight:900; vertical-align:middle;'>✅ 정답입니다</span>";
            transcriptBox.style.color = "#334155";

            resultBox.innerText = "";
            resultBox.style.display = "none";

            speak(currentItem.word);
            cleanupRecognition();
        } else {
            answerBox.style.display = "none";
            transcriptBox.style.color = "#334155";
            resultBox.style.display = "block";
            resultBox.innerText = "완전히 다른 단어가 아니면 비슷한 발음도 정답으로 인정됩니다. 다시 한 번 말해 보세요.";
            resultBox.style.background = "#fff7ed";
            resultBox.style.borderColor = "#fed7aa";
            resultBox.style.color = "#92400e";
        }
    }

    async function startRecognition() {
        if (!SpeechRecognition) {
            resultBox.innerText = "이 브라우저에서는 음성 인식을 사용할 수 없습니다. Chrome에서 실행해 보세요.";
            resultBox.style.display = "block";
            resultBox.style.background = "#fef2f2";
            resultBox.style.borderColor = "#fecaca";
            resultBox.style.color = "#991b1b";
            resetMicButton();
            return;
        }

        if (finished || !currentItem) {
            resetMicButton();
            return;
        }

        if (correctMap[getItemKey(currentItem)]) {
            resultBox.innerText = "";
            resultBox.style.display = "none";
            resetMicButton();
            return;
        }

        cleanupRecognition();

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                stream.getTracks().forEach(function(track) { track.stop(); });
            } catch (err) {
                resultBox.innerText = "마이크 권한을 허용한 뒤 다시 눌러 주세요.";
                resultBox.style.display = "block";
                resultBox.style.background = "#fef2f2";
                resultBox.style.borderColor = "#fecaca";
                resultBox.style.color = "#991b1b";
                resetMicButton();
                return;
            }
        }

        window.speechSynthesis.cancel();

        recognitionRunId += 1;
        const thisRunId = recognitionRunId;

        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = true;
        recognition.continuous = false;
        recognition.maxAlternatives = 30;

        isListening = true;
        micBtn.disabled = true;
        micBtn.style.opacity = "0.72";
        micBtn.style.cursor = "wait";
        micBtn.innerText = "🎙️ 듣는 중...";

        resultBox.innerText = "";
        resultBox.style.display = "none";
        resultBox.style.background = "#fff7ed";
        resultBox.style.borderColor = "#fed7aa";
        resultBox.style.color = "#92400e";

        recognition.onresult = function(event) {
            if (thisRunId !== recognitionRunId) return;

            if (!event.results || !event.results[0]) {
                resetMicButton();
                return;
            }

            const picked = pickBestTranscriptFromEvent(event, currentItem.word);
            const bestTranscript = picked.transcript || "";

            transcriptBox.style.color = "#334155";
            transcriptBox.innerText = bestTranscript;

            // 정답 후보가 나오면 final을 기다리지 않고 바로 채점
            // final이 오면 그때도 채점
            if (picked.isCorrectCandidate || picked.hasFinal) {
                checkSpeech(bestTranscript);
            }
        };

        recognition.onerror = function(event) {
            if (thisRunId !== recognitionRunId) return;

            if (event.error === "not-allowed" || event.error === "service-not-allowed") {
                resultBox.innerText = "마이크 권한을 허용해 주세요.";
                resultBox.style.display = "block";
                resultBox.style.background = "#fef2f2";
                resultBox.style.borderColor = "#fecaca";
                resultBox.style.color = "#991b1b";
            } else if (event.error === "no-speech") {
                resultBox.innerText = "소리가 인식되지 않았습니다. 다시 눌러 주세요.";
                resultBox.style.display = "block";
                resultBox.style.background = "#f8fafc";
                resultBox.style.borderColor = "#e2e8f0";
                resultBox.style.color = "#334155";
            } else {
                resultBox.innerText = "다시 눌러 주세요.";
                resultBox.style.display = "block";
                resultBox.style.background = "#f8fafc";
                resultBox.style.borderColor = "#e2e8f0";
                resultBox.style.color = "#334155";
            }

            resetMicButton();
        };

        recognition.onend = function() {
            if (thisRunId !== recognitionRunId) return;
            recognition = null;
            resetMicButton();
        };

        micSafetyTimer = setTimeout(function() {
            if (thisRunId !== recognitionRunId) return;
            if (isListening) {
                try { recognition.stop(); } catch (e) {}
                try { recognition.abort(); } catch (e) {}
                recognition = null;
                resetMicButton();
            }
        }, 11000);

        try {
            recognition.start();
        } catch (err) {
            resultBox.innerText = "다시 눌러 주세요.";
            resultBox.style.display = "block";
            resultBox.style.background = "#f8fafc";
            resultBox.style.borderColor = "#e2e8f0";
            resultBox.style.color = "#334155";
            cleanupRecognition();
        }
    }

    function resetCurrentRange() {
        cleanupRecognition();
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
        cleanupRecognition();
        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    });

    randomBtn.addEventListener("click", function() {
        cleanupRecognition();
        currentList = shuffleArray(getFilteredItems());
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    });

    resetBtn.addEventListener("click", resetCurrentRange);
    finishRetryBtn.addEventListener("click", resetCurrentRange);
    micBtn.addEventListener("click", startRecognition);

    answerBtn.addEventListener("click", function() {
        if (!currentItem) return;
        answerBox.style.display = "block";
        answerBox.style.background = "#ecfdf5";
        answerBox.style.borderColor = "#bbf7d0";
        answerBox.style.color = "#166534";
        answerBox.innerText = "정답: " + currentItem.word;
        speak(currentItem.word);

        resultBox.style.display = "block";
        resultBox.innerText = "듣고 다시 말해 보세요.";
        resultBox.style.background = "#eff6ff";
        resultBox.style.borderColor = "#bfdbfe";
        resultBox.style.color = "#1d4ed8";
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
        cleanupRecognition();
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
