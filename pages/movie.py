import streamlit as st
import random

st.set_page_config(page_title="Batman English Mission", page_icon="🦇", layout="wide")

VIDEO_URL = "https://www.youtube.com/watch?v=U4fhEziQsc8"

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: #f9fafb;
}

.main-title {
    font-size: 46px;
    font-weight: 1000;
    color: #facc15;
    margin-bottom: 4px;
}

.sub-title {
    font-size: 17px;
    color: #d1d5db;
    margin-bottom: 24px;
}

.hero-box {
    background: linear-gradient(135deg,#111827 0%,#1f2937 50%,#92400e 100%);
    border: 1px solid #374151;
    border-radius: 28px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.45);
}

.hero-title {
    font-size: 31px;
    font-weight: 1000;
    color: #facc15;
    margin-bottom: 8px;
}

.hero-sub {
    font-size: 17px;
    color: #e5e7eb;
    line-height: 1.7;
}

.section-card {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 24px;
    padding: 24px;
    margin: 18px 0;
    box-shadow: 0 6px 22px rgba(0,0,0,0.35);
}

.section-title {
    font-size: 26px;
    font-weight: 900;
    color: #facc15;
    margin-bottom: 10px;
}

.small-guide {
    color: #d1d5db;
    font-size: 15px;
    margin-bottom: 14px;
}

.line-box {
    background: #1f2937;
    border: 1px solid #4b5563;
    border-radius: 18px;
    padding: 18px;
    line-height: 1.8;
    font-size: 17px;
    margin-bottom: 12px;
}

.kor {
    color: #d1d5db;
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
    background: #064e3b;
    border: 1px solid #34d399;
    border-radius: 18px;
    padding: 16px;
    color: #d1fae5;
    font-weight: 900;
    margin-top: 14px;
}

.fail-box {
    background: #7f1d1d;
    border: 1px solid #fca5a5;
    border-radius: 18px;
    padding: 16px;
    color: #fee2e2;
    font-weight: 900;
    margin-top: 14px;
}

.exp-box {
    background: #1f2937;
    border: 1px solid #facc15;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
}

.exp-title {
    font-size: 18px;
    font-weight: 900;
    color: #fde68a;
}

.exp-meaning {
    color: #e5e7eb;
    font-size: 15px;
    margin-top: 4px;
}

.mission-box {
    background: #0f172a;
    border: 1px solid #475569;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 12px;
}

.badge {
    display:inline-block;
    background:#facc15;
    color:#111827;
    padding:5px 10px;
    border-radius:999px;
    font-size:13px;
    font-weight:900;
    margin-right:6px;
}

div[data-testid="stRadio"] label {
    color: #f9fafb !important;
}

div[data-testid="stSelectbox"] label {
    color: #f9fafb !important;
}

.stButton button {
    background: #facc15;
    color: #111827;
    border: none;
    border-radius: 14px;
    font-weight: 900;
    padding: 0.6rem 1.2rem;
}

