import streamlit as st
from urllib.parse import quote
from pathlib import Path
import requests
import re

st.set_page_config(
    page_title="Speaking Practice",
    page_icon="🎤",
    layout="wide"
)

# =========================
# 기본 함수
# =========================
def make_google_translate_url(text, source="auto", target="en"):
    encoded_text = quote(str(text).strip())
    return f"https://translate.google.com/?sl={source}&tl={target}&text={encoded_text}&op=translate"


def make_google_tts_url(text, lang="en"):
    clean_text = str(text).strip() or "Hello."
    encoded = quote(clean_text)
    return f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang}&q={encoded}"


@st.cache_data(show_spinner=False)
def get_tts_mp3_bytes(text, lang="en"):
    clean_text = str(text).strip() or "Hello."
    url = make_google_tts_url(clean_text, lang=lang)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://translate.google.com/",
    }
    response = requests.get(url, headers=headers, timeout=12)
    response.raise_for_status()
    audio_bytes = response.content
    if not audio_bytes or len(audio_bytes) < 500:
        raise ValueError("음성 파일이 비어 있습니다.")
    return audio_bytes


def english_audio_player(text):
    """화면에 영어 오디오를 바로 표시합니다."""
    text = str(text).strip()
    if not text:
        return
    try:
        audio_bytes = get_tts_mp3_bytes(text, lang="en")
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error("영어 발음 오디오를 만들지 못했습니다.")
        st.caption(f"오류 내용: {e}")
        st.link_button("🔊 새 창에서 듣기", make_google_tts_url(text, lang="en"), use_container_width=True)


# =========================
# 문제 언어: 한국어 / 베트남어 → 영어
# =========================
PROBLEM_TEXT = {
    "ko": {
        "flag": "🇰🇷",
        "label": "한국어 → 영어",
        "intro": "영어 문장을 보고, 듣고, 따라 말해 봅시다.",
        "name_input": "내 이름을 한국어 또는 영어로 써 보세요.",
        "name_placeholder": "예: 정우창, 김민수, Jimin",
        "name_problem": "나는 (성 + 이름)입니다.",
        "hobby_problem_1": "내 취미는 (        )입니다.",
        "hobby_problem_2": "나는 학생이고 키가 큽니다.",
        "hobby_input": "취미를 한국어 또는 베트남어로 입력하면 영어 문장에 바로 반영됩니다.",
        "hobby_placeholder": "예: 축구, 노래 부르기, 게임하기, 음악 듣기, đá bóng, nghe nhạc",
        "hobby_translate": "🌐 구글 번역에서 더 정확한 영어 표현과 발음 확인하기",
        "hobby_empty_info": "취미를 한국어 또는 베트남어로 입력하면 구글 번역으로 연결됩니다.",
        "hobby_en_input": "영어 취미 표현을 확인하거나 수정하세요.",
        "hobby_sentence_problem": "내 취미는 {hobby}입니다. 나는 학생이고 키가 큽니다.",
        "time_problem": "지금 몇 시인가요? 저는 지금 집에 가고 싶습니다.",
        "need_problem": "물을 마시고 싶어요. 음식도 먹고 싶습니다.",
        "picture_timer": "⏱️ 20초 안에 사진을 묘사해 봅시다.",
        "picture_listen": "📢 사진 묘사 전체 듣기",
        "final_success": "영어 문장을 듣고 따라 말하면서 연습해 보세요.",
    },
    "vi": {
        "flag": "🇻🇳",
        "label": "베트남어 → 영어",
        "intro": "Hãy nhìn câu tiếng Anh, nghe và luyện nói theo.",
        "name_input": "Hãy viết tên của em bằng tiếng Việt, tiếng Hàn hoặc tiếng Anh.",
        "name_placeholder": "Ví dụ: Jeong Woochang, Nguyễn Văn An, 정우창",
        "name_problem": "Tôi là (họ + tên).",
        "hobby_problem_1": "Sở thích của tôi là (        ).",
        "hobby_problem_2": "Tôi là học sinh và cao.",
        "hobby_input": "Nhập sở thích bằng tiếng Việt hoặc tiếng Hàn, rồi kiểm tra câu tiếng Anh.",
        "hobby_placeholder": "Ví dụ: đá bóng, nghe nhạc, chơi game, đọc sách, 축구, 음악 듣기",
        "hobby_translate": "🌐 Kiểm tra cách nói tiếng Anh và phát âm bằng Google Dịch",
        "hobby_empty_info": "Nhập sở thích bằng tiếng Việt hoặc tiếng Hàn để mở Google Dịch.",
        "hobby_en_input": "Kiểm tra hoặc sửa cách nói sở thích bằng tiếng Anh.",
        "hobby_sentence_problem": "Sở thích của tôi là {hobby}. Tôi là học sinh và cao.",
        "time_problem": "Bây giờ là mấy giờ? Tôi muốn về nhà bây giờ.",
        "need_problem": "Tôi muốn uống nước. Tôi cũng muốn ăn đồ ăn.",
        "picture_timer": "⏱️ Hãy miêu tả bức tranh trong 20 giây.",
        "picture_listen": "📢 Nghe toàn bộ phần miêu tả tranh",
        "final_success": "Hãy nghe câu tiếng Anh và luyện nói theo.",
    }
}


