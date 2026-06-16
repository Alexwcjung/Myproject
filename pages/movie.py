import streamlit as st
import streamlit.components.v1 as components

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
# CSS - BRIGHT CLASSROOM STYLE
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
        "time": "0:48",
        "en": "Sometimes people deserve more.",
        "ko": "때로 사람들은 더 많은 것을 받을 자격이 있다.",
        "easy": "People sometimes need hope, not only truth."
    },
    {
        "time": "0:57",
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

# 정답을 뒤쪽 번호에 오도록 선택지 순서를 조정함
blank_questions = [
    {
        "audio": "I'm whatever Gotham needs me to be.",
        "sentence": "I'm whatever Gotham ______ me to be.",
        "options": ["need", "needed", "needs"],
        "answer": "needs"
    },
    {
        "audio": "Not the hero we deserved, but the hero we needed.",
        "sentence": "Not the hero we ______, but the hero we ______.",
        "options": ["need / deserve", "needs / deserved", "deserved / needed"],
        "answer": "deserved / needed"
    },
    {
        "audio": "Sometimes people deserve more.",
        "sentence": "Sometimes people ______ more.",
        "options": ["deserves", "deserved", "deserve"],
        "answer": "deserve"
    },
    {
        "audio": "Because he can take it.",
        "sentence": "Because he can ______ it.",
        "options": ["takes", "took", "take"],
        "answer": "take"
    },
    {
        "audio": "A silent guardian, a watchful protector.",
        "sentence": "A silent ______, a watchful ______.",
        "options": ["student / teacher", "singer / dancer", "guardian / protector"],
        "answer": "guardian / protector"
    }
]

correct_map = {
    "I'm whatever Gotham needs me to be.": "나는 고담시가 필요로 하는 무엇이든 될 거야.",
    "Not the hero we deserved.": "우리가 받을 자격이 있던 영웅은 아니다.",
    "The hero we needed.": "우리에게 필요했던 영웅.",
    "Sometimes people deserve more.": "때로 사람들은 더 많은 것을 받을 자격이 있다.",
    "Because he can take it.": "왜냐하면 그는 그것을 감당할 수 있으니까.",
    "A silent guardian.": "조용한 수호자.",
    "A watchful protector.": "늘 지켜보는 보호자."
}

story_order_options = {
    "A": "Batman decides to take the blame.",
    "B": "People think Batman is bad.",
    "C": "Gotham starts to hunt Batman.",
    "D": "Batman still protects Gotham.",
    "E": "Batman becomes a silent guardian."
}

story_order_answer = "ABCDE"

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
        "order": False,
        "grammar": False
    }

if "selected_match" not in st.session_state:
    st.session_state.selected_match = None

if "matched_pairs" not in st.session_state:
    st.session_state.matched_pairs = set()


# =========================
# HEADER
# =========================

