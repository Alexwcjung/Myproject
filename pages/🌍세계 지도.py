import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
import json
import random

try:
    import countryinfo
    COUNTRYINFO_AVAILABLE = True
except Exception:
    COUNTRYINFO_AVAILABLE = False

st.set_page_config(
    page_title="세계 지도 학습 자료",
    page_icon="🌍",
    layout="wide"
)

# =====================================================
# 기본 라벨 데이터
# =====================================================
CONTINENTS = [
    {"name": "북아메리카\nNorth America", "lat": 50, "lon": -105},
    {"name": "남아메리카\nSouth America", "lat": -18, "lon": -60},
    {"name": "유럽\nEurope", "lat": 54, "lon": 15},
    {"name": "아프리카\nAfrica", "lat": 5, "lon": 20},
    {"name": "아시아\nAsia", "lat": 40, "lon": 90},
    {"name": "오세아니아\nOceania", "lat": -25, "lon": 135},
    {"name": "남극\nAntarctica", "lat": -78, "lon": 20},
]

SEAS = [
    {"name": "태평양\nPacific Ocean", "lat": 8, "lon": -155},
    {"name": "태평양\nPacific Ocean", "lat": 5, "lon": 160},
    {"name": "대서양\nAtlantic Ocean", "lat": 10, "lon": -35},
    {"name": "인도양\nIndian Ocean", "lat": -20, "lon": 80},
    {"name": "북극해\nArctic Ocean", "lat": 78, "lon": 0},
    {"name": "남극해\nSouthern Ocean", "lat": -58, "lon": 80},
    {"name": "홍해\nRed Sea", "lat": 20, "lon": 38},
    {"name": "지중해\nMediterranean Sea", "lat": 35, "lon": 18},
    {"name": "흑해\nBlack Sea", "lat": 43, "lon": 35},
    {"name": "카리브해\nCaribbean Sea", "lat": 15, "lon": -75},
    {"name": "아라비아해\nArabian Sea", "lat": 16, "lon": 64},
    {"name": "벵골만\nBay of Bengal", "lat": 15, "lon": 88},
    {"name": "남중국해\nSouth China Sea", "lat": 14, "lon": 114},
    {"name": "동중국해\nEast China Sea", "lat": 28, "lon": 125},
    {"name": "서해\nYellow Sea", "lat": 35, "lon": 123},
    {"name": "동해/일본해\nEast Sea / Sea of Japan", "lat": 40, "lon": 136},
    {"name": "필리핀해\nPhilippine Sea", "lat": 20, "lon": 135},
    {"name": "베링해\nBering Sea", "lat": 58, "lon": -176},
    {"name": "산호해\nCoral Sea", "lat": -18, "lon": 155},
    {"name": "태즈먼해\nTasman Sea", "lat": -38, "lon": 158},
    {"name": "노르웨이해\nNorwegian Sea", "lat": 68, "lon": 3},
    {"name": "발트해\nBaltic Sea", "lat": 58, "lon": 20},
    {"name": "카스피해\nCaspian Sea", "lat": 41, "lon": 51},
    {"name": "페르시아만\nPersian Gulf", "lat": 26, "lon": 52},
    {"name": "멕시코만\nGulf of Mexico", "lat": 24, "lon": -90},
    {"name": "허드슨만\nHudson Bay", "lat": 60, "lon": -85},
    {"name": "기니만\nGulf of Guinea", "lat": 0, "lon": 2},
    {"name": "아덴만\nGulf of Aden", "lat": 13, "lon": 48},
    {"name": "안다만해\nAndaman Sea", "lat": 11, "lon": 96},
    {"name": "자와해\nJava Sea", "lat": -6, "lon": 112},
    {"name": "아라푸라해\nArafura Sea", "lat": -10, "lon": 136},
    {"name": "래브라도해\nLabrador Sea", "lat": 58, "lon": -50},
]

