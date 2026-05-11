import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Phonics Speaking Mole Pop Game",
    page_icon="💥",
    layout="wide"
)

# =========================
# 파닉스 단어 세트
# =========================
PHONICS_WORD_SETS = {
    "짧은 모음": [
        "cat", "bat", "map", "hat", "bed", "red", "pen", "sit", "pig", "fish",
        "hot", "dog", "box", "cup", "sun", "run", "bus", "bug"
    ],
    "긴 모음": [
        "cake", "name", "rain", "day", "tree", "see", "bike", "kite",
        "home", "boat", "cube", "music"
    ],
    "자음 이어 읽기": [
        "black", "brown", "clock", "crab", "frog", "green", "plane",
        "snake", "spoon", "star", "tree", "smile"
    ],
    "두 글자 한 소리": [
        "chair", "ship", "three", "this", "phone", "duck", "whale",
        "chick", "shell", "thin"
    ],
    "모음 두 글자 소리": [
        "rain", "day", "see", "eat", "boat", "snow", "cow", "house",
        "coin", "boy"
    ],
    "자음 예외": [
        "city", "cent", "cycle", "gem", "giant", "gym", "knee",
        "write", "lamb", "exam"
    ]
}

# =========================
# 상단 화면
# =========================
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #fff1f2 0%, #eef2ff 50%, #ecfeff 100%);
        border-radius: 30px;
        padding: 32px;
        margin-bottom: 24px;
        text-align: center;
        border: 1px solid #fbcfe8;
        box-shadow: 0 10px 24px rgba(0,0,0,0.08);
    ">
        <div style="font-size: 42px; font-weight: 900; color: #334155;">
            💥🐹 파닉스 발음 두더지 터뜨리기
        </div>
        <div style="font-size: 18px; color: #64748b; line-height: 1.8; margin-top: 10px;">
            단어 두더지가 튀어나오면 그 단어를 영어로 말해 보세요.<br>
            발음이 인식되면 두더지가 펑! 하고 터집니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

selected_set = st.selectbox(
    "연습할 파닉스 영역을 선택하세요",
    list(PHONICS_WORD_SETS.keys())
)

words = PHONICS_WORD_SETS[selected_set]
words_js_array = "[" + ",".join([f'"{w}"' for w in words]) + "]"

