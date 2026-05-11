import streamlit as st
import random

st.set_page_config(
    page_title="우리나라 역사와 근현대사",
    page_icon="🇰🇷",
    layout="wide"
)

# =====================================================
# 전체 흐름
# =====================================================
HISTORY_FLOW = [
    {
        "name": "선사",
        "emoji": "🪨",
        "years": "문자 사용 이전",
        "one": "도구와 농경의 시작",
    },
    {
        "name": "고조선",
        "emoji": "🐻",
        "years": "기원전 2333년 전설적 건국 ~ 기원전 108년",
        "one": "우리 역사상 첫 국가",
    },
    {
        "name": "삼국",
        "emoji": "⚔️",
        "years": "기원전 1세기경 ~ 668년",
        "one": "고구려·백제·신라 경쟁",
    },
    {
        "name": "남북국",
        "emoji": "🌅",
        "years": "7세기 후반 ~ 10세기",
        "one": "통일 신라와 발해",
    },
    {
        "name": "고려",
        "emoji": "📜",
        "years": "918년 ~ 1392년",
        "one": "불교 문화와 금속활자",
    },
    {
        "name": "조선",
        "emoji": "👑",
        "years": "1392년 ~ 1897년",
        "one": "유교 정치와 훈민정음",
    },
    {
        "name": "근현대",
        "emoji": "🇰🇷",
        "years": "1876년 개항 이후 ~ 현재",
        "one": "독립·전쟁·산업화·민주화",
    },
]

# =====================================================
# 고대~조선 설명
# =====================================================
PREMODERN_PERIODS = [
    {
        "name": "고조선",
        "emoji": "🐻",
        "years": "기원전 2333년 전설적 건국 ~ 기원전 108년",
        "period": "우리 역사상 첫 국가",
        "core": "청동기 문화를 바탕으로 성장한 우리나라 최초의 국가입니다.",
        "details": [
            "단군왕검이 세웠다고 전해집니다.",
            "홍익인간은 널리 인간을 이롭게 한다는 뜻입니다.",
            "8조법을 통해 당시 사회에 법과 질서가 있었음을 알 수 있습니다.",
            "청동기 문화와 고인돌이 중요한 특징입니다."
        ],
        "keywords": ["단군왕검", "홍익인간", "청동기", "고인돌", "8조법"]
    },
    {
        "name": "삼국 시대",
        "emoji": "⚔️",
        "years": "기원전 1세기경 ~ 668년",
        "period": "고구려 · 백제 · 신라",
        "core": "세 나라가 한반도와 만주 일대에서 서로 경쟁하며 성장한 시대입니다.",
        "details": [
            "고구려는 북쪽의 강한 군사력을 바탕으로 넓은 영토를 차지했습니다.",
            "백제는 한강 유역을 바탕으로 성장했고 일본과 문화 교류가 활발했습니다.",
            "신라는 삼국 중 늦게 발전했지만, 결국 삼국 통일을 주도했습니다.",
            "불교가 수용되면서 왕권 강화와 문화 발전에 큰 영향을 주었습니다."
        ],
        "keywords": ["고구려", "백제", "신라", "불교", "한강 유역"]
    },
    {
        "name": "남북국 시대",
        "emoji": "🌅",
        "years": "7세기 후반 ~ 10세기",
        "period": "통일 신라 · 발해",
        "core": "남쪽에는 통일 신라, 북쪽에는 고구려를 계승한 발해가 있던 시대입니다.",
        "details": [
            "통일 신라는 삼국 통일 이후 불국사와 석굴암 같은 뛰어난 문화를 남겼습니다.",
            "발해는 고구려 계승 의식을 바탕으로 만주와 한반도 북부에서 발전했습니다.",
            "발해는 해동성국이라고 불릴 정도로 강성했습니다.",
            "이 시기를 남북국 시대라고 부르기도 합니다."
        ],
        "keywords": ["통일 신라", "발해", "불국사", "석굴암", "해동성국"]
    },
    {
        "name": "고려",
        "emoji": "📜",
        "years": "918년 ~ 1392년",
        "period": "왕건 건국",
        "core": "왕건이 세운 나라로, 불교 문화와 인쇄술이 크게 발달했습니다.",
        "details": [
            "후삼국을 통일하고 새 왕조를 열었습니다.",
            "불교가 국가와 사회에 큰 영향을 주었습니다.",
            "팔만대장경은 몽골 침입을 극복하려는 마음과 뛰어난 목판 인쇄술을 보여 줍니다.",
            "세계적으로 이른 시기에 금속활자를 사용했습니다."
        ],
        "keywords": ["왕건", "불교", "팔만대장경", "금속활자", "몽골 침입"]
    },
    {
        "name": "조선",
        "emoji": "👑",
        "years": "1392년 ~ 1897년",
        "period": "이성계 건국",
        "core": "유교를 바탕으로 나라를 운영했고, 훈민정음이 창제되었습니다.",
        "details": [
            "이성계가 세운 나라입니다.",
            "유교 이념을 바탕으로 정치와 사회 질서를 세웠습니다.",
            "세종대왕은 훈민정음을 창제하고 과학 기술과 문화를 발전시켰습니다.",
            "임진왜란과 병자호란 등 큰 전쟁을 겪었습니다.",
            "후기에는 실학이 등장하고 근대 사회로 변화하려는 움직임이 나타났습니다."
        ],
        "keywords": ["이성계", "유교", "세종대왕", "훈민정음", "임진왜란", "실학"]
    },
]

