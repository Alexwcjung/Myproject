import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="말하면 터지는 문장 게임",
    page_icon="💥",
    layout="centered"
)

# =========================================================
# 제목
# =========================================================
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 50%, #f7fee7 100%);
        padding: 30px 24px;
        border-radius: 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 26px rgba(80, 80, 120, 0.12);
        text-align: center;
        border: 1.5px solid #e0f2fe;
    ">
        <h1 style="color:#334155; margin-bottom:10px; font-size:36px; font-weight:900;">
            💥 말하면 터지는 문장 게임
        </h1>
        <p style="color:#64748b; font-size:19px; margin:0; line-height:1.7;">
            한국어 문장을 보고 영어로 말하면 카드가 팡! 터집니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info("사용 방법: 문법 선택 → 게임 시작 → 한국어 문장을 영어로 말하기 → 맞으면 카드가 터지고 정답과 발음이 나옵니다.")

# =========================================================
# 말하기 문제 데이터
# =========================================================
speaking_questions = [
    {"category": "💪 can 조동사", "korean": "나는 수영할 수 있다.", "sentence": "I can swim."},
    {"category": "💪 can 조동사", "korean": "그녀는 노래할 수 있다.", "sentence": "She can sing."},
    {"category": "💪 can 조동사", "korean": "그들은 축구를 할 수 있다.", "sentence": "They can play soccer."},
    {"category": "💪 can 조동사", "korean": "나는 수영할 수 없다.", "sentence": "I cannot swim."},
    {"category": "💪 can 조동사", "korean": "그는 영어를 말할 수 없다.", "sentence": "He can't speak English."},
    {"category": "💪 can 조동사", "korean": "너는 수영할 수 있니?", "sentence": "Can you swim?"},
    {"category": "💪 can 조동사", "korean": "그녀는 피아노를 칠 수 있니?", "sentence": "Can she play the piano?"},

    {"category": "📢 명령문", "korean": "문을 열어라.", "sentence": "Open the door."},
    {"category": "📢 명령문", "korean": "주의 깊게 들어라.", "sentence": "Listen carefully."},
    {"category": "📢 명령문", "korean": "일어서라.", "sentence": "Stand up."},
    {"category": "📢 명령문", "korean": "교실에서 뛰지 마라.", "sentence": "Don't run in the classroom."},
    {"category": "📢 명령문", "korean": "이것을 만지지 마라.", "sentence": "Don't touch this."},
    {"category": "📢 명령문", "korean": "늦지 마라.", "sentence": "Don't be late."},

    {"category": "📍 There is / are", "korean": "책상 위에 책 한 권이 있다.", "sentence": "There is a book on the desk."},
    {"category": "📍 There is / are", "korean": "교실에 학생 한 명이 있다.", "sentence": "There is a student in the classroom."},
    {"category": "📍 There is / are", "korean": "탁자 아래에 개 한 마리가 있다.", "sentence": "There is a dog under the table."},
    {"category": "📍 There is / are", "korean": "책상 위에 책 두 권이 있다.", "sentence": "There are two books on the desk."},
    {"category": "📍 There is / are", "korean": "교실에 학생 세 명이 있다.", "sentence": "There are three students in the classroom."},
    {"category": "📍 There is / are", "korean": "거리에 많은 자동차들이 있다.", "sentence": "There are many cars on the street."},

    {"category": "🧭 전치사", "korean": "고양이는 상자 안에 있다.", "sentence": "The cat is in the box."},
    {"category": "🧭 전치사", "korean": "책은 책상 위에 있다.", "sentence": "The book is on the desk."},
    {"category": "🧭 전치사", "korean": "공은 의자 아래에 있다.", "sentence": "The ball is under the chair."},
    {"category": "🧭 전치사", "korean": "학교는 공원 옆에 있다.", "sentence": "The school is next to the park."},
    {"category": "🧭 전치사", "korean": "개는 문 뒤에 있다.", "sentence": "The dog is behind the door."},
    {"category": "🧭 전치사", "korean": "버스 정류장은 학교 앞에 있다.", "sentence": "The bus stop is in front of the school."},

    {"category": "💭 want", "korean": "나는 물을 원한다.", "sentence": "I want water."},
    {"category": "💭 want", "korean": "너는 피자를 원한다.", "sentence": "You want pizza."},
    {"category": "💭 want", "korean": "그들은 새 휴대전화를 원한다.", "sentence": "They want a new phone."},
    {"category": "💭 want", "korean": "그는 물을 원한다.", "sentence": "He wants water."},
    {"category": "💭 want", "korean": "그녀는 자전거를 원한다.", "sentence": "She wants a bike."},
    {"category": "💭 want", "korean": "내 남동생은 피자를 원한다.", "sentence": "My brother wants pizza."},

    {"category": "🚀 want to", "korean": "나는 먹고 싶다.", "sentence": "I want to eat."},
    {"category": "🚀 want to", "korean": "나는 집에 가고 싶다.", "sentence": "I want to go home."},
    {"category": "🚀 want to", "korean": "우리는 축구를 하고 싶다.", "sentence": "We want to play soccer."},
    {"category": "🚀 want to", "korean": "그들은 영어를 공부하고 싶다.", "sentence": "They want to study English."},
    {"category": "🚀 want to", "korean": "그는 축구를 하고 싶다.", "sentence": "He wants to play soccer."},
    {"category": "🚀 want to", "korean": "그녀는 노래하고 싶다.", "sentence": "She wants to sing."},
    {"category": "🚀 want to", "korean": "내 여동생은 TV를 보고 싶다.", "sentence": "My sister wants to watch TV."},
    {"category": "🚀 want to", "korean": "나는 물을 마시고 싶다.", "sentence": "I want to drink water."},
    {"category": "🚀 want to", "korean": "그녀는 자전거를 타고 싶다.", "sentence": "She wants to ride a bike."},

    {"category": "🎒 have / has", "korean": "나는 자전거를 가지고 있다.", "sentence": "I have a bike."},
    {"category": "🎒 have / has", "korean": "너는 휴대전화를 가지고 있다.", "sentence": "You have a phone."},
    {"category": "🎒 have / has", "korean": "우리는 많은 책을 가지고 있다.", "sentence": "We have many books."},
    {"category": "🎒 have / has", "korean": "그들은 개 한 마리를 가지고 있다.", "sentence": "They have a dog."},
    {"category": "🎒 have / has", "korean": "그는 자전거를 가지고 있다.", "sentence": "He has a bike."},
    {"category": "🎒 have / has", "korean": "그녀는 개 한 마리를 가지고 있다.", "sentence": "She has a dog."},
    {"category": "🎒 have / has", "korean": "내 친구는 새 휴대전화를 가지고 있다.", "sentence": "My friend has a new phone."},
    {"category": "🎒 have / has", "korean": "그 학교는 체육관을 가지고 있다.", "sentence": "The school has a gym."},

    {"category": "🔗 because", "korean": "나는 영어를 좋아한다. 왜냐하면 재미있기 때문이다.", "sentence": "I like English because it is fun."},
    {"category": "🔗 because", "korean": "그녀는 행복하다. 왜냐하면 개를 가지고 있기 때문이다.", "sentence": "She is happy because she has a dog."},
    {"category": "🔗 because", "korean": "나는 물을 원한다. 왜냐하면 목이 마르기 때문이다.", "sentence": "I want water because I am thirsty."},

    {"category": "🔗 so", "korean": "나는 배고프다. 그래서 피자를 원한다.", "sentence": "I am hungry, so I want pizza."},
    {"category": "🔗 so", "korean": "날씨가 춥다. 그래서 나는 재킷을 입는다.", "sentence": "It is cold, so I wear a jacket."},
    {"category": "🔗 so", "korean": "그는 피곤하다. 그래서 집에 간다.", "sentence": "He is tired, so he goes home."},

    {"category": "🔗 but", "korean": "나는 축구를 좋아한다. 하지만 야구는 좋아하지 않는다.", "sentence": "I like soccer, but I don't like baseball."},
    {"category": "🔗 but", "korean": "그녀는 노래할 수 있다. 하지만 춤은 출 수 없다.", "sentence": "She can sing, but she can't dance."},
    {"category": "🔗 but", "korean": "나는 자전거를 가지고 있다. 하지만 자동차는 가지고 있지 않다.", "sentence": "I have a bike, but I don't have a car."},

    {"category": "🔗 if", "korean": "만약 비가 오면, 나는 집에 있을 것이다.", "sentence": "If it rains, I will stay home."},
    {"category": "🔗 if", "korean": "만약 내가 배고프면, 나는 피자를 먹을 것이다.", "sentence": "If I am hungry, I will eat pizza."},
    {"category": "🔗 if", "korean": "만약 네가 도움이 필요하면, 내가 도와줄 수 있다.", "sentence": "If you need help, I can help you."},
]