# =========================
# 한글 이름 간단 로마자 변환
# =========================
CHO = [
    "g", "kk", "n", "d", "tt", "r", "m", "b", "pp", "s",
    "ss", "", "j", "jj", "ch", "k", "t", "p", "h"
]
JUNG = [
    "a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa",
    "wae", "oe", "yo", "u", "wo", "we", "wi", "yu", "eu", "ui", "i"
]
JONG = [
    "", "k", "k", "ks", "n", "nj", "nh", "t", "l", "lk",
    "lm", "lb", "ls", "lt", "lp", "lh", "m", "p", "ps", "t",
    "t", "ng", "t", "t", "k", "t", "p", "t"
]


COMMON_SURNAMES = {
    "김": "Kim", "이": "Lee", "박": "Park", "최": "Choi", "정": "Jeong",
    "강": "Kang", "조": "Cho", "윤": "Yoon", "장": "Jang", "임": "Lim",
    "한": "Han", "오": "Oh", "서": "Seo", "신": "Shin", "권": "Kwon",
    "황": "Hwang", "안": "Ahn", "송": "Song", "전": "Jeon", "홍": "Hong",
    "유": "Yoo", "고": "Ko", "문": "Moon", "양": "Yang", "손": "Son",
    "배": "Bae", "백": "Baek", "허": "Heo", "남": "Nam", "심": "Shim",
    "노": "Noh", "하": "Ha", "곽": "Kwak", "성": "Sung", "차": "Cha",
    "주": "Joo", "우": "Woo", "구": "Koo", "민": "Min", "류": "Ryu",
}

SPECIAL_SYLLABLES = {
    "우": "Woo", "창": "chang", "민": "min", "수": "su", "지": "ji",
    "준": "jun", "영": "young", "현": "hyun", "서": "seo", "연": "yeon",
    "윤": "yoon", "아": "a", "나": "na", "래": "rae", "송": "song", "희": "hee",
}


def romanize_hangul_syllable(ch):
    """한글 한 글자를 간단히 로마자로 바꿉니다."""
    if ch in SPECIAL_SYLLABLES:
        return SPECIAL_SYLLABLES[ch]

    code = ord(ch)
    if 0xAC00 <= code <= 0xD7A3:
        s_index = code - 0xAC00
        cho = s_index // 588
        jung = (s_index % 588) // 28
        jong = s_index % 28
        return CHO[cho] + JUNG[jung] + JONG[jong]
    return ch


def romanize_hangul_name(text):
    """
    이름 입력용 간단 로마자 변환.
    한글 이름은 성 + 이름 순서로 띄어 씁니다.
    예: 정우창 → Jeong Woochang
    """
    text = str(text).strip()
    if not text:
        return "Jeong Woochang"

    # 이미 영어/베트남어 알파벳으로 입력한 경우: 단어 첫 글자만 대문자로 정리
    if not any(0xAC00 <= ord(ch) <= 0xD7A3 for ch in text):
        cleaned = re.sub(r"\s+", " ", text).strip()
        return " ".join(part.capitalize() for part in cleaned.split()) or "Jeong Woochang"

    hangul_chars = [ch for ch in text if 0xAC00 <= ord(ch) <= 0xD7A3]
    if not hangul_chars:
        return "Jeong Woochang"

    last_name = COMMON_SURNAMES.get(hangul_chars[0], romanize_hangul_syllable(hangul_chars[0]).capitalize())
    first_name_raw = "".join(romanize_hangul_syllable(ch) for ch in hangul_chars[1:])
    first_name = first_name_raw.capitalize() if first_name_raw else ""

    if first_name:
        return f"{last_name} {first_name}"
    return last_name


