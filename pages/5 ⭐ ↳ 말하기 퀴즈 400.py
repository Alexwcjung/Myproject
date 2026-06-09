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

            #cardBox {
                position: relative;
                overflow: hidden;
                transform-origin: center center;
                will-change: transform, opacity, filter;
            }

            /* 다음 단어로 넘어갈 때 카드 위에 표시되는 반짝 전환 효과 */
            #cardBox::before {
                content: "다음 단어";
                position: absolute;
                top: 18px;
                left: 50%;
                transform: translateX(-50%) translateY(-16px) scale(0.88);
                background: linear-gradient(135deg, #2563eb, #7c3aed);
                color: white;
                border: 3px solid rgba(255,255,255,0.92);
                border-radius: 999px;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: 900;
                letter-spacing: -0.2px;
                box-shadow: 0 12px 26px rgba(37,99,235,0.24);
                opacity: 0;
                z-index: 8;
                pointer-events: none;
                white-space: nowrap;
            }

            #cardBox::after {
                content: "";
                position: absolute;
                inset: 0;
                pointer-events: none;
                background: linear-gradient(90deg,
                    rgba(219,234,254,0) 0%,
                    rgba(219,234,254,0.88) 34%,
                    rgba(237,233,254,0.92) 50%,
                    rgba(254,243,199,0.88) 66%,
                    rgba(219,234,254,0) 100%);
                transform: translateX(-115%);
                opacity: 0;
                z-index: 7;
            }

            .next-card-animate {
                animation: nextCardSlide 0.58s cubic-bezier(.2,.8,.2,1);
            }

            .next-card-animate::before {
                animation: nextBadgePop 0.58s cubic-bezier(.2,.8,.2,1);
            }

            .next-card-animate::after {
                animation: nextLightSweep 0.58s ease-out;
            }

            @keyframes nextCardSlide {
                0% {
                    opacity: 0;
                    transform: translateX(46px) scale(0.965);
                    filter: blur(3px) brightness(1.05);
                }
                55% {
                    opacity: 1;
                    transform: translateX(-7px) scale(1.012);
                    filter: blur(0) brightness(1.03);
                }
                100% {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                    filter: blur(0) brightness(1);
                }
            }

            @keyframes nextBadgePop {
                0% {
                    opacity: 0;
                    transform: translateX(-50%) translateY(-18px) scale(0.86);
                }
                20% {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0) scale(1.04);
                }
                62% {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0) scale(1);
                }
                100% {
                    opacity: 0;
                    transform: translateX(-50%) translateY(-8px) scale(0.96);
                }
            }

            @keyframes nextLightSweep {
                0% {
                    opacity: 0;
                    transform: translateX(-115%);
                }
                20% {
                    opacity: 1;
                }
                100% {
                    opacity: 0;
                    transform: translateX(115%);
                }
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
            <label style="font-weight:900; color:#334155;">단어 범위 선택</label>
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
            ">🎲 이 범위 섞기</button>

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
            <div style="display:flex; justify-content:flex-end; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <div id="scoreLabel" style="
                    display:inline-block;
                    background:#f0fdf4;
                    color:#166534;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1px solid #bbf7d0;
                ">정답 0 / 0 · 연습 필요 단어 0</div>
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
                " id="meaningLangBadge">한국어 뜻</div>

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

                <div id="hintBox" style="
                    display:none;
                    background:#fff7ed;
                    border:1.5px solid #fed7aa;
                    color:#9a3412;
                    border-radius:20px;
                    padding:14px 16px;
                    font-size:30px;
                    font-weight:900;
                    margin-top:14px;
                    word-break:break-word;
                ">hint</div>

                <div id="cardFeedbackBox" style="
                    display:none;
                    background:#ecfdf5;
                    border:1.5px solid #bbf7d0;
                    color:#166534;
                    border-radius:20px;
                    padding:14px 16px;
                    font-size:28px;
                    font-weight:900;
                    margin-top:14px;
                    word-break:break-word;
                ">✅ 정답입니다!</div>
            </div>

            <div id="buttonBox" style="margin-bottom:16px;">
                <div style="display:grid; grid-template-columns:1fr; gap:8px; margin-bottom:8px;">
                    <button id="micBtn" style="
                        width:100%;
                        border:1.5px solid #fecaca;
                        background:#fff1f2;
                        color:#be123c;
                        border-radius:999px;
                        padding:15px 20px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:18px;
                    ">🎙️ 말하기</button>
                </div>

                <div style="
                    background:#f8fafc;
                    border:1.5px solid #e2e8f0;
                    border-radius:18px;
                    padding:12px 14px;
                    margin-bottom:8px;
                    min-height:54px;
                ">
                    <div style="font-size:13px; color:#64748b; font-weight:900; margin-bottom:5px;">인식된 단어</div>
                    <div id="transcriptBox" style="font-size:22px; font-weight:900; color:#334155; word-break:break-word;"></div>
                </div>

                <div id="smallButtonRow" style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px;">
                    <button id="hintBtn" style="
                        border:1.5px solid #fed7aa;
                        background:#fff7ed;
                        color:#9a3412;
                        border-radius:999px;
                        padding:10px 5px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:13px;
                        white-space:nowrap;
                    ">💡 힌트</button>

                    <button id="answerBtn" style="
                        border:1.5px solid #bfdbfe;
                        background:#eff6ff;
                        color:#1d4ed8;
                        border-radius:999px;
                        padding:10px 5px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:13px;
                        white-space:nowrap;
                    ">정답+🔊</button>

                    <button id="skipBtn" style="
                        border:1.5px solid #c7d2fe;
                        background:#eef2ff;
                        color:#3730a3;
                        border-radius:999px;
                        padding:10px 5px;
                        font-weight:900;
                        cursor:pointer;
                        font-size:13px;
                        white-space:nowrap;
                    ">다음 ➡️</button>
                </div>
            </div>

            <div id="resultBox" style="
                display:none;
                background:#f1f5f9;
                border:1.5px solid #e2e8f0;
                border-radius:18px;
                padding:10px 12px;
                font-size:16px;
                font-weight:900;
                color:#334155;
            ">
                마이크 버튼을 누르고 영어 단어를 말해 보세요. 발음 시험이 아니라 단어를 아는지 확인하는 활동입니다.
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
            ">범위 완료!</div>
            <div id="finishScore" style="
                font-size:24px;
                font-weight:900;
                color:#166534;
                margin-bottom:18px;
            ">정답 0 / 0 · 연습 필요 단어 0</div>
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

    const scoreLabel = document.getElementById("scoreLabel");
    const cardBox = document.getElementById("cardBox");
    const emojiBox = document.getElementById("emojiBox");
    const meaningBox = document.getElementById("meaningBox");
    const meaningLangBadge = document.getElementById("meaningLangBadge");
    const answerBox = document.getElementById("answerBox");
    const hintBox = document.getElementById("hintBox");
    const cardFeedbackBox = document.getElementById("cardFeedbackBox");

    const micBtn = document.getElementById("micBtn");
    const answerBtn = document.getElementById("answerBtn");
    const hintBtn = document.getElementById("hintBtn");
    const skipBtn = document.getElementById("skipBtn");

    const transcriptBox = document.getElementById("transcriptBox");
    const resultBox = document.getElementById("resultBox");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;
    let micSafetyTimer = null;
    let recognitionRunId = 0;

    function resetMicButton() {
        isListening = false;

        if (micSafetyTimer) {
            clearTimeout(micSafetyTimer);
            micSafetyTimer = null;
        }

        micBtn.disabled = false;
        micBtn.style.opacity = "1";
        micBtn.style.cursor = "pointer";
        micBtn.innerText = "🎙️ 말하기";
    }

    function cleanupRecognition() {
        recognitionRunId += 1;

        if (micSafetyTimer) {
            clearTimeout(micSafetyTimer);
            micSafetyTimer = null;
        }

        if (recognition) {
            try { recognition.onresult = null; } catch (e) {}
            try { recognition.onerror = null; } catch (e) {}
            try { recognition.onend = null; } catch (e) {}
            try { recognition.abort(); } catch (e) {}
            try { recognition.stop(); } catch (e) {}
            recognition = null;
        }

        resetMicButton();
    }

    function uniqueCategories() {
        const ranges = [];
        const chunkSize = 50;

        for (let start = 0; start < ITEMS.length; start += chunkSize) {
            const end = Math.min(start + chunkSize, ITEMS.length);
            ranges.push((start + 1) + "~" + end);
        }

        return ranges;
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
        const chunkSize = 50;

        if (!selected || selected.indexOf("~") === -1) {
            return ITEMS.slice(0, chunkSize);
        }

        const parts = selected.split("~");
        const start = parseInt(parts[0], 10) - 1;
        const end = parseInt(parts[1], 10);

        return ITEMS.slice(start, end);
    }

    function getItemKey(item) {
        return item.cat + "||" + item.meaning + "||" + item.word;
    }

    function escapeHtml(text) {
        return String(text || "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
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
            .replace(/\bi'm\b/g, "i am")
            .replace(/\bim\b/g, "i am")
            .replace(/\byou're\b/g, "you are")
            .replace(/\bhe's\b/g, "he is")
            .replace(/\bshe's\b/g, "she is")
            .replace(/\bit's\b/g, "it is")
            .replace(/\bwe're\b/g, "we are")
            .replace(/\bthey're\b/g, "they are")
            .replace(/\bdon't\b/g, "do not")
            .replace(/\bdoesn't\b/g, "do not")
            .replace(/\bdidn't\b/g, "do not")
            .replace(/\bcan't\b/g, "cannot")
            .replace(/\bcant\b/g, "cannot")
            .replace(/\bi'll\b/g, "i will")
            .replace(/\byou'll\b/g, "you will")
            .replace(/\bhe'll\b/g, "he will")
            .replace(/\bshe'll\b/g, "she will")
            .replace(/\bp\.?e\.?\b/g, "pe")
            .replace(/\bphysical education\b/g, "pe")
            .replace(/\bt shirt\b/g, "tshirt")
            .replace(/\btee shirt\b/g, "tshirt")
            .replace(/\bwi fi\b/g, "wifi")
            .replace(/\bwi-fi\b/g, "wifi")
            .replace(/\bwifi\b/g, "wifi")
            .replace(/\bok\b/g, "okay")
            .replace(/\bo k\b/g, "okay")
            .replace(/[.,!?;:'"’‘“”]/g, "")
            .replace(/-/g, " ")
            .replace(/\s+/g, " ")
            .trim();
    }

    const KNOWN_ANSWER_WORDS = ITEMS.map(item =>
        normalizeText(item.word).replace(/\s+/g, "")
    );

    function wordsOnly(text) {
        return normalizeText(text)
            .split(" ")
            .filter(function(w) {
                return w.length > 0;
            });
    }

    function editDistance(a, b) {
        a = String(a || "");
        b = String(b || "");

        const dp = [];
        for (let i = 0; i <= a.length; i++) {
            dp[i] = [];
            for (let j = 0; j <= b.length; j++) {
                dp[i][j] = 0;
            }
        }

        for (let i = 0; i <= a.length; i++) dp[i][0] = i;
        for (let j = 0; j <= b.length; j++) dp[0][j] = j;

        for (let i = 1; i <= a.length; i++) {
            for (let j = 1; j <= b.length; j++) {
                const cost = a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1;
                dp[i][j] = Math.min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost
                );
            }
        }

        return dp[a.length][b.length];
    }

    function wordSimilarity(a, b) {
        a = String(a || "");
        b = String(b || "");

        if (!a || !b) return 0;
        if (a === b) return 1;

        const dist = editDistance(a, b);
        const maxLen = Math.max(a.length, b.length);
        return 1 - (dist / maxLen);
    }

    function soundKey(text) {
        return normalizeText(text)
            .replace(/[^a-z]/g, "")
            .replace(/tion/g, "shun")
            .replace(/sion/g, "shun")
            .replace(/th/g, "d")
            .replace(/ph/g, "f")
            .replace(/gh/g, "g")
            .replace(/ck/g, "k")
            .replace(/qu/g, "kw")
            .replace(/x/g, "ks")
            .replace(/c/g, "k")
            .replace(/q/g, "k")
            .replace(/z/g, "s")
            .replace(/v/g, "b")
            .replace(/f/g, "p")
            .replace(/r/g, "l")
            .replace(/j/g, "g")
            .replace(/w/g, "u")
            .replace(/ee/g, "i")
            .replace(/ea/g, "i")
            .replace(/ie/g, "i")
            .replace(/ei/g, "i")
            .replace(/oo/g, "u")
            .replace(/ou/g, "u")
            .replace(/ow/g, "o")
            .replace(/oa/g, "o")
            .replace(/ai/g, "e")
            .replace(/ay/g, "e")
            .replace(/[aeiouy]/g, "")
            .replace(/(.)\1+/g, "$1");
    }

    function vowelLooseKey(text) {
        return normalizeText(text)
            .replace(/[^a-z]/g, "")
            .replace(/ee/g, "i")
            .replace(/ea/g, "i")
            .replace(/ie/g, "i")
            .replace(/ei/g, "i")
            .replace(/oo/g, "u")
            .replace(/ou/g, "u")
            .replace(/ow/g, "o")
            .replace(/oa/g, "o")
            .replace(/ai/g, "e")
            .replace(/ay/g, "e")
            .replace(/[aeiouy]+/g, "v")
            .replace(/(.)\1+/g, "$1");
    }

    function aliasMatch(spokenWord, answerWord) {
        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        const aliases = {
            "i": ["i", "eye", "hi", "ai", "a"],
            "you": ["you", "u", "yew", "yo", "ya", "your"],
            "he": ["he", "hi", "hey"],
            "she": ["she", "see", "sea", "shi", "seat"],
            "we": ["we", "wee", "wi", "me", "be"],
            "they": ["they", "day", "dey", "the", "there", "their", "that"],
            "one": ["one", "won"],
            "two": ["two", "to", "too"],
            "three": ["three", "tree", "free"],
            "four": ["four", "for"],
            "five": ["five", "fife"],
            "six": ["six", "sex", "sick"],
            "eight": ["eight", "ate"],
            "here": ["here", "hear"],
            "there": ["there", "their"],
            "right": ["right", "write", "light"],
            "wait": ["wait", "weight"],
            "know": ["know", "no"],
            "okay": ["okay", "ok", "kay"],
            "pe": ["pe", "pee", "p", "physicaleducation"],
            "wifi": ["wifi", "wi", "wifei"],
            "tshirt": ["tshirt", "teeshirt", "t shirt", "tee shirt"],
            "math": ["math", "mat", "mass", "meth", "matt"],
            "art": ["art", "heart", "at"],
            "science": ["science", "sience", "signs"],
            "history": ["history", "his story", "hisstory"],
            "music": ["music", "musick"]
        };

        if (!aliases[aw]) return false;
        return aliases[aw].includes(sw);
    }

    function clearlyWrongPronoun(spokenWord, answerWord) {
        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");
        const pronouns = ["i", "you", "he", "she", "we", "they"];

        if (!pronouns.includes(aw)) return false;
        if (!pronouns.includes(sw)) return false;

        return sw !== aw;
    }

    function soundOverlap(a, b) {
        const ka = soundKey(a);
        const kb = soundKey(b);

        if (!ka || !kb) return 0;
        if (ka === kb) return 1;

        let overlap = 0;
        for (let i = 0; i < ka.length; i++) {
            if (kb.indexOf(ka.charAt(i)) !== -1) overlap += 1;
        }

        return overlap / Math.max(1, Math.min(ka.length, kb.length));
    }

    function hasSharedBigram(a, b) {
        a = String(a || "");
        b = String(b || "");
        if (a.length < 2 || b.length < 2) return false;

        for (let i = 0; i < a.length - 1; i++) {
            if (b.includes(a.slice(i, i + 2))) return true;
        }
        return false;
    }

    function isClearlyDifferentKnownWord(sw, aw) {
        if (typeof KNOWN_ANSWER_WORDS === "undefined") return false;
        if (!KNOWN_ANSWER_WORDS.includes(sw)) return false;
        if (sw === aw) return false;
        if (aliasMatch(sw, aw)) return false;

        const sim = wordSimilarity(sw, aw);
        const soundSim = wordSimilarity(soundKey(sw), soundKey(aw));
        const vowelSim = wordSimilarity(vowelLooseKey(sw), vowelLooseKey(aw));

        const sameFirst = sw.charAt(0) === aw.charAt(0);
        const sameLast = sw.charAt(sw.length - 1) === aw.charAt(aw.length - 1);
        const sameFirstTwo = sw.slice(0, 2) === aw.slice(0, 2);
        const sameLastTwo = sw.slice(-2) === aw.slice(-2);

        // Daily English 400 안의 다른 단어라도 ASR 오인식 가능성이 있으면 막지 않습니다.
        // 예: art→heart, math→mass, clothes→close, weather→whether 등
        // 다만 assignment→project, subject→music처럼 완전히 다른 단어는 오답 처리합니다.
        const hasClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            hasSharedBigram(sw, aw) ||
            sim >= 0.38 ||
            soundSim >= 0.28 ||
            vowelSim >= 0.30;

        return !hasClue;
    }

    function isSmallRecognitionMistake(spokenWord, answerWord) {
        if (!spokenWord || !answerWord) return false;

        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        if (!sw || !aw) return false;
        if (sw === aw) return true;
        if (aliasMatch(sw, aw)) return true;

        // I / you / he / she / we / they처럼 의미가 크게 바뀌는 대명사는 alias가 아니면 통과시키지 않습니다.
        const pronouns = ["i", "you", "he", "she", "we", "they"];
        if (pronouns.includes(aw) && pronouns.includes(sw) && aw !== sw) {
            return false;
        }

        // 단어 목록 안의 완전히 다른 단어를 말한 경우는 오답
        if (isClearlyDifferentKnownWord(sw, aw)) {
            return false;
        }

        const dist = editDistance(sw, aw);
        const sim = wordSimilarity(sw, aw);

        const soundSw = soundKey(sw);
        const soundAw = soundKey(aw);
        const soundDist = editDistance(soundSw, soundAw);
        const soundSim = wordSimilarity(soundSw, soundAw);

        const vowelSw = vowelLooseKey(sw);
        const vowelAw = vowelLooseKey(aw);
        const vowelSim = wordSimilarity(vowelSw, vowelAw);

        const sameFirst = sw.charAt(0) === aw.charAt(0);
        const sameLast = sw.charAt(sw.length - 1) === aw.charAt(aw.length - 1);
        const sameFirstTwo = sw.slice(0, 2) === aw.slice(0, 2);
        const sameFirstThree = sw.slice(0, 3) === aw.slice(0, 3);
        const sameLastTwo = sw.slice(-2) === aw.slice(-2);

        const soundSameFirst =
            soundSw && soundAw && soundSw.charAt(0) === soundAw.charAt(0);

        const soundSameLast =
            soundSw && soundAw &&
            soundSw.charAt(soundSw.length - 1) === soundAw.charAt(soundAw.length - 1);

        const overlap = soundOverlap(sw, aw);

        // 완전히 다른 단어 방지용 최소 단서
        const hasAnyClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            soundSameFirst ||
            soundSameLast ||
            hasSharedBigram(sw, aw) ||
            soundSim >= 0.22 ||
            vowelSim >= 0.25 ||
            sim >= 0.28 ||
            overlap >= 0.28;

        if (!hasAnyClue) return false;

        // 한 단어 인식에서 브라우저가 일부만 잡거나 붙여 잡는 경우 허용
        // 예: refrigerator → refriger, cafeteria → cafe, comfortable → comfort
        if (aw.length >= 4 && sw.length >= 2 && (aw.includes(sw) || sw.includes(aw))) {
            return true;
        }

        // 자음 뼈대가 같거나 거의 같으면 단어를 안 것으로 처리
        if (soundSw && soundAw && soundSw === soundAw) return true;
        if (soundSw && soundAw && soundDist <= 2 && soundSim >= 0.22) return true;

        // 1~2글자 단어: P.E. 같은 짧은 단어도 관대하게
        if (aw.length <= 2) {
            return (
                sim >= 0.50 ||
                soundSim >= 0.28 ||
                sameFirst ||
                sameLast ||
                soundSameFirst ||
                soundSameLast
            );
        }

        // 3~4글자 단어: 특히 관대하게
        // art, club, copy, fill, roof, yard, sofa, song 등 한 단어 ASR이 흔들림
        if (aw.length <= 4) {
            return (
                dist <= 2 ||
                sim >= 0.30 ||
                soundSim >= 0.20 ||
                vowelSim >= 0.24 ||
                sameFirst ||
                sameLast ||
                soundSameFirst ||
                soundSameLast ||
                hasSharedBigram(sw, aw)
            );
        }

        // 5~6글자 단어: 3~4글자 차이까지 허용
        if (aw.length <= 6) {
            return (
                dist <= 4 ||
                sim >= 0.32 ||
                soundSim >= 0.22 ||
                vowelSim >= 0.25 ||
                sameFirst ||
                sameFirstTwo ||
                sameLast ||
                sameLastTwo ||
                hasSharedBigram(sw, aw)
            );
        }

        // 7글자 이상 긴 단어: 일부 음절만 맞아도 단어를 안 것으로 처리
        return (
            dist <= 6 ||
            sim >= 0.28 ||
            soundSim >= 0.20 ||
            vowelSim >= 0.22 ||
            sameFirst ||
            sameFirstTwo ||
            sameFirstThree ||
            sameLast ||
            sameLastTwo ||
            hasSharedBigram(sw, aw)
        );
    }

    function hasKoreanText(text) {
        return /[가-힣ㄱ-ㅎㅏ-ㅣ]/.test(String(text || ""));
    }

    function hasEnglishText(text) {
        return /[a-zA-Z]/.test(String(text || ""));
    }

    function koreanPronunciationAliasMatch(spoken, answer) {
        const raw = String(spoken || "").replace(/\s+/g, "").toLowerCase();
        const aw = normalizeText(answer).replace(/\s+/g, "");

        const aliases = {
            "subject": ["서브젝트"],
            "math": ["매스", "메스"],
            "science": ["사이언스"],
            "history": ["히스토리"],
            "music": ["뮤직"],
            "art": ["아트"],
            "pe": ["피이", "피"],
            "club": ["클럽"],
            "schedule": ["스케줄"],
            "semester": ["세메스터", "시메스터"],
            "assignment": ["어사인먼트", "어싸인먼트"],
            "project": ["프로젝트"],
            "presentation": ["프레젠테이션", "프리젠테이션"],
            "report": ["리포트", "레포트"],
            "textbook": ["텍스트북"],
            "workbook": ["워크북"],
            "library": ["라이브러리"],
            "cafeteria": ["카페테리아"],
            "hallway": ["홀웨이"],
            "attendance": ["어텐던스", "어텐댄스"],
            "copy": ["카피"],
            "repeat": ["리핏", "리피트"],
            "underline": ["언더라인"],
            "circle": ["서클"],
            "choose": ["추즈", "츄즈"],
            "check": ["체크"],
            "match": ["매치"],
            "complete": ["컴플리트"],
            "fill": ["필"],
            "spell": ["스펠"],
            "pronounce": ["프로나운스"],
            "review": ["리뷰"],
            "explain": ["익스플레인"],
            "describe": ["디스크라이브"],
            "compare": ["컴페어"],
            "discuss": ["디스커스"],
            "present": ["프레젠트", "프리젠트"],
            "livingroom": ["리빙룸"],
            "bedroom": ["베드룸"],
            "kitchen": ["키친"],
            "balcony": ["발코니"],
            "floor": ["플로어"],
            "wall": ["월"],
            "roof": ["루프"],
            "garden": ["가든"],
            "yard": ["야드"],
            "sofa": ["소파"],
            "television": ["텔레비전"],
            "refrigerator": ["리프리저레이터", "레프리저레이터"],
            "microwave": ["마이크로웨이브"],
            "blanket": ["블랭킷", "블랭켓"],
            "pillow": ["필로우"],
            "towel": ["타월"],
            "soap": ["솝", "소프"],
            "mirror": ["미러"],
            "closet": ["클로젯"],
            "trash": ["트래시"],
            "routine": ["루틴"],
            "wakeup": ["웨이크업"],
            "getup": ["겟업"],
            "brush": ["브러시", "브러쉬"],
            "shower": ["샤워"],
            "dress": ["드레스"],
            "leave": ["리브"],
            "arrive": ["어라이브"],
            "return": ["리턴"],
            "finish": ["피니시", "피니쉬"],
            "relax": ["릴랙스"],
            "weekday": ["위크데이"],
            "weekend": ["위켄드", "위크엔드"],
            "usually": ["유주얼리", "유쥬얼리"],
            "often": ["오픈", "오프튼"],
            "sometimes": ["섬타임즈"],
            "always": ["올웨이즈"],
            "never": ["네버"],
            "habit": ["해빗"],
            "lifestyle": ["라이프스타일"],
            "hobby": ["하비"],
            "movie": ["무비"],
            "drama": ["드라마"],
            "song": ["송"],
            "concert": ["콘서트"],
            "dance": ["댄스"],
            "drawing": ["드로잉"],
            "painting": ["페인팅"],
            "comic": ["코믹"],
            "novel": ["노블", "노벨"],
            "photography": ["포토그래피"],
            "cooking": ["쿠킹"],
            "baking": ["베이킹"],
            "camping": ["캠핑"],
            "hiking": ["하이킹"],
            "fishing": ["피싱", "피슁"],
            "freetime": ["프리타임"],
            "favorite": ["페이버릿", "페이보릿"],
            "popular": ["파퓰러", "파퓰라"],
            "relaxing": ["릴랙싱"],
            "soccer": ["사커"],
            "baseball": ["베이스볼"],
            "basketball": ["배스킷볼", "바스켓볼"],
            "volleyball": ["발리볼", "볼리볼"],
            "tennis": ["테니스"],
            "badminton": ["배드민턴"],
            "swimming": ["스위밍"],
            "cycling": ["사이클링"],
            "skating": ["스케이팅"],
            "boxing": ["복싱"],
            "taekwondo": ["태권도", "타이퀀도"],
            "yoga": ["요가"],
            "fitness": ["피트니스"],
            "field": ["필드"],
            "court": ["코트"],
            "stadium": ["스타디움"],
            "coach": ["코치"],
            "competition": ["컴피티션"],
            "medal": ["메달"],
            "season": ["시즌"],
            "spring": ["스프링"],
            "summer": ["서머", "썸머"],
            "fall": ["폴"],
            "winter": ["윈터"],
            "cloudy": ["클라우디"],
            "rainy": ["레이니"],
            "snowy": ["스노위"],
            "windy": ["윈디"],
            "stormy": ["스토미"],
            "foggy": ["포기"],
            "dry": ["드라이"],
            "wet": ["웻"],
            "humid": ["휴미드"],
            "temperature": ["템퍼러처", "템퍼처"],
            "degree": ["디그리"],
            "forecast": ["포캐스트", "포어캐스트"],
            "umbrella": ["엄브렐라"],
            "raincoat": ["레인코트"],
            "rainbow": ["레인보우"],
            "nature": ["네이처"],
            "environment": ["인바이런먼트"],
            "plant": ["플랜트"],
            "forest": ["포레스트"],
            "lake": ["레이크"],
            "ocean": ["오션"],
            "island": ["아일랜드"],
            "desert": ["데저트"],
            "farm": ["팜"],
            "village": ["빌리지"],
            "leaf": ["리프"],
            "root": ["루트"],
            "stone": ["스톤"],
            "sand": ["샌드"],
            "soil": ["소일"],
            "plastic": ["플라스틱"],
            "recycle": ["리사이클"],
            "protect": ["프로텍트"],
            "pollution": ["폴루션"],
            "restaurant": ["레스토랑"],
            "menu": ["메뉴"],
            "seat": ["시트"],
            "waiter": ["웨이터"],
            "waitress": ["웨이트리스"],
            "order": ["오더"],
            "dish": ["디시", "디쉬"],
            "meal": ["밀"],
            "soup": ["수프", "숩"],
            "salad": ["샐러드"],
            "steak": ["스테이크"],
            "pizza": ["피자"],
            "pasta": ["파스타"],
            "burger": ["버거"],
            "sandwich": ["샌드위치"],
            "dessert": ["디저트"],
            "spicy": ["스파이시"],
            "sweet": ["스윗"],
            "bill": ["빌"],
            "receipt": ["리시트", "리십트"],
            "shop": ["샵"],
            "market": ["마켓"],
            "mall": ["몰"],
            "supermarket": ["슈퍼마켓"],
            "cashier": ["캐셔"],
            "customer": ["커스터머"],
            "price": ["프라이스"],
            "sale": ["세일"],
            "discount": ["디스카운트"],
            "coupon": ["쿠폰"],
            "change": ["체인지"],
            "coin": ["코인"],
            "expensive": ["익스펜시브"],
            "cheap": ["칩", "치프"],
            "size": ["사이즈"],
            "color": ["컬러"],
            "brand": ["브랜드"],
            "exchange": ["익스체인지"],
            "refund": ["리펀드"],
            "tshirt": ["티셔츠"],
            "pants": ["팬츠"],
            "jeans": ["진스"],
            "shorts": ["쇼츠"],
            "skirt": ["스커트"],
            "jacket": ["재킷", "자켓"],
            "coat": ["코트"],
            "sweater": ["스웨터"],
            "hoodie": ["후디"],
            "uniform": ["유니폼"],
            "socks": ["삭스"],
            "sneakers": ["스니커즈"],
            "boots": ["부츠"],
            "sandals": ["샌들"],
            "scarf": ["스카프"],
            "gloves": ["글러브스"],
            "belt": ["벨트"],
            "glasses": ["글래시즈", "글래스"],
            "comfortable": ["컴포터블"],
            "busstop": ["버스스탑"],
            "subway": ["서브웨이"],
            "airport": ["에어포트"],
            "terminal": ["터미널"],
            "platform": ["플랫폼"],
            "route": ["루트"],
            "direction": ["디렉션"],
            "straight": ["스트레이트"],
            "corner": ["코너"],
            "block": ["블록"],
            "traffic": ["트래픽"],
            "crosswalk": ["크로스워크"],
            "sidewalk": ["사이드워크"],
            "bridge": ["브릿지", "브리지"],
            "tunnel": ["터널"],
            "entrance": ["엔트런스"],
            "exit": ["엑싯"],
            "transfer": ["트랜스퍼"],
            "lost": ["로스트"],
            "guide": ["가이드"],
            "travel": ["트래블"],
            "trip": ["트립"],
            "vacation": ["베케이션"],
            "tourist": ["투어리스트"],
            "passport": ["패스포트"],
            "flight": ["플라이트"],
            "hotel": ["호텔"],
            "motel": ["모텔"],
            "hostel": ["호스텔"],
            "reservation": ["레저베이션", "리저베이션"],
            "checkin": ["체크인"],
            "checkout": ["체크아웃"],
            "luggage": ["러기지"],
            "suitcase": ["수트케이스"],
            "backpack": ["백팩"],
            "souvenir": ["수비니어", "수베니어"],
            "museum": ["뮤지엄"],
            "famous": ["페이머스"],
            "local": ["로컬"],
            "friendship": ["프렌드십"],
            "bestfriend": ["베스트프렌드"],
            "teammate": ["팀메이트"],
            "partner": ["파트너"],
            "message": ["메시지", "메세지"],
            "call": ["콜"],
            "chat": ["챗"],
            "invite": ["인바이트"],
            "visit": ["비짓"],
            "meet": ["밋"],
            "hangout": ["행아웃"],
            "laugh": ["래프"],
            "share": ["쉐어", "셰어"],
            "trust": ["트러스트"],
            "promise": ["프로미스"],
            "secret": ["시크릿"],
            "joke": ["조크"],
            "together": ["투게더"],
            "alone": ["얼론"],
            "forgive": ["포기브"],
            "excited": ["익사이티드"],
            "nervous": ["너버스"],
            "bored": ["보어드"],
            "surprised": ["서프라이즈드"],
            "confused": ["컨퓨즈드"],
            "embarrassed": ["임배러스트"],
            "proud": ["프라우드"],
            "disappointed": ["디서포인티드"],
            "lonely": ["론리"],
            "calm": ["캄"],
            "upset": ["업셋"],
            "interested": ["인터레스티드"],
            "satisfied": ["새티스파이드"],
            "thankful": ["땡크풀", "탱크풀"],
            "hopeful": ["호프풀"],
            "mood": ["무드"],
            "stress": ["스트레스"],
            "confidence": ["컨피던스"],
            "courage": ["커리지"],
            "think": ["띵크", "싱크"],
            "believe": ["빌리브"],
            "guess": ["게스"],
            "remember": ["리멤버"],
            "forget": ["포겟"],
            "mean": ["민"],
            "agree": ["어그리"],
            "disagree": ["디스어그리"],
            "opinion": ["어피니언", "오피니언"],
            "idea": ["아이디어"],
            "reason": ["리즌"],
            "example": ["이그잼플", "익잼플"],
            "fact": ["팩트"],
            "choice": ["초이스"],
            "decision": ["디시전"],
            "advice": ["어드바이스"],
            "suggestion": ["서제스천"],
            "possible": ["파서블"],
            "impossible": ["임파서블"],
            "confusing": ["컨퓨징"],
            "plan": ["플랜"],
            "appointment": ["어포인트먼트"],
            "meeting": ["미팅"],
            "date": ["데이트"],
            "event": ["이벤트"],
            "party": ["파티"],
            "festival": ["페스티벌"],
            "deadline": ["데드라인"],
            "calendar": ["캘린더"],
            "nextweek": ["넥스트위크"],
            "join": ["조인"],
            "prepare": ["프리페어"],
            "decide": ["디사이드"],
            "cancel": ["캔슬"],
            "ontime": ["온타임"],
            "available": ["어베일러블"],
            "reminder": ["리마인더"],
            "health": ["헬스"],
            "body": ["바디"],
            "eye": ["아이"],
            "ear": ["이어"],
            "nose": ["노즈"],
            "mouth": ["마우스"],
            "tooth": ["투스"],
            "hand": ["핸드"],
            "arm": ["암"],
            "leg": ["레그"],
            "foot": ["풋"],
            "stomach": ["스토먹", "스터먹"],
            "back": ["백"],
            "heart": ["하트"],
            "clinic": ["클리닉"],
            "vitamin": ["비타민"],
            "diet": ["다이어트"],
            "cough": ["코프", "커프"],
            "flu": ["플루"],
            "breathe": ["브리드"],
            "smartphone": ["스마트폰"],
            "screen": ["스크린"],
            "app": ["앱"],
            "website": ["웹사이트"],
            "internet": ["인터넷"],
            "wifi": ["와이파이"],
            "password": ["패스워드"],
            "text": ["텍스트"],
            "videocall": ["비디오콜"],
            "gallery": ["갤러리"],
            "news": ["뉴스"],
            "channel": ["채널"],
            "post": ["포스트"],
            "comment": ["코멘트", "커멘트"],
            "upload": ["업로드"],
            "download": ["다운로드"],
            "search": ["서치"],
            "click": ["클릭"],
            "battery": ["배터리"],
            "notification": ["노티피케이션"],
            "job": ["잡"],
            "work": ["워크"],
            "company": ["컴퍼니"],
            "office": ["오피스"],
            "factory": ["팩토리"],
            "engineer": ["엔지니어"],
            "mechanic": ["메카닉"],
            "chef": ["셰프", "쉐프"],
            "firefighter": ["파이어파이터"],
            "farmer": ["파머"],
            "designer": ["디자이너"],
            "singer": ["싱어"],
            "actor": ["액터"],
            "athlete": ["애슬리트"],
            "dream": ["드림"],
            "future": ["퓨처"],
            "goal": ["골"],
            "skill": ["스킬"],
            "interview": ["인터뷰"],
            "experience": ["익스피리언스"]
        };

        if (!aliases[aw]) return false;
        return aliases[aw].includes(raw);
    }

    function isMostlyKoreanMeaningAnswer(spoken, answer) {
        const raw = String(spoken || "").trim();
        if (!hasKoreanText(raw)) return false;

        // 영어 알파벳이 같이 잡힌 경우에는 기존 관대한 발음 판정을 유지합니다.
        // 예: "water 워터", "school 스쿨"처럼 섞여 들어온 경우
        if (hasEnglishText(raw)) return false;

        // 순수 한글이어도 영어 발음을 한글로 적은 경우는 허용합니다.
        // 예: math→매스, water→워터, school→스쿨
        if (koreanPronunciationAliasMatch(raw, answer)) return false;

        // 그 외 순수 한국어는 한국어 뜻을 말한 것으로 보고 오답 처리합니다.
        // 예: math 문제에서 "수학", water 문제에서 "물"
        return true;
    }

    function isCorrectSpeech(spoken, answer) {
        // 한국어 뜻을 그대로 말하는 경우는 오답 처리합니다.
        // 단, 브라우저가 영어 발음을 한글로 잡은 경우는 위 예외 목록으로 허용합니다.
        if (isMostlyKoreanMeaningAnswer(spoken, answer)) return false;
        if (!hasEnglishText(String(spoken || "")) && !koreanPronunciationAliasMatch(spoken, answer)) return false;
        if (koreanPronunciationAliasMatch(spoken, answer)) return true;

        const s = normalizeText(spoken);
        const a = normalizeText(answer);

        if (!s || !a) return false;
        if (s === a) return true;

        const spokenWords = wordsOnly(s);
        const answerWords = wordsOnly(a);

        if (spokenWords.length === 0 || answerWords.length === 0) return false;

        // 한 단어 정답:
        // 발음 시험이 아니라 단어를 아는지 보는 활동이므로 매우 관대하게 처리합니다.
        if (answerWords.length === 1) {
            const target = answerWords[0];

            // 전체 인식 문장이 바로 비슷하면 정답
            // 예: "a subject", "the subject", "subject please"
            if (isSmallRecognitionMistake(s, target)) return true;

            // 후보 단어 중 하나라도 정답과 비슷하면 정답
            for (const sw of spokenWords) {
                if (isSmallRecognitionMistake(sw, target)) {
                    return true;
                }
            }

            // 브라우저가 한 단어를 붙여서 인식한 경우
            const joinedSpoken = spokenWords.join("");
            if (isSmallRecognitionMistake(joinedSpoken, target)) return true;

            // 앞뒤 filler 제거 후 다시 확인
            const fillerRemoved = spokenWords.filter(w =>
                !["a", "an", "the", "uh", "um", "please", "yes", "no", "is", "it"].includes(w)
            );

            if (fillerRemoved.length > 0) {
                const joinedClean = fillerRemoved.join("");
                if (isSmallRecognitionMistake(joinedClean, target)) return true;

                for (const w of fillerRemoved) {
                    if (isSmallRecognitionMistake(w, target)) return true;
                }
            }

            return false;
        }

        // 두 단어 이상 표현:
        if (s.includes(a)) return true;

        // check in / take notes / living room처럼 띄어쓰기 차이 허용
        const joinedSpoken = spokenWords.join("");
        const joinedAnswer = answerWords.join("");
        if (isSmallRecognitionMistake(joinedSpoken, joinedAnswer)) return true;

        // 순서대로 핵심 단어가 비슷하게 잡히면 정답
        let pos = 0;

        for (const sw of spokenWords) {
            const target = answerWords[pos];
            if (!target) break;

            if (isSmallRecognitionMistake(sw, target)) {
                pos += 1;
            }

            if (pos >= answerWords.length) break;
        }

        return pos >= answerWords.length;
    }

    function countCorrectInCurrentRange() {
        const list = getFilteredItems();
        let count = 0;

        list.forEach(item => {
            if (correctMap[getItemKey(item)]) count += 1;
        });

        return count;
    }

    function countMissedInCurrentRange() {
        const list = getFilteredItems();
        let count = 0;

        list.forEach(item => {
            if (missedMap[getItemKey(item)]) count += 1;
        });

        return count;
    }

    function updateScore() {
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentRange();
        const missedCount = countMissedInCurrentRange();
        scoreLabel.innerText = "정답 " + correctCount + " / " + list.length + " · 연습 필요 단어 " + missedCount;
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
        cleanupRecognition();
        finished = true;
        const list = getFilteredItems();
        const correctCount = countCorrectInCurrentRange();
        const missedCount = countMissedInCurrentRange();

        finishScore.innerText = "정답 " + correctCount + " / " + list.length + " · 연습 필요 단어 " + missedCount;

        gameArea.style.display = "none";
        finishBox.style.display = "block";
    }

    function getCurrentMeaning(item) {
        return item.meaning || "";
    }

    function updateMeaningLanguageBadge() {
        if (!meaningLangBadge) return;
        meaningLangBadge.innerText = "한국어 뜻";
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
        cleanupRecognition();

        currentIndex = index;
        currentItem = currentList[currentIndex];

        emojiBox.innerText = currentItem.emoji || "🌱";
        updateMeaningLanguageBadge();
        meaningBox.innerText = getCurrentMeaning(currentItem);

        answerBox.style.display = "none";
        answerBox.innerText = "정답: " + currentItem.word;

        hintBox.style.display = "none";
        hintBox.innerText = "";

        cardFeedbackBox.style.display = "none";
        cardFeedbackBox.innerText = "";

        transcriptBox.innerText = "";
        transcriptBox.style.color = "#334155";
        resultBox.innerText = "마이크 버튼을 누르고 영어 단어를 말해 보세요. 발음 시험이 아니라 단어를 아는지 확인하는 활동입니다.";
        resultBox.style.background = "#f1f5f9";
        resultBox.style.borderColor = "#e2e8f0";
        resultBox.style.color = "#334155";

        cardBox.classList.remove("next-card-animate");
        void cardBox.offsetWidth;
        cardBox.classList.add("next-card-animate");

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

            // 맞았을 때는 음성 인식 결과 대신
            // 정확한 정답 영어 단어를 인식된 단어 칸에 보여 줍니다.
            // 예: subject ✅ 정답입니다
            cardFeedbackBox.style.display = "none";
            transcriptBox.innerHTML =
                "<span style='color:#334155;'>" + escapeHtml(currentItem.word) + "</span>" +
                " <span style='display:inline-block; margin-left:8px; padding:4px 9px; border-radius:999px; background:#dcfce7; color:#166534; border:1px solid #bbf7d0; font-size:0.82em; font-weight:900; vertical-align:middle;'>✅ 정답입니다</span>";
            transcriptBox.style.color = "#334155";

            resultBox.innerText = "";
            resultBox.style.background = "#f8fafc";
            resultBox.style.borderColor = "#e2e8f0";
            resultBox.style.color = "#334155";

            speak(currentItem.word);

            // 정답을 맞혀도 자동으로 넘어가지 않습니다.
            // 정답 개수만 올라가고, 학생이 직접 '다음' 버튼을 눌러 이동합니다.
            cleanupRecognition();
            resultBox.style.display = "none";
            resultBox.innerText = "";
        } else {
            // 틀렸을 때는 인식된 단어는 그대로 두고,
            // 아래 안내만 짧게 보여 줍니다.
            cardFeedbackBox.style.display = "none";
            transcriptBox.style.color = "#334155";
            resultBox.innerText = "다시 말해 보세요.";
            resultBox.style.background = "#fff7ed";
            resultBox.style.borderColor = "#fed7aa";
            resultBox.style.color = "#9a3412";
        }
    }

    async function startRecognition() {
        if (!SpeechRecognition) {
            resultBox.innerText = "이 브라우저에서는 음성 인식을 사용할 수 없습니다. Chrome에서 실행해 보세요.";
            resultBox.style.background = "#fef2f2";
            resultBox.style.borderColor = "#fecaca";
            resultBox.style.color = "#991b1b";
            resetMicButton();
            return;
        }

        if (finished || !currentItem) {
            resetMicButton();
            return;
        }

        // 이미 듣는 중이면 이전 인식을 정리하고 새로 시작합니다.
        // 몇 문제 뒤 버튼이 멈추는 현상을 막기 위한 안전장치입니다.
        cleanupRecognition();

        // 모바일 브라우저에서 마이크 권한이 꼬이는 경우를 줄입니다.
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                stream.getTracks().forEach(function(track) { track.stop(); });
            } catch (err) {
                resultBox.innerText = "마이크 권한을 허용한 뒤 다시 눌러 주세요.";
                resultBox.style.background = "#fef2f2";
                resultBox.style.borderColor = "#fecaca";
                resultBox.style.color = "#991b1b";
                resetMicButton();
                return;
            }
        }

        window.speechSynthesis.cancel();

        recognitionRunId += 1;
        const thisRunId = recognitionRunId;

        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = false;
        recognition.continuous = false;
        recognition.maxAlternatives = 10;

        isListening = true;
        micBtn.disabled = true;
        micBtn.style.opacity = "0.72";
        micBtn.style.cursor = "wait";
        micBtn.innerText = "🎙️ 듣는 중...";

        resultBox.innerText = "말해 보세요.";
        resultBox.style.background = "#eff6ff";
        resultBox.style.borderColor = "#bfdbfe";
        resultBox.style.color = "#1d4ed8";

        recognition.onresult = function(event) {
            if (thisRunId !== recognitionRunId) return;
            let bestTranscript = "";

            if (!event.results || !event.results[0]) {
                resetMicButton();
                return;
            }

            for (let i = 0; i < event.results[0].length; i++) {
                const transcript = event.results[0][i].transcript.trim();
                if (i === 0) bestTranscript = transcript;

                if (isCorrectSpeech(transcript, currentItem.word)) {
                    bestTranscript = transcript;
                    break;
                }
            }

            // 인식된 단어는 아까처럼 한꺼번에 보여 줍니다.
            transcriptBox.style.color = "#334155";
            transcriptBox.innerText = bestTranscript;
            checkSpeech(bestTranscript);
        };

        recognition.onerror = function(event) {
            if (thisRunId !== recognitionRunId) return;
            if (event.error === "not-allowed" || event.error === "service-not-allowed") {
                resultBox.innerText = "마이크 권한을 허용해 주세요.";
                resultBox.style.background = "#fef2f2";
                resultBox.style.borderColor = "#fecaca";
                resultBox.style.color = "#991b1b";
            } else if (event.error === "no-speech") {
                resultBox.innerText = "소리가 인식되지 않았습니다. 다시 눌러 주세요.";
                resultBox.style.background = "#f8fafc";
                resultBox.style.borderColor = "#e2e8f0";
                resultBox.style.color = "#334155";
            } else {
                resultBox.innerText = "다시 눌러 주세요.";
                resultBox.style.background = "#f8fafc";
                resultBox.style.borderColor = "#e2e8f0";
                resultBox.style.color = "#334155";
            }

            resetMicButton();
        };

        recognition.onend = function() {
            if (thisRunId !== recognitionRunId) return;
            recognition = null;
            resetMicButton();
        };

        // 혹시 브라우저가 onend를 늦게 주거나 누락해도 버튼을 살립니다.
        setTimeout(function() {
            if (isListening) {
                resetMicButton();
            }
        }, 9000);

        micSafetyTimer = setTimeout(function() {
            if (thisRunId !== recognitionRunId) return;
            if (isListening) {
                try { recognition.abort(); } catch (e) {}
                try { recognition.stop(); } catch (e) {}
                recognition = null;
                resetMicButton();
            }
        }, 11000);

        try {
            recognition.start();
        } catch (err) {
            resultBox.innerText = "다시 눌러 주세요.";
            resultBox.style.background = "#f8fafc";
            resultBox.style.borderColor = "#e2e8f0";
            resultBox.style.color = "#334155";
            cleanupRecognition();
        }
    }

    function resetCurrentRange() {
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

    resetBtn.addEventListener("click", resetCurrentRange);
    finishRetryBtn.addEventListener("click", resetCurrentRange);

    micBtn.addEventListener("click", startRecognition);

    answerBtn.addEventListener("click", function() {
        if (!currentItem) return;
        answerBox.style.display = "block";
        answerBox.innerText = "정답: " + currentItem.word;
        speak(currentItem.word);
    });

    hintBtn.addEventListener("click", function() {
        if (!currentItem) return;

        const cleanWord = String(currentItem.word || "").trim();
        const words = cleanWord.split(/\s+/).filter(Boolean);

        const hintText = words.map(function(word) {
            const lettersOnly = word.replace(/[^a-zA-Z]/g, "");
            if (lettersOnly.length <= 2) return word;

            const firstTwo = lettersOnly.slice(0, 2);
            const blanks = "_".repeat(Math.max(1, lettersOnly.length - 2));

            return firstTwo + blanks;
        }).join(" ");

        hintBox.style.display = "block";
        hintBox.innerText = "힌트: " + hintText;
    });

    skipBtn.addEventListener("click", function() {
        cleanupRecognition();
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
