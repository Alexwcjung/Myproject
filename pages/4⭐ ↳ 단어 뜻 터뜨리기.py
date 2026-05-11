import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="단어 뜻 터뜨리기 게임",
    page_icon="💥",
    layout="wide"
)

st.title("💥 Survival English 단어 뜻 터뜨리기 게임")
st.caption("첫 번째 학습 단어에 맞춰, 위에서 떨어지는 영어 단어의 한국어 뜻을 입력하면 단어가 터집니다!")

# -----------------------------
# 단어 + 한국어 뜻 목록
# -----------------------------
word_data = [
    {
        "word": "I",
        "meanings": [
            "나"
        ]
    },
    {
        "word": "you",
        "meanings": [
            "너, 당신",
            "너",
            "당신"
        ]
    },
    {
        "word": "he",
        "meanings": [
            "그"
        ]
    },
    {
        "word": "she",
        "meanings": [
            "그녀"
        ]
    },
    {
        "word": "we",
        "meanings": [
            "우리"
        ]
    },
    {
        "word": "they",
        "meanings": [
            "그들",
            "그녀들"
        ]
    },
    {
        "word": "friend",
        "meanings": [
            "친구"
        ]
    },
    {
        "word": "teacher",
        "meanings": [
            "선생님"
        ]
    },
    {
        "word": "student",
        "meanings": [
            "학생"
        ]
    },
    {
        "word": "classmate",
        "meanings": [
            "반 친구"
        ]
    },
    {
        "word": "family",
        "meanings": [
            "가족"
        ]
    },
    {
        "word": "father",
        "meanings": [
            "아버지"
        ]
    },
    {
        "word": "mother",
        "meanings": [
            "어머니"
        ]
    },
    {
        "word": "brother",
        "meanings": [
            "형제, 남자 형제",
            "형제",
            "남자 형제",
            "남자형제",
            "오빠",
            "형",
            "남동생"
        ]
    },
    {
        "word": "sister",
        "meanings": [
            "자매, 여자 형제",
            "자매",
            "여자 형제",
            "여자형제",
            "언니",
            "누나",
            "여동생"
        ]
    },
    {
        "word": "name",
        "meanings": [
            "이름"
        ]
    },
    {
        "word": "person",
        "meanings": [
            "사람"
        ]
    },
    {
        "word": "man",
        "meanings": [
            "남자"
        ]
    },
    {
        "word": "woman",
        "meanings": [
            "여자"
        ]
    },
    {
        "word": "child",
        "meanings": [
            "아이"
        ]
    },
    {
        "word": "go",
        "meanings": [
            "가다"
        ]
    },
    {
        "word": "come",
        "meanings": [
            "오다"
        ]
    },
    {
        "word": "walk",
        "meanings": [
            "걷다"
        ]
    },
    {
        "word": "run",
        "meanings": [
            "달리다"
        ]
    },
    {
        "word": "sit",
        "meanings": [
            "앉다"
        ]
    },
    {
        "word": "stand",
        "meanings": [
            "서다"
        ]
    },
    {
        "word": "stop",
        "meanings": [
            "멈추다"
        ]
    },
    {
        "word": "start",
        "meanings": [
            "시작하다"
        ]
    },
    {
        "word": "open",
        "meanings": [
            "열다"
        ]
    },
    {
        "word": "close",
        "meanings": [
            "닫다"
        ]
    },
    {
        "word": "eat",
        "meanings": [
            "먹다"
        ]
    },
    {
        "word": "drink",
        "meanings": [
            "마시다"
        ]
    },
    {
        "word": "sleep",
        "meanings": [
            "자다"
        ]
    },
    {
        "word": "study",
        "meanings": [
            "공부하다"
        ]
    },
    {
        "word": "read",
        "meanings": [
            "읽다"
        ]
    },
    {
        "word": "write",
        "meanings": [
            "쓰다"
        ]
    },
    {
        "word": "listen",
        "meanings": [
            "듣다"
        ]
    },
    {
        "word": "speak",
        "meanings": [
            "말하다"
        ]
    },
    {
        "word": "help",
        "meanings": [
            "돕다"
        ]
    },
    {
        "word": "wait",
        "meanings": [
            "기다리다"
        ]
    },
    {
        "word": "happy",
        "meanings": [
            "행복한"
        ]
    },
    {
        "word": "sad",
        "meanings": [
            "슬픈"
        ]
    },
    {
        "word": "angry",
        "meanings": [
            "화난"
        ]
    },
    {
        "word": "tired",
        "meanings": [
            "피곤한"
        ]
    },
    {
        "word": "hungry",
        "meanings": [
            "배고픈"
        ]
    },
    {
        "word": "thirsty",
        "meanings": [
            "목마른"
        ]
    },
    {
        "word": "sick",
        "meanings": [
            "아픈"
        ]
    },
    {
        "word": "okay",
        "meanings": [
            "괜찮은",
            "괜찮다"
        ]
    },
    {
        "word": "fine",
        "meanings": [
            "괜찮은",
            "괜찮다"
        ]
    },
    {
        "word": "cold",
        "meanings": [
            "추운, 차가운",
            "추운",
            "차가운",
            "춥다",
            "차갑다"
        ]
    },
    {
        "word": "hot",
        "meanings": [
            "더운, 뜨거운",
            "더운",
            "뜨거운",
            "덥다",
            "뜨겁다"
        ]
    },
    {
        "word": "pain",
        "meanings": [
            "통증"
        ]
    },
    {
        "word": "headache",
        "meanings": [
            "두통"
        ]
    },
    {
        "word": "stomachache",
        "meanings": [
            "복통"
        ]
    },
    {
        "word": "fever",
        "meanings": [
            "열"
        ]
    },
    {
        "word": "hurt",
        "meanings": [
            "아프다, 다치다",
            "아프다",
            "다치다",
            "아픈"
        ]
    },
    {
        "word": "good",
        "meanings": [
            "좋은",
            "좋다"
        ]
    },
    {
        "word": "bad",
        "meanings": [
            "나쁜",
            "나쁘다"
        ]
    },
    {
        "word": "worried",
        "meanings": [
            "걱정하는",
            "걱정되는"
        ]
    },
    {
        "word": "scared",
        "meanings": [
            "무서워하는",
            "무서운"
        ]
    },
    {
        "word": "food",
        "meanings": [
            "음식"
        ]
    },
    {
        "word": "water",
        "meanings": [
            "물"
        ]
    },
    {
        "word": "rice",
        "meanings": [
            "밥, 쌀",
            "밥",
            "쌀"
        ]
    },
    {
        "word": "bread",
        "meanings": [
            "빵"
        ]
    },
    {
        "word": "milk",
        "meanings": [
            "우유"
        ]
    },
    {
        "word": "juice",
        "meanings": [
            "주스"
        ]
    },
    {
        "word": "coffee",
        "meanings": [
            "커피"
        ]
    },
    {
        "word": "tea",
        "meanings": [
            "차"
        ]
    },
    {
        "word": "apple",
        "meanings": [
            "사과"
        ]
    },
    {
        "word": "banana",
        "meanings": [
            "바나나"
        ]
    },
    {
        "word": "egg",
        "meanings": [
            "달걀"
        ]
    },
    {
        "word": "meat",
        "meanings": [
            "고기"
        ]
    },
    {
        "word": "chicken",
        "meanings": [
            "닭고기, 닭",
            "닭고기",
            "닭"
        ]
    },
    {
        "word": "fish",
        "meanings": [
            "생선, 물고기",
            "생선",
            "물고기"
        ]
    },
    {
        "word": "breakfast",
        "meanings": [
            "아침 식사"
        ]
    },
    {
        "word": "lunch",
        "meanings": [
            "점심 식사"
        ]
    },
    {
        "word": "dinner",
        "meanings": [
            "저녁 식사"
        ]
    },
    {
        "word": "snack",
        "meanings": [
            "간식"
        ]
    },
    {
        "word": "medicine",
        "meanings": [
            "약"
        ]
    },
    {
        "word": "hospital",
        "meanings": [
            "병원"
        ]
    },
    {
        "word": "home",
        "meanings": [
            "집"
        ]
    },
    {
        "word": "school",
        "meanings": [
            "학교"
        ]
    },
    {
        "word": "classroom",
        "meanings": [
            "교실"
        ]
    },
    {
        "word": "bathroom",
        "meanings": [
            "화장실"
        ]
    },
    {
        "word": "hospital",
        "meanings": [
            "병원"
        ]
    },
    {
        "word": "store",
        "meanings": [
            "가게"
        ]
    },
    {
        "word": "station",
        "meanings": [
            "역"
        ]
    },
    {
        "word": "bus",
        "meanings": [
            "버스"
        ]
    },
    {
        "word": "car",
        "meanings": [
            "자동차"
        ]
    },
    {
        "word": "taxi",
        "meanings": [
            "택시"
        ]
    },
    {
        "word": "train",
        "meanings": [
            "기차"
        ]
    },
    {
        "word": "bike",
        "meanings": [
            "자전거"
        ]
    },
    {
        "word": "road",
        "meanings": [
            "도로"
        ]
    },
    {
        "word": "street",
        "meanings": [
            "거리"
        ]
    },
    {
        "word": "here",
        "meanings": [
            "여기"
        ]
    },
    {
        "word": "there",
        "meanings": [
            "거기"
        ]
    },
    {
        "word": "near",
        "meanings": [
            "가까운",
            "가깝다"
        ]
    },
    {
        "word": "far",
        "meanings": [
            "먼",
            "멀다"
        ]
    },
    {
        "word": "left",
        "meanings": [
            "왼쪽"
        ]
    },
    {
        "word": "right",
        "meanings": [
            "오른쪽, 맞는",
            "오른쪽",
            "맞는",
            "맞다"
        ]
    },
    {
        "word": "time",
        "meanings": [
            "시간"
        ]
    },
    {
        "word": "now",
        "meanings": [
            "지금"
        ]
    },
    {
        "word": "today",
        "meanings": [
            "오늘"
        ]
    },
    {
        "word": "tomorrow",
        "meanings": [
            "내일"
        ]
    },
    {
        "word": "yesterday",
        "meanings": [
            "어제"
        ]
    },
    {
        "word": "morning",
        "meanings": [
            "아침"
        ]
    },
    {
        "word": "afternoon",
        "meanings": [
            "오후"
        ]
    },
    {
        "word": "evening",
        "meanings": [
            "저녁"
        ]
    },
    {
        "word": "night",
        "meanings": [
            "밤"
        ]
    },
    {
        "word": "nine",
        "meanings": [
            "아홉"
        ]
    },
    {
        "word": "late",
        "meanings": [
            "늦은",
            "늦다"
        ]
    },
    {
        "word": "one",
        "meanings": [
            "하나"
        ]
    },
    {
        "word": "two",
        "meanings": [
            "둘"
        ]
    },
    {
        "word": "three",
        "meanings": [
            "셋"
        ]
    },
    {
        "word": "four",
        "meanings": [
            "넷"
        ]
    },
    {
        "word": "five",
        "meanings": [
            "다섯"
        ]
    },
    {
        "word": "six",
        "meanings": [
            "여섯"
        ]
    },
    {
        "word": "seven",
        "meanings": [
            "일곱"
        ]
    },
    {
        "word": "eight",
        "meanings": [
            "여덟"
        ]
    },
    {
        "word": "ten",
        "meanings": [
            "열"
        ]
    },
    {
        "word": "bag",
        "meanings": [
            "가방"
        ]
    },
    {
        "word": "phone",
        "meanings": [
            "전화기"
        ]
    },
    {
        "word": "book",
        "meanings": [
            "책"
        ]
    },
    {
        "word": "notebook",
        "meanings": [
            "공책"
        ]
    },
    {
        "word": "pen",
        "meanings": [
            "펜"
        ]
    },
    {
        "word": "pencil",
        "meanings": [
            "연필"
        ]
    },
    {
        "word": "desk",
        "meanings": [
            "책상"
        ]
    },
    {
        "word": "chair",
        "meanings": [
            "의자"
        ]
    },
    {
        "word": "door",
        "meanings": [
            "문"
        ]
    },
    {
        "word": "window",
        "meanings": [
            "창문"
        ]
    },
    {
        "word": "key",
        "meanings": [
            "열쇠"
        ]
    },
    {
        "word": "money",
        "meanings": [
            "돈"
        ]
    },
    {
        "word": "card",
        "meanings": [
            "카드"
        ]
    },
    {
        "word": "ticket",
        "meanings": [
            "표, 티켓",
            "표",
            "티켓"
        ]
    },
    {
        "word": "clothes",
        "meanings": [
            "옷"
        ]
    },
    {
        "word": "shoes",
        "meanings": [
            "신발"
        ]
    },
    {
        "word": "hat",
        "meanings": [
            "모자"
        ]
    },
    {
        "word": "watch",
        "meanings": [
            "시계"
        ]
    },
    {
        "word": "cup",
        "meanings": [
            "컵"
        ]
    },
    {
        "word": "bottle",
        "meanings": [
            "병"
        ]
    },
    {
        "word": "help",
        "meanings": [
            "도움, 돕다",
            "도움",
            "돕다"
        ]
    },
    {
        "word": "please",
        "meanings": [
            "부디, 제발",
            "부디",
            "제발"
        ]
    },
    {
        "word": "sorry",
        "meanings": [
            "미안합니다"
        ]
    },
    {
        "word": "excuse me",
        "meanings": [
            "실례합니다"
        ]
    },
    {
        "word": "again",
        "meanings": [
            "다시"
        ]
    },
    {
        "word": "slowly",
        "meanings": [
            "천천히"
        ]
    },
    {
        "word": "understand",
        "meanings": [
            "이해하다"
        ]
    },
    {
        "word": "question",
        "meanings": [
            "질문"
        ]
    },
    {
        "word": "problem",
        "meanings": [
            "문제"
        ]
    },
    {
        "word": "need",
        "meanings": [
            "필요하다"
        ]
    },
    {
        "word": "want",
        "meanings": [
            "원하다"
        ]
    },
    {
        "word": "know",
        "meanings": [
            "알다"
        ]
    },
    {
        "word": "say",
        "meanings": [
            "말하다"
        ]
    },
    {
        "word": "tell",
        "meanings": [
            "말하다, 알려주다",
            "말하다",
            "알려주다"
        ]
    },
    {
        "word": "ask",
        "meanings": [
            "묻다"
        ]
    },
    {
        "word": "answer",
        "meanings": [
            "대답, 답",
            "대답",
            "답"
        ]
    },
    {
        "word": "repeat",
        "meanings": [
            "반복하다"
        ]
    },
    {
        "word": "speak",
        "meanings": [
            "말하다"
        ]
    },
    {
        "word": "look",
        "meanings": [
            "보다"
        ]
    },
    {
        "word": "listen",
        "meanings": [
            "듣다"
        ]
    }
]