RIVERS = [
    {"name": "나일강\nNile", "lat": 18, "lon": 31},
    {"name": "콩고강\nCongo", "lat": -2, "lon": 21},
    {"name": "니제르강\nNiger", "lat": 11, "lon": 5},
    {"name": "잠베지강\nZambezi", "lat": -16, "lon": 28},
    {"name": "오렌지강\nOrange", "lat": -29, "lon": 22},
    {"name": "아마존강\nAmazon", "lat": -3, "lon": -60},
    {"name": "오리노코강\nOrinoco", "lat": 7, "lon": -65},
    {"name": "파라나강\nParaná", "lat": -25, "lon": -58},
    {"name": "미시시피강\nMississippi", "lat": 35, "lon": -90},
    {"name": "미주리강\nMissouri", "lat": 45, "lon": -101},
    {"name": "리오그란데강\nRio Grande", "lat": 28, "lon": -102},
    {"name": "세인트로렌스강\nSt. Lawrence", "lat": 47, "lon": -71},
    {"name": "유콘강\nYukon", "lat": 64, "lon": -155},
    {"name": "매켄지강\nMackenzie", "lat": 64, "lon": -122},
    {"name": "다뉴브강\nDanube", "lat": 46, "lon": 20},
    {"name": "라인강\nRhine", "lat": 50, "lon": 7},
    {"name": "볼가강\nVolga", "lat": 55, "lon": 45},
    {"name": "드네프르강\nDnieper", "lat": 49, "lon": 32},
    {"name": "우랄강\nUral", "lat": 49, "lon": 51},
    {"name": "템스강\nThames", "lat": 51.5, "lon": 0},
    {"name": "세느강\nSeine", "lat": 48.7, "lon": 2.5},
    {"name": "티그리스강\nTigris", "lat": 33, "lon": 44},
    {"name": "유프라테스강\nEuphrates", "lat": 34, "lon": 41},
    {"name": "인더스강\nIndus", "lat": 29, "lon": 70},
    {"name": "갠지스강\nGanges", "lat": 25, "lon": 83},
    {"name": "브라마푸트라강\nBrahmaputra", "lat": 25, "lon": 91},
    {"name": "양쯔강\nYangtze", "lat": 30, "lon": 112},
    {"name": "황허\nYellow River", "lat": 35, "lon": 110},
    {"name": "메콩강\nMekong", "lat": 16, "lon": 105},
    {"name": "이라와디강\nIrrawaddy", "lat": 19, "lon": 96},
    {"name": "오비강\nOb", "lat": 61, "lon": 72},
    {"name": "예니세이강\nYenisei", "lat": 64, "lon": 92},
    {"name": "레나강\nLena", "lat": 64, "lon": 125},
    {"name": "아무르강\nAmur", "lat": 49, "lon": 134},
    {"name": "머리강\nMurray", "lat": -34, "lon": 142},
]

# =====================================================
# 퀴즈용 나라 데이터
# flag 포함
# =====================================================
QUIZ_COUNTRIES = [
    {"ko": "대한민국", "en": "South Korea", "iso": "KOR", "continent": "아시아", "flag": "🇰🇷"},
    {"ko": "일본", "en": "Japan", "iso": "JPN", "continent": "아시아", "flag": "🇯🇵"},
    {"ko": "중국", "en": "China", "iso": "CHN", "continent": "아시아", "flag": "🇨🇳"},
    {"ko": "인도", "en": "India", "iso": "IND", "continent": "아시아", "flag": "🇮🇳"},
    {"ko": "태국", "en": "Thailand", "iso": "THA", "continent": "아시아", "flag": "🇹🇭"},
    {"ko": "베트남", "en": "Vietnam", "iso": "VNM", "continent": "아시아", "flag": "🇻🇳"},
    {"ko": "필리핀", "en": "Philippines", "iso": "PHL", "continent": "아시아", "flag": "🇵🇭"},
    {"ko": "인도네시아", "en": "Indonesia", "iso": "IDN", "continent": "아시아", "flag": "🇮🇩"},
    {"ko": "사우디아라비아", "en": "Saudi Arabia", "iso": "SAU", "continent": "아시아", "flag": "🇸🇦"},
    {"ko": "튀르키예", "en": "Turkey", "iso": "TUR", "continent": "아시아/유럽", "flag": "🇹🇷"},
    {"ko": "영국", "en": "United Kingdom", "iso": "GBR", "continent": "유럽", "flag": "🇬🇧"},
    {"ko": "프랑스", "en": "France", "iso": "FRA", "continent": "유럽", "flag": "🇫🇷"},
    {"ko": "독일", "en": "Germany", "iso": "DEU", "continent": "유럽", "flag": "🇩🇪"},
    {"ko": "이탈리아", "en": "Italy", "iso": "ITA", "continent": "유럽", "flag": "🇮🇹"},
    {"ko": "스페인", "en": "Spain", "iso": "ESP", "continent": "유럽", "flag": "🇪🇸"},
    {"ko": "포르투갈", "en": "Portugal", "iso": "PRT", "continent": "유럽", "flag": "🇵🇹"},
    {"ko": "그리스", "en": "Greece", "iso": "GRC", "continent": "유럽", "flag": "🇬🇷"},
    {"ko": "러시아", "en": "Russia", "iso": "RUS", "continent": "유럽/아시아", "flag": "🇷🇺"},
    {"ko": "미국", "en": "United States", "iso": "USA", "continent": "북아메리카", "flag": "🇺🇸"},
    {"ko": "캐나다", "en": "Canada", "iso": "CAN", "continent": "북아메리카", "flag": "🇨🇦"},
    {"ko": "멕시코", "en": "Mexico", "iso": "MEX", "continent": "북아메리카", "flag": "🇲🇽"},
    {"ko": "쿠바", "en": "Cuba", "iso": "CUB", "continent": "북아메리카", "flag": "🇨🇺"},
    {"ko": "브라질", "en": "Brazil", "iso": "BRA", "continent": "남아메리카", "flag": "🇧🇷"},
    {"ko": "아르헨티나", "en": "Argentina", "iso": "ARG", "continent": "남아메리카", "flag": "🇦🇷"},
    {"ko": "칠레", "en": "Chile", "iso": "CHL", "continent": "남아메리카", "flag": "🇨🇱"},
    {"ko": "페루", "en": "Peru", "iso": "PER", "continent": "남아메리카", "flag": "🇵🇪"},
    {"ko": "콜롬비아", "en": "Colombia", "iso": "COL", "continent": "남아메리카", "flag": "🇨🇴"},
    {"ko": "이집트", "en": "Egypt", "iso": "EGY", "continent": "아프리카", "flag": "🇪🇬"},
    {"ko": "남아프리카공화국", "en": "South Africa", "iso": "ZAF", "continent": "아프리카", "flag": "🇿🇦"},
    {"ko": "케냐", "en": "Kenya", "iso": "KEN", "continent": "아프리카", "flag": "🇰🇪"},
    {"ko": "나이지리아", "en": "Nigeria", "iso": "NGA", "continent": "아프리카", "flag": "🇳🇬"},
    {"ko": "모로코", "en": "Morocco", "iso": "MAR", "continent": "아프리카", "flag": "🇲🇦"},
    {"ko": "호주", "en": "Australia", "iso": "AUS", "continent": "오세아니아", "flag": "🇦🇺"},
    {"ko": "뉴질랜드", "en": "New Zealand", "iso": "NZL", "continent": "오세아니아", "flag": "🇳🇿"},
]


