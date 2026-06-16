import streamlit as st
import random

st.set_page_config(page_title="Batman English Mission", page_icon="🦇", layout="wide")

VIDEO_URL = "https://www.youtube.com/watch?v=U4fhEziQsc8"

# =========================
# CSS - BRIGHT STYLE
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

.exp-box {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
}

.exp-title {
    font-size: 18px;
    font-weight: 900;
    color: #92400e;
}

.exp-meaning {
    color: #374151;
    font-size: 15px;
    margin-top: 4px;
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
        "q": "At first, what do people think Batman is?",
        "options": ["A hero", "A criminal", "A singer", "A teacher"],
        "answer": "A criminal"
    },
    {
        "q": "What is Batman really doing?",
        "options": ["Running away", "Taking the blame", "Looking for money", "Making music"],
        "answer": "Taking the blame"
    },
    {
        "q": "What kind of person is Batman in this scene?",
        "options": ["Selfish", "Lazy", "Sacrificing", "Funny"],
        "answer": "Sacrificing"
    }
]

blank_questions = [
    {
        "sentence": "I'm whatever Gotham ______ me to be.",
        "options": ["need", "needs", "needed"],
        "answer": "needs"
    },
    {
        "sentence": "Not the hero we ______, but the hero we ______.",
        "options": ["deserved / needed", "need / deserve", "needs / deserved"],
        "answer": "deserved / needed"
    },
    {
        "sentence": "Sometimes people ______ more.",
        "options": ["deserve", "deserves", "deserved"],
        "answer": "deserve"
    },
    {
        "sentence": "Because he can ______ it.",
        "options": ["takes", "take", "took"],
        "answer": "take"
    },
    {
        "sentence": "A silent ______, a watchful ______.",
        "options": ["guardian / protector", "student / teacher", "singer / dancer"],
        "answer": "guardian / protector"
    }
]

matching_items = [
    ("I'm whatever Gotham needs me to be.", "나는 고담시가 필요로 하는 무엇이든 될 거야."),
    ("Not the hero we deserved.", "우리가 받을 자격이 있던 영웅은 아니다."),
    ("The hero we needed.", "우리에게 필요했던 영웅."),
    ("Sometimes people deserve more.", "때로 사람들은 더 많은 것을 받을 자격이 있다."),
    ("Because he can take it.", "왜냐하면 그는 그것을 감당할 수 있으니까."),
    ("A silent guardian.", "조용한 수호자."),
    ("A watchful protector.", "늘 지켜보는 보호자.")
]

story_order_answer = [
    "Batman decides to take the blame.",
    "People think Batman is bad.",
    "Gotham starts to hunt Batman.",
    "Batman still protects Gotham.",
    "Batman becomes a silent guardian."
]

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

if "story_options" not in st.session_state:
    temp = story_order_answer.copy()
    random.shuffle(temp)
    st.session_state.story_options = temp


# =========================
# HEADER
# =========================

st.markdown('<div class="main-title">🦇 Batman English Mission</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Video-based English Activity · Bright Classroom Version</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-title">Hero or Villain?</div>
    <div class="hero-sub">
        Watch the Batman scene and complete five missions: choose Batman's role, fill in key lines,
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
    st.markdown('<div class="small-guide">영상 속 배트맨의 역할을 추리해 봅시다. 2문제 이상 맞히면 성공입니다.</div>', unsafe_allow_html=True)

    choice_score = 0

    for i, item in enumerate(hero_questions, start=1):
        st.markdown(f"**Q{i}. {item['q']}**")
        user_answer = st.radio(
            "Choose one.",
            item["options"],
            key=f"hero_{i}",
            horizontal=True
        )

        if user_answer == item["answer"]:
            choice_score += 1

        st.write("")

    if st.button("Hero or Villain 채점하기", key="check_hero"):
        st.markdown(f"### 점수: {choice_score} / {len(hero_questions)}")

        if choice_score >= 2:
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
# TAB 3 LINE BLANKS
# =========================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎧 Line Blanks</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상 속 핵심 대사를 듣고 빈칸에 들어갈 말을 고르세요. 4개 이상 맞히면 성공입니다.</div>', unsafe_allow_html=True)

    blank_score = 0

    for i, item in enumerate(blank_questions, start=1):
        st.markdown(f"""
        <div class="mission-box">
            <b>Q{i}. {item["sentence"]}</b>
        </div>
        """, unsafe_allow_html=True)

        user_answer = st.radio(
            "Choose one.",
            item["options"],
            key=f"blank_{i}",
            horizontal=True
        )

        if user_answer == item["answer"]:
            blank_score += 1

        st.write("")

    if st.button("빈칸 채점하기", key="check_blank"):
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
                조금만 더! 영상을 다시 보고 핵심 대사를 확인해 봅시다.
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
# TAB 5 QUOTE MATCHING
# =========================

with tab5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 Quote Matching</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영어 대사와 알맞은 한국어 뜻을 연결하세요. 6개 이상 맞히면 성공입니다.</div>', unsafe_allow_html=True)

    korean_options = [ko for en, ko in matching_items]
    matching_score = 0

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
            matching_score += 1

    if st.button("Quote Matching 채점하기", key="check_matching"):
        st.markdown(f"### 점수: {matching_score} / {len(matching_items)}")

        if matching_score >= 6:
            st.session_state.batman_complete["matching"] = True
            st.markdown("""
            <div class="success-box">
                🧩 Quote Matching 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                다시 한 번 영어 대사와 한국어 뜻을 천천히 확인해 봅시다.
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

    user_order = []
    order_score = 0

    for i in range(len(story_order_answer)):
        choice = st.selectbox(
            f"{i+1}번째 순서",
            ["선택하세요"] + st.session_state.story_options,
            key=f"order_{i}"
        )
        user_order.append(choice)

    for i, ans in enumerate(story_order_answer):
        if user_order[i] == ans:
            order_score += 1

    if st.button("Story Order 채점하기", key="check_order"):
        st.markdown(f"### 점수: {order_score} / {len(story_order_answer)}")

        if order_score == len(story_order_answer):
            st.session_state.batman_complete["order"] = True
            st.markdown("""
            <div class="success-box">
                🕵️ Story Order 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                순서를 다시 생각해 봅시다. Batman은 먼저 어떤 선택을 했을까요?
            </div>
            """, unsafe_allow_html=True)

    with st.expander("정답 순서 보기"):
        for i, sent in enumerate(story_order_answer, start=1):
            st.write(f"{i}. {sent}")

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

    if st.button("Grammar 채점하기", key="check_grammar"):
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
