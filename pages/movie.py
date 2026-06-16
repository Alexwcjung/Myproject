import streamlit as st
import random

st.set_page_config(page_title="Spring 2026", page_icon="🌸", layout="wide")

IMAGE_URL = "https://raw.githubusercontent.com/Alexwcjung/Fun-English/main/a143182b-832c-4a27-87fb-74214eabb338.png?v=11"

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
    font-size: 44px;
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
    background: linear-gradient(135deg,#fce7f3 0%,#e0f2fe 55%,#dcfce7 100%);
    border: 1px solid #fbcfe8;
    border-radius: 28px;
    padding: 26px 30px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(236,72,153,0.10);
}

.hero-title {
    font-size: 30px;
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
    font-size: 25px;
    font-weight: 900;
    color: #111827;
    margin-bottom: 10px;
}

.small-guide {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 14px;
}

.lyric-box {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px;
    line-height: 1.8;
    font-size: 17px;
}

.kor {
    color: #6b7280;
    font-size: 15px;
}

.success-box {
    background: #dcfce7;
    border: 1px solid #86efac;
    border-radius: 18px;
    padding: 16px;
    color: #166534;
    font-weight: 800;
    margin-top: 14px;
}

.fail-box {
    background: #fee2e2;
    border: 1px solid #fecaca;
    border-radius: 18px;
    padding: 16px;
    color: #991b1b;
    font-weight: 800;
    margin-top: 14px;
}

.exp-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
}

.exp-title {
    font-size: 18px;
    font-weight: 900;
    color: #1e3a8a;
}

.exp-meaning {
    color: #374151;
    font-size: 15px;
    margin-top: 4px;
}

.match-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 10px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# DATA
# =========================

lyrics = [
    {
        "en": "Spring is coming, flowers are blooming.",
        "ko": "봄이 오고 있고, 꽃들이 피고 있다."
    },
    {
        "en": "The warm wind makes me feel free.",
        "ko": "따뜻한 바람은 나를 자유롭게 느끼게 한다."
    },
    {
        "en": "I walk outside and see the bright sky.",
        "ko": "나는 밖을 걷고 밝은 하늘을 본다."
    },
    {
        "en": "Every new day gives me hope.",
        "ko": "새로운 하루하루가 나에게 희망을 준다."
    },
    {
        "en": "Spring reminds me to start again.",
        "ko": "봄은 나에게 다시 시작하라고 떠올리게 한다."
    }
]

quiz_questions = [
    {
        "q": "What season is the text about?",
        "options": ["Winter", "Spring", "Summer", "Fall"],
        "answer": "Spring"
    },
    {
        "q": "What is blooming?",
        "options": ["Flowers", "Books", "Clouds", "Stars"],
        "answer": "Flowers"
    },
    {
        "q": "How does the warm wind make the speaker feel?",
        "options": ["Sad", "Angry", "Free", "Tired"],
        "answer": "Free"
    },
    {
        "q": "What does every new day give the speaker?",
        "options": ["Hope", "Homework", "Money", "Rain"],
        "answer": "Hope"
    },
    {
        "q": "What does spring remind the speaker to do?",
        "options": ["Sleep again", "Start again", "Run away", "Stay home"],
        "answer": "Start again"
    }
]

key_expressions = [
    {
        "exp": "Spring is coming.",
        "meaning": "봄이 오고 있다.",
        "point": "is coming은 '오고 있다'라는 현재진행 표현입니다."
    },
    {
        "exp": "Flowers are blooming.",
        "meaning": "꽃들이 피고 있다.",
        "point": "are blooming은 여러 꽃들이 피고 있는 모습을 나타냅니다."
    },
    {
        "exp": "makes me feel free",
        "meaning": "나를 자유롭게 느끼게 한다.",
        "point": "make + 사람 + 동사원형 구조입니다."
    },
    {
        "exp": "Every new day gives me hope.",
        "meaning": "새로운 하루하루가 나에게 희망을 준다.",
        "point": "give + 사람 + 사물 구조입니다."
    },
    {
        "exp": "start again",
        "meaning": "다시 시작하다.",
        "point": "again은 '다시'라는 뜻입니다."
    }
]

matching_items = [
    ("Spring is coming.", "봄이 오고 있다."),
    ("Flowers are blooming.", "꽃들이 피고 있다."),
    ("The warm wind makes me feel free.", "따뜻한 바람은 나를 자유롭게 느끼게 한다."),
    ("I see the bright sky.", "나는 밝은 하늘을 본다."),
    ("Every new day gives me hope.", "새로운 하루하루가 나에게 희망을 준다."),
    ("Spring reminds me to start again.", "봄은 나에게 다시 시작하라고 떠올리게 한다.")
]