# 지도에 표시할 주요 국가 한국어 이름
KOREAN_NAME_BY_ISO = {
    "KOR": "대한민국", "PRK": "북한", "JPN": "일본", "CHN": "중국", "MNG": "몽골",
    "TWN": "대만", "HKG": "홍콩", "SGP": "싱가포르", "VNM": "베트남", "THA": "태국",
    "PHL": "필리핀", "IDN": "인도네시아", "MYS": "말레이시아", "KHM": "캄보디아",
    "LAO": "라오스", "MMR": "미얀마", "IND": "인도", "PAK": "파키스탄",
    "BGD": "방글라데시", "NPL": "네팔", "LKA": "스리랑카", "AFG": "아프가니스탄",
    "IRN": "이란", "IRQ": "이라크", "SAU": "사우디아라비아", "TUR": "튀르키예",
    "ISR": "이스라엘", "JOR": "요르단", "SYR": "시리아", "LBN": "레바논",
    "ARE": "아랍에미리트", "QAT": "카타르", "KWT": "쿠웨이트", "OMN": "오만",
    "YEM": "예멘",

    "USA": "미국", "CAN": "캐나다", "MEX": "멕시코", "CUB": "쿠바",
    "GTM": "과테말라", "PAN": "파나마", "CRI": "코스타리카", "HND": "온두라스",
    "SLV": "엘살바도르", "NIC": "니카라과", "DOM": "도미니카공화국", "HTI": "아이티",

    "BRA": "브라질", "ARG": "아르헨티나", "CHL": "칠레", "PER": "페루",
    "COL": "콜롬비아", "VEN": "베네수엘라", "ECU": "에콰도르", "BOL": "볼리비아",
    "PRY": "파라과이", "URY": "우루과이",

    "GBR": "영국", "IRL": "아일랜드", "FRA": "프랑스", "DEU": "독일",
    "ITA": "이탈리아", "ESP": "스페인", "PRT": "포르투갈", "NLD": "네덜란드",
    "BEL": "벨기에", "CHE": "스위스", "AUT": "오스트리아", "POL": "폴란드",
    "CZE": "체코", "SVK": "슬로바키아", "HUN": "헝가리", "ROU": "루마니아",
    "BGR": "불가리아", "GRC": "그리스", "SWE": "스웨덴", "NOR": "노르웨이",
    "FIN": "핀란드", "DNK": "덴마크", "ISL": "아이슬란드", "RUS": "러시아",
    "UKR": "우크라이나", "BLR": "벨라루스", "EST": "에스토니아", "LVA": "라트비아",
    "LTU": "리투아니아", "SRB": "세르비아", "HRV": "크로아티아", "SVN": "슬로베니아",

    "EGY": "이집트", "MAR": "모로코", "DZA": "알제리", "TUN": "튀니지",
    "LBY": "리비아", "SDN": "수단", "ETH": "에티오피아", "KEN": "케냐",
    "TZA": "탄자니아", "UGA": "우간다", "NGA": "나이지리아", "GHA": "가나",
    "CMR": "카메룬", "COD": "콩고민주공화국", "COG": "콩고공화국", "ZAF": "남아프리카공화국",
    "ZWE": "짐바브웨", "AGO": "앙골라", "MOZ": "모잠비크", "MDG": "마다가스카르",

    "AUS": "호주", "NZL": "뉴질랜드", "PNG": "파푸아뉴기니", "FJI": "피지"
}


