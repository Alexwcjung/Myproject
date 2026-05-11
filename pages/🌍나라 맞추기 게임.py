import streamlit as st
import random
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="세계 지도 나라 맞추기 게임",
    page_icon="🌍",
    layout="wide"
)

# =====================================================
# 나라 데이터
# iso_alpha는 Plotly 지도 표시용 국가 코드
# =====================================================
COUNTRIES = [
    {"ko": "대한민국", "en": "South Korea", "iso": "KOR"},
    {"ko": "일본", "en": "Japan", "iso": "JPN"},
    {"ko": "중국", "en": "China", "iso": "CHN"},
    {"ko": "미국", "en": "United States", "iso": "USA"},
    {"ko": "캐나다", "en": "Canada", "iso": "CAN"},
    {"ko": "멕시코", "en": "Mexico", "iso": "MEX"},
    {"ko": "브라질", "en": "Brazil", "iso": "BRA"},
    {"ko": "아르헨티나", "en": "Argentina", "iso": "ARG"},
    {"ko": "영국", "en": "United Kingdom", "iso": "GBR"},
    {"ko": "프랑스", "en": "France", "iso": "FRA"},
    {"ko": "독일", "en": "Germany", "iso": "DEU"},
    {"ko": "이탈리아", "en": "Italy", "iso": "ITA"},
    {"ko": "스페인", "en": "Spain", "iso": "ESP"},
    {"ko": "포르투갈", "en": "Portugal", "iso": "PRT"},
    {"ko": "러시아", "en": "Russia", "iso": "RUS"},
    {"ko": "인도", "en": "India", "iso": "IND"},
    {"ko": "태국", "en": "Thailand", "iso": "THA"},
    {"ko": "베트남", "en": "Vietnam", "iso": "VNM"},
    {"ko": "필리핀", "en": "Philippines", "iso": "PHL"},
    {"ko": "인도네시아", "en": "Indonesia", "iso": "IDN"},
    {"ko": "호주", "en": "Australia", "iso": "AUS"},
    {"ko": "뉴질랜드", "en": "New Zealand", "iso": "NZL"},
    {"ko": "이집트", "en": "Egypt", "iso": "EGY"},
    {"ko": "남아프리카공화국", "en": "South Africa", "iso": "ZAF"},
    {"ko": "케냐", "en": "Kenya", "iso": "KEN"},
    {"ko": "사우디아라비아", "en": "Saudi Arabia", "iso": "SAU"},
    {"ko": "튀르키예", "en": "Turkey", "iso": "TUR"},
    {"ko": "그리스", "en": "Greece", "iso": "GRC"},
]

# =====================================================
# 세션 상태 초기화
# =====================================================
if "score" not in st.session_state:
    st.session_state.score = 0

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "current_country" not in st.session_state:
    st.session_state.current_country = random.choice(COUNTRIES)

if "options" not in st.session_state:
    correct = st.session_state.current_country
    wrongs = random.sample(
        [c for c in COUNTRIES if c["ko"] != correct["ko"]],
        3
    )
    options = wrongs + [correct]
    random.shuffle(options)
    st.session_state.options = options

if "answered" not in st.session_state:
    st.session_state.answered = False

if "result_message" not in st.session_state:
    st.session_state.result_message = ""

# =====================================================
# 함수
# =====================================================
def make_new_question():
    st.session_state.current_country = random.choice(COUNTRIES)

    correct = st.session_state.current_country
    wrongs = random.sample(
        [c for c in COUNTRIES if c["ko"] != correct["ko"]],
        3
    )

    options = wrongs + [correct]
    random.shuffle(options)

    st.session_state.options = options
    st.session_state.answered = False
    st.session_state.result_message = ""


def reset_game():
    st.session_state.score = 0
    st.session_state.question_count = 0
    make_new_question()


def check_answer(selected_country):
    if st.session_state.answered:
        return

    st.session_state.answered = True
    st.session_state.question_count += 1

    correct = st.session_state.current_country

    if selected_country["ko"] == correct["ko"]:
        st.session_state.score += 1
        st.session_state.result_message = f"✅ 정답! {correct['ko']}입니다."
    else:
        st.session_state.result_message = f"❌ 아쉬워요. 정답은 {correct['ko']}입니다."