# -----------------------------
# 조절 옵션
# -----------------------------
speed = st.slider(
    "🚀 떨어지는 속도",
    min_value=1,
    max_value=10,
    value=3,
    help="숫자가 클수록 단어가 더 빠르게 떨어집니다."
)

word_count = st.slider(
    "📚 사용할 단어 개수",
    min_value=5,
    max_value=len(word_data),
    value=15
)

batch_count = st.slider(
    "🌧️ 한 번에 떨어지는 단어 개수",
    min_value=1,
    max_value=5,
    value=1
)

spawn_interval = st.slider(
    "⏳ 단어 나오는 간격",
    min_value=800,
    max_value=3500,
    value=2000,
    step=100,
    help="숫자가 클수록 단어가 더 천천히 나옵니다."
)

show_hint = st.checkbox(
    "💡 뜻 힌트 보기",
    value=False
)

selected_words = word_data[:word_count]
word_data_js = json.dumps(selected_words, ensure_ascii=False)
show_hint_js = "true" if show_hint else "false"

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
    body {{
        margin: 0;
        overflow: hidden;
        font-family: Arial, sans-serif;
        background: linear-gradient(180deg, #dff7ff, #fff7d6);
    }}

    #gameArea {{
        position: relative;
        width: 100%;
        height: 660px;
        overflow: hidden;
        border-radius: 28px;
        background: linear-gradient(180deg, #aeefff 0%, #fff4bd 100%);
        border: 5px solid white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}

    .word {{
        position: absolute;
        top: -80px;
        padding: 14px 24px;
        font-size: 30px;
        font-weight: bold;
        color: #333;
        background: white;
        border-radius: 999px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.18);
        transition: transform 0.2s, opacity 0.2s;
        white-space: nowrap;
        border: 3px solid #ffd6ea;
        z-index: 5;
    }}

    .pop {{
        animation: pop 0.35s forwards;
    }}

    @keyframes pop {{
        0% {{
            transform: scale(1);
            opacity: 1;
        }}
        50% {{
            transform: scale(1.8) rotate(10deg);
            opacity: 0.8;
        }}
        100% {{
            transform: scale(0);
            opacity: 0;
        }}
    }}

    #status {{
        position: absolute;
        top: 15px;
        left: 20px;
        z-index: 20;
        background: rgba(255,255,255,0.94);
        padding: 12px 18px;
        border-radius: 20px;
        font-size: 19px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        max-width: 55%;
        line-height: 1.4;
    }}

    #scoreBox {{
        position: absolute;
        top: 15px;
        right: 20px;
        z-index: 20;
        background: rgba(255,255,255,0.94);
        padding: 12px 18px;
        border-radius: 20px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }}

    #inputPanel {{
        position: absolute;
        bottom: 22px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 30;
        width: 86%;
        background: rgba(255,255,255,0.95);
        border: 3px solid #bfdbfe;
        border-radius: 28px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        box-sizing: border-box;
        text-align: center;
    }}

    #answerInput {{
        width: 68%;
        padding: 14px 18px;
        border-radius: 999px;
        border: 2px solid #93c5fd;
        font-size: 22px;
        font-weight: bold;
        outline: none;
        text-align: center;
    }}

    #answerInput:focus {{
        border-color: #ec4899;
        box-shadow: 0 0 0 4px rgba(236,72,153,0.15);
    }}

    #submitBtn {{
        margin-left: 10px;
        padding: 14px 24px;
        border: none;
        border-radius: 999px;
        font-size: 21px;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #ff7eb3, #ffb86c);
        box-shadow: 0 6px 14px rgba(0,0,0,0.18);
    }}

    #startBtn {{
        margin-left: 10px;
        padding: 14px 24px;
        border: none;
        border-radius: 999px;
        font-size: 21px;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #60a5fa, #34d399);
        box-shadow: 0 6px 14px rgba(0,0,0,0.18);
    }}

    #hintBox {{
        margin-top: 10px;
        font-size: 17px;
        font-weight: bold;
        color: #475569;
        min-height: 24px;
    }}

    .effect {{
        position: absolute;
        font-size: 42px;
        pointer-events: none;
        animation: floatUp 0.7s forwards;
        z-index: 40;
    }}

    @keyframes floatUp {{
        0% {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
        100% {{
            opacity: 0;
            transform: translateY(-60px) scale(1.5);
        }}
    }}

    @media (max-width: 700px) {{
        #gameArea {{
            height: 620px;
            border-radius: 22px;
        }}

        .word {{
            font-size: 24px;
            padding: 11px 18px;
        }}

        #status {{
            font-size: 15px;
            max-width: 52%;
            padding: 9px 12px;
            top: 10px;
            left: 10px;
        }}

        #scoreBox {{
            font-size: 16px;
            padding: 9px 12px;
            top: 10px;
            right: 10px;
        }}

        #inputPanel {{
            width: 94%;
            padding: 14px 12px;
            bottom: 14px;
        }}

        #answerInput {{
            width: 58%;
            font-size: 18px;
            padding: 12px 14px;
        }}

        #submitBtn, #startBtn {{
            font-size: 16px;
            padding: 12px 14px;
            margin-left: 4px;
        }}

        #hintBox {{
            font-size: 14px;
        }}
    }}