# =====================================================
# 전체 나라 이름 불러오기
# =====================================================
@st.cache_data
def load_all_countries():
    if COUNTRYINFO_AVAILABLE:
        data_dir = os.path.join(os.path.dirname(countryinfo.__file__), "data")
        rows = []

        for filename in os.listdir(data_dir):
            if not filename.endswith(".json"):
                continue

            path = os.path.join(data_dir, filename)
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)

                name = data.get("name")
                iso = (data.get("ISO") or {}).get("alpha3")
                latlng = data.get("latlng")
                region = data.get("region", "")
                capital = data.get("capital", "")

                if name and iso and isinstance(latlng, list) and len(latlng) >= 2:
                    ko_name = KOREAN_NAME_BY_ISO.get(iso)
                    display_name = f"{ko_name} / {name}" if ko_name else name

                    rows.append({
                        "name": display_name,
                        "ko_name": ko_name if ko_name else "",
                        "en_name": name,
                        "iso": iso,
                        "lat": float(latlng[0]),
                        "lon": float(latlng[1]),
                        "region": region,
                        "capital": capital,
                    })
            except Exception:
                continue

        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.drop_duplicates(subset=["iso"]).sort_values("name").reset_index(drop=True)
            return df

    return pd.DataFrame([
        {
            "name": f"{c['ko']} / {c['en']}",
            "ko_name": c["ko"],
            "en_name": c["en"],
            "iso": c["iso"],
            "lat": 0,
            "lon": 0,
            "region": c["continent"],
            "capital": ""
        }
        for c in QUIZ_COUNTRIES
    ])

countries_df = load_all_countries()

# =====================================================
# 퀴즈 세션 상태
# =====================================================
QUIZ_LENGTH = 10

def get_quiz_pool():
    level = st.session_state.get("quiz_level", "전체")

    if level == "전체":
        pool = QUIZ_COUNTRIES
    else:
        pool = [c for c in QUIZ_COUNTRIES if level in c["continent"]]

    if len(pool) < 4:
        pool = QUIZ_COUNTRIES

    return pool

def start_new_quiz():
    pool = get_quiz_pool()

    # 새 퀴즈가 시작될 때 버튼 key를 새로 만들기 위한 번호입니다.
    st.session_state.quiz_total = st.session_state.get("quiz_total", 0) + 1

    if len(pool) >= QUIZ_LENGTH:
        quiz_list = random.sample(pool, QUIZ_LENGTH)
    else:
        quiz_list = random.choices(pool, k=QUIZ_LENGTH)

    st.session_state.quiz_list = quiz_list
    st.session_state.quiz_index = 0
    st.session_state.quiz_correct_count = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_result = ""
    st.session_state.quiz_correct_flag = False
    make_current_options()

def make_current_options():
    """현재 문제와 4지선다 선택지를 새로 만듭니다."""
    quiz_list = st.session_state.get("quiz_list", [])
    quiz_index = st.session_state.get("quiz_index", 0)

    # 세션에 이전 오류값(None 등)이 남아 있을 때 안전하게 다시 시작합니다.
    if (
        not isinstance(quiz_list, list)
        or len(quiz_list) == 0
        or not isinstance(quiz_index, int)
        or quiz_index < 0
        or quiz_index >= len(quiz_list)
    ):
        start_new_quiz()
        return

    current = quiz_list[quiz_index]

    if not isinstance(current, dict) or not current.get("iso"):
        start_new_quiz()
        return

    wrong_pool = [
        c for c in QUIZ_COUNTRIES
        if isinstance(c, dict) and c.get("iso") and c.get("iso") != current.get("iso")
    ]

    if len(wrong_pool) < 3:
        wrong_pool = [
            c for c in QUIZ_COUNTRIES
            if isinstance(c, dict) and c.get("iso") != current.get("iso")
        ]

    wrongs = random.sample(wrong_pool, 3)
    options = wrongs + [current]
    random.shuffle(options)

    # 혹시 모를 비정상 값 제거
    options = [o for o in options if isinstance(o, dict) and o.get("iso")]

    st.session_state.quiz_current = current
    st.session_state.quiz_options = options
    st.session_state.quiz_answered = False
    st.session_state.quiz_result = ""
    st.session_state.quiz_correct_flag = False


