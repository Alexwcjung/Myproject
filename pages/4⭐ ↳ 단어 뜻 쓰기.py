import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="단어 뜻 터뜨리기 게임",
    page_icon="💥",
    layout="wide"
)

st.title("💥 Survival English 단어 뜻 터뜨리기 게임")
st.caption("생존단어 160개를 바탕으로, 한 판에서 같은 영어 단어가 한 번만 나오도록 만든 단어 뜻 쓰기 게임입니다.")

# -----------------------------
# 단어 + 한국어 뜻 목록
# -----------------------------
word_data = [
    {
        "word": "I",
        "meanings": [
            "나"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "you",
        "meanings": [
            "너, 당신",
            "너",
            "당신"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "he",
        "meanings": [
            "그"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "she",
        "meanings": [
            "그녀"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "we",
        "meanings": [
            "우리"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "they",
        "meanings": [
            "그들"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "friend",
        "meanings": [
            "친구"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "teacher",
        "meanings": [
            "선생님"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "student",
        "meanings": [
            "학생"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "classmate",
        "meanings": [
            "반 친구"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "family",
        "meanings": [
            "가족"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "father",
        "meanings": [
            "아버지"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "mother",
        "meanings": [
            "어머니"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "brother",
        "meanings": [
            "형제, 남자 형제",
            "형제",
            "남자 형제"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "sister",
        "meanings": [
            "자매, 여자 형제",
            "자매",
            "여자 형제"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "name",
        "meanings": [
            "이름"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "person",
        "meanings": [
            "사람"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "man",
        "meanings": [
            "남자"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "woman",
        "meanings": [
            "여자"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "child",
        "meanings": [
            "아이"
        ],
        "theme": "🧍 나와 사람"
    },
    {
        "word": "go",
        "meanings": [
            "가다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "come",
        "meanings": [
            "오다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "walk",
        "meanings": [
            "걷다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "run",
        "meanings": [
            "달리다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "sit",
        "meanings": [
            "앉다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "stand",
        "meanings": [
            "서다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "stop",
        "meanings": [
            "멈추다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "start",
        "meanings": [
            "시작하다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "open",
        "meanings": [
            "열다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "close",
        "meanings": [
            "닫다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "eat",
        "meanings": [
            "먹다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "drink",
        "meanings": [
            "마시다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "sleep",
        "meanings": [
            "자다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "study",
        "meanings": [
            "공부하다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "read",
        "meanings": [
            "읽다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "write",
        "meanings": [
            "쓰다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "listen",
        "meanings": [
            "듣다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "speak",
        "meanings": [
            "말하다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "help",
        "meanings": [
            "돕다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "wait",
        "meanings": [
            "기다리다"
        ],
        "theme": "🏃 기본 동작"
    },
    {
        "word": "happy",
        "meanings": [
            "행복한"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "sad",
        "meanings": [
            "슬픈"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "angry",
        "meanings": [
            "화난"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "tired",
        "meanings": [
            "피곤한"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "hungry",
        "meanings": [
            "배고픈"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "thirsty",
        "meanings": [
            "목마른"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "sick",
        "meanings": [
            "아픈"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "okay",
        "meanings": [
            "괜찮은"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "fine",
        "meanings": [
            "괜찮은"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "cold",
        "meanings": [
            "추운, 차가운",
            "추운",
            "차가운"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "hot",
        "meanings": [
            "더운, 뜨거운",
            "더운",
            "뜨거운"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "pain",
        "meanings": [
            "통증"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "headache",
        "meanings": [
            "두통"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "stomachache",
        "meanings": [
            "복통"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "fever",
        "meanings": [
            "열"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "hurt",
        "meanings": [
            "아프다, 다치다",
            "아프다",
            "다치다"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "good",
        "meanings": [
            "좋은"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "bad",
        "meanings": [
            "나쁜"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "worried",
        "meanings": [
            "걱정하는"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "scared",
        "meanings": [
            "무서워하는"
        ],
        "theme": "💖 감정·몸 상태"
    },
    {
        "word": "food",
        "meanings": [
            "음식"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "water",
        "meanings": [
            "물"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "rice",
        "meanings": [
            "밥, 쌀",
            "밥",
            "쌀"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "bread",
        "meanings": [
            "빵"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "milk",
        "meanings": [
            "우유"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "juice",
        "meanings": [
            "주스"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "coffee",
        "meanings": [
            "커피"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "tea",
        "meanings": [
            "차"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "apple",
        "meanings": [
            "사과"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "banana",
        "meanings": [
            "바나나"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "egg",
        "meanings": [
            "달걀"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "meat",
        "meanings": [
            "고기"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "chicken",
        "meanings": [
            "닭고기, 닭",
            "닭고기",
            "닭"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "fish",
        "meanings": [
            "생선, 물고기",
            "생선",
            "물고기"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "breakfast",
        "meanings": [
            "아침 식사"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "lunch",
        "meanings": [
            "점심 식사"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "dinner",
        "meanings": [
            "저녁 식사"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "snack",
        "meanings": [
            "간식"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "medicine",
        "meanings": [
            "약"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "hospital",
        "meanings": [
            "병원"
        ],
        "theme": "🍎 음식·물"
    },
    {
        "word": "home",
        "meanings": [
            "집"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "school",
        "meanings": [
            "학교"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "classroom",
        "meanings": [
            "교실"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "bathroom",
        "meanings": [
            "화장실"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "hospital",
        "meanings": [
            "병원"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "store",
        "meanings": [
            "가게"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "station",
        "meanings": [
            "역"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "bus",
        "meanings": [
            "버스"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "car",
        "meanings": [
            "자동차"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "taxi",
        "meanings": [
            "택시"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "train",
        "meanings": [
            "기차"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "bike",
        "meanings": [
            "자전거"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "road",
        "meanings": [
            "도로"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "street",
        "meanings": [
            "거리"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "here",
        "meanings": [
            "여기"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "there",
        "meanings": [
            "거기"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "near",
        "meanings": [
            "가까운"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "far",
        "meanings": [
            "먼"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "left",
        "meanings": [
            "왼쪽"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "right",
        "meanings": [
            "오른쪽, 맞는",
            "오른쪽",
            "맞는"
        ],
        "theme": "🚗 장소·이동"
    },
    {
        "word": "time",
        "meanings": [
            "시간"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "now",
        "meanings": [
            "지금"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "today",
        "meanings": [
            "오늘"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "tomorrow",
        "meanings": [
            "내일"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "yesterday",
        "meanings": [
            "어제"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "morning",
        "meanings": [
            "아침"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "afternoon",
        "meanings": [
            "오후"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "evening",
        "meanings": [
            "저녁"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "night",
        "meanings": [
            "밤"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "nine",
        "meanings": [
            "아홉"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "late",
        "meanings": [
            "늦은"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "one",
        "meanings": [
            "하나"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "two",
        "meanings": [
            "둘"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "three",
        "meanings": [
            "셋"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "four",
        "meanings": [
            "넷"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "five",
        "meanings": [
            "다섯"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "six",
        "meanings": [
            "여섯"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "seven",
        "meanings": [
            "일곱"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "eight",
        "meanings": [
            "여덟"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "ten",
        "meanings": [
            "열"
        ],
        "theme": "⏰ 시간·숫자"
    },
    {
        "word": "bag",
        "meanings": [
            "가방"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "phone",
        "meanings": [
            "전화기"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "book",
        "meanings": [
            "책"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "notebook",
        "meanings": [
            "공책"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "pen",
        "meanings": [
            "펜"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "pencil",
        "meanings": [
            "연필"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "desk",
        "meanings": [
            "책상"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "chair",
        "meanings": [
            "의자"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "door",
        "meanings": [
            "문"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "window",
        "meanings": [
            "창문"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "key",
        "meanings": [
            "열쇠"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "money",
        "meanings": [
            "돈"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "card",
        "meanings": [
            "카드"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "ticket",
        "meanings": [
            "표, 티켓",
            "표",
            "티켓"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "clothes",
        "meanings": [
            "옷"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "shoes",
        "meanings": [
            "신발"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "hat",
        "meanings": [
            "모자"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "watch",
        "meanings": [
            "시계"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "cup",
        "meanings": [
            "컵"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "bottle",
        "meanings": [
            "병"
        ],
        "theme": "🎒 물건·돈"
    },
    {
        "word": "help",
        "meanings": [
            "도움, 돕다",
            "도움",
            "돕다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "please",
        "meanings": [
            "부디, 제발",
            "부디",
            "제발"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "sorry",
        "meanings": [
            "미안합니다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "excuse me",
        "meanings": [
            "실례합니다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "again",
        "meanings": [
            "다시"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "slowly",
        "meanings": [
            "천천히"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "understand",
        "meanings": [
            "이해하다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "question",
        "meanings": [
            "질문"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "problem",
        "meanings": [
            "문제"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "need",
        "meanings": [
            "필요하다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "want",
        "meanings": [
            "원하다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "know",
        "meanings": [
            "알다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "say",
        "meanings": [
            "말하다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "tell",
        "meanings": [
            "말하다, 알려주다",
            "말하다",
            "알려주다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "ask",
        "meanings": [
            "묻다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "answer",
        "meanings": [
            "대답, 답",
            "대답",
            "답"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "repeat",
        "meanings": [
            "반복하다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "speak",
        "meanings": [
            "말하다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "look",
        "meanings": [
            "보다"
        ],
        "theme": "🆘 도움 요청"
    },
    {
        "word": "listen",
        "meanings": [
            "듣다"
        ],
        "theme": "🆘 도움 요청"
    }
]

# -----------------------------
# 조절 옵션
# -----------------------------
speed = st.slider(
    "🚀 떨어지는 속도",
    min_value=1,
    max_value=10,
    value=3,
    help="숫자가 클수록 단어가 더 빠르게 떨어집니다."
)

word_count = st.slider(
    "📚 사용할 단어 개수",
    min_value=5,
    max_value=len(word_data),
    value=30,
    help="생존단어 160개 목록에서 앞에서부터 선택합니다. 게임에서는 같은 영어 단어가 한 번만 나옵니다."
)

batch_count = st.slider(
    "🌧️ 한 번에 떨어지는 단어 개수",
    min_value=1,
    max_value=5,
    value=1
)

spawn_interval = st.slider(
    "⏳ 단어 나오는 간격",
    min_value=800,
    max_value=3500,
    value=2000,
    step=100,
    help="숫자가 클수록 단어가 더 천천히 나옵니다."
)

time_limit_options = {
    "30초": 30,
    "1분": 60,
    "1분 30초": 90,
    "2분": 120,
    "2분 30초": 150,
    "3분": 180,
    "3분 30초": 210,
    "4분": 240,
}

time_limit_label = st.selectbox(
    "⏱️ 시간 제한",
    list(time_limit_options.keys()),
    index=1
)

time_limit_seconds = time_limit_options[time_limit_label]

show_hint = st.checkbox(
    "💡 뜻 힌트 보기",
    value=False
)

selected_words = word_data[:word_count]

# 선택된 단어 수와 실제 고유 영어 단어 수 안내
unique_word_count = len({item["word"].lower() for item in selected_words})
st.info(f"선택된 생존단어 항목: {len(selected_words)}개 | 실제 게임에서 한 번만 나오는 고유 영어 단어: {unique_word_count}개")

word_data_js = json.dumps(selected_words, ensure_ascii=False)
show_hint_js = "true" if show_hint else "false"
time_limit_js = time_limit_seconds

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
    body {{
        margin: 0;
        overflow: hidden;
        font-family: Arial, sans-serif;
        background: linear-gradient(180deg, #dff7ff, #fff7d6);
    }}

    #gameArea {{
        position: relative;
        width: 100%;
        height: 660px;
        overflow: hidden;
        border-radius: 28px;
        background: linear-gradient(180deg, #aeefff 0%, #fff4bd 100%);
        border: 5px solid white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}

    .word {{
        position: absolute;
        top: -80px;
        padding: 14px 24px;
        font-size: 30px;
        font-weight: bold;
        color: #333;
        background: white;
        border-radius: 999px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.18);
        transition: transform 0.2s, opacity 0.2s;
        white-space: nowrap;
        border: 3px solid #ffd6ea;
        z-index: 5;
    }}

    .pop {{
        animation: pop 0.35s forwards;
    }}

    @keyframes pop {{
        0% {{
            transform: scale(1);
            opacity: 1;
        }}
        50% {{
            transform: scale(1.8) rotate(10deg);
            opacity: 0.8;
        }}
        100% {{
            transform: scale(0);
            opacity: 0;
        }}
    }}

    #status {{
        position: absolute;
        top: 78px;
        left: 20px;
        z-index: 20;
        background: rgba(255,255,255,0.94);
        padding: 12px 18px;
        border-radius: 20px;
        font-size: 19px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        max-width: 55%;
        line-height: 1.4;
    }}

    #scoreBox {{
        position: absolute;
        top: 15px;
        left: 20px;
        z-index: 20;
        background: rgba(255,255,255,0.95);
        padding: 12px 18px;
        border-radius: 20px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }}

    #timerBox {{
        position: absolute;
        top: 15px;
        right: 20px;
        z-index: 25;
        background: rgba(255,255,255,0.97);
        padding: 10px 20px;
        border-radius: 24px;
        font-size: 42px;
        font-weight: 900;
        color: #e11d48;
        box-shadow: 0 5px 14px rgba(0,0,0,0.16);
        min-width: 140px;
        text-align: center;
        border: 3px solid #fecdd3;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }}

    #clockIcon {{
        position: relative;
        width: 44px;
        height: 44px;
        border: 4px solid #e11d48;
        border-radius: 50%;
        background: radial-gradient(circle, #fff 0%, #fff7ed 100%);
        box-shadow: inset 0 0 0 3px rgba(254,205,211,0.65);
        flex-shrink: 0;
    }}

    #clockIcon::before {{
        content: "";
        position: absolute;
        width: 4px;
        height: 4px;
        border-radius: 50%;
        background: #e11d48;
        top: 5px;
        left: 50%;
        transform: translateX(-50%);
        box-shadow:
            0 26px 0 #e11d48,
            13px 13px 0 #e11d48,
            -13px 13px 0 #e11d48;
        opacity: 0.75;
    }}

    #clockHour {{
        position: absolute;
        width: 5px;
        height: 14px;
        background: #be123c;
        left: 50%;
        top: 50%;
        transform-origin: bottom center;
        transform: translate(-50%, -100%) rotate(315deg);
        border-radius: 999px;
    }}

    #clockMinute {{
        position: absolute;
        width: 4px;
        height: 18px;
        background: #fb7185;
        left: 50%;
        top: 50%;
        transform-origin: bottom center;
        transform: translate(-50%, -100%) rotate(40deg);
        border-radius: 999px;
    }}

    #clockCenter {{
        position: absolute;
        width: 8px;
        height: 8px;
        background: #e11d48;
        border-radius: 50%;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }}

    #timerBox.time-warning {{
        animation: timerPulse 0.8s infinite alternate;
    }}

    @keyframes timerPulse {{
        from {{
            transform: scale(1);
            box-shadow: 0 5px 14px rgba(0,0,0,0.16);
        }}
        to {{
            transform: scale(1.04);
            box-shadow: 0 8px 24px rgba(225,29,72,0.35);
        }}
    }}

    #endOverlay {{
        display: none;
        position: absolute;
        inset: 0;
        z-index: 100;
        background: rgba(15, 23, 42, 0.75);
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 24px;
        box-sizing: border-box;
    }}

    #endCard {{
        background: white;
        border-radius: 30px;
        padding: 34px 38px;
        max-width: 620px;
        width: 92%;
        box-shadow: 0 12px 35px rgba(0,0,0,0.3);
        border: 5px solid #fde68a;
    }}

    #endTitle {{
        font-size: 44px;
        font-weight: 900;
        color: #ef4444;
        margin-bottom: 16px;
    }}

    #endScore {{
        font-size: 34px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 12px;
    }}

    #endMessage {{
        font-size: 21px;
        font-weight: 800;
        color: #475569;
        line-height: 1.5;
    }}

    #inputPanel {{
        position: absolute;
        bottom: 22px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 30;
        width: 86%;
        background: rgba(255,255,255,0.95);
        border: 3px solid #bfdbfe;
        border-radius: 28px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        box-sizing: border-box;
        text-align: center;
    }}

    #answerInput {{
        width: 68%;
        padding: 14px 18px;
        border-radius: 999px;
        border: 2px solid #93c5fd;
        font-size: 22px;
        font-weight: bold;
        outline: none;
        text-align: center;
    }}

    #answerInput:focus {{
        border-color: #ec4899;
        box-shadow: 0 0 0 4px rgba(236,72,153,0.15);
    }}

    #submitBtn {{
        margin-left: 10px;
        padding: 14px 24px;
        border: none;
        border-radius: 999px;
        font-size: 21px;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #ff7eb3, #ffb86c);
        box-shadow: 0 6px 14px rgba(0,0,0,0.18);
    }}

    #startBtn {{
        margin-left: 10px;
        padding: 14px 24px;
        border: none;
        border-radius: 999px;
        font-size: 21px;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #60a5fa, #34d399);
        box-shadow: 0 6px 14px rgba(0,0,0,0.18);
    }}

    #hintBox {{
        margin-top: 10px;
        font-size: 17px;
        font-weight: bold;
        color: #475569;
        min-height: 24px;
    }}

    .effect {{
        position: absolute;
        font-size: 42px;
        pointer-events: none;
        animation: floatUp 0.7s forwards;
        z-index: 40;
    }}

    @keyframes floatUp {{
        0% {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
        100% {{
            opacity: 0;
            transform: translateY(-60px) scale(1.5);
        }}
    }}

    @media (max-width: 700px) {{
        #gameArea {{
            height: 620px;
            border-radius: 22px;
        }}

        .word {{
            font-size: 24px;
            padding: 11px 18px;
        }}

        #status {{
            font-size: 15px;
            max-width: 62%;
            padding: 9px 12px;
            top: 62px;
            left: 10px;
        }}

        #scoreBox {{
            font-size: 15px;
            padding: 9px 12px;
            top: 10px;
            left: 10px;
        }}

        #timerBox {{
            font-size: 30px;
            padding: 8px 13px;
            top: 10px;
            right: 10px;
            min-width: 118px;
            gap: 8px;
        }}

        #clockIcon {{
            width: 34px;
            height: 34px;
            border-width: 3px;
        }}

        #clockHour {{
            width: 4px;
            height: 11px;
        }}

        #clockMinute {{
            width: 3px;
            height: 14px;
        }}

        #clockCenter {{
            width: 6px;
            height: 6px;
        }}

        #inputPanel {{
            width: 94%;
            padding: 14px 12px;
            bottom: 14px;
        }}

        #answerInput {{
            width: 58%;
            font-size: 18px;
            padding: 12px 14px;
        }}

        #submitBtn, #startBtn {{
            font-size: 16px;
            padding: 12px 14px;
            margin-left: 4px;
        }}

        #hintBox {{
            font-size: 14px;
        }}
    }}
</style>
</head>

<body>
<div id="gameArea">
    <div id="scoreBox">✅ 점수: <span id="score">0</span></div>
    <div id="timerBox">
        <div id="clockIcon">
            <div id="clockHour"></div>
            <div id="clockMinute"></div>
            <div id="clockCenter"></div>
        </div>
        <span id="timeLeft">{time_limit_js}</span>
    </div>
    <div id="status">🎮 게임 시작을 누르세요</div>

    <div id="endOverlay">
        <div id="endCard">
            <div id="endTitle">⏰ 시간 종료!</div>
            <div id="endScore">정답 개수: <span id="finalScore">0</span>개</div>
            <div id="endMessage">수고했습니다. 다시 하려면 시작 버튼을 다시 누르세요.</div>
        </div>
    </div>

    <div id="inputPanel">
        <input id="answerInput" type="text" placeholder="한국어 뜻 입력 예: 고양이" autocomplete="off">
        <button id="submitBtn">💥 제출</button>
        <button id="startBtn">▶️ 시작</button>
        <div id="hintBox"></div>
    </div>
</div>

<script>
const wordData = {word_data_js};
const showHint = {show_hint_js};
    const timeLimitSeconds = {time_limit_js};

const gameArea = document.getElementById("gameArea");
const statusBox = document.getElementById("status");
const scoreSpan = document.getElementById("score");
const timeLeftSpan = document.getElementById("timeLeft");
const timerBox = document.getElementById("timerBox");
const endOverlay = document.getElementById("endOverlay");
const finalScoreSpan = document.getElementById("finalScore");
const answerInput = document.getElementById("answerInput");
const submitBtn = document.getElementById("submitBtn");
const startBtn = document.getElementById("startBtn");
const hintBox = document.getElementById("hintBox");

let activeWords = [];
let score = 0;
let gameStarted = false;
let gameEnded = false;
let createInterval = null;
let countdownInterval = null;
let remainingSeconds = timeLimitSeconds;
let usedWords = new Set();

// 같은 영어 단어가 한 판에서 다시 나오지 않도록,
// 중복 항목은 의미만 합치고 단어는 하나로 정리합니다.
const uniqueWordMap = new Map();
wordData.forEach(item => {{
    const key = item.word.toLowerCase().trim();
    if (!uniqueWordMap.has(key)) {{
        uniqueWordMap.set(key, {{
            word: item.word,
            meanings: [...item.meanings],
            theme: item.theme || ""
        }});
    }} else {{
        const oldItem = uniqueWordMap.get(key);
        item.meanings.forEach(m => {{
            if (!oldItem.meanings.includes(m)) {{
                oldItem.meanings.push(m);
            }}
        }});
    }}
}});

const uniqueWordData = Array.from(uniqueWordMap.values());

let fallSpeed = {speed};
let batchCount = {batch_count};
let spawnInterval = {spawn_interval};

// 속도 조절: 숫자가 클수록 빠름
let baseSpeed = 0.10 + fallSpeed * 0.06;

// 단어 겹침 방지용 레인
const laneCount = 6;
let laneBusy = Array(laneCount).fill(false);

function updateTimerDisplay() {{
    const safeSeconds = Math.max(remainingSeconds, 0);
    timeLeftSpan.innerText = String(safeSeconds);

    if (safeSeconds <= 10 && gameStarted && !gameEnded) {{
        timerBox.classList.add("time-warning");
    }} else {{
        timerBox.classList.remove("time-warning");
    }}
}}

function playEndSignal() {{
    try {{
        const audio = new Audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg");
        audio.play();
    }} catch (e) {{
        console.log("Audio failed:", e);
    }}
}}

function endGame(messageText = "⏰ 시간이 끝났습니다!") {{
    if (gameEnded) return;

    gameEnded = true;
    gameStarted = false;

    if (createInterval) {{
        clearInterval(createInterval);
        createInterval = null;
    }}

    if (countdownInterval) {{
        clearInterval(countdownInterval);
        countdownInterval = null;
    }}

    activeWords.forEach(item => item.element.remove());
    activeWords = [];

    answerInput.value = "";
    answerInput.disabled = true;
    submitBtn.disabled = true;

    finalScoreSpan.innerText = score;
    statusBox.innerText = messageText + " 정답 개수: " + score + "개";
    endOverlay.style.display = "flex";
    playEndSignal();
}}

function startCountdown() {{
    remainingSeconds = timeLimitSeconds;
    updateTimerDisplay();

    if (countdownInterval) {{
        clearInterval(countdownInterval);
    }}

    countdownInterval = setInterval(() => {{
        if (!gameStarted || gameEnded) return;

        remainingSeconds -= 1;
        updateTimerDisplay();

        if (remainingSeconds <= 0) {{
            endGame("⏰ 시간 종료!");
        }}
    }}, 1000);
}}

function normalizeKorean(text) {{
    return text
        .toLowerCase()
        .replace(/\\s+/g, "")
        .replace(/[.,!?~]/g, "")
        .trim();
}}

function getLaneX(laneIndex) {{
    const areaWidth = gameArea.clientWidth;
    const laneWidth = areaWidth / laneCount;
    const maxOffset = Math.max(5, laneWidth - 120);
    const randomOffset = 6 + Math.random() * maxOffset;
    return laneIndex * laneWidth + randomOffset;
}}

function getFreeLane() {{
    let freeLanes = [];

    for (let i = 0; i < laneCount; i++) {{
        if (!laneBusy[i]) {{
            freeLanes.push(i);
        }}
    }}

    if (freeLanes.length === 0) {{
        return null;
    }}

    return freeLanes[Math.floor(Math.random() * freeLanes.length)];
}}

function createOneWord() {{
    if (!gameStarted || gameEnded) return;

    const activeWordKeys = activeWords.map(item => item.word.toLowerCase().trim());

    const availableWords = uniqueWordData.filter(item => {{
        const key = item.word.toLowerCase().trim();
        return !usedWords.has(key) && !activeWordKeys.includes(key);
    }});

    if (availableWords.length === 0) {{
        if (activeWords.length === 0) {{
            endGame("🎉 모든 단어를 한 번씩 완료했습니다!");
        }}
        return;
    }}

    const lane = getFreeLane();
    if (lane === null) return;

    laneBusy[lane] = true;

    const item = availableWords[Math.floor(Math.random() * availableWords.length)];
    const key = item.word.toLowerCase().trim();
    usedWords.add(key);

    const wordDiv = document.createElement("div");

    wordDiv.className = "word";
    wordDiv.innerText = item.word;
    wordDiv.dataset.word = item.word;
    wordDiv.style.left = getLaneX(lane) + "px";
    wordDiv.style.top = "-80px";

    gameArea.appendChild(wordDiv);

    activeWords.push({{
        element: wordDiv,
        word: item.word,
        meanings: item.meanings,
        y: -80,
        speed: baseSpeed + Math.random() * 0.12,
        lane: lane
    }});

    const remaining = Math.max(0, uniqueWordData.length - usedWords.size);
    statusBox.innerText = "✏️ 뜻을 입력하세요! 남은 새 단어: " + remaining + "개";

    setTimeout(() => {{
        laneBusy[lane] = false;
    }}, 2200);
}}

function createWordsBatch() {{
    if (!gameStarted || gameEnded) return;

    for (let i = 0; i < batchCount; i++) {{
        setTimeout(() => {{
            createOneWord();
        }}, i * 300);
    }}
}}

function moveWords() {{
    for (let i = activeWords.length - 1; i >= 0; i--) {{
        let item = activeWords[i];
        item.y += item.speed;
        item.element.style.top = item.y + "px";

        if (item.y > gameArea.clientHeight - 120) {{
            item.element.remove();
            activeWords.splice(i, 1);
            statusBox.innerText = "⬇️ 지나간 단어: " + item.word + " = " + item.meanings[0];
        }}
    }}

    if (gameStarted && usedWords.size >= uniqueWordData.length && activeWords.length === 0) {{
        endGame("🎉 모든 단어를 한 번씩 완료했습니다!");
    }}

    updateHint();
    requestAnimationFrame(moveWords);
}}

function checkAnswer() {{
    if (!gameStarted || gameEnded) return;

    const rawAnswer = answerInput.value;
    const userAnswer = normalizeKorean(rawAnswer);

    if (!userAnswer) {{
        statusBox.innerText = "✏️ 한국어 뜻을 입력하세요!";
        answerInput.value = "";
        answerInput.focus();
        return;
    }}

    for (let i = activeWords.length - 1; i >= 0; i--) {{
        let item = activeWords[i];

        let correct = item.meanings.some(m => normalizeKorean(m) === userAnswer);

        if (correct) {{
            popWord(item, i);
            answerInput.value = "";
            answerInput.focus();
            return;
        }}
    }}

    statusBox.innerText = "🤔 오답입니다. 다시 도전하세요: " + rawAnswer;
    answerInput.value = "";
    answerInput.focus();
}}

function popWord(item, index) {{
    const rect = item.element.getBoundingClientRect();
    const parentRect = gameArea.getBoundingClientRect();

    showEffect(
        rect.left - parentRect.left,
        rect.top - parentRect.top
    );

    item.element.classList.add("pop");

    setTimeout(() => {{
        if (item.element) item.element.remove();
    }}, 300);

    activeWords.splice(index, 1);
    score++;
    scoreSpan.innerText = score;

    statusBox.innerText = "✅ 정답! " + item.word + " = " + item.meanings[0] + " | 이 단어는 다시 나오지 않습니다.";
}}

function showEffect(x, y) {{
    const effects = ["💥", "✨", "🎉", "⭐", "👏", "🌟"];
    const effect = document.createElement("div");
    effect.className = "effect";
    effect.innerText = effects[Math.floor(Math.random() * effects.length)];
    effect.style.left = x + "px";
    effect.style.top = y + "px";
    gameArea.appendChild(effect);

    setTimeout(() => {{
        effect.remove();
    }}, 700);
}}

function updateHint() {{
    if (!showHint || !gameStarted) {{
        hintBox.innerText = "";
        return;
    }}

    if (activeWords.length === 0) {{
        hintBox.innerText = "";
        return;
    }}

    const sample = activeWords[activeWords.length - 1];
    const firstMeaning = sample.meanings[0];
    hintBox.innerText = "💡 힌트: 화면의 한 단어 뜻은 '" + firstMeaning[0] + "'로 시작합니다.";
}}

function startGame() {{
    if (createInterval) {{
        clearInterval(createInterval);
        createInterval = null;
    }}

    if (countdownInterval) {{
        clearInterval(countdownInterval);
        countdownInterval = null;
    }}

    gameStarted = true;
    gameEnded = false;
    score = 0;
    remainingSeconds = timeLimitSeconds;

    activeWords.forEach(item => item.element.remove());
    activeWords = [];
    usedWords = new Set();
    laneBusy = Array(laneCount).fill(false);

    scoreSpan.innerText = score;
    updateTimerDisplay();
    timerBox.classList.remove("time-warning");
    endOverlay.style.display = "none";

    answerInput.disabled = false;
    submitBtn.disabled = false;
    answerInput.value = "";
    answerInput.focus();

    statusBox.innerText = "✏️ 떨어지는 단어의 한국어 뜻을 입력하세요! 같은 단어는 한 번만 나옵니다.";

    createWordsBatch();
    createInterval = setInterval(createWordsBatch, spawnInterval);
    startCountdown();
}}

submitBtn.addEventListener("click", checkAnswer);

answerInput.addEventListener("keydown", function(event) {{
    if (event.key === "Enter") {{
        checkAnswer();
    }}
}});

startBtn.addEventListener("click", startGame);

updateTimerDisplay();
moveWords();
</script>
</body>
</html>
"""

components.html(html_code, height=730)