# =====================================================
# 근현대사 세부 단계
# =====================================================
MODERN_STEPS = [
    {
        "title": "개항과 근대화의 시작",
        "years": "1876년 이후",
        "emoji": "🚢",
        "summary": "강화도 조약 이후 조선은 외국과 본격적으로 관계를 맺기 시작했습니다.",
        "details": [
            "서양과 일본의 압력이 커졌습니다.",
            "근대 문물과 제도가 들어오기 시작했습니다.",
            "전통 질서와 새로운 변화가 충돌했습니다."
        ],
        "keywords": ["강화도 조약", "개항", "근대 문물"]
    },
    {
        "title": "대한제국",
        "years": "1897년 ~ 1910년",
        "emoji": "🦅",
        "summary": "고종은 대한제국을 선포하고 자주 독립 국가와 근대 국가를 지향했습니다.",
        "details": [
            "고종이 황제로 즉위했습니다.",
            "광무개혁을 통해 근대화를 추진했습니다.",
            "그러나 주변 열강의 간섭이 심해졌습니다."
        ],
        "keywords": ["고종", "황제", "광무개혁"]
    },
    {
        "title": "일제 강점기",
        "years": "1910년 ~ 1945년",
        "emoji": "🕯️",
        "summary": "일본의 식민 지배를 받았지만, 국내외에서 독립운동이 계속되었습니다.",
        "details": [
            "1910년 나라의 주권을 빼앗겼습니다.",
            "3·1운동은 전 민족적 독립운동이었습니다.",
            "대한민국 임시정부가 수립되어 독립운동을 이어 갔습니다."
        ],
        "keywords": ["국권 피탈", "3·1운동", "대한민국 임시정부", "독립운동"]
    },
    {
        "title": "광복과 정부 수립",
        "years": "1945년 ~ 1948년",
        "emoji": "🌅",
        "summary": "1945년 광복을 맞았고, 1948년 대한민국 정부가 수립되었습니다.",
        "details": [
            "일본의 패망으로 광복을 맞았습니다.",
            "남과 북에 서로 다른 체제가 형성되었습니다.",
            "1948년 대한민국 정부가 수립되었습니다."
        ],
        "keywords": ["광복", "분단", "정부 수립"]
    },
    {
        "title": "6·25 전쟁",
        "years": "1950년 ~ 1953년",
        "emoji": "🪖",
        "summary": "전쟁으로 큰 피해를 입었고, 휴전 이후 분단이 계속되었습니다.",
        "details": [
            "1950년 북한의 남침으로 전쟁이 시작되었습니다.",
            "많은 인명 피해와 사회적 혼란이 있었습니다.",
            "1953년 정전협정 이후 현재까지 분단 상태가 이어지고 있습니다."
        ],
        "keywords": ["6·25 전쟁", "휴전", "분단"]
    },
    {
        "title": "산업화",
        "years": "1960년대 ~ 1980년대",
        "emoji": "🏭",
        "summary": "수출과 제조업 중심으로 경제가 빠르게 성장했습니다.",
        "details": [
            "경제 개발 계획이 추진되었습니다.",
            "수출 중심 산업이 성장했습니다.",
            "도시화와 산업화가 빠르게 진행되었습니다."
        ],
        "keywords": ["경제 개발", "수출", "새마을운동", "산업화"]
    },
    {
        "title": "민주화",
        "years": "1980년대 ~ 1990년대",
        "emoji": "🗳️",
        "summary": "시민들의 노력으로 민주주의가 발전했습니다.",
        "details": [
            "5·18 민주화운동은 민주주의를 위한 중요한 사건입니다.",
            "1987년 6월 민주항쟁으로 대통령 직선제가 실현되었습니다.",
            "시민의 권리와 참여가 확대되었습니다."
        ],
        "keywords": ["5·18", "6월 민주항쟁", "대통령 직선제"]
    },
    {
        "title": "오늘날 대한민국",
        "years": "2000년대 이후",
        "emoji": "🌐",
        "summary": "민주주의, 경제, 기술, 문화가 발전하며 세계와 활발히 연결되고 있습니다.",
        "details": [
            "IT, 반도체, 자동차, 조선 등 다양한 산업이 발전했습니다.",
            "K-문화가 세계적으로 확산되었습니다.",
            "민주주의와 사회 갈등 해결이 계속 중요한 과제로 남아 있습니다."
        ],
        "keywords": ["IT", "K-문화", "세계화", "민주주의"]
    },
]