# =========================
# 취미 간단 변환: 한국어/베트남어 → 영어
# =========================
HOBBY_TRANSLATIONS = {
    # Korean
    "축구": "playing soccer",
    "야구": "playing baseball",
    "농구": "playing basketball",
    "배구": "playing volleyball",
    "테니스": "playing tennis",
    "배드민턴": "playing badminton",
    "수영": "swimming",
    "자전거": "riding a bike",
    "자전거 타기": "riding a bike",
    "게임": "playing games",
    "게임하기": "playing games",
    "노래": "singing",
    "노래 부르기": "singing",
    "음악": "listening to music",
    "음악 듣기": "listening to music",
    "영화": "watching movies",
    "영화 보기": "watching movies",
    "드라마": "watching dramas",
    "드라마 보기": "watching dramas",
    "독서": "reading books",
    "책 읽기": "reading books",
    "그림": "drawing",
    "그림 그리기": "drawing",
    "요리": "cooking",
    "요리하기": "cooking",
    "빵 굽기": "baking",
    "캠핑": "camping",
    "하이킹": "hiking",
    "낚시": "fishing",
    "사진": "taking pictures",
    "사진 찍기": "taking pictures",
    "자동차 정비": "fixing cars",
    "정비": "fixing cars",
    "태권도": "doing taekwondo",
    "복싱": "boxing",
    "운동": "exercising",
    "잠자기": "sleeping",
    "춤": "dancing",
    "춤추기": "dancing",

    # Vietnamese
    "đá bóng": "playing soccer",
    "bóng đá": "playing soccer",
    "chơi bóng đá": "playing soccer",
    "bóng rổ": "playing basketball",
    "chơi bóng rổ": "playing basketball",
    "bóng chuyền": "playing volleyball",
    "chơi bóng chuyền": "playing volleyball",
    "cầu lông": "playing badminton",
    "chơi cầu lông": "playing badminton",
    "bơi": "swimming",
    "đạp xe": "riding a bike",
    "chơi game": "playing games",
    "trò chơi": "playing games",
    "hát": "singing",
    "nghe nhạc": "listening to music",
    "xem phim": "watching movies",
    "xem drama": "watching dramas",
    "đọc sách": "reading books",
    "vẽ": "drawing",
    "nấu ăn": "cooking",
    "làm bánh": "baking",
    "cắm trại": "camping",
    "đi bộ đường dài": "hiking",
    "câu cá": "fishing",
    "chụp ảnh": "taking pictures",
    "sửa xe": "fixing cars",
    "taekwondo": "doing taekwondo",
    "quyền anh": "boxing",
    "tập thể dục": "exercising",
    "ngủ": "sleeping",
    "nhảy": "dancing",
}


def guess_hobby_english(input_text):
    """자주 쓰는 취미는 앱 안에서 바로 영어로 보여 주고, 어려운 표현은 구글 번역 확인을 유도합니다."""
    key = str(input_text).strip().lower()
    if not key:
        return ""
    return HOBBY_TRANSLATIONS.get(key, "")


# =========================
# 디자인
# =========================
st.markdown(
    """
    <style>
    .stApp { background-color:#ffffff; }
    .main-title {
        background:linear-gradient(135deg,#ecfeff,#fef3c7,#fce7f3);
        padding:26px;
        border-radius:22px;
        border:1px solid #e5e7eb;
        box-shadow:0 6px 18px rgba(0,0,0,0.06);
        margin-bottom:24px;
    }
    .main-title h1 {
        margin:0;
        font-size:42px;
        font-weight:900;
        color:#111827;
    }
    .main-title p {
        margin:8px 0 0 0;
        font-size:17px;
        font-weight:800;
        color:#475569;
    }
    .sentence-card {
        background:linear-gradient(135deg,#ffffff,#f8fafc);
        border:1px solid #e5e7eb;
        border-radius:18px;
        padding:18px 20px;
        margin:10px 0 10px 0;
        box-shadow:0 3px 10px rgba(0,0,0,0.04);
    }
    .problem-line {
        font-size:17px;
        color:#374151;
        font-weight:800;
        margin-bottom:8px;
        line-height:1.6;
    }
    .en-line {
        font-size:28px;
        color:#111827;
        font-weight:900;
        line-height:1.5;
    }
    .orange-card {
        background:linear-gradient(135deg,#fff7ed,#fffbeb);
        border:1px solid #fed7aa;
        border-radius:18px;
        padding:18px 20px;
        margin:10px 0 12px 0;
        box-shadow:0 3px 10px rgba(0,0,0,0.04);
    }
    </style>
    """,
    unsafe_allow_html=True
)