.stButton button:hover {
    background: #fde68a;
    color: #111827;
}
</style>
""", unsafe_allow_html=True)


# =========================
# DATA
# =========================

lines = [
    {
        "time": "0:00",
        "en": "I killed those people. That's what I can be.",
        "ko": "내가 그 사람들을 죽였어. 나는 그런 사람이 될 수 있어.",
        "simple": "Batman says he can take the blame."
    },
    {
        "time": "0:09",
        "en": "No, you can't. You're not.",
        "ko": "아니, 넌 그럴 수 없어. 넌 그런 사람이 아니야.",
        "simple": "Someone says Batman is not a bad person."
    },
    {
        "time": "0:12",
        "en": "I'm whatever Gotham needs me to be.",
        "ko": "나는 고담시가 필요로 하는 무엇이든 될 거야.",
        "simple": "Batman will become what Gotham needs."
    },
    {
        "time": "0:16",
        "en": "A hero. Not the hero we deserved, but the hero we needed.",
        "ko": "영웅. 우리가 받을 자격이 있던 영웅은 아니지만, 우리에게 필요했던 영웅.",
        "simple": "Batman is the hero Gotham needs."
    },
    {
        "time": "0:48",
        "en": "Sometimes people deserve more.",
        "ko": "때로 사람들은 더 많은 것을 받을 자격이 있다.",
        "simple": "People sometimes need more than truth."
    },
    {
        "time": "0:57",
        "en": "Sometimes people deserve to have their faith rewarded.",
        "ko": "때로 사람들은 자신의 믿음이 보상받을 자격이 있다.",
        "simple": "People's hope should be rewarded."
    },
    {
        "time": "1:42",
        "en": "He's the hero Gotham deserves, but not the one it needs right now.",
        "ko": "그는 고담시가 받을 자격이 있는 영웅이지만, 지금 필요한 영웅은 아니다.",
        "simple": "Batman cannot be seen as the public hero now."
    },
    {
        "time": "1:52",
        "en": "Because he can take it.",
        "ko": "왜냐하면 그는 그것을 견딜 수 있으니까.",
        "simple": "Batman can endure blame."
    },
    {
        "time": "2:06",
        "en": "He's a silent guardian, a watchful protector.",
        "ko": "그는 조용한 수호자이자, 늘 지켜보는 보호자이다.",
        "simple": "Batman protects Gotham quietly."
    }
]

quiz_questions = [
    {
        "q": "What does Batman say he can be?",
        "options": [
            "Whatever Gotham needs him to be",
            "A singer",
            "A student",
            "A police officer only"
        ],
        "answer": "Whatever Gotham needs him to be",
        "explain": "Batman says, 'I'm whatever Gotham needs me to be.'"
    },
    {
        "q": "What kind of hero is Batman in this scene?",
        "options": [
            "The hero Gotham needs",
            "The hero who wants money",
            "The hero who gives up",
            "The hero who runs away"
        ],
        "answer": "The hero Gotham needs",
        "explain": "The line says, 'Not the hero we deserved, but the hero we needed.'"
    },
    {
        "q": "What does Batman decide to take?",
        "options": [
            "Blame",
            "A prize",
            "A vacation",
            "A new car"
        ],
        "answer": "Blame",
        "explain": "Batman chooses to be hunted because he can take it."
    },
    {
        "q": "Which word is closest to 'protector'?",
        "options": [
            "Guardian",
            "Enemy",
            "Singer",
            "Runner"
        ],
        "answer": "Guardian",
        "explain": "A guardian is someone who protects others."
    },
    {
        "q": "What is the mood of this scene?",
        "options": [
            "Dark and heroic",
            "Funny and silly",
            "Bright and romantic",
            "Lazy and boring"
        ],
        "answer": "Dark and heroic",
        "explain": "The scene shows sacrifice, blame, and heroism."
    }
]

key_expressions = [
    {
        "exp": "whatever Gotham needs me to be",
        "meaning": "고담시가 내가 되기를 필요로 하는 무엇이든",
        "point": "whatever는 '무엇이든'이라는 뜻입니다."
    },
    {
        "exp": "the hero we needed",
        "meaning": "우리에게 필요했던 영웅",
        "point": "needed는 need의 과거형입니다."
    },
    {
        "exp": "deserve",
        "meaning": "~을 받을 자격이 있다",
        "point": "deserve 뒤에는 명사나 to부정사가 올 수 있습니다."
    },
    {
        "exp": "take it",
        "meaning": "그것을 견디다 / 감당하다",
        "point": "여기서 take는 '받아들이다, 견디다'에 가깝습니다."
    },
    {
        "exp": "silent guardian",
        "meaning": "조용한 수호자",
        "point": "silent는 '조용한', guardian은 '수호자'입니다."
    },
    {
        "exp": "watchful protector",
        "meaning": "늘 지켜보는 보호자",
        "point": "watchful은 '주의 깊게 지켜보는'이라는 뜻입니다."
    }
]

matching_items = [
    ("I'm whatever Gotham needs me to be.", "나는 고담시가 필요로 하는 무엇이든 될 거야."),
    ("Not the hero we deserved.", "우리가 받을 자격이 있던 영웅은 아니다."),
    ("The hero we needed.", "우리에게 필요했던 영웅."),
    ("Sometimes people deserve more.", "때로 사람들은 더 많은 것을 받을 자격이 있다."),
    ("Because he can take it.", "왜냐하면 그는 그것을 견딜 수 있으니까."),
    ("A silent guardian.", "조용한 수호자.")
]

order_answer = [
    "Batman takes the blame.",
    "People think he is not a hero.",
    "Gotham hunts him.",
    "But he still protects Gotham.",
    "He becomes a silent guardian."
]

grammar_questions = [
    {
        "q": "I'm whatever Gotham ___ me to be.",
        "options": ["need", "needs", "needed"],
        "answer": "needs",
        "explain": "Gotham은 단수 주어이므로 현재시제에서 needs를 씁니다."
    },
    {
        "q": "The hero we ___.",
        "options": ["need", "needed", "needs"],
        "answer": "needed",
        "explain": "영상에서는 과거의 상황을 말하므로 needed를 씁니다."
    },
    {
        "q": "Sometimes people deserve ___ more.",
        "options": ["have", "to have", "having"],
        "answer": "to have",
        "explain": "deserve 뒤에 동사가 올 때는 to + 동사 형태를 쓸 수 있습니다."
    },
    {
        "q": "He can ___ it.",
        "options": ["take", "takes", "took"],
        "answer": "take",
        "explain": "can 뒤에는 동사원형 take를 씁니다."
    }
]


# =========================
# SESSION STATE
# =========================

if "mission_complete" not in st.session_state:
    st.session_state.mission_complete = {
        "quiz": False,
        "key": False,
        "matching": False,
        "order": False,
        "grammar": False
    }

if "order_options" not in st.session_state:
    temp = order_answer.copy()
    random.shuffle(temp)
    st.session_state.order_options = temp


# =========================
# HEADER
# =========================

st.markdown('<div class="main-title">🦇 Batman English Mission</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Video-based English Activity · No Writing Task</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-title">The Dark Knight: Hero or Outlaw?</div>
    <div class="hero-sub">
        Watch the scene, understand Batman's sacrifice, learn powerful expressions, 
        match sentences, arrange the story, and discover grammar rules.
    </div>
</div>
""", unsafe_allow_html=True)