</style>
</head>

<body>
<div id="gameArea">
    <div id="status">🎮 게임 시작을 누르세요</div>
    <div id="scoreBox">점수: <span id="score">0</span></div>

    <div id="inputPanel">
        <input id="answerInput" type="text" placeholder="한국어 뜻 입력 예: 고양이" autocomplete="off">
        <button id="submitBtn">💥 제출</button>
        <button id="startBtn">▶️ 시작</button>
        <div id="hintBox"></div>
    </div>
</div>

<script>
const wordData = {word_data_js};
const showHint = {show_hint_js};

const gameArea = document.getElementById("gameArea");
const statusBox = document.getElementById("status");
const scoreSpan = document.getElementById("score");
const answerInput = document.getElementById("answerInput");
const submitBtn = document.getElementById("submitBtn");
const startBtn = document.getElementById("startBtn");
const hintBox = document.getElementById("hintBox");

let activeWords = [];
let score = 0;
let gameStarted = false;
let createInterval = null;

let fallSpeed = {speed};
let batchCount = {batch_count};
let spawnInterval = {spawn_interval};

// 속도 조절: 숫자가 클수록 빠름
let baseSpeed = 0.10 + fallSpeed * 0.06;

// 단어 겹침 방지용 레인
const laneCount = 6;
let laneBusy = Array(laneCount).fill(false);