def next_quiz_question():
    """다음 문제로 이동하거나 퀴즈를 종료합니다."""
    if st.session_state.quiz_index < QUIZ_LENGTH - 1:
        st.session_state.quiz_index += 1
        make_current_options()
    else:
        st.session_state.quiz_finished = True


def check_quiz_answer(option):
    """학생이 고른 답을 채점합니다.
    틀리면 같은 문제를 계속 다시 풀 수 있고, 정답을 맞힌 뒤에만 다음 문제로 넘어갑니다.
    """
    if st.session_state.get("quiz_answered", False):
        return

    if not isinstance(option, dict):
        st.session_state.quiz_answered = False
        st.session_state.quiz_result = "❌ 선택지 오류가 있어요. 다시 골라 보세요."
        st.session_state.quiz_correct_flag = False
        return

    correct = st.session_state.get("quiz_current", {})

    if isinstance(correct, dict) and option.get("iso") == correct.get("iso"):
        st.session_state.quiz_answered = True
        st.session_state.quiz_correct_count += 1
        st.session_state.quiz_result = f"✅ 정답입니다! {correct.get('ko', '')} / {correct.get('en', '')}"
        st.session_state.quiz_correct_flag = True
    else:
        # 오답일 때는 정답을 공개하지 않고, 같은 문제를 계속 풀 수 있게 둡니다.
        st.session_state.quiz_answered = False
        st.session_state.quiz_result = "❌ 아쉬워요. 다시 골라보세요! 정답을 맞히면 다음 문제로 넘어갈 수 있습니다."
        st.session_state.quiz_correct_flag = False


# =====================================================
# 퀴즈 세션 초기화
# =====================================================
if "quiz_level" not in st.session_state:
    st.session_state.quiz_level = "전체"

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0

# 이전 실행에서 None 또는 잘못된 값이 세션에 남아 있으면 자동으로 새로 시작합니다.
def is_valid_quiz_state():
    try:
        quiz_list = st.session_state.get("quiz_list")
        quiz_index = st.session_state.get("quiz_index")
        quiz_options = st.session_state.get("quiz_options")
        quiz_current = st.session_state.get("quiz_current")

        return (
            isinstance(quiz_list, list)
            and len(quiz_list) == QUIZ_LENGTH
            and all(isinstance(q, dict) and q.get("iso") for q in quiz_list)
            and isinstance(quiz_index, int)
            and 0 <= quiz_index < QUIZ_LENGTH
            and isinstance(quiz_options, list)
            and len(quiz_options) == 4
            and all(isinstance(o, dict) and o.get("iso") for o in quiz_options)
            and isinstance(quiz_current, dict)
            and quiz_current.get("iso")
        )
    except Exception:
        return False

if not is_valid_quiz_state():
    start_new_quiz()

