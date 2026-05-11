import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="문장 구조 말하기 게임",
    page_icon="🎤",
    layout="centered"
)

# =========================================================
# 디자인 CSS
# =========================================================
st.markdown(
    """
    <style>
    .main {
        background-color: #fffdfc;
    }

    .title-box {
        background: linear-gradient(135deg, #fff7ed 0%, #fffdf7 50%, #eef7ff 100%);
        padding: 30px 24px;
        border-radius: 30px;
        margin-bottom: 22px;
        box-shadow: 0 10px 26px rgba(80, 80, 120, 0.12);
        text-align: center;
        border: 1.5px solid #fed7aa;
    }

    .title-box h1 {
        color: #334155;
        margin-bottom: 10px;
        font-size: 35px;
        font-weight: 900;
    }

    .title-box p {
        color: #64748b;
        font-size: 18px;
        margin: 0;
        line-height: 1.7;
    }

    .guide-card {
        background: linear-gradient(135deg, #ffffff, #f8fbff);
        border-radius: 24px;
        padding: 18px 20px;
        margin: 14px 0 20px 0;
        box-shadow: 0 5px 16px rgba(0,0,0,0.055);
        border: 1.5px solid #edf2ff;
    }

    .guide-card p {
        font-size: 19px;
        line-height: 1.65;
        color: #374151;
        margin: 0;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 800;
        padding: 0.45rem 1.1rem;
        border: 1.5px solid #d9e7ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 제목
# =========================================================
st.markdown(
    """
    <div class="title-box">
        <h1>🎤 문장 구조 말하기 게임</h1>
        <p>한국어 문장을 보고 영어로 말하면 카드가 팡! 터지고 다음 문제가 바로 나옵니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info("사용 방법: 문법 선택 → 게임 시작 → 한국어 문장을 영어로 말하기 → 맞으면 정답과 발음 확인!")

# =========================================================
# 말하기 문제
# =========================================================
speaking_questions = [
    {"category": "🌱 Be동사", "korean": "나는 학생이다.", "sentence": "I am a student."},
    {"category": "🌱 Be동사", "korean": "그녀는 행복하다.", "sentence": "She is happy."},
    {"category": "🌱 Be동사", "korean": "그는 친절하다.", "sentence": "He is kind."},
    {"category": "🌱 Be동사", "korean": "그들은 바쁘다.", "sentence": "They are busy."},
    {"category": "🌱 Be동사", "korean": "우리는 학생들이다.", "sentence": "We are students."},

    {"category": "🏃 현재진행형", "korean": "나는 점심을 먹고 있다.", "sentence": "I am eating lunch."},
    {"category": "🏃 현재진행형", "korean": "그녀는 책을 읽고 있다.", "sentence": "She is reading a book."},
    {"category": "🏃 현재진행형", "korean": "그들은 축구를 하고 있다.", "sentence": "They are playing soccer."},
    {"category": "🏃 현재진행형", "korean": "그는 음악을 듣고 있다.", "sentence": "He is listening to music."},
    {"category": "🏃 현재진행형", "korean": "우리는 영어를 공부하고 있다.", "sentence": "We are studying English."},

    {"category": "🚀 미래형 will", "korean": "나는 영어를 공부할 것이다.", "sentence": "I will study English."},
    {"category": "🚀 미래형 will", "korean": "그녀는 나에게 전화할 것이다.", "sentence": "She will call me."},
    {"category": "🚀 미래형 will", "korean": "우리는 부산에 갈 것이다.", "sentence": "We will go to Busan."},
    {"category": "🚀 미래형 will", "korean": "그는 축구를 할 것이다.", "sentence": "He will play soccer."},

    {"category": "🚀 미래형 be going to", "korean": "나는 영어를 공부할 예정이다.", "sentence": "I am going to study English."},
    {"category": "🚀 미래형 be going to", "korean": "그녀는 나에게 전화할 예정이다.", "sentence": "She is going to call me."},
    {"category": "🚀 미래형 be going to", "korean": "우리는 부산에 갈 예정이다.", "sentence": "We are going to go to Busan."},
    {"category": "🚀 미래형 be going to", "korean": "그들은 축구를 할 예정이다.", "sentence": "They are going to play soccer."},

    {"category": "🕰️ 과거형", "korean": "나는 어제 축구를 했다.", "sentence": "I played soccer yesterday."},
    {"category": "🕰️ 과거형", "korean": "그녀는 학교에 걸어갔다.", "sentence": "She walked to school."},
    {"category": "🕰️ 과거형", "korean": "우리는 방을 청소했다.", "sentence": "We cleaned the room."},
    {"category": "🕰️ 과거형", "korean": "나는 어제 점심을 먹었다.", "sentence": "I ate lunch yesterday."},
    {"category": "🕰️ 과거형", "korean": "그는 학교에 갔다.", "sentence": "He went to school."},

    {"category": "❌ 부정문", "korean": "나는 학생이 아니다.", "sentence": "I am not a student."},
    {"category": "❌ 부정문", "korean": "그녀는 행복하지 않다.", "sentence": "She is not happy."},
    {"category": "❌ 부정문", "korean": "그들은 바쁘지 않다.", "sentence": "They are not busy."},
    {"category": "❌ 부정문", "korean": "나는 커피를 좋아하지 않는다.", "sentence": "I do not like coffee."},
    {"category": "❌ 부정문", "korean": "그는 축구를 하지 않는다.", "sentence": "He does not play soccer."},
    {"category": "❌ 부정문", "korean": "그들은 어제 학교에 가지 않았다.", "sentence": "They did not go to school yesterday."},

    {"category": "❓ 의문문", "korean": "너는 학생이니?", "sentence": "Are you a student?"},
    {"category": "❓ 의문문", "korean": "그녀는 행복하니?", "sentence": "Is she happy?"},
    {"category": "❓ 의문문", "korean": "그들은 교실에 있니?", "sentence": "Are they in the classroom?"},
    {"category": "❓ 의문문", "korean": "너는 커피를 좋아하니?", "sentence": "Do you like coffee?"},
    {"category": "❓ 의문문", "korean": "그는 축구를 하니?", "sentence": "Does he play soccer?"},
    {"category": "❓ 의문문", "korean": "그들은 어제 학교에 갔니?", "sentence": "Did they go to school yesterday?"},

    {"category": "🕵️ 의문사 의문문", "korean": "너는 무엇을 좋아하니?", "sentence": "What do you like?"},
    {"category": "🕵️ 의문사 의문문", "korean": "너는 언제 일어나니?", "sentence": "When do you get up?"},
    {"category": "🕵️ 의문사 의문문", "korean": "너는 어디에 사니?", "sentence": "Where do you live?"},
    {"category": "🕵️ 의문사 의문문", "korean": "너는 왜 행복하니?", "sentence": "Why are you happy?"},
    {"category": "🕵️ 의문사 의문문", "korean": "너는 어떻게 학교에 가니?", "sentence": "How do you go to school?"},
    {"category": "🕵️ 의문사 의문문", "korean": "그는 누구니?", "sentence": "Who is he?"},
]

# =========================================================
# 선택 영역
# =========================================================
categories = ["전체"] + sorted(list(set([q["category"] for q in speaking_questions])))

selected_category = st.selectbox(
    "연습할 문법을 고르세요.",
    categories
)

if selected_category == "전체":
    filtered_questions = speaking_questions
else:
    filtered_questions = [q for q in speaking_questions if q["category"] == selected_category]

game_question_count = st.slider(
    "🎯 게임 문제 개수",
    min_value=3,
    max_value=len(filtered_questions),
    value=min(10, len(filtered_questions))
)

pass_ratio = st.slider(
    "✅ 정답 인정 기준",
    min_value=50,
    max_value=100,
    value=70,
    step=5,
    help="낮을수록 학생 발음을 더 너그럽게 인정합니다."
)

show_english_hint = st.checkbox("영어 첫 글자 힌트 보이기", value=False)

game_questions = filtered_questions[:game_question_count]

st.markdown(
    """
    <div class="guide-card">
        <p>
            <b>게임 시작</b>을 누른 뒤, 화면에 나오는 한국어 문장을 영어로 말하세요.<br>
            맞으면 카드가 터지고, <b>정답 문장과 원어민 발음 버튼</b>이 바로 나옵니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 빠른 진행 말하기 게임
# =========================================================
questions_json = json.dumps(game_questions, ensure_ascii=False)
hint_value = "true" if show_english_hint else "false"

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
        min-height: 560px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #fff7ed, #eef7ff);
        border: 2px solid #fed7aa;
        border-radius: 30px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.08);
        padding: 24px 18px;
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
    }}

    .top-bar {{
        width: 92%;
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 18px;
        flex-wrap: wrap;
    }}

    .badge {{
        background: rgba(255,255,255,0.95);
        border-radius: 999px;
        padding: 10px 16px;
        font-size: 18px;
        font-weight: 900;
        color: #334155;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}

    .category {{
        font-size: 19px;
        font-weight: 900;
        color: #9a3412;
        margin-bottom: 12px;
        text-align: center;
    }}

    .bubble {{
        background: white;
        border: 4px solid #ffd6ea;
        border-radius: 32px;
        width: 88%;
        min-height: 135px;
        padding: 24px 22px;
        text-align: center;
        box-shadow: 0 10px 24px rgba(0,0,0,0.14);
        transition: all 0.22s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}

    .korean {{
        font-size: 34px;
        font-weight: 900;
        color: #111827;
        line-height: 1.35;
    }}

    .hint {{
        margin-top: 12px;
        font-size: 20px;
        color: #64748b;
        font-weight: 800;
    }}

    .bubble.pop {{
        animation: pop 0.42s forwards;
    }}

    @keyframes pop {{
        0% {{
            transform: scale(1);
            opacity: 1;
        }}
        45% {{
            transform: scale(1.35) rotate(3deg);
            opacity: 0.9;
        }}
        100% {{
            transform: scale(0);
            opacity: 0;
        }}
    }}

    .answer-area {{
        width: 88%;
        margin-top: 18px;
        background: rgba(255,255,255,0.96);
        border: 2px solid #dbeafe;
        border-radius: 26px;
        padding: 18px 18px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        display: none;
    }}

    .answer-label {{
        font-size: 18px;
        font-weight: 900;
        color: #475569;
        margin-bottom: 8px;
    }}

    .answer-sentence {{
        font-size: 30px;
        font-weight: 900;
        color: #2563eb;
        line-height: 1.35;
        margin-bottom: 14px;
    }}

    .btn-row {{
        display: flex;
        gap: 10px;
        margin-top: 22px;
        flex-wrap: wrap;
        justify-content: center;
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
    }}

    .sub-btn {{
        background: linear-gradient(135deg, #60a5fa, #93c5fd);
    }}

    .sound-btn {{
        background: linear-gradient(135deg, #34d399, #60a5fa);
        font-size: 19px;
        padding: 12px 22px;
    }}

    .btn:active {{
        transform: scale(0.96);
    }}

    .status {{
        margin-top: 16px;
        font-size: 18px;
        font-weight: 800;
        color: #475569;
        text-align: center;
        min-height: 30px;
        line-height: 1.45;
    }}

    .effect {{
        position: absolute;
        font-size: 42px;
        animation: floatUp 0.75s forwards;
        pointer-events: none;
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
</style>
</head>

<body>
<div class="game-wrap">
    <div class="top-bar">
        <div class="badge">문제 <span id="qNum">1</span> / <span id="total">0</span></div>
        <div class="badge">점수 <span id="score">0</span></div>
    </div>

    <div id="category" class="category">문법</div>

    <div id="bubble" class="bubble">
        <div id="korean" class="korean">게임 시작을 눌러 주세요 🎮</div>
        <div id="hint" class="hint"></div>
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
    </div>

    <div id="status" class="status">시작하면 마이크가 계속 듣고, 맞히면 정답과 발음 버튼이 바로 나옵니다.</div>
</div>

<script>
const questions = {questions_json};
const passRatio = {pass_ratio} / 100;
const showHint = {hint_value};

let currentIndex = 0;
let score = 0;
let recognition = null;
let gameStarted = false;
let recognizing = false;
let locked = false;

const qNum = document.getElementById("qNum");
const total = document.getElementById("total");
const scoreBox = document.getElementById("score");
const categoryBox = document.getElementById("category");
const koreanBox = document.getElementById("korean");
const hintBox = document.getElementById("hint");
const bubble = document.getElementById("bubble");
const statusBox = document.getElementById("status");
const answerArea = document.getElementById("answerArea");
const answerSentence = document.getElementById("answerSentence");

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
        .split(" ")
        .map(w => w[0])
        .join(" ");
}}

function showCurrentQuestion() {{
    if (currentIndex >= questions.length) {{
        endGame();
        return;
    }}

    locked = false;
    bubble.classList.remove("pop");
    bubble.style.opacity = "1";
    bubble.style.transform = "scale(1)";
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

    statusBox.innerText = "🎧 듣는 중... 영어로 말해 보세요!";
}}

function similarityCheck(spoken, target) {{
    let s = normalizeText(spoken);
    let t = normalizeText(target);

    if (s.includes(t)) {{
        return true;
    }}

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

function showEffects() {{
    const wrap = document.querySelector(".game-wrap");
    const icons = ["💥", "✨", "🎉", "⭐", "👏", "🌟"];

    for (let i = 0; i < 10; i++) {{
        const e = document.createElement("div");
        e.className = "effect";
        e.innerText = icons[Math.floor(Math.random() * icons.length)];
        e.style.left = Math.random() * 85 + 5 + "%";
        e.style.top = Math.random() * 50 + 20 + "%";
        wrap.appendChild(e);

        setTimeout(() => {{
            e.remove();
        }}, 800);
    }}
}}

function showAnswerArea() {{
    if (currentIndex >= questions.length) return;

    answerSentence.innerText = questions[currentIndex].sentence;
    answerArea.style.display = "block";
}}

function speakText(text) {{
    if (!("speechSynthesis" in window)) {{
        statusBox.innerText = "❌ 이 브라우저는 음성 재생을 지원하지 않습니다.";
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

function correctAnswer() {{
    if (locked) return;
    locked = true;

    score++;
    scoreBox.innerText = score;

    statusBox.innerText = "✅ 정답! 정답 문장과 발음을 확인하세요.";
    showAnswerArea();

    bubble.classList.add("pop");
    showEffects();

    // 맞히면 자동으로 발음도 한 번 들려줌
    setTimeout(() => {{
        speakCurrentAnswer();
    }}, 350);

    // 1.8초 뒤 다음 문제로 이동
    setTimeout(() => {{
        currentIndex++;
        showCurrentQuestion();
    }}, 1800);
}}

function skipQuestion() {{
    if (!gameStarted) return;

    showAnswerArea();
    statusBox.innerText = "➡️ 정답을 확인하고 다음 문제로 넘어갑니다.";

    setTimeout(() => {{
        currentIndex++;
        showCurrentQuestion();
    }}, 1000);
}}

function showAnswer() {{
    if (!gameStarted) return;

    showAnswerArea();
    statusBox.innerText = "👀 정답을 확인한 뒤, 발음 버튼을 눌러 들어보세요.";
}}

function startGame() {{
    if (gameStarted) return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {{
        statusBox.innerText = "❌ 이 브라우저는 음성 인식을 지원하지 않습니다. Chrome으로 접속해 주세요.";
        return;
    }}

    gameStarted = true;
    currentIndex = 0;
    score = 0;
    scoreBox.innerText = score;

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = function() {{
        recognizing = true;
        statusBox.innerText = "🎧 듣는 중...";
    }};

    recognition.onresult = function(event) {{
        if (!gameStarted || locked || currentIndex >= questions.length) return;

        let transcript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {{
            transcript += event.results[i][0].transcript;
        }}

        statusBox.innerText = "🗣️ " + transcript;

        const target = questions[currentIndex].sentence;

        if (similarityCheck(transcript, target)) {{
            correctAnswer();
        }}
    }};

    recognition.onerror = function(event) {{
        statusBox.innerText = "⚠️ 마이크 오류: " + event.error;
    }};

    recognition.onend = function() {{
        recognizing = false;
        if (gameStarted && currentIndex < questions.length) {{
            try {{
                recognition.start();
            }} catch(e) {{}}
        }}
    }};

    showCurrentQuestion();
    recognition.start();
}}

function endGame() {{
    gameStarted = false;

    if (recognition) {{
        try {{
            recognition.stop();
        }} catch(e) {{}}
    }}

    categoryBox.innerText = "🎉 게임 종료";
    koreanBox.innerText = "최종 점수: " + score + " / " + questions.length;
    hintBox.innerText = "수고했습니다!";
    answerArea.style.display = "none";
    statusBox.innerText = "다시 하려면 페이지를 새로고침하세요.";
}}
</script>
</body>
</html>
"""

components.html(game_html, height=620)
