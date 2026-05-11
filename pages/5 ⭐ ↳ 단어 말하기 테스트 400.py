import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="Daily English 400 단어 카드 말하기 게임",
    page_icon="🌱",
    layout="wide"
)

# =========================================================
# Daily English 400 단어 데이터
# =========================================================
WORD_THEMES = {
    "🏫 학교생활": [
        {
            "word": "subject",
            "meaning": "과목"
        },
        {
            "word": "math",
            "meaning": "수학"
        },
        {
            "word": "science",
            "meaning": "과학"
        },
        {
            "word": "history",
            "meaning": "역사"
        },
        {
            "word": "music",
            "meaning": "음악"
        },
        {
            "word": "art",
            "meaning": "미술"
        },
        {
            "word": "P.E.",
            "meaning": "체육"
        },
        {
            "word": "club",
            "meaning": "동아리"
        },
        {
            "word": "schedule",
            "meaning": "일정표"
        },
        {
            "word": "semester",
            "meaning": "학기"
        },
        {
            "word": "assignment",
            "meaning": "과제"
        },
        {
            "word": "project",
            "meaning": "프로젝트"
        },
        {
            "word": "presentation",
            "meaning": "발표"
        },
        {
            "word": "report",
            "meaning": "보고서"
        },
        {
            "word": "textbook",
            "meaning": "교과서"
        },
        {
            "word": "workbook",
            "meaning": "문제집"
        },
        {
            "word": "library",
            "meaning": "도서관"
        },
        {
            "word": "cafeteria",
            "meaning": "급식소, 식당"
        },
        {
            "word": "hallway",
            "meaning": "복도"
        },
        {
            "word": "attendance",
            "meaning": "출석"
        }
    ],
    "✏️ 교실 활동": [
        {
            "word": "copy",
            "meaning": "베껴 쓰다"
        },
        {
            "word": "repeat",
            "meaning": "반복하다"
        },
        {
            "word": "underline",
            "meaning": "밑줄 치다"
        },
        {
            "word": "circle",
            "meaning": "동그라미 치다"
        },
        {
            "word": "choose",
            "meaning": "고르다"
        },
        {
            "word": "check",
            "meaning": "확인하다"
        },
        {
            "word": "match",
            "meaning": "연결하다, 맞추다"
        },
        {
            "word": "complete",
            "meaning": "완성하다"
        },
        {
            "word": "fill",
            "meaning": "채우다"
        },
        {
            "word": "spell",
            "meaning": "철자를 말하다"
        },
        {
            "word": "pronounce",
            "meaning": "발음하다"
        },
        {
            "word": "review",
            "meaning": "복습하다"
        },
        {
            "word": "explain",
            "meaning": "설명하다"
        },
        {
            "word": "describe",
            "meaning": "묘사하다"
        },
        {
            "word": "compare",
            "meaning": "비교하다"
        },
        {
            "word": "discuss",
            "meaning": "토론하다"
        },
        {
            "word": "present",
            "meaning": "발표하다"
        },
        {
            "word": "take notes",
            "meaning": "필기하다"
        },
        {
            "word": "turn in",
            "meaning": "제출하다"
        },
        {
            "word": "hand out",
            "meaning": "나누어 주다"
        }
    ],
    "🏠 집과 생활": [
        {
            "word": "living room",
            "meaning": "거실"
        },
        {
            "word": "bedroom",
            "meaning": "침실"
        },
        {
            "word": "kitchen",
            "meaning": "부엌"
        },
        {
            "word": "balcony",
            "meaning": "발코니"
        },
        {
            "word": "floor",
            "meaning": "바닥, 층"
        },
        {
            "word": "wall",
            "meaning": "벽"
        },
        {
            "word": "roof",
            "meaning": "지붕"
        },
        {
            "word": "garden",
            "meaning": "정원"
        },
        {
            "word": "yard",
            "meaning": "마당"
        },
        {
            "word": "sofa",
            "meaning": "소파"
        },
        {
            "word": "television",
            "meaning": "텔레비전"
        },
        {
            "word": "refrigerator",
            "meaning": "냉장고"
        },
        {
            "word": "microwave",
            "meaning": "전자레인지"
        },
        {
            "word": "blanket",
            "meaning": "담요"
        },
        {
            "word": "pillow",
            "meaning": "베개"
        },
        {
            "word": "towel",
            "meaning": "수건"
        },
        {
            "word": "soap",
            "meaning": "비누"
        },
        {
            "word": "mirror",
            "meaning": "거울"
        },
        {
            "word": "closet",
            "meaning": "옷장"
        },
        {
            "word": "trash",
            "meaning": "쓰레기"
        }
    ],
    "🌅 하루 일과": [
        {
            "word": "routine",
            "meaning": "일과"
        },
        {
            "word": "wake up",
            "meaning": "잠에서 깨다"
        },
        {
            "word": "get up",
            "meaning": "일어나다"
        },
        {
            "word": "brush",
            "meaning": "닦다"
        },
        {
            "word": "shower",
            "meaning": "샤워하다"
        },
        {
            "word": "dress",
            "meaning": "옷을 입다"
        },
        {
            "word": "leave",
            "meaning": "떠나다"
        },
        {
            "word": "arrive",
            "meaning": "도착하다"
        },
        {
            "word": "return",
            "meaning": "돌아오다"
        },
        {
            "word": "finish",
            "meaning": "끝내다"
        },
        {
            "word": "relax",
            "meaning": "쉬다"
        },
        {
            "word": "weekday",
            "meaning": "평일"
        },
        {
            "word": "weekend",
            "meaning": "주말"
        },
        {
            "word": "usually",
            "meaning": "보통"
        },
        {
            "word": "often",
            "meaning": "자주"
        },
        {
            "word": "sometimes",
            "meaning": "가끔"
        },
        {
            "word": "always",
            "meaning": "항상"
        },
        {
            "word": "never",
            "meaning": "절대 ~않다"
        },
        {
            "word": "habit",
            "meaning": "습관"
        },
        {
            "word": "lifestyle",
            "meaning": "생활 방식"
        }
    ],
    "🎮 취미와 여가": [
        {
            "word": "hobby",
            "meaning": "취미"
        },
        {
            "word": "movie",
            "meaning": "영화"
        },
        {
            "word": "drama",
            "meaning": "드라마"
        },
        {
            "word": "song",
            "meaning": "노래"
        },
        {
            "word": "concert",
            "meaning": "콘서트"
        },
        {
            "word": "dance",
            "meaning": "춤"
        },
        {
            "word": "drawing",
            "meaning": "그림 그리기"
        },
        {
            "word": "painting",
            "meaning": "그림, 회화"
        },
        {
            "word": "comic",
            "meaning": "만화"
        },
        {
            "word": "novel",
            "meaning": "소설"
        },
        {
            "word": "photography",
            "meaning": "사진 촬영"
        },
        {
            "word": "cooking",
            "meaning": "요리"
        },
        {
            "word": "baking",
            "meaning": "빵 굽기"
        },
        {
            "word": "camping",
            "meaning": "캠핑"
        },
        {
            "word": "hiking",
            "meaning": "하이킹"
        },
        {
            "word": "fishing",
            "meaning": "낚시"
        },
        {
            "word": "free time",
            "meaning": "여가 시간"
        },
        {
            "word": "favorite",
            "meaning": "가장 좋아하는"
        },
        {
            "word": "popular",
            "meaning": "인기 있는"
        },
        {
            "word": "relaxing",
            "meaning": "편안한"
        }
    ],
    "⚽ 운동과 활동": [
        {
            "word": "soccer",
            "meaning": "축구"
        },
        {
            "word": "baseball",
            "meaning": "야구"
        },
        {
            "word": "basketball",
            "meaning": "농구"
        },
        {
            "word": "volleyball",
            "meaning": "배구"
        },
        {
            "word": "tennis",
            "meaning": "테니스"
        },
        {
            "word": "badminton",
            "meaning": "배드민턴"
        },
        {
            "word": "swimming",
            "meaning": "수영"
        },
        {
            "word": "cycling",
            "meaning": "자전거 타기"
        },
        {
            "word": "skating",
            "meaning": "스케이트 타기"
        },
        {
            "word": "boxing",
            "meaning": "복싱"
        },
        {
            "word": "taekwondo",
            "meaning": "태권도"
        },
        {
            "word": "yoga",
            "meaning": "요가"
        },
        {
            "word": "fitness",
            "meaning": "체력 운동"
        },
        {
            "word": "field",
            "meaning": "경기장, 들판"
        },
        {
            "word": "court",
            "meaning": "코트"
        },
        {
            "word": "stadium",
            "meaning": "경기장"
        },
        {
            "word": "coach",
            "meaning": "코치"
        },
        {
            "word": "match",
            "meaning": "경기"
        },
        {
            "word": "competition",
            "meaning": "대회"
        },
        {
            "word": "medal",
            "meaning": "메달"
        }
    ],
    "🌦️ 날씨와 계절": [
        {
            "word": "season",
            "meaning": "계절"
        },
        {
            "word": "spring",
            "meaning": "봄"
        },
        {
            "word": "summer",
            "meaning": "여름"
        },
        {
            "word": "fall",
            "meaning": "가을"
        },
        {
            "word": "winter",
            "meaning": "겨울"
        },
        {
            "word": "cloudy",
            "meaning": "흐린"
        },
        {
            "word": "rainy",
            "meaning": "비 오는"
        },
        {
            "word": "snowy",
            "meaning": "눈 오는"
        },
        {
            "word": "windy",
            "meaning": "바람 부는"
        },
        {
            "word": "stormy",
            "meaning": "폭풍우 치는"
        },
        {
            "word": "foggy",
            "meaning": "안개 낀"
        },
        {
            "word": "dry",
            "meaning": "건조한"
        },
        {
            "word": "wet",
            "meaning": "젖은"
        },
        {
            "word": "humid",
            "meaning": "습한"
        },
        {
            "word": "temperature",
            "meaning": "온도"
        },
        {
            "word": "degree",
            "meaning": "도"
        },
        {
            "word": "forecast",
            "meaning": "일기예보"
        },
        {
            "word": "umbrella",
            "meaning": "우산"
        },
        {
            "word": "raincoat",
            "meaning": "비옷"
        },
        {
            "word": "rainbow",
            "meaning": "무지개"
        }
    ],
    "🌳 자연과 환경": [
        {
            "word": "nature",
            "meaning": "자연"
        },
        {
            "word": "environment",
            "meaning": "환경"
        },
        {
            "word": "plant",
            "meaning": "식물"
        },
        {
            "word": "forest",
            "meaning": "숲"
        },
        {
            "word": "lake",
            "meaning": "호수"
        },
        {
            "word": "ocean",
            "meaning": "대양"
        },
        {
            "word": "island",
            "meaning": "섬"
        },
        {
            "word": "desert",
            "meaning": "사막"
        },
        {
            "word": "field",
            "meaning": "들판"
        },
        {
            "word": "farm",
            "meaning": "농장"
        },
        {
            "word": "village",
            "meaning": "마을"
        },
        {
            "word": "leaf",
            "meaning": "잎"
        },
        {
            "word": "root",
            "meaning": "뿌리"
        },
        {
            "word": "stone",
            "meaning": "돌"
        },
        {
            "word": "sand",
            "meaning": "모래"
        },
        {
            "word": "soil",
            "meaning": "흙"
        },
        {
            "word": "plastic",
            "meaning": "플라스틱"
        },
        {
            "word": "recycle",
            "meaning": "재활용하다"
        },
        {
            "word": "protect",
            "meaning": "보호하다"
        },
        {
            "word": "pollution",
            "meaning": "오염"
        }
    ],
    "🍽️ 식당과 주문": [
        {
            "word": "restaurant",
            "meaning": "식당"
        },
        {
            "word": "menu",
            "meaning": "메뉴"
        },
        {
            "word": "seat",
            "meaning": "자리"
        },
        {
            "word": "waiter",
            "meaning": "남자 종업원"
        },
        {
            "word": "waitress",
            "meaning": "여자 종업원"
        },
        {
            "word": "order",
            "meaning": "주문하다"
        },
        {
            "word": "dish",
            "meaning": "요리, 접시"
        },
        {
            "word": "meal",
            "meaning": "식사"
        },
        {
            "word": "soup",
            "meaning": "수프"
        },
        {
            "word": "salad",
            "meaning": "샐러드"
        },
        {
            "word": "steak",
            "meaning": "스테이크"
        },
        {
            "word": "pizza",
            "meaning": "피자"
        },
        {
            "word": "pasta",
            "meaning": "파스타"
        },
        {
            "word": "burger",
            "meaning": "버거"
        },
        {
            "word": "sandwich",
            "meaning": "샌드위치"
        },
        {
            "word": "dessert",
            "meaning": "디저트"
        },
        {
            "word": "spicy",
            "meaning": "매운"
        },
        {
            "word": "sweet",
            "meaning": "단"
        },
        {
            "word": "bill",
            "meaning": "계산서"
        },
        {
            "word": "receipt",
            "meaning": "영수증"
        }
    ],
    "🛍️ 쇼핑과 가격": [
        {
            "word": "shop",
            "meaning": "가게"
        },
        {
            "word": "market",
            "meaning": "시장"
        },
        {
            "word": "mall",
            "meaning": "쇼핑몰"
        },
        {
            "word": "supermarket",
            "meaning": "슈퍼마켓"
        },
        {
            "word": "cashier",
            "meaning": "계산원"
        },
        {
            "word": "customer",
            "meaning": "손님"
        },
        {
            "word": "price",
            "meaning": "가격"
        },
        {
            "word": "sale",
            "meaning": "할인 판매"
        },
        {
            "word": "discount",
            "meaning": "할인"
        },
        {
            "word": "coupon",
            "meaning": "쿠폰"
        },
        {
            "word": "change",
            "meaning": "거스름돈"
        },
        {
            "word": "coin",
            "meaning": "동전"
        },
        {
            "word": "bill",
            "meaning": "지폐, 계산서"
        },
        {
            "word": "expensive",
            "meaning": "비싼"
        },
        {
            "word": "cheap",
            "meaning": "싼"
        },
        {
            "word": "size",
            "meaning": "크기"
        },
        {
            "word": "color",
            "meaning": "색깔"
        },
        {
            "word": "brand",
            "meaning": "상표"
        },
        {
            "word": "exchange",
            "meaning": "교환하다"
        },
        {
            "word": "refund",
            "meaning": "환불"
        }
    ],
    "👕 옷과 외모": [
        {
            "word": "T-shirt",
            "meaning": "티셔츠"
        },
        {
            "word": "pants",
            "meaning": "바지"
        },
        {
            "word": "jeans",
            "meaning": "청바지"
        },
        {
            "word": "shorts",
            "meaning": "반바지"
        },
        {
            "word": "skirt",
            "meaning": "치마"
        },
        {
            "word": "dress",
            "meaning": "드레스, 원피스"
        },
        {
            "word": "jacket",
            "meaning": "재킷"
        },
        {
            "word": "coat",
            "meaning": "코트"
        },
        {
            "word": "sweater",
            "meaning": "스웨터"
        },
        {
            "word": "hoodie",
            "meaning": "후드티"
        },
        {
            "word": "uniform",
            "meaning": "교복, 제복"
        },
        {
            "word": "socks",
            "meaning": "양말"
        },
        {
            "word": "sneakers",
            "meaning": "운동화"
        },
        {
            "word": "boots",
            "meaning": "부츠"
        },
        {
            "word": "sandals",
            "meaning": "샌들"
        },
        {
            "word": "scarf",
            "meaning": "목도리"
        },
        {
            "word": "gloves",
            "meaning": "장갑"
        },
        {
            "word": "belt",
            "meaning": "벨트"
        },
        {
            "word": "glasses",
            "meaning": "안경"
        },
        {
            "word": "comfortable",
            "meaning": "편안한"
        }
    ],
    "🚇 교통과 길 찾기": [
        {
            "word": "bus stop",
            "meaning": "버스 정류장"
        },
        {
            "word": "subway",
            "meaning": "지하철"
        },
        {
            "word": "airport",
            "meaning": "공항"
        },
        {
            "word": "terminal",
            "meaning": "터미널"
        },
        {
            "word": "platform",
            "meaning": "승강장"
        },
        {
            "word": "route",
            "meaning": "경로"
        },
        {
            "word": "direction",
            "meaning": "방향"
        },
        {
            "word": "straight",
            "meaning": "똑바로"
        },
        {
            "word": "corner",
            "meaning": "모퉁이"
        },
        {
            "word": "block",
            "meaning": "구역, 블록"
        },
        {
            "word": "traffic",
            "meaning": "교통"
        },
        {
            "word": "crosswalk",
            "meaning": "횡단보도"
        },
        {
            "word": "sidewalk",
            "meaning": "인도"
        },
        {
            "word": "bridge",
            "meaning": "다리"
        },
        {
            "word": "tunnel",
            "meaning": "터널"
        },
        {
            "word": "entrance",
            "meaning": "입구"
        },
        {
            "word": "exit",
            "meaning": "출구"
        },
        {
            "word": "transfer",
            "meaning": "갈아타다"
        },
        {
            "word": "lost",
            "meaning": "길을 잃은"
        },
        {
            "word": "guide",
            "meaning": "안내하다, 안내자"
        }
    ],
    "🧳 여행과 숙박": [
        {
            "word": "travel",
            "meaning": "여행하다"
        },
        {
            "word": "trip",
            "meaning": "여행"
        },
        {
            "word": "vacation",
            "meaning": "방학, 휴가"
        },
        {
            "word": "tourist",
            "meaning": "관광객"
        },
        {
            "word": "guide",
            "meaning": "안내자"
        },
        {
            "word": "passport",
            "meaning": "여권"
        },
        {
            "word": "flight",
            "meaning": "항공편"
        },
        {
            "word": "hotel",
            "meaning": "호텔"
        },
        {
            "word": "motel",
            "meaning": "모텔"
        },
        {
            "word": "hostel",
            "meaning": "호스텔"
        },
        {
            "word": "reservation",
            "meaning": "예약"
        },
        {
            "word": "check in",
            "meaning": "체크인하다"
        },
        {
            "word": "check out",
            "meaning": "체크아웃하다"
        },
        {
            "word": "luggage",
            "meaning": "짐"
        },
        {
            "word": "suitcase",
            "meaning": "여행 가방"
        },
        {
            "word": "backpack",
            "meaning": "배낭"
        },
        {
            "word": "souvenir",
            "meaning": "기념품"
        },
        {
            "word": "museum",
            "meaning": "박물관"
        },
        {
            "word": "famous",
            "meaning": "유명한"
        },
        {
            "word": "local",
            "meaning": "현지의"
        }
    ],
    "👥 친구 관계": [
        {
            "word": "friendship",
            "meaning": "우정"
        },
        {
            "word": "best friend",
            "meaning": "가장 친한 친구"
        },
        {
            "word": "teammate",
            "meaning": "팀 동료"
        },
        {
            "word": "partner",
            "meaning": "짝, 파트너"
        },
        {
            "word": "message",
            "meaning": "메시지"
        },
        {
            "word": "call",
            "meaning": "전화하다"
        },
        {
            "word": "chat",
            "meaning": "채팅하다"
        },
        {
            "word": "invite",
            "meaning": "초대하다"
        },
        {
            "word": "visit",
            "meaning": "방문하다"
        },
        {
            "word": "meet",
            "meaning": "만나다"
        },
        {
            "word": "hang out",
            "meaning": "어울려 놀다"
        },
        {
            "word": "laugh",
            "meaning": "웃다"
        },
        {
            "word": "share",
            "meaning": "나누다, 공유하다"
        },
        {
            "word": "trust",
            "meaning": "믿다"
        },
        {
            "word": "promise",
            "meaning": "약속"
        },
        {
            "word": "secret",
            "meaning": "비밀"
        },
        {
            "word": "joke",
            "meaning": "농담"
        },
        {
            "word": "together",
            "meaning": "함께"
        },
        {
            "word": "alone",
            "meaning": "혼자"
        },
        {
            "word": "forgive",
            "meaning": "용서하다"
        }
    ],
    "😊 감정 표현 확장": [
        {
            "word": "excited",
            "meaning": "신난"
        },
        {
            "word": "nervous",
            "meaning": "긴장한"
        },
        {
            "word": "bored",
            "meaning": "지루한"
        },
        {
            "word": "surprised",
            "meaning": "놀란"
        },
        {
            "word": "confused",
            "meaning": "혼란스러운"
        },
        {
            "word": "embarrassed",
            "meaning": "당황한"
        },
        {
            "word": "proud",
            "meaning": "자랑스러운"
        },
        {
            "word": "disappointed",
            "meaning": "실망한"
        },
        {
            "word": "lonely",
            "meaning": "외로운"
        },
        {
            "word": "relaxed",
            "meaning": "편안한"
        },
        {
            "word": "calm",
            "meaning": "차분한"
        },
        {
            "word": "upset",
            "meaning": "속상한"
        },
        {
            "word": "interested",
            "meaning": "관심 있는"
        },
        {
            "word": "satisfied",
            "meaning": "만족한"
        },
        {
            "word": "thankful",
            "meaning": "감사하는"
        },
        {
            "word": "hopeful",
            "meaning": "희망적인"
        },
        {
            "word": "mood",
            "meaning": "기분"
        },
        {
            "word": "stress",
            "meaning": "스트레스"
        },
        {
            "word": "confidence",
            "meaning": "자신감"
        },
        {
            "word": "courage",
            "meaning": "용기"
        }
    ],
    "💭 생각과 의견": [
        {
            "word": "think",
            "meaning": "생각하다"
        },
        {
            "word": "believe",
            "meaning": "믿다"
        },
        {
            "word": "guess",
            "meaning": "추측하다"
        },
        {
            "word": "remember",
            "meaning": "기억하다"
        },
        {
            "word": "forget",
            "meaning": "잊다"
        },
        {
            "word": "mean",
            "meaning": "의미하다"
        },
        {
            "word": "agree",
            "meaning": "동의하다"
        },
        {
            "word": "disagree",
            "meaning": "동의하지 않다"
        },
        {
            "word": "opinion",
            "meaning": "의견"
        },
        {
            "word": "idea",
            "meaning": "생각, 아이디어"
        },
        {
            "word": "reason",
            "meaning": "이유"
        },
        {
            "word": "example",
            "meaning": "예시"
        },
        {
            "word": "fact",
            "meaning": "사실"
        },
        {
            "word": "choice",
            "meaning": "선택"
        },
        {
            "word": "decision",
            "meaning": "결정"
        },
        {
            "word": "advice",
            "meaning": "조언"
        },
        {
            "word": "suggestion",
            "meaning": "제안"
        },
        {
            "word": "possible",
            "meaning": "가능한"
        },
        {
            "word": "impossible",
            "meaning": "불가능한"
        },
        {
            "word": "confusing",
            "meaning": "혼란스러운"
        }
    ],
    "📅 계획과 약속": [
        {
            "word": "plan",
            "meaning": "계획"
        },
        {
            "word": "appointment",
            "meaning": "약속, 예약"
        },
        {
            "word": "promise",
            "meaning": "약속"
        },
        {
            "word": "meeting",
            "meaning": "모임, 회의"
        },
        {
            "word": "date",
            "meaning": "날짜, 데이트"
        },
        {
            "word": "event",
            "meaning": "행사"
        },
        {
            "word": "party",
            "meaning": "파티"
        },
        {
            "word": "festival",
            "meaning": "축제"
        },
        {
            "word": "deadline",
            "meaning": "마감일"
        },
        {
            "word": "calendar",
            "meaning": "달력"
        },
        {
            "word": "next week",
            "meaning": "다음 주"
        },
        {
            "word": "message",
            "meaning": "메시지"
        },
        {
            "word": "join",
            "meaning": "참여하다"
        },
        {
            "word": "prepare",
            "meaning": "준비하다"
        },
        {
            "word": "decide",
            "meaning": "결정하다"
        },
        {
            "word": "change",
            "meaning": "바꾸다"
        },
        {
            "word": "cancel",
            "meaning": "취소하다"
        },
        {
            "word": "on time",
            "meaning": "시간 맞춰"
        },
        {
            "word": "available",
            "meaning": "시간이 되는, 이용 가능한"
        },
        {
            "word": "reminder",
            "meaning": "알림"
        }
    ],
    "🩺 건강한 생활": [
        {
            "word": "health",
            "meaning": "건강"
        },
        {
            "word": "body",
            "meaning": "몸"
        },
        {
            "word": "eye",
            "meaning": "눈"
        },
        {
            "word": "ear",
            "meaning": "귀"
        },
        {
            "word": "nose",
            "meaning": "코"
        },
        {
            "word": "mouth",
            "meaning": "입"
        },
        {
            "word": "tooth",
            "meaning": "이"
        },
        {
            "word": "hand",
            "meaning": "손"
        },
        {
            "word": "arm",
            "meaning": "팔"
        },
        {
            "word": "leg",
            "meaning": "다리"
        },
        {
            "word": "foot",
            "meaning": "발"
        },
        {
            "word": "stomach",
            "meaning": "배, 위"
        },
        {
            "word": "back",
            "meaning": "등, 허리"
        },
        {
            "word": "heart",
            "meaning": "심장"
        },
        {
            "word": "clinic",
            "meaning": "의원, 진료소"
        },
        {
            "word": "vitamin",
            "meaning": "비타민"
        },
        {
            "word": "diet",
            "meaning": "식단"
        },
        {
            "word": "cough",
            "meaning": "기침"
        },
        {
            "word": "flu",
            "meaning": "독감"
        },
        {
            "word": "breathe",
            "meaning": "숨 쉬다"
        }
    ],
    "📱 미디어와 스마트폰": [
        {
            "word": "smartphone",
            "meaning": "스마트폰"
        },
        {
            "word": "screen",
            "meaning": "화면"
        },
        {
            "word": "app",
            "meaning": "앱"
        },
        {
            "word": "website",
            "meaning": "웹사이트"
        },
        {
            "word": "internet",
            "meaning": "인터넷"
        },
        {
            "word": "Wi-Fi",
            "meaning": "와이파이"
        },
        {
            "word": "password",
            "meaning": "비밀번호"
        },
        {
            "word": "text",
            "meaning": "문자 메시지"
        },
        {
            "word": "video call",
            "meaning": "영상 통화"
        },
        {
            "word": "gallery",
            "meaning": "사진첩"
        },
        {
            "word": "news",
            "meaning": "뉴스"
        },
        {
            "word": "channel",
            "meaning": "채널"
        },
        {
            "word": "post",
            "meaning": "게시물"
        },
        {
            "word": "comment",
            "meaning": "댓글"
        },
        {
            "word": "upload",
            "meaning": "업로드하다"
        },
        {
            "word": "download",
            "meaning": "다운로드하다"
        },
        {
            "word": "search",
            "meaning": "검색하다"
        },
        {
            "word": "click",
            "meaning": "클릭하다"
        },
        {
            "word": "battery",
            "meaning": "배터리"
        },
        {
            "word": "notification",
            "meaning": "알림"
        }
    ],
    "🌈 직업과 미래": [
        {
            "word": "job",
            "meaning": "직업"
        },
        {
            "word": "work",
            "meaning": "일하다"
        },
        {
            "word": "company",
            "meaning": "회사"
        },
        {
            "word": "office",
            "meaning": "사무실"
        },
        {
            "word": "factory",
            "meaning": "공장"
        },
        {
            "word": "engineer",
            "meaning": "기술자, 엔지니어"
        },
        {
            "word": "mechanic",
            "meaning": "정비사"
        },
        {
            "word": "chef",
            "meaning": "요리사"
        },
        {
            "word": "firefighter",
            "meaning": "소방관"
        },
        {
            "word": "farmer",
            "meaning": "농부"
        },
        {
            "word": "designer",
            "meaning": "디자이너"
        },
        {
            "word": "singer",
            "meaning": "가수"
        },
        {
            "word": "actor",
            "meaning": "배우"
        },
        {
            "word": "athlete",
            "meaning": "운동선수"
        },
        {
            "word": "dream",
            "meaning": "꿈"
        },
        {
            "word": "future",
            "meaning": "미래"
        },
        {
            "word": "goal",
            "meaning": "목표"
        },
        {
            "word": "skill",
            "meaning": "기술, 능력"
        },
        {
            "word": "interview",
            "meaning": "면접"
        },
        {
            "word": "experience",
            "meaning": "경험"
        }
    ]
}