function normalizeKorean(text) {{
    return text
        .toLowerCase()
        .replace(/\\s+/g, "")
        .replace(/[.,!?~]/g, "")
        .trim();
}}

function getLaneX(laneIndex) {{
    const areaWidth = gameArea.clientWidth;
    const laneWidth = areaWidth / laneCount;
    const maxOffset = Math.max(5, laneWidth - 120);
    const randomOffset = 6 + Math.random() * maxOffset;
    return laneIndex * laneWidth + randomOffset;
}}

function getFreeLane() {{
    let freeLanes = [];

    for (let i = 0; i < laneCount; i++) {{
        if (!laneBusy[i]) {{
            freeLanes.push(i);
        }}
    }}

    if (freeLanes.length === 0) {{
        return null;
    }}

    return freeLanes[Math.floor(Math.random() * freeLanes.length)];
}}

function createOneWord() {{
    if (!gameStarted) return;

    const lane = getFreeLane();
    if (lane === null) return;

    laneBusy[lane] = true;

    const item = wordData[Math.floor(Math.random() * wordData.length)];
    const wordDiv = document.createElement("div");

    wordDiv.className = "word";
    wordDiv.innerText = item.word;
    wordDiv.dataset.word = item.word;
    wordDiv.style.left = getLaneX(lane) + "px";
    wordDiv.style.top = "-80px";

    gameArea.appendChild(wordDiv);

    activeWords.push({{
        element: wordDiv,
        word: item.word,
        meanings: item.meanings,
        y: -80,
        speed: baseSpeed + Math.random() * 0.12,
        lane: lane
    }});

    setTimeout(() => {{
        laneBusy[lane] = false;
    }}, 2200);
}}

