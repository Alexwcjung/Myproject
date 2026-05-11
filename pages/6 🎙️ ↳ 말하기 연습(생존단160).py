import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="생존 문장 말하기 훈련",
    page_icon="🎙️",
    layout="wide"
)

# =========================================================
# 데이터
# =========================================================
PRACTICE_ITEMS = [{'cat': '🙋 내 상태 말하기', 'ko': '나는 배고파.', 'blank': 'I am ______.', 'answer': 'I am hungry.', 'hint': 'hungry', 'emoji': '🍽️'}, {'cat': '🙋 내 상태 말하기', 'ko': '나는 목말라.', 'blank': 'I am ______.', 'answer': 'I am thirsty.', 'hint': 'thirsty', 'emoji': '💧'}, {'cat': '🙋 내 상태 말하기', 'ko': '나는 피곤해.', 'blank': 'I am ______.', 'answer': 'I am tired.', 'hint': 'tired', 'emoji': '😴'}, {'cat': '🙋 내 상태 말하기', 'ko': '나는 아파.', 'blank': 'I am ______.', 'answer': 'I am sick.', 'hint': 'sick', 'emoji': '🤒'}, {'cat': '🙋 내 상태 말하기', 'ko': '나는 괜찮아.', 'blank': 'I am ______.', 'answer': 'I am okay.', 'hint': 'okay', 'emoji': '🙂'}, {'cat': '🙋 내 상태 말하기', 'ko': '나는 추워.', 'blank': 'I am ______.', 'answer': 'I am cold.', 'hint': 'cold', 'emoji': '🥶'}, {'cat': '🙋 내 상태 말하기', 'ko': '나는 걱정돼.', 'blank': 'I am ______.', 'answer': 'I am worried.', 'hint': 'worried', 'emoji': '😟'}, {'cat': '🙋 내 상태 말하기', 'ko': '나는 무서워.', 'blank': 'I am ______.', 'answer': 'I am scared.', 'hint': 'scared', 'emoji': '😨'}, {'cat': '🆘 필요한 것 말하기', 'ko': '나는 물이 필요해.', 'blank': 'I need ______.', 'answer': 'I need water.', 'hint': 'water', 'emoji': '💧'}, {'cat': '🆘 필요한 것 말하기', 'ko': '나는 음식이 필요해.', 'blank': 'I need ______.', 'answer': 'I need food.', 'hint': 'food', 'emoji': '🍽️'}, {'cat': '🆘 필요한 것 말하기', 'ko': '나는 도움이 필요해.', 'blank': 'I need ______.', 'answer': 'I need help.', 'hint': 'help', 'emoji': '🆘'}, {'cat': '🆘 필요한 것 말하기', 'ko': '나는 약이 필요해.', 'blank': 'I need ______.', 'answer': 'I need medicine.', 'hint': 'medicine', 'emoji': '💊'}, {'cat': '🆘 필요한 것 말하기', 'ko': '나는 병원이 필요해.', 'blank': 'I need a ______.', 'answer': 'I need a hospital.', 'hint': 'hospital', 'emoji': '🏥'}, {'cat': '🆘 필요한 것 말하기', 'ko': '나는 택시가 필요해.', 'blank': 'I need a ______.', 'answer': 'I need a taxi.', 'hint': 'taxi', 'emoji': '🚕'}, {'cat': '🆘 필요한 것 말하기', 'ko': '나는 표가 필요해.', 'blank': 'I need a ______.', 'answer': 'I need a ticket.', 'hint': 'ticket', 'emoji': '🎫'}, {'cat': '🆘 필요한 것 말하기', 'ko': '나는 열쇠가 필요해.', 'blank': 'I need a ______.', 'answer': 'I need a key.', 'hint': 'key', 'emoji': '🔑'}, {'cat': '💭 원하는 것 말하기', 'ko': '나는 음식을 원해.', 'blank': 'I want ______.', 'answer': 'I want food.', 'hint': 'food', 'emoji': '🍽️'}, {'cat': '💭 원하는 것 말하기', 'ko': '나는 물을 원해.', 'blank': 'I want ______.', 'answer': 'I want water.', 'hint': 'water', 'emoji': '💧'}, {'cat': '💭 원하는 것 말하기', 'ko': '나는 밥을 원해.', 'blank': 'I want ______.', 'answer': 'I want rice.', 'hint': 'rice', 'emoji': '🍚'}, {'cat': '💭 원하는 것 말하기', 'ko': '나는 빵을 원해.', 'blank': 'I want ______.', 'answer': 'I want bread.', 'hint': 'bread', 'emoji': '🍞'}, {'cat': '💭 원하는 것 말하기', 'ko': '나는 우유를 원해.', 'blank': 'I want ______.', 'answer': 'I want milk.', 'hint': 'milk', 'emoji': '🥛'}, {'cat': '💭 원하는 것 말하기', 'ko': '나는 주스를 원해.', 'blank': 'I want ______.', 'answer': 'I want juice.', 'hint': 'juice', 'emoji': '🧃'}, {'cat': '💭 원하는 것 말하기', 'ko': '나는 커피를 원해.', 'blank': 'I want ______.', 'answer': 'I want coffee.', 'hint': 'coffee', 'emoji': '☕'}, {'cat': '💭 원하는 것 말하기', 'ko': '나는 간식을 원해.', 'blank': 'I want a ______.', 'answer': 'I want a snack.', 'hint': 'snack', 'emoji': '🍪'}, {'cat': '🏃 지금 하는 일 말하기', 'ko': '나는 먹고 있어.', 'blank': 'I am ______.', 'answer': 'I am eating.', 'hint': 'eating', 'emoji': '🍽️'}, {'cat': '🏃 지금 하는 일 말하기', 'ko': '나는 마시고 있어.', 'blank': 'I am ______.', 'answer': 'I am drinking.', 'hint': 'drinking', 'emoji': '🥤'}, {'cat': '🏃 지금 하는 일 말하기', 'ko': '나는 기다리고 있어.', 'blank': 'I am ______.', 'answer': 'I am waiting.', 'hint': 'waiting', 'emoji': '⏳'}, {'cat': '🏃 지금 하는 일 말하기', 'ko': '나는 공부하고 있어.', 'blank': 'I am ______.', 'answer': 'I am studying.', 'hint': 'studying', 'emoji': '📚'}, {'cat': '🏃 지금 하는 일 말하기', 'ko': '나는 읽고 있어.', 'blank': 'I am ______.', 'answer': 'I am reading.', 'hint': 'reading', 'emoji': '📖'}, {'cat': '🏃 지금 하는 일 말하기', 'ko': '나는 쓰고 있어.', 'blank': 'I am ______.', 'answer': 'I am writing.', 'hint': 'writing', 'emoji': '✏️'}, {'cat': '🏃 지금 하는 일 말하기', 'ko': '나는 걷고 있어.', 'blank': 'I am ______.', 'answer': 'I am walking.', 'hint': 'walking', 'emoji': '🚶'}, {'cat': '🏃 지금 하는 일 말하기', 'ko': '나는 듣고 있어.', 'blank': 'I am ______.', 'answer': 'I am listening.', 'hint': 'listening', 'emoji': '👂'}, {'cat': '🚀 앞으로 할 일 말하기', 'ko': '나는 집에 갈 거야.', 'blank': 'I will ______ home.', 'answer': 'I will go home.', 'hint': 'go', 'emoji': '🏠'}, {'cat': '🚀 앞으로 할 일 말하기', 'ko': '나는 기다릴 거야.', 'blank': 'I will ______.', 'answer': 'I will wait.', 'hint': 'wait', 'emoji': '⏳'}, {'cat': '🚀 앞으로 할 일 말하기', 'ko': '나는 너를 도와줄 거야.', 'blank': 'I will ______ you.', 'answer': 'I will help you.', 'hint': 'help', 'emoji': '🤝'}, {'cat': '🚀 앞으로 할 일 말하기', 'ko': '나는 영어를 공부할 거야.', 'blank': 'I will ______ English.', 'answer': 'I will study English.', 'hint': 'study', 'emoji': '📚'}, {'cat': '🚀 앞으로 할 일 말하기', 'ko': '나는 점심을 먹을 거야.', 'blank': 'I will ______ lunch.', 'answer': 'I will eat lunch.', 'hint': 'eat', 'emoji': '🍱'}, {'cat': '🚀 앞으로 할 일 말하기', 'ko': '나는 물을 마실 거야.', 'blank': 'I will ______ water.', 'answer': 'I will drink water.', 'hint': 'drink', 'emoji': '💧'}, {'cat': '❌ 아니라고 말하기', 'ko': '나는 아프지 않아.', 'blank': 'I am not ______.', 'answer': 'I am not sick.', 'hint': 'sick', 'emoji': '🙂'}, {'cat': '❌ 아니라고 말하기', 'ko': '나는 배고프지 않아.', 'blank': 'I am not ______.', 'answer': 'I am not hungry.', 'hint': 'hungry', 'emoji': '🙅🍽️'}, {'cat': '❌ 아니라고 말하기', 'ko': '나는 괜찮지 않아.', 'blank': 'I am not ______.', 'answer': 'I am not okay.', 'hint': 'okay', 'emoji': '😟'}, {'cat': '❌ 아니라고 말하기', 'ko': '나는 몰라.', 'blank': 'I do not ______.', 'answer': 'I do not know.', 'hint': 'know', 'emoji': '🤷'}, {'cat': '❌ 아니라고 말하기', 'ko': '나는 이해하지 못해.', 'blank': 'I do not ______.', 'answer': 'I do not understand.', 'hint': 'understand', 'emoji': '❓'}, {'cat': '❌ 아니라고 말하기', 'ko': '나는 그것을 원하지 않아.', 'blank': 'I do not ______ it.', 'answer': 'I do not want it.', 'hint': 'want', 'emoji': '🙅'}, {'cat': '❓ 간단히 물어보기', 'ko': '괜찮니?', 'blank': 'Are you ______?', 'answer': 'Are you okay?', 'hint': 'okay', 'emoji': '🙂'}, {'cat': '❓ 간단히 물어보기', 'ko': '아프니?', 'blank': 'Are you ______?', 'answer': 'Are you sick?', 'hint': 'sick', 'emoji': '🤒'}, {'cat': '❓ 간단히 물어보기', 'ko': '배고프니?', 'blank': 'Are you ______?', 'answer': 'Are you hungry?', 'hint': 'hungry', 'emoji': '🍽️'}, {'cat': '❓ 간단히 물어보기', 'ko': '목마르니?', 'blank': 'Are you ______?', 'answer': 'Are you thirsty?', 'hint': 'thirsty', 'emoji': '💧'}, {'cat': '❓ 간단히 물어보기', 'ko': '도움이 필요하니?', 'blank': 'Do you need ______?', 'answer': 'Do you need help?', 'hint': 'help', 'emoji': '🆘'}, {'cat': '❓ 간단히 물어보기', 'ko': '물이 필요하니?', 'blank': 'Do you need ______?', 'answer': 'Do you need water?', 'hint': 'water', 'emoji': '💧'}, {'cat': '🕵️ 필요한 정보 묻기', 'ko': '화장실은 어디에 있나요?', 'blank': 'Where is the ______?', 'answer': 'Where is the bathroom?', 'hint': 'bathroom', 'emoji': '🚻'}, {'cat': '🕵️ 필요한 정보 묻기', 'ko': '병원은 어디에 있나요?', 'blank': 'Where is the ______?', 'answer': 'Where is the hospital?', 'hint': 'hospital', 'emoji': '🏥'}, {'cat': '🕵️ 필요한 정보 묻기', 'ko': '가게는 어디에 있나요?', 'blank': 'Where is the ______?', 'answer': 'Where is the store?', 'hint': 'store', 'emoji': '🏪'}, {'cat': '🕵️ 필요한 정보 묻기', 'ko': '역은 어디에 있나요?', 'blank': 'Where is the ______?', 'answer': 'Where is the station?', 'hint': 'station', 'emoji': '🚉'}, {'cat': '🕵️ 필요한 정보 묻기', 'ko': '지금 몇 시인가요?', 'blank': 'What ______ is it?', 'answer': 'What time is it?', 'hint': 'time', 'emoji': '⏰'}, {'cat': '🕵️ 필요한 정보 묻기', 'ko': '이름이 무엇인가요?', 'blank': 'What is your ______?', 'answer': 'What is your name?', 'hint': 'name', 'emoji': '🏷️'}]


