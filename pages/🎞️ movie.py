import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Batman English Mission", page_icon="🦇", layout="wide")

VIDEO_URL = "https://www.youtube.com/watch?v=U4fhEziQsc8"


# =========================
# BROWSER TTS BUTTON
# =========================

def speak_button(text, key):
    safe_text = (
        text.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace("\n", " ")
    )

    components.html(
        f"""
        <button 
            onclick="speak_{key}()"
            style="
                background:#facc15;
                color:#111827;
                border:none;
                border-radius:12px;
                padding:8px 14px;
                font-weight:900;
                cursor:pointer;
                margin:6px 0 10px 0;
            "
        >
            🔊 듣기
        </button>

        <script>
        function speak_{key}() {{
            const text = "{safe_text}";
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = "en-US";
            utterance.rate = 0.82;
            utterance.pitch = 1.0;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }}
        </script>
        """,
        height=55
    )


# =========================
# CSS
# =========================

st.markdown("""
<style>
.stApp {
    background: #ffffff;
    color: #111827;
}

.main-title {
    font-size: 46px;
    font-weight: 1000;
    color: #111827;
    margin-bottom: 4px;
}

.sub-title {
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 24px;
}

.hero-box {
    background: linear-gradient(135deg,#fef3c7 0%,#e0f2fe 55%,#f3e8ff 100%);
    border: 1px solid #fde68a;
    border-radius: 28px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(251,191,36,0.18);
}

.hero-title {
    font-size: 31px;
    font-weight: 1000;
    color: #0f172a;
    margin-bottom: 8px;
}

.hero-sub {
    font-size: 17px;
    color: #475569;
    line-height: 1.7;
}

.section-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    padding: 24px;
    margin: 18px 0;
    box-shadow: 0 6px 18px rgba(15,23,42,0.06);
}

.section-title {
    font-size: 26px;
    font-weight: 900;
    color: #111827;
    margin-bottom: 10px;
}

.small-guide {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 14px;
}

.line-box {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px;
    line-height: 1.8;
    font-size: 17px;
    margin-bottom: 12px;
}

.script-box {
    background: #ffffff;
    border: 1px solid #bfdbfe;
    border-radius: 18px;
    padding: 16px;
    line-height: 1.75;
    font-size: 16px;
    margin-bottom: 10px;
}

.kor {
    color: #6b7280;
    font-size: 15px;
}

.time-tag {
    display: inline-block;
    background: #facc15;
    color: #111827;
    font-weight: 900;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 13px;
    margin-bottom: 8px;
}

.success-box {
    background: #dcfce7;
    border: 1px solid #86efac;
    border-radius: 18px;
    padding: 16px;
    color: #166534;
    font-weight: 900;
    margin-top: 14px;
}

.fail-box {
    background: #fee2e2;
    border: 1px solid #fecaca;
    border-radius: 18px;
    padding: 16px;
    color: #991b1b;
    font-weight: 900;
    margin-top: 14px;
}

.info-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 18px;
    padding: 16px;
    color: #1e3a8a;
    font-weight: 800;
    margin-bottom: 12px;
}

.mission-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}

.badge {
    display:inline-block;
    background:#fef3c7;
    color:#92400e;
    border:1px solid #fde68a;
    padding:7px 12px;
    border-radius:999px;
    font-size:14px;
    font-weight:900;
    margin-right:6px;
}

.order-card {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 10px;
    font-size: 16px;
}

.choice-letter {
    display: inline-block;
    background: #111827;
    color: white;
    font-weight: 900;
    padding: 4px 9px;
    border-radius: 999px;
    margin-right: 8px;
}

div[data-testid="stButton"] button {
    border: 1px solid #bfdbfe;
    background: #ffffff;
    color: #111827;
    border-radius: 14px;
    padding: 14px 16px;
    font-weight: 900;
    text-align: left;
    min-height: 46px;
}

div[data-testid="stButton"] button:hover {
    background: #eff6ff;
    border: 1px solid #60a5fa;
    color: #111827;
}

div[data-testid="stButton"] button:disabled {
    background: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;
}

button[kind="primary"] {
    background: #facc15 !important;
    color: #111827 !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 900 !important;
}

input {
    font-weight: 900 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# DATA
# =========================

full_script = [
    {
        "time": "0:02",
        "en": "I killed those people. That's what I can be.",
        "ko": "내가 그 사람들을 죽였어. 나는 그런 사람이 될 수 있어."
    },
    {
        "time": "0:09",
        "en": "No, no. You can't. You're not.",
        "ko": "아니, 안 돼. 넌 그럴 수 없어. 넌 그런 사람이 아니야."
    },
    {
        "time": "0:12",
        "en": "I'm whatever Gotham needs me to be.",
        "ko": "나는 고담시가 필요로 하는 무엇이든 될 거야."
    },
    {
        "time": "0:16",
        "en": "A hero. Not the hero we deserved, but the hero we needed.",
        "ko": "영웅. 우리가 받을 자격이 있던 영웅은 아니지만, 우리에게 필요했던 영웅."
    },
    {
        "time": "0:20",
        "en": "Nothing less than a knight.",
        "ko": "그는 진정한 기사와 같은 존재야."
    },
    {
        "time": "0:28",
        "en": "You heard me. You can tell them.",
        "ko": "내 말 들었지. 사람들에게 그렇게 말해."
    },
    {
        "time": "0:32",
        "en": "You set the dogs on me.",
        "ko": "개들을 나에게 풀어."
    },
    {
        "time": "0:37",
        "en": "The truth isn't good enough.",
        "ko": "진실만으로는 충분하지 않아."
    },
    {
        "time": "0:48",
        "en": "Sometimes people deserve more.",
        "ko": "때로 사람들은 더 많은 것을 받을 자격이 있어."
    },
    {
        "time": "0:53",
        "en": "Sometimes people deserve to have their faith rewarded.",
        "ko": "때로 사람들은 자신의 믿음이 보상받을 자격이 있어."
    },
    {
        "time": "1:42",
        "en": "He's the hero Gotham deserves, but not the one it needs right now.",
        "ko": "그는 고담시가 받을 자격이 있는 영웅이지만, 지금 고담시에 필요한 영웅은 아니야."
    },
    {
        "time": "1:48",
        "en": "So we'll hunt him.",
        "ko": "그래서 우리는 그를 쫓을 거야."
    },
    {
        "time": "1:52",
        "en": "Because he can take it.",
        "ko": "왜냐하면 그는 그것을 감당할 수 있으니까."
    },
    {
        "time": "1:56",
        "en": "Because he's not our hero.",
        "ko": "왜냐하면 그는 우리의 영웅이 아니니까."
    },
    {
        "time": "2:06",
        "en": "He's a silent guardian, a watchful protector.",
        "ko": "그는 조용한 수호자이자, 늘 지켜보는 보호자야."
    }
]

key_lines = [
    {
        "time": "0:12",
        "en": "I'm whatever Gotham needs me to be.",
        "ko": "나는 고담시가 필요로 하는 무엇이든 될 거야.",
        "easy": "Batman will become what Gotham needs."
    },
    {
        "time": "0:16",
        "en": "Not the hero we deserved, but the hero we needed.",
        "ko": "우리가 받을 자격이 있던 영웅은 아니지만, 우리에게 필요했던 영웅.",
        "easy": "Batman is not a perfect public hero, but he is necessary."
    },
    {
        "time": "0:37",
        "en": "The truth isn't good enough.",
        "ko": "진실만으로는 충분하지 않아.",
        "easy": "Sometimes truth alone is not enough."
    },
    {
        "time": "0:48",
        "en": "Sometimes people deserve more.",
        "ko": "때로 사람들은 더 많은 것을 받을 자격이 있다.",
        "easy": "People sometimes need more than truth."
    },
    {
        "time": "0:53",
        "en": "Sometimes people deserve to have their faith rewarded.",
        "ko": "때로 사람들은 자신의 믿음이 보상받을 자격이 있다.",
        "easy": "People's hope should be protected."
    },
    {
        "time": "1:42",
        "en": "He's the hero Gotham deserves, but not the one it needs right now.",
        "ko": "그는 고담시가 받을 자격이 있는 영웅이지만, 지금 필요한 영웅은 아니다.",
        "easy": "Batman cannot be the public hero right now."
    },
    {
        "time": "1:52",
        "en": "Because he can take it.",
        "ko": "왜냐하면 그는 그것을 감당할 수 있으니까.",
        "easy": "Batman can endure blame."
    },
    {
        "time": "2:06",
        "en": "He's a silent guardian, a watchful protector.",
        "ko": "그는 조용한 수호자이자, 늘 지켜보는 보호자이다.",
        "easy": "Batman protects Gotham quietly."
    }
]


key_expressions = [
    {"word": "whatever", "ko": "무엇이든, 어떤 것이든", "example": "I'm whatever Gotham needs me to be."},
    {"word": "deserve", "ko": "~할 자격이 있다, ~을 받을 만하다", "example": "Sometimes people deserve more."},
    {"word": "hero", "ko": "영웅", "example": "He's the hero Gotham deserves."},
    {"word": "truth", "ko": "진실", "example": "The truth isn't good enough."},
    {"word": "faith", "ko": "믿음, 신뢰", "example": "People deserve to have their faith rewarded."},
    {"word": "reward", "ko": "보상하다", "example": "Their faith is rewarded."},
    {"word": "hunt", "ko": "쫓다, 추적하다", "example": "So we'll hunt him."},
    {"word": "take it", "ko": "그것을 감당하다, 견디다", "example": "Because he can take it."},
    {"word": "guardian", "ko": "수호자", "example": "He's a silent guardian."},
    {"word": "watchful", "ko": "주의 깊게 지켜보는", "example": "A watchful protector."},
    {"word": "protector", "ko": "보호자", "example": "A watchful protector."},
    {"word": "need", "ko": "필요로 하다", "example": "Gotham needs me."}
]

hero_questions = [
    {
        "q": "Q1. At first, what do people think Batman is?",
        "options": ["A hero", "A criminal", "A singer", "A teacher"],
        "answer": "A criminal"
    },
    {
        "q": "Q2. What is Batman really doing?",
        "options": ["Taking the blame", "Running away", "Making money", "Singing a song"],
        "answer": "Taking the blame"
    },
    {
        "q": "Q3. What kind of person is Batman in this scene?",
        "options": ["Sacrificing", "Lazy", "Selfish", "Funny"],
        "answer": "Sacrificing"
    },
    {
        "q": "Q4. Why can Batman endure it?",
        "options": ["Because he can take it", "Because he is tired", "Because he wants money", "Because he forgot"],
        "answer": "Because he can take it"
    }
]

blank_questions = [
    {
        "audio": "I'm whatever Gotham needs me to be.",
        "sentence": "I'm whatever Gotham ______ me to be.",
        "options": ["needs", "follows", "remembers"],
        "answer": "needs"
    },
    {
        "audio": "Not the hero we deserved, but the hero we needed.",
        "sentence": "Not the hero we ______, but the hero we ______.",
        "options": ["deserved / needed", "found / lost", "saw / followed"],
        "answer": "deserved / needed"
    },
    {
        "audio": "Sometimes people deserve more.",
        "sentence": "Sometimes people ______ more.",
        "options": ["deserve", "forget", "hide"],
        "answer": "deserve"
    },
    {
        "audio": "Because he can take it.",
        "sentence": "Because he can ______ it.",
        "options": ["take", "find", "change"],
        "answer": "take"
    },
    {
        "audio": "A silent guardian, a watchful protector.",
        "sentence": "A silent ______, a watchful ______.",
        "options": ["guardian / protector", "student / teacher", "singer / dancer"],
        "answer": "guardian / protector"
    }
]

correct_map = {
    "I'm whatever Gotham needs me to be.": "나는 고담시가 필요로 하는 무엇이든 될 거야.",
    "The truth isn't good enough.": "진실만으로는 충분하지 않아.",
    "Sometimes people deserve more.": "때로 사람들은 더 많은 것을 받을 자격이 있다.",
    "Because he can take it.": "왜냐하면 그는 그것을 감당할 수 있으니까.",
    "A silent guardian.": "조용한 수호자.",
    "A watchful protector.": "늘 지켜보는 보호자."
}


grammar_questions = [
    {
        "q": "He can ___ it.",
        "options": ["take", "takes", "took"],
        "answer": "take",
        "explain": "can 뒤에는 동사원형을 씁니다. 그래서 can take가 맞습니다."
    },
    {
        "q": "You can't ___ that.",
        "options": ["do", "does", "did"],
        "answer": "do",
        "explain": "can't 뒤에도 동사원형을 씁니다."
    },
    {
        "q": "Gotham ___ me.",
        "options": ["need", "needs", "needed"],
        "answer": "needs",
        "explain": "Gotham은 단수 주어이므로 현재시제에서는 needs를 씁니다."
    },
    {
        "q": "People deserve ___ more.",
        "options": ["have", "to have", "having"],
        "answer": "to have",
        "explain": "deserve 뒤에 동사가 올 때는 deserve to + 동사 형태를 쓸 수 있습니다."
    }
]


# =========================
# SESSION STATE
# =========================

if "batman_complete" not in st.session_state:
    st.session_state.batman_complete = {
        "choice": False,
        "blank": False,
        "matching": False,
        "grammar": False
    }

if "selected_match" not in st.session_state:
    st.session_state.selected_match = None

if "matched_pairs" not in st.session_state:
    st.session_state.matched_pairs = set()

if "matching_english_list" not in st.session_state:
    st.session_state.matching_english_list = [
        "Because he can take it.",
        "A watchful protector.",
        "I'm whatever Gotham needs me to be.",
        "Sometimes people deserve more.",
        "A silent guardian.",
        "The truth isn't good enough."
    ]

if "matching_korean_list" not in st.session_state:
    st.session_state.matching_korean_list = [
        "진실만으로는 충분하지 않아.",
        "조용한 수호자.",
        "나는 고담시가 필요로 하는 무엇이든 될 거야.",
        "늘 지켜보는 보호자.",
        "왜냐하면 그는 그것을 감당할 수 있으니까.",
        "때로 사람들은 더 많은 것을 받을 자격이 있다."
    ]


# 객관식 재도전 상태
for mission_name in ["hero", "blank", "grammar"]:
    attempt_key = f"{mission_name}_attempt"
    wrong_key = f"{mission_name}_wrong"
    if attempt_key not in st.session_state:
        st.session_state[attempt_key] = 0
    if wrong_key not in st.session_state:
        st.session_state[wrong_key] = []


# 대사 빈칸 보기 순서: 정답 위치가 항상 같지 않도록 문항별로 섞어서 유지
if "blank_option_orders" not in st.session_state:
    st.session_state.blank_option_orders = {}


# =========================
# HEADER
# =========================

st.markdown('<div class="main-title">🦇 Batman English Mission</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Video-based English Activity · Bright Classroom Version</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-title">Hero or Villain?</div>
    <div class="hero-sub">
        Watch the Batman scene, read the subtitles, answer the first mission,
        listen and fill in key lines, match quotes, and discover grammar rules.
        <br>
        <span class="kor">배트맨 장면을 보고 4개의 영어 미션을 완성해 봅시다.</span>
    </div>
</div>
""", unsafe_allow_html=True)

