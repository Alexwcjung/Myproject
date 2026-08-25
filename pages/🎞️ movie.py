import streamlit as st
import streamlit.components.v1 as components
import random
import io
from gtts import gTTS

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



@st.cache_data(show_spinner=False)
def make_blank_tts_audio(text):
    """대사 빈칸 듣기용 mp3를 생성합니다."""
    safe_text = str(text).strip()
    if not safe_text:
        return b""

    fp = io.BytesIO()
    tts = gTTS(text=safe_text, lang="en", slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def show_blank_audio(text):
    """Streamlit 내장 오디오 플레이어로 대사를 재생합니다."""
    try:
        audio_bytes = make_blank_tts_audio(text)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.warning("음성을 불러오지 못했습니다. requirements.txt에 gTTS가 있는지 확인해 주세요.")
        st.caption(f"오류 내용: {e}")


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

.game-card {
    background:linear-gradient(135deg,#eef2ff,#f8fafc);
    border:1px solid #c7d2fe;
    border-radius:18px;
    padding:20px;
    margin-bottom:18px;
}

.big-guide {
    font-size:1.12rem;
    font-weight:800;
    color:#475569;
    line-height:1.7;
}

.score-box {
    background:linear-gradient(135deg,#dcfce7,#bbf7d0);
    padding:18px;
    border-radius:18px;
    border:1px solid #86efac;
    margin-top:18px;
    text-align:center;
    font-size:1.15rem;
    font-weight:900;
}

.wrong-box {
    background:#fff7ed;
    padding:15px;
    border-radius:14px;
    border:1px solid #fdba74;
    margin-top:10px;
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


if "blank_first_results" not in st.session_state:
    st.session_state.blank_first_results = {}


if "blank_current_index" not in st.session_state:
    st.session_state.blank_current_index = 0

if "blank_last_wrong" not in st.session_state:
    st.session_state.blank_last_wrong = False

if "blank_last_correct_answer" not in st.session_state:
    st.session_state.blank_last_correct_answer = None


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



# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎬 영상",
    "🎧 대사 빈칸",
    "🧩 대사 연결",
    "📘 문법",
    "💬 핵심 대사 & 표현"
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

    st.markdown(
        '<div class="game-card"><div class="big-guide">'
        '모든 문제를 먼저 풀어 보세요.<br>'
        '각 문제의 오디오 플레이어에서 대사를 듣고 빈칸에 들어갈 말을 고른 뒤 '
        '<b>대사 빈칸 정답 확인</b>을 누르세요.'
        '</div></div>',
        unsafe_allow_html=True
    )

    blank_user_answers = []

    for i, item in enumerate(blank_questions, start=1):
        # Pop Song 가사 이해도 퀴즈와 같은 문제 카드
        question_html = (
            '<div style="background:#ffffff;'
            'padding:16px 18px;'
            'border-radius:18px;'
            'border:1px solid #e2e8f0;'
            'margin-top:18px;">'
            '<div style="font-size:0.95rem;'
            'font-weight:900;'
            'color:#6366f1;'
            'margin-bottom:6px;">'
            '대사 듣기'
            '</div>'
            '<div style="font-size:1.12rem;'
            'font-weight:950;'
            'color:#1e293b;'
            'line-height:1.6;">'
            + str(i) + '. ' + item["sentence"] +
            '</div>'
            '</div>'
        )

        st.markdown(question_html, unsafe_allow_html=True)

        # HTML 버튼이 아닌 Streamlit 내장 오디오 플레이어
        show_blank_audio(item["audio"])

        # 정답 위치 고정 방지
        options = item["options"].copy()
        rng = random.Random(f"batman_blank_pop_quiz_{i}")
        rng.shuffle(options)

        picked = st.radio(
            "정답을 고르세요.",
            options,
            key=f"batman_blank_pop_answer_{i}",
            index=None,
            label_visibility="collapsed"
        )

        blank_user_answers.append((item, picked))

    c1, c2 = st.columns(2)

    with c1:
        submit_blank = st.button(
            "대사 빈칸 정답 확인",
            key="batman_blank_pop_submit",
            use_container_width=True,
            type="primary"
        )

    with c2:
        reset_blank = st.button(
            "대사 빈칸 다시 풀기",
            key="batman_blank_pop_reset",
            use_container_width=True
        )

    if reset_blank:
        for k in list(st.session_state.keys()):
            if str(k).startswith("batman_blank_pop_answer_"):
                del st.session_state[k]

        st.session_state.batman_complete["blank"] = False
        st.rerun()

    if submit_blank:
        unanswered = [
            idx
            for idx, (item, picked) in enumerate(blank_user_answers, start=1)
            if picked is None
        ]

        if unanswered:
            st.warning(
                "모든 문제에 답한 뒤 정답을 확인하세요. "
                f"선택하지 않은 문제: {', '.join(map(str, unanswered))}번"
            )

        else:
            score = sum(
                1
                for item, picked in blank_user_answers
                if picked == item["answer"]
            )

            st.markdown(
                f'<div class="score-box">점수: {score} / {len(blank_questions)}</div>',
                unsafe_allow_html=True
            )

            if score == len(blank_questions):
                st.session_state.batman_complete["blank"] = True
                st.success(
                    f"모두 맞혔습니다! "
                    f"{len(blank_questions)}문제 중 {score}문제를 맞혔습니다. 🎉"
                )
            else:
                st.session_state.batman_complete["blank"] = False
                st.warning(
                    f"{len(blank_questions)}문제 중 {score}문제를 맞혔습니다. "
                    "아래에서 결과를 확인한 뒤 다시 풀어 보세요."
                )

            # 결과 표시:
            # 정답이면 "정답입니다"만,
            # 오답이면 정답과 선택 답을 공개하지 않고 다시 풀도록 안내
            for idx, (item, picked) in enumerate(blank_user_answers, start=1):
                answer = item["answer"]

                if picked == answer:
                    st.success(f"{idx}번 정답입니다. ✅")
                else:
                    st.markdown(
                        f'<div class="wrong-box">'
                        f'<b>{idx}번</b> 다시 확인해 보세요. ❌<br>'
                        '정답은 아직 공개하지 않습니다. 대사를 다시 듣고 다시 풀어 보세요.'
                        '</div>',
                        unsafe_allow_html=True
                    )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 3 QUOTE MATCHING
# =========================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 대사 연결</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-guide">'
        '왼쪽 영어 대사를 하나 클릭하고, 오른쪽에서 알맞은 한국어 뜻을 하나 클릭하세요. '
        '정답이면 두 카드가 반짝이며 터지듯 사라집니다.'
        '</div>',
        unsafe_allow_html=True
    )

    import json
    import uuid

    # 각 쌍에 동일한 id 부여
    matching_pairs = [
        {
            "id": f"pair_{i}",
            "en": en,
            "ko": ko
        }
        for i, (en, ko) in enumerate(correct_map.items(), start=1)
    ]

    en_cards = [
        {"id": p["id"], "text": p["en"]}
        for p in matching_pairs
    ]

    ko_cards = [
        {"id": p["id"], "text": p["ko"]}
        for p in matching_pairs
    ]

    # 영어와 한국어 순서는 서로 다르게 섞음
    rng_en = random.Random("batman_matching_en")
    rng_ko = random.Random("batman_matching_ko")
    rng_en.shuffle(en_cards)
    rng_ko.shuffle(ko_cards)

    matching_payload = {
        "en": en_cards,
        "ko": ko_cards,
        "total": len(matching_pairs)
    }

    matching_json = json.dumps(matching_payload, ensure_ascii=False)
    component_id = "batman_match_" + uuid.uuid4().hex

    components.html(
        f"""
        <div id="{component_id}" class="match-app">

            <div class="match-status">
                <div id="status_{component_id}">
                    먼저 왼쪽에서 영어 대사를 하나 선택하세요.
                </div>
                <div id="score_{component_id}">
                    맞춘 개수: 0 / {len(matching_pairs)}
                </div>
            </div>

            <div class="match-board">
                <div class="match-col">
                    <div class="col-title">🇺🇸 English</div>
                    <div id="en_{component_id}" class="card-wrap"></div>
                </div>

                <div class="match-col">
                    <div class="col-title">🇰🇷 Korean</div>
                    <div id="ko_{component_id}" class="card-wrap"></div>
                </div>
            </div>

            <div class="progress-outer">
                <div id="bar_{component_id}" class="progress-inner"></div>
            </div>

            <button id="reset_{component_id}" class="reset-btn">
                🔄 매칭 다시 시작
            </button>

            <div id="done_{component_id}" class="done-message" style="display:none;">
                🎉 모든 대사를 맞췄습니다!
            </div>

        </div>

        <style>
            #{component_id}.match-app {{
                font-family: Arial, sans-serif;
                width:100%;
                box-sizing:border-box;
                background:linear-gradient(135deg,#eef2ff 0%,#f0f9ff 50%,#fdf2f8 100%);
                border:1px solid #c7d2fe;
                border-radius:22px;
                padding:22px;
                margin:8px 0 22px 0;
                color:#1e293b;
            }}

            #{component_id} .match-status {{
                display:grid;
                grid-template-columns:1.5fr .8fr;
                gap:10px;
                margin-bottom:14px;
            }}

            #{component_id} .match-status > div {{
                background:#ffffff;
                border:1px solid #dbeafe;
                border-radius:14px;
                padding:12px 14px;
                font-size:15px;
                font-weight:900;
                color:#1d4ed8;
            }}

            #{component_id} .match-board {{
                display:grid;
                grid-template-columns:1fr 1fr;
                gap:14px;
            }}

            #{component_id} .match-col {{
                background:rgba(255,255,255,.76);
                border:1px solid #e5e7eb;
                border-radius:18px;
                padding:14px;
            }}

            #{component_id} .col-title {{
                font-size:22px;
                font-weight:1000;
                color:#111827;
                margin-bottom:12px;
            }}

            #{component_id} .card-wrap {{
                display:flex;
                flex-direction:column;
                gap:10px;
            }}

            #{component_id} .match-card {{
                width:100%;
                text-align:left;
                border:2px solid #c7d2fe;
                background:#ffffff;
                color:#1e293b;
                border-radius:16px;
                padding:14px 15px;
                font-size:17px;
                font-weight:900;
                line-height:1.55;
                cursor:pointer;
                box-shadow:0 4px 12px rgba(15,23,42,.06);
                transition:
                    transform .16s ease,
                    background .16s ease,
                    border-color .16s ease,
                    box-shadow .16s ease;
                position:relative;
                overflow:hidden;
            }}

            #{component_id} .match-card:hover {{
                transform:translateY(-2px);
                border-color:#818cf8;
                box-shadow:0 8px 18px rgba(99,102,241,.16);
            }}

            #{component_id} .match-card.selected {{
                background:linear-gradient(135deg,#fef3c7,#fde68a);
                border-color:#f59e0b;
                color:#78350f;
                box-shadow:
                    0 0 0 4px rgba(245,158,11,.18),
                    0 8px 20px rgba(245,158,11,.22);
                transform:scale(1.015);
            }}

            #{component_id} .match-card.wrong {{
                animation:shake_{component_id} .30s ease-in-out;
                background:#fee2e2;
                border-color:#ef4444;
                color:#7f1d1d;
            }}

            /* 정답 카드: 초록빛 + 팝 + 폭발 */
            #{component_id} .match-card.correct {{
                background:linear-gradient(135deg,#dcfce7,#bbf7d0);
                border-color:#22c55e;
                color:#14532d;
                animation:explodeOut_{component_id} .78s ease forwards;
                z-index:5;
            }}

            #{component_id} .match-card.correct::before {{
                content:"";
                position:absolute;
                left:50%;
                top:50%;
                width:24px;
                height:24px;
                transform:translate(-50%,-50%);
                border-radius:50%;
                background:
                    radial-gradient(circle,
                        rgba(255,255,255,1) 0%,
                        rgba(250,204,21,.95) 18%,
                        rgba(251,146,60,.85) 35%,
                        rgba(244,63,94,.55) 52%,
                        rgba(255,255,255,0) 72%);
                animation:burst_{component_id} .78s ease forwards;
                pointer-events:none;
            }}

            #{component_id} .match-card.correct::after {{
                content:"✨ 💥 ✨";
                position:absolute;
                inset:0;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:34px;
                letter-spacing:4px;
                background:
                    radial-gradient(circle,
                        rgba(255,255,255,.98),
                        rgba(255,255,255,.45),
                        rgba(255,255,255,0));
                animation:sparkle_{component_id} .78s ease forwards;
                pointer-events:none;
            }}

            @keyframes explodeOut_{component_id} {{
                0% {{
                    opacity:1;
                    transform:scale(1);
                    max-height:220px;
                }}
                22% {{
                    transform:scale(1.08);
                    box-shadow:
                        0 0 0 8px rgba(34,197,94,.16),
                        0 0 32px rgba(250,204,21,.65);
                }}
                48% {{
                    transform:scale(1.16);
                    opacity:1;
                }}
                72% {{
                    transform:scale(.92) rotate(1deg);
                    opacity:.60;
                    max-height:220px;
                }}
                100% {{
                    transform:scale(.25) rotate(-5deg);
                    opacity:0;
                    max-height:0;
                    padding-top:0;
                    padding-bottom:0;
                    border-width:0;
                    margin:0;
                }}
            }}

            @keyframes burst_{component_id} {{
                0% {{
                    opacity:0;
                    transform:translate(-50%,-50%) scale(.15);
                }}
                28% {{
                    opacity:1;
                    transform:translate(-50%,-50%) scale(2.4);
                }}
                58% {{
                    opacity:.95;
                    transform:translate(-50%,-50%) scale(5);
                }}
                100% {{
                    opacity:0;
                    transform:translate(-50%,-50%) scale(7);
                }}
            }}

            @keyframes sparkle_{component_id} {{
                0% {{
                    opacity:0;
                    transform:scale(.5) rotate(0deg);
                }}
                30% {{
                    opacity:1;
                    transform:scale(1.3) rotate(8deg);
                }}
                60% {{
                    opacity:1;
                    transform:scale(1.65) rotate(-8deg);
                }}
                100% {{
                    opacity:0;
                    transform:scale(2.2) rotate(18deg);
                }}
            }}

            @keyframes shake_{component_id} {{
                0%,100% {{ transform:translateX(0); }}
                25% {{ transform:translateX(-6px); }}
                50% {{ transform:translateX(6px); }}
                75% {{ transform:translateX(-3px); }}
            }}

            #{component_id} .progress-outer {{
                width:100%;
                height:14px;
                background:#e5e7eb;
                border-radius:999px;
                overflow:hidden;
                margin:16px 0 12px;
            }}

            #{component_id} .progress-inner {{
                width:0%;
                height:100%;
                background:linear-gradient(90deg,#60a5fa,#a78bfa,#f472b6);
                border-radius:999px;
                transition:width .28s ease;
            }}

            #{component_id} .reset-btn {{
                width:100%;
                border:1px solid #c7d2fe;
                background:#ffffff;
                color:#4338ca;
                border-radius:999px;
                min-height:46px;
                font-size:16px;
                font-weight:1000;
                cursor:pointer;
            }}

            #{component_id} .reset-btn:hover {{
                background:#eef2ff;
            }}

            #{component_id} .done-message {{
                background:linear-gradient(135deg,#dcfce7,#bbf7d0);
                border:2px solid #22c55e;
                color:#14532d;
                border-radius:16px;
                padding:18px;
                margin-top:16px;
                font-size:20px;
                font-weight:1000;
                text-align:center;
                animation:donePop_{component_id} .45s ease;
            }}

            @keyframes donePop_{component_id} {{
                0% {{ opacity:0; transform:scale(.85); }}
                100% {{ opacity:1; transform:scale(1); }}
            }}

            @media(max-width:720px) {{
                #{component_id} .match-board {{
                    grid-template-columns:1fr;
                }}
                #{component_id} .match-status {{
                    grid-template-columns:1fr;
                }}
                #{component_id} .match-card {{
                    font-size:15px;
                }}
            }}
        </style>

        <script>
            const data_{component_id} = {matching_json};

            const root_{component_id} =
                document.getElementById("{component_id}");

            const enBox_{component_id} =
                document.getElementById("en_{component_id}");

            const koBox_{component_id} =
                document.getElementById("ko_{component_id}");

            const status_{component_id} =
                document.getElementById("status_{component_id}");

            const score_{component_id} =
                document.getElementById("score_{component_id}");

            const bar_{component_id} =
                document.getElementById("bar_{component_id}");

            const reset_{component_id} =
                document.getElementById("reset_{component_id}");

            const doneBox_{component_id} =
                document.getElementById("done_{component_id}");

            let selected_{component_id} = null;
            let completed_{component_id} = new Set();
            let locked_{component_id} = false;

            function escapeHtml_{component_id}(str) {{
                return String(str)
                    .replaceAll("&","&amp;")
                    .replaceAll("<","&lt;")
                    .replaceAll(">","&gt;")
                    .replaceAll('"',"&quot;")
                    .replaceAll("'","&#039;");
            }}

            function makeCard_{component_id}(card, kind) {{
                const btn = document.createElement("button");
                btn.className = "match-card";
                btn.dataset.id = card.id;
                btn.dataset.kind = kind;
                btn.innerHTML = escapeHtml_{component_id}(card.text);

                btn.addEventListener(
                    "click",
                    () => handleClick_{component_id}(btn, card, kind)
                );

                return btn;
            }}

            function render_{component_id}() {{
                enBox_{component_id}.innerHTML = "";
                koBox_{component_id}.innerHTML = "";

                data_{component_id}.en.forEach(card => {{
                    if (!completed_{component_id}.has(card.id)) {{
                        enBox_{component_id}.appendChild(
                            makeCard_{component_id}(card, "en")
                        );
                    }}
                }});

                data_{component_id}.ko.forEach(card => {{
                    if (!completed_{component_id}.has(card.id)) {{
                        koBox_{component_id}.appendChild(
                            makeCard_{component_id}(card, "ko")
                        );
                    }}
                }});

                updateScore_{component_id}();
            }}

            function updateScore_{component_id}() {{
                const count = completed_{component_id}.size;
                const total = data_{component_id}.total;

                score_{component_id}.textContent =
                    "맞춘 개수: " + count + " / " + total;

                bar_{component_id}.style.width =
                    ((count / total) * 100) + "%";

                if (count === total) {{
                    status_{component_id}.textContent =
                        "모든 대사를 맞췄습니다! 🎉";

                    doneBox_{component_id}.style.display = "block";
                }}
            }}

            function clearSelection_{component_id}() {{
                root_{component_id}
                    .querySelectorAll(".match-card.selected")
                    .forEach(el => el.classList.remove("selected"));

                selected_{component_id} = null;
            }}

            function handleClick_{component_id}(el, card, kind) {{
                if (locked_{component_id}) return;
                if (completed_{component_id}.has(card.id)) return;

                // 처음 선택
                if (!selected_{component_id}) {{
                    selected_{component_id} = {{el, card, kind}};
                    el.classList.add("selected");

                    status_{component_id}.textContent =
                        kind === "en"
                        ? "오른쪽에서 알맞은 한국어 뜻을 고르세요."
                        : "왼쪽에서 알맞은 영어 대사를 고르세요.";

                    return;
                }}

                // 같은 카드 다시 누르면 선택 취소
                if (selected_{component_id}.el === el) {{
                    clearSelection_{component_id}();

                    status_{component_id}.textContent =
                        "선택을 취소했습니다. 다시 하나를 고르세요.";

                    return;
                }}

                // 같은 열의 다른 카드 클릭 시 선택 변경
                if (selected_{component_id}.kind === kind) {{
                    selected_{component_id}.el.classList.remove("selected");

                    selected_{component_id} = {{el, card, kind}};
                    el.classList.add("selected");

                    status_{component_id}.textContent =
                        kind === "en"
                        ? "오른쪽에서 알맞은 한국어 뜻을 고르세요."
                        : "왼쪽에서 알맞은 영어 대사를 고르세요.";

                    return;
                }}

                // 정답
                if (
                    selected_{component_id}.card.id === card.id &&
                    selected_{component_id}.kind !== kind
                ) {{
                    locked_{component_id} = true;

                    const firstEl = selected_{component_id}.el;
                    const secondEl = el;
                    const matchedId = card.id;

                    firstEl.classList.remove("selected");
                    secondEl.classList.remove("selected");

                    firstEl.classList.add("correct");
                    secondEl.classList.add("correct");

                    status_{component_id}.textContent =
                        "정답입니다! 💥 두 카드가 터지며 사라집니다.";

                    setTimeout(() => {{
                        completed_{component_id}.add(matchedId);
                        selected_{component_id} = null;
                        locked_{component_id} = false;

                        render_{component_id}();

                        if (
                            completed_{component_id}.size <
                            data_{component_id}.total
                        ) {{
                            status_{component_id}.textContent =
                                "좋아요! 다음 영어 대사를 골라 보세요.";
                        }}
                    }}, 780);

                }} else {{
                    // 오답
                    locked_{component_id} = true;

                    const firstEl = selected_{component_id}.el;
                    const secondEl = el;

                    firstEl.classList.add("wrong");
                    secondEl.classList.add("wrong");

                    status_{component_id}.textContent =
                        "아쉬워요. 다시 짝을 맞춰 보세요. ❌";

                    setTimeout(() => {{
                        firstEl.classList.remove("selected","wrong");
                        secondEl.classList.remove("wrong");

                        selected_{component_id} = null;
                        locked_{component_id} = false;

                        status_{component_id}.textContent =
                            "다시 왼쪽에서 영어 대사를 하나 선택하세요.";
                    }}, 430);
                }}
            }}

            reset_{component_id}.addEventListener("click", () => {{
                selected_{component_id} = null;
                completed_{component_id} = new Set();
                locked_{component_id} = false;

                doneBox_{component_id}.style.display = "none";

                status_{component_id}.textContent =
                    "먼저 왼쪽에서 영어 대사를 하나 선택하세요.";

                render_{component_id}();
            }});

            render_{component_id}();
        </script>
        """,
        height=760,
        scrolling=True
    )

    # HTML component 내부 게임이므로 Streamlit 쪽 진행률은 별도 상태 동기화가 어렵습니다.
    # 사용자가 다른 탭 활동을 계속할 수 있도록 matching 미션은 화면 게임 자체에서 완료 처리합니다.

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
# TAB 5 KEY QUOTES & EXPRESSIONS
# =========================

with tab5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 핵심 대사 & 핵심 표현</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-guide">'
        '영상 속 핵심 대사와 핵심 단어·표현을 한곳에서 확인하세요.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 💬 핵심 대사")

    for line in key_lines:
        st.markdown(f"""
        <div class="line-box">
            <span class="time-tag">{line["time"]}</span><br>
            <b>{line["en"]}</b><br>
            <span class="kor">{line["ko"]}</span><br><br>
            <b>Easy Meaning:</b> {line["easy"]}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔑 핵심 표현")
    st.markdown(
        '<div class="small-guide">'
        '핵심 단어와 표현의 뜻을 확인하고 듣기 버튼으로 발음과 예문을 들어 보세요.'
        '</div>',
        unsafe_allow_html=True
    )

    for i, item in enumerate(key_expressions, start=1):
        st.markdown(f"""
        <div class="line-box">
            <b>{i}. {item["word"]}</b><br>
            <span class="kor">{item["ko"]}</span><br><br>
            <b>Example:</b> {item["example"]}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**🔊 TTS 듣기**")
        show_blank_audio(item["word"])

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