col_a, col_b, col_c, col_d, col_e = st.columns(5)

with col_a:
    st.markdown(f"<span class='badge'>Quiz {'✅' if st.session_state.mission_complete['quiz'] else '⬜'}</span>", unsafe_allow_html=True)
with col_b:
    st.markdown(f"<span class='badge'>Key {'✅' if st.session_state.mission_complete['key'] else '⬜'}</span>", unsafe_allow_html=True)
with col_c:
    st.markdown(f"<span class='badge'>Matching {'✅' if st.session_state.mission_complete['matching'] else '⬜'}</span>", unsafe_allow_html=True)
with col_d:
    st.markdown(f"<span class='badge'>Order {'✅' if st.session_state.mission_complete['order'] else '⬜'}</span>", unsafe_allow_html=True)
with col_e:
    st.markdown(f"<span class='badge'>Grammar {'✅' if st.session_state.mission_complete['grammar'] else '⬜'}</span>", unsafe_allow_html=True)

completed_count = sum(st.session_state.mission_complete.values())
st.progress(completed_count / 5)


# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎬 Video",
    "📖 Lines & Meaning",
    "✅ Comprehension Quiz",
    "🔑 Key Expressions",
    "🧩 Sentence Matching",
    "🕵️ Story Order",
    "📘 Grammar"
])


