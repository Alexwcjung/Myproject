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
            padding: 13px 8px !important;
            min-height: 58px !important;
            font-size: 17px !important;
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


        #speaking-app #hintBtn:hover,
        #speaking-app #answerBtn:hover,
        #speaking-app #listenBtn:hover,
        #speaking-app #nextBtn:hover {
            border-color: #22c55e !important;
            color: #22c55e !important;
        }

        @media (max-width: 640px) {
            #speaking-app div[style*="grid-template-columns:repeat(4"] {
                grid-template-columns: repeat(1, minmax(0, 1fr)) !important;
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
            <label style="font-weight:900; color:#334155;">문장 범위 선택</label>
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
                ">정답 0개</div>
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

            <div style="display:flex; flex-direction:column; gap:12px; align-items:center; justify-content:center; margin-bottom:12px;">
                <button id="micBtn" style="
                    border:4px solid rgba(255,255,255,0.95);
                    background: linear-gradient(135deg, #8b5cf6, #ec4899);
                    color:white;
                    border-radius:999px;
                    width:108px;
                    height:108px;
                    font-weight:1000;
                    cursor:pointer;
                    font-size:38px;
                    box-shadow:0 12px 26px rgba(124,58,237,0.26);
                    flex: 0 0 auto;
                ">🎙️</button>

                <div style="display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:10px; width:100%; max-width:760px;">
                    <button id="hintBtn" style="
                        border:1.5px solid #bbf7d0;
                        background:white;
                        color:#111827;
                        border-radius:999px;
                        padding:18px 14px;
                        min-height:72px;
                        font-size:22px;
                        font-weight:1000;
                        cursor:pointer;
                        box-shadow:0 6px 16px rgba(34,197,94,0.16);
                    ">💡 힌트</button>

                    <button id="answerBtn" style="
                        display:inline-block;
                        border:1.5px solid #bbf7d0;
                        background:white;
                        color:#111827;
                        border-radius:999px;
                        padding:18px 14px;
                        min-height:72px;
                        font-size:22px;
                        font-weight:1000;
                        cursor:pointer;
                        box-shadow:0 6px 16px rgba(34,197,94,0.16);
                    ">👀🔊 정답 보기·듣기</button>

                    <button id="listenBtn" style="display:none;">🔊 듣기</button>

                    <button id="nextBtn" style="
                        display:inline-block;
                        border:1.5px solid #bbf7d0;
                        background:white;
                        color:#111827;
                        border-radius:999px;
                        padding:18px 14px;
                        min-height:72px;
                        font-size:22px;
                        font-weight:1000;
                        cursor:pointer;
                        box-shadow:0 6px 16px rgba(34,197,94,0.16);
                    ">➡️ 다음</button>
                </div>
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
            ※ 문장은 말해야 합니다. 다만 발음 시험은 아니므로 핵심 단어와 문장 흐름을 관대하게 봅니다.<br>
            ※ 마이크 권한 요청이 나오면 허용을 눌러 주세요.
        </div>
    </div>

    <script>
    const ITEMS = __ITEMS_JSON__;

    let currentList = [];
    let currentIndex = 0;
    let currentItem = null;
    let score = 0;
    let alreadyCorrect = false;
    let isListening = false;
    let recognitionTimeout = null;

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
        const ranges = [];
        const chunkSize = 50;

        for (let start = 0; start < ITEMS.length; start += chunkSize) {
            const end = Math.min(start + chunkSize, ITEMS.length);
            ranges.push((start + 1) + "~" + end);
        }

        return ranges;
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
        const chunkSize = 50;

        if (!selected || selected.indexOf("~") === -1) {
            return ITEMS.slice(0, chunkSize);
        }

        const parts = selected.split("~");
        const start = parseInt(parts[0], 10) - 1;
        const end = parseInt(parts[1], 10);

        return ITEMS.slice(start, end);
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
            .replace(/\bok\b/g, "okay")
            .replace(/\bo k\b/g, "okay")
            .replace(/\bwanna\b/g, "want")
            .replace(/\bgonna\b/g, "going to")
            .replace(/\bgotta\b/g, "have to")
            .replace(/[.,!?;:'"’‘“”]/g, "")
            .replace(/-/g, " ")
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

    function hasSharedBigram(a, b) {
        a = String(a || "");
        b = String(b || "");
        if (a.length < 2 || b.length < 2) return false;

        for (let i = 0; i < a.length - 1; i++) {
            if (b.includes(a.slice(i, i + 2))) return true;
        }

        return false;
    }

    function aliasMatch(spokenWord, answerWord) {
        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        const aliases = {
            "i": ["i", "eye", "hi", "ai", "a"],
            "am": ["am", "im", "i'm", "em"],
            "you": ["you", "u", "yew", "yo", "ya", "your"],
            "are": ["are", "r", "our"],
            "do": ["do", "du", "due"],
            "not": ["not", "nut", "no"],
            "will": ["will", "wheel", "well"],
            "is": ["is", "iz", "his"],
            "it": ["it", "eat"],
            "a": ["a", "uh", "an"],
            "the": ["the", "da", "d"],

            "hungry": ["hungry", "hangry", "angry", "hungi"],
            "thirsty": ["thirsty", "firsty", "thursty", "thirsti"],
            "tired": ["tired", "tyred", "tire"],
            "sick": ["sick", "six", "seek"],
            "okay": ["okay", "ok", "kay", "okey"],
            "cold": ["cold", "called", "gold"],
            "worried": ["worried", "worry", "warried"],
            "scared": ["scared", "skared", "scarred"],

            "water": ["water", "wader", "워터"],
            "food": ["food", "fud", "put"],
            "help": ["help", "hell", "halp"],
            "medicine": ["medicine", "medisin", "medicen"],
            "hospital": ["hospital", "hospitel", "hostpital"],
            "taxi": ["taxi", "teksi", "tax"],
            "ticket": ["ticket", "tiket"],
            "key": ["key", "ki"],
            "rice": ["rice", "rise", "lice"],
            "bread": ["bread", "bred"],
            "milk": ["milk", "melk"],
            "juice": ["juice", "juse"],
            "coffee": ["coffee", "coffe", "copy"],
            "snack": ["snack", "snek"],

            "eating": ["eating", "eatin", "eading"],
            "drinking": ["drinking", "drinkin", "dringking"],
            "waiting": ["waiting", "waitin", "weighting"],
            "studying": ["studying", "studyin", "studding"],
            "reading": ["reading", "reeding"],
            "writing": ["writing", "righting", "lighting"],
            "walking": ["walking", "working", "woking"],
            "listening": ["listening", "lissening", "lessonning"],

            "go": ["go", "goal", "고"],
            "wait": ["wait", "weight", "wet"],
            "study": ["study", "stady", "steady"],
            "eat": ["eat", "it"],
            "drink": ["drink", "dring", "drank"],
            "know": ["know", "no", "now"],
            "understand": ["understand", "understend", "understanded"],
            "want": ["want", "won", "wanna"],
            "bathroom": ["bathroom", "bath room", "batroom"],
            "store": ["store", "stole"],
            "station": ["station", "stashion", "staytion"],
            "time": ["time", "타임"],
            "name": ["name", "네임"]
        };

        if (!aliases[aw]) return false;
        return aliases[aw].includes(sw);
    }

    function isSmallRecognitionMistake(spokenWord, answerWord) {
        if (!spokenWord || !answerWord) return false;

        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        if (!sw || !aw) return false;
        if (sw === aw) return true;
        if (aliasMatch(sw, aw)) return true;

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
        const sameLastTwo = sw.slice(-2) === aw.slice(-2);

        const soundSameFirst =
            soundSw && soundAw && soundSw.charAt(0) === soundAw.charAt(0);

        const soundSameLast =
            soundSw && soundAw &&
            soundSw.charAt(soundSw.length - 1) === soundAw.charAt(soundAw.length - 1);

        // 완전히 다른 단어 방지용 최소 단서
        const hasAnyClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            soundSameFirst ||
            soundSameLast ||
            hasSharedBigram(sw, aw) ||
            sim >= 0.30 ||
            soundSim >= 0.22 ||
            vowelSim >= 0.25;

        if (!hasAnyClue) return false;

        // 일부만 인식된 경우 허용: medicine -> medicin, hospital -> hospi 등
        if (aw.length >= 4 && sw.length >= 2 && (aw.includes(sw) || sw.includes(aw))) {
            return true;
        }

        // 자음 뼈대가 같거나 거의 같으면 통과
        if (soundSw && soundAw && soundSw === soundAw) return true;
        if (soundSw && soundAw && soundDist <= 2 && soundSim >= 0.22) return true;

        // 1~2글자 단어도 문장 속 기능어라 너무 엄격하지 않게 처리
        if (aw.length <= 2) {
            return (
                sim >= 0.50 ||
                soundSim >= 0.28 ||
                sameFirst ||
                sameLast ||
                soundSameFirst ||
                soundSameLast
            );
        }

        // 3~4글자 핵심 단어: water, food, sick, cold, taxi, key 등 관대하게
        if (aw.length <= 4) {
            return (
                dist <= 2 ||
                sim >= 0.30 ||
                soundSim >= 0.20 ||
                vowelSim >= 0.24 ||
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
                sim >= 0.32 ||
                soundSim >= 0.22 ||
                vowelSim >= 0.25 ||
                sameFirst ||
                sameFirstTwo ||
                sameLast ||
                sameLastTwo ||
                hasSharedBigram(sw, aw)
            );
        }

        // 긴 단어: 일부 음절과 흐름이 맞으면 인정
        return (
            dist <= 6 ||
            sim >= 0.28 ||
            soundSim >= 0.20 ||
            vowelSim >= 0.22 ||
            sameFirst ||
            sameFirstTwo ||
            sameLast ||
            sameLastTwo ||
            hasSharedBigram(sw, aw)
        );
    }

    function getCoreHintWords() {
        if (!currentItem || !currentItem.hint) return [];
        return String(currentItem.hint || "")
            .split("/")
            .map(x => normalizeText(x).trim())
            .filter(x => x.length > 0);
    }

    function removeFillerWords(words) {
        return words.filter(w =>
            !["a", "an", "the", "uh", "um", "please", "yes", "no"].includes(w)
        );
    }

    function isCloseEnough(spoken, answer) {
        const s = normalizeText(spoken);
        const a = normalizeText(answer);

        if (!s || !a) return false;
        if (s === a) return true;

        const spokenWords = wordsOnly(s);
        const answerWords = wordsOnly(a);

        if (spokenWords.length === 0 || answerWords.length === 0) return false;

        // 문장 말하기 활동이므로 핵심 단어만 말하면 오답입니다.
        // 예: "I am hungry."에서 "hungry"만 말하면 오답
        // 대신 문장 골격을 말했으면 나머지 발음/인식은 관대하게 봅니다.

        // 너무 짧게 말한 경우는 문장으로 인정하지 않음
        // 단, "I need hospital"처럼 a 하나 빠지는 정도는 허용
        const minWordsNeeded = Math.max(2, answerWords.length - 1);
        if (spokenWords.length < minWordsNeeded) {
            return false;
        }

        // 첫 단어는 문장 골격이므로 반드시 비슷하게 맞아야 함
        // I / Are / Do / Where / What 등
        if (!isSmallRecognitionMistake(spokenWords[0], answerWords[0])) {
            return false;
        }

        // 핵심 빈칸 단어는 반드시 포함되어야 함
        const coreHints = getCoreHintWords();
        let coreMatched = coreHints.length === 0;

        for (const hint of coreHints) {
            const hintWords = wordsOnly(hint);
            const joinedHint = hintWords.join("");

            if (hintWords.length === 1) {
                const target = hintWords[0];

                for (const sw of spokenWords) {
                    if (isSmallRecognitionMistake(sw, target)) {
                        coreMatched = true;
                        break;
                    }
                }
            } else if (hintWords.length >= 2) {
                const joinedSpoken = spokenWords.join("");
                if (isSmallRecognitionMistake(joinedSpoken, joinedHint)) {
                    coreMatched = true;
                } else {
                    let pos = 0;
                    for (const sw of spokenWords) {
                        const target = hintWords[pos];
                        if (!target) break;

                        if (isSmallRecognitionMistake(sw, target)) {
                            pos += 1;
                        }

                        if (pos >= hintWords.length) break;
                    }

                    if (pos >= hintWords.length) coreMatched = true;
                }
            }

            if (coreMatched) break;
        }

        if (!coreMatched) return false;

        // 문장 전체 단어를 순서대로 관대하게 매칭
        // 기능어 하나 빠짐, filler 하나 들어감 정도는 허용
        let answerPos = 0;
        let matched = 0;

        for (let i = 0; i < spokenWords.length; i++) {
            const sw = spokenWords[i];
            const target = answerWords[answerPos];

            if (!target) break;

            if (isSmallRecognitionMistake(sw, target)) {
                matched += 1;
                answerPos += 1;
                continue;
            }

            // 불필요하게 들어간 filler는 건너뜀
            if (["a", "an", "the", "uh", "um", "please", "yes", "no"].includes(sw)) {
                continue;
            }

            // 정답 쪽의 짧은 기능어가 빠진 경우 허용
            // 예: I need a hospital -> I need hospital
            const nextTarget = answerWords[answerPos + 1];
            if (
                target &&
                target.length <= 2 &&
                nextTarget &&
                isSmallRecognitionMistake(sw, nextTarget)
            ) {
                matched += 1;      // 기능어 하나는 맞은 흐름으로 인정
                answerPos += 2;
                continue;
            }

            // 현재 spoken 단어가 다음 정답 단어와 맞으면, 중간 단어 하나 빠진 것으로 허용
            // 예: I do not understand -> I don't understand 정규화 흔들림 대비
            if (
                nextTarget &&
                isSmallRecognitionMistake(sw, nextTarget)
            ) {
                matched += 1;
                answerPos += 2;
                continue;
            }
        }

        // 핵심 단어는 맞았고, 문장 골격 대부분이 맞으면 정답
        const requiredMatches = Math.max(2, Math.ceil(answerWords.length * 0.60));

        if (matched >= requiredMatches) {
            return true;
        }

        // 짧은 문장은 첫 단어 + 핵심 단어 + 단어 수 조건을 만족하면 통과
        // 예: I am hungry / Are you hungry / Do you need water
        if (
            answerWords.length <= 4 &&
            coreMatched &&
            spokenWords.length >= minWordsNeeded &&
            isSmallRecognitionMistake(spokenWords[0], answerWords[0])
        ) {
            return true;
        }

        return false;
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

    function makeFilledBlankSentenceHtml(blankText, hintText) {
        const answers = String(hintText || "")
            .split("/")
            .map(x => x.trim())
            .filter(x => x.length > 0);

        let blankIndex = 0;
        const parts = String(blankText || "").split(/(______)/g);

        return parts.map(part => {
            if (part === "______") {
                const fill = answers[blankIndex] || "";
                blankIndex += 1;

                return "<span style='display:inline-block; min-width:96px; vertical-align:middle; background:#dcfce7; color:#166534; border-radius:14px; margin:0 6px; padding:4px 12px; border:1.5px solid #86efac; font-weight:900; box-shadow:0 3px 8px rgba(34,197,94,0.10);'>"
                    + escapeHtml(fill) +
                    "</span>";
            }

            return escapeHtml(part);
        }).join("");
    }

    function makeAnswerSentenceHtml(answer) {
        return answer.split(/\s+/).map(word => {
            return "<span style='display:inline-block; margin:4px 5px; padding:6px 11px; border-radius:999px; background:#dcfce7; color:#166534; border:1px solid #bbf7d0; font-weight:900;'>" +
                    escapeHtml(word) + "</span>";
        }).join("");
    }


    function updateScore() {
        scoreLabel.innerText = "정답 " + score + "개";
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

        categoryLabel.innerText = "문장 " + categorySelect.value + " · " + (currentIndex + 1) + " / " + currentList.length;
        const emoji = currentItem.emoji || "🛟";
        koPrompt.innerHTML =
            "<span style='font-size:42px; margin-right:10px; vertical-align:middle;'>" + emoji + "</span>" +
            "<span style='vertical-align:middle;'>" + currentItem.ko + "</span>";
        blankSentence.innerHTML = makeBlankSentenceHtml(currentItem.blank);
        hintBox.style.display = "none";
        answerBox.style.display = "none";
        hintBox.innerText = "";
        answerBox.innerText = "";
        transcriptBox.innerText = "";

        // 처음에는 힌트, 말하기, 다음 버튼을 보이게 함
        resetMicState();
        hintBtn.style.display = "inline-block";
        micBtn.style.display = "inline-block";
        answerBtn.style.display = "inline-block";
        listenBtn.style.display = "none";
        nextBtn.style.display = "inline-block";

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

    function resetMicState() {
        isListening = false;
        if (recognitionTimeout) {
            clearTimeout(recognitionTimeout);
            recognitionTimeout = null;
        }
        micBtn.disabled = false;
        micBtn.style.opacity = "1";
        micBtn.style.pointerEvents = "auto";
        micBtn.innerText = "🎙️";
    }

    function stopRecognition() {
        if (recognitionTimeout) {
            clearTimeout(recognitionTimeout);
            recognitionTimeout = null;
        }
        if (recognition) {
            try { recognition.onresult = null; } catch (e) {}
            try { recognition.onerror = null; } catch (e) {}
            try { recognition.onend = null; } catch (e) {}
            try { recognition.stop(); } catch (e) {}
            try { recognition.abort(); } catch (e) {}
            recognition = null;
        }
        resetMicState();
    }

    function goNextQuestion() {
        stopRecognition();
        window.speechSynthesis.cancel();
        loadQuestion(currentIndex + 1);
    }

    function checkSpeech(spokenText) {
        if (!currentItem) return;

        const recognized = String(spokenText || "").trim();

        if (isCorrectSpeech(recognized, currentItem.answer)) {
            if (!alreadyCorrect) {
                score += 1;
                alreadyCorrect = true;
            }

            updateScore();

            // 말해보카1 방식: 내가 말한 문장을 마이크 버튼 위에 띄우고, 빈칸에만 정답 단어를 채움
            transcriptBox.innerHTML =
                "<span style='color:#4c1d95;'>" + escapeHtml(recognized || currentItem.answer) + "</span> " +
                "<span style='color:#166534;'>✅ 정답입니다</span>";

            blankSentence.innerHTML = makeFilledBlankSentenceHtml(currentItem.blank, currentItem.hint);

            hintBox.style.display = "none";
            answerBox.style.display = "none";
            answerBtn.style.display = "inline-block";
            listenBtn.style.display = "none";
            nextBtn.style.display = "inline-block";

            resultBox.style.display = "none";
            resultBox.innerText = "";

            speak(currentItem.answer);
        } else {
            // 말해보카2 방식: 한 번 틀리면 힌트를 바로 보여줌
            transcriptBox.innerHTML =
                "<span style='color:#991b1b;'>" + escapeHtml(recognized || "인식 실패") + "</span> " +
                "<span style='color:#991b1b;'>❌</span>";

            hintBox.style.display = "block";
            hintBox.innerText = "힌트: " + makeTwoLetterHint(currentItem.hint);

            answerBtn.style.display = "inline-block";
            listenBtn.style.display = "none";
            nextBtn.style.display = "inline-block";

            resultBox.style.display = "block";
            resultBox.style.color = "#92400e";
            resultBox.innerText = "문장은 말해야 합니다. 다만 발음 시험은 아니므로, 문장 흐름과 핵심 단어가 맞으면 관대하게 정답으로 인정됩니다.";
        }
    }

    async function startRecognition() {
        if (!SpeechRecognition) {
            transcriptBox.innerText = "Chrome에서 열어 주세요.";
            return;
        }

        if (!currentItem) return;

        // 이전 음성 인식 객체가 남아 있으면 먼저 정리해서 버튼 먹통을 방지함
        stopRecognition();

        // 모바일에서 먼저 마이크 권한 요청
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                stream.getTracks().forEach(track => track.stop());
            } catch (err) {
                transcriptBox.innerText = "마이크 허용 후 다시 눌러 주세요.";
                resetMicState();
                return;
            }
        }

        window.speechSynthesis.cancel();

        try {
            recognition = new SpeechRecognition();
            recognition.lang = "en-US";
            recognition.interimResults = true;
            recognition.continuous = false;
            recognition.maxAlternatives = 5;

            isListening = true;
            micBtn.disabled = true;
            micBtn.style.opacity = "0.78";
            micBtn.innerText = "👂";
            resultBox.style.display = "none";
            resultBox.innerText = "";
            transcriptBox.innerText = "";

            recognitionTimeout = setTimeout(function() {
                if (isListening) {
                    try { recognition.stop(); } catch (e) {}
                    resetMicState();
                }
            }, 8000);

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
                    stopRecognition();
                    checkSpeech(spokenText);
                }
            };

            recognition.onerror = function(event) {
                stopRecognition();

                if (event.error === "not-allowed" || event.error === "service-not-allowed") {
                    transcriptBox.innerText = "마이크 허용 후 다시 눌러 주세요.";
                } else {
                    transcriptBox.innerText = "인식 실패";
                    hintBox.style.display = "block";
                    hintBox.innerText = "힌트: " + makeTwoLetterHint(currentItem.hint);
                    answerBtn.style.display = "inline-block";
                    nextBtn.style.display = "inline-block";
                    resultBox.style.display = "block";
                    resultBox.style.color = "#64748b";
                    resultBox.innerText = "다시 누르거나 다음 문제로 넘어갈 수 있습니다.";
                }
            };

            recognition.onend = function() {
                resetMicState();
            };

            recognition.start();
        } catch (err) {
            stopRecognition();
            transcriptBox.innerText = "다시 눌러 주세요.";
        }
    }

    categorySelect.addEventListener("change", function() {
        stopRecognition();
        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
    });

    randomBtn.addEventListener("click", function() {
        stopRecognition();
        currentList = shuffleArray(getFilteredItems());
        loadQuestion(0);
    });

    resetBtn.addEventListener("click", function() {
        stopRecognition();
        score = 0;
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
        if (!currentItem) return;
        answerBox.style.display = "none";
        blankSentence.innerHTML = makeFilledBlankSentenceHtml(currentItem.blank, currentItem.hint);
        transcriptBox.innerHTML = "<span style='color:#166534;'>" + escapeHtml(currentItem.answer) + "</span>";
        listenBtn.style.display = "none";
        nextBtn.style.display = "inline-block";
        speak(currentItem.answer);

        resultBox.style.display = "block";
        resultBox.style.color = "#166534";
        resultBox.innerText = "정답을 보고 들은 뒤, 다시 말하면 정답으로 인정됩니다.";
    });

    micBtn.addEventListener("click", startRecognition);

    nextBtn.addEventListener("click", function() {
        // 정답을 말하지 않고 넘어가면 정답 개수에는 포함하지 않음
        goNextQuestion();
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