def sentence_card(problem_sentence, english, flag="🇰🇷"):
    st.markdown(
        f"""
        <div class="sentence-card">
            <div class="problem-line">{flag} {problem_sentence}</div>
            <div class="en-line">{english}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    english_audio_player(english)


# =========================
# 화면 시작
# =========================
st.markdown(
    """
    <div class="main-title">
        <h1>🎤 영어 말하기 수행평가 연습</h1>
        <p>한국어 또는 베트남어 문제를 보고 영어로 말해 봅시다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

problem_choice = st.radio(
    "문제 언어를 선택하세요.",
    ["한국어 → 영어", "베트남어 → 영어"],
    horizontal=True
)

problem_lang = "vi" if problem_choice == "베트남어 → 영어" else "ko"
TXT = PROBLEM_TEXT[problem_lang]
FLAG = TXT["flag"]

st.info(f"현재 선택: **{TXT['label']}**")

st.markdown("---")

# =========================
# 1. 자기소개
# =========================
st.subheader("1. 자기소개하기")

name_input = st.text_input(
    TXT["name_input"],
    placeholder=TXT["name_placeholder"]
)

name_text = str(name_input).strip() if str(name_input).strip() else "정우창"
romanized_name = romanize_hangul_name(name_text)

if name_input.strip() and romanized_name.lower() != name_text.lower():
    st.info(f"영어 이름 표기 예시: **{romanized_name}**")

name_sentence = f"I am {romanized_name}."

sentence_card(
    TXT["name_problem"],
    name_sentence,
    flag=FLAG
)

st.markdown("---")

# =========================
# 2. 내가 좋아하는 것 / 취미 말하기
# =========================
st.subheader("2. 내가 좋아하는 것 말하기")

st.markdown(
    f"""
    <div class="orange-card">
        <div class="problem-line" style="color:#9a3412;">
            {FLAG} {TXT["hobby_problem_1"]}<br>
            {TXT["hobby_problem_2"]}
        </div>
        <div class="en-line">
            My hobby is ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ).<br>
            I am a student and tall.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

hobby_input = st.text_input(
    TXT["hobby_input"],
    placeholder=TXT["hobby_placeholder"]
)

if hobby_input.strip():
    st.link_button(
        TXT["hobby_translate"],
        make_google_translate_url(hobby_input, source="auto", target="en"),
        use_container_width=True
    )
else:
    st.info(TXT["hobby_empty_info"])

auto_hobby_en = guess_hobby_english(hobby_input)

hobby_en_input = st.text_input(
    TXT["hobby_en_input"],
    value=auto_hobby_en,
    placeholder="예: playing soccer, listening to music, playing games"
)

hobby_en = str(hobby_en_input).strip()

if hobby_en:
    hobby_sentence = f"My hobby is {hobby_en}. I am a student and tall."
else:
    hobby_sentence = "My hobby is blank. I am a student and tall."

hobby_problem_word = hobby_input.strip() if hobby_input.strip() else "(취미)"
sentence_card(
    TXT["hobby_sentence_problem"].format(hobby=hobby_problem_word),
    hobby_sentence,
    flag=FLAG
)

st.markdown("---")

# =========================
# 3. 시간 묻기
# =========================
st.subheader("3. 시간 묻기와 하고 싶은 말하기")

sentence_card(
    TXT["time_problem"],
    "What time is it? I want to go home now.",
    flag=FLAG
)

st.markdown("---")

# =========================
# 4. 필요한 것 말하기
# =========================
st.subheader("4. 필요한 것 말하기")

sentence_card(
    TXT["need_problem"],
    "I want water. I want food too.",
    flag=FLAG
)

st.markdown("---")

# =========================
# 5. 사진 묘사하기
# =========================
st.subheader("5. 사진 묘사하기")

image_paths = [
    Path("pages/images/speaking_test.png"),
    Path("pages/images/수행평가 그림.png"),
    Path("images/speaking_test.png"),
    Path("images/수행평가 그림.png"),
]

image_path = None
for p in image_paths:
    if p.exists():
        image_path = p
        break

left_col, center_col, right_col = st.columns([1.2, 1.8, 1.2])

with center_col:
    if image_path:
        st.image(
            str(image_path),
            caption="Describe the picture.",
            use_container_width=True
        )
    else:
        st.warning(
            "사진 파일을 찾을 수 없습니다. "
            "pages/images/speaking_test.png 또는 images/speaking_test.png 로 저장하세요."
        )

st.info(TXT["picture_timer"])

picture_script = (
    "There are many people in the street. "
    "I can see trees and buildings too. "
    "Some people are riding bikes and some are sitting in chairs. "
    "They look happy."
)

st.markdown(f"### {TXT['picture_listen']}")
english_audio_player(picture_script)

st.markdown(
    """
    <div style="
        background:#f8fafc;
        border:1px solid #e5e7eb;
        border-radius:18px;
        padding:18px 20px;
        margin-top:12px;
    ">
        <div style="font-size:25px; font-weight:800; line-height:1.7; color:#111827;">
            There are many people in the street.<br>
            I can see trees and buildings too.<br>
            Some people are riding bikes and some are sitting in chairs.<br>
            They look happy.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.success(TXT["final_success"])