function createWordsBatch() {{
    if (!gameStarted) return;

    for (let i = 0; i < batchCount; i++) {{
        setTimeout(() => {{
            createOneWord();
        }}, i * 300);
    }}
}}

function moveWords() {{
    for (let i = activeWords.length - 1; i >= 0; i--) {{
        let item = activeWords[i];
        item.y += item.speed;
        item.element.style.top = item.y + "px";

        if (item.y > gameArea.clientHeight - 120) {{
            item.element.remove();
            activeWords.splice(i, 1);
        }}
    }}

    updateHint();
    requestAnimationFrame(moveWords);
}}

function checkAnswer() {{
    if (!gameStarted) return;

    const userAnswer = normalizeKorean(answerInput.value);

    if (!userAnswer) {{
        statusBox.innerText = "✏️ 한국어 뜻을 입력하세요!";
        return;
    }}

    for (let i = activeWords.length - 1; i >= 0; i--) {{
        let item = activeWords[i];

        let correct = item.meanings.some(m => normalizeKorean(m) === userAnswer);

        if (correct) {{
            popWord(item, i);
            answerInput.value = "";
            return;
        }}
    }}

    statusBox.innerText = "🤔 아직 맞는 단어가 없어요: " + answerInput.value;
    answerInput.select();
}}

