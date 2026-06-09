import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="자동차과 실무 영어 단어 카드 말하기 게임",
    page_icon="🚗",
    layout="wide"
)

# =========================================================
# 자동차과 실무 영어 단어 데이터
# 순서: 정밀기계 → 용접 → 자동차수리 → 전기·전자
# =========================================================
WORD_THEMES = {
    "⚙️ 정밀기계": [
        {"word": "precision machine", "meaning": "정밀 기계"},
        {"word": "lathe", "meaning": "선반"},
        {"word": "milling machine", "meaning": "밀링 머신"},
        {"word": "drilling machine", "meaning": "드릴링 머신"},
        {"word": "grinder", "meaning": "연삭기"},
        {"word": "CNC machine", "meaning": "CNC 기계"},
        {"word": "cutting tool", "meaning": "절삭 공구"},
        {"word": "workpiece", "meaning": "가공물"},
        {"word": "chuck", "meaning": "척, 고정 장치"},
        {"word": "spindle", "meaning": "주축"},
        {"word": "feed rate", "meaning": "이송 속도"},
        {"word": "cutting speed", "meaning": "절삭 속도"},
        {"word": "surface finish", "meaning": "표면 거칠기, 표면 마감"},
        {"word": "tolerance", "meaning": "공차"},
        {"word": "dimension", "meaning": "치수"},
        {"word": "diameter", "meaning": "직경"},
        {"word": "depth", "meaning": "깊이"},
        {"word": "thread", "meaning": "나사산"},
        {"word": "groove", "meaning": "홈"},
        {"word": "burr", "meaning": "버, 날카로운 찌꺼기"},
        {"word": "deburring", "meaning": "버 제거"},
        {"word": "caliper", "meaning": "버니어 캘리퍼스"},
        {"word": "micrometer", "meaning": "마이크로미터"},
        {"word": "gauge", "meaning": "게이지"},
        {"word": "blueprint", "meaning": "도면"},
        {"word": "measure", "meaning": "측정하다"},
        {"word": "machine", "meaning": "가공하다"},
        {"word": "adjust", "meaning": "조정하다"},
        {"word": "align", "meaning": "정렬하다"},
        {"word": "inspect", "meaning": "검사하다"},
    ],
    "🔥 용접": [
        {"word": "welding", "meaning": "용접"},
        {"word": "welder", "meaning": "용접공, 용접기"},
        {"word": "arc welding", "meaning": "아크 용접"},
        {"word": "gas welding", "meaning": "가스 용접"},
        {"word": "spot welding", "meaning": "점용접"},
        {"word": "MIG welding", "meaning": "MIG 용접"},
        {"word": "TIG welding", "meaning": "TIG 용접"},
        {"word": "electrode", "meaning": "전극봉"},
        {"word": "welding rod", "meaning": "용접봉"},
        {"word": "filler metal", "meaning": "용가재"},
        {"word": "base metal", "meaning": "모재"},
        {"word": "weld bead", "meaning": "용접 비드"},
        {"word": "joint", "meaning": "이음부"},
        {"word": "seam", "meaning": "이음선"},
        {"word": "torch", "meaning": "토치"},
        {"word": "shielding gas", "meaning": "보호 가스"},
        {"word": "spark", "meaning": "불꽃"},
        {"word": "slag", "meaning": "슬래그"},
        {"word": "spatter", "meaning": "스패터, 튄 금속"},
        {"word": "welding mask", "meaning": "용접면"},
        {"word": "welding gloves", "meaning": "용접 장갑"},
        {"word": "apron", "meaning": "앞치마"},
        {"word": "grind", "meaning": "갈다, 연마하다"},
        {"word": "clamp", "meaning": "클램프"},
        {"word": "cutting torch", "meaning": "절단 토치"},
        {"word": "heat", "meaning": "가열하다"},
        {"word": "melt", "meaning": "녹이다"},
        {"word": "cool down", "meaning": "식히다"},
        {"word": "crack", "meaning": "균열"},
        {"word": "burn mark", "meaning": "그을린 자국"},
    ],
    "🔧 자동차수리": [
        {"word": "auto repair", "meaning": "자동차 수리"},
        {"word": "mechanic", "meaning": "정비사"},
        {"word": "repair shop", "meaning": "정비소"},
        {"word": "inspection", "meaning": "점검"},
        {"word": "maintenance", "meaning": "정비, 유지관리"},
        {"word": "engine", "meaning": "엔진"},
        {"word": "transmission", "meaning": "변속기"},
        {"word": "brake", "meaning": "브레이크"},
        {"word": "brake pad", "meaning": "브레이크 패드"},
        {"word": "tire", "meaning": "타이어"},
        {"word": "wheel", "meaning": "휠"},
        {"word": "suspension", "meaning": "서스펜션"},
        {"word": "shock absorber", "meaning": "쇼크 업소버"},
        {"word": "radiator", "meaning": "라디에이터"},
        {"word": "coolant", "meaning": "냉각수"},
        {"word": "engine oil", "meaning": "엔진 오일"},
        {"word": "oil filter", "meaning": "오일 필터"},
        {"word": "air filter", "meaning": "에어 필터"},
        {"word": "spark plug", "meaning": "점화 플러그"},
        {"word": "belt", "meaning": "벨트"},
        {"word": "hose", "meaning": "호스"},
        {"word": "muffler", "meaning": "소음기"},
        {"word": "exhaust pipe", "meaning": "배기관"},
        {"word": "jack", "meaning": "잭"},
        {"word": "wrench", "meaning": "렌치"},
        {"word": "screwdriver", "meaning": "드라이버"},
        {"word": "replace", "meaning": "교체하다"},
        {"word": "tighten", "meaning": "조이다"},
        {"word": "loosen", "meaning": "풀다"},
        {"word": "test drive", "meaning": "시운전"},
    ],
    "🔋 전기·전자": [
        {"word": "electricity", "meaning": "전기"},
        {"word": "electronics", "meaning": "전자"},
        {"word": "battery", "meaning": "배터리"},
        {"word": "alternator", "meaning": "발전기"},
        {"word": "starter motor", "meaning": "시동 모터"},
        {"word": "motor", "meaning": "모터"},
        {"word": "generator", "meaning": "발전기"},
        {"word": "circuit", "meaning": "회로"},
        {"word": "wire", "meaning": "전선"},
        {"word": "connector", "meaning": "커넥터"},
        {"word": "terminal", "meaning": "단자"},
        {"word": "fuse", "meaning": "퓨즈"},
        {"word": "relay", "meaning": "릴레이"},
        {"word": "switch", "meaning": "스위치"},
        {"word": "sensor", "meaning": "센서"},
        {"word": "ECU", "meaning": "전자제어장치"},
        {"word": "voltage", "meaning": "전압"},
        {"word": "current", "meaning": "전류"},
        {"word": "resistance", "meaning": "저항"},
        {"word": "ground", "meaning": "접지"},
        {"word": "short circuit", "meaning": "합선"},
        {"word": "open circuit", "meaning": "단선"},
        {"word": "multimeter", "meaning": "멀티미터"},
        {"word": "diagnostic scanner", "meaning": "진단 스캐너"},
        {"word": "OBD port", "meaning": "차량 진단 포트"},
        {"word": "warning light", "meaning": "경고등"},
        {"word": "check engine light", "meaning": "엔진 경고등"},
        {"word": "electric vehicle", "meaning": "전기차"},
        {"word": "charging port", "meaning": "충전구"},
        {"word": "inverter", "meaning": "인버터"},
    ],
}