# =====================================================
# 대한민국 역대 대통령
# =====================================================
PRESIDENTS = [
    {
        "order": "1~3대",
        "name": "이승만",
        "years": "1948년 ~ 1960년",
        "main": "대한민국 초대 대통령",
        "points": ["대한민국 정부 수립", "6·25 전쟁 시기 국정 운영", "반공 체제 강화"],
        "note": "장기 집권과 3·15 부정선거 이후 4·19 혁명으로 하야"
    },
    {
        "order": "4대",
        "name": "윤보선",
        "years": "1960년 ~ 1962년",
        "main": "제2공화국 대통령",
        "points": ["4·19 혁명 이후 대통령", "의원내각제 시기 대통령"],
        "note": "5·16 군사정변 이후 정치적 영향력 약화"
    },
    {
        "order": "5~9대",
        "name": "박정희",
        "years": "1963년 ~ 1979년",
        "main": "산업화와 경제 개발 추진",
        "points": ["경제 개발 5개년 계획", "수출 중심 산업화", "새마을운동", "경부고속도로 건설"],
        "note": "유신 체제와 장기 집권, 민주주의 억압에 대한 비판"
    },
    {
        "order": "10대",
        "name": "최규하",
        "years": "1979년 ~ 1980년",
        "main": "과도기 대통령",
        "points": ["박정희 사망 이후 과도기 국정 운영", "서울의 봄 시기 대통령"],
        "note": "신군부 등장 이후 짧은 기간 재임"
    },
    {
        "order": "11~12대",
        "name": "전두환",
        "years": "1980년 ~ 1988년",
        "main": "제5공화국 대통령",
        "points": ["제5공화국 출범", "1986 아시안게임 개최", "1988 서울올림픽 준비"],
        "note": "5·18 민주화운동 유혈 진압과 권위주의 통치에 대한 비판"
    },
    {
        "order": "13대",
        "name": "노태우",
        "years": "1988년 ~ 1993년",
        "main": "직선제 개헌 이후 첫 대통령",
        "points": ["1988 서울올림픽 개최", "북방외교", "남북 기본합의서 채택"],
        "note": "군사정권 출신이라는 점과 정치자금 문제에 대한 비판"
    },
    {
        "order": "14대",
        "name": "김영삼",
        "years": "1993년 ~ 1998년",
        "main": "문민정부 출범",
        "points": ["금융실명제", "하나회 해체", "지방자치 확대"],
        "note": "임기 말 외환위기 발생"
    },
    {
        "order": "15대",
        "name": "김대중",
        "years": "1998년 ~ 2003년",
        "main": "외환위기 극복과 남북 화해 추진",
        "points": ["외환위기 극복 노력", "햇볕정책", "남북정상회담", "노벨평화상 수상"],
        "note": "대북 정책 평가를 둘러싼 논쟁"
    },
    {
        "order": "16대",
        "name": "노무현",
        "years": "2003년 ~ 2008년",
        "main": "참여정부와 권위주의 문화 완화",
        "points": ["권위주의 완화", "지방분권 추진", "전자정부 발전", "한미 FTA 추진"],
        "note": "정책 추진 방식과 정치 갈등에 대한 논쟁"
    },
    {
        "order": "17대",
        "name": "이명박",
        "years": "2008년 ~ 2013년",
        "main": "경제 성장과 인프라 사업 강조",
        "points": ["글로벌 금융위기 대응", "G20 서울 정상회의", "4대강 사업"],
        "note": "4대강 사업과 자원외교 등에 대한 논쟁"
    },
    {
        "order": "18대",
        "name": "박근혜",
        "years": "2013년 ~ 2017년",
        "main": "첫 여성 대통령",
        "points": ["문화융성 정책", "창조경제 정책", "복지 정책 확대 시도"],
        "note": "국정농단 사건으로 탄핵 및 파면"
    },
    {
        "order": "19대",
        "name": "문재인",
        "years": "2017년 ~ 2022년",
        "main": "촛불 이후 정부 출범",
        "points": ["남북정상회담", "코로나19 대응", "검찰개혁 추진"],
        "note": "부동산 정책과 경제 정책 평가를 둘러싼 논쟁"
    },
    {
        "order": "20대",
        "name": "윤석열",
        "years": "2022년 ~ 2025년",
        "main": "검찰총장 출신 대통령",
        "points": ["한미일 안보 협력 강화", "노동·연금·교육 개혁 추진", "원전 정책 전환"],
        "note": "2024년 비상계엄 사태 이후 탄핵 및 파면"
    },
    {
        "order": "21대",
        "name": "이재명",
        "years": "2025년 ~ 현재",
        "main": "조기 대선 이후 출범",
        "points": ["정치 위기 이후 국정 안정 과제", "민생 경제 회복 강조", "불평등 완화와 개혁 과제 제시"],
        "note": "현재 재임 중이므로 평가는 진행 중"
    },
]