function popWord(item, index) {{
    const rect = item.element.getBoundingClientRect();
    const parentRect = gameArea.getBoundingClientRect();

    showEffect(
        rect.left - parentRect.left,
        rect.top - parentRect.top
    );

    item.element.classList.add("pop");

    setTimeout(() => {{
        if (item.element) item.element.remove();
    }}, 300);

    activeWords.splice(index, 1);
    score++;
    scoreSpan.innerText = score;

    statusBox.innerText = "✅ 정답! " + item.word + " = " + item.meanings[0];
}}

function showEffect(x, y) {{
    const effects = ["💥", "✨", "🎉", "⭐", "👏", "🌟"];
    const effect = document.createElement("div");
    effect.className = "effect";
    effect.innerText = effects[Math.floor(Math.random() * effects.length)];
    effect.style.left = x + "px";
    effect.style.top = y + "px";
    gameArea.appendChild(effect);

    setTimeout(() => {{
        effect.remove();
    }}, 700);
}}

function updateHint() {{
    if (!showHint || !gameStarted) {{
        hintBox.innerText = "";
        return;
    }}

    if (activeWords.length === 0) {{
        hintBox.innerText = "";
        return;
    }}

    const sample = activeWords[activeWords.length - 1];
    const firstMeaning = sample.meanings[0];
    hintBox.innerText = "💡 힌트: 화면의 한 단어 뜻은 '" + firstMeaning[0] + "'로 시작합니다.";
}}

function startGame() {{
    if (gameStarted) return;

    gameStarted = true;
    score = 0;
    activeWords = [];
    scoreSpan.innerText = score;
    statusBox.innerText = "✏️ 떨어지는 단어의 한국어 뜻을 입력하세요!";

    answerInput.focus();

    if (createInterval) {{
        clearInterval(createInterval);
    }}

    createInterval = setInterval(createWordsBatch, spawnInterval);
}}

submitBtn.addEventListener("click", checkAnswer);

answerInput.addEventListener("keydown", function(event) {{
    if (event.key === "Enter") {{
        checkAnswer();
    }}
}});

startBtn.addEventListener("click", startGame);

moveWords();
</script>
</body>
</html>
"""

components.html(html_code, height=730)
