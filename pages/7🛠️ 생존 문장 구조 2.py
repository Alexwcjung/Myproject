import streamlit as st

st.set_page_config(page_title="Survival Sentence Builder 2", page_icon="🛠️", layout="centered")

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
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 50%, #f7fee7 100%);
        padding: 34px 30px;
        border-radius: 32px;
        margin-bottom: 28px;
        box-shadow: 0 10px 26px rgba(80, 80, 120, 0.12);
        text-align: center;
        border: 1.5px solid #e0f2fe;
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
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 50%, #f7fee7 100%);
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
        border: 1.5px solid #bbf7d0;
        border-radius: 999px;
        padding: 8px 14px;
        margin: 5px 4px;
        font-size: 16px;
        font-weight: 900;
        color: #166534;
        box-shadow: 0 3px 8px rgba(22,101,52,0.06);
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
        <h1>🛠️ Survival Sentence Builder 2</h1>
        <p>
            이제는 더 실제 상황으로 갑니다.<br>
            할 수 있는 일 말하기, 부탁하기, 위치 말하기, 원하는 것 말하기, 문장 연결하기까지 익혀 봅시다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="path-box">
        <h3>🧭 생존 문장 확장 순서</h3>
        <p>
            앞에서 기본 문장을 만들었다면, 이제는 실제 상황에서 더 많이 쓰는 표현을 배웁니다.
            <b>할 수 있다, 해 주세요, 어디에 있다, 원한다, 가지고 있다, 이유를 말한다</b> 같은 말이 핵심입니다.
        </p>
        <span class="mission-chip">1. 할 수 있는 일 말하기</span>
        <span class="mission-chip">2. 부탁하고 지시하기</span>
        <span class="mission-chip">3. 위치 말하기</span>
        <span class="mission-chip">4. 원하는 것 말하기</span>
        <span class="mission-chip">5. 하고 싶은 일 말하기</span>
        <span class="mission-chip">6. 가진 것 말하기</span>
        <span class="mission-chip">7. 이유와 조건 붙이기</span>
    </div>
    """,
    unsafe_allow_html=True
)


tabs = st.tabs([
    "💪 할 수 있는 일 말하기",
    "📢 부탁하고 지시하기",
    "📍 어디에 있는지 말하기",
    "🧭 위치 자세히 말하기",
    "💭 원하는 것 말하기",
    "🚀 하고 싶은 일 말하기",
    "🎒 가진 것 말하기",
    "🔗 이유와 조건 붙이기"
])


# =========================================================
# Tab 1: can 
# =========================================================
with tabs[0]:
    st.subheader("💪 할 수 있는 일 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#eef6ff,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: can</span>
            <h3 style="color:#1d4ed8;">💪 할 수 있는 일 말하기</h3>
            <p>
                실제 상황에서는 “할 수 있어요”, “도와줄 수 있어요”, “영어를 조금 말할 수 있어요” 같은 말이 자주 필요합니다.
                <b>can</b>을 쓰면 내가 할 수 있는 일이나 가능한 일을 쉽게 말할 수 있습니다.
            </p>
            <div class="formula-box" style="color:#1d4ed8;">
                can + 동사
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. 할 수 있다고 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>can 뒤에는 동사</b>을 씁니다.</p>
            <p>can swims ❌ / can swim ✅</p>
        </div>

        <div class="example-box">
            I <b>can swim</b>.<br>
            → 나는 수영할 수 있다.
        </div>

        <div class="example-box">
            She <b>can sing</b>.<br>
            → 그녀는 노래할 수 있다.
        </div>

        <div class="example-box">
            They <b>can play</b> soccer.<br>
            → 그들은 축구를 할 수 있다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 할 수 없다고 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>cannot / can't + 동사</b></p>
            <p><b>cannot</b>은 <b>~할 수 없다</b>라는 뜻입니다.</p>
        </div>

        <div class="example-box">
            I <b>cannot swim</b>.<br>
            → 나는 수영할 수 없다.
        </div>

        <div class="example-box">
            He <b>can't speak</b> English.<br>
            → 그는 영어를 말할 수 없다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 3. 할 수 있는지 물어보기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>Can + 사람 + 동사 ~ ?</b></p>
            <p>물어볼 때는 <b>Can</b>으로 시작합니다.</p>
        </div>

        <div class="example-box">
            You can swim.<br>
            ↓<br>
            <b>Can you swim?</b><br>
            → 너는 수영할 수 있니?
        </div>

        <div class="example-box">
            She can play the piano.<br>
            ↓<br>
            <b>Can she play</b> the piano?<br>
            → 그녀는 피아노를 칠 수 있니?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: can 뒤에는 항상 동사을 씁니다. 예: can plays ❌ / can play ✅")


# =========================================================
# Tab 2: 부탁하거나 지시하는 말
# =========================================================
with tabs[1]:
    st.subheader("📢 부탁하고 지시하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#fff7ed,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: 동사로 시작하기</span>
            <h3 style="color:#c2410c;">📢 부탁하고 지시하기</h3>
            <p>
                길을 알려 주거나, 조심하라고 말하거나, 교실에서 활동을 안내할 때는 짧고 분명한 말이 필요합니다.
                이때는 <b>Open, Listen, Stand, Don't run</b>처럼 바로 행동을 말합니다.
            </p>
            <div class="formula-box" style="color:#c2410c;">
                Open / Listen / Don't run
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. 해 달라고 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>동사 ~.</b></p>
            <p>말하는 대상 You를 쓰지 않고, 바로 동사로 시작합니다.</p>
        </div>

        <div class="example-box">
            <b>Open</b> the door.<br>
            → 문을 열어라.
        </div>

        <div class="example-box">
            <b>Listen</b> carefully.<br>
            → 주의 깊게 들어라.
        </div>

        <div class="example-box">
            <b>Stand</b> up.<br>
            → 일어서라.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 부정 부탁하거나 지시하는 말")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>Don't + 동사 ~.</b></p>
            <p><b>~하지 마라</b>라고 말할 때 씁니다.</p>
        </div>

        <div class="example-box">
            <b>Don't run</b> in the classroom.<br>
            → 교실에서 뛰지 마라.
        </div>

        <div class="example-box">
            <b>Don't touch</b> this.<br>
            → 이것을 만지지 마라.
        </div>

        <div class="example-box">
            <b>Don't be</b> late.<br>
            → 늦지 마라.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: 부탁하거나 지시하는 말은 보통 말하는 대상 You를 생략하고 동사로 시작합니다.")


# =========================================================
# Tab 3: There is / There are
# =========================================================
with tabs[2]:
    st.subheader("📍 어디에 있는지 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#ecfdf5,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: There is / There are</span>
            <h3 style="color:#047857;">📍 어디에 무엇이 있는지 말하기</h3>
            <p>
                낯선 곳에서는 “책상이 있어요”, “사람들이 있어요”, “가게가 있어요”처럼
                <b>무엇이 있는지</b> 말하는 표현이 중요합니다.
            </p>
            <div class="formula-box" style="color:#047857;">
                There is + 하나 / There are + 여러 개
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. 하나가 있다고 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>There is + 하나</b></p>
            <p>한 사람 또는 한 물건이 있을 때 씁니다.</p>
        </div>

        <div class="example-box">
            <b>There is</b> a book on the desk.<br>
            → 책상 위에 책 한 권이 있다.
        </div>

        <div class="example-box">
            <b>There is</b> a student in the classroom.<br>
            → 교실에 학생 한 명이 있다.
        </div>

        <div class="example-box">
            <b>There is</b> a dog under the table.<br>
            → 탁자 아래에 개 한 마리가 있다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 여러 개가 있다고 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>There are + 두 개 이상</b></p>
            <p>사람이나 물건이 2개 이상 있을 때 씁니다.</p>
        </div>

        <div class="example-box">
            <b>There are</b> two books on the desk.<br>
            → 책상 위에 책 두 권이 있다.
        </div>

        <div class="example-box">
            <b>There are</b> three students in the classroom.<br>
            → 교실에 학생 세 명이 있다.
        </div>

        <div class="example-box">
            <b>There are</b> many cars on the street.<br>
            → 거리에 많은 자동차들이 있다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: 하나면 There is, 두 개 이상이면 There are를 씁니다.")


# =========================================================
# Tab 4: 위치를 알려주는 말
# =========================================================
with tabs[3]:
    st.subheader("🧭 위치 자세히 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#f5f3ff,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: in / on / under / next to</span>
            <h3 style="color:#6d28d9;">🧭 위치를 자세히 말하기</h3>
            <p>
                “어디에 있어요?”라는 질문에 답하려면 위치를 정확히 말할 수 있어야 합니다.
                <b>안에, 위에, 아래에, 옆에, 뒤에, 앞에</b>를 말하는 표현을 익혀 봅니다.
            </p>
            <div class="formula-box" style="color:#6d28d9;">
                in / on / under / next to / behind / in front of
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 자주 쓰는 위치 표현")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>in</b> = ~안에</p>
            <p><b>on</b> = ~위에</p>
            <p><b>under</b> = ~아래에</p>
            <p><b>next to</b> = ~옆에</p>
            <p><b>behind</b> = ~뒤에</p>
            <p><b>in front of</b> = ~앞에</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 위치를 문장으로 말하기")

    st.markdown(
        """
        <div class="example-box">
            The cat is <b>in</b> the box.<br>
            → 고양이는 상자 안에 있다.
        </div>

        <div class="example-box">
            The book is <b>on</b> the desk.<br>
            → 책은 책상 위에 있다.
        </div>

        <div class="example-box">
            The ball is <b>under</b> the chair.<br>
            → 공은 의자 아래에 있다.
        </div>

        <div class="example-box">
            The school is <b>next to</b> the park.<br>
            → 학교는 공원 옆에 있다.
        </div>

        <div class="example-box">
            The dog is <b>behind</b> the door.<br>
            → 개는 문 뒤에 있다.
        </div>

        <div class="example-box">
            The bus stop is <b>in front of</b> the school.<br>
            → 버스 정류장은 학교 앞에 있다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: 위치를 알려주는 말는 그림이나 교실 물건을 보면서 연습하면 훨씬 쉽게 익힐 수 있습니다.")


