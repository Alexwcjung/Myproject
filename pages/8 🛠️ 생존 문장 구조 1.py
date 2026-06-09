import streamlit as st

st.set_page_config(page_title="Survival Sentence Guide", page_icon="🛟", layout="centered")

# =========================================================
# 전체 디자인 CSS
# =========================================================
st.markdown(
    """
    <style>
    .main {
        background-color: #fffdfc;
    }

    .title-box {
        background: linear-gradient(135deg, #fff7fb 0%, #eef7ff 50%, #fff8e8 100%);
        padding: 34px 30px;
        border-radius: 32px;
        margin-bottom: 28px;
        box-shadow: 0 10px 26px rgba(80, 80, 120, 0.12);
        text-align: center;
        border: 1.5px solid #f3e8ff;
    }

    .title-box h1 {
        color: #334155;
        margin-bottom: 10px;
        font-size: 38px;
        font-weight: 900;
    }

    .title-box p {
        color: #64748b;
        font-size: 19px;
        margin: 0;
        line-height: 1.7;
    }

    .grammar-card {
        border-radius: 30px;
        padding: 28px 30px;
        margin: 20px 0 26px 0;
        box-shadow: 0 8px 22px rgba(0,0,0,0.07);
        border: 1.5px solid rgba(255,255,255,0.9);
    }

    .grammar-card h3 {
        margin-top: 0;
        font-size: 27px;
        font-weight: 900;
    }

    .grammar-card p {
        font-size: 21px;
        line-height: 1.85;
        color: #374151;
    }

    .formula-box {
        background: rgba(255,255,255,0.85);
        padding: 18px 20px;
        border-radius: 22px;
        font-size: 27px;
        font-weight: 900;
        text-align: center;
        margin-top: 16px;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.9);
    }

    .example-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        padding: 20px 22px;
        border-radius: 22px;
        margin: 16px 0;
        box-shadow: 0 5px 14px rgba(0,0,0,0.055);
        font-size: 20px;
        line-height: 1.85;
        border: 1.5px solid #e8f0ff;
        color: #334155;
    }

    .example-box b {
        color: #2563eb;
    }

    .mini-card {
        background: linear-gradient(135deg, #ffffff 0%, #fbfdff 100%);
        border-radius: 24px;
        padding: 22px 24px;
        margin: 14px 0;
        box-shadow: 0 5px 16px rgba(0,0,0,0.055);
        border: 1.5px solid #edf2ff;
    }

    .mini-card h4 {
        margin-top: 0;
        color: #2563eb;
        font-size: 22px;
        font-weight: 900;
    }

    .mini-card p {
        font-size: 20px;
        line-height: 1.75;
        color: #374151;
    }


    .path-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 50%, #fdf2f8 100%);
        border: 1.5px solid #dbeafe;
        border-radius: 28px;
        padding: 24px 26px;
        margin: 18px 0 28px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.065);
    }

    .path-box h3 {
        margin-top: 0;
        color: #1e3a8a;
        font-size: 25px;
        font-weight: 900;
    }

    .path-box p {
        font-size: 19px;
        line-height: 1.8;
        color: #374151;
        margin: 8px 0;
    }

    .mission-chip {
        display: inline-block;
        background: white;
        border: 1.5px solid #c7d2fe;
        border-radius: 999px;
        padding: 8px 14px;
        margin: 5px 4px;
        font-size: 16px;
        font-weight: 900;
        color: #3730a3;
        box-shadow: 0 3px 8px rgba(55,48,163,0.06);
    }

    .tool-label {
        display: inline-block;
        background: #eef6ff;
        color: #1d4ed8;
        border-radius: 999px;
        padding: 7px 13px;
        font-size: 16px;
        font-weight: 900;
        margin-bottom: 10px;
        border: 1px solid #bfdbfe;
    }

    .word-chip {
        display: inline-block;
        background: linear-gradient(135deg, #eef6ff, #ffffff);
        border: 1.5px solid #cfe2ff;
        border-radius: 999px;
        padding: 9px 16px;
        margin: 6px;
        font-size: 18px;
        font-weight: 800;
        color: #1f4e79;
        box-shadow: 0 3px 8px rgba(31,78,121,0.08);
    }

    button[data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 800;
    }

    table {
        font-size: 18px !important;
        border-radius: 14px;
        overflow: hidden;
    }

    thead tr th {
        background-color: #eef6ff !important;
        color: #1f4e79 !important;
        font-weight: 900 !important;
    }

    tbody tr td {
        background-color: #ffffff !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 18px;
        font-size: 18px;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 800;
        padding: 0.45rem 1.1rem;
        border: 1.5px solid #d9e7ff;
    }

    .stButton > button:hover {
        border-color: #60a5fa;
        color: #2563eb;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 상단 제목
# =========================================================
st.markdown(
    """
    <div class="title-box">
        <h1>🛟 Survival Sentence Guide</h1>
        <p>
            영어 문법을 외우는 것이 아니라,<br>
            실제 상황에서 살아남기 위한 문장 구조를 순서대로 익혀 봅시다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="path-box">
        <h3>🧭 생존 문장 구조 학습 순서</h3>
        <p>
            이 수업은 문법 이름을 외우는 순서가 아니라,
            <b>실제 상황에서 필요한 말부터</b> 익히는 순서입니다.
        </p>
        <span class="mission-chip">1. 나와 상태 말하기</span>
        <span class="mission-chip">2. 지금 하는 일 말하기</span>
        <span class="mission-chip">3. 앞으로 할 일 말하기</span>
        <span class="mission-chip">4. 지난 일 말하기</span>
        <span class="mission-chip">5. 아니라고 말하기</span>
        <span class="mission-chip">6. 물어보기</span>
        <span class="mission-chip">7. 자세히 물어보기</span>
    </div>
    """,
    unsafe_allow_html=True
)


tabs = st.tabs([
    "🙋 나와 상태 말하기",
    "🏃 지금 하는 일 말하기",
    "🚀 앞으로 할 일 말하기",
    "🕰️ 지난 일 말하기",
    "🎮 지난 일 단어 게임",
    "❌ 아니라고 말하기",
    "❓ 간단히 물어보기",
    "🕵️ 자세히 물어보기"
])


# =========================================================
# Tab 1: be동사 / 행동 표현
# =========================================================
with tabs[0]:
    st.subheader("🙋 나와 상태 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#f3f8ff,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: 나를 말하는 말 / 행동을 말하는 말</span>
            <h3 style="color:#1f4e79;">🙋 생존의 첫 문장: 나는 누구이고, 어떤 상태인가?</h3>
            <p>
                낯선 상황에서 가장 먼저 필요한 말은 <b>나를 소개하고, 내 상태를 말하는 것</b>입니다.
                <b>am, are, is</b>를 알면 “나는 학생이다”, “나는 배고프다”, “괜찮다” 같은 기본 문장을 만들 수 있습니다.
            </p>
            <div class="example-box">
                <b>I am hungry.</b><br>
                → 나는 배고프다.<br><br>
                <b>I am a student.</b><br>
                → 나는 학생이다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success("be동사에는 am, are, is가 있습니다.")

    st.markdown("### ✅ 나와 상태를 말할 때 be동사 고르는 법")

    st.markdown(
        """
        <div class="mini-card">
            <h4>🌷 1. is</h4>
            <p>주어가 <b>1개</b>일 때 씁니다.</p>
            <div class="example-box">
                He <b>is</b> kind.<br>
                She <b>is</b> happy.<br>
                It <b>is</b> a dog.
            </div>
        </div>

        <div class="mini-card">
            <h4>🌈 2. are</h4>
            <p>주어가 <b>2개 이상</b>이거나 <b>you / we / they</b>일 때 씁니다.</p>
            <div class="example-box">
                You <b>are</b> my friend.<br>
                We <b>are</b> students.<br>
                They <b>are</b> happy.
            </div>
        </div>
                <div class="mini-card">
            <h4>🌱 3. am</h4>
            <p>주어가 <b>I</b>일 때 씁니다. '나'는 1명이지만 나는 특별하기에 다른 것들과 차별을 두기 위해서 'is'가 아닌 'am'을 씁니다.</p>
            <div class="example-box">
                I <b>am</b> a student.<br>
                → 나는 학생이다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 행동을 말할 때 쓰는 행동 표현")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#fffdf4,#ffffff);">
            <p>
                <b>be동사 am, are, is를 제외한 나머지 동작 표현</b>은 대부분 행동 표현입니다.
            </p>
            <p>예를 들면 다음과 같습니다.</p>
            <span class="word-chip">do 하다</span>
            <span class="word-chip">play 놀다 / 경기하다</span>
            <span class="word-chip">sleep 자다</span>
            <span class="word-chip">eat 먹다</span>
            <span class="word-chip">go 가다</span>
            <span class="word-chip">study 공부하다</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# Tab 2: 현재진행형
# =========================================================
with tabs[1]:
    st.subheader("🏃 지금 하는 일 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#fff8e6,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: 지금 하는 일을 말하는 모양</span>
            <h3 style="color:#8a5a00;">🏃 지금 무슨 일이 일어나고 있는지 말하기</h3>
            <p>
                생존 상황에서는 “지금 기다리고 있어요”, “지금 먹고 있어요”, “지금 가고 있어요”처럼
                <b>현재 상황</b>을 말할 수 있어야 합니다.
            </p>
            <div class="formula-box" style="color:#8a5a00;">
                am / are / is + 동사 + ing
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 지금 하는 일을 만드는 법")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>am / are / is + 동사 + ing</b></p>
        </div>

        <div class="example-box">
            I <b>am eating</b> lunch.<br>
            → 나는 점심을 먹고 있다.
        </div>

        <div class="example-box">
            She <b>is reading</b> a book.<br>
            → 그녀는 책을 읽고 있다.
        </div>

        <div class="example-box">
            They <b>are playing</b> soccer.<br>
            → 그들은 축구를 하고 있다.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# Tab 3: 미래형
# =========================================================
# Tab 3: 미래형
# =========================================================
with tabs[2]:
    st.subheader("🚀 앞으로 할 일 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#ecfff1,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: 앞으로 할 일을 말하는 모양</span>
            <h3 style="color:#247a3d;">🚀 앞으로 할 일 말하기</h3>
            <p>
                약속을 잡거나 계획을 말할 때는 <b>앞으로 할 일</b>을 표현해야 합니다.
                “갈 거예요”, “전화할게요”, “도와줄게요” 같은 말이 여기에 들어갑니다.
            </p>
            <div class="formula-box" style="color:#247a3d;">
                will + 동사 / be going to + 동사
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. 바로 할 일을 말할 때: will")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>will + 동사의 기본 모양</b></p>
            <p>will 뒤에는 동사를 바로 씁니다.</p>
        </div>

        <div class="example-box">
            I <b>will study</b> English.<br>
            → 나는 영어를 공부할 것이다.
        </div>

        <div class="example-box">
            She <b>will call</b> me.<br>
            → 그녀는 나에게 전화할 것이다.
        </div>

        <div class="example-box">
            We <b>will go</b> to Busan.<br>
            → 우리는 부산에 갈 것이다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 계획된 일을 말할 때: be going to")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>am / are / is + going to + 동사의 기본 모양</b></p>
            <p><b>be going to</b>도 앞으로 할 일을 말할 때 씁니다.</p>
            <p>주어에 맞게 <b>am, are, is</b>를 골라 씁니다.</p>
        </div>

        <div class="example-box">
            I <b>am going to study</b> English.<br>
            → 나는 영어를 공부할 예정이다.
        </div>

        <div class="example-box">
            She <b>is going to call</b> me.<br>
            → 그녀는 나에게 전화할 예정이다.
        </div>

        <div class="example-box">
            We <b>are going to go</b> to Busan.<br>
            → 우리는 부산에 갈 예정이다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 3. 앞으로 할 일 표현 비교")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>will</b>과 <b>be going to</b>는 둘 다 미래를 나타냅니다.</p>
            <p>처음 배울 때는 둘 다 <b>~할 것이다 / ~할 예정이다</b> 정도로 이해하면 됩니다.</p>
        </div>

        <div class="example-box">
            I <b>will study</b> English.<br>
            → 나는 영어를 공부할 것이다.
        </div>

        <div class="example-box">
            I <b>am going to study</b> English.<br>
            → 나는 영어를 공부할 예정이다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: will 뒤에도 동사, be going to 뒤에도 동사가 바로 옵니다.")

# =========================================================
# Tab 4: 과거형
# =========================================================
with tabs[3]:
    st.subheader("🕰️ 지난 일 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#fff0f6,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: 지난 일을 말하는 모양</span>
            <h3 style="color:#9b2c5a;">🕰️ 이미 일어난 일 말하기</h3>
            <p>
                무슨 일이 있었는지 설명하려면 <b>지난 일</b>을 말할 수 있어야 합니다.
                “어제 갔어요”, “먹었어요”, “봤어요” 같은 문장이 필요합니다.
            </p>
            <div class="formula-box" style="color:#9b2c5a;">
                규칙동사: 동사 + ed / 불규칙동사: 따로 익히기
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 지난 일을 말하는 기본 방법")

    st.markdown(
        """
        <div class="mini-card">
            <p>규칙동사는 보통 동사 뒤에 <b>-ed</b>를 붙입니다.</p>
        </div>

        <div class="example-box">
            play → <b>played</b><br>
            I <b>played</b> soccer yesterday.<br>
            → 나는 어제 축구를 했다.
        </div>

        <div class="example-box">
            walk → <b>walked</b><br>
            She <b>walked</b> to school.<br>
            → 그녀는 학교에 걸어갔다.
        </div>

        <div class="example-box">
            clean → <b>cleaned</b><br>
            We <b>cleaned</b> the room.<br>
            → 우리는 방을 청소했다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ⭐ 자주 쓰는 지난 일 표현: 불규칙동사")

    st.warning("모든 동사에 -ed를 붙이는 것은 아닙니다. 불규칙동사는 따로 외워야 합니다.")

    st.markdown(
        """
        | 현재형 | 과거형 | 뜻 |
        |---|---|---|
        | go | went | 가다 |
        | eat | ate | 먹다 |
        | see | saw | 보다 |
        | have | had | 가지다 / 먹다 |
        | make | made | 만들다 |
        | come | came | 오다 |
        | do | did | 하다 |
        | take | took | 가져가다 / 타다 |
        | write | wrote | 쓰다 |
        | read | read | 읽다 |
        """
    )

    st.info("Tip: 불규칙동사는 바로 옆의 🎮 불규칙동사 게임 탭에서 재미있게 연습할 수 있습니다.")


# =========================================================
# Tab 5: 불규칙동사 게임
# =========================================================
with tabs[4]:
    st.subheader("🎮 지난 일 단어 게임")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#fffbe6,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: 지난 일을 말할 때 자주 쓰는 단어</span>
            <h3 style="color:#8a6d00;">🎲 지난 일을 말하려면 꼭 필요한 단어들</h3>
            <p>
                “갔다”, “먹었다”, “봤다”, “샀다”처럼 자주 쓰는 말은 과거형 모양이 따로 바뀝니다.
                생존 영어에서는 이런 단어들을 먼저 익히는 것이 중요합니다.
            </p>
            <div class="formula-box" style="color:#8a6d00;">
                go → went / eat → ate / see → saw
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("먼저 카드로 외우고, 그다음 직접 맞혀 보세요!")

    irregular_verbs = [
        {"base": "be", "past": "was / were", "meaning": "~이다 / 있다"},
        {"base": "become", "past": "became", "meaning": "~이 되다"},
        {"base": "begin", "past": "began", "meaning": "시작하다"},
        {"base": "break", "past": "broke", "meaning": "깨다 / 부수다"},
        {"base": "bring", "past": "brought", "meaning": "가져오다"},
        {"base": "build", "past": "built", "meaning": "짓다 / 만들다"},
        {"base": "buy", "past": "bought", "meaning": "사다"},
        {"base": "catch", "past": "caught", "meaning": "잡다"},
        {"base": "choose", "past": "chose", "meaning": "고르다"},
        {"base": "come", "past": "came", "meaning": "오다"},
        {"base": "cut", "past": "cut", "meaning": "자르다"},
        {"base": "do", "past": "did", "meaning": "하다"},
        {"base": "draw", "past": "drew", "meaning": "그리다"},
        {"base": "drink", "past": "drank", "meaning": "마시다"},
        {"base": "drive", "past": "drove", "meaning": "운전하다"},
        {"base": "eat", "past": "ate", "meaning": "먹다"},
        {"base": "fall", "past": "fell", "meaning": "떨어지다 / 넘어지다"},
        {"base": "feel", "past": "felt", "meaning": "느끼다"},
        {"base": "find", "past": "found", "meaning": "찾다 / 발견하다"},
        {"base": "fly", "past": "flew", "meaning": "날다"},
        {"base": "forget", "past": "forgot", "meaning": "잊다"},
        {"base": "get", "past": "got", "meaning": "얻다 / 받다 / 되다"},
        {"base": "give", "past": "gave", "meaning": "주다"},
        {"base": "go", "past": "went", "meaning": "가다"},
        {"base": "grow", "past": "grew", "meaning": "자라다 / 기르다"},
        {"base": "have", "past": "had", "meaning": "가지다 / 먹다"},
        {"base": "hear", "past": "heard", "meaning": "듣다"},
        {"base": "hold", "past": "held", "meaning": "잡다 / 열다"},
        {"base": "keep", "past": "kept", "meaning": "유지하다 / 보관하다"},
        {"base": "know", "past": "knew", "meaning": "알다"},
        {"base": "leave", "past": "left", "meaning": "떠나다 / 남기다"},
        {"base": "lose", "past": "lost", "meaning": "잃다 / 지다"},
        {"base": "make", "past": "made", "meaning": "만들다"},
        {"base": "meet", "past": "met", "meaning": "만나다"},
        {"base": "pay", "past": "paid", "meaning": "지불하다"},
        {"base": "put", "past": "put", "meaning": "놓다 / 두다"},
        {"base": "read", "past": "read", "meaning": "읽다"},
        {"base": "ride", "past": "rode", "meaning": "타다"},
        {"base": "run", "past": "ran", "meaning": "달리다"},
        {"base": "say", "past": "said", "meaning": "말하다"},
        {"base": "see", "past": "saw", "meaning": "보다"},
        {"base": "sell", "past": "sold", "meaning": "팔다"},
        {"base": "send", "past": "sent", "meaning": "보내다"},
        {"base": "sing", "past": "sang", "meaning": "노래하다"},
        {"base": "sit", "past": "sat", "meaning": "앉다"},
        {"base": "sleep", "past": "slept", "meaning": "자다"},
        {"base": "speak", "past": "spoke", "meaning": "말하다"},
        {"base": "spend", "past": "spent", "meaning": "쓰다 / 보내다"},
        {"base": "stand", "past": "stood", "meaning": "서다"},
        {"base": "swim", "past": "swam", "meaning": "수영하다"},
    ]

    game_tabs = st.tabs([
        "🃏 카드로 외우기",
        "✏️ 직접 맞히기",
        "📋 전체 리스트"
    ])

    with game_tabs[0]:
        st.markdown("### 🃏 카드로 외우기")
        st.caption("버튼을 누르면 불규칙동사가 하나씩 나옵니다.")

        if "verb_card_index" not in st.session_state:
            st.session_state.verb_card_index = 0

        current = irregular_verbs[st.session_state.verb_card_index]

        st.markdown(
            f"""
            <div style="
                background:linear-gradient(135deg,#eef5ff,#ffffff);
                border-radius:30px;
                padding:32px;
                margin:20px 0;
                text-align:center;
                box-shadow:0 8px 22px rgba(0,0,0,0.08);
                border:1.5px solid #d7e8ff;
            ">
                <p style="font-size:20px; color:#666; margin-bottom:8px;">현재형</p>
                <h1 style="font-size:48px; color:#1f4e79; margin:8px 0;">{current["base"]}</h1>
                <p style="font-size:20px; color:#666; margin-bottom:8px;">과거형</p>
                <h1 style="font-size:48px; color:#d46b08; margin:8px 0;">{current["past"]}</h1>
                <p style="font-size:23px; color:#333; margin-top:18px;">
                    뜻: <b>{current["meaning"]}</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            f"현재 카드: **{st.session_state.verb_card_index + 1} / {len(irregular_verbs)}**"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅️ 이전 카드"):
                st.session_state.verb_card_index -= 1

                if st.session_state.verb_card_index < 0:
                    st.session_state.verb_card_index = len(irregular_verbs) - 1

                st.rerun()

        with col2:
            if st.button("다음 카드 ➡️"):
                st.session_state.verb_card_index += 1

                if st.session_state.verb_card_index >= len(irregular_verbs):
                    st.session_state.verb_card_index = 0

                st.rerun()

    with game_tabs[1]:
        st.markdown("### ✏️ 직접 맞히기")
        st.caption("현재형을 보고 과거형을 직접 입력해 봅시다.")

        if "verb_quiz_index" not in st.session_state:
            st.session_state.verb_quiz_index = 0

        if "verb_score" not in st.session_state:
            st.session_state.verb_score = 0

        if "verb_answer_checked" not in st.session_state:
            st.session_state.verb_answer_checked = False

        quiz_item = irregular_verbs[st.session_state.verb_quiz_index]

        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border-radius:26px;
                padding:26px;
                margin:18px 0;
                text-align:center;
                box-shadow:0 6px 16px rgba(0,0,0,0.07);
                border:1.5px solid #eeeeee;
            ">
                <p style="font-size:20px; color:#666;">다음 동사의 과거형은?</p>
                <h1 style="font-size:46px; color:#1f4e79;">{quiz_item["base"]}</h1>
                <p style="font-size:20px;">뜻: <b>{quiz_item["meaning"]}</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

        user_answer = st.text_input(
            "과거형을 입력하세요.",
            key=f"verb_input_{st.session_state.verb_quiz_index}"
        )

        if st.button("정답 확인"):
            st.session_state.verb_answer_checked = True

            correct_answer = quiz_item["past"].replace(" ", "").lower()
            user_clean = user_answer.strip().replace(" ", "").lower()

            if user_clean == correct_answer:
                st.success("정답입니다! 아주 좋아요 🎉")
                st.balloons()
                st.session_state.verb_score += 1
            else:
                st.error("아쉽습니다. 다시 확인해 봅시다.")
                st.write(f"정답은 **{quiz_item['past']}** 입니다.")

        if st.session_state.verb_answer_checked:
            if st.button("다음 문제"):
                st.session_state.verb_quiz_index += 1
                st.session_state.verb_answer_checked = False

                if st.session_state.verb_quiz_index >= len(irregular_verbs):
                    st.session_state.verb_quiz_index = 0
                    st.success("한 바퀴를 모두 끝냈습니다! 다시 처음부터 연습합니다.")

                st.rerun()

        st.markdown("---")
        st.write(f"현재 문제: **{st.session_state.verb_quiz_index + 1} / {len(irregular_verbs)}**")
        st.write(f"현재 점수: **{st.session_state.verb_score}점**")

        if st.button("점수 초기화"):
            st.session_state.verb_score = 0
            st.session_state.verb_quiz_index = 0
            st.session_state.verb_answer_checked = False
            st.rerun()

    with game_tabs[2]:
        st.markdown("### 📋 자주 나오는 불규칙동사 50개")
        st.caption("10개씩 나누어 보면서 익혀 봅시다.")

        for i in range(0, len(irregular_verbs), 10):
            st.markdown(f"#### {i + 1}번 ~ {min(i + 10, len(irregular_verbs))}번")

            table_text = "| 현재형 | 과거형 | 뜻 |\n|---|---|---|\n"

            for verb in irregular_verbs[i:i + 10]:
                table_text += f"| {verb['base']} | {verb['past']} | {verb['meaning']} |\n"

            st.markdown(table_text)

        st.info("먼저 카드로 외우고, 그다음 직접 맞히기를 하면 훨씬 잘 기억납니다.")


# =========================================================
# Tab 6: 아니라고 말하는 문장
# =========================================================
with tabs[5]:
    st.subheader("❌ 아니라고 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#fff3f3,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: 아니라고 말하는 not</span>
            <h3 style="color:#b23a3a;">❌ 아니라고 말하기</h3>
            <p>
                생존 상황에서는 거절하거나, 모른다고 하거나, 아프지 않다고 말해야 할 때가 있습니다.
                이때 필요한 것이 <b>not</b>입니다.
            </p>
            <div class="formula-box" style="color:#b23a3a;">
                be동사 + not / do not + 동사의 기본 모양
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. 상태를 아니라고 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>be동사 + not</b></p>
            <p>am, are, is 뒤에 <b>not</b>을 붙입니다.</p>
        </div>

        <div class="example-box">
            I <b>am not</b> a student.<br>
            → 나는 학생이 아니다.
        </div>

        <div class="example-box">
            She <b>is not</b> happy.<br>
            → 그녀는 행복하지 않다.
        </div>

        <div class="example-box">
            They <b>are not</b> busy.<br>
            → 그들은 바쁘지 않다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 행동을 안 한다고 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>do not / does not / did not + 동사</b></p>
            <p>행동 표현는 바로 not을 붙이지 않고 <b>do, does, did</b>의 도움을 받습니다.</p>
        </div>

        <div class="example-box">
            I <b>do not like</b> coffee.<br>
            → 나는 커피를 좋아하지 않는다.
        </div>

        <div class="example-box">
            He <b>does not play</b> soccer.<br>
            → 그는 축구를 하지 않는다.
        </div>

        <div class="example-box">
            They <b>did not go</b> to school yesterday.<br>
            → 그들은 어제 학교에 가지 않았다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: does not, did not 뒤에는 동사를 바로 씁니다. 예: does not plays ❌ / does not play ✅")


# =========================================================
# Tab 7: 질문하는 문장
# =========================================================
with tabs[6]:
    st.subheader("❓ 간단히 물어보기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#f3f0ff,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: 짧게 확인하는 질문</span>
            <h3 style="color:#5b3aa4;">❓ 간단히 물어보기</h3>
            <p>
                “괜찮니?”, “필요하니?”, “먹었니?”처럼 짧게 확인하는 질문은 실제 대화에서 매우 자주 씁니다.
                질문을 만들 때는 <b>문장 앞에 오는 단어</b>가 중요합니다.
            </p>
            <div class="formula-box" style="color:#5b3aa4;">
                be동사 + 주어? / Do, Does, Did + 주어 + 동사의 기본 모양?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. 상태를 확인하는 질문")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>be동사 + 주어 ~ ?</b></p>
            <p>am, are, is를 문장 앞으로 보냅니다.</p>
        </div>

        <div class="example-box">
            You are a student.<br>
            ↓<br>
            <b>Are you</b> a student?<br>
            → 너는 학생이니?
        </div>

        <div class="example-box">
            She is happy.<br>
            ↓<br>
            <b>Is she</b> happy?<br>
            → 그녀는 행복하니?
        </div>

        <div class="example-box">
            They are in the classroom.<br>
            ↓<br>
            <b>Are they</b> in the classroom?<br>
            → 그들은 교실에 있니?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 행동을 확인하는 질문")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>Do / Does / Did + 주어 + 동사 ~ ?</b></p>
            <p>행동 표현 질문하는 문장은 <b>Do, Does, Did</b>를 문장 앞에 씁니다.</p>
        </div>

        <div class="example-box">
            You like coffee.<br>
            ↓<br>
            <b>Do you like</b> coffee?<br>
            → 너는 커피를 좋아하니?
        </div>

        <div class="example-box">
            He plays soccer.<br>
            ↓<br>
            <b>Does he play</b> soccer?<br>
            → 그는 축구를 하니?
        </div>

        <div class="example-box">
            They went to school yesterday.<br>
            ↓<br>
            <b>Did they go</b> to school yesterday?<br>
            → 그들은 어제 학교에 갔니?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: Does, Did가 앞에 오면 뒤의 동사는 s나 ed를 붙이지 않습니다. 예: Does he plays? ❌ / Does he play? ✅")

# Tab 7: 자세한 질문
# =========================================================
with tabs[7]:
    st.subheader("🕵️ 자세히 물어보기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#e0f7ff,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: 자세히 묻는 질문 단어</span>
            <h3 style="color:#0477a8;">🕵️ 자세히 물어보기</h3>
            <p>
                단순히 yes/no로 끝나는 질문보다 더 중요한 질문도 있습니다.
                “어디예요?”, “언제예요?”, “무엇을 원하세요?”, “어떻게 가나요?”처럼
                <b>자세한 정보를 묻는 문장</b>입니다.
            </p>
            <div class="formula-box" style="color:#0477a8;">
                질문 단어 + 질문
            </div>
            <p style="margin-top:14px;">
                쉽게 말하면, <b>이미 만든 질문하는 문장 앞에 What, When, Where, Who, Why, How를 붙이면 됩니다.</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. 자세히 물을 때 필요한 말")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>What</b> = 무엇</p>
            <p><b>When</b> = 언제</p>
            <p><b>Where</b> = 어디에 / 어디에서</p>
            <p><b>Who</b> = 누구</p>
            <p><b>Why</b> = 왜</p>
            <p><b>How</b> = 어떻게</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 자세한 질문 만드는 방법")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>질문 단어 + 질문</b></p>
            <p>
                be동사 질문하는 문장이든, 행동 표현 질문하는 문장이든
                <b>완성된 질문하는 문장 앞에 What, When, Where, Who, Why, How를 붙이면 됩니다.</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 3. 상태를 자세히 물어보기")

    st.markdown(
        """
        <div class="example-box">
            Are you happy?<br>
            ↓<br>
            <b>Why are you happy?</b><br>
            → 너는 왜 행복하니?
        </div>

        <div class="example-box">
            Is she in the classroom?<br>
            ↓<br>
            <b>Where is she?</b><br>
            → 그녀는 어디에 있니?
        </div>

        <div class="example-box">
            Are they here?<br>
            ↓<br>
            <b>Why are they here?</b><br>
            → 그들은 왜 여기에 있니?
        </div>

        <div class="example-box">
            Is he your brother?<br>
            ↓<br>
            <b>Who is he?</b><br>
            → 그는 누구니?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 4. 행동을 자세히 물어보기")

    st.markdown(
        """
        <div class="example-box">
            Do you like pizza?<br>
            ↓<br>
            <b>What do you like?</b><br>
            → 너는 무엇을 좋아하니?
        </div>

        <div class="example-box">
            Does he play soccer after school?<br>
            ↓<br>
            <b>When does he play soccer?</b><br>
            → 그는 언제 축구를 하니?
        </div>

        <div class="example-box">
            Did they go to school yesterday?<br>
            ↓<br>
            <b>When did they go to school?</b><br>
            → 그들은 언제 학교에 갔니?
        </div>

        <div class="example-box">
            Do you study English at school?<br>
            ↓<br>
            <b>Where do you study English?</b><br>
            → 너는 어디에서 영어를 공부하니?
        </div>

        <div class="example-box">
            Does she like him?<br>
            ↓<br>
            <b>Why does she like him?</b><br>
            → 그녀는 왜 그를 좋아하니?
        </div>

        <div class="example-box">
            Do you go to school by bus?<br>
            ↓<br>
            <b>How do you go to school?</b><br>
            → 너는 어떻게 학교에 가니?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 5. 생존 질문 예문 정리")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>What do you want?</b> → 너는 무엇을 원하니?</p>
            <p><b>When do you get up?</b> → 너는 언제 일어나니?</p>
            <p><b>Where do you live?</b> → 너는 어디에 사니?</p>
            <p><b>Who is he?</b> → 그는 누구니?</p>
            <p><b>Why are you sad?</b> → 너는 왜 슬프니?</p>
            <p><b>How do you feel?</b> → 너는 기분이 어떠니?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Tip: 자세한 질문은 어렵게 생각하지 말고, 이미 만든 질문하는 문장 앞에 What, When, Where, Who, Why, How 같은 말을 붙이면 됩니다."
    )