# =====================================================
# 스타일
# =====================================================
st.markdown(
    """
    <style>
    .title-box {
        background: linear-gradient(135deg, #dbeafe 0%, #ecfeff 45%, #fef3c7 100%);
        border-radius: 28px;
        padding: 26px 30px;
        margin-bottom: 18px;
        border: 1.5px solid #bfdbfe;
        box-shadow: 0 8px 20px rgba(0,0,0,0.07);
    }
    .title-box h1 {
        margin: 0;
        font-size: 38px;
        font-weight: 900;
        color: #0f172a;
    }
    .title-box p {
        margin-top: 10px;
        font-size: 18px;
        color: #334155;
        font-weight: 700;
        line-height: 1.6;
    }
    .info-box {
        background: white;
        border: 1.5px solid #e2e8f0;
        border-radius: 20px;
        padding: 16px 18px;
        margin-bottom: 14px;
        font-size: 16px;
        font-weight: 700;
        color: #334155;
    }
    .score-card {
        background: white;
        border: 1.5px solid #dbeafe;
        border-radius: 22px;
        padding: 18px 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        text-align: center;
    }
    .score-label {
        font-size: 15px;
        color: #64748b;
        font-weight: 800;
    }
    .score-value {
        font-size: 34px;
        color: #1e3a8a;
        font-weight: 950;
        margin-top: 5px;
    }
    .question-card {
        background: linear-gradient(135deg, #fff7ed 0%, #fffbeb 100%);
        border: 1.5px solid #fed7aa;
        border-radius: 26px;
        padding: 20px 22px;
        margin: 14px 0;
        text-align: center;
        box-shadow: 0 5px 14px rgba(0,0,0,0.05);
    }
    .question-card .small {
        color: #9a3412;
        font-size: 16px;
        font-weight: 850;
    }
    .question-card .big {
        color: #7c2d12;
        font-size: 34px;
        font-weight: 950;
        margin-top: 6px;
    }
    .result-card {
        background: #f8fafc;
        border: 1.5px solid #e2e8f0;
        border-radius: 22px;
        padding: 17px 20px;
        margin-top: 14px;
        font-size: 30px;
        font-weight: 950;
        text-align: center;
        color: #334155;
    }

    /* 모든 버튼 기본 모양 */
    div.stButton > button {
        border-radius: 24px;
        font-weight: 1000 !important;
        min-height: 124px;
        font-size: 2.15rem !important;
        line-height: 1.35;
        border: 3px solid #93c5fd;
        background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%);
        color: #0f172a;
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.12);
    }

    /* Streamlit 버튼 내부 글자 크기 강제 적용 */
    div.stButton > button p {
        font-size: 2.15rem !important;
        font-weight: 1000 !important;
        line-height: 1.35 !important;
        color: #0f172a !important;
    }

    /* 퀴즈 보기 버튼이 더 또렷하게 보이도록 */
    div.stButton > button div,
    div.stButton > button span {
        font-size: 2.15rem !important;
        font-weight: 1000 !important;
    }

    div.stButton > button:hover {
        border: 3px solid #2563eb;
        background: linear-gradient(135deg, #dbeafe 0%, #f0f9ff 100%);
        color: #1e3a8a;
        transform: translateY(-1px);
    }

    div.stButton > button:hover p {
        color: #1e3a8a !important;
    }

    .next-guide {
        background: #f8fafc;
        border: 2px dashed #cbd5e1;
        border-radius: 22px;
        padding: 22px 12px;
        text-align: center;
        color: #64748b;
        font-size: 18px;
        font-weight: 900;
        line-height: 1.55;
        margin-top: 8px;
    }


    @keyframes sparklePop {
        0% { transform: scale(0.6); opacity: 0; }
        35% { transform: scale(1.25); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    .sparkle-box {
        background: linear-gradient(135deg, #dcfce7 0%, #fef9c3 100%);
        border: 2px solid #86efac;
        border-radius: 28px;
        padding: 22px;
        margin-top: 18px;
        text-align: center;
        font-size: 34px;
        font-weight: 950;
        color: #166534;
        animation: sparklePop 0.7s ease-out;
        box-shadow: 0 8px 24px rgba(34,197,94,0.22);
    }
    .sparkle-line {
        font-size: 45px;
        margin-bottom: 8px;
    }


    .learn-hero {
        background: linear-gradient(135deg, #ecfdf5 0%, #eff6ff 50%, #fff7ed 100%);
        border: 1.5px solid #bbf7d0;
        border-radius: 30px;
        padding: 24px 26px;
        margin-bottom: 18px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
    }
    .learn-hero h2 {
        margin: 0;
        font-size: 34px;
        font-weight: 950;
        color: #0f172a;
    }
    .learn-hero p {
        margin-top: 10px;
        font-size: 17px;
        color: #334155;
        font-weight: 750;
        line-height: 1.6;
    }
    .continent-card {
        background: white;
        border: 1.5px solid #dbeafe;
        border-radius: 24px;
        padding: 20px 22px;
        margin-bottom: 16px;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06);
    }
    .continent-card h3 {
        margin: 0 0 10px 0;
        font-size: 28px;
        font-weight: 950;
        color: #1e3a8a;
    }
    .country-chip {
        display: inline-block;
        background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
        border: 1.5px solid #bfdbfe;
        border-radius: 999px;
        padding: 10px 14px;
        margin: 6px 5px;
        font-size: 18px;
        font-weight: 900;
        color: #0f172a;
        box-shadow: 0 3px 8px rgba(15, 23, 42, 0.05);
    }
    .country-chip small {
        color: #475569;
        font-size: 14px;
        font-weight: 800;
    }
    .learning-table {
        font-size: 18px;
        font-weight: 800;
    }

    @media (max-width: 768px) {
        .title-box { padding: 20px 18px; border-radius: 22px; }
        .title-box h1 { font-size: 34px; }
        .title-box p { font-size: 15px; }
        .quiz-hero h2 { font-size: 30px; }
        .question-card .big { font-size: 23px; }
        div.stButton > button { font-size: 1.6rem !important; min-height: 94px; }
        div.stButton > button p { font-size: 1.6rem !important; font-weight: 1000 !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="title-box">
        <h1>🌍 세계 지도 학습 자료</h1>
        <p>
            지도에서 색칠된 나라를 보고 정답을 고르는 세계 지도 퀴즈입니다.<br>
            세계지도에서 대륙, 바다, 강, 나라 이름도 함께 확인할 수 있습니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

tab_quiz, tab_map = st.tabs(["🎮 나라 맞추기 퀴즈", "🗺️ 세계지도"])

# =====================================================
# 2번 탭: 세계지도
# =====================================================
with tab_map:
    row1 = st.columns(4)
    with row1[0]:
        show_continents = st.checkbox("대륙 이름 보기", value=True)
    with row1[1]:
        show_seas = st.checkbox("바다 이름 보기", value=True)
    with row1[2]:
        show_rivers = st.checkbox("강 이름 보기", value=False)
    with row1[3]:
        show_countries = st.checkbox("나라 이름 보기", value=False)

    row2 = st.columns(4)
    with row2[0]:
        country_font = st.slider("나라 이름 크기", 6, 18, 8)
    with row2[1]:
        sea_font = st.slider("바다 이름 크기", 10, 24, 16)
    with row2[2]:
        river_font = st.slider("강 이름 크기", 8, 20, 12)
    with row2[3]:
        continent_font = st.slider("대륙 이름 크기", 14, 30, 22)

    st.markdown(
        f"""
        <div class="info-box">
        ✅ 이 탭은 <b>세계지도</b>입니다. 나라 이름은 가능한 경우 <b>한국어 / 영어</b>로 함께 표시됩니다. 현재 표시 가능 데이터: <b>{len(countries_df)}개</b><br>
        ✅ 지도는 마우스로 확대/축소할 수 있고, 확대하면 나라 이름을 더 자세히 볼 수 있습니다.<br>
        ✅ Plotly 범례에서도 레이어를 클릭해서 보이기/숨기기를 할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lon=[c["lon"] for c in CONTINENTS],
        lat=[c["lat"] for c in CONTINENTS],
        mode="text",
        text=[c["name"] for c in CONTINENTS],
        textfont=dict(size=continent_font, color="#7c2d12"),
        textposition="middle center",
        name="대륙",
        hoverinfo="skip",
        visible=show_continents
    ))

    fig.add_trace(go.Scattergeo(
        lon=[s["lon"] for s in SEAS],
        lat=[s["lat"] for s in SEAS],
        mode="text",
        text=[s["name"] for s in SEAS],
        textfont=dict(size=sea_font, color="#0369a1"),
        textposition="middle center",
        name="바다",
        hoverinfo="skip",
        visible=show_seas
    ))

    fig.add_trace(go.Scattergeo(
        lon=[r["lon"] for r in RIVERS],
        lat=[r["lat"] for r in RIVERS],
        mode="markers+text",
        text=[r["name"] for r in RIVERS],
        textfont=dict(size=river_font, color="#1d4ed8"),
        textposition="top center",
        marker=dict(size=4, color="#60a5fa", opacity=0.7),
        name="강",
        hoverinfo="skip",
        visible=show_rivers
    ))

    if not countries_df.empty:
        fig.add_trace(go.Scattergeo(
            lon=countries_df["lon"],
            lat=countries_df["lat"],
            mode="markers+text",
            text=countries_df["name"],
            textfont=dict(size=country_font, color="#111827"),
            textposition="top center",
            marker=dict(size=3, color="#ef4444", opacity=0.65),
            name="나라",
            hovertext=[
                (
                    f"{row['name']}<br>Region: {row['region']}<br>Capital: {row['capital']}"
                    if row.get("capital")
                    else f"{row['name']}<br>Region: {row['region']}"
                )
                for _, row in countries_df.iterrows()
            ],
            hoverinfo="text",
            visible=show_countries
        ))

    fig.update_layout(
        height=780,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.01,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.75)"
        ),
        geo=dict(
            projection_type="natural earth",
            showland=True,
            landcolor="#f8fafc",
            showocean=True,
            oceancolor="#dbeafe",
            showcountries=True,
            countrycolor="#94a3b8",
            coastlinecolor="#475569",
            showcoastlines=True,
            showframe=False,
            lataxis=dict(showgrid=True, gridcolor="#e2e8f0"),
            lonaxis=dict(showgrid=True, gridcolor="#e2e8f0"),
            resolution=50,
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"scrollZoom": True, "displaylogo": False}
    )

    st.markdown("---")
    st.markdown("## 📌 수업용 빠른 정리")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            ### 🌎 7대륙
            - 아시아 / Asia
            - 유럽 / Europe
            - 아프리카 / Africa
            - 북아메리카 / North America
            - 남아메리카 / South America
            - 오세아니아 / Oceania
            - 남극 / Antarctica
            """
        )

    with c2:
        st.markdown(
            """
            ### 🌊 주요 바다 / 강 예시
            **바다**
            - 태평양 / Pacific Ocean
            - 대서양 / Atlantic Ocean
            - 인도양 / Indian Ocean
            - 홍해 / Red Sea
            - 지중해 / Mediterranean Sea

            **강**
            - 나일강 / Nile
            - 아마존강 / Amazon
            - 미시시피강 / Mississippi
            - 양쯔강 / Yangtze
            - 메콩강 / Mekong
            """
        )


# =====================================================
# 1번 탭: 나라 맞추기 퀴즈
# =====================================================
with tab_quiz:

    if st.session_state.quiz_finished:
        st.markdown(
            f"""
            <div class="sparkle-box">
                <div class="sparkle-line">🎉 🌍 🎉</div>
                퀴즈 완료!<br>
                최종 정답: {st.session_state.quiz_correct_count} / {QUIZ_LENGTH}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🔁 10문제 다시 풀기", use_container_width=True):
            st.session_state.quiz_finished = False
            start_new_quiz()
            st.rerun()

        st.stop()

    current = st.session_state.quiz_current

    map_data = pd.DataFrame([
        {
            "iso_alpha": current["iso"],
            "country": f"{current['ko']} / {current['en']}",
            "value": 1
        }
    ])

    qfig = px.choropleth(
        map_data,
        locations="iso_alpha",
        color="value",
        hover_name="country",
        color_continuous_scale=[[0, "#93c5fd"], [1, "#1d4ed8"]],
        projection="natural earth"
    )

    qfig.update_layout(
        height=720,
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_showscale=False,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#475569",
            showcountries=True,
            countrycolor="#cbd5e1",
            showland=True,
            landcolor="#f8fafc",
            showocean=True,
            oceancolor="#e0f2fe",
            projection_type="natural earth"
        )
    )

    map_col, next_col = st.columns([5.2, 1])

    with map_col:
        st.plotly_chart(qfig, use_container_width=True, config={"displaylogo": False})

    with next_col:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if st.session_state.quiz_answered:
            next_label = "➡️\n다음" if st.session_state.quiz_index < QUIZ_LENGTH - 1 else "🏁\n결과"
            if st.button(next_label, use_container_width=True, key="next_button_side"):
                next_quiz_question()
                st.rerun()
        else:
            st.markdown(
                """
                <div class="next-guide">
                    정답을 맞히면<br>➡️ 다음 버튼
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("## 정답을 골라 보세요")

    option_cols = st.columns(2)
    option_labels = ["A", "B", "C", "D"]

    safe_options = [
        o for o in st.session_state.get("quiz_options", [])
        if isinstance(o, dict) and o.get("iso")
    ]

    if len(safe_options) != 4:
        st.warning("퀴즈 선택지에 오류가 있어 새 문제를 다시 불러옵니다.")
        make_current_options()
        st.rerun()

    for i, option in enumerate(safe_options):
        with option_cols[i % 2]:
            ko_name = option.get("ko", "")
            en_name = option.get("en", "")
            iso_code = option.get("iso", str(i))
            button_label = f"{option_labels[i]}.  {ko_name}  /  {en_name}"
            if st.button(
                button_label,
                key=f"quiz_option_{i}_{iso_code}_{st.session_state.get('quiz_total', 0)}",
                use_container_width=True,
                disabled=st.session_state.quiz_answered
            ):
                check_quiz_answer(option)
                st.rerun()

    if st.session_state.quiz_result:
        if st.session_state.quiz_correct_flag:
            st.balloons()
            st.markdown(
                f"""
                <div class="sparkle-box">
                    <div class="sparkle-line">✨ 🎉 💥 🌟 ✨</div>
                    반짝! 정답입니다!<br>
                    {st.session_state.quiz_result}<br>
                    <span style="font-size:20px; color:#15803d;">대륙: {current.get('continent', '')}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="result-card">
                    {st.session_state.quiz_result}<br>
                    <span style="font-size:18px; color:#64748b;">같은 문제를 다시 풀어 보세요.</span>
                </div>
                """,
                unsafe_allow_html=True
            )


st.caption("필요한 패키지: streamlit, plotly, pandas, countryinfo")
