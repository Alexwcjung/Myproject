import streamlit as st
import streamlit.components.v1 as components
import random
import html
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="Movie English: The Dark Knight",
    page_icon="🦇",
    layout="wide"
)

# =========================
# PDF 생성
# =========================
def make_mission_pdf(activity_name, student_name, detail_text):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib import colors

        buffer = BytesIO()

        # 한글 폰트가 서버에 없을 수 있으므로 기본 폰트 사용
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()

        title_style = styles["Title"]
        title_style.alignment = TA_CENTER
        title_style.textColor = colors.HexColor("#111827")

        normal = styles["BodyText"]
        normal.fontSize = 12
        normal.leading = 18

        story = []

        story.append(Paragraph("Mission Complete", title_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"<b>Activity:</b> {activity_name}", normal))
        story.append(Paragraph(f"<b>Student:</b> {student_name if student_name else 'Student'}", normal))
        story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal))
        story.append(Spacer(1, 20))
        story.append(Paragraph("<b>Completed Task</b>", normal))
        story.append(Paragraph(detail_text, normal))
        story.append(Spacer(1, 30))
        story.append(Paragraph("You have completed this English mission successfully.", normal))

        doc.build(story)
        buffer.seek(0)
        return buffer

    except Exception as e:
        st.warning("PDF 생성을 위해 reportlab 설치가 필요합니다. requirements.txt에 reportlab을 추가하세요.")
        return None


# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: #f8fafc;
    color: #111827;
}
.main-title {
    font-size: 42px;
    font-weight: 1000;
    color: #111827;
    margin-bottom: 4px;
}
.sub-title {
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 20px;
}
.hero-box {
    background: linear-gradient(135deg,#dbeafe 0%,#ede9fe 55%,#fef3c7 100%);
    border: 1px solid #c7d2fe;
    border-radius: 28px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(30,64,175,0.10);
}
.hero-title {
    font-size: 30px;
    font-weight: 1000;
    color: #0f172a;
    margin-bottom: 8px;
}
.card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 4px 14px rgba(15,23,42,0.06);
}
.script-line {
    background: #f9fafb;
    border-left: 6px solid #6366f1;
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 10px;
    font-size: 18px;
    line-height: 1.6;
}
.korean {
    color: #6b7280;
    font-size: 15px;
    margin-top: 4px;
}
.success-box {
    background: #ecfdf5;
    border: 1px solid #bbf7d0;
    color: #065f46;
    border-radius: 18px;
    padding: 16px;
    font-weight: 800;
    margin: 12px 0;
}
.fail-box {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    color: #9a3412;
    border-radius: 18px;
    padding: 16px;
    font-weight: 800;
    margin: 12px 0;
}
.small-note {
    color: #6b7280;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# 데이터
# =========================
VIDEO_URL = "https://www.youtube.com/embed/U4fhEziQsc8"

SCRIPT = [
    {
        "speaker": "Batman",
        "en": "I killed those people. That's what I can be.",
        "ko": "내가 그 사람들을 죽인 걸로 해. 그게 내가 될 수 있는 모습이야."
    },
    {
        "speaker": "Gordon",
        "en": "No, no. You can't. You're not.",
        "ko": "안 돼. 넌 그럴 수 없어. 넌 그런 사람이 아니야."
    },
    {
        "speaker": "Batman",
        "en": "I'm whatever Gotham needs me to be.",
        "ko": "나는 고담이 필요로 하는 어떤 존재든 될 수 있어."
    },
    {
        "speaker": "Gordon",
        "en": "A hero. Not the hero we deserved, but the hero we needed.",
        "ko": "영웅. 우리가 받을 자격이 있는 영웅은 아니지만, 우리에게 필요했던 영웅."
    },
    {
        "speaker": "Batman",
        "en": "You'll hunt me. You'll condemn me. Set the dogs on me.",
        "ko": "나를 쫓아. 나를 비난해. 추격하게 만들어."
    },
    {
        "speaker": "Batman",
        "en": "Because that's what needs to happen.",
        "ko": "왜냐하면 그래야 하기 때문이야."
    },
    {
        "speaker": "Batman",
        "en": "Because sometimes the truth isn't good enough.",
        "ko": "때로는 진실만으로는 충분하지 않기 때문이야."
    },
    {
        "speaker": "Batman",
        "en": "Sometimes people deserve more.",
        "ko": "때로 사람들은 그 이상의 것을 받을 자격이 있어."
    },
    {
        "speaker": "Batman",
        "en": "Sometimes people deserve to have their faith rewarded.",
        "ko": "때로 사람들은 자신의 믿음이 보상받을 자격이 있어."
    },
    {
        "speaker": "Gordon",
        "en": "Because he's the hero Gotham deserves, but not the one it needs right now.",
        "ko": "그는 고담이 받을 자격이 있는 영웅이지만, 지금 고담에게 필요한 영웅은 아니기 때문이야."
    },
    {
        "speaker": "Gordon",
        "en": "So we'll hunt him. Because he can take it.",
        "ko": "그래서 우리는 그를 쫓을 거야. 그는 감당할 수 있으니까."
    },
    {
        "speaker": "Gordon",
        "en": "Because he's not our hero.",
        "ko": "그는 우리의 영웅이 아니니까."
    },
    {
        "speaker": "Gordon",
        "en": "He's a silent guardian. A watchful protector. A Dark Knight.",
        "ko": "그는 조용한 수호자. 지켜보는 보호자. 어둠의 기사야."
    },
]

QUIZ = [
    {
        "q": "Why does Batman want Gordon to blame him?",
        "choices": [
            "Because he wants money",
            "Because Gotham needs hope",
            "Because he hates Gordon",
            "Because he wants to leave Gotham"
        ],
        "answer": "Because Gotham needs hope"
    },
    {
        "q": "What does Batman say he can be?",
        "choices": [
            "Whatever Gotham needs him to be",
            "A police officer",
            "A normal citizen",
            "A king"
        ],
        "answer": "Whatever Gotham needs him to be"
    },
    {
        "q": "What does Gordon say about Batman?",
        "choices": [
            "He is a bad man",
            "He is not important",
            "He is a silent guardian",
            "He is afraid"
        ],
        "answer": "He is a silent guardian"
    },
    {
        "q": "What does 'the truth isn't good enough' mean in this scene?",
        "choices": [
            "Truth is always useless",
            "People sometimes need hope more than painful truth",
            "Batman does not know the truth",
            "Gordon lies for no reason"
        ],
        "answer": "People sometimes need hope more than painful truth"
    },
    {
        "q": "Which word means 'to follow and try to catch someone'?",
        "choices": [
            "deserve",
            "reward",
            "hunt",
            "protect"
        ],
        "answer": "hunt"
    },
]

KEY_EXPRESSIONS = [
    ("take the blame", "책임을 대신 지다", "Batman takes the blame for Gotham."),
    ("whatever A needs B to be", "A가 B에게 필요로 하는 어떤 존재든", "I'm whatever Gotham needs me to be."),
    ("deserve", "받을 자격이 있다", "People deserve more."),
    ("faith", "믿음", "People deserve to have their faith rewarded."),
    ("reward", "보상하다", "Their faith is rewarded."),
    ("hunt", "쫓다, 추격하다", "The police will hunt Batman."),
    ("condemn", "비난하다, 유죄로 여기다", "They will condemn him."),
    ("silent guardian", "조용한 수호자", "He is a silent guardian."),
    ("watchful protector", "지켜보는 보호자", "He is a watchful protector."),
    ("Dark Knight", "어둠의 기사", "Batman becomes the Dark Knight."),
]

MATCHING = [
    ("I'm whatever Gotham needs me to be.", "나는 고담이 필요로 하는 어떤 존재든 될 수 있어."),
    ("Sometimes the truth isn't good enough.", "때로는 진실만으로는 충분하지 않아."),
    ("Sometimes people deserve more.", "때로 사람들은 그 이상의 것을 받을 자격이 있어."),
    ("So we'll hunt him.", "그래서 우리는 그를 쫓을 거야."),
    ("Because he can take it.", "그는 감당할 수 있으니까."),
    ("He's a silent guardian.", "그는 조용한 수호자야."),
    ("A watchful protector.", "지켜보는 보호자."),
    ("A Dark Knight.", "어둠의 기사."),
]


# =========================
# 세션 상태
# =========================
if "completed" not in st.session_state:
    st.session_state.completed = set()

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "matching_order" not in st.session_state:
    korean_items = [ko for en, ko in MATCHING]
    random.shuffle(korean_items)
    st.session_state.matching_order = korean_items


# =========================
# 완료 처리 함수
# =========================
def complete_activity(activity_name):
    st.session_state.completed.add(activity_name)
    st.markdown(
        f"<div class='success-box'>✅ {activity_name} 임무를 완성하셨습니다!</div>",
        unsafe_allow_html=True
    )

    pdf = make_mission_pdf(
        activity_name=activity_name,
        student_name=st.session_state.student_name,
        detail_text=f"{activity_name} activity was completed successfully in the Movie English lesson."
    )

    if pdf:
        st.download_button(
            label=f"📄 {activity_name} 완료 PDF 저장",
            data=pdf,
            file_name=f"mission_complete_{activity_name}.pdf",
            mime="application/pdf",
            key=f"pdf_{activity_name}"
        )


# =========================
# 메인 화면
# =========================
st.markdown("<div class='main-title'>🦇 Movie English: The Dark Knight</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>영상으로 듣고, 스크립트로 이해하고, 핵심 표현을 익히는 영어 활동</div>", unsafe_allow_html=True)

st.markdown("""
<div class='hero-box'>
    <div class='hero-title'>Today's Mission</div>
    <div style='font-size:18px; line-height:1.7;'>
    Watch the scene, understand the script, learn key expressions, match sentences, and write your own thoughts.
    <br>
    영상을 보고 대사를 이해한 뒤, 핵심 표현을 배우고 자신의 생각을 영어로 써 봅시다.
    </div>
</div>
""", unsafe_allow_html=True)

st.session_state.student_name = st.text_input(
    "학생 이름을 입력하세요",
    value=st.session_state.student_name,
    placeholder="예: 1학년 3반 홍길동"
)


tabs = st.tabs([
    "🎬 1. 영상 보기",
    "📜 2. 스크립트",
    "✅ 3. 이해도 퀴즈",
    "🔑 4. 핵심 표현",
    "🧩 5. 문장 매칭",
    "🧠 6. 생각 쓰기",
    "📘 7. Grammar"
])


# =========================
# 1. 영상 보기
# =========================
with tabs[0]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎬 Watch the Scene")

    components.html(
        f"""
        <iframe width="100%" height="480"
        src="{VIDEO_URL}"
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen>
        </iframe>
        """,
        height=500
    )

    st.info("영상을 보면서 Batman과 Gordon이 왜 이런 선택을 하는지 생각해 봅시다.")

    if st.button("🎬 영상 보기 완료", key="complete_video"):
        complete_activity("영상 보기")

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# 2. 스크립트
# =========================
with tabs[1]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📜 Script Reading")

    show_korean = st.toggle("한국어 뜻 보기", value=True)

    for i, line in enumerate(SCRIPT, 1):
        st.markdown(
            f"""
            <div class='script-line'>
                <b>{i}. {line['speaker']}:</b><br>
                {html.escape(line['en'])}
                {f"<div class='korean'>{html.escape(line['ko'])}</div>" if show_korean else ""}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 빈칸 채우기")

    c1, c2 = st.columns(2)
    with c1:
        blank1 = st.text_input("1. I'm ________ Gotham needs me to be.")
    with c2:
        blank2 = st.text_input("2. Sometimes the ________ isn't good enough.")

    if st.button("📜 스크립트 확인", key="check_script"):
        score = 0
        if blank1.strip().lower() == "whatever":
            score += 1
        if blank2.strip().lower() == "truth":
            score += 1

        st.write(f"점수: {score}/2")

        if score == 2:
            complete_activity("스크립트 이해")
        else:
            st.markdown("<div class='fail-box'>조금 더 다시 읽어 봅시다. 힌트: whatever / truth</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# 3. 이해도 퀴즈
# =========================
with tabs[2]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✅ Comprehension Quiz")

    quiz_answers = []

    for idx, item in enumerate(QUIZ, 1):
        st.markdown(f"**Q{idx}. {item['q']}**")
        ans = st.radio(
            label="정답을 고르세요",
            options=item["choices"],
            key=f"quiz_{idx}",
            label_visibility="collapsed"
        )
        quiz_answers.append(ans)
        st.markdown("---")

    if st.button("✅ 퀴즈 채점하기", key="grade_quiz"):
        score = 0
        for user_ans, item in zip(quiz_answers, QUIZ):
            if user_ans == item["answer"]:
                score += 1

        st.write(f"점수: {score}/{len(QUIZ)}")

        if score >= 4:
            complete_activity("이해도 퀴즈")
        else:
            st.markdown("<div class='fail-box'>다시 도전해 봅시다. 5문제 중 4문제 이상 맞히면 완료입니다.</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# 4. 핵심 표현
# =========================
with tabs[3]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔑 Key Expressions")

    for exp, meaning, example in KEY_EXPRESSIONS:
        st.markdown(
            f"""
            <div class='script-line'>
                <b>{exp}</b> : {meaning}
                <div class='korean'>Example: {example}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 핵심 표현 확인 문제")

    q1 = st.selectbox(
        "1. '책임을 대신 지다'에 해당하는 표현은?",
        ["choose one", "take the blame", "watchful protector", "faith", "reward"]
    )

    q2 = st.selectbox(
        "2. '쫓다, 추격하다'에 해당하는 표현은?",
        ["choose one", "deserve", "hunt", "truth", "silent guardian"]
    )

    q3 = st.selectbox(
        "3. '받을 자격이 있다'에 해당하는 표현은?",
        ["choose one", "condemn", "deserve", "guardian", "knight"]
    )

    if st.button("🔑 핵심 표현 확인", key="check_key"):
        score = 0
        if q1 == "take the blame":
            score += 1
        if q2 == "hunt":
            score += 1
        if q3 == "deserve":
            score += 1

        st.write(f"점수: {score}/3")

        if score == 3:
            complete_activity("핵심 표현")
        else:
            st.markdown("<div class='fail-box'>핵심 표현을 다시 확인해 봅시다.</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# 5. 문장 매칭
# =========================
with tabs[4]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧩 Sentence Matching")

    st.write("영어 문장과 알맞은 한국어 뜻을 연결하세요.")

    user_matches = []

    for idx, (en, ko) in enumerate(MATCHING, 1):
        st.markdown(f"**{idx}. {en}**")
        selected = st.selectbox(
            "뜻을 고르세요",
            ["choose one"] + st.session_state.matching_order,
            key=f"match_{idx}"
        )
        user_matches.append((selected, ko))
        st.markdown("---")

    if st.button("🧩 문장 매칭 채점하기", key="grade_matching"):
        score = sum(1 for selected, correct in user_matches if selected == correct)

        st.write(f"점수: {score}/{len(MATCHING)}")

        if score >= 6:
            complete_activity("문장 매칭")
        else:
            st.markdown("<div class='fail-box'>8문제 중 6문제 이상 맞히면 완료입니다. 다시 도전해 봅시다.</div>", unsafe_allow_html=True)

    if st.button("🔄 문장 매칭 보기 섞기", key="shuffle_matching"):
        korean_items = [ko for en, ko in MATCHING]
        random.shuffle(korean_items)
        st.session_state.matching_order = korean_items
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# 6. 생각 쓰기
# =========================
with tabs[5]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧠 Write Your Thoughts")

    st.write("아래 질문 중 하나를 골라 영어로 3문장 이상 써 봅시다.")

    prompt = st.radio(
        "Writing Topic",
        [
            "1. Why does Batman choose to take the blame?",
            "2. Do you think truth is always the best choice?",
            "3. What kind of hero does Gotham need?",
            "4. Who is a silent guardian in your life?"
        ]
    )

    writing = st.text_area(
        "Your Writing",
        height=220,
        placeholder="I think Batman chooses to take the blame because..."
    )

    word_count = len(writing.split())
    sentence_count = writing.count(".") + writing.count("!") + writing.count("?")

    st.write(f"단어 수: {word_count} words")
    st.write(f"문장 수 추정: {sentence_count} sentences")

    st.markdown("### Writing Helper")
    st.markdown("""
    - I think Batman chooses to...
    - In my opinion, truth is...
    - Gotham needs a hero who can...
    - A silent guardian is someone who...
    - This scene shows that...
    """)

    if st.button("🧠 생각 쓰기 제출", key="submit_writing"):
        if word_count >= 20 and sentence_count >= 3:
            complete_activity("생각 쓰기")
        else:
            st.markdown(
                "<div class='fail-box'>영어로 3문장 이상, 20단어 이상 써 봅시다.</div>",
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# 7. Grammar
# =========================
with tabs[6]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📘 Grammar Discovery")

    st.markdown("""
    오늘의 문법 포인트는 다음 문장입니다.

    **I'm whatever Gotham needs me to be.**

    이 문장은 조금 어렵지만, 구조를 나누면 이해할 수 있습니다.
    """)

    st.markdown("""
    ### 1. 문장 구조 발견하기

    **I'm whatever Gotham needs me to be.**

    - I’m = I am
    - whatever = 무엇이든 / 어떤 존재든
    - Gotham needs me to be = 고담이 내가 되기를 필요로 하는

    그래서 전체 뜻은  
    **나는 고담이 내가 되기를 필요로 하는 어떤 존재든 될 수 있다.**
    """)

    st.markdown("""
    ### 2. 비슷한 문장 만들기

    아래 문장을 보고 규칙을 찾아봅시다.

    - I am whatever my family needs me to be.
    - I am whatever my friends need me to be.
    - I am whatever my students need me to be.

    **whatever + 주어 + need(s) + 사람 + to be**

    뜻:  
    **주어가 그 사람이 되기를 필요로 하는 어떤 존재든**
    """)

    st.markdown("### Grammar Practice")

    g1 = st.text_input("1. 나는 우리 가족이 필요로 하는 사람이 될 수 있다. → I am whatever my family ________ me to be.")
    g2 = st.text_input("2. 그는 고담이 필요로 하는 영웅이다. → He is the hero Gotham ________.")
    g3 = st.text_input("3. 우리는 그를 쫓을 것이다. → We will ________ him.")

    if st.button("📘 Grammar 확인", key="check_grammar"):
        score = 0

        if g1.strip().lower() == "needs":
            score += 1
        if g2.strip().lower() == "needs":
            score += 1
        if g3.strip().lower() == "hunt":
            score += 1

        st.write(f"점수: {score}/3")

        if score == 3:
            complete_activity("Grammar")
        else:
            st.markdown("<div class='fail-box'>힌트: needs / needs / hunt</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# 전체 진행 상황
# =========================
st.markdown("---")
st.subheader("📌 Mission Progress")

all_activities = [
    "영상 보기",
    "스크립트 이해",
    "이해도 퀴즈",
    "핵심 표현",
    "문장 매칭",
    "생각 쓰기",
    "Grammar"
]

cols = st.columns(len(all_activities))

for col, act in zip(cols, all_activities):
    with col:
        if act in st.session_state.completed:
            st.success(f"✅ {act}")
        else:
            st.info(f"⬜ {act}")

progress = len(st.session_state.completed) / len(all_activities)
st.progress(progress)

if len(st.session_state.completed) == len(all_activities):
    st.balloons()
    st.markdown(
        "<div class='success-box'>🎉 모든 Movie English 활동을 완료했습니다!</div>",
        unsafe_allow_html=True
    )

    final_pdf = make_mission_pdf(
        activity_name="The Dark Knight 전체 활동",
        student_name=st.session_state.student_name,
        detail_text="영상 보기, 스크립트 이해, 이해도 퀴즈, 핵심 표현, 문장 매칭, 생각 쓰기, Grammar 활동을 모두 완료했습니다."
    )

    if final_pdf:
        st.download_button(
            label="🏆 전체 활동 완료 PDF 저장",
            data=final_pdf,
            file_name="mission_complete_The_Dark_Knight_all_activities.pdf",
            mime="application/pdf",
            key="final_pdf"
        )