grammar_questions = [
    {
        "q": "Flowers ___ blooming.",
        "options": ["is", "are", "am"],
        "answer": "are",
        "explain": "Flowers는 복수이므로 are를 씁니다."
    },
    {
        "q": "Spring ___ coming.",
        "options": ["is", "are", "am"],
        "answer": "is",
        "explain": "Spring은 단수이므로 is를 씁니다."
    },
    {
        "q": "The warm wind makes me ___ free.",
        "options": ["feel", "feels", "to feel"],
        "answer": "feel",
        "explain": "make + 사람 + 동사원형 구조이므로 feel을 씁니다."
    }
]


# =========================
# HEADER
# =========================

st.markdown('<div class="main-title">🌸 Spring 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Image-based English Activity</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-title">Spring English Master Class</div>
    <div class="hero-sub">
        Look at the spring image, read the short text, understand key expressions, 
        solve quizzes, match sentences, and discover grammar rules.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌸 Image",
    "🎧 Text & Meaning",
    "✅ Comprehension Quiz",
    "🔑 Key Expressions",
    "🧩 Sentence Matching",
    "📘 Grammar"
])


# =========================
# TAB 1 IMAGE
# =========================

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌸 Look at the Image</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">그림을 보고 봄과 관련된 분위기를 생각해 봅시다.</div>', unsafe_allow_html=True)

    st.image(IMAGE_URL, use_container_width=True)

    st.markdown("""
    <div class="lyric-box">
        <b>Today’s Topic:</b> Spring, flowers, warm wind, bright sky, hope
        <br>
        <span class="kor">오늘의 주제: 봄, 꽃, 따뜻한 바람, 밝은 하늘, 희망</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 2 TEXT & MEANING
# =========================

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎧 Text & Meaning</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영어 문장을 읽고 한국어 뜻을 확인하세요.</div>', unsafe_allow_html=True)

    for line in lyrics:
        st.markdown(f"""
        <div class="lyric-box">
            <b>{line["en"]}</b><br>
            <span class="kor">{line["ko"]}</span>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 3 COMPREHENSION QUIZ
# =========================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✅ Comprehension Quiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">본문 내용을 바탕으로 알맞은 답을 고르세요.</div>', unsafe_allow_html=True)

    quiz_score = 0

    for i, item in enumerate(quiz_questions, start=1):
        st.markdown(f"**Q{i}. {item['q']}**")
        user_answer = st.radio(
            "Choose one.",
            item["options"],
            key=f"quiz_{i}",
            horizontal=True
        )

        if user_answer == item["answer"]:
            quiz_score += 1

        st.write("")

    if st.button("퀴즈 채점하기", key="check_quiz"):
        st.markdown(f"### 점수: {quiz_score} / {len(quiz_questions)}")

        if quiz_score >= 4:
            st.markdown("""
            <div class="success-box">
                🎉 이해도 퀴즈 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                조금만 더! Text & Meaning을 다시 보고 도전해 봅시다.
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 4 KEY EXPRESSIONS
# =========================

with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔑 Key Expressions</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">중요 표현을 확인하고 뜻과 문법 포인트를 익히세요.</div>', unsafe_allow_html=True)

    for i, item in enumerate(key_expressions, start=1):
        st.markdown(f"""
        <div class="exp-box">
            <div class="exp-title">{i}. {item["exp"]}</div>
            <div class="exp-meaning">뜻: {item["meaning"]}</div>
            <div class="exp-meaning">포인트: {item["point"]}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Key Expressions 학습 완료", key="key_complete"):
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
    st.markdown('<div class="small-guide">영어 문장과 알맞은 한국어 뜻을 연결하세요.</div>', unsafe_allow_html=True)

    korean_options = [ko for en, ko in matching_items]
    match_score = 0

    for i, (en, ko) in enumerate(matching_items, start=1):
        st.markdown(f"""
        <div class="match-card">
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
# TAB 6 GRAMMAR
# =========================

with tab6:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📘 Grammar Discovery</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">문장을 보고 규칙을 스스로 발견해 봅시다.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lyric-box">
        <b>Look at these sentences.</b><br><br>
        1. Spring <b>is coming</b>.<br>
        2. Flowers <b>are blooming</b>.<br>
        3. The warm wind <b>makes me feel</b> free.<br><br>
        <span class="kor">
        생각해 봅시다: Spring에는 왜 is를 쓰고, Flowers에는 왜 are를 쓸까요?
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

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
            st.markdown("""
            <div class="success-box">
                📘 Grammar 임무를 완성하셨습니다!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fail-box">
                거의 다 왔습니다! is / are 규칙과 make + 사람 + 동사원형을 다시 확인하세요.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="lyric-box">
        <b>Grammar Rule</b><br><br>
        1. 단수 주어에는 <b>is</b>를 씁니다.<br>
        예: Spring is coming.<br><br>
        2. 복수 주어에는 <b>are</b>를 씁니다.<br>
        예: Flowers are blooming.<br><br>
        3. <b>make + 사람 + 동사원형</b>은 '~가 사람을 ...하게 만들다'라는 뜻입니다.<br>
        예: The warm wind makes me feel free.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