# =========================
# HTML / JS 게임
# =========================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        background: #fffdfb;
    }}

    .game-wrap {{
        max-width: 1120px;
        margin: 0 auto;
        padding: 20px;
    }}

    .control-box {{
        background: linear-gradient(135deg, #fff7ed 0%, #fffbeb 100%);
        border: 1px solid #fed7aa;
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    }}

    .title {{
        font-size: 28px;
        font-weight: 900;
        color: #c2410c;
        margin-bottom: 10px;
    }}

    .desc {{
        font-size: 16px;
        color: #7c2d12;
        line-height: 1.7;
        margin-bottom: 15px;
    }}

    .btn {{
        border: none;
        border-radius: 999px;
        padding: 13px 24px;
        margin: 5px;
        font-size: 17px;
        font-weight: 900;
        cursor: pointer;
        background: #f97316;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }}

    .btn:hover {{
        background: #ea580c;
    }}

    .btn-stop {{
        background: #64748b;
    }}

    .btn-stop:hover {{
        background: #475569;
    }}

    .status-box {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 14px;
        margin-bottom: 20px;
    }}

    .status-card {{
        background: white;
        border-radius: 20px;
        padding: 16px;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}

    .status-label {{
        font-size: 14px;
        color: #64748b;
        font-weight: 800;
        margin-bottom: 6px;
    }}

    .status-value {{
        font-size: 24px;
        color: #111827;
        font-weight: 900;
    }}

    .board {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 22px;
        margin-top: 20px;
    }}

    .hole {{
        position: relative;
        height: 190px;
        background: linear-gradient(180deg, #d9f99d 0%, #86efac 55%, #4ade80 100%);
        border-radius: 28px;
        overflow: hidden;
        box-shadow: inset 0 -12px 0 rgba(22, 101, 52, 0.18), 0 8px 18px rgba(0,0,0,0.08);
        border: 2px solid #bbf7d0;
    }}

    .ground-hole {{
        position: absolute;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        width: 72%;
        height: 42px;
        background: #78350f;
        border-radius: 50%;
        box-shadow: inset 0 8px 15px rgba(0,0,0,0.45);
        z-index: 1;
    }}

    .mole {{
        position: absolute;
        left: 50%;
        bottom: -125px;
        transform: translateX(-50%);
        width: 155px;
        height: 138px;
        background: linear-gradient(135deg, #92400e 0%, #b45309 100%);
        border-radius: 50% 50% 35% 35%;
        z-index: 2;
        transition: bottom 0.32s ease;
        text-align: center;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.18);
    }}

    .mole.show {{
        bottom: 34px;
        animation: popUp 0.42s ease;
    }}

    @keyframes popUp {{
        0% {{ transform: translateX(-50%) scale(0.65); }}
        60% {{ transform: translateX(-50%) scale(1.12); }}
        100% {{ transform: translateX(-50%) scale(1); }}
    }}

    .face {{
        font-size: 35px;
        margin-top: 12px;
    }}

    .word {{
        font-size: 25px;
        font-weight: 900;
        margin-top: 4px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.25);
    }}

    /* 맞았을 때 두더지 폭발 */
    .mole.explode {{
        animation: explodeMole 0.6s ease-out forwards;
    }}

    @keyframes explodeMole {{
        0% {{
            transform: translateX(-50%) scale(1);
            opacity: 1;
            filter: brightness(1);
        }}
        35% {{
            transform: translateX(-50%) scale(1.35) rotate(8deg);
            opacity: 1;
            filter: brightness(1.8);
        }}
        100% {{
            transform: translateX(-50%) scale(0.05) rotate(-20deg);
            opacity: 0;
            bottom: 80px;
            filter: brightness(2.2);
        }}
    }}

    .boom {{
        position: absolute;
        left: 50%;
        bottom: 88px;
        transform: translateX(-50%);
        font-size: 58px;
        font-weight: 900;
        color: #ef4444;
        opacity: 0;
        z-index: 4;
        pointer-events: none;
        text-shadow: 0 3px 8px rgba(0,0,0,0.25);
    }}

    .boom.show {{
        animation: boomText 0.75s ease-out forwards;
    }}

    @keyframes boomText {{
        0% {{
            opacity: 0;
            transform: translateX(-50%) scale(0.4) rotate(-10deg);
        }}
        35% {{
            opacity: 1;
            transform: translateX(-50%) scale(1.3) rotate(8deg);
        }}
        100% {{
            opacity: 0;
            transform: translateX(-50%) scale(1.8) rotate(-5deg);
        }}
    }}

    .particle {{
        position: absolute;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        left: 50%;
        bottom: 105px;
        opacity: 0;
        z-index: 3;
        pointer-events: none;
    }}

    .particle.red {{ background: #ef4444; }}
    .particle.yellow {{ background: #facc15; }}
    .particle.orange {{ background: #fb923c; }}
    .particle.pink {{ background: #ec4899; }}
    .particle.blue {{ background: #38bdf8; }}

    .particle.p1.show {{ animation: particle1 0.75s ease-out forwards; }}
    .particle.p2.show {{ animation: particle2 0.75s ease-out forwards; }}
    .particle.p3.show {{ animation: particle3 0.75s ease-out forwards; }}
    .particle.p4.show {{ animation: particle4 0.75s ease-out forwards; }}
    .particle.p5.show {{ animation: particle5 0.75s ease-out forwards; }}
    .particle.p6.show {{ animation: particle6 0.75s ease-out forwards; }}

    @keyframes particle1 {{
        0% {{ opacity: 1; transform: translate(0,0) scale(1); }}
        100% {{ opacity: 0; transform: translate(-95px,-80px) scale(0.4); }}
    }}
    @keyframes particle2 {{
        0% {{ opacity: 1; transform: translate(0,0) scale(1); }}
        100% {{ opacity: 0; transform: translate(95px,-85px) scale(0.4); }}
    }}
    @keyframes particle3 {{
        0% {{ opacity: 1; transform: translate(0,0) scale(1); }}
        100% {{ opacity: 0; transform: translate(-70px,30px) scale(0.4); }}
    }}
    @keyframes particle4 {{
        0% {{ opacity: 1; transform: translate(0,0) scale(1); }}
        100% {{ opacity: 0; transform: translate(75px,35px) scale(0.4); }}
    }}
    @keyframes particle5 {{
        0% {{ opacity: 1; transform: translate(0,0) scale(1); }}
        100% {{ opacity: 0; transform: translate(0,-110px) scale(0.4); }}
    }}
    @keyframes particle6 {{
        0% {{ opacity: 1; transform: translate(0,0) scale(1); }}
        100% {{ opacity: 0; transform: translate(0,70px) scale(0.4); }}
    }}

    .heard-box {{
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #bfdbfe;
        border-radius: 22px;
        padding: 18px;
        margin-top: 22px;
        text-align: center;
    }}

    .heard-title {{
        font-size: 16px;
        font-weight: 900;
        color: #1d4ed8;
        margin-bottom: 8px;
    }}

    .heard-text {{
        font-size: 26px;
        font-weight: 900;
        color: #111827;
    }}

    .message {{
        margin-top: 18px;
        padding: 16px;
        border-radius: 18px;
        font-size: 22px;
        font-weight: 900;
        text-align: center;
    }}

    .good {{
        background: #dcfce7;
        color: #166534;
    }}

    .bad {{
        background: #fee2e2;
        color: #991b1b;
    }}

    .tip {{
        margin-top: 20px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 18px;
        color: #475569;
        line-height: 1.7;
        font-size: 15px;
    }}

    @media (max-width: 800px) {{
        .board {{
            grid-template-columns: repeat(2, 1fr);
        }}
        .status-box {{
            grid-template-columns: 1fr;
        }}
    }}
</style>
</head>

<body>
<div class="game-wrap">

    <div class="control-box">
        <div class="title">💥 발음하면 두더지가 터져요!</div>
        <div class="desc">
            마이크 시작을 누른 뒤, 화면에 나온 단어를 영어로 말하세요.<br>
            발음이 맞게 인식되면 단어 두더지가 <b>펑!</b> 하고 터집니다.
        </div>
        <button class="btn" onclick="startGame()">🎙️ 마이크 시작 / 게임 시작</button>
        <button class="btn btn-stop" onclick="stopGame()">⏹️ 정지</button>
        <button class="btn btn-stop" onclick="resetGame()">🔄 다시 시작</button>
    </div>

    <div class="status-box">
        <div class="status-card">
            <div class="status-label">점수</div>
            <div class="status-value" id="score">0</div>
        </div>
        <div class="status-card">
            <div class="status-label">현재 단어</div>
            <div class="status-value" id="targetWord">-</div>
        </div>
        <div class="status-card">
            <div class="status-label">마이크 상태</div>
            <div class="status-value" id="micStatus">대기</div>
        </div>
    </div>

    <div class="board">
        <div class="hole">
            <div class="mole" id="mole0"><div class="face">🐹</div><div class="word"></div></div>
            <div class="boom" id="boom0">💥</div>
            <div class="particle p1 red" id="p0_1"></div><div class="particle p2 yellow" id="p0_2"></div><div class="particle p3 orange" id="p0_3"></div><div class="particle p4 pink" id="p0_4"></div><div class="particle p5 blue" id="p0_5"></div><div class="particle p6 red" id="p0_6"></div>
            <div class="ground-hole"></div>
        </div>

        <div class="hole">
            <div class="mole" id="mole1"><div class="face">🐹</div><div class="word"></div></div>
            <div class="boom" id="boom1">💥</div>
            <div class="particle p1 red" id="p1_1"></div><div class="particle p2 yellow" id="p1_2"></div><div class="particle p3 orange" id="p1_3"></div><div class="particle p4 pink" id="p1_4"></div><div class="particle p5 blue" id="p1_5"></div><div class="particle p6 red" id="p1_6"></div>
            <div class="ground-hole"></div>
        </div>

        <div class="hole">
            <div class="mole" id="mole2"><div class="face">🐹</div><div class="word"></div></div>
            <div class="boom" id="boom2">💥</div>
            <div class="particle p1 red" id="p2_1"></div><div class="particle p2 yellow" id="p2_2"></div><div class="particle p3 orange" id="p2_3"></div><div class="particle p4 pink" id="p2_4"></div><div class="particle p5 blue" id="p2_5"></div><div class="particle p6 red" id="p2_6"></div>
            <div class="ground-hole"></div>
        </div>

        <div class="hole">
            <div class="mole" id="mole3"><div class="face">🐹</div><div class="word"></div></div>
            <div class="boom" id="boom3">💥</div>
            <div class="particle p1 red" id="p3_1"></div><div class="particle p2 yellow" id="p3_2"></div><div class="particle p3 orange" id="p3_3"></div><div class="particle p4 pink" id="p3_4"></div><div class="particle p5 blue" id="p3_5"></div><div class="particle p6 red" id="p3_6"></div>
            <div class="ground-hole"></div>
        </div>

        <div class="hole">
            <div class="mole" id="mole4"><div class="face">🐹</div><div class="word"></div></div>
            <div class="boom" id="boom4">💥</div>
            <div class="particle p1 red" id="p4_1"></div><div class="particle p2 yellow" id="p4_2"></div><div class="particle p3 orange" id="p4_3"></div><div class="particle p4 pink" id="p4_4"></div><div class="particle p5 blue" id="p4_5"></div><div class="particle p6 red" id="p4_6"></div>
            <div class="ground-hole"></div>
        </div>

        <div class="hole">
            <div class="mole" id="mole5"><div class="face">🐹</div><div class="word"></div></div>
            <div class="boom" id="boom5">💥</div>
            <div class="particle p1 red" id="p5_1"></div><div class="particle p2 yellow" id="p5_2"></div><div class="particle p3 orange" id="p5_3"></div><div class="particle p4 pink" id="p5_4"></div><div class="particle p5 blue" id="p5_5"></div><div class="particle p6 red" id="p5_6"></div>
            <div class="ground-hole"></div>
        </div>
    </div>

    <div class="heard-box">
        <div class="heard-title">🎧 인식된 발음</div>
        <div class="heard-text" id="heardText">아직 인식된 말이 없습니다.</div>
    </div>

    <div id="message"></div>

    <div class="tip">
        💡 <b>사용 팁</b><br>
        • Chrome 브라우저에서 가장 잘 작동합니다.<br>
        • 처음 실행할 때 마이크 허용을 눌러야 합니다.<br>
        • 학생이 단어를 말하면, 인식된 발음이 목표 단어와 같을 때 두더지가 터집니다.<br>
        • 조용한 환경에서 또박또박 말하면 인식률이 좋아집니다.
    </div>

</div>

<script>
const WORDS = {words_js_array};

let score = 0;
let currentTarget = "";
let currentMoleIndex = -1;
let gameTimer = null;
let recognition = null;
let isRunning = false;
let isExploding = false;

const moleCount = 6;

function randomChoice(arr) {{
    return arr[Math.floor(Math.random() * arr.length)];
}}

function clearEffects() {{
    for (let i = 0; i < moleCount; i++) {{
        const boom = document.getElementById("boom" + i);
        boom.classList.remove("show");

        for (let j = 1; j <= 6; j++) {{
            const p = document.getElementById("p" + i + "_" + j);
            p.classList.remove("show");
        }}
    }}
}}

function clearMoles() {{
    for (let i = 0; i < moleCount; i++) {{
        const mole = document.getElementById("mole" + i);
        mole.classList.remove("show");
        mole.classList.remove("explode");
        mole.querySelector(".word").innerText = "";
    }}
    clearEffects();
}}

function popMole() {{
    if (isExploding) return;

    clearMoles();

    currentTarget = randomChoice(WORDS);
    currentMoleIndex = Math.floor(Math.random() * moleCount);

    const mole = document.getElementById("mole" + currentMoleIndex);
    mole.querySelector(".word").innerText = currentTarget;
    mole.classList.add("show");

    document.getElementById("targetWord").innerText = currentTarget;
    showMessage("🎯 '" + currentTarget + "' 를 발음해 보세요!", "good");
}}

function normalizeText(text) {{
    return text
        .toLowerCase()
        .replace(/[^a-z ]/g, "")
        .trim();
}}

function checkAnswer(spokenText) {{
    const heard = normalizeText(spokenText);
    const target = normalizeText(currentTarget);

    document.getElementById("heardText").innerText = spokenText;

    if (!target || isExploding) return;

    const heardWords = heard.split(" ");

    if (heard === target || heardWords.includes(target)) {{
        explodeMole();
    }} else {{
        showMessage("😅 '" + spokenText + "'로 들렸어요. 다시 말해 보세요!", "bad");
    }}
}}

function explodeMole() {{
    isExploding = true;

    const mole = document.getElementById("mole" + currentMoleIndex);
    const boom = document.getElementById("boom" + currentMoleIndex);

    mole.classList.remove("show");
    mole.classList.add("explode");

    boom.classList.remove("show");
    void boom.offsetWidth;
    boom.classList.add("show");

    for (let j = 1; j <= 6; j++) {{
        const p = document.getElementById("p" + currentMoleIndex + "_" + j);
        p.classList.remove("show");
        void p.offsetWidth;
        p.classList.add("show");
    }}

    score += 1;
    document.getElementById("score").innerText = score;

    showMessage("💥 정답! '" + currentTarget + "' 두더지가 터졌어요!", "good");

    setTimeout(() => {{
        mole.classList.remove("explode");
        mole.querySelector(".word").innerText = "";
        isExploding = false;

        if (isRunning) {{
            popMole();
        }}
    }}, 900);
}}

function showMessage(text, type) {{
    const message = document.getElementById("message");
    message.innerHTML = '<div class="message ' + type + '">' + text + '</div>';
}}

function startGame() {{
    if (isRunning) return;

    isRunning = true;
    document.getElementById("micStatus").innerText = "듣는 중";

    popMole();
    startRecognition();

    gameTimer = setInterval(() => {{
        if (isRunning && !isExploding) {{
            popMole();
        }}
    }}, 6500);
}}

function stopGame() {{
    isRunning = false;
    document.getElementById("micStatus").innerText = "정지";
    clearInterval(gameTimer);

    if (recognition) {{
        recognition.stop();
    }}
}}

function resetGame() {{
    stopGame();
    score = 0;
    currentTarget = "";
    currentMoleIndex = -1;
    isExploding = false;

    document.getElementById("score").innerText = "0";
    document.getElementById("targetWord").innerText = "-";
    document.getElementById("heardText").innerText = "아직 인식된 말이 없습니다.";
    document.getElementById("message").innerHTML = "";
    clearMoles();
}}

function startRecognition() {{
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {{
        document.getElementById("micStatus").innerText = "지원 안 됨";
        showMessage("이 브라우저는 음성 인식을 지원하지 않습니다. Chrome을 사용해 주세요.", "bad");
        return;
    }}

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onstart = function() {{
        document.getElementById("micStatus").innerText = "듣는 중";
    }};

    recognition.onresult = function(event) {{
        const last = event.results.length - 1;
        const spokenText = event.results[last][0].transcript;
        checkAnswer(spokenText);
    }};

    recognition.onerror = function(event) {{
        document.getElementById("micStatus").innerText = "오류";
        showMessage("마이크 오류가 났습니다: " + event.error, "bad");
    }};

    recognition.onend = function() {{
        if (isRunning) {{
            try {{
                recognition.start();
            }} catch (e) {{}}
        }}
    }};

    try {{
        recognition.start();
    }} catch (e) {{}}
}}
</script>
</body>
</html>
"""

components.html(html_code, height=980, scrolling=True)