# =====================================================
# 퀴즈
# =====================================================
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "quiz_mode" not in st.session_state:
    st.session_state.quiz_mode = "흐름 맞추기"

def make_quiz():
    mode = st.session_state.get("quiz_mode", "흐름 맞추기")

    if mode == "흐름 맞추기":
        question = "다음 중 우리나라 역사 흐름으로 가장 알맞은 것은?"
        correct = "선사 → 고조선 → 삼국 → 남북국 → 고려 → 조선 → 근현대"
        options = [
            correct,
            "조선 → 고려 → 삼국 → 고조선 → 대한민국",
            "삼국 → 선사 → 고려 → 조선 → 고조선",
            "대한민국 → 조선 → 고려 → 삼국 → 고조선"
        ]

    elif mode == "시대 설명 맞추기":
        item = random.choice(PREMODERN_PERIODS)
        question = f"다음 설명에 해당하는 시대는?<br><br>{item['core']}"
        correct = item["name"]
        options = [x["name"] for x in PREMODERN_PERIODS]
        options = random.sample(options, 4)
        if correct not in options:
            options[0] = correct

    elif mode == "연도 맞추기":
        all_items = PREMODERN_PERIODS + MODERN_STEPS + PRESIDENTS
        item = random.choice(all_items)
        item_name = item.get("name", item.get("title", ""))
        question = f"{item_name}의 시기 또는 재임 기간은?"
        correct = item["years"]
        options = [x["years"] for x in all_items]
        options = random.sample(options, 4)
        if correct not in options:
            options[0] = correct

    elif mode == "근현대사 맞추기":
        item = random.choice(MODERN_STEPS)
        question = f"다음 설명에 해당하는 근현대사 단계는?<br><br>{item['summary']}"
        correct = item["title"]
        options = [x["title"] for x in MODERN_STEPS]
        options = random.sample(options, 4)
        if correct not in options:
            options[0] = correct

    elif mode == "대통령 맞추기":
        item = random.choice(PRESIDENTS)
        point = random.choice(item["points"])
        question = f"다음 내용과 관련 깊은 대통령은?<br><br>{point}"
        correct = item["name"]
        options = [x["name"] for x in PRESIDENTS]
        options = random.sample(options, 4)
        if correct not in options:
            options[0] = correct

    else:
        item = random.choice(PRESIDENTS)
        question = f"{item['name']} 대통령의 재임 시기는?"
        correct = item["years"]
        options = [x["years"] for x in PRESIDENTS]
        options = random.sample(options, 4)
        if correct not in options:
            options[0] = correct

    random.shuffle(options)
    st.session_state.quiz_question = question
    st.session_state.quiz_correct = correct
    st.session_state.quiz_options = options
    st.session_state.quiz_answered = False
    st.session_state.quiz_result = ""