# =========================
# TAB 1 VIDEO
# =========================

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎬 Watch the Video</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상을 보고 배트맨이 왜 스스로 비난을 감당하려 하는지 생각해 봅시다.</div>', unsafe_allow_html=True)

    st.video(VIDEO_URL)

    st.markdown("""
    <div class="line-box">
        <b>Today's Mission</b><br>
        Is Batman a criminal, a hero, or something more complicated?
        <br>
        <span class="kor">오늘의 미션: 배트맨은 범죄자인가, 영웅인가, 아니면 더 복잡한 존재인가?</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 2 LINES & MEANING
# =========================

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📖 Lines & Meaning</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상 속 핵심 대사와 쉬운 의미를 확인하세요.</div>', unsafe_allow_html=True)

    for line in lines:
        st.markdown(f"""
        <div class="line-box">
            <span class="time-tag">{line["time"]}</span><br>
            <b>{line["en"]}</b><br>
            <span class="kor">{line["ko"]}</span><br><br>
            <b>Easy Meaning:</b> {line["simple"]}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 3 QUIZ
# =========================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✅ Comprehension Quiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상과 핵심 대사를 바탕으로 알맞은 답을 고르세요. 4개 이상 맞히면 성공입니다.</div>', unsafe_allow_html=True)

    quiz_score = 0

    for i, item in enumerate(quiz_questions, start=1):
        st.markdown(f"**Q{i}. {item['q']}**")
        user_answer = st.radio(
            "Choose one.",
            item["options"],
            key=f"quiz_{i}",
            horizontal=False
        )

        if user_answer == item["answer"]:
            quiz_score += 1

        with st.expander("Hint / Explanation"):
            st.write(item["explain"])

        st.write("")

    if st.button("퀴즈 채점하기", key="check_quiz"):
        st.markdown(f"### 점수: {quiz_score} / {len(quiz_questions)}")

        if quiz_score >= 4:
            st.session_state.mission_complete["quiz"] = True
            st.markdown("""
            <div class="success-box">
                🎉 이해도 퀴즈 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                조금만 더! Lines & Meaning을 다시 보고 도전해 봅시다.
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 4 KEY EXPRESSIONS
# =========================

with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔑 Key Expressions</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">배트맨 장면에서 나온 강한 표현들을 익혀 봅시다.</div>', unsafe_allow_html=True)

    for i, item in enumerate(key_expressions, start=1):
        st.markdown(f"""
        <div class="exp-box">
            <div class="exp-title">{i}. {item["exp"]}</div>
            <div class="exp-meaning">뜻: {item["meaning"]}</div>
            <div class="exp-meaning">포인트: {item["point"]}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Key Expressions 학습 완료", key="key_complete"):
        st.session_state.mission_complete["key"] = True
        st.markdown("""
        <div class="success-box">
            🔑 Key Expressions 임무를 완성하셨습니다!
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 5 SENTENCE MATCHING
# =========================

with tab5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 Sentence Matching</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영어 문장과 알맞은 한국어 뜻을 연결하세요. 5개 이상 맞히면 성공입니다.</div>', unsafe_allow_html=True)

    korean_options = [ko for en, ko in matching_items]
    match_score = 0

    for i, (en, ko) in enumerate(matching_items, start=1):
        st.markdown(f"""
        <div class="mission-box">
            <b>{i}. {en}</b>
        </div>
        """, unsafe_allow_html=True)

        user_match = st.selectbox(
            "알맞은 뜻을 고르세요.",
            ["선택하세요"] + korean_options,
            key=f"match_{i}"
        )

        if user_match == ko:
            match_score += 1

    if st.button("문장 매칭 채점하기", key="check_matching"):
        st.markdown(f"### 점수: {match_score} / {len(matching_items)}")

        if match_score >= 5:
            st.session_state.mission_complete["matching"] = True
            st.markdown("""
            <div class="success-box">
                🧩 문장 매칭 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                다시 한 번 문장과 뜻을 천천히 확인해 봅시다.
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 6 STORY ORDER
# =========================

with tab6:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🕵️ Story Order Mission</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">배트맨의 선택을 이야기 순서대로 배열하세요.</div>', unsafe_allow_html=True)

    order_score = 0
    user_order = []

    for i in range(len(order_answer)):
        choice = st.selectbox(
            f"{i+1}번째 순서",
            ["선택하세요"] + st.session_state.order_options,
            key=f"order_{i}"
        )
        user_order.append(choice)

    for i, ans in enumerate(order_answer):
        if user_order[i] == ans:
            order_score += 1

    if st.button("이야기 순서 채점하기", key="check_order"):
        st.markdown(f"### 점수: {order_score} / {len(order_answer)}")

        if order_score == len(order_answer):
            st.session_state.mission_complete["order"] = True
            st.markdown("""
            <div class="success-box">
                🕵️ Story Order 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                순서를 다시 생각해 봅시다. Batman이 먼저 무엇을 선택했는지 떠올려 보세요.
            </div>
            """, unsafe_allow_html=True)

    with st.expander("정답 순서 보기"):
        for i, sent in enumerate(order_answer, start=1):
            st.write(f"{i}. {sent}")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 7 GRAMMAR
# =========================

with tab7:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📘 Grammar Discovery</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">문장을 보고 규칙을 스스로 발견해 봅시다. 전부 맞히면 성공입니다.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="line-box">
        <b>Look at these sentences.</b><br><br>
        1. Gotham <b>needs</b> me.<br>
        2. The hero we <b>needed</b>.<br>
        3. People deserve <b>to have</b> their faith rewarded.<br>
        4. He can <b>take</b> it.<br><br>
        <span class="kor">
        생각해 봅시다: 왜 needs, needed, to have, take가 쓰였을까요?
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

    if st.button("Grammar 채점하기", key="check_grammar"):
        st.markdown(f"### 점수: {grammar_score} / {len(grammar_questions)}")

        if grammar_score == len(grammar_questions):
            st.session_state.mission_complete["grammar"] = True
            st.markdown("""
            <div class="success-box">
                📘 Grammar 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                거의 다 왔습니다! 단수 주어 + 동사 -s, 과거형, deserve to, can + 동사원형을 다시 확인하세요.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="line-box">
        <b>Grammar Rule</b><br><br>
        1. 단수 주어 현재동사에는 보통 <b>-s</b>를 붙입니다.<br>
        예: Gotham needs me.<br><br>
        2. 과거의 일을 말할 때는 과거형을 씁니다.<br>
        예: The hero we needed.<br><br>
        3. <b>deserve to + 동사</b>는 '~할 자격이 있다'라는 뜻입니다.<br>
        예: People deserve to have their faith rewarded.<br><br>
        4. <b>can + 동사원형</b>을 씁니다.<br>
        예: He can take it.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# FINAL MISSION STATUS
# =========================

st.markdown("---")

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