# =========================================================
# 상단 디자인
# =========================================================
st.markdown(
    """
    <style>
    .main-title-box {
        background: linear-gradient(135deg, #dcfce7 0%, #e0f2fe 50%, #fef3c7 100%);
        border: 1.5px solid #bbf7d0;
        border-radius: 30px;
        padding: 28px 30px;
        margin-bottom: 22px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.07);
    }

    .main-title-box h1 {
        margin: 0 0 10px 0;
        color: #0f172a;
        font-size: 38px;
        font-weight: 900;
    }

    .main-title-box p {
        margin: 0;
        color: #475569;
        font-size: 18px;
        line-height: 1.7;
        font-weight: 700;
    }

    @media (max-width: 768px) {
        .main-title-box {
            padding: 20px 18px;
            border-radius: 22px;
        }

        .main-title-box h1 {
            font-size: 27px;
        }

        .main-title-box p {
            font-size: 15px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-title-box">
        <h1>🌱 Daily English 400 단어 카드 말하기 게임</h1>
        <p>
            한국말 뜻을 보고 <b>영어 단어 또는 표현</b>을 말해 보세요.<br>
            음성 인식으로 정답이면 자동으로 다음 카드로 넘어갑니다.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 말하기 카드 게임 컴포넌트
# =========================================================
def daily_word_card_speaking_game(word_themes):
    items = []
    for cat, words in word_themes.items():
        cat_emoji = cat.split()[0] if cat else "🌱"
        for item in words:
            new_item = dict(item)
            new_item["cat"] = cat
            new_item["emoji"] = cat_emoji
            items.append(new_item)

    items_json = json.dumps(items, ensure_ascii=False)

    html = r"""
    <div id="daily-word-card-app" style="
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #f0fdf4 0%, #eff6ff 50%, #fff7ed 100%);
        border: 1.5px solid #bbf7d0;
        border-radius: 30px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        max-width: 100%;
        overflow-x: hidden;
        box-sizing: border-box;
    ">
        <style>
            #daily-word-card-app * {
                box-sizing: border-box;
            }

            #daily-word-card-app button {
                -webkit-tap-highlight-color: transparent;
                touch-action: manipulation;
            }

            #daily-word-card-app select {
                max-width: 100%;
            }

            .bounce-card {
                animation: cardBounce 0.42s ease;
            }

            @keyframes cardBounce {
                0% { transform: scale(1); }
                40% { transform: scale(1.035); }
                100% { transform: scale(1); }
            }

            @media (max-width: 768px) {
                #daily-word-card-app {
                    padding: 14px !important;
                    border-radius: 22px !important;
                }

                #categorySelect {
                    width: 100%;
                    font-size: 14px !important;
                }

                #topControlBox {
                    gap: 8px !important;
                }

                #topControlBox button {
                    flex: 1 1 45%;
                    font-size: 14px !important;
                    padding: 10px 10px !important;
                }

                #cardBox {
                    padding: 18px 14px !important;
                    border-radius: 24px !important;
                }

                #emojiBox {
                    font-size: 72px !important;
                }

                #meaningBox {
                    font-size: 32px !important;
                    line-height: 1.25 !important;
                }

                #answerBox {
                    font-size: 27px !important;
                    padding: 14px 12px !important;
                    word-break: break-word;
                }

                #buttonBox button {
                    flex: 1 1 100%;
                    font-size: 16px !important;
                    padding: 13px 12px !important;
                }

                #transcriptBox {
                    font-size: 19px !important;
                }

                #resultBox {
                    font-size: 17px !important;
                }
            }
        </style>

        <div id="topControlBox" style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:18px;">
            <label style="font-weight:900; color:#334155;">단어 테마 선택</label>
            <select id="categorySelect" style="
                padding: 10px 14px;
                border-radius: 999px;
                border: 1.5px solid #bbf7d0;
                font-size: 15px;
                font-weight: 800;
                color: #0f172a;
                background: white;
            "></select>

            <button id="randomBtn" style="
                border: 1.5px solid #c7d2fe;
                background: white;
                color: #3730a3;
                border-radius: 999px;
                padding: 10px 15px;
                font-weight: 900;
                cursor: pointer;
            ">🎲 섞어서 풀기</button>

            <button id="resetBtn" style="
                border: 1.5px solid #fed7aa;
                background: #fff7ed;
                color: #9a3412;
                border-radius: 999px;
                padding: 10px 15px;
                font-weight: 900;
                cursor: pointer;
            ">🔄 다시 시작</button>
        </div>

        <div id="gameArea">
            <div style="display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <div id="categoryLabel" style="
                    display:inline-block;
                    background:#eff6ff;
                    color:#1d4ed8;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1px solid #bfdbfe;
                "></div>

                <div id="scoreLabel" style="
                    display:inline-block;
                    background:#f0fdf4;
                    color:#166534;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1px solid #bbf7d0;
                ">정답 0 / 0 · 못 말한 단어 0</div>
            </div>

            <div id="cardBox" style="
                background:white;
                border-radius:32px;
                padding:30px 24px;
                border:1.5px solid #dcfce7;
                box-shadow:0 8px 24px rgba(0,0,0,0.07);
                text-align:center;
                margin-bottom:18px;
            ">
                <div id="emojiBox" style="
                    font-size: 96px;
                    line-height: 1.1;
                    margin-bottom: 14px;
                ">🌱</div>

                <div style="
                    display:inline-block;
                    background:#fef3c7;
                    color:#92400e;
                    border:1.5px solid #fde68a;
                    border-radius:999px;
                    padding:7px 14px;
                    font-size:14px;
                    font-weight:900;
                    margin-bottom:14px;
                ">한국말 뜻</div>

                <div id="meaningBox" style="
                    font-size: 44px;
                    font-weight: 900;
                    color: #111827;
                    line-height: 1.35;
                    margin-bottom: 16px;
                ">뜻</div>

                <div id="answerBox" style="
                    display:none;
                    background:#ecfdf5;
                    border:1.5px solid #bbf7d0;
                    color:#166534;
                    border-radius:20px;
                    padding:16px 18px;
                    font-size:34px;
                    font-weight:900;
                    margin-top:18px;
                ">answer</div>
            </div>

            <div id="buttonBox" style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:16px;">
                <button id="micBtn" style="
                    border:1.5px solid #fecaca;
                    background:#fff1f2;
                    color:#be123c;
                    border-radius:999px;
                    padding:13px 20px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:17px;
                ">🎙️ 말하기</button>

                <button id="answerBtn" style="
                    border:1.5px solid #bfdbfe;
                    background:#eff6ff;
                    color:#1d4ed8;
                    border-radius:999px;
                    padding:13px 20px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:17px;
                ">🔊 정답 듣기/보기</button>

                <button id="skipBtn" style="
                    border:1.5px solid #c7d2fe;
                    background:#eef2ff;
                    color:#3730a3;
                    border-radius:999px;
                    padding:13px 20px;
                    font-weight:900;
                    cursor:pointer;
                    font-size:17px;
                ">➡️ 다음 단어</button>
            </div>

            <div style="
                background:#f8fafc;
                border:1.5px solid #e2e8f0;
                border-radius:18px;
                padding:14px 16px;
                margin-bottom:14px;
                min-height:54px;
            ">
                <div style="font-size:13px; color:#64748b; font-weight:900; margin-bottom:5px;">인식된 단어</div>
                <div id="transcriptBox" style="font-size:22px; font-weight:900; color:#334155;"></div>
            </div>

            <div id="resultBox" style="
                background:#f1f5f9;
                border:1.5px solid #e2e8f0;
                border-radius:18px;
                padding:14px 16px;
                font-size:20px;
                font-weight:900;
                color:#334155;
            ">
                마이크 버튼을 누르고 영어 단어를 말해 보세요.
            </div>
        </div>

        <div id="finishBox" style="
            display:none;
            background:white;
            border-radius:30px;
            padding:30px 24px;
            border:1.5px solid #bbf7d0;
            box-shadow:0 8px 24px rgba(0,0,0,0.07);
            text-align:center;
            margin-top:16px;
        ">
            <div style="font-size:64px; margin-bottom:10px;">🎉</div>
            <div id="finishTitle" style="
                font-size:34px;
                font-weight:900;
                color:#14532d;
                margin-bottom:10px;
            ">테마 완료!</div>
            <div id="finishScore" style="
                font-size:24px;
                font-weight:900;
                color:#166534;
                margin-bottom:18px;
            ">정답 0 / 0 · 못 말한 단어 0</div>
            <button id="finishRetryBtn" style="
                border:1.5px solid #a7f3d0;
                background:#ecfdf5;
                color:#047857;
                border-radius:999px;
                padding:13px 22px;
                font-weight:900;
                cursor:pointer;
                font-size:17px;
            ">🔁 다시 풀기</button>
        </div>
    </div>

    <script>
    const ITEMS = __ITEMS_JSON__;

    let currentList = [];
    let currentIndex = 0;
    let currentItem = null;
    let correctMap = {};
    let missedMap = {};
    let finished = false;

    const categorySelect = document.getElementById("categorySelect");
    const randomBtn = document.getElementById("randomBtn");
    const resetBtn = document.getElementById("resetBtn");

    const gameArea = document.getElementById("gameArea");
    const finishBox = document.getElementById("finishBox");
    const finishScore = document.getElementById("finishScore");
    const finishRetryBtn = document.getElementById("finishRetryBtn");

    const categoryLabel = document.getElementById("categoryLabel");
    const scoreLabel = document.getElementById("scoreLabel");
    const cardBox = document.getElementById("cardBox");
    const emojiBox = document.getElementById("emojiBox");
    const meaningBox = document.getElementById("meaningBox");
    const answerBox = document.getElementById("answerBox");

    const micBtn = document.getElementById("micBtn");
    const answerBtn = document.getElementById("answerBtn");
    const skipBtn = document.getElementById("skipBtn");

    const transcriptBox = document.getElementById("transcriptBox");
    const resultBox = document.getElementById("resultBox");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    function uniqueCategories() {
        const cats = ["전체"];
        ITEMS.forEach(item => {
            if (!cats.includes(item.cat)) cats.push(item.cat);
        });
        return cats;
    }

    function initCategories() {
        const cats = uniqueCategories();
        categorySelect.innerHTML = "";
        cats.forEach(cat => {
            const option = document.createElement("option");
            option.value = cat;
            option.innerText = cat;
            categorySelect.appendChild(option);
        });
    }

    function getFilteredItems() {
        const selected = categorySelect.value;
        if (selected === "전체") return ITEMS.slice();
        return ITEMS.filter(item => item.cat === selected);
    }

    function getItemKey(item) {
        return item.cat + "||" + item.meaning + "||" + item.word;
    }

    function shuffleArray(arr) {
        const copied = arr.slice();
        for (let i = copied.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copied[i], copied[j]] = [copied[j], copied[i]];
        }
        return copied;
    }

    function normalizeText(text) {
        return String(text || "")
            .toLowerCase()
            .replace(/\bp\.?e\.?\b/g, "pe")
            .replace(/\bt shirt\b/g, "t shirt")
            .replace(/[.,!?;:'"’‘“”]/g, "")
            .replace(/-/g, " ")
            .replace(/\s+/g, " ")
            .trim();
    }

    function isCorrectSpeech(spoken, answer) {
        const s = normalizeText(spoken);
        const a = normalizeText(answer);

        if (!s || !a) return false;
        if (s === a) return true;

        const spokenWords = s.split(" ").filter(Boolean);
        const answerWords = a.split(" ").filter(Boolean);

        // 한 단어 정답: 앞뒤에 다른 말이 조금 붙어도 핵심 단어가 있으면 정답
        if (answerWords.length === 1) {
            return spokenWords.includes(a);
        }

        // 두 단어 이상 표현: 표현 전체가 포함되면 정답
        if (s.includes(a)) return true;

        // 표현 단어들이 순서대로 들어오면 정답
        let pos = 0;
        for (const w of spokenWords) {
            if (w === answerWords[pos]) pos += 1;
            if (pos >= answerWords.length) return true;
        }

        return false;
    }

    function countCorrectInCurrentTheme() {
        const list = getFilteredItems();
        let count = 0;

        list.forEach(item => {
            if (correctMap[getItemKey(item)]) count += 1;
        });

        return count;
    }

    function countMissedInCurrentTheme() {
        const list = getFilteredItems();
        let count = 0;

        list.forEach(item => {
            if (missedMap[getItemKey(item)]) count += 1;
        });

        return count;
    }

    function updateScore() {
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentTheme();
        const missedCount = countMissedInCurrentTheme();
        scoreLabel.innerText = "정답 " + correctCount + " / " + list.length + " · 못 말한 단어 " + missedCount;
    }

    function speak(text) {
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        utterance.rate = 0.82;
        utterance.pitch = 1.05;

        const voices = window.speechSynthesis.getVoices();
        const preferred = voices.find(v =>
            v.lang && v.lang.toLowerCase().startsWith("en") &&
            /(samantha|jenny|aria|zira|google us english|karen|victoria|female)/i.test(v.name)
        );
        if (preferred) utterance.voice = preferred;

        window.speechSynthesis.speak(utterance);
    }

    function showGameArea() {
        gameArea.style.display = "block";
        finishBox.style.display = "none";
        finished = false;
    }

    function showFinishScreen() {
        finished = true;
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentTheme();
        const missedCount = countMissedInCurrentTheme();

        finishScore.innerText = "정답 " + correctCount + " / " + list.length + " · 못 말한 단어 " + missedCount;

        gameArea.style.display = "none";
        finishBox.style.display = "block";
    }

    function loadQuestion(index = 0) {
        if (currentList.length === 0) {
            currentList = getFilteredItems();
        }

        if (index >= currentList.length) {
            showFinishScreen();
            return;
        }

        if (index < 0) index = 0;

        showGameArea();

        currentIndex = index;
        currentItem = currentList[currentIndex];

        categoryLabel.innerText = currentItem.cat + " · " + (currentIndex + 1) + " / " + currentList.length;
        emojiBox.innerText = currentItem.emoji || "🌱";
        meaningBox.innerText = currentItem.meaning;

        answerBox.style.display = "none";
        answerBox.innerText = "정답: " + currentItem.word;

        transcriptBox.innerText = "";
        resultBox.innerText = "마이크 버튼을 누르고 영어 단어를 말해 보세요.";
        resultBox.style.background = "#f1f5f9";
        resultBox.style.borderColor = "#e2e8f0";
        resultBox.style.color = "#334155";

        cardBox.classList.remove("bounce-card");
        void cardBox.offsetWidth;
        cardBox.classList.add("bounce-card");

        updateScore();
    }

    function goNextCard() {
        if (currentIndex + 1 >= currentList.length) {
            showFinishScreen();
        } else {
            loadQuestion(currentIndex + 1);
        }
    }

    function checkSpeech(spokenText) {
        if (!currentItem) return;

        if (isCorrectSpeech(spokenText, currentItem.word)) {
            correctMap[getItemKey(currentItem)] = true;
            delete missedMap[getItemKey(currentItem)];
            updateScore();

            resultBox.innerHTML =
                "✅ 정답입니다!<br>" +
                "<span style='font-size:17px;'>잘 말했어요: " + currentItem.word + "</span>";

            resultBox.style.background = "#ecfdf5";
            resultBox.style.borderColor = "#bbf7d0";
            resultBox.style.color = "#166534";

            speak(currentItem.word);

            setTimeout(function() {
                goNextCard();
            }, 900);
        } else {
            resultBox.innerHTML =
                "🍊 다시 말해 보세요.<br>" +
                "<span style='font-size:17px;'>한국말 뜻을 보고 영어 단어 또는 표현을 말하면 됩니다.</span>";

            resultBox.style.background = "#fff7ed";
            resultBox.style.borderColor = "#fed7aa";
            resultBox.style.color = "#9a3412";
        }
    }

    function startRecognition() {
        if (!SpeechRecognition) {
            resultBox.innerText = "이 브라우저에서는 음성 인식을 사용할 수 없습니다. Chrome에서 실행해 보세요.";
            resultBox.style.background = "#fef2f2";
            resultBox.style.borderColor = "#fecaca";
            resultBox.style.color = "#991b1b";
            return;
        }

        if (finished) return;

        window.speechSynthesis.cancel();

        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = false;
        recognition.continuous = false;
        recognition.maxAlternatives = 3;

        micBtn.innerText = "🎙️ 듣는 중...";
        resultBox.innerText = "말해 보세요.";
        resultBox.style.background = "#eff6ff";
        resultBox.style.borderColor = "#bfdbfe";
        resultBox.style.color = "#1d4ed8";

        recognition.onresult = function(event) {
            let bestTranscript = "";

            for (let i = 0; i < event.results[0].length; i++) {
                const transcript = event.results[0][i].transcript;
                if (i === 0) bestTranscript = transcript;

                if (isCorrectSpeech(transcript, currentItem.word)) {
                    bestTranscript = transcript;
                    break;
                }
            }

            transcriptBox.innerText = bestTranscript;
            checkSpeech(bestTranscript);
        };

        recognition.onerror = function(event) {
            resultBox.innerText = "다시 눌러 주세요.";
            resultBox.style.background = "#fef2f2";
            resultBox.style.borderColor = "#fecaca";
            resultBox.style.color = "#991b1b";
            micBtn.innerText = "🎙️ 말하기";
        };

        recognition.onend = function() {
            micBtn.innerText = "🎙️ 말하기";
        };

        recognition.start();
    }

    function resetCurrentTheme() {
        const list = getFilteredItems();

        list.forEach(item => {
            delete correctMap[getItemKey(item)];
            delete missedMap[getItemKey(item)];
        });

        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    }

    categorySelect.addEventListener("change", function() {
        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    });

    randomBtn.addEventListener("click", function() {
        currentList = shuffleArray(getFilteredItems());
        currentIndex = 0;
        loadQuestion(0);
        updateScore();
    });

    resetBtn.addEventListener("click", resetCurrentTheme);
    finishRetryBtn.addEventListener("click", resetCurrentTheme);

    micBtn.addEventListener("click", startRecognition);

    answerBtn.addEventListener("click", function() {
        if (!currentItem) return;
        answerBox.style.display = "block";
        answerBox.innerText = "정답: " + currentItem.word;
        speak(currentItem.word);
    });

    skipBtn.addEventListener("click", function() {
        if (currentItem && !correctMap[getItemKey(currentItem)]) {
            missedMap[getItemKey(currentItem)] = true;
            updateScore();
        }
        goNextCard();
    });

    initCategories();
    currentList = getFilteredItems();
    loadQuestion(0);
    updateScore();
    </script>
    """

    html = html.replace("__ITEMS_JSON__", items_json)
    components.html(html, height=800, scrolling=True)


daily_word_card_speaking_game(WORD_THEMES)