if "quiz_options" not in st.session_state:
    make_quiz()

def reset_score():
    st.session_state.score = 0
    st.session_state.total = 0
    make_quiz()

# =====================================================
# 화면
# =====================================================
st.title("🇰🇷 우리나라 역사와 근현대사")
st.caption("각 시대와 단계마다 연도/시기를 함께 표시했습니다.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧭 큰 흐름",
    "🏛️ 고조선~조선",
    "🇰🇷 근현대사",
    "👤 대통령 정리",
    "📌 한눈에 정리",
    "🎮 확인 퀴즈"
])

with tab1:
    st.subheader("🧭 우리나라 역사 큰 흐름")

    cols = st.columns(len(HISTORY_FLOW))
    for i, item in enumerate(HISTORY_FLOW):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"### {item['emoji']}")
                st.markdown(f"**{item['name']}**")
                st.caption(item["years"])
                st.markdown(item["one"])

    st.info("암기 순서: 선사 → 고조선 → 삼국 → 남북국 → 고려 → 조선 → 근현대")

with tab2:
    st.subheader("🏛️ 고조선부터 조선까지")

    for item in PREMODERN_PERIODS:
        with st.container(border=True):
            st.markdown(f"## {item['emoji']} {item['name']}")
            st.caption(item["years"])
            st.markdown(f"**구분:** {item['period']}")
            st.markdown(f"**핵심:** {item['core']}")

            st.markdown("**설명**")
            for d in item["details"]:
                st.markdown(f"- {d}")

            st.markdown("**키워드**")
            st.write(" · ".join(item["keywords"]))