st.markdown('<div class="main-title">🦇 Batman English Mission</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Video-based English Activity · Bright Classroom Version</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-title">Hero or Villain?</div>
    <div class="hero-sub">
        Watch the Batman scene and complete five missions: choose Batman's role, listen and fill in key lines,
        match quotes, arrange the story, and discover grammar rules.
        <br>
        <span class="kor">배트맨 장면을 보고 5개의 영어 미션을 완성해 봅시다.</span>
    </div>
</div>
""", unsafe_allow_html=True)

completed_count = sum(st.session_state.batman_complete.values())

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f"<span class='badge'>Choice {'✅' if st.session_state.batman_complete['choice'] else '⬜'}</span>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<span class='badge'>Blanks {'✅' if st.session_state.batman_complete['blank'] else '⬜'}</span>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<span class='badge'>Matching {'✅' if st.session_state.batman_complete['matching'] else '⬜'}</span>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<span class='badge'>Order {'✅' if st.session_state.batman_complete['order'] else '⬜'}</span>", unsafe_allow_html=True)
with c5:
    st.markdown(f"<span class='badge'>Grammar {'✅' if st.session_state.batman_complete['grammar'] else '⬜'}</span>", unsafe_allow_html=True)

st.progress(completed_count / 5)


# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎬 Video",
    "🦸 Hero or Villain",
    "🎧 Line Blanks",
    "💬 Quotes",
    "🧩 Quote Matching",
    "🕵️ Story Order",
    "📘 Grammar"
])


# =========================
# TAB 1 VIDEO
# =========================

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎬 Watch the Video</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상을 보고 배트맨이 왜 나쁜 사람처럼 보이는 선택을 하는지 생각해 봅시다.</div>', unsafe_allow_html=True)

    st.video(VIDEO_URL)

    st.markdown("""
    <div class="line-box">
        <b>Today's Question</b><br>
        Is Batman a hero, a villain, or both?
        <br>
        <span class="kor">오늘의 질문: 배트맨은 영웅인가, 악당인가, 아니면 둘 다인가?</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 2 HERO OR VILLAIN
# =========================

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🦸 Hero or Villain?</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">질문은 영어와 한국어를 함께 읽고 고르세요. 3문제 이상 맞히면 성공입니다.</div>', unsafe_allow_html=True)

    choice_score = 0

    for i, item in enumerate(hero_questions, start=1):
        st.markdown(f"**{item['q']}**")
        user_answer = st.radio(
            "Choose one.",
            item["options"],
            key=f"hero_{i}",
            horizontal=False
        )

        if user_answer == item["answer"]:
            choice_score += 1

        st.write("")

    if st.button("Hero or Villain 채점하기", key="check_hero", type="primary"):
        st.markdown(f"### 점수: {choice_score} / {len(hero_questions)}")

        if choice_score >= 3:
            st.session_state.batman_complete["choice"] = True
            st.markdown("""
            <div class="success-box">
                🦸 Hero or Villain 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                다시 생각해 봅시다. Batman은 왜 비난을 감당하려 했을까요?
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 3 LINE BLANKS WITH LISTENING BUTTON
# =========================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎧 Line Blanks</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">각 문장의 듣기 버튼을 누르고, 빈칸에 들어갈 말을 고르세요. 4개 이상 맞히면 성공입니다.</div>', unsafe_allow_html=True)

    blank_score = 0

    for i, item in enumerate(blank_questions, start=1):
        st.markdown(f"""
        <div class="mission-box">
            <b>Q{i}. Listen and choose.</b><br><br>
            <b>{item["sentence"]}</b>
        </div>
        """, unsafe_allow_html=True)

        speak_button(item["audio"], f"blank_{i}")

        user_answer = st.radio(
            "Choose one.",
            item["options"],
            key=f"blank_{i}",
            horizontal=True
        )

        if user_answer == item["answer"]:
            blank_score += 1

        st.write("")

    if st.button("빈칸 채점하기", key="check_blank", type="primary"):
        st.markdown(f"### 점수: {blank_score} / {len(blank_questions)}")

        if blank_score >= 4:
            st.session_state.batman_complete["blank"] = True
            st.markdown("""
            <div class="success-box">
                🎧 대사 빈칸 채우기 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                조금만 더! 듣기 버튼을 다시 누르고 핵심 대사를 확인해 봅시다.
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 4 QUOTES
# =========================

with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Key Quotes</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상 속 핵심 대사와 쉬운 뜻을 확인하세요.</div>', unsafe_allow_html=True)

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
# TAB 5 QUOTE MATCHING - POP SONG STYLE
# =========================

with tab5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 Quote Matching</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">먼저 영어 또는 한국어 박스를 하나 선택하세요. 그다음 짝이 되는 박스를 선택하세요.</div>', unsafe_allow_html=True)

    def handle_match_click(text, side):
        selected = st.session_state.selected_match

        if selected is None:
            st.session_state.selected_match = {"text": text, "side": side}
            return

        if selected["side"] == side:
            st.session_state.selected_match = {"text": text, "side": side}
            return

        first_text = selected["text"]
        second_text = text

        if selected["side"] == "en":
            en_text = first_text
            ko_text = second_text
        else:
            en_text = second_text
            ko_text = first_text

        if en_text in correct_map and correct_map[en_text] == ko_text:
            st.session_state.matched_pairs.add(en_text)
            st.session_state.selected_match = None
            st.toast("정답입니다!", icon="✅")
        else:
            st.session_state.selected_match = None
            st.toast("다시 시도해 보세요!", icon="❌")

    top1, top2 = st.columns([2, 1])

    with top1:
        if st.session_state.selected_match:
            selected_text = st.session_state.selected_match["text"]
            st.markdown(f"""
            <div class="info-box">
                선택됨: {selected_text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                먼저 영어 또는 한국어 박스를 하나 선택하세요.
            </div>
            """, unsafe_allow_html=True)

    with top2:
        st.markdown(f"""
        <div class="info-box">
            맞춘 개수: {len(st.session_state.matched_pairs)} / {len(correct_map)}
        </div>
        """, unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    english_list = list(correct_map.keys())
    korean_list = list(correct_map.values())

    with left_col:
        st.markdown("### English")

        for i, en in enumerate(english_list, start=1):
            is_done = en in st.session_state.matched_pairs
            label = f"✅ {en}" if is_done else en

            clicked = st.button(
                label,
                key=f"en_match_{i}",
                use_container_width=True,
                disabled=is_done
            )

            if clicked:
                handle_match_click(en, "en")
                st.rerun()

    with right_col:
        st.markdown("### Korean")

        for i, ko in enumerate(korean_list, start=1):
            matched_english = None

            for en, correct_ko in correct_map.items():
                if correct_ko == ko:
                    matched_english = en

            is_done = matched_english in st.session_state.matched_pairs
            label = f"✅ {ko}" if is_done else ko

            clicked = st.button(
                label,
                key=f"ko_match_{i}",
                use_container_width=True,
                disabled=is_done
            )

            if clicked:
                handle_match_click(ko, "ko")
                st.rerun()

    if len(st.session_state.matched_pairs) >= 6:
        st.session_state.batman_complete["matching"] = True
        st.markdown("""
        <div class="success-box">
            🧩 Quote Matching 임무를 완성하셨습니다!
        </div>
        """, unsafe_allow_html=True)

    if st.button("매칭 다시 하기", key="reset_matching", type="primary"):
        st.session_state.selected_match = None
        st.session_state.matched_pairs = set()
        st.session_state.batman_complete["matching"] = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 6 STORY ORDER - A B C D E INPUT
# =========================

with tab6:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🕵️ Story Order Mission</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">아래 영어 문장 A-E를 보고, 이야기 순서대로 알파벳을 입력하세요. 예: ABCDE</div>', unsafe_allow_html=True)

    st.markdown("### Story Cards")

    for letter, sentence in story_order_options.items():
        st.markdown(f"""
        <div class="order-card">
            <span class="choice-letter">{letter}</span>
            <b>{sentence}</b>
        </div>
        """, unsafe_allow_html=True)

    user_order = st.text_input(
        "정답 순서를 입력하세요. 예: ABCDE",
        max_chars=5,
        key="story_order_input"
    ).strip().upper().replace(" ", "").replace(",", "")

    if st.button("Story Order 채점하기", key="check_order", type="primary"):
        if user_order == story_order_answer:
            st.session_state.batman_complete["order"] = True
            st.markdown("""
            <div class="success-box">
                🕵️ Story Order 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="fail-box">
                다시 생각해 봅시다. 입력한 답: {user_order}
            </div>
            """, unsafe_allow_html=True)

    with st.expander("정답 순서 보기"):
        st.write("A → B → C → D → E")
        for letter, sentence in story_order_options.items():
            st.write(f"{letter}. {sentence}")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 7 GRAMMAR
# =========================

with tab7:
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

    grammar_score = 0

    for i, item in enumerate(grammar_questions, start=1):
        st.markdown(f"**Q{i}. {item['q']}**")
        user_answer = st.radio(
            "Choose one.",
            item["options"],
            key=f"grammar_{i}",
            horizontal=True
        )

        if user_answer == item["answer"]:
            grammar_score += 1

        with st.expander("해설 보기"):
            st.write(item["explain"])

        st.write("")

    if st.button("Grammar 채점하기", key="check_grammar", type="primary"):
        st.markdown(f"### 점수: {grammar_score} / {len(grammar_questions)}")

        if grammar_score == len(grammar_questions):
            st.session_state.batman_complete["grammar"] = True
            st.markdown("""
            <div class="success-box">
                📘 Grammar 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                거의 다 왔습니다! can/can't + 동사원형 규칙을 다시 확인하세요.
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
# FINAL STATUS
# =========================

st.markdown("---")

completed_count = sum(st.session_state.batman_complete.values())

if completed_count == 5:
    st.markdown("""
    <div class="success-box">
        🦇 모든 배트맨 영어 미션을 완성하셨습니다!  
        You are Gotham's English Guardian!
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="line-box">
        <b>Mission Progress:</b> {completed_count} / 5 completed<br>
        <span class="kor">아직 완료하지 않은 미션을 마저 해결하세요.</span>
    </div>
    """, unsafe_allow_html=True)