# =========================================================
# Tab 5: want
# =========================================================
with tabs[4]:
    st.subheader("💭 원하는 것 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#fff7ed,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: want</span>
            <h3 style="color:#c2410c;">💭 원하는 것 말하기</h3>
            <p>
                생존 영어에서 가장 중요한 말 중 하나는 “원해요”입니다.
                물, 음식, 휴대폰, 도움처럼 <b>필요하거나 원하는 것</b>을 말할 때 씁니다.
            </p>
            <div class="formula-box" style="color:#c2410c;">
                want + 원하는 것
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. want + 원하는 것")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>want 뒤에는 원하는 물건이나 대상을 씁니다.</b></p>
            <p>water, pizza, a bike, a phone 같은 말이 올 수 있습니다.</p>
        </div>

        <div class="example-box">
            I <b>want water</b>.<br>
            → 나는 물을 원한다.
        </div>

        <div class="example-box">
            You <b>want pizza</b>.<br>
            → 너는 피자를 원한다.
        </div>

        <div class="example-box">
            They <b>want a new phone</b>.<br>
            → 그들은 새 휴대전화를 원한다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 한 사람의 원하는 것 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p>말하는 대상가 <b>He / She / It</b>처럼 1명 또는 1개일 때는 보통 동사 뒤에 <b>-s</b>를 붙입니다.</p>
            <p><b>want → wants</b></p>
        </div>

        <div class="example-box">
            He <b>wants water</b>.<br>
            → 그는 물을 원한다.
        </div>

        <div class="example-box">
            She <b>wants a bike</b>.<br>
            → 그녀는 자전거를 원한다.
        </div>

        <div class="example-box">
            My brother <b>wants pizza</b>.<br>
            → 내 남동생은 피자를 원한다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: I, You, We, They는 want / He, She, It은 wants를 씁니다.")


# =========================================================
# Tab 6: want to
# =========================================================
with tabs[5]:
    st.subheader("🚀 하고 싶은 일 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#eef6ff,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: want to</span>
            <h3 style="color:#1d4ed8;">🚀 하고 싶은 일 말하기</h3>
            <p>
                “물을 원해요”에서 한 걸음 더 나아가 “물을 마시고 싶어요”, “집에 가고 싶어요”처럼
                <b>하고 싶은 행동</b>을 말해 봅니다.
            </p>
            <div class="formula-box" style="color:#1d4ed8;">
                want to + 동사
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. 하고 싶은 일 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>want to 뒤에는 동사</b>을 씁니다.</p>
            <p>want to eats ❌ / want to eat ✅</p>
        </div>

        <div class="example-box">
            I <b>want to eat</b>.<br>
            → 나는 먹고 싶다.
        </div>

        <div class="example-box">
            I <b>want to go</b> home.<br>
            → 나는 집에 가고 싶다.
        </div>

        <div class="example-box">
            We <b>want to play</b> soccer.<br>
            → 우리는 축구를 하고 싶다.
        </div>

        <div class="example-box">
            They <b>want to study</b> English.<br>
            → 그들은 영어를 공부하고 싶다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 한 사람의 원하는 것 말하기 to")

    st.markdown(
        """
        <div class="mini-card">
            <p>말하는 대상가 <b>He / She / It</b>이면 <b>wants to</b>를 씁니다.</p>
            <p>하지만 <b>to 뒤에는 s를 붙이지 않은 동사가 옵니다.</b></p>
        </div>

        <div class="example-box">
            He <b>wants to play</b> soccer.<br>
            → 그는 축구를 하고 싶다.
        </div>

        <div class="example-box">
            She <b>wants to sing</b>.<br>
            → 그녀는 노래하고 싶다.
        </div>

        <div class="example-box">
            My sister <b>wants to watch</b> TV.<br>
            → 내 여동생은 TV를 보고 싶다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 3. 원하는 것과 하고 싶은 일 비교")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>want + 원하는 것</b> = 무엇을 원하다</p>
            <p><b>want to + 동사</b> = ~하고 싶다</p>
        </div>

        <div class="example-box">
            I <b>want water</b>.<br>
            → 나는 물을 원한다.
        </div>

        <div class="example-box">
            I <b>want to drink</b> water.<br>
            → 나는 물을 마시고 싶다.
        </div>

        <div class="example-box">
            She <b>wants a bike</b>.<br>
            → 그녀는 자전거를 원한다.
        </div>

        <div class="example-box">
            She <b>wants to ride</b> a bike.<br>
            → 그녀는 자전거를 타고 싶다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: want 뒤에는 물건, want to 뒤에는 행동이 옵니다. 예: want pizza / want to eat pizza")


# =========================================================
# Tab 7: have / has
# =========================================================
with tabs[6]:
    st.subheader("🎒 가진 것 말하기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#ecfdf5,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: have / has</span>
            <h3 style="color:#047857;">🎒 가진 것 말하기</h3>
            <p>
                여행이나 학교생활에서는 내가 가진 물건, 친구, 가족, 필요한 물건을 말해야 할 때가 많습니다.
                이때 <b>have / has</b>를 씁니다.
            </p>
            <div class="formula-box" style="color:#047857;">
                I have / He has
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. 내가 가진 것 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>I / You / We / They</b> 뒤에는 보통 <b>have</b>를 씁니다.</p>
        </div>

        <div class="example-box">
            I <b>have a bike</b>.<br>
            → 나는 자전거를 가지고 있다.
        </div>

        <div class="example-box">
            You <b>have a phone</b>.<br>
            → 너는 휴대전화를 가지고 있다.
        </div>

        <div class="example-box">
            We <b>have many books</b>.<br>
            → 우리는 많은 책을 가지고 있다.
        </div>

        <div class="example-box">
            They <b>have a dog</b>.<br>
            → 그들은 개 한 마리를 가지고 있다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. 한 사람이 가진 것 말하기")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>He / She / It</b> 뒤에는 보통 <b>has</b>를 씁니다.</p>
            <p>have가 has로 바뀐다고 생각하면 됩니다.</p>
        </div>

        <div class="example-box">
            He <b>has a bike</b>.<br>
            → 그는 자전거를 가지고 있다.
        </div>

        <div class="example-box">
            She <b>has a dog</b>.<br>
            → 그녀는 개 한 마리를 가지고 있다.
        </div>

        <div class="example-box">
            My friend <b>has a new phone</b>.<br>
            → 내 친구는 새 휴대전화를 가지고 있다.
        </div>

        <div class="example-box">
            The school <b>has a gym</b>.<br>
            → 그 학교는 체육관을 가지고 있다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 3. 원한다 / 하고 싶다 / 가지고 있다 연결하기")

    st.markdown(
        """
        <div class="example-box">
            I <b>want water</b>.<br>
            → 나는 물을 원한다.
        </div>

        <div class="example-box">
            I <b>want to drink</b> water.<br>
            → 나는 물을 마시고 싶다.
        </div>

        <div class="example-box">
            I <b>have water</b>.<br>
            → 나는 물을 가지고 있다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: I, You, We, They는 have / He, She, It은 has를 씁니다.")


# =========================================================
# Tab 8: 문장 연결하기
# =========================================================
with tabs[7]:
    st.subheader("🔗 이유와 조건 붙이기")

    st.markdown(
        """
        <div class="grammar-card" style="background:linear-gradient(135deg,#fef9c3,#ffffff);">
            <span class="tool-label">오늘의 문장 도구: because / so / but / if</span>
            <h3 style="color:#a16207;">🔗 이유와 조건 붙이기</h3>
            <p>
                짧은 문장만 말해도 통하지만, 이유를 붙이면 훨씬 자연스럽습니다.
                “배고파서 먹고 싶어요”, “비가 오면 집에 있을게요”처럼 문장을 이어 봅니다.
            </p>
            <div class="formula-box" style="color:#a16207;">
                because / so / but / if
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ✅ 1. because = 왜냐하면")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>because</b>는 <b>왜냐하면</b>이라는 뜻입니다.</p>
            <p>이유를 말할 때 씁니다.</p>
        </div>

        <div class="example-box">
            I like English <b>because</b> it is fun.<br>
            → 나는 영어를 좋아한다. 왜냐하면 재미있기 때문이다.
        </div>

        <div class="example-box">
            She is happy <b>because</b> she has a dog.<br>
            → 그녀는 행복하다. 왜냐하면 개를 가지고 있기 때문이다.
        </div>

        <div class="example-box">
            I want water <b>because</b> I am thirsty.<br>
            → 나는 물을 원한다. 왜냐하면 목이 마르기 때문이다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 2. so = 그래서")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>so</b>는 <b>그래서</b>라는 뜻입니다.</p>
            <p>앞 문장 다음에 이어지는 일을 말할 때 씁니다.</p>
        </div>

        <div class="example-box">
            I am hungry, <b>so</b> I want pizza.<br>
            → 나는 배고프다. 그래서 피자를 원한다.
        </div>

        <div class="example-box">
            It is cold, <b>so</b> I wear a jacket.<br>
            → 날씨가 춥다. 그래서 나는 재킷을 입는다.
        </div>

        <div class="example-box">
            He is tired, <b>so</b> he goes home.<br>
            → 그는 피곤하다. 그래서 집에 간다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 3. but = 하지만")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>but</b>은 <b>하지만</b>이라는 뜻입니다.</p>
            <p>앞 문장과 반대되는 내용을 말할 때 씁니다.</p>
        </div>

        <div class="example-box">
            I like soccer, <b>but</b> I don't like baseball.<br>
            → 나는 축구를 좋아한다. 하지만 야구는 좋아하지 않는다.
        </div>

        <div class="example-box">
            She can sing, <b>but</b> she can't dance.<br>
            → 그녀는 노래할 수 있다. 하지만 춤은 출 수 없다.
        </div>

        <div class="example-box">
            I have a bike, <b>but</b> I don't have a car.<br>
            → 나는 자전거를 가지고 있다. 하지만 자동차는 가지고 있지 않다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 4. if = 만약 ~라면")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>if</b>는 <b>만약 ~라면</b>이라는 뜻입니다.</p>
            <p>어떤 일이 일어날 때를 상상해서 말할 때 씁니다.</p>
        </div>

        <div class="example-box">
            <b>If</b> it rains, I will stay home.<br>
            → 만약 비가 오면, 나는 집에 있을 것이다.
        </div>

        <div class="example-box">
            <b>If</b> I am hungry, I will eat pizza.<br>
            → 만약 내가 배고프면, 나는 피자를 먹을 것이다.
        </div>

        <div class="example-box">
            <b>If</b> you need help, I can help you.<br>
            → 만약 네가 도움이 필요하면, 내가 도와줄 수 있다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✅ 이어 주는 말 정리")

    st.markdown(
        """
        <div class="mini-card">
            <p><b>because</b> = 왜냐하면</p>
            <p><b>so</b> = 그래서</p>
            <p><b>but</b> = 하지만</p>
            <p><b>if</b> = 만약 ~라면</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Tip: 처음에는 because, so, but, if의 뜻만 알고 짧은 문장을 이어 보면 됩니다.")