with tab3:
    st.subheader("🇰🇷 근현대사 조금 더 자세히")

    cols = st.columns(4)
    for i, item in enumerate(MODERN_STEPS):
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"### {item['emoji']} {item['title']}")
                st.caption(item["years"])
                st.markdown(item["summary"])
                for d in item["details"]:
                    st.markdown(f"- {d}")
                st.caption(" · ".join(item["keywords"]))

with tab4:
    st.subheader("👤 대한민국 역대 대통령 주요 내용")
    st.warning("대통령별 내용은 수업용 요약입니다. 특정 인물 평가가 아니라 주요 정책·사건·쟁점을 함께 보는 것이 목적입니다.")

    cols = st.columns(3)
    for i, p in enumerate(PRESIDENTS):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {p['order']} {p['name']}")
                st.caption(p["years"])
                st.markdown(f"**핵심:** {p['main']}")
                st.markdown("**주요 내용**")
                for point in p["points"]:
                    st.markdown(f"- {point}")
                st.markdown(f"**함께 볼 점:** {p['note']}")

with tab5:
    st.subheader("📌 한눈에 정리")

    st.markdown("### 고조선~조선")
    st.dataframe(
        [
            {
                "시대": x["name"],
                "연도/시기": x["years"],
                "구분": x["period"],
                "핵심": x["core"],
                "키워드": ", ".join(x["keywords"])
            }
            for x in PREMODERN_PERIODS
        ],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 근현대사")
    st.dataframe(
        [
            {
                "단계": x["title"],
                "연도/시기": x["years"],
                "핵심 설명": x["summary"],
                "키워드": ", ".join(x["keywords"])
            }
            for x in MODERN_STEPS
        ],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 대통령")
    st.dataframe(
        [
            {
                "대수": p["order"],
                "대통령": p["name"],
                "재임 기간": p["years"],
                "핵심": p["main"]
            }
            for p in PRESIDENTS
        ],
        use_container_width=True,
        hide_index=True
    )

with tab6:
    st.subheader("🎮 우리나라 역사 확인 퀴즈")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("점수", f"{st.session_state.score} / {st.session_state.total}")
    with c2:
        acc = round(st.session_state.score / st.session_state.total * 100) if st.session_state.total > 0 else 0
        st.metric("정답률", f"{acc}%")
    with c3:
        if st.button("🔄 점수 초기화", use_container_width=True):
            reset_score()
            st.rerun()

    selected_mode = st.radio(
        "퀴즈 유형",
        ["흐름 맞추기", "시대 설명 맞추기", "연도 맞추기", "근현대사 맞추기", "대통령 맞추기", "재임 시기 맞추기"],
        horizontal=True,
        key="history_quiz_radio_v3"
    )

    if selected_mode != st.session_state.quiz_mode:
        st.session_state.quiz_mode = selected_mode
        make_quiz()
        st.rerun()

    st.markdown(f"### {st.session_state.quiz_question}", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, option in enumerate(st.session_state.quiz_options):
        with cols[i % 2]:
            if st.button(
                option,
                key=f"history_quiz_v3_{i}_{st.session_state.total}",
                use_container_width=True,
                disabled=st.session_state.quiz_answered
            ):
                st.session_state.quiz_answered = True
                st.session_state.total += 1

                if option == st.session_state.quiz_correct:
                    st.session_state.score += 1
                    st.session_state.quiz_result = f"✅ 정답입니다! {st.session_state.quiz_correct}"
                else:
                    st.session_state.quiz_result = f"❌ 아쉬워요. 정답은 `{st.session_state.quiz_correct}`입니다."

                st.rerun()

    if st.session_state.quiz_result:
        if st.session_state.quiz_result.startswith("✅"):
            st.success(st.session_state.quiz_result)
        else:
            st.error(st.session_state.quiz_result)

    if st.button("➡️ 다음 문제", use_container_width=True):
        make_quiz()
        st.rerun()

st.caption("필요 패키지: streamlit")