# =========================================================
# 디자인
# =========================================================
st.markdown(
    """
    <style>
    

    

    

    
    
    @media (max-width: 640px) {
        #speaking-app {
            padding: 10px !important;
            border-radius: 20px !important;
        }
        #speaking-app #blankSentence {
            font-size: 20px !important;
            padding: 13px 12px !important;
            margin-bottom: 8px !important;
            line-height: 1.35 !important;
        }
        #speaking-app #koPrompt {
            font-size: 19px !important;
            margin-bottom: 8px !important;
            line-height: 1.35 !important;
        }
        #speaking-app #transcriptBox {
            font-size: 17px !important;
            line-height: 1.45 !important;
        }
        #speaking-app #micBtn {
            width: 78px !important;
            height: 78px !important;
            font-size: 27px !important;
        }
        #speaking-app #hintBtn,
        #speaking-app #answerBtn,
        #speaking-app #listenBtn,
        #speaking-app #nextBtn {
            padding: 8px 12px !important;
            font-size: 13px !important;
        }
        #speaking-app #hintBox {
            font-size: 13px !important;
            padding: 6px 8px !important;
            line-height: 1.2 !important;
            max-width: 100% !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
            white-space: normal !important;
            box-sizing: border-box !important;
        }
    }

</style>
    """,
    unsafe_allow_html=True
)