# =========================================================
# 상단 디자인
# =========================================================
st.markdown(
    """
    <style>
    .main-title-box {
        background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 50%, #fff7ed 100%);
        border: 1.5px solid #bfdbfe;
        border-radius: 30px;
        padding: 28px 30px;
        margin-bottom: 22px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.07);
    }

    .main-title-box h1 {
        margin: 0 0 10px 0;
        color: #0f172a;
        font-size: 38px;
        font-weight: 1000;
    }

    .main-title-box p {
        margin: 0;
        color: #475569;
        font-size: 18px;
        line-height: 1.7;
        font-weight: 800;
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
        <h1>🚗 자동차과 실무 영어 단어 카드 말하기 게임</h1>
        <p>한국말 뜻을 보고 영어 단어를 말해 보세요. 발음 시험이 아니라 전공 단어를 알고 있는지 확인하는 활동입니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 말하기 카드 게임 컴포넌트
# =========================================================
def auto_word_card_speaking_game(word_themes):
    items = []
    for cat, words in word_themes.items():
        cat_emoji = cat.split()[0] if cat else "🚗"
        for item in words:
            new_item = dict(item)
            new_item["cat"] = cat
            new_item["emoji"] = cat_emoji
            items.append(new_item)

    items_json = json.dumps(items, ensure_ascii=False)

    html = r"""
    <div id="auto-word-card-app" style="
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 50%, #fff7ed 100%);
        border: 1.5px solid #bfdbfe;
        border-radius: 30px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        max-width: 100%;
        overflow-x: hidden;
        box-sizing: border-box;
    ">
        <style>
            #auto-word-card-app * {
                box-sizing: border-box;
            }

            #auto-word-card-app button {
                -webkit-tap-highlight-color: transparent;
                touch-action: manipulation;
            }

            #auto-word-card-app select {
                max-width: 100%;
            }

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
                0% {
                    opacity: 0;
                    transform: translateX(46px) scale(0.965);
                    filter: blur(3px) brightness(1.05);
                }
                55% {
                    opacity: 1;
                    transform: translateX(-7px) scale(1.012);
                    filter: blur(0) brightness(1.03);
                }
                100% {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                    filter: blur(0) brightness(1);
                }
            }

            @keyframes nextBadgePop {
                0% {
                    opacity: 0;
                    transform: translateX(-50%) translateY(-18px) scale(0.86);
                }
                20% {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0) scale(1.04);
                }
                62% {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0) scale(1);
                }
                100% {
                    opacity: 0;
                    transform: translateX(-50%) translateY(-8px) scale(0.96);
                }
            }

            @keyframes nextLightSweep {
                0% {
                    opacity: 0;
                    transform: translateX(-115%);
                }
                20% {
                    opacity: 1;
                }
                100% {
                    opacity: 0;
                    transform: translateX(115%);
                }
            }

            @media (max-width: 768px) {
                #auto-word-card-app {
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
            <label style="font-weight:900; color:#334155;">단어 범위 선택</label>
            <select id="categorySelect" style="
                padding: 10px 14px;
                border-radius: 999px;
                border: 1.5px solid #bfdbfe;
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
                    background:#eff6ff;
                    color:#1d4ed8;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1px solid #bfdbfe;
                ">정답 0 / 0 · 연습 필요 단어 0</div>
            </div>

            <div id="cardBox" style="
                background:white;
                border-radius:32px;
                padding:30px 24px;
                border:1.5px solid #dbeafe;
                box-shadow:0 8px 24px rgba(0,0,0,0.07);
                text-align:center;
                margin-bottom:18px;
            ">
                <div id="emojiBox" style="
                    font-size: 96px;
                    line-height: 1.1;
                    margin-bottom: 14px;
                ">🚗</div>

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

                <div id="categoryBadge" style="
                    display:inline-block;
                    background:#eff6ff;
                    color:#1d4ed8;
                    border:1.5px solid #bfdbfe;
                    border-radius:999px;
                    padding:7px 14px;
                    font-size:14px;
                    font-weight:900;
                    margin-bottom:10px;
                ">분류</div>

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
                    word-break:break-word;
                ">hint</div>

                <div id="cardFeedbackBox" style="
                    display:none;
                    background:#ecfdf5;
                    border:1.5px solid #bbf7d0;
                    color:#166534;
                    border-radius:20px;
                    padding:14px 16px;
                    font-size:28px;
                    font-weight:900;
                    margin-top:14px;
                    word-break:break-word;
                ">✅ 정답입니다!</div>
            </div>

            <div id="buttonBox" style="margin-bottom:16px;">
                <div style="display:grid; grid-template-columns:1fr; gap:8px; margin-bottom:8px;">
                    <button id="micBtn" style="
                        width:100%;
                        border:1.5px solid #fecaca;
                        background:#fff1f2;
                        color:#be123c;
                        border-radius:999px;
                        padding:15px 20px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:18px;
                    ">🎙️ 말하기</button>
                </div>

                <div style="
                    background:#f8fafc;
                    border:1.5px solid #e2e8f0;
                    border-radius:18px;
                    padding:12px 14px;
                    margin-bottom:8px;
                    min-height:54px;
                ">
                    <div style="font-size:13px; color:#64748b; font-weight:900; margin-bottom:5px;">인식된 단어</div>
                    <div id="transcriptBox" style="font-size:22px; font-weight:900; color:#334155; word-break:break-word;"></div>
                </div>

                <div id="smallButtonRow" style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px;">
                    <button id="hintBtn" style="
                        border:1.5px solid #fed7aa;
                        background:#fff7ed;
                        color:#9a3412;
                        border-radius:999px;
                        padding:10px 5px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:13px;
                        white-space:nowrap;
                    ">💡 힌트</button>

                    <button id="answerBtn" style="
                        border:1.5px solid #bfdbfe;
                        background:#eff6ff;
                        color:#1d4ed8;
                        border-radius:999px;
                        padding:10px 5px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:13px;
                        white-space:nowrap;
                    ">정답+🔊</button>

                    <button id="skipBtn" style="
                        border:1.5px solid #c7d2fe;
                        background:#eef2ff;
                        color:#3730a3;
                        border-radius:999px;
                        padding:10px 5px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:13px;
                        white-space:nowrap;
                    ">다음 ➡️</button>
                </div>
            </div>

            <div id="resultBox" style="
                display:none;
                background:#f1f5f9;
                border:1.5px solid #e2e8f0;
                border-radius:18px;
                padding:10px 12px;
                font-size:16px;
                font-weight:900;
                color:#334155;
            ">
                마이크 버튼을 누르고 영어 단어를 말해 보세요. 발음 시험이 아니라 전공 단어를 아는지 확인하는 활동입니다.
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
            <div id="finishTitle" style="
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
            ">정답 0 / 0 · 연습 필요 단어 0</div>
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
    const categoryBadge = document.getElementById("categoryBadge");
    const answerBox = document.getElementById("answerBox");
    const hintBox = document.getElementById("hintBox");
    const cardFeedbackBox = document.getElementById("cardFeedbackBox");

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

    function uniqueCategories() {
        const categories = [];
        ITEMS.forEach(item => {
            if (!categories.includes(item.cat)) categories.push(item.cat);
        });
        return ["전체"] .concat(categories);
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
        const selected = categorySelect.value || "전체";
        if (selected === "전체") return ITEMS.slice();
        return ITEMS.filter(item => item.cat === selected);
    }

    function getItemKey(item) {
        return item.cat + "||" + item.meaning + "||" + item.word;
    }

    function escapeHtml(text) {
        return String(text || "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
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
            .replace(/\bcnc\b/g, "cnc")
            .replace(/\becu\b/g, "ecu")
            .replace(/\bobd\b/g, "obd")
            .replace(/\bmig\b/g, "mig")
            .replace(/\btig\b/g, "tig")
            .replace(/\bok\b/g, "okay")
            .replace(/\bo k\b/g, "okay")
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
            for (let j = 0; j <= b.length; j++) {
                dp[i][j] = 0;
            }
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
            "cncmachine": ["cncmachine", "cnc", "cncmashin", "cncmachin"],
            "ecU": ["ecu"],
            "ecu": ["ecu", "e c u"],
            "obdport": ["obdport", "obd", "obdboard", "obdpart"],
            "migwelding": ["migwelding", "mig", "megwelding"],
            "tigwelding": ["tigwelding", "tig", "teegwelding"],
            "lathe": ["lathe", "레이스", "lath", "late"],
            "millingmachine": ["millingmachine", "milling", "millionmachine"],
            "drillingmachine": ["drillingmachine", "drilling"],
            "grinder": ["grinder", "grind"],
            "caliper": ["caliper", "calliper", "calipers"],
            "micrometer": ["micrometer", "micro meter"],
            "welding": ["welding", "weld", "welting"],
            "welder": ["welder", "weldor"],
            "electrode": ["electrode", "electron"],
            "weldingrod": ["weldingrod", "weld rod", "welding lot"],
            "weldbead": ["weldbead", "weld bead"],
            "spatter": ["spatter", "splatter"],
            "spark": ["spark", "spock"],
            "torch": ["torch", "touch"],
            "brake": ["brake", "break"],
            "brakepad": ["brakepad", "breakpad", "brake pads"],
            "tire": ["tire", "tyre"],
            "wheel": ["wheel", "will"],
            "engineoil": ["engineoil", "engine oil"],
            "oilfilter": ["oilfilter", "oil filter"],
            "airfilter": ["airfilter", "air filter"],
            "sparkplug": ["sparkplug", "spark plug"],
            "wrench": ["wrench", "렌치", "rench"],
            "screwdriver": ["screwdriver", "screw driver"],
            "testdrive": ["testdrive", "test drive"],
            "battery": ["battery", "batery"],
            "alternator": ["alternator", "alter nator"],
            "startermotor": ["startermotor", "starter motor"],
            "circuit": ["circuit", "cirkit"],
            "wire": ["wire", "why are"],
            "fuse": ["fuse", "퓨즈"],
            "relay": ["relay", "realay"],
            "sensor": ["sensor", "censor"],
            "voltage": ["voltage", "bolt age"],
            "current": ["current", "curent"],
            "resistance": ["resistance", "resistants"],
            "shortcircuit": ["shortcircuit", "short circuit"],
            "opencircuit": ["opencircuit", "open circuit"],
            "multimeter": ["multimeter", "multi meter"],
            "diagnosticscanner": ["diagnosticscanner", "diagnostic scanner", "scanner"],
            "warninglight": ["warninglight", "warning light"],
            "checkenginelight": ["checkenginelight", "check engine light"],
            "electricvehicle": ["electricvehicle", "electric vehicle", "ev"],
            "chargingport": ["chargingport", "charging port"],
            "inverter": ["inverter", "invertor"]
        };

        if (!aliases[aw]) return false;
        return aliases[aw].includes(sw);
    }

    function soundOverlap(a, b) {
        const ka = soundKey(a);
        const kb = soundKey(b);

        if (!ka || !kb) return 0;
        if (ka === kb) return 1;

        let overlap = 0;
        for (let i = 0; i < ka.length; i++) {
            if (kb.indexOf(ka.charAt(i)) !== -1) overlap += 1;
        }

        return overlap / Math.max(1, Math.min(ka.length, kb.length));
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
        if (typeof KNOWN_ANSWER_WORDS === "undefined") return false;
        if (!KNOWN_ANSWER_WORDS.includes(sw)) return false;
        if (sw === aw) return false;
        if (aliasMatch(sw, aw)) return false;

        const sim = wordSimilarity(sw, aw);
        const soundSim = wordSimilarity(soundKey(sw), soundKey(aw));
        const vowelSim = wordSimilarity(vowelLooseKey(sw), vowelLooseKey(aw));

        const sameFirst = sw.charAt(0) === aw.charAt(0);
        const sameLast = sw.charAt(sw.length - 1) === aw.charAt(aw.length - 1);
        const sameFirstTwo = sw.slice(0, 2) === aw.slice(0, 2);
        const sameLastTwo = sw.slice(-2) === aw.slice(-2);

        const hasClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            hasSharedBigram(sw, aw) ||
            sim >= 0.38 ||
            soundSim >= 0.28 ||
            vowelSim >= 0.30;

        return !hasClue;
    }

    function isSmallRecognitionMistake(spokenWord, answerWord) {
        if (!spokenWord || !answerWord) return false;

        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        if (!sw || !aw) return false;
        if (sw === aw) return true;
        if (aliasMatch(sw, aw)) return true;

        if (isClearlyDifferentKnownWord(sw, aw)) {
            return false;
        }

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

        const soundSameFirst =
            soundSw && soundAw && soundSw.charAt(0) === soundAw.charAt(0);

        const soundSameLast =
            soundSw && soundAw &&
            soundSw.charAt(soundSw.length - 1) === soundAw.charAt(soundAw.length - 1);

        const overlap = soundOverlap(sw, aw);

        const hasAnyClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            soundSameFirst ||
            soundSameLast ||
            hasSharedBigram(sw, aw) ||
            soundSim >= 0.22 ||
            vowelSim >= 0.25 ||
            sim >= 0.28 ||
            overlap >= 0.28;

        if (!hasAnyClue) return false;

        // 일부만 인식되거나 붙여 인식되는 경우 허용
        if (aw.length >= 4 && sw.length >= 2 && (aw.includes(sw) || sw.includes(aw))) {
            return true;
        }

        // 자음 뼈대가 같거나 거의 같으면 단어를 안 것으로 처리
        if (soundSw && soundAw && soundSw === soundAw) return true;
        if (soundSw && soundAw && soundDist <= 2 && soundSim >= 0.22) return true;

        // 1~2글자 단어
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

        // 3~4글자 단어
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

        // 긴 단어
        return (
            dist <= 6 ||
            sim >= 0.28 ||
            soundSim >= 0.20 ||
            vowelSim >= 0.22 ||
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

            if (isSmallRecognitionMistake(s, target)) return true;

            for (const sw of spokenWords) {
                if (isSmallRecognitionMistake(sw, target)) {
                    return true;
                }
            }

            const joinedSpoken = spokenWords.join("");
            if (isSmallRecognitionMistake(joinedSpoken, target)) return true;

            const fillerRemoved = spokenWords.filter(w =>
                !["a", "an", "the", "uh", "um", "please", "yes", "no", "is", "it"].includes(w)
            );

            if (fillerRemoved.length > 0) {
                const joinedClean = fillerRemoved.join("");
                if (isSmallRecognitionMistake(joinedClean, target)) return true;

                for (const w of fillerRemoved) {
                    if (isSmallRecognitionMistake(w, target)) return true;
                }
            }

            return false;
        }

        if (s.includes(a)) return true;

        const joinedSpoken = spokenWords.join("");
        const joinedAnswer = answerWords.join("");
        if (isSmallRecognitionMistake(joinedSpoken, joinedAnswer)) return true;

        let pos = 0;

        for (const sw of spokenWords) {
            const target = answerWords[pos];
            if (!target) break;

            if (isSmallRecognitionMistake(sw, target)) {
                pos += 1;
            }

            if (pos >= answerWords.length) break;
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

                if (isSmallRecognitionMistake(sw, aw)) {
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
        if (currentList.length === 0) {
            currentList = getFilteredItems();
        }

        if (index >= currentList.length) {
            showFinishScreen();
            return;
        }

        if (index < 0) index = 0;

        showGameArea();
        cleanupRecognition();

        currentIndex = index;
        currentItem = currentList[currentIndex];

        emojiBox.innerText = currentItem.emoji || "🚗";
        meaningBox.innerText = currentItem.meaning;
        categoryBadge.innerText = currentItem.cat;

        answerBox.style.display = "none";
        answerBox.style.background = "#ecfdf5";
        answerBox.style.borderColor = "#bbf7d0";
        answerBox.style.color = "#166534";
        answerBox.innerText = "정답: " + currentItem.word;

        hintBox.style.display = "none";
        hintBox.innerText = "";

        cardFeedbackBox.style.display = "none";
        cardFeedbackBox.innerText = "✅ 정답입니다!";

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
            hintBox.style.display = "none";
            cardFeedbackBox.style.display = "block";
            cardFeedbackBox.innerText = "✅ 정답입니다! " + currentItem.word;

            transcriptBox.innerHTML =
                "<span style='color:#334155;'>" + escapeHtml(currentItem.word) + "</span>" +
                " <span style='display:inline-block; margin-left:8px; padding:4px 9px; border-radius:999px; background:#dcfce7; color:#166534; border:1px solid #bbf7d0; font-size:0.82em; font-weight:900; vertical-align:middle;'>✅ 정답</span>";
            transcriptBox.style.color = "#334155";

            resultBox.innerText = "";
            resultBox.style.display = "none";

            speak(currentItem.word);
            cleanupRecognition();
        } else {
            answerBox.style.display = "none";
            transcriptBox.style.color = "#334155";
            resultBox.style.display = "block";
            resultBox.innerText = "발음 시험이 아닙니다. 완전히 다른 단어가 아니면 비슷한 인식도 정답으로 인정됩니다. 다시 말해 보세요.";
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
        cardFeedbackBox.style.display = "none";
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
        cardFeedbackBox.style.display = "none";
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

    components.html(html, height=820, scrolling=True)


auto_word_card_speaking_game(WORD_THEMES)