completed_count = sum(st.session_state.batman_complete.values())

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<span class='badge'>선택 문제 {'✅' if st.session_state.batman_complete['choice'] else '⬜'}</span>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<span class='badge'>대사 빈칸 {'✅' if st.session_state.batman_complete['blank'] else '⬜'}</span>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<span class='badge'>대사 연결 {'✅' if st.session_state.batman_complete['matching'] else '⬜'}</span>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<span class='badge'>문법 {'✅' if st.session_state.batman_complete['grammar'] else '⬜'}</span>", unsafe_allow_html=True)

st.progress(completed_count / 4)


# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎬 영상",
    "🎧 대사 빈칸",
    "🧩 대사 연결",
    "📘 문법",
    "💬 핵심 대사",
    "🔑 핵심 표현"
])


# =========================
# TAB 1 VIDEO + FULL SCRIPT + HERO QUESTIONS
# =========================

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎬 Watch the Video</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상을 보면서 아래 영어 자막과 한국어 해석을 함께 확인하세요.</div>', unsafe_allow_html=True)

    st.video(VIDEO_URL)

    st.markdown("""
    <div class="line-box">
        <b>Today's Question</b><br>
        Is Batman a hero, a villain, or both?
        <br>
        <span class="kor">오늘의 질문: 배트맨은 영웅인가, 악당인가, 아니면 둘 다인가?</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📖 Full Script & Meaning")

    for line in full_script:
        st.markdown(f"""
        <div class="script-box">
            <span class="time-tag">{line["time"]}</span><br>
            <b>{line["en"]}</b><br>
            <span class="kor">{line["ko"]}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🦸 Hero or Villain Mission")
    st.markdown('<div class="small-guide">Read the questions and choose the best answer. Get 3 or more correct to complete the mission.</div>', unsafe_allow_html=True)

    # 1차: 전체 문제 / 2차: 틀린 문제만 다시 풀기
    hero_indices = (
        st.session_state.hero_wrong
        if st.session_state.hero_attempt == 1 and st.session_state.hero_wrong
        else list(range(len(hero_questions)))
    )

    hero_answers = {}

    for idx in hero_indices:
        item = hero_questions[idx]
        st.markdown(f"**{item['q']}**")
        hero_answers[idx] = st.radio(
            "하나를 고르세요.",
            item["options"],
            key=f"hero_{idx}_attempt_{st.session_state.hero_attempt}",
            horizontal=False
        )
        st.write("")

    if st.session_state.hero_attempt == 0:
        if st.button("Hero or Villain 1차 채점", key="check_hero_first", type="primary"):
            wrong = [
                idx for idx in hero_indices
                if hero_answers.get(idx) != hero_questions[idx]["answer"]
            ]
            score = len(hero_questions) - len(wrong)

            if not wrong:
                st.session_state.batman_complete["choice"] = True
                st.session_state.hero_attempt = 2
                st.markdown(f"### 점수: {score} / {len(hero_questions)}")
                st.markdown("""
                <div class="success-box">
                    🦸 전부 맞았습니다! Hero or Villain 임무를 완성했습니다.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.session_state.hero_wrong = wrong
                st.session_state.hero_attempt = 1
                st.markdown(f"### 점수: {score} / {len(hero_questions)}")
                st.markdown(f"""
                <div class="fail-box">
                    틀린 문제가 {len(wrong)}개 있습니다. 정답은 아직 보여주지 않습니다.<br>
                    틀린 문제만 다시 풀어 보세요.
                </div>
                """, unsafe_allow_html=True)
                st.rerun()

    elif st.session_state.hero_attempt == 1:
        if st.button("틀린 문제 다시 채점", key="check_hero_retry", type="primary"):
            still_wrong = [
                idx for idx in hero_indices
                if hero_answers.get(idx) != hero_questions[idx]["answer"]
            ]

            st.session_state.hero_attempt = 2
            st.session_state.hero_wrong = still_wrong
            st.session_state.batman_complete["choice"] = True

            if not still_wrong:
                st.markdown("""
                <div class="success-box">
                    🦸 재도전에서 모두 맞았습니다!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-box">
                    재도전이 끝났습니다. 아래에서 남은 오답의 정답을 확인하세요.
                </div>
                """, unsafe_allow_html=True)
                for idx in still_wrong:
                    st.write(f"**{hero_questions[idx]['q']}** → 정답: **{hero_questions[idx]['answer']}**")

    else:
        if st.session_state.hero_wrong:
            st.markdown("### 남은 오답 정답")
            for idx in st.session_state.hero_wrong:
                st.write(f"**{hero_questions[idx]['q']}** → **{hero_questions[idx]['answer']}**")
        else:
            st.markdown("""
            <div class="success-box">
                🦸 이 미션을 완료했습니다.
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 2 LINE BLANKS
# =========================

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎧 대사 빈칸</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">각 문장의 듣기 버튼을 누르고 빈칸에 들어갈 말을 고르세요. 1차 채점 후 틀린 문제만 다시 풀 수 있습니다.</div>', unsafe_allow_html=True)

    # 1차에는 전체 문제, 재도전에는 1차에서 틀린 문제만 보여 줍니다.
    if st.session_state.blank_attempt == 1:
        st.markdown("""
        <div class="fail-box">
            ❌ 아래 문제들은 1차에서 틀린 문제입니다.<br>
            정답은 아직 공개하지 않습니다. 다시 듣고 한 번 더 풀어 보세요.
        </div>
        """, unsafe_allow_html=True)
        blank_indices = st.session_state.blank_wrong
    else:
        blank_indices = list(range(len(blank_questions)))

    blank_answers = {}

    for idx in blank_indices:
        item = blank_questions[idx]

        if st.session_state.blank_attempt == 1:
            q_label = f"❌ Q{idx + 1}. 1차 오답 — 다시 풀기"
        else:
            q_label = f"Q{idx + 1}. 듣고 고르세요."

        st.markdown(f"""
        <div class="mission-box">
            <b>{q_label}</b><br><br>
            <b>{item["sentence"]}</b>
        </div>
        """, unsafe_allow_html=True)

        speak_button(item["audio"], f"blank_{idx}_{st.session_state.blank_attempt}")

        # 정답이 늘 첫 번째에 오지 않도록 보기 순서를 섞습니다.
        # 같은 화면에서 Streamlit이 rerun되어도 순서는 유지됩니다.
        order_key = f"{idx}_{st.session_state.blank_attempt}"
        if order_key not in st.session_state.blank_option_orders:
            shuffled_options = item["options"].copy()
            random.shuffle(shuffled_options)

            # 우연히 정답이 첫 번째가 되면 가능한 경우 한 번 위치를 바꿉니다.
            if len(shuffled_options) > 1 and shuffled_options[0] == item["answer"]:
                swap_index = (idx % (len(shuffled_options) - 1)) + 1
                shuffled_options[0], shuffled_options[swap_index] = (
                    shuffled_options[swap_index],
                    shuffled_options[0],
                )

            st.session_state.blank_option_orders[order_key] = shuffled_options

        displayed_options = st.session_state.blank_option_orders[order_key]

        blank_answers[idx] = st.radio(
            "하나를 고르세요.",
            displayed_options,
            key=f"blank_{idx}_attempt_{st.session_state.blank_attempt}",
            horizontal=True,
            index=None
        )
        st.write("")

    # 1차 채점: 틀린 번호를 저장하고 정답은 공개하지 않음
    if st.session_state.blank_attempt == 0:
        if st.button("대사 빈칸 1차 채점", key="check_blank_first", type="primary"):
            unanswered = [idx for idx in blank_indices if blank_answers.get(idx) is None]

            if unanswered:
                st.warning("모든 문제에 답한 뒤 채점하세요.")
            else:
                wrong = [
                    idx for idx in blank_indices
                    if blank_answers.get(idx) != blank_questions[idx]["answer"]
                ]
                score = len(blank_questions) - len(wrong)

                if not wrong:
                    st.session_state.batman_complete["blank"] = True
                    st.session_state.blank_attempt = 2
                    st.session_state.blank_wrong = []
                    st.markdown(f"### 점수: {score} / {len(blank_questions)}")
                    st.markdown("""
                    <div class="success-box">
                        🎧 전부 맞았습니다! 대사 빈칸 임무를 완성했습니다.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.session_state.blank_wrong = wrong
                    st.session_state.blank_attempt = 1
                    st.rerun()

    # 재도전: 1차에서 틀린 문제만 다시 채점
    elif st.session_state.blank_attempt == 1:
        if st.button("틀린 빈칸 다시 채점", key="check_blank_retry", type="primary"):
            unanswered = [idx for idx in blank_indices if blank_answers.get(idx) is None]

            if unanswered:
                st.warning("재도전 문제에 모두 답한 뒤 채점하세요.")
            else:
                still_wrong = [
                    idx for idx in blank_indices
                    if blank_answers.get(idx) != blank_questions[idx]["answer"]
                ]

                st.session_state.blank_attempt = 2
                st.session_state.blank_wrong = still_wrong
                st.session_state.batman_complete["blank"] = True

                if not still_wrong:
                    st.markdown("""
                    <div class="success-box">
                        🎧 재도전에서 모두 맞았습니다!
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="info-box">
                        재도전이 끝났습니다. 아래에서 아직 틀린 문제의 정답을 확인하세요.
                    </div>
                    """, unsafe_allow_html=True)
                    for idx in still_wrong:
                        st.markdown(
                            f"❌ **Q{idx + 1}. {blank_questions[idx]['sentence']}**  "
                            f"→ 정답: **{blank_questions[idx]['answer']}**"
                        )

    # 재도전까지 끝난 뒤에만 남은 오답의 정답 공개
    else:
        if st.session_state.blank_wrong:
            st.markdown("### ❌ 재도전 후 남은 오답")
            for idx in st.session_state.blank_wrong:
                st.markdown(
                    f"**Q{idx + 1}. {blank_questions[idx]['sentence']}**  "
                    f"→ 정답: **{blank_questions[idx]['answer']}**"
                )
        else:
            st.markdown("""
            <div class="success-box">
                🎧 이 미션을 완료했습니다.
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 3 QUOTE MATCHING
# =========================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 대사 연결</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-guide">'
        '① 왼쪽 영어 대사를 하나 클릭하세요. '
        '② 오른쪽에서 알맞은 한국어 뜻을 하나 클릭하세요. '
        '정답이면 두 항목이 사라지고, 틀리면 다시 선택할 수 있습니다.'
        '</div>',
        unsafe_allow_html=True
    )

    # -------------------------
    # Matching 상태
    # -------------------------
    if "matching_selected_en" not in st.session_state:
        st.session_state.matching_selected_en = None

    if "matching_feedback" not in st.session_state:
        st.session_state.matching_feedback = None

    if "matching_feedback_type" not in st.session_state:
        st.session_state.matching_feedback_type = None

    # 기존 버전의 selected_match가 남아 있어도 충돌하지 않게 초기화
    st.session_state.selected_match = None

    matched_count = len(st.session_state.matched_pairs)

    # 상태 안내
    if st.session_state.matching_selected_en is None:
        guide_text = "👈 먼저 왼쪽에서 영어 대사를 하나 선택하세요."
    else:
        guide_text = f"선택한 영어: {st.session_state.matching_selected_en} → 오른쪽에서 뜻을 하나 고르세요."

    st.markdown(f"""
    <div class="info-box">
        {guide_text}<br>
        <b>맞춘 개수: {matched_count} / {len(correct_map)}</b>
    </div>
    """, unsafe_allow_html=True)

    # 직전 선택 결과 표시
    if st.session_state.matching_feedback:
        if st.session_state.matching_feedback_type == "correct":
            st.markdown(
                f'<div class="success-box">{st.session_state.matching_feedback}</div>',
                unsafe_allow_html=True
            )
        elif st.session_state.matching_feedback_type == "wrong":
            st.markdown(
                f'<div class="fail-box">{st.session_state.matching_feedback}</div>',
                unsafe_allow_html=True
            )

    # 맞힌 항목은 화면에서 사라지게 함
    remaining_english = [
        en for en in st.session_state.matching_english_list
        if en not in st.session_state.matched_pairs
    ]

    remaining_korean = [
        ko for ko in st.session_state.matching_korean_list
        if not any(
            en in st.session_state.matched_pairs and correct_ko == ko
            for en, correct_ko in correct_map.items()
        )
    ]

    left_col, right_col = st.columns(2)

    # -------------------------
    # 왼쪽: 영어 하나 선택
    # -------------------------
    with left_col:
        st.markdown("### 🇺🇸 English")

        if not remaining_english:
            st.success("영어 대사를 모두 맞췄습니다. ✅")
        else:
            for i, en in enumerate(remaining_english):
                is_selected = (st.session_state.matching_selected_en == en)

                if is_selected:
                    label = f"🟨 {en}"
                else:
                    label = en

                # 영어를 하나 선택한 뒤에는 다른 영어를 눌러 선택을 바꿀 수 있음
                if st.button(
                    label,
                    key=f"match_en_card_{i}_{en}",
                    use_container_width=True
                ):
                    st.session_state.matching_selected_en = en
                    st.session_state.matching_feedback = None
                    st.session_state.matching_feedback_type = None
                    st.rerun()

    # -------------------------
    # 오른쪽: 한국어 하나 선택
    # 영어를 먼저 선택해야 클릭 가능
    # -------------------------
    with right_col:
        st.markdown("### 🇰🇷 Korean")

        if not remaining_korean:
            st.success("한국어 뜻을 모두 맞췄습니다. ✅")
        else:
            for i, ko in enumerate(remaining_korean):
                can_click = st.session_state.matching_selected_en is not None

                if st.button(
                    ko,
                    key=f"match_ko_card_{i}_{ko}",
                    use_container_width=True,
                    disabled=not can_click
                ):
                    selected_en = st.session_state.matching_selected_en

                    if correct_map.get(selected_en) == ko:
                        st.session_state.matched_pairs.add(selected_en)
                        st.session_state.matching_feedback = "✅ 정답입니다! 맞춘 두 항목이 사라졌습니다."
                        st.session_state.matching_feedback_type = "correct"
                    else:
                        st.session_state.matching_feedback = "❌ 틀렸습니다. 영어 대사를 다시 선택해서 한 번 더 맞춰 보세요."
                        st.session_state.matching_feedback_type = "wrong"

                    # 한 쌍을 판정하면 반드시 선택 초기화
                    st.session_state.matching_selected_en = None
                    st.rerun()

    # -------------------------
    # 완료
    # -------------------------
    if len(st.session_state.matched_pairs) == len(correct_map):
        st.session_state.batman_complete["matching"] = True
        st.markdown("""
        <div class="success-box">
            🎉 대사 연결을 모두 완성했습니다!
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    if st.button("🔄 매칭 다시 시작", key="reset_matching", type="primary"):
        st.session_state.matching_selected_en = None
        st.session_state.matching_feedback = None
        st.session_state.matching_feedback_type = None
        st.session_state.matched_pairs = set()
        st.session_state.batman_complete["matching"] = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 4 GRAMMAR
# =========================

with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📘 Grammar Discovery</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상 대사를 보고 문법 규칙을 발견해 봅시다. 전부 맞히면 성공입니다.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="line-box">
        <b>Look at these lines.</b><br><br>
        1. He <b>can take</b> it.<br>
        2. You <b>can't do</b> that.<br>
        3. Gotham <b>needs</b> me.<br>
        4. People deserve <b>to have</b> more.<br><br>
        <span class="kor">
        생각해 봅시다: can/can't 뒤에는 어떤 모양의 동사가 올까요?
        </span>
    </div>
    """, unsafe_allow_html=True)

    grammar_indices = (
        st.session_state.grammar_wrong
        if st.session_state.grammar_attempt == 1 and st.session_state.grammar_wrong
        else list(range(len(grammar_questions)))
    )

    grammar_answers = {}

    for idx in grammar_indices:
        item = grammar_questions[idx]
        st.markdown(f"**Q{idx + 1}. {item['q']}**")
        grammar_answers[idx] = st.radio(
            "하나를 고르세요.",
            item["options"],
            key=f"grammar_{idx}_attempt_{st.session_state.grammar_attempt}",
            horizontal=True
        )
        st.write("")

    if st.session_state.grammar_attempt == 0:
        if st.button("문법 1차 채점", key="check_grammar_first", type="primary"):
            wrong = [
                idx for idx in grammar_indices
                if grammar_answers.get(idx) != grammar_questions[idx]["answer"]
            ]
            score = len(grammar_questions) - len(wrong)

            if not wrong:
                st.session_state.batman_complete["grammar"] = True
                st.session_state.grammar_attempt = 2
                st.markdown(f"### 점수: {score} / {len(grammar_questions)}")
                st.markdown("""
                <div class="success-box">
                    📘 전부 맞았습니다! 문법 임무를 완성했습니다.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.session_state.grammar_wrong = wrong
                st.session_state.grammar_attempt = 1
                st.markdown(f"### 점수: {score} / {len(grammar_questions)}")
                st.markdown(f"""
                <div class="fail-box">
                    틀린 문제가 {len(wrong)}개 있습니다. 해설과 정답은 아직 공개하지 않습니다.<br>
                    틀린 문제만 다시 풀어 보세요.
                </div>
                """, unsafe_allow_html=True)
                st.rerun()

    elif st.session_state.grammar_attempt == 1:
        if st.button("틀린 문법 다시 채점", key="check_grammar_retry", type="primary"):
            still_wrong = [
                idx for idx in grammar_indices
                if grammar_answers.get(idx) != grammar_questions[idx]["answer"]
            ]

            st.session_state.grammar_attempt = 2
            st.session_state.grammar_wrong = still_wrong
            st.session_state.batman_complete["grammar"] = True

            if not still_wrong:
                st.markdown("""
                <div class="success-box">
                    📘 재도전에서 모두 맞았습니다!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-box">
                    재도전이 끝났습니다. 남은 오답의 정답과 해설을 확인하세요.
                </div>
                """, unsafe_allow_html=True)
                for idx in still_wrong:
                    item = grammar_questions[idx]
                    st.write(f"**Q{idx + 1}. 정답: {item['answer']}**")
                    st.write(item["explain"])

    else:
        if st.session_state.grammar_wrong:
            st.markdown("### 남은 오답 정답 및 해설")
            for idx in st.session_state.grammar_wrong:
                item = grammar_questions[idx]
                st.write(f"**Q{idx + 1}. 정답: {item['answer']}**")
                st.write(item["explain"])
        else:
            st.markdown("""
            <div class="success-box">
                📘 이 미션을 완료했습니다.
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.grammar_attempt >= 2:
        st.markdown("""
    <div class="line-box">
        <b>Grammar Rule</b><br><br>
        1. <b>can + 동사원형</b><br>
        예: He can take it.<br><br>
        2. <b>can't + 동사원형</b><br>
        예: You can't do that.<br><br>
        3. 단수 주어 현재동사에는 보통 <b>-s</b>를 붙입니다.<br>
        예: Gotham needs me.<br><br>
        4. <b>deserve to + 동사</b>는 '~할 자격이 있다'라는 뜻입니다.<br>
        예: People deserve to have more.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)



# =========================
# TAB 5 QUOTES
# =========================

with tab5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Key Quotes</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상 속 핵심 대사와 쉬운 뜻을 마지막으로 다시 확인하세요.</div>', unsafe_allow_html=True)

    for line in key_lines:
        st.markdown(f"""
        <div class="line-box">
            <span class="time-tag">{line["time"]}</span><br>
            <b>{line["en"]}</b><br>
            <span class="kor">{line["ko"]}</span><br><br>
            <b>Easy Meaning:</b> {line["easy"]}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 6 KEY EXPRESSIONS
# =========================

with tab6:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔑 Key Expressions</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영화 속 핵심 단어와 표현을 뜻, 예문, TTS와 함께 확인하세요.</div>', unsafe_allow_html=True)

    for i, item in enumerate(key_expressions, start=1):
        st.markdown(f"""
        <div class="line-box">
            <b>{i}. {item["word"]}</b><br>
            <span class="kor">{item["ko"]}</span><br><br>
            <b>Example:</b> {item["example"]}
        </div>
        """, unsafe_allow_html=True)

        speak_button(item["word"], f"key_word_{i}")
        speak_button(item["example"], f"key_example_{i}")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# FINAL STATUS
# =========================

st.markdown("---")

completed_count = sum(st.session_state.batman_complete.values())

if completed_count == 4:
    st.markdown("""
    <div class="success-box">
        🦇 모든 배트맨 영어 미션을 완성하셨습니다!  
        You are Gotham's English Guardian!
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="line-box">
        <b>Mission Progress:</b> {completed_count} / 4 completed<br>
        <span class="kor">아직 완료하지 않은 미션을 마저 해결하세요.</span>
    </div>
    """, unsafe_allow_html=True)
