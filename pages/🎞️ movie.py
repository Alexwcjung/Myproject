import streamlit as st
import streamlit.components.v1 as components
import random
import io
import json
import uuid
import base64
from datetime import datetime, timezone, timedelta
from gtts import gTTS

st.set_page_config(page_title="Batman English Mission", page_icon="🦇", layout="wide")

VIDEO_URL = "https://www.youtube.com/watch?v=U4fhEziQsc8"


# =========================
# TTS
# =========================

@st.cache_data(show_spinner=False)
def make_tts_audio(text):
    safe_text = str(text).strip()
    if not safe_text:
        return b""

    fp = io.BytesIO()
    tts = gTTS(text=safe_text, lang="en", slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def show_tts_audio(text):
    """가로 폭이 짧은 미니 TTS 오디오 플레이어"""
    try:
        audio_bytes = make_tts_audio(text)
        if audio_bytes:
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

            components.html(
                f"""
                <div style="
                    width:320px;
                    max-width:100%;
                    margin:4px 0 10px 0;
                ">
                    <audio
                        controls
                        preload="metadata"
                        style="
                            width:320px;
                            max-width:100%;
                            height:34px;
                            display:block;
                        "
                    >
                        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                    </audio>
                </div>
                """,
                height=48
            )
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

.game-card {
    background: linear-gradient(135deg,#eef2ff,#f8fafc);
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

.cert-box {
    background: linear-gradient(135deg,#fff7ed,#fefce8,#eff6ff);
    border: 2px solid #f59e0b;
    border-radius: 24px;
    padding: 26px;
    margin-top: 18px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(245,158,11,.14);
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

button[kind="primary"] {
    background: #facc15 !important;
    color: #111827 !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 900 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# DATA
# =========================

full_script = [
    {"time": "0:02", "en": "I killed those people. That's what I can be.", "ko": "내가 그 사람들을 죽였어. 나는 그런 사람이 될 수 있어."},
    {"time": "0:09", "en": "No, no. You can't. You're not.", "ko": "아니, 안 돼. 넌 그럴 수 없어. 넌 그런 사람이 아니야."},
    {"time": "0:12", "en": "I'm whatever Gotham needs me to be.", "ko": "나는 고담시가 필요로 하는 무엇이든 될 거야."},
    {"time": "0:16", "en": "A hero. Not the hero we deserved, but the hero we needed.", "ko": "영웅. 우리가 받을 자격이 있던 영웅은 아니지만, 우리에게 필요했던 영웅."},
    {"time": "0:20", "en": "Nothing less than a knight.", "ko": "그는 진정한 기사와 같은 존재야."},
    {"time": "0:28", "en": "You heard me. You can tell them.", "ko": "내 말 들었지. 사람들에게 그렇게 말해."},
    {"time": "0:32", "en": "You set the dogs on me.", "ko": "개들을 나에게 풀어."},
    {"time": "0:37", "en": "The truth isn't good enough.", "ko": "진실만으로는 충분하지 않아."},
    {"time": "0:48", "en": "Sometimes people deserve more.", "ko": "때로 사람들은 더 많은 것을 받을 자격이 있어."},
    {"time": "0:53", "en": "Sometimes people deserve to have their faith rewarded.", "ko": "때로 사람들은 자신의 믿음이 보상받을 자격이 있어."},
    {"time": "1:42", "en": "He's the hero Gotham deserves, but not the one it needs right now.", "ko": "그는 고담시가 받을 자격이 있는 영웅이지만, 지금 고담시에 필요한 영웅은 아니야."},
    {"time": "1:48", "en": "So we'll hunt him.", "ko": "그래서 우리는 그를 쫓을 거야."},
    {"time": "1:52", "en": "Because he can take it.", "ko": "왜냐하면 그는 그것을 감당할 수 있으니까."},
    {"time": "1:56", "en": "Because he's not our hero.", "ko": "왜냐하면 그는 우리의 영웅이 아니니까."},
    {"time": "2:06", "en": "He's a silent guardian, a watchful protector.", "ko": "그는 조용한 수호자이자, 늘 지켜보는 보호자야."}
]

key_lines = [
    {"time": "0:12", "en": "I'm whatever Gotham needs me to be.", "ko": "나는 고담시가 필요로 하는 무엇이든 될 거야.", "easy": "Batman will become what Gotham needs."},
    {"time": "0:16", "en": "Not the hero we deserved, but the hero we needed.", "ko": "우리가 받을 자격이 있던 영웅은 아니지만, 우리에게 필요했던 영웅.", "easy": "Batman is not a perfect public hero, but he is necessary."},
    {"time": "0:37", "en": "The truth isn't good enough.", "ko": "진실만으로는 충분하지 않아.", "easy": "Sometimes truth alone is not enough."},
    {"time": "0:48", "en": "Sometimes people deserve more.", "ko": "때로 사람들은 더 많은 것을 받을 자격이 있다.", "easy": "People sometimes need more than truth."},
    {"time": "0:53", "en": "Sometimes people deserve to have their faith rewarded.", "ko": "때로 사람들은 자신의 믿음이 보상받을 자격이 있다.", "easy": "People's hope should be protected."},
    {"time": "1:42", "en": "He's the hero Gotham deserves, but not the one it needs right now.", "ko": "그는 고담시가 받을 자격이 있는 영웅이지만, 지금 필요한 영웅은 아니다.", "easy": "Batman cannot be the public hero right now."},
    {"time": "1:52", "en": "Because he can take it.", "ko": "왜냐하면 그는 그것을 감당할 수 있으니까.", "easy": "Batman can endure blame."},
    {"time": "2:06", "en": "He's a silent guardian, a watchful protector.", "ko": "그는 조용한 수호자이자, 늘 지켜보는 보호자이다.", "easy": "Batman protects Gotham quietly."}
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
    {"q": "Q1. At first, what do people think Batman is?", "options": ["A hero", "A criminal", "A singer", "A teacher"], "answer": "A criminal"},
    {"q": "Q2. What is Batman really doing?", "options": ["Taking the blame", "Running away", "Making money", "Singing a song"], "answer": "Taking the blame"},
    {"q": "Q3. What kind of person is Batman in this scene?", "options": ["Sacrificing", "Lazy", "Selfish", "Funny"], "answer": "Sacrificing"},
    {"q": "Q4. Why can Batman endure it?", "options": ["Because he can take it", "Because he is tired", "Because he wants money", "Because he forgot"], "answer": "Because he can take it"}
]

blank_questions = [
    {"audio": "I'm whatever Gotham needs me to be.", "sentence": "I'm whatever Gotham ______ me to be.", "options": ["needs", "follows", "remembers"], "answer": "needs"},
    {"audio": "Not the hero we deserved, but the hero we needed.", "sentence": "Not the hero we ______, but the hero we ______.", "options": ["deserved / needed", "found / lost", "saw / followed"], "answer": "deserved / needed"},
    {"audio": "Sometimes people deserve more.", "sentence": "Sometimes people ______ more.", "options": ["deserve", "forget", "hide"], "answer": "deserve"},
    {"audio": "Because he can take it.", "sentence": "Because he can ______ it.", "options": ["take", "find", "change"], "answer": "take"},
    {"audio": "A silent guardian, a watchful protector.", "sentence": "A silent ______, a watchful ______.", "options": ["guardian / protector", "student / teacher", "singer / dancer"], "answer": "guardian / protector"}
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
    {"q": "He can ___ it.", "options": ["take", "takes", "took"], "answer": "take", "explain": "can 뒤에는 동사원형을 씁니다. 그래서 can take가 맞습니다."},
    {"q": "You can't ___ that.", "options": ["do", "does", "did"], "answer": "do", "explain": "can't 뒤에도 동사원형을 씁니다."},
    {"q": "Gotham ___ me.", "options": ["need", "needs", "needed"], "answer": "needs", "explain": "Gotham은 단수 주어이므로 현재시제에서는 needs를 씁니다."},
    {"q": "People deserve ___ more.", "options": ["have", "to have", "having"], "answer": "to have", "explain": "deserve 뒤에 동사가 올 때는 deserve to + 동사 형태를 쓸 수 있습니다."}
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

for mission_name in ["hero"]:
    if f"{mission_name}_attempt" not in st.session_state:
        st.session_state[f"{mission_name}_attempt"] = 0
    if f"{mission_name}_wrong" not in st.session_state:
        st.session_state[f"{mission_name}_wrong"] = []
    if f"{mission_name}_first_correct" not in st.session_state:
        st.session_state[f"{mission_name}_first_correct"] = []

if "blank_phase" not in st.session_state:
    st.session_state.blank_phase = 0

if "blank_wrong" not in st.session_state:
    st.session_state.blank_wrong = []

if "blank_first_correct" not in st.session_state:
    st.session_state.blank_first_correct = []

if "matching_completed_manual" not in st.session_state:
    st.session_state.matching_completed_manual = False

if "student_name" not in st.session_state:
    st.session_state.student_name = ""


# =========================
# HEADER
# =========================

st.markdown('<div class="main-title">🦇 Batman English Mission</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Video-based English Activity · Bright Classroom Version</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-title">Hero or Villain?</div>
    <div class="hero-sub">
        Watch the Batman scene, read the subtitles, answer the missions,
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
# TAB 1 VIDEO
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
            index=None,
            horizontal=False
        )

    if st.session_state.hero_attempt == 0:
        if st.button("Hero or Villain 1차 채점", key="check_hero_first", type="primary"):
            unanswered = [idx for idx in hero_indices if hero_answers.get(idx) is None]

            if unanswered:
                st.warning("모든 문제에 답한 뒤 채점하세요.")
            else:
                wrong = [
                    idx for idx in hero_indices
                    if hero_answers[idx] != hero_questions[idx]["answer"]
                ]
                correct = [idx for idx in hero_indices if idx not in wrong]
                st.session_state.hero_first_correct = correct

                if not wrong:
                    st.session_state.batman_complete["choice"] = True
                    st.session_state.hero_attempt = 2
                    st.rerun()
                else:
                    st.session_state.hero_wrong = wrong
                    st.session_state.hero_attempt = 1
                    st.rerun()

    elif st.session_state.hero_attempt == 1:
        for idx in st.session_state.hero_first_correct:
            st.success(f"{idx + 1}번 정답입니다. ✅")

        if st.button("틀린 문제 다시 채점", key="check_hero_retry", type="primary"):
            unanswered = [idx for idx in hero_indices if hero_answers.get(idx) is None]

            if unanswered:
                st.warning("재도전 문제에 모두 답한 뒤 채점하세요.")
            else:
                still_wrong = [
                    idx for idx in hero_indices
                    if hero_answers[idx] != hero_questions[idx]["answer"]
                ]
                st.session_state.hero_wrong = still_wrong
                st.session_state.hero_attempt = 2
                st.session_state.batman_complete["choice"] = True
                st.rerun()

    else:
        if st.session_state.hero_wrong:
            st.markdown("### 재도전 후 남은 오답")
            for idx in st.session_state.hero_wrong:
                st.write(f"**{hero_questions[idx]['q']}** → 정답: **{hero_questions[idx]['answer']}**")
        else:
            st.markdown('<div class="success-box">🦸 Hero or Villain 미션 완료!</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 2 LINE BLANKS
# =========================

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎧 대사 빈칸</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="game-card"><div class="big-guide">'
        '대사를 듣고 빈칸에 들어갈 말을 고르세요. '
        '틀린 문제는 정답을 바로 보여주지 않고 한 번 더 풀게 됩니다.'
        '</div></div>',
        unsafe_allow_html=True
    )

    blank_indices = (
        st.session_state.blank_wrong
        if st.session_state.blank_phase == 1 and st.session_state.blank_wrong
        else list(range(len(blank_questions)))
    )

    blank_answers = {}

    for idx in blank_indices:
        item = blank_questions[idx]
        st.markdown(f"""
        <div class="line-box">
            <b>{idx + 1}. {item["sentence"]}</b>
        </div>
        """, unsafe_allow_html=True)

        show_tts_audio(item["audio"])

        options = item["options"].copy()
        rng = random.Random(f"batman_blank_{idx}")
        rng.shuffle(options)

        blank_answers[idx] = st.radio(
            "정답을 고르세요.",
            options,
            key=f"blank_{idx}_phase_{st.session_state.blank_phase}",
            index=None,
            label_visibility="collapsed"
        )

    if st.session_state.blank_phase == 0:
        if st.button("대사 빈칸 1차 채점", key="blank_first_check", type="primary"):
            unanswered = [idx for idx in blank_indices if blank_answers.get(idx) is None]

            if unanswered:
                st.warning("모든 문제에 답한 뒤 채점하세요.")
            else:
                wrong = [
                    idx for idx in blank_indices
                    if blank_answers[idx] != blank_questions[idx]["answer"]
                ]
                st.session_state.blank_first_correct = [
                    idx for idx in blank_indices if idx not in wrong
                ]
                st.session_state.blank_wrong = wrong

                if not wrong:
                    st.session_state.blank_phase = 2
                    st.session_state.batman_complete["blank"] = True
                else:
                    st.session_state.blank_phase = 1

                st.rerun()

    elif st.session_state.blank_phase == 1:
        st.markdown("### 1차 결과")
        for idx in st.session_state.blank_first_correct:
            st.success(f"{idx + 1}번 정답입니다. ✅")
        for idx in st.session_state.blank_wrong:
            st.markdown(
                f'<div class="wrong-box"><b>{idx + 1}번</b>은 다시 풀어 보세요. ❌</div>',
                unsafe_allow_html=True
            )

        if st.button("틀린 대사 다시 채점", key="blank_retry_check", type="primary"):
            unanswered = [idx for idx in blank_indices if blank_answers.get(idx) is None]

            if unanswered:
                st.warning("재도전 문제에 모두 답한 뒤 채점하세요.")
            else:
                still_wrong = [
                    idx for idx in blank_indices
                    if blank_answers[idx] != blank_questions[idx]["answer"]
                ]
                st.session_state.blank_wrong = still_wrong
                st.session_state.blank_phase = 2
                st.session_state.batman_complete["blank"] = True
                st.rerun()

    else:
        if st.session_state.blank_wrong:
            st.markdown("### 재도전 후 남은 오답")
            for idx in st.session_state.blank_wrong:
                st.write(
                    f"**{idx + 1}번 정답:** "
                    f"**{blank_questions[idx]['answer']}**"
                )
        else:
            st.markdown('<div class="success-box">🎧 대사 빈칸 미션 완료!</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 3 MATCHING
# =========================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 대사 연결</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-guide">'
        '왼쪽 영어 대사를 하나 클릭하고, 오른쪽에서 알맞은 한국어 뜻을 하나 클릭하세요. '
        '모든 카드가 사라지면 아래 완료 버튼을 누르세요.'
        '</div>',
        unsafe_allow_html=True
    )

    matching_pairs = [
        {"id": f"pair_{i}", "en": en, "ko": ko}
        for i, (en, ko) in enumerate(correct_map.items(), start=1)
    ]

    en_cards = [{"id": p["id"], "text": p["en"]} for p in matching_pairs]
    ko_cards = [{"id": p["id"], "text": p["ko"]} for p in matching_pairs]

    random.Random("batman_match_en").shuffle(en_cards)
    random.Random("batman_match_ko").shuffle(ko_cards)

    matching_json = json.dumps(
        {"en": en_cards, "ko": ko_cards, "total": len(matching_pairs)},
        ensure_ascii=False
    )

    component_id = "batman_match_" + uuid.uuid4().hex

    components.html(
        f"""
        <div id="{component_id}" class="match-app">
            <div class="match-status">
                <div id="status_{component_id}">먼저 왼쪽에서 영어 대사를 하나 선택하세요.</div>
                <div id="score_{component_id}">맞춘 개수: 0 / {len(matching_pairs)}</div>
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

            <button id="reset_{component_id}" class="reset-btn">🔄 매칭 다시 시작</button>
            <div id="done_{component_id}" class="done-message" style="display:none;">
                🎉 모든 대사를 맞췄습니다! 아래의 '대사 연결 완료' 버튼을 눌러 주세요.
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
            transition:.16s ease;
            position:relative;
            overflow:hidden;
        }}

        #{component_id} .match-card.selected {{
            background:linear-gradient(135deg,#fef3c7,#fde68a);
            border-color:#f59e0b;
        }}

        #{component_id} .match-card.wrong {{
            animation:shake_{component_id} .30s ease-in-out;
            background:#fee2e2;
            border-color:#ef4444;
        }}

        #{component_id} .match-card.correct {{
            background:linear-gradient(135deg,#dcfce7,#bbf7d0);
            border-color:#22c55e;
            animation:explodeOut_{component_id} .78s ease forwards;
            z-index:5;
        }}

        #{component_id} .match-card.correct::after {{
            content:"✨ 💥 ✨";
            position:absolute;
            inset:0;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:34px;
            background:radial-gradient(circle,rgba(255,255,255,.98),rgba(255,255,255,.45),rgba(255,255,255,0));
            animation:sparkle_{component_id} .78s ease forwards;
        }}

        @keyframes explodeOut_{component_id} {{
            0% {{opacity:1; transform:scale(1); max-height:220px;}}
            25% {{transform:scale(1.10);}}
            60% {{opacity:1; transform:scale(1.18);}}
            100% {{opacity:0; transform:scale(.25); max-height:0; padding:0; border-width:0; margin:0;}}
        }}

        @keyframes sparkle_{component_id} {{
            0% {{opacity:0; transform:scale(.5);}}
            35% {{opacity:1; transform:scale(1.35);}}
            100% {{opacity:0; transform:scale(2.2);}}
        }}

        @keyframes shake_{component_id} {{
            0%,100% {{transform:translateX(0);}}
            25% {{transform:translateX(-6px);}}
            50% {{transform:translateX(6px);}}
            75% {{transform:translateX(-3px);}}
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
        }}
        </style>

        <script>
        const data = {matching_json};
        const root = document.getElementById("{component_id}");
        const enBox = document.getElementById("en_{component_id}");
        const koBox = document.getElementById("ko_{component_id}");
        const status = document.getElementById("status_{component_id}");
        const score = document.getElementById("score_{component_id}");
        const bar = document.getElementById("bar_{component_id}");
        const doneBox = document.getElementById("done_{component_id}");
        const resetBtn = document.getElementById("reset_{component_id}");

        let selected = null;
        let completed = new Set();
        let locked = false;

        function makeCard(card, kind) {{
            const btn = document.createElement("button");
            btn.className = "match-card";
            btn.textContent = card.text;
            btn.onclick = () => handleClick(btn, card, kind);
            return btn;
        }}

        function render() {{
            enBox.innerHTML = "";
            koBox.innerHTML = "";

            data.en.forEach(card => {{
                if (!completed.has(card.id)) enBox.appendChild(makeCard(card, "en"));
            }});

            data.ko.forEach(card => {{
                if (!completed.has(card.id)) koBox.appendChild(makeCard(card, "ko"));
            }});

            const count = completed.size;
            score.textContent = "맞춘 개수: " + count + " / " + data.total;
            bar.style.width = ((count / data.total) * 100) + "%";

            if (count === data.total) {{
                doneBox.style.display = "block";
                status.textContent = "모든 대사를 맞췄습니다! 🎉";
            }}
        }}

        function clearSelected() {{
            root.querySelectorAll(".selected").forEach(x => x.classList.remove("selected"));
            selected = null;
        }}

        function handleClick(el, card, kind) {{
            if (locked) return;

            if (!selected) {{
                selected = {{el, card, kind}};
                el.classList.add("selected");
                status.textContent = kind === "en"
                    ? "오른쪽에서 알맞은 한국어 뜻을 고르세요."
                    : "왼쪽에서 알맞은 영어 대사를 고르세요.";
                return;
            }}

            if (selected.el === el) {{
                clearSelected();
                return;
            }}

            if (selected.kind === kind) {{
                selected.el.classList.remove("selected");
                selected = {{el, card, kind}};
                el.classList.add("selected");
                return;
            }}

            if (selected.card.id === card.id) {{
                locked = true;
                const firstEl = selected.el;
                const secondEl = el;
                const matchedId = card.id;

                firstEl.classList.remove("selected");
                firstEl.classList.add("correct");
                secondEl.classList.add("correct");

                setTimeout(() => {{
                    completed.add(matchedId);
                    selected = null;
                    locked = false;
                    render();
                }}, 780);

            }} else {{
                locked = true;
                const firstEl = selected.el;
                const secondEl = el;

                firstEl.classList.add("wrong");
                secondEl.classList.add("wrong");

                setTimeout(() => {{
                    firstEl.classList.remove("selected","wrong");
                    secondEl.classList.remove("wrong");
                    selected = null;
                    locked = false;
                }}, 430);
            }}
        }}

        resetBtn.onclick = () => {{
            selected = null;
            completed = new Set();
            locked = false;
            doneBox.style.display = "none";
            render();
        }};

        render();
        </script>
        """,
        height=760,
        scrolling=True
    )

    if st.session_state.batman_complete["matching"]:
        st.markdown('<div class="success-box">🧩 대사 연결 미션 완료!</div>', unsafe_allow_html=True)
    else:
        if st.button("✅ 대사 연결 완료", key="matching_finish", type="primary"):
            st.session_state.batman_complete["matching"] = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 4 GRAMMAR
# =========================

with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📘 문법</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-guide">'
        '문제는 항상 그대로 유지됩니다. 답을 고르고 채점하면 각 문제 아래에 '
        '정답 또는 오답만 표시됩니다. 정답 자체는 공개하지 않습니다. '
        '오답은 답을 바꿔 다시 채점할 수 있습니다.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="line-box">
        <b>Look at these lines.</b><br><br>
        1. He <b>can take</b> it.<br>
        2. You <b>can't do</b> that.<br>
        3. Gotham <b>needs</b> me.<br>
        4. People deserve <b>to have</b> more.
    </div>
    """, unsafe_allow_html=True)

    if "grammar_status" not in st.session_state:
        st.session_state.grammar_status = [None] * len(grammar_questions)

    grammar_answers = {}

    # 모든 문제를 항상 그대로 표시
    for idx, item in enumerate(grammar_questions):
        st.markdown(f"**Q{idx + 1}. {item['q']}**")

        grammar_answers[idx] = st.radio(
            "하나를 고르세요.",
            item["options"],
            key=f"grammar_fixed_{idx}",
            index=None,
            horizontal=True
        )

        # 채점 결과만 문제 바로 아래 표시
        if st.session_state.grammar_status[idx] is True:
            st.success("정답입니다. ✅")

        elif st.session_state.grammar_status[idx] is False:
            st.error("오답입니다. ❌ 다시 생각해 보세요.")

        st.write("")

    if st.button(
        "문법 채점",
        key="check_grammar_fixed",
        type="primary"
    ):
        unanswered = [
            idx
            for idx in range(len(grammar_questions))
            if grammar_answers.get(idx) is None
        ]

        if unanswered:
            st.warning(
                "모든 문제에 답한 뒤 채점하세요. "
                f"선택하지 않은 문제: {', '.join(str(i + 1) for i in unanswered)}번"
            )

        else:
            for idx, item in enumerate(grammar_questions):
                st.session_state.grammar_status[idx] = (
                    grammar_answers[idx] == item["answer"]
                )

            if all(st.session_state.grammar_status):
                st.session_state.batman_complete["grammar"] = True
            else:
                st.session_state.batman_complete["grammar"] = False

            st.rerun()

    # 모두 맞힌 경우에만 완료 메시지
    if all(status is True for status in st.session_state.grammar_status):
        st.markdown("""
        <div class="success-box">
            📘 모든 문법 문제를 맞혔습니다! 문법 미션 완료! 🎉
        </div>
        """, unsafe_allow_html=True)

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
# TAB 5 KEY LINES & EXPRESSIONS
# =========================

with tab5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 핵심 대사 & 핵심 표현</div>', unsafe_allow_html=True)

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

    for i, item in enumerate(key_expressions, start=1):
        st.markdown(f"""
        <div class="line-box">
            <b>{i}. {item["word"]}</b><br>
            <span class="kor">{item["ko"]}</span><br><br>
            <b>Example:</b> {item["example"]}
        </div>
        """, unsafe_allow_html=True)

        st.caption("🔊 TTS 듣기")
        show_tts_audio(item["word"])

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# FINAL STATUS + CERTIFICATE
# =========================

st.markdown("---")

completed_count = sum(st.session_state.batman_complete.values())

if completed_count == 4:
    st.markdown("""
    <div class="success-box">
        🦇 모든 배트맨 영어 미션을 완성했습니다!<br>
        You are Gotham's English Guardian!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏆 인증서 발급")

    student_name = st.text_input(
        "이름을 입력하세요.",
        value=st.session_state.student_name,
        key="certificate_name_input",
        placeholder="예: 홍길동"
    )

    if student_name.strip():
        st.session_state.student_name = student_name.strip()

        korea_tz = timezone(timedelta(hours=9))
        issue_date = datetime.now(korea_tz).strftime("%Y-%m-%d")

        certificate_text = f"""
============================================================
                BATMAN ENGLISH MISSION
                  CERTIFICATE
============================================================

This certificate is proudly presented to

{student_name.strip()}

for successfully completing all four
Batman English Missions:

1. Hero or Villain
2. Line Blanks
3. Quote Matching
4. Grammar Discovery

You are Gotham's English Guardian!

Issued on: {issue_date}

============================================================
"""

        st.markdown(f"""
        <div class="cert-box">
            <div style="font-size:34px;font-weight:1000;">🏆 Certificate of Completion</div>
            <div style="font-size:20px;margin-top:16px;">This certificate is proudly presented to</div>
            <div style="font-size:32px;font-weight:1000;margin:14px 0;">{student_name.strip()}</div>
            <div style="font-size:18px;line-height:1.8;">
                for successfully completing all four<br>
                <b>Batman English Missions</b><br><br>
                🦇 You are Gotham's English Guardian!
            </div>
            <div style="margin-top:18px;color:#6b7280;">Issued on {issue_date}</div>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            label="📥 인증서 다운로드",
            data=certificate_text.encode("utf-8"),
            file_name=f"Batman_English_Certificate_{student_name.strip()}.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )

    else:
        st.info("이름을 입력하면 인증서 미리보기와 다운로드 버튼이 나타납니다.")

else:
    st.markdown(f"""
    <div class="line-box">
        <b>Mission Progress:</b> {completed_count} / 4 completed<br>
        <span class="kor">4개의 미션을 모두 완료하면 인증서를 발급할 수 있습니다.</span>
    </div>
    """, unsafe_allow_html=True)