# =========================================================
# 말하기 훈련 컴포넌트
# =========================================================
def speaking_practice_component(items):
    items_json = json.dumps(items, ensure_ascii=False)

    html = r"""
    <div id="speaking-app" style="
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #eff6ff 0%, #fdf4ff 35%, #fff7ed 68%, #f0fdf4 100%);
        border: 2px solid #c4b5fd;
        border-radius: 34px;
        padding: 24px;
        box-shadow: 0 12px 28px rgba(124,58,237,0.12);
    ">
        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:18px;">
            <label style="font-weight:900; color:#334155;">문장 구조 선택</label>
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
            ">🎲 랜덤</button>

            <button id="resetBtn" style="
                border: 1.5px solid #fed7aa;
                background: #fff7ed;
                color: #9a3412;
                border-radius: 999px;
                padding: 10px 15px;
                font-weight: 900;
                cursor: pointer;
            ">🔄 점수 초기화</button>
        </div>

        <div style="
            background:white;
            border-radius:26px;
            padding:24px;
            border:1.5px solid #e0f2fe;
            box-shadow:0 5px 16px rgba(0,0,0,0.055);
        ">
            <div style="display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <div id="categoryLabel" style="
                    display:inline-block;
                    background:linear-gradient(135deg,#dbeafe,#ede9fe);
                    color:#3730a3;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1.5px solid #c4b5fd;
                "></div>

                <div id="scoreLabel" style="
                    display:inline-block;
                    background:linear-gradient(135deg,#dcfce7,#fef9c3);
                    color:#166534;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1.5px solid #86efac;
                ">0 / 0</div>
            </div>

            <div style="
                font-size: 26px;
                font-weight: 900;
                color: #111827;
                line-height: 1.35;
                margin-bottom: 10px;
            " id="koPrompt">
                한국어 상황
            </div>

            <div style="
                background: linear-gradient(135deg, #ffffff 0%, #eff6ff 45%, #fdf4ff 100%);
                border: 2px solid #c4b5fd;
                border-radius: 24px;
                padding: 18px 16px;
                margin-bottom: 12px;
                font-size: 30px;
                font-weight: 900;
                color: #1f2937;
                line-height: 1.45;
                box-shadow: 0 6px 16px rgba(99,102,241,0.08);
                word-break: break-word;
            " id="blankSentence">
                I am ______.
            </div>

            <div style="
                background:linear-gradient(135deg,#eef2ff,#fdf2f8);
                border:1.5px solid #c4b5fd;
                border-radius:20px;
                padding:14px 16px;
                margin-bottom:12px;
                min-height:52px;
                box-shadow: 0 4px 12px rgba(124,58,237,0.08);
            ">
                <div id="transcriptBox" style="
                    font-size:24px;
                    font-weight:900;
                    color:#4c1d95;
                    line-height:1.6;
                    min-height:32px;
                    word-break: break-word;
                "></div>
            </div>

            <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; justify-content:center; margin-bottom:12px;">
                <button id="hintBtn" style="
                    border:1.5px solid #fcd34d;
                    background:linear-gradient(135deg,#fef3c7,#fde68a);
                    color:#92400e;
                    border-radius:999px;
                    padding:10px 16px;
                    font-weight:900;
                    cursor:pointer;
                    box-shadow:0 4px 10px rgba(245,158,11,0.14);
                ">💡 힌트</button>

                <button id="micBtn" style="
                    border:4px solid rgba(255,255,255,0.95);
                    background: linear-gradient(135deg, #8b5cf6, #ec4899);
                    color:white;
                    border-radius:999px;
                    width:100px;
                    height:100px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:36px;
                    box-shadow:0 12px 26px rgba(124,58,237,0.26);
                    flex: 0 0 auto;
                ">🎙️</button>

                <button id="answerBtn" style="
                    display:none;
                    border:1.5px solid #86efac;
                    background:linear-gradient(135deg,#dcfce7,#f0fdf4);
                    color:#166534;
                    border-radius:999px;
                    padding:10px 16px;
                    font-weight:900;
                    cursor:pointer;
                    box-shadow:0 4px 10px rgba(34,197,94,0.12);
                ">👀 정답</button>

                <button id="listenBtn" style="
                    display:none;
                    border:1.5px solid #93c5fd;
                    background:linear-gradient(135deg,#dbeafe,#eff6ff);
                    color:#1d4ed8;
                    border-radius:999px;
                    padding:10px 16px;
                    font-weight:900;
                    cursor:pointer;
                    box-shadow:0 4px 10px rgba(59,130,246,0.12);
                ">🔊 듣기</button>

                <button id="nextBtn" style="
                    display:none;
                    border:1.5px solid #c4b5fd;
                    background:linear-gradient(135deg,#ede9fe,#eef2ff);
                    color:#5b21b6;
                    border-radius:999px;
                    padding:10px 16px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:16px;
                    box-shadow:0 4px 10px rgba(124,58,237,0.12);
                ">➡️ 다음</button>
            </div>

            <div id="hintBox" style="
                display:none;
                background:linear-gradient(135deg,#fff7ed,#fffbeb);
                border:1.5px solid #fbbf24;
                color:#92400e;
                border-radius:14px;
                padding:7px 10px;
                margin-top:6px;
                margin-bottom:6px;
                font-size:16px;
                font-weight:900;
                line-height:1.25;
                word-break:break-word;
                overflow-wrap:anywhere;
                white-space:normal;
                max-width:100%;
                box-sizing:border-box;
                box-shadow: 0 3px 8px rgba(251,191,36,0.10);
            "></div>

            <div id="answerBox" style="display:none;"></div>

            <div id="resultBox" style="
                display:none;
                margin-top:8px;
                font-size:15px;
                font-weight:800;
                color:#64748b;
            "></div>
        </div>

        <div style="
            margin-top:14px;
            color:#64748b;
            font-size:13px;
            line-height:1.6;
            font-weight:700;
        ">
            ※ Chrome 계열 브라우저에서 음성 인식이 가장 잘 작동합니다.<br>
            ※ 마이크 권한 요청이 나오면 허용을 눌러 주세요.
        </div>
    </div>

    <script>
    const ITEMS = __ITEMS_JSON__;

    let currentList = [];
    let currentIndex = 0;
    let currentItem = null;
    let score = 0;
    let attempts = 0;
    let alreadyCorrect = false;

    const categorySelect = document.getElementById("categorySelect");
    const randomBtn = document.getElementById("randomBtn");
    const resetBtn = document.getElementById("resetBtn");
    const categoryLabel = document.getElementById("categoryLabel");
    const scoreLabel = document.getElementById("scoreLabel");
    const koPrompt = document.getElementById("koPrompt");
    const blankSentence = document.getElementById("blankSentence");
    const hintBox = document.getElementById("hintBox");
    const answerBox = document.getElementById("answerBox");
    const hintBtn = document.getElementById("hintBtn");
    const listenBtn = document.getElementById("listenBtn");
    const answerBtn = document.getElementById("answerBtn");
    const micBtn = document.getElementById("micBtn");
    const nextBtn = document.getElementById("nextBtn");
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

    function shuffleArray(arr) {
        const copied = arr.slice();
        for (let i = copied.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copied[i], copied[j]] = [copied[j], copied[i]];
        }
        return copied;
    }

    function makeTwoLetterHint(answerWord) {
        if (!answerWord) return "";

        return answerWord.split(" ").map(word => {
            const clean = word.trim();
            if (clean.length <= 2) return clean;
            return clean.slice(0, 2) + "_".repeat(clean.length - 2);
        }).join(" ");
    }

    function normalizeText(text) {
        return text
            .toLowerCase()
            // 축약형을 먼저 풀어 줌
            .replace(/\bi'm\b/g, "i am")
            .replace(/\bim\b/g, "i am")
            .replace(/\byou're\b/g, "you are")
            .replace(/\bhe's\b/g, "he is")
            .replace(/\bshe's\b/g, "she is")
            .replace(/\bit's\b/g, "it is")
            .replace(/\bwe're\b/g, "we are")
            .replace(/\bthey're\b/g, "they are")
            .replace(/\bdon't\b/g, "do not")
            .replace(/\bdoesn't\b/g, "does not")
            .replace(/\bdidn't\b/g, "did not")
            .replace(/\bcan't\b/g, "cannot")
            .replace(/\bcant\b/g, "cannot")
            .replace(/\bi'll\b/g, "i will")
            .replace(/\byou'll\b/g, "you will")
            .replace(/\bhe'll\b/g, "he will")
            .replace(/\bshe'll\b/g, "she will")
            .replace(/[.,!?;:'"’‘“”]/g, "")
            .replace(/\s+/g, " ")
            .trim();
    }

    function wordsOnly(text) {
        return normalizeText(text)
            .split(" ")
            .filter(w => w.length > 0);
    }

    function editDistance(a, b) {
        const dp = Array.from({ length: a.length + 1 }, () => Array(b.length + 1).fill(0));

        for (let i = 0; i <= a.length; i++) dp[i][0] = i;
        for (let j = 0; j <= b.length; j++) dp[0][j] = j;

        for (let i = 1; i <= a.length; i++) {
            for (let j = 1; j <= b.length; j++) {
                const cost = a[i - 1] === b[j - 1] ? 0 : 1;
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
        if (!a || !b) return 0;
        if (a === b) return 1;

        const dist = editDistance(a, b);
        const maxLen = Math.max(a.length, b.length);

        return 1 - (dist / maxLen);
    }

    function isSmallRecognitionMistake(spokenWord, answerWord) {
        if (!spokenWord || !answerWord) return false;
        if (spokenWord === answerWord) return true;

        const dist = editDistance(spokenWord, answerWord);
        const maxLen = Math.max(spokenWord.length, answerWord.length);
        const sim = wordSimilarity(spokenWord, answerWord);

        // 아주 짧은 단어는 엄격하게 채점
        // 예: I, a, am, go, do, is, it 등
        if (answerWord.length <= 2) {
            return dist === 0;
        }

        // 3~4글자 단어는 1글자 정도만 허용
        // 예: sick → sik, cold → col 정도는 허용
        // 하지만 완전히 다른 단어는 오답
        if (answerWord.length <= 4) {
            return dist <= 1 && sim >= 0.75;
        }

        // 5글자 이상 단어는 음성 인식 오류를 조금 더 허용
        // 예: hungry → hungri, thirsty → thursty 정도 허용
        if (answerWord.length >= 5) {
            return dist <= 1 || sim >= 0.82;
        }

        return false;
    }

    function isCloseEnough(spoken, answer) {
        const s = normalizeText(spoken);
        const a = normalizeText(answer);

        if (!s || !a) return false;

        // 완전히 같으면 바로 정답
        if (s === a) return true;

        const spokenWords = wordsOnly(s);
        const answerWords = wordsOnly(a);

        // 단어 개수가 다르면 오답
        // 예: "hungry"만 말함 → 오답
        // 예: "I hungry" → 오답
        if (spokenWords.length !== answerWords.length) {
            return false;
        }

        let weakMatchCount = 0;

        for (let i = 0; i < answerWords.length; i++) {
            const sw = spokenWords[i];
            const aw = answerWords[i];

            if (sw === aw) {
                continue;
            }

            if (isSmallRecognitionMistake(sw, aw)) {
                weakMatchCount += 1;
                continue;
            }

            // 한 단어라도 완전히 다르면 오답
            // 예: I am tired ≠ I am hungry
            return false;
        }

        // 짧은 문장에서 애매하게 맞은 단어가 너무 많으면 오답
        // 예: 3~4단어 문장에서 2단어 이상이 부정확하면 오답
        if (answerWords.length <= 4 && weakMatchCount >= 2) {
            return false;
        }

        // 긴 문장에서도 절반 가까이 애매하면 오답
        if (answerWords.length >= 5 && weakMatchCount >= Math.ceil(answerWords.length / 2)) {
            return false;
        }

        return true;
    }

    function isCorrectSpeech(spoken, answer) {
        return isCloseEnough(spoken, answer);
    }

    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function highlightTranscript(spoken, answer) {
        const spokenWordsRaw = spoken.trim().split(/\s+/).filter(w => w.length > 0);
        const spokenWordsNorm = wordsOnly(spoken);
        const answerWordsNorm = wordsOnly(answer);

        if (spokenWordsRaw.length === 0) {
            return "아직 말하지 않았습니다.";
        }

        let html = "";

        for (let i = 0; i < spokenWordsRaw.length; i++) {
            const raw = escapeHtml(spokenWordsRaw[i]);
            const norm = spokenWordsNorm[i] || "";
            const target = answerWordsNorm[i] || "";

            let bg = "#fee2e2";
            let color = "#991b1b";
            let border = "#fecaca";

            if (isSmallRecognitionMistake(norm, target)) {
                bg = "#dcfce7";
                color = "#166534";
                border = "#bbf7d0";
            }

            html += "<span style='display:inline-block; margin:3px 4px; padding:5px 9px; border-radius:999px; background:" +
                    bg + "; color:" + color + "; border:1px solid " + border + "; font-weight:900;'>" +
                    raw + "</span>";
        }

        if (spokenWordsNorm.length < answerWordsNorm.length) {
            const missing = answerWordsNorm.slice(spokenWordsNorm.length);
            missing.forEach(w => {
                html += "<span style='display:inline-block; margin:3px 4px; padding:5px 9px; border-radius:999px; background:#f1f5f9; color:#64748b; border:1px dashed #cbd5e1; font-weight:900;'>"
                        + w + "</span>";
            });
        }

        return html;
    }


    function makeBlankSentenceHtml(blankText) {
        const parts = blankText.split(/(______)/g);

        return parts.map(part => {
            if (part === "______") {
                return "<span style='display:inline-block; min-width:120px; height:42px; vertical-align:middle; background:#e0f2fe; border-radius:14px; margin:0 6px; border:1.5px solid #bae6fd;'></span>";
            }

            return escapeHtml(part);
        }).join("");
    }

    function makeSpokenSentenceHtml(spoken, answer) {
        const spokenWordsRaw = spoken.trim().split(/\s+/).filter(w => w.length > 0);
        const spokenWordsNorm = wordsOnly(spoken);
        const answerWordsNorm = wordsOnly(answer);

        if (spokenWordsRaw.length === 0) {
            return makeBlankSentenceHtml(currentItem.blank);
        }

        let html = "";

        for (let i = 0; i < spokenWordsRaw.length; i++) {
            const raw = escapeHtml(spokenWordsRaw[i]);
            const norm = spokenWordsNorm[i] || "";
            const target = answerWordsNorm[i] || "";

            let bg = "#fee2e2";
            let color = "#991b1b";
            let border = "#fecaca";

            if (isSmallRecognitionMistake(norm, target)) {
                bg = "#dcfce7";
                color = "#166534";
                border = "#bbf7d0";
            }

            html += "<span style='display:inline-block; margin:4px 5px; padding:6px 11px; border-radius:999px; background:" +
                    bg + "; color:" + color + "; border:1px solid " + border + "; font-weight:900;'>" +
                    raw + "</span>";
        }

        if (spokenWordsNorm.length < answerWordsNorm.length) {
            const missing = answerWordsNorm.slice(spokenWordsNorm.length);
            missing.forEach(w => {
                html += "<span style='display:inline-block; margin:4px 5px; padding:6px 11px; border-radius:999px; background:#f1f5f9; color:#94a3b8; border:1px dashed #cbd5e1; font-weight:900;'>"
                        + w + "</span>";
            });
        }

        return html;
    }

    function makeAnswerSentenceHtml(answer) {
        return answer.split(/\s+/).map(word => {
            return "<span style='display:inline-block; margin:4px 5px; padding:6px 11px; border-radius:999px; background:#dcfce7; color:#166534; border:1px solid #bbf7d0; font-weight:900;'>" +
                    escapeHtml(word) + "</span>";
        }).join("");
    }


    function updateScore() {
        scoreLabel.innerText = score + " / " + attempts;
    }

    function loadQuestion(index = 0) {
        if (currentList.length === 0) {
            currentList = getFilteredItems();
        }

        if (index >= currentList.length) index = 0;
        if (index < 0) index = currentList.length - 1;

        currentIndex = index;
        currentItem = currentList[currentIndex];
        alreadyCorrect = false;

        categoryLabel.innerText = currentItem.cat + " · " + (currentIndex + 1) + " / " + currentList.length;
        const emoji = currentItem.emoji || "🛟";
        koPrompt.innerHTML =
            "<span style='font-size:42px; margin-right:10px; vertical-align:middle;'>" + emoji + "</span>" +
            "<span style='vertical-align:middle;'>" + currentItem.ko + "</span>";
        blankSentence.innerText = currentItem.blank;
        hintBox.style.display = "none";
        answerBox.style.display = "none";
        hintBox.innerText = "";
        answerBox.innerText = "";
        transcriptBox.innerText = "";

        // 처음에는 힌트와 말하기 버튼만 보이게 함
        hintBtn.style.display = "inline-block";
        micBtn.style.display = "inline-block";
        answerBtn.style.display = "none";
        listenBtn.style.display = "none";
        nextBtn.style.display = "none";

        resultBox.style.display = "none";
        resultBox.innerText = "";
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

    function checkSpeech(spokenText) {
        attempts += 1;

        if (isCorrectSpeech(spokenText, currentItem.answer)) {
            if (!alreadyCorrect) {
                score += 1;
                alreadyCorrect = true;
            }

            resultBox.style.display = "none";

            answerBox.style.display = "none";
            transcriptBox.innerText = currentItem.answer;

            answerBtn.style.display = "none";
            listenBtn.style.display = "inline-block";
            nextBtn.style.display = "inline-block";

            speak(currentItem.answer);
        } else {
            resultBox.style.display = "none";

            // 틀린 뒤에만 정답 보기 버튼 제공
            answerBtn.style.display = "inline-block";
            nextBtn.style.display = "none";
        }

        updateScore();
    }

    async function startRecognition() {
        if (!SpeechRecognition) {
            transcriptBox.innerText = "Chrome에서 열어 주세요.";
            return;
        }

        // 모바일에서 먼저 마이크 권한 요청
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                stream.getTracks().forEach(track => track.stop());
            } catch (err) {
                transcriptBox.innerText = "마이크 허용 후 다시 눌러 주세요.";
                return;
            }
        }

        window.speechSynthesis.cancel();

        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = true;
        recognition.continuous = false;
        recognition.maxAlternatives = 3;

        micBtn.innerText = "👂";
        resultBox.style.display = "none";
        resultBox.innerText = "";
        transcriptBox.innerText = "";

        recognition.onresult = function(event) {
            let spokenText = "";
            let hasFinal = false;

            for (let i = 0; i < event.results.length; i++) {
                const piece = event.results[i][0].transcript.trim();
                if (piece) {
                    spokenText += (spokenText ? " " : "") + piece;
                }
                if (event.results[i].isFinal) {
                    hasFinal = true;
                }
            }

            transcriptBox.innerText = spokenText;

            if (hasFinal) {
                checkSpeech(spokenText);
            }
        };

        recognition.onerror = function(event) {
            if (event.error === "not-allowed" || event.error === "service-not-allowed") {
                transcriptBox.innerText = "마이크 허용 후 다시 눌러 주세요.";
            } else if (event.error === "no-speech") {
                transcriptBox.innerText = "";
            } else {
                transcriptBox.innerText = "다시 눌러 주세요.";
            }
            micBtn.innerText = "🎙️";
        };

        recognition.onend = function() {
            micBtn.innerText = "🎙️";
        };

        try {
            recognition.start();
        } catch (err) {
            transcriptBox.innerText = "다시 눌러 주세요.";
            micBtn.innerText = "🎙️";
        }
    }

    categorySelect.addEventListener("change", function() {
        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
    });

    randomBtn.addEventListener("click", function() {
        currentList = shuffleArray(getFilteredItems());
        loadQuestion(0);
    });

    resetBtn.addEventListener("click", function() {
        score = 0;
        attempts = 0;
        alreadyCorrect = false;
        updateScore();
        resultBox.style.display = "none";
        resultBox.innerText = "";
    });

    hintBtn.addEventListener("click", function() {
        hintBox.style.display = "block";
        hintBox.innerText = makeTwoLetterHint(currentItem.hint);
    });

    listenBtn.addEventListener("click", function() {
        speak(currentItem.answer);
    });

    answerBtn.addEventListener("click", function() {
        answerBox.style.display = "none";
        transcriptBox.innerText = currentItem.answer;
        listenBtn.style.display = "inline-block";
        speak(currentItem.answer);

        resultBox.style.display = "none";
        resultBox.innerText = "";
    });

    micBtn.addEventListener("click", startRecognition);

    nextBtn.addEventListener("click", function() {
        if (!alreadyCorrect) {
            resultBox.style.display = "none";
            resultBox.innerText = "";
            return;
        }

        loadQuestion(currentIndex + 1);
    });

    initCategories();
    currentList = getFilteredItems();
    updateScore();
    loadQuestion(0);
    </script>
    """

    html = html.replace("__ITEMS_JSON__", items_json)
    components.html(html, height=840)


speaking_practice_component(PRACTICE_ITEMS)