# =========================================================
# 게임 설정
# =========================================================
categories = ["전체"] + list(dict.fromkeys([q["category"] for q in speaking_questions]))

selected_category = st.selectbox(
    "연습할 문법을 고르세요.",
    categories
)

if selected_category == "전체":
    filtered_questions = speaking_questions
else:
    filtered_questions = [q for q in speaking_questions if q["category"] == selected_category]

col1, col2 = st.columns(2)

with col1:
    game_question_count = st.slider(
        "🎯 게임 문제 개수",
        min_value=1,
        max_value=len(filtered_questions),
        value=min(10, len(filtered_questions)),
        step=1
    )

with col2:
    pass_ratio = st.slider(
        "✅ 정답 인정 기준",
        min_value=50,
        max_value=100,
        value=70,
        step=5,
        help="낮을수록 학생 발음을 더 너그럽게 인정합니다."
    )

show_hint = st.checkbox("영어 첫 글자 힌트 보이기", value=False)
auto_sound = st.checkbox("맞히면 원어민 발음 자동 재생", value=True)

game_questions = filtered_questions[:game_question_count]

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #ffffff, #f8fbff);
        border-radius: 24px;
        padding: 20px 22px;
        margin: 16px 0 22px 0;
        box-shadow: 0 5px 16px rgba(0,0,0,0.055);
        border: 1.5px solid #edf2ff;
        font-size: 19px;
        line-height: 1.7;
        color: #374151;
    ">
        💡 <b>게임 시작</b>을 누른 뒤, 한국어 문장을 영어로 말하세요.<br>
        맞게 인식되면 카드가 <b>팡!</b> 터지고 정답 문장과 발음 버튼이 나옵니다.
    </div>
    """,
    unsafe_allow_html=True
)

questions_json = json.dumps(game_questions, ensure_ascii=False)
hint_js = "true" if show_hint else "false"
auto_sound_js = "true" if auto_sound else "false"

# =========================================================
# 게임 HTML
# =========================================================
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        background: transparent;
    }}

    .game-wrap {{
        width: 100%;
        min-height: 660px;
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 50%, #f7fee7 100%);
        border: 4px solid #bfdbfe;
        border-radius: 32px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.12);
        padding: 24px;
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
    }}

    .top-bar {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-bottom: 18px;
    }}

    .badge {{
        background: rgba(255,255,255,0.95);
        border: 2px solid #dbeafe;
        border-radius: 20px;
        padding: 12px 8px;
        text-align: center;
        font-size: 19px;
        font-weight: 900;
        color: #334155;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        line-height: 1.4;
    }}

    .message {{
        background: linear-gradient(135deg, #fef3c7, #fed7aa);
        border: 3px solid #fb923c;
        border-radius: 24px;
        padding: 14px;
        text-align: center;
        font-size: 22px;
        font-weight: 900;
        color: #7c2d12;
        margin-bottom: 18px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        min-height: 34px;
        line-height: 1.4;
    }}

    .card-area {{
        width: 100%;
        min-height: 250px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }}

    .question-card {{
        width: 88%;
        min-height: 210px;
        background: linear-gradient(135deg, #ffffff, #fff7ed);
        border: 4px solid #fed7aa;
        border-radius: 34px;
        box-shadow: 0 12px 26px rgba(0,0,0,0.14);
        padding: 28px 24px;
        box-sizing: border-box;
        text-align: center;
        transition: all 0.25s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .question-card.pop {{
        animation: pop 0.55s forwards;
    }}

    @keyframes pop {{
        0% {{
            transform: scale(1);
            opacity: 1;
        }}
        45% {{
            transform: scale(1.25) rotate(3deg);
            opacity: 0.9;
        }}
        100% {{
            transform: scale(0);
            opacity: 0;
        }}
    }}

    .category {{
        font-size: 20px;
        font-weight: 900;
        color: #9a3412;
        margin-bottom: 12px;
    }}

    .korean {{
        font-size: 32px;
        font-weight: 900;
        color: #111827;
        line-height: 1.45;
        word-break: keep-all;
    }}

    .hint {{
        margin-top: 12px;
        font-size: 20px;
        color: #64748b;
        font-weight: 800;
    }}

    .answer-area {{
        display: none;
        width: 88%;
        margin: 18px auto 0 auto;
        background: rgba(255,255,255,0.96);
        border: 2px solid #dbeafe;
        border-radius: 26px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }}

    .answer-label {{
        font-size: 18px;
        font-weight: 900;
        color: #475569;
        margin-bottom: 8px;
    }}

    .answer-sentence {{
        font-size: 29px;
        font-weight: 900;
        color: #2563eb;
        line-height: 1.35;
        margin-bottom: 14px;
    }}

    .btn-row {{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 22px;
    }}

    .btn {{
        border: none;
        border-radius: 999px;
        padding: 13px 24px;
        font-size: 20px;
        font-weight: 900;
        color: white;
        background: linear-gradient(135deg, #ff7eb3, #ffb86c);
        box-shadow: 0 8px 18px rgba(0,0,0,0.18);
        cursor: pointer;
    }}

    .sub-btn {{
        background: linear-gradient(135deg, #60a5fa, #93c5fd);
    }}

    .sound-btn {{
        background: linear-gradient(135deg, #34d399, #60a5fa);
        font-size: 18px;
        padding: 11px 20px;
    }}

    .btn:active {{
        transform: scale(0.96);
    }}

    .recognized {{
        margin-top: 16px;
        text-align: center;
        font-size: 18px;
        font-weight: 800;
        color: #475569;
        min-height: 32px;
        line-height: 1.5;
    }}

    .effect {{
        position: absolute;
        font-size: 44px;
        animation: floatUp 0.8s forwards;
        pointer-events: none;
        z-index: 30;
    }}

    @keyframes floatUp {{
        0% {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
        100% {{
            opacity: 0;
            transform: translateY(-70px) scale(1.6);
        }}
    }}

    @media (max-width: 700px) {{
        .game-wrap {{
            padding: 12px;
            min-height: 640px;
            border-radius: 24px;
            border-width: 3px;
        }}

        .top-bar {{
            gap: 5px;
            margin-bottom: 12px;
        }}

        .badge {{
            font-size: 14px;
            padding: 9px 4px;
            border-radius: 14px;
            line-height: 1.3;
        }}

        .message {{
            font-size: 17px;
            padding: 10px 8px;
            border-radius: 18px;
            margin-bottom: 12px;
        }}

        .card-area {{
            min-height: 240px;
        }}

        .question-card {{
            width: 96%;
            min-height: 210px;
            padding: 22px 14px;
            border-radius: 24px;
        }}

        .category {{
            font-size: 17px;
        }}

        .korean {{
            font-size: 25px;
            line-height: 1.45;
        }}

        .hint {{
            font-size: 17px;
        }}

        .answer-area {{
            width: 96%;
            padding: 14px 12px;
            border-radius: 22px;
        }}

        .answer-sentence {{
            font-size: 23px;
        }}

        .btn {{
            font-size: 15px;
            padding: 10px 13px;
        }}

        .sound-btn {{
            font-size: 15px;
            padding: 10px 13px;
        }}

        .recognized {{
            font-size: 15px;
        }}

        .effect {{
            font-size: 34px;
        }}
    }}
</style>
</head>

<body>
<div class="game-wrap">
    <div class="top-bar">
        <div class="badge">문제<br><span id="qNum">0</span> / <span id="total">0</span></div>
        <div class="badge">점수<br><span id="score">0</span></div>
        <div class="badge">상태<br><span id="state">대기</span></div>
    </div>

    <div id="message" class="message">
        게임 시작을 누르고 한국어 문장을 영어로 말해 보세요!
    </div>

    <div class="card-area">
        <div id="questionCard" class="question-card">
            <div id="category" class="category">문법</div>
            <div id="korean" class="korean">게임 시작을 눌러 주세요 🎮</div>
            <div id="hint" class="hint"></div>
        </div>
    </div>

    <div id="answerArea" class="answer-area">
        <div class="answer-label">정답 문장</div>
        <div id="answerSentence" class="answer-sentence"></div>
        <button class="btn sound-btn" onclick="speakCurrentAnswer()">🔊 원어민 발음 듣기</button>
    </div>

    <div class="btn-row">
        <button class="btn" onclick="startGame()">🎤 게임 시작</button>
        <button class="btn sub-btn" onclick="skipQuestion()">➡️ 넘기기</button>
        <button class="btn sub-btn" onclick="showAnswer()">👀 정답 보기</button>
        <button class="btn sub-btn" onclick="resetGame()">🔄 다시 시작</button>
    </div>

    <div id="recognized" class="recognized">
        Chrome에서 마이크 권한을 허용해 주세요.
    </div>
</div>

<script>
const questions = {questions_json};
const passRatio = {pass_ratio} / 100;
const showHint = {hint_js};
const autoSound = {auto_sound_js};

let currentIndex = 0;
let score = 0;
let gameStarted = false;
let recognition = null;
let locked = false;

const qNum = document.getElementById("qNum");
const total = document.getElementById("total");
const scoreBox = document.getElementById("score");
const stateBox = document.getElementById("state");
const messageBox = document.getElementById("message");
const questionCard = document.getElementById("questionCard");
const categoryBox = document.getElementById("category");
const koreanBox = document.getElementById("korean");
const hintBox = document.getElementById("hint");
const answerArea = document.getElementById("answerArea");
const answerSentence = document.getElementById("answerSentence");
const recognizedBox = document.getElementById("recognized");

total.innerText = questions.length;

function normalizeText(text) {{
    return text
        .toLowerCase()
        .replace(/[.,!?]/g, "")
        .replace(/\\s+/g, " ")
        .trim();
}}

function makeHint(sentence) {{
    return sentence
        .replace(/[.,!?]/g, "")
        .split(" ")
        .map(w => w[0])
        .join(" ");
}}

function similarityCheck(spoken, target) {{
    let s = normalizeText(spoken);
    let t = normalizeText(target);

    if (s.includes(t)) return true;

    let targetWords = t.split(" ");
    let spokenWords = s.split(" ");

    let matched = 0;
    for (let word of targetWords) {{
        if (spokenWords.includes(word)) {{
            matched++;
        }}
    }}

    let ratio = matched / targetWords.length;
    return ratio >= passRatio;
}}

function showCurrentQuestion() {{
    if (currentIndex >= questions.length) {{
        endGame();
        return;
    }}

    locked = false;
    questionCard.classList.remove("pop");
    questionCard.style.opacity = "1";
    questionCard.style.transform = "scale(1)";
    answerArea.style.display = "none";

    const q = questions[currentIndex];

    qNum.innerText = currentIndex + 1;
    categoryBox.innerText = q.category;
    koreanBox.innerText = q.korean;

    if (showHint) {{
        hintBox.innerText = "힌트: " + makeHint(q.sentence);
    }} else {{
        hintBox.innerText = "";
    }}

    messageBox.innerText = "🎧 듣는 중... 영어로 말해 보세요!";
    stateBox.innerText = "듣는 중";
}}

function showAnswerArea() {{
    if (currentIndex >= questions.length) return;

    answerSentence.innerText = questions[currentIndex].sentence;
    answerArea.style.display = "block";
}}

function speakText(text) {{
    if (!("speechSynthesis" in window)) {{
        recognizedBox.innerText = "❌ 이 브라우저는 음성 재생을 지원하지 않습니다.";
        return;
    }}

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 0.85;
    utterance.pitch = 1.0;

    window.speechSynthesis.speak(utterance);
}}

function speakCurrentAnswer() {{
    if (currentIndex >= questions.length) return;
    speakText(questions[currentIndex].sentence);
}}

function showEffects() {{
    const wrap = document.querySelector(".game-wrap");
    const icons = ["💥", "✨", "🎉", "⭐", "👏", "🌟"];

    for (let i = 0; i < 12; i++) {{
        const e = document.createElement("div");
        e.className = "effect";
        e.innerText = icons[Math.floor(Math.random() * icons.length)];
        e.style.left = Math.random() * 80 + 10 + "%";
        e.style.top = Math.random() * 50 + 20 + "%";
        wrap.appendChild(e);

        setTimeout(() => {{
            e.remove();
        }}, 850);
    }}
}}

function correctAnswer() {{
    if (locked) return;

    locked = true;
    score++;
    scoreBox.innerText = score;

    messageBox.innerText = "💥 정답! 카드가 터졌어요!";
    stateBox.innerText = "정답";
    showAnswerArea();

    questionCard.classList.add("pop");
    showEffects();

    if (autoSound) {{
        setTimeout(() => {{
            speakCurrentAnswer();
        }}, 350);
    }}

    setTimeout(() => {{
        currentIndex++;
        showCurrentQuestion();
    }}, 2200);
}}

function skipQuestion() {{
    if (!gameStarted || currentIndex >= questions.length) return;

    locked = true;
    showAnswerArea();
    messageBox.innerText = "➡️ 정답 확인 후 다음 문제로 넘어갑니다.";
    stateBox.innerText = "넘김";

    setTimeout(() => {{
        currentIndex++;
        showCurrentQuestion();
    }}, 1500);
}}

function showAnswer() {{
    if (!gameStarted || currentIndex >= questions.length) return;

    showAnswerArea();
    messageBox.innerText = "👀 정답을 확인하고 발음을 들어 보세요.";
    stateBox.innerText = "정답 보기";
}}

function checkSpeech(transcript) {{
    if (!gameStarted || locked || currentIndex >= questions.length) return;

    recognizedBox.innerText = "🗣️ 인식: " + transcript;

    const target = questions[currentIndex].sentence;

    if (similarityCheck(transcript, target)) {{
        correctAnswer();
    }}
}}

function startRecognition() {{
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {{
        recognizedBox.innerText = "❌ 이 브라우저는 음성 인식을 지원하지 않습니다. Chrome으로 접속해 주세요.";
        return false;
    }}

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = function() {{
        recognizedBox.innerText = "🎧 마이크가 듣고 있습니다.";
    }};

    recognition.onresult = function(event) {{
        let transcript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {{
            transcript += event.results[i][0].transcript;
        }}

        checkSpeech(transcript);
    }};

    recognition.onerror = function(event) {{
        recognizedBox.innerText = "⚠️ 마이크 오류: " + event.error;
    }};

    recognition.onend = function() {{
        if (gameStarted) {{
            try {{
                recognition.start();
            }} catch(e) {{}}
        }}
    }};

    try {{
        recognition.start();
        return true;
    }} catch(e) {{
        recognizedBox.innerText = "⚠️ 마이크를 다시 시작해 주세요.";
        return false;
    }}
}}

function startGame() {{
    if (gameStarted) return;

    gameStarted = true;
    currentIndex = 0;
    score = 0;
    locked = false;

    scoreBox.innerText = score;
    qNum.innerText = 1;
    stateBox.innerText = "시작";

    const ok = startRecognition();
    if (!ok) {{
        gameStarted = false;
        stateBox.innerText = "오류";
        return;
    }}

    showCurrentQuestion();
}}

function resetGame() {{
    gameStarted = false;
    currentIndex = 0;
    score = 0;
    locked = false;

    if (recognition) {{
        try {{
            recognition.stop();
        }} catch(e) {{}}
    }}

    scoreBox.innerText = score;
    qNum.innerText = 0;
    stateBox.innerText = "대기";
    messageBox.innerText = "게임 시작을 누르고 한국어 문장을 영어로 말해 보세요!";
    categoryBox.innerText = "문법";
    koreanBox.innerText = "게임 시작을 눌러 주세요 🎮";
    hintBox.innerText = "";
    answerArea.style.display = "none";
    recognizedBox.innerText = "Chrome에서 마이크 권한을 허용해 주세요.";
    questionCard.classList.remove("pop");
    questionCard.style.opacity = "1";
    questionCard.style.transform = "scale(1)";
}}

function endGame() {{
    gameStarted = false;

    if (recognition) {{
        try {{
            recognition.stop();
        }} catch(e) {{}}
    }}

    stateBox.innerText = "완료";
    messageBox.innerText = "🎉 게임 종료! 수고했습니다!";
    categoryBox.innerText = "최종 점수";
    koreanBox.innerText = score + " / " + questions.length;
    hintBox.innerText = "다시 하려면 다시 시작을 눌러 주세요.";
    answerArea.style.display = "none";
    recognizedBox.innerText = "최종 점수: " + score + "점";
}}
</script>
</body>
</html>
"""

components.html(game_html, height=720)