# =====================================================
# 디자인
# =====================================================
st.markdown(
    """
    <style>
    .title-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #fef3c7 50%, #dcfce7 100%);
        border-radius: 28px;
        padding: 28px 30px;
        margin-bottom: 20px;
        border: 1.5px solid #bae6fd;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    .title-box h1 {
        margin: 0;
        font-size: 40px;
        font-weight: 900;
        color: #0f172a;
    }

    .title-box p {
        margin-top: 10px;
        font-size: 18px;
        color: #334155;
        font-weight: 700;
    }

    .score-box {
        background: white;
        border-radius: 20px;
        padding: 16px 20px;
        border: 1.5px solid #dbeafe;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        font-size: 20px;
        font-weight: 900;
        color: #1e3a8a;
        text-align: center;
    }

    .question-box {
        background: #fff7ed;
        border: 1.5px solid #fed7aa;
        border-radius: 22px;
        padding: 18px 20px;
        margin: 16px 0;
        font-size: 24px;
        font-weight: 900;
        color: #9a3412;
        text-align: center;
    }

    .result-box {
        background: #f8fafc;
        border: 1.5px solid #e2e8f0;
        border-radius: 18px;
        padding: 16px 20px;
        margin-top: 16px;
        font-size: 22px;
        font-weight: 900;
        text-align: center;
        color: #334155;
    }

    @media (max-width: 768px) {
        .title-box {
            padding: 20px 18px;
            border-radius: 22px;
        }

        .title-box h1 {
            font-size: 28px;
        }

        .title-box p {
            font-size: 15px;
        }

        .question-box {
            font-size: 20px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="title-box">
        <h1>🌍 세계 지도 나라 맞추기 게임</h1>
        <p>지도에서 색칠된 나라를 보고 정답을 골라 보세요.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# 상단 점수
# =====================================================
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(
        f"""
        <div class="score-box">
            점수<br>{st.session_state.score} / {st.session_state.question_count}
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    accuracy = 0
    if st.session_state.question_count > 0:
        accuracy = round(st.session_state.score / st.session_state.question_count * 100)
    st.markdown(
        f"""
        <div class="score-box">
            정답률<br>{accuracy}%
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    if st.button("🔄 처음부터 다시", use_container_width=True):
        reset_game()
        st.rerun()

# =====================================================
# 문제 표시
# =====================================================
st.markdown(
    """
    <div class="question-box">
        색칠된 나라는 어디일까요?
    </div>
    """,
    unsafe_allow_html=True
)

current = st.session_state.current_country

# =====================================================
# 세계 지도 만들기
# =====================================================
map_data = pd.DataFrame([
    {
        "iso_alpha": current["iso"],
        "country": current["ko"],
        "value": 1
    }
])

fig = px.choropleth(
    map_data,
    locations="iso_alpha",
    color="value",
    hover_name="country",
    color_continuous_scale="Blues",
    projection="natural earth"
)

fig.update_layout(
    height=500,
    margin=dict(l=0, r=0, t=0, b=0),
    coloraxis_showscale=False,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="natural earth"
    )
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 선택지
# =====================================================
st.markdown("### 정답을 골라 보세요")

option_cols = st.columns(2)

for i, option in enumerate(st.session_state.options):
    with option_cols[i % 2]:
        if st.button(
            f"{option['ko']} / {option['en']}",
            key=f"option_{i}_{option['ko']}",
            use_container_width=True,
            disabled=st.session_state.answered
        ):
            check_answer(option)
            st.rerun()

# =====================================================
# 결과 표시
# =====================================================
if st.session_state.result_message:
    st.markdown(
        f"""
        <div class="result-box">
            {st.session_state.result_message}
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# 다음 문제
# =====================================================
if st.session_state.answered:
    if st.button("➡️ 다음 나라", use_container_width=True):
        make_new_question()
        st.rerun()
