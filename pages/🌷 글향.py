import streamlit as st
from pathlib import Path
from gtts import gTTS
import io
import base64
import random
import json
import re
import uuid
from urllib.parse import quote
import streamlit.components.v1 as components

# =========================================================
# 기본 설정
# =========================================================
st.set_page_config(
    page_title="Fun English Reading",
    page_icon="🌈",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

# =========================================================
# TTS
# =========================================================
@st.cache_data
def make_tts(text, lang="en"):
    fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def direct_tts_player(text, lang="en"):
    """버튼을 한 번 더 누르지 않고 바로 재생 가능한 TTS 플레이어를 보여줍니다."""
    text = str(text).strip()
    if not text:
        return

    try:
        st.audio(make_tts(text, lang=lang), format="audio/mp3")
    except Exception as e:
        st.error("음성 파일을 만들지 못했습니다. requirements.txt에 gTTS가 있는지 확인해 주세요.")
        st.caption(f"오류 내용: {e}")

# =========================================================
# 서술형 피드백 함수
# =========================================================

def play_persistent_full_audio(text, key, button_label="🎧 전체 듣기", lang="en"):
    """
    전체 듣기:
    - st.audio() 대신 HTML audio 사용
    - 한국어 해석 보기 toggle을 눌러도 재생 위치를 localStorage에 저장/복원
    - rerun 후에도 가능하면 이어서 재생
    """
    audio_state_key = f"{key}_audio_bytes"

    if st.button(button_label, use_container_width=True, key=f"{key}_btn"):
        try:
            audio_bytes = make_tts(text, lang=lang)
            st.session_state[audio_state_key] = audio_bytes
        except Exception as e:
            st.error("음성 파일을 만들지 못했습니다. requirements.txt에 gTTS가 있는지 확인해 주세요.")
            st.caption(f"오류 내용: {e}")

    if audio_state_key in st.session_state:
        audio_bytes = st.session_state[audio_state_key]
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        safe_audio_id = re.sub(r"[^a-zA-Z0-9_]+", "_", str(key))

        components.html(
            f"""
            <audio
                id="audio_{safe_audio_id}"
                controls
                style="width: 100%;"
                src="data:audio/mp3;base64,{audio_b64}">
            </audio>

            <script>
            const audio = document.getElementById("audio_{safe_audio_id}");

            const timeKey = "reading_full_audio_time_{safe_audio_id}";
            const playingKey = "reading_full_audio_playing_{safe_audio_id}";

            const savedTime = localStorage.getItem(timeKey);
            if (savedTime !== null) {{
                audio.currentTime = parseFloat(savedTime);
            }}

            const wasPlaying = localStorage.getItem(playingKey);
            if (wasPlaying === "true") {{
                setTimeout(() => {{
                    audio.play().catch(() => {{
                        // 브라우저 자동재생 정책상 막힐 수 있음
                    }});
                }}, 300);
            }}

            audio.addEventListener("timeupdate", () => {{
                localStorage.setItem(timeKey, audio.currentTime);
            }});

            audio.addEventListener("play", () => {{
                localStorage.setItem(playingKey, "true");
            }});

            audio.addEventListener("pause", () => {{
                localStorage.setItem(playingKey, "false");
                localStorage.setItem(timeKey, audio.currentTime);
            }});

            audio.addEventListener("ended", () => {{
                localStorage.setItem(playingKey, "false");
                localStorage.setItem(timeKey, "0");
            }});

            window.addEventListener("beforeunload", () => {{
                localStorage.setItem(timeKey, audio.currentTime);
                localStorage.setItem(playingKey, !audio.paused);
            }});
            </script>
            """,
            height=95,
        )


# =========================================================
# 서술형 피드백 함수
# =========================================================
def detect_language(text):
    english_count = sum(1 for ch in text if ch.lower() in "abcdefghijklmnopqrstuvwxyz")
    korean_count = sum(1 for ch in text if "가" <= ch <= "힣")
    return "ko" if korean_count > english_count else "en"


def join_ideas(ideas):
    if len(ideas) == 1:
        return ideas[0]
    if len(ideas) == 2:
        return ideas[0] + " and " + ideas[1]
    return ", ".join(ideas[:-1]) + ", and " + ideas[-1]


def make_korean_to_english(text, topic_name):
    ideas = []
    korean_points = []

    if "포기" in text:
        ideas.append("I should not give up easily")
        korean_points.append("쉽게 포기하지 않겠다는 태도가 잘 드러납니다.")
    if "연습" in text or "훈련" in text:
        ideas.append("I should keep practicing step by step")
        korean_points.append("꾸준한 연습의 중요성을 잘 이해했습니다.")
    if "노력" in text or "최선" in text:
        ideas.append("I should do my best even when it is difficult")
        korean_points.append("어려운 상황에서도 최선을 다하려는 마음이 좋습니다.")
    if "믿" in text or "자신감" in text:
        ideas.append("I should believe in myself")
        korean_points.append("자신을 믿는 태도가 핵심 교훈으로 잘 연결됩니다.")
    if "성실" in text or "꾸준" in text:
        ideas.append("I should be hardworking and consistent")
        korean_points.append("성실함과 꾸준함을 배움으로 연결한 점이 좋습니다.")
    if "도전" in text:
        ideas.append("I should challenge myself without fear")
        korean_points.append("도전을 두려워하지 않겠다는 생각이 잘 표현되었습니다.")
    if "꿈" in text or "목표" in text:
        ideas.append("I should work hard for my dream and goal")
        korean_points.append("꿈과 목표를 향한 태도가 분명합니다.")
    if "팀" in text or "협동" in text or "동료" in text:
        ideas.append("I should respect teamwork and my teammates")
        korean_points.append("협동과 존중의 가치를 잘 파악했습니다.")
    if "실수" in text or "실패" in text:
        ideas.append("I should learn from mistakes and failure")
        korean_points.append("실패를 성장의 기회로 바라본 점이 좋습니다.")
    if "창의" in text or "상상" in text:
        ideas.append("I should think creatively and express my ideas")
        korean_points.append("창의성과 표현의 가치를 잘 연결했습니다.")
    if "자연" in text or "여행" in text:
        ideas.append("I should learn from travel and nature")
        korean_points.append("자연과 경험에서 배움을 찾은 점이 좋습니다.")
    if "문화" in text or "역사" in text:
        ideas.append("I should respect culture and history")
        korean_points.append("문화와 역사를 존중하는 태도가 잘 드러납니다.")

    if not ideas:
        ideas = ["I should learn a positive attitude", "I should keep trying in my own life"]
        korean_points = ["핵심 생각은 좋습니다. 다음에는 구체적인 단어를 하나 더 넣으면 더 풍부해집니다.", "예를 들어 노력, 자신감, 도전, 존중 같은 표현을 넣어 보세요."]

    idea_sentence = join_ideas(ideas)
    english_feedback = (
        f"Through {topic_name}, I learned that {idea_sentence}. "
        f"This lesson is meaningful because it reminds me that small actions can change my future. "
        f"I want to remember this lesson, practice it in my daily life, and become a better person."
    )

    korean_feedback = " ".join(korean_points[:3])
    korean_feedback += " 문장을 조금 더 길게 쓰고, 왜 그렇게 생각했는지 이유를 한 문장 더 붙이면 더 좋은 답이 됩니다."

    return korean_feedback, english_feedback


def improve_english_answer(text, topic_name):
    lower_text = text.lower()
    ideas = []
    korean_points = []

    if "give up" in lower_text:
        ideas.append("I should not give up easily")
        korean_points.append("포기하지 않겠다는 핵심 메시지가 잘 보입니다.")
    if "practice" in lower_text or "train" in lower_text:
        ideas.append("I should keep practicing step by step")
        korean_points.append("연습과 성장의 관계를 잘 표현했습니다.")
    if "believe" in lower_text or "confidence" in lower_text:
        ideas.append("I should believe in myself")
        korean_points.append("자신감과 자기 믿음이 잘 드러납니다.")
    if "hard" in lower_text or "hardworking" in lower_text or "effort" in lower_text:
        ideas.append("I should work hard for my goal")
        korean_points.append("노력의 중요성을 잘 연결했습니다.")
    if "best" in lower_text:
        ideas.append("I should do my best even when it is difficult")
        korean_points.append("최선을 다하려는 태도가 좋습니다.")
    if "dream" in lower_text or "goal" in lower_text:
        ideas.append("I should keep working toward my dream")
        korean_points.append("꿈과 목표를 향한 방향이 분명합니다.")
    if "team" in lower_text:
        ideas.append("I should respect teamwork")
        korean_points.append("팀워크의 가치를 잘 파악했습니다.")
    if "mistake" in lower_text or "failure" in lower_text:
        ideas.append("I should learn from mistakes and failure")
        korean_points.append("실패를 배움으로 바꾼 점이 좋습니다.")
    if "creative" in lower_text or "idea" in lower_text:
        ideas.append("I should think creatively and express my ideas")
        korean_points.append("창의적인 표현의 의미를 잘 잡았습니다.")
    if "travel" in lower_text or "nature" in lower_text:
        ideas.append("I should learn from travel and nature")
        korean_points.append("경험과 자연에서 배움을 찾은 점이 좋습니다.")
    if "culture" in lower_text or "history" in lower_text:
        ideas.append("I should respect culture and history")
        korean_points.append("문화와 역사의 가치를 잘 이해했습니다.")

    if not ideas:
        ideas = ["I should have a positive attitude", "I should keep trying"]
        korean_points = ["전체적인 생각은 좋습니다. 다음에는 본문에서 배운 핵심 단어를 한두 개 넣어 보세요."]

    idea_sentence = join_ideas(ideas)
    improved_english = (
        f"Through {topic_name}, I learned that {idea_sentence}. "
        f"This lesson is important because it can help me grow not only in class but also in my daily life. "
        f"I will try to remember this message and use it when I face a difficult moment."
    )

    korean_feedback = " ".join(korean_points[:3])
    korean_feedback += " 영어 문장은 의미가 전달됩니다. 더 자연스럽게 하려면 'because'로 이유를 붙이고, 마지막에 앞으로의 다짐을 한 문장 추가하면 좋습니다."

    return korean_feedback, improved_english

# =========================================================
# 디자인
# =========================================================
st.markdown("""
<style>
/* =====================================================
   Garden Theme: flowers + grass
   ===================================================== */
.stApp {
    background:
        radial-gradient(circle at 8% 12%, rgba(244,114,182,0.18) 0, rgba(244,114,182,0.00) 26%),
        radial-gradient(circle at 92% 10%, rgba(134,239,172,0.22) 0, rgba(134,239,172,0.00) 28%),
        linear-gradient(180deg, #fff7fb 0%, #f7fff4 48%, #ecfdf5 100%);
}

/* 페이지 전체 여백 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* 맨 위 제목 */
.main-title {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg, rgba(255,255,255,0.96) 0%, rgba(255,241,247,0.98) 48%, rgba(236,253,245,0.98) 100%);
    color: #0f172a;
    padding: 34px 26px 30px 26px;
    border-radius: 34px;
    text-align: center;
    margin-bottom: 22px;
    border: 2px solid #fbcfe8;
    box-shadow: 0 16px 36px rgba(15,23,42,0.10);
}
.main-title:before {
    content: "🌸";
    position: absolute;
    left: 26px;
    top: 16px;
    font-size: 72px;
    opacity: 0.23;
}
.main-title:after {
    content: "🌿";
    position: absolute;
    right: 28px;
    bottom: 12px;
    font-size: 78px;
    opacity: 0.24;
}
.main-title h1 {
    margin: 0;
    font-size: 46px;
    font-weight: 950;
    letter-spacing: -0.8px;
    color: #be185d;
}
.main-title p {
    margin-top: 12px;
    font-size: 18px;
    color: #475569;
    font-weight: 800;
    line-height: 1.65;
}
.garden-line {
    margin-top: 18px;
    font-size: 26px;
    letter-spacing: 8px;
}

/* 선택 영역 */
.selector-card {
    background: rgba(255,255,255,0.78);
    border: 1.5px solid #bbf7d0;
    border-radius: 24px;
    padding: 16px 18px 8px 18px;
    margin-bottom: 18px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.06);
}

/* 소개 카드 */
.info-card {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #ffffff 0%, #fff7fb 55%, #f0fdf4 100%);
    padding: 24px 26px;
    border-radius: 28px;
    border: 2px solid #fbcfe8;
    margin-bottom: 20px;
    box-shadow: 0 10px 24px rgba(15,23,42,0.08);
}
.info-card:after {
    content: "🌱";
    position: absolute;
    right: 22px;
    top: 18px;
    font-size: 46px;
    opacity: 0.22;
}
.info-card h2 {
    margin-top: 0;
    margin-bottom: 6px;
    color: #166534;
    font-size: 30px;
    font-weight: 950;
}
.info-card p {
    color: #475569;
    font-size: 17px;
    font-weight: 750;
}

/* 지식 카드 */
.fact-card {
    background: linear-gradient(135deg, #fff7fb 0%, #ffffff 45%, #f0fdf4 100%);
    padding: 22px;
    border-radius: 26px;
    border: 2px solid #fbcfe8;
    box-shadow: 0 8px 20px rgba(15,23,42,0.07);
    margin-bottom: 18px;
}
.fact-card h3 {
    margin-top: 0;
    color: #be185d;
    font-size: 25px;
    font-weight: 950;
}
.tag {
    display: inline-block;
    background: linear-gradient(135deg, #dcfce7 0%, #ffffff 100%);
    color: #166534;
    padding: 8px 13px;
    border-radius: 999px;
    font-weight: 900;
    margin-right: 8px;
    margin-bottom: 8px;
    border: 1.5px solid #bbf7d0;
    box-shadow: 0 3px 8px rgba(15,23,42,0.04);
}

/* Reading 본문 */
.reading-card {
    background:
        linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(255,247,251,0.98) 100%);
    padding: 30px;
    border-radius: 30px;
    border: 2px solid #bfdbfe;
    font-size: 21px;
    line-height: 1.85;
    box-shadow: 0 10px 24px rgba(15,23,42,0.08);
}
.reading-card b {
    color: #1d4ed8;
}

/* 해석 카드 */
.korean-card {
    background: linear-gradient(135deg, #fffbeb 0%, #ffffff 50%, #f0fdf4 100%);
    padding: 26px;
    border-radius: 26px;
    border: 2px solid #fde68a;
    font-size: 20px;
    line-height: 1.75;
    box-shadow: 0 8px 20px rgba(15,23,42,0.06);
}

/* 표현 카드 */
.expression {
    background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
    padding: 15px 17px;
    border-radius: 18px;
    margin-bottom: 10px;
    font-size: 19px;
    font-weight: 800;
    border-left: 8px solid #22c55e;
    box-shadow: 0 3px 10px rgba(15,23,42,0.05);
}

/* 섹션 박스 */
.section-box {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #ffffff 0%, #fff7fb 100%);
    padding: 20px 22px;
    border-radius: 24px;
    border: 1.5px solid #fbcfe8;
    box-shadow: 0 6px 16px rgba(15,23,42,0.07);
    margin-bottom: 16px;
}
.section-box h3 {
    margin: 0;
    color: #be185d;
    font-size: 24px;
    font-weight: 950;
}
.section-box:after {
    content: "🌿";
    position: absolute;
    right: 16px;
    top: 12px;
    font-size: 32px;
    opacity: 0.20;
}

/* 탭 */
div[data-testid="stTabs"] button {
    font-size: 18px;
    font-weight: 900;
    border-radius: 16px 16px 0 0;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #be185d;
}

/* 버튼 */
.stButton > button {
    border-radius: 18px;
    font-weight: 900;
    border: 2px solid #bbf7d0;
    background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
    color: #14532d;
    box-shadow: 0 5px 14px rgba(15,23,42,0.08);
}
.stButton > button:hover {
    border: 2px solid #f9a8d4;
    background: linear-gradient(135deg, #fff7fb 0%, #ffffff 100%);
    color: #be185d;
}

/* 라디오, 입력창 */
div[role="radiogroup"] {
    background: rgba(255,255,255,0.72);
    padding: 12px 14px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
}
textarea {
    border-radius: 18px !important;
}

/* 미션/카드/문자 활동 */
.mission-card {
    background: linear-gradient(135deg, #eff6ff 0%, #ffffff 55%, #f0fdf4 100%);
    border: 2px solid #bfdbfe;
    border-radius: 24px;
    padding: 18px 20px;
    margin-bottom: 14px;
    box-shadow: 0 6px 16px rgba(15,23,42,0.06);
}
.mission-title {
    font-size: 22px;
    font-weight: 950;
    color: #1d4ed8;
    margin-bottom: 8px;
}
.mission-guide {
    font-size: 17px;
    font-weight: 800;
    color: #475569;
    line-height: 1.7;
}
.story-card {
    background: linear-gradient(135deg, #ffffff 0%, #fff7ed 48%, #f0fdf4 100%);
    border: 2px solid #fed7aa;
    border-radius: 26px;
    padding: 18px 20px;
    margin-bottom: 16px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.07);
}
.story-card-title {
    font-size: 23px;
    font-weight: 950;
    color: #c2410c;
    margin-bottom: 10px;
}
.message-card {
    background: linear-gradient(135deg, #fdf2f8 0%, #ffffff 55%, #eff6ff 100%);
    border: 2px solid #f9a8d4;
    border-radius: 26px;
    padding: 18px 20px;
    margin-top: 12px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.07);
}
.message-line {
    font-size: 20px;
    font-weight: 850;
    color: #334155;
    line-height: 1.7;
}


/* 이미지, 비디오 주변 */
div[data-testid="stImage"] img {
    border-radius: 26px;
    box-shadow: 0 10px 24px rgba(15,23,42,0.12);
}

/* 모바일 */
@media (max-width: 768px) {
    .main-title {
        padding: 28px 18px 24px 18px;
        border-radius: 26px;
    }
    .main-title h1 {
        font-size: 34px;
    }
    .main-title p {
        font-size: 15px;
    }
    .reading-card {
        font-size: 18px;
        padding: 22px;
    }
    .korean-card {
        font-size: 17px;
        padding: 20px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 자료
# 이미지 파일은 pages/images 폴더에 넣으면 됩니다.
# =========================================================
data_bank = {
    "인물": {
        "⚽ Ronaldo": {
            "title": "Cristiano Ronaldo",
            "subtitle": "Country, family, teams, and achievements",
            "video_url": "https://www.youtube.com/watch?v=yQU8q_wXESU",
            "image_path": BASE_DIR / "images" / "ronaldo.png",
            "facts": [
                "Born in Portugal in 1985",
                "Grew up on the island of Madeira",
                "Won the Champions League in 2008 and Euro 2016 with Portugal"
            ],
            "dialogue": [
                ("Text", "Cristiano Ronaldo was born in Portugal in 1985.", "크리스티아누 호날두는 1985년에 포르투갈에서 태어났다."),
                ("Text", "He grew up on the island of Madeira.", "그는 마데이라 섬에서 자랐다."),
                ("Text", "He has one brother and two sisters.", "그에게는 남자 형제 한 명과 여자 형제 두 명이 있다."),
                ("Text", "His brother's name is Hugo.", "그의 남자 형제 이름은 후고이다."),
                ("Text", "His sisters' names are Elma and Katia.", "그의 여자 형제 이름은 엘마와 카티아이다."),
                ("Text", "Ronaldo first played for Sporting CP in Portugal.", "호날두는 처음에 포르투갈의 스포르팅 CP에서 뛰었다."),
                ("Text", "Later, he moved to Manchester United in England.", "나중에 그는 영국의 맨체스터 유나이티드로 이적했다."),
                ("Text", "He won his first Ballon d'Or in 2008.", "그는 2008년에 첫 발롱도르를 받았다."),
                ("Text", "In 2008, he won the Champions League with Manchester United.", "2008년에 그는 맨체스터 유나이티드와 함께 챔피언스리그에서 우승했다."),
                ("Text", "In 2016, he won Euro 2016 with Portugal.", "2016년에 그는 포르투갈과 함께 유로 2016에서 우승했다."),
                ("Text", "He says talent is helpful, but good habits are more important.", "그는 재능도 도움이 되지만 좋은 습관이 더 중요하다고 말한다.")
            ],
            "key_expressions": [
                "was born in",
                "grew up",
                "one brother and two sisters",
                "first played for",
                "moved to",
                "won his first Ballon d'Or",
                "won the Champions League",
                "good habits are more important"
            ],
            "questions": [
                ("1. Ronaldo는 어느 나라에서 태어났나요?", ["Spain", "Portugal", "Brazil", "England"], "Portugal"),
                ("2. Ronaldo는 몇 년에 태어났나요?", ["1985", "1995", "2008", "2016"], "1985"),
                ("3. Ronaldo는 어느 섬에서 자랐나요?", ["Jeju", "Madeira", "Hawaii", "Bali"], "Madeira"),
                ("4. Ronaldo에게는 형제가 몇 명 있나요?", ["One brother and two sisters", "Two brothers and one sister", "Three brothers", "Three sisters"], "One brother and two sisters"),
                ("5. Ronaldo가 첫 Ballon d'Or를 받은 해는 언제인가요?", ["1985", "2008", "2016", "2023"], "2008")
            ],
            "reflection_prompt": "Ronaldo를 통해 내가 배울 점은 무엇인가요?"
        },

        "🏀 Jordan": {
            "title": "Basketball Talk with Jordan",
            "subtitle": "Failure, effort, and mental strength",
            "video_url": "https://www.youtube.com/watch?v=wIbsBey5s8A",
            "image_path": BASE_DIR / "images" / "jordan.png",
            "facts": [
                "American basketball legend",
                "Won 6 NBA championships with the Chicago Bulls",
                "Known for strong competitiveness and clutch performances",
                "Famous lesson: failure can become motivation"
            ],
            "dialogue": [
                ("Jordan", "Hi! Do you like basketball?", "안녕! 너는 농구를 좋아하니?"),
                ("Me", "Yes, I do. I love basketball.", "네, 좋아해요. 저는 농구를 정말 좋아해요."),
                ("Jordan", "That is great. Do you know what I am famous for?", "멋지다. 내가 무엇으로 유명한지 아니?"),
                ("Me", "You are famous for winning many championships.", "많은 우승을 한 것으로 유명해요."),
                ("Jordan", "Yes. I won six NBA championships with the Chicago Bulls.", "맞아. 나는 시카고 불스와 함께 NBA 챔피언십에서 여섯 번 우승했어."),
                ("Me", "That is amazing. Were you always the best?", "정말 대단해요. 항상 최고였나요?"),
                ("Jordan", "No. I faced failure many times.", "아니. 나는 여러 번 실패를 겪었어."),
                ("Me", "Really? I thought great players never failed.", "정말요? 훌륭한 선수들은 실패하지 않는 줄 알았어요."),
                ("Jordan", "Great players fail, but they use failure as motivation.", "훌륭한 선수들도 실패해. 하지만 실패를 동기로 사용해."),
                ("Me", "I sometimes miss easy shots.", "저는 가끔 쉬운 슛도 놓쳐요."),
                ("Jordan", "That is normal. Missing a shot does not make you weak.", "그건 자연스러운 일이야. 슛을 놓친다고 약한 사람이 되는 건 아니야."),
                ("Me", "Then what should I do after a mistake?", "그럼 실수한 뒤에는 어떻게 해야 하나요?"),
                ("Jordan", "Think about why it happened, practice again, and take the next shot with confidence.", "왜 그런 일이 일어났는지 생각하고, 다시 연습하고, 다음 슛을 자신 있게 던져."),
                ("Me", "I heard you were very competitive.", "당신은 승부욕이 정말 강했다고 들었어요."),
                ("Jordan", "Yes. I wanted to win, but I also worked very hard to deserve winning.", "맞아. 나는 이기고 싶었지만, 이길 자격을 갖추기 위해 정말 열심히 노력했어."),
                ("Me", "So competitiveness is not just wanting to win?", "그러면 승부욕은 단순히 이기고 싶어 하는 것만은 아니네요?"),
                ("Jordan", "Right. Real competitiveness means preparation, focus, and responsibility.", "맞아. 진짜 승부욕은 준비, 집중, 책임감을 뜻해."),
                ("Me", "I want to have that kind of mindset.", "저도 그런 마음가짐을 갖고 싶어요."),
                ("Jordan", "Then practice hard, learn from failure, and never be afraid of the next challenge.", "그렇다면 열심히 연습하고, 실패에서 배우고, 다음 도전을 두려워하지 마."),
                ("Me", "I will remember that failure can become motivation.", "실패가 동기가 될 수 있다는 것을 기억할게요."),
                ("Jordan", "Good. Champions are made by effort, courage, and a strong mind.", "좋아. 챔피언은 노력, 용기, 강한 마음으로 만들어져.")
            ],
            "key_expressions": [
                "I won six NBA championships.",
                "Failure can become motivation.",
                "Take the next shot with confidence.",
                "Real competitiveness means preparation.",
                "Learn from failure.",
                "Never be afraid of the next challenge."
            ],
            "questions": [
                ("1. 조던은 시카고 불스와 함께 NBA에서 몇 번 우승했나요?", ["Six", "Two", "Ten", "One"], "Six"),
                ("2. 조던은 훌륭한 선수들이 실패를 무엇으로 사용한다고 말하나요?", ["Motivation", "An excuse", "A game", "A secret"], "Motivation"),
                ("3. 진짜 승부욕은 무엇을 뜻하나요?", ["Preparation, focus, and responsibility", "Only wanting to win", "Getting angry", "Never practicing"], "Preparation, focus, and responsibility")
            ],
            "reflection_prompt": "Jordan을 통해 내가 배울 점은 무엇인가요?"
        },

        "⚽ Son Heung-min": {
            "title": "Talk with Son Heung-min",
            "subtitle": "Teamwork, humility, and respect",
            "video_url": "https://www.youtube.com/watch?v=AmKHi17sy1Q",
            "image_path": BASE_DIR / "images" / "son.png",
            "facts": [
                "South Korean soccer star",
                "Known for speed, finishing, teamwork, and a humble attitude",
                "He trained very hard with his father when he was young",
                "Lesson: strong basics and discipline can build great skills"
            ],
            "dialogue": [
                ("Son", "Hi! Do you enjoy playing soccer with your friends?", "안녕! 친구들과 축구하는 것을 즐기니?"),
                ("Me", "Yes, I do. I like playing as a team.", "네. 저는 한 팀으로 경기하는 것을 좋아해요."),
                ("Son", "That is great. Soccer is not only about one player.", "좋아. 축구는 한 사람만의 경기가 아니야."),
                ("Me", "What is important in a team?", "팀에서 중요한 것은 무엇인가요?"),
                ("Son", "Respect, communication, and hard work are important.", "존중, 소통, 노력이 중요해."),
                ("Me", "I heard you trained very hard with your father.", "아버지와 정말 열심히 훈련했다고 들었어요."),
                ("Son", "Yes. When I was young, my father helped me build strong basics.", "맞아. 어릴 때 아버지는 내가 탄탄한 기본기를 만들도록 도와주셨어."),
                ("Me", "What kind of training did you do?", "어떤 훈련을 했나요?"),
                ("Son", "I practiced simple skills again and again, like ball control and shooting.", "볼 컨트롤과 슈팅 같은 기본 기술을 반복해서 연습했어."),
                ("Me", "That sounds boring sometimes.", "가끔은 지루했을 것 같아요."),
                ("Son", "It was not always fun, but basics become power in real games.", "항상 재미있지는 않았지만, 기본기는 실제 경기에서 힘이 돼."),
                ("Me", "Sometimes I want to score alone.", "가끔은 혼자 골을 넣고 싶어요."),
                ("Son", "Scoring is good, but helping your team is also important.", "골을 넣는 것도 좋지만, 팀을 돕는 것도 중요해."),
                ("Me", "How can I help my team?", "어떻게 하면 팀에 도움이 될 수 있을까요?"),
                ("Son", "Listen to your teammates and move together.", "동료들의 말을 듣고 함께 움직여."),
                ("Me", "I sometimes get angry when we lose.", "질 때 가끔 화가 나요."),
                ("Son", "That can happen. But a good player stays humble.", "그럴 수 있어. 하지만 좋은 선수는 겸손함을 잃지 않아."),
                ("Me", "Why is humility important?", "왜 겸손함이 중요한가요?"),
                ("Son", "Because it helps you learn from others and respect the team.", "겸손함은 다른 사람에게서 배우고 팀을 존중하게 도와주기 때문이야."),
                ("Me", "I will practice the basics and respect my team.", "기본기를 연습하고 팀을 존중할게요."),
                ("Son", "Good. Great players are built by discipline, teamwork, and attitude.", "좋아. 훌륭한 선수는 discipline, teamwork, attitude로 만들어져.")
            ],
            "key_expressions": [
                "Soccer is not only about one player.",
                "Build strong basics.",
                "Basics become power in real games.",
                "Listen to your teammates.",
                "Stay humble.",
                "Discipline, teamwork, and attitude are important."
            ],
            "questions": [
                ("1. 손흥민이 탄탄한 기본기를 만들도록 도와준 사람은 누구인가요?", ["His father", "A singer", "A movie director", "A chef"], "His father"),
                ("2. 손흥민은 어떤 기본 기술을 연습했나요?", ["Ball control and shooting", "Cooking and drawing", "Singing and dancing", "Sleeping and resting"], "Ball control and shooting"),
                ("3. 실제 경기에서 힘이 되는 것은 무엇인가요?", ["Basics", "Only luck", "Noise", "A phone"], "Basics")
            ],
            "reflection_prompt": "Son Heung-min을 통해 내가 배울 점은 무엇인가요?"
        },

        "🎤 IU": {
            "title": "Music Talk with IU",
            "subtitle": "Creativity, sincerity, and expression",
            "video_url": "https://www.youtube.com/watch?v=0k1uM8LmT-o",
            "image_path": BASE_DIR / "images" / "iu.png",
            "facts": [
                "Korean singer-songwriter and actor",
                "Known for emotional lyrics, storytelling, and sincere expression",
                "Lesson: honest feelings can become powerful words"
            ],
            "dialogue": [
                ("IU", "Hi! Do you like music?", "안녕! 너는 음악을 좋아하니?"),
                ("Me", "Yes, I do. Music makes me happy.", "네. 음악은 저를 행복하게 해요."),
                ("IU", "That is wonderful. What kind of music do you like?", "멋지다. 어떤 음악을 좋아하니?"),
                ("Me", "I like songs with warm messages.", "저는 따뜻한 메시지가 있는 노래를 좋아해요."),
                ("IU", "A good song can comfort people.", "좋은 노래는 사람들을 위로할 수 있어."),
                ("Me", "I want to express my feelings better.", "저도 제 감정을 더 잘 표현하고 싶어요."),
                ("IU", "Then you need to listen to your heart.", "그렇다면 너의 마음에 귀 기울여야 해."),
                ("Me", "Sometimes I do not know what I feel.", "가끔은 제가 무엇을 느끼는지 잘 모르겠어요."),
                ("IU", "That is okay. Write one small sentence first.", "괜찮아. 먼저 짧은 문장 하나를 써 봐."),
                ("Me", "Can a small sentence become a song?", "짧은 문장이 노래가 될 수 있나요?"),
                ("IU", "Yes. Honest feelings can become powerful words.", "그럼. 솔직한 감정은 힘 있는 말이 될 수 있어."),
                ("Me", "I am shy about showing my writing.", "제 글을 보여주는 것이 부끄러워요."),
                ("IU", "Many people feel that way. But sincerity touches people.", "많은 사람들이 그렇게 느껴. 하지만 진심은 사람들에게 닿아."),
                ("Me", "So I should not hide my feelings all the time?", "그러면 제 감정을 항상 숨기지 않아도 되나요?"),
                ("IU", "Right. You can express them slowly and honestly.", "맞아. 천천히, 솔직하게 표현하면 돼."),
                ("Me", "I will try to express myself.", "저도 제 자신을 표현해 볼게요."),
                ("IU", "Good. Be honest, keep writing, and trust your voice.", "좋아. 솔직해지고, 계속 쓰고, 너의 목소리를 믿어.")
            ],
            "key_expressions": [
                "Music can comfort people.",
                "Listen to your heart.",
                "Honest feelings can become powerful words.",
                "Sincerity touches people.",
                "Trust your voice."
            ],
            "questions": [
                ("1. 학생을 행복하게 만드는 것은 무엇인가요?", ["Music", "Math", "Rain", "Homework"], "Music"),
                ("2. 솔직한 감정은 무엇이 될 수 있나요?", ["Powerful words", "A problem", "A mistake", "A game"], "Powerful words"),
                ("3. 아이유는 학생에게 무엇을 믿으라고 말하나요?", ["Your voice", "Only luck", "A phone", "Other people"], "Your voice")
            ],
            "reflection_prompt": "IU를 통해 내가 배울 점은 무엇인가요?"
        },

        "⛸️ Kim Yuna": {
            "title": "Skating Talk with Kim Yuna",
            "subtitle": "Focus, balance, and mental strength",
            "video_url": "https://www.youtube.com/watch?v=DaSyR7putcg",
            "image_path": BASE_DIR / "images" / "kim_yuna.png",
            "facts": [
                "South Korean figure skating champion",
                "Known for graceful performances, strong technique, and calmness under pressure",
                "Lesson: preparation helps control nervousness"
            ],
            "dialogue": [
                ("Kim Yuna", "Hi! Do you like watching figure skating?", "안녕! 너는 피겨스케이팅 보는 것을 좋아하니?"),
                ("Me", "Yes, I do. It looks beautiful and difficult.", "네. 아름답고 어려워 보여요."),
                ("Kim Yuna", "You are right. It needs balance, practice, and focus.", "맞아. 균형, 연습, 집중이 필요해."),
                ("Me", "Were you nervous before a competition?", "경기 전에 긴장했나요?"),
                ("Kim Yuna", "Of course. Everyone can feel nervous before an important moment.", "물론이지. 중요한 순간 전에는 누구나 긴장할 수 있어."),
                ("Me", "How did you control your mind?", "마음을 어떻게 다스렸나요?"),
                ("Kim Yuna", "I focused on what I practiced. I trusted my training.", "내가 연습한 것에 집중했어. 내 훈련을 믿었지."),
                ("Me", "Sometimes I worry too much before a test.", "저는 시험 전에 가끔 너무 많이 걱정해요."),
                ("Kim Yuna", "That is natural. But worry alone does not help.", "그건 자연스러운 일이야. 하지만 걱정만으로는 도움이 되지 않아."),
                ("Me", "Then what should I do?", "그럼 어떻게 해야 할까요?"),
                ("Kim Yuna", "Prepare step by step, breathe slowly, and focus on one thing at a time.", "차근차근 준비하고, 천천히 숨 쉬고, 한 번에 하나에 집중해."),
                ("Me", "I want to be calm under pressure.", "압박감 속에서도 침착해지고 싶어요."),
                ("Kim Yuna", "Calmness comes from practice and trust in yourself.", "침착함은 연습과 자신에 대한 믿음에서 나와."),
                ("Me", "I will practice more and worry less.", "더 연습하고 덜 걱정할게요."),
                ("Kim Yuna", "Good. Do your best, but also enjoy your own growth.", "좋아. 최선을 다하되, 너의 성장도 즐겨 봐.")
            ],
            "key_expressions": [
                "It needs balance, practice, and focus.",
                "Trust your training.",
                "Worry alone does not help.",
                "Focus on one thing at a time.",
                "Enjoy your own growth."
            ],
            "questions": [
                ("1. 피겨스케이팅에는 무엇이 필요한가요?", ["Balance, practice, and focus", "Only luck", "No practice", "A loud voice"], "Balance, practice, and focus"),
                ("2. 김연아는 무엇에 집중했나요?", ["What she practiced", "Other people's mistakes", "Only the result", "Her phone"], "What she practiced"),
                ("3. 학생은 시험 전에 어떻게 해야 하나요?", ["Prepare step by step", "Only worry", "Give up", "Forget everything"], "Prepare step by step")
            ],
            "reflection_prompt": "Kim Yuna를 통해 내가 배울 점은 무엇인가요?"
        },

        "🎤 BTS Jungkook": {
            "title": "Music Talk with Jungkook",
            "subtitle": "Practice, stage, and growth",
            "video_url": "여기에_정국_유튜브_링크",
            "image_path": BASE_DIR / "images" / "jungkook.png",
            "facts": [
                "Korean singer and performer known worldwide",
                "Known for strong stage performance, steady practice, and self-improvement",
                "Lesson: focus on your own growth, not comparison"
            ],
            "dialogue": [
                ("Jungkook", "Hi! Do you like music and dancing?", "안녕! 너는 음악과 춤을 좋아하니?"),
                ("Me", "Yes, I do. I like singing and watching performances.", "네. 저는 노래하는 것과 공연 보는 것을 좋아해요."),
                ("Jungkook", "That is great. Performing can be exciting, but it takes a lot of practice.", "멋지다. 공연은 신날 수 있지만 많은 연습이 필요해."),
                ("Me", "Do you practice every day?", "매일 연습하나요?"),
                ("Jungkook", "I try to practice often. Small practice every day can make a big difference.", "자주 연습하려고 해. 매일의 작은 연습이 큰 차이를 만들 수 있어."),
                ("Me", "Sometimes I feel nervous in front of people.", "가끔 사람들 앞에서 긴장돼요."),
                ("Jungkook", "That is natural. Even performers can feel nervous before a stage.", "그건 자연스러운 일이야. 공연자들도 무대 전에 긴장할 수 있어."),
                ("Me", "How can I become more confident?", "어떻게 하면 더 자신감을 가질 수 있을까요?"),
                ("Jungkook", "Prepare well, breathe slowly, and focus on the message you want to share.", "잘 준비하고, 천천히 숨 쉬고, 네가 전하고 싶은 메시지에 집중해."),
                ("Me", "I worry that I am not talented enough.", "제가 충분히 재능이 없을까 봐 걱정돼요."),
                ("Jungkook", "Talent is helpful, but effort and attitude are also very important.", "재능도 도움이 되지만 노력과 태도도 매우 중요해."),
                ("Me", "I want to improve little by little.", "조금씩 발전하고 싶어요."),
                ("Jungkook", "That is the right mindset. Do not compare yourself too much with others.", "그게 좋은 마음가짐이야. 다른 사람과 너무 많이 비교하지 마."),
                ("Me", "I will focus on my own growth.", "제 성장에 집중할게요."),
                ("Jungkook", "Good. Keep practicing, enjoy the process, and trust your own voice.", "좋아. 계속 연습하고, 과정을 즐기고, 너만의 목소리를 믿어.")
            ],
            "key_expressions": [
                "Small practice can make a big difference.",
                "I feel nervous.",
                "How can I become more confident?",
                "Effort and attitude are important.",
                "Focus on my own growth.",
                "Trust your own voice."
            ],
            "questions": [
                ("1. 학생은 무엇을 좋아하나요?", ["Singing and watching performances", "Only sleeping", "Cooking alone", "Reading maps"], "Singing and watching performances"),
                ("2. 매일의 작은 연습은 무엇을 만들 수 있나요?", ["Make a big difference", "Make people forget everything", "Stop growth", "Make practice useless"], "Make a big difference"),
                ("3. 정국은 학생에게 무엇을 믿으라고 말하나요?", ["Your own voice", "Only luck", "A computer", "Other people's opinions"], "Your own voice")
            ],
            "reflection_prompt": "Jungkook을 통해 내가 배울 점은 무엇인가요?"
        }
    },

    "장소": {
        "🏜️ Grand Canyon": {
            "title": "A Trip to the Grand Canyon",
            "subtitle": "Nature, time, and wonder",
            "video_url": "여기에_그랜드캐니언_유튜브_링크",
            "image_path": BASE_DIR / "images" / "grand_canyon.png",
            "facts": [
                "Located in Arizona, USA",
                "Formed mainly by the Colorado River and erosion over a very long time",
                "Representative feature: colorful rock layers that show Earth's history"
            ],
            "dialogue": [
                ("Guide", "Welcome to the Grand Canyon.", "그랜드캐니언에 오신 것을 환영합니다."),
                ("Me", "Wow, it is huge and beautiful.", "와, 정말 크고 아름다워요."),
                ("Guide", "Nature can make us feel small.", "자연은 우리를 작게 느끼게 할 수 있어요."),
                ("Me", "I feel amazed when I look down.", "아래를 내려다보니 정말 경이로워요."),
                ("Guide", "This canyon was shaped over a very long time.", "이 협곡은 아주 오랜 시간에 걸쳐 형성되었어요."),
                ("Me", "How was it made?", "어떻게 만들어졌나요?"),
                ("Guide", "The Colorado River and erosion slowly cut through the rocks.", "콜로라도강과 침식 작용이 천천히 바위를 깎아냈어요."),
                ("Me", "So water can change the land?", "그러면 물이 땅을 바꿀 수 있나요?"),
                ("Guide", "Yes. Small forces can make huge changes over time.", "네. 작은 힘도 오랜 시간 동안 큰 변화를 만들 수 있어요."),
                ("Me", "That is surprising.", "놀라워요."),
                ("Guide", "The colorful rock layers show different periods of Earth's history.", "알록달록한 암석층은 지구 역사의 여러 시기를 보여줘요."),
                ("Me", "It is like reading a book made of rocks.", "바위로 된 책을 읽는 것 같아요."),
                ("Guide", "Exactly. Nature has many stories.", "맞아요. 자연에는 많은 이야기가 있어요."),
                ("Me", "I want to protect nature.", "저는 자연을 보호하고 싶어요."),
                ("Guide", "Good. When we understand nature, we can respect it more.", "좋아요. 자연을 이해할 때 우리는 자연을 더 존중할 수 있어요.")
            ],
            "key_expressions": [
                "Nature can make us feel small.",
                "Erosion can change the land.",
                "Small forces can make huge changes.",
                "Rock layers show history.",
                "Protect nature."
            ],
            "questions": [
                ("1. 그랜드캐니언은 어디에 있나요?", ["Arizona, USA", "London, UK", "Seoul, Korea", "Paris, France"], "Arizona, USA"),
                ("2. 그랜드캐니언 형성에 도움을 준 것은 무엇인가요?", ["The Colorado River and erosion", "Only people", "A machine", "A building"], "The Colorado River and erosion"),
                ("3. 암석층은 무엇을 보여 주나요?", ["Earth's history", "Only sports", "Modern fashion", "A school rule"], "Earth's history")
            ],
            "reflection_prompt": "Grand Canyon을 통해 내가 배울 점은 무엇인가요?"
        },

        "🗽 New York": {
            "title": "A Visit to New York",
            "subtitle": "Dreams, diversity, and city life",
            "video_url": "여기에_뉴욕_유튜브_링크",
            "image_path": BASE_DIR / "images" / "new_york.png",
            "facts": [
                "One of the most famous cities in the United States",
                "Known for Times Square, the Statue of Liberty, Central Park, and diverse cultures",
                "Representative feature: a global city where many cultures meet"
            ],
            "dialogue": [
                ("Guide", "Welcome to New York.", "뉴욕에 오신 것을 환영합니다."),
                ("Me", "There are so many people here.", "여기에는 정말 많은 사람들이 있어요."),
                ("Guide", "People from many cultures live here.", "다양한 문화의 사람들이 이곳에 살고 있어요."),
                ("Me", "It feels busy and exciting.", "바쁘고 신나게 느껴져요."),
                ("Guide", "New York is often called a global city.", "뉴욕은 종종 세계적인 도시라고 불려요."),
                ("Me", "What does global city mean?", "세계적인 도시라는 것은 무슨 뜻인가요?"),
                ("Guide", "It means people, ideas, money, art, and culture from many countries meet here.", "많은 나라의 사람, 생각, 돈, 예술, 문화가 이곳에서 만난다는 뜻이에요."),
                ("Me", "That sounds powerful.", "강력하게 들려요."),
                ("Guide", "Yes. Places like Times Square show energy, and the Statue of Liberty shows freedom.", "맞아요. 타임스퀘어는 에너지를 보여주고, 자유의 여신상은 자유를 보여줘요."),
                ("Me", "I want to see both places.", "두 곳 모두 보고 싶어요."),
                ("Guide", "You should. But remember, a big city can also be difficult.", "그래요. 하지만 큰 도시는 힘들 수도 있다는 것을 기억하세요."),
                ("Me", "Why is it difficult?", "왜 힘든가요?"),
                ("Guide", "Life can be fast, expensive, and competitive.", "삶이 빠르고, 비싸고, 경쟁적일 수 있어요."),
                ("Me", "Still, I want to follow my dream.", "그래도 저는 제 꿈을 따라가고 싶어요."),
                ("Guide", "Then stay curious, keep learning, and respect different cultures.", "그렇다면 호기심을 갖고, 계속 배우고, 다양한 문화를 존중하세요.")
            ],
            "key_expressions": [
                "People from many cultures live here.",
                "New York is a global city.",
                "The Statue of Liberty shows freedom.",
                "Life can be competitive.",
                "Respect different cultures."
            ],
            "questions": [
                ("1. 뉴욕은 어떤 도시인가요?", ["A global city", "A small village", "A quiet farm", "A desert"], "A global city"),
                ("2. 자유의 여신상은 무엇을 보여 주나요?", ["Freedom", "Homework", "Sports", "Silence"], "Freedom"),
                ("3. 학생은 무엇을 존중해야 하나요?", ["Different cultures", "Only one idea", "Noise", "Fear"], "Different cultures")
            ],
            "reflection_prompt": "New York을 통해 내가 배울 점은 무엇인가요?"
        },

        "🏯 Gyeongbokgung": {
            "title": "A Visit to Gyeongbokgung",
            "subtitle": "History, culture, and Korean identity",
            "video_url": "여기에_경복궁_유튜브_링크",
            "image_path": BASE_DIR / "images" / "gyeongbokgung.png",
            "facts": [
                "Gyeongbokgung was first built in 1395 during the Joseon Dynasty.",
                "It was the main royal palace of Joseon.",
                "Representative feature: Geunjeongjeon Hall and traditional palace architecture."
            ],
            "dialogue": [
                ("Guide", "Welcome to Gyeongbokgung.", "경복궁에 오신 것을 환영합니다."),
                ("Me", "This palace is beautiful.", "이 궁궐은 아름다워요."),
                ("Guide", "Gyeongbokgung was first built in 1395 during the Joseon Dynasty.", "경복궁은 조선 시대인 1395년에 처음 지어졌어요."),
                ("Me", "So it is a very old palace.", "그러면 아주 오래된 궁궐이네요."),
                ("Guide", "Yes. It was the main royal palace of Joseon.", "맞아요. 조선의 중심 궁궐이었어요."),
                ("Me", "What does the name Gyeongbokgung mean?", "경복궁이라는 이름은 무슨 뜻인가요?"),
                ("Guide", "It means a palace greatly blessed by heaven.", "하늘이 크게 복을 내린 궁궐이라는 뜻이에요."),
                ("Me", "That meaning is impressive.", "그 뜻이 인상적이에요."),
                ("Guide", "The palace shows Korean history, architecture, and royal culture.", "이 궁궐은 한국의 역사, 건축, 왕실 문화를 보여줘요."),
                ("Me", "I can see old buildings and traditional colors.", "오래된 건물과 전통적인 색을 볼 수 있어요."),
                ("Guide", "One important building is Geunjeongjeon Hall, where important state events were held.", "중요한 건물 중 하나는 근정전이고, 중요한 국가 행사가 열렸던 곳이에요."),
                ("Me", "It feels like history is alive here.", "이곳에서는 역사가 살아 있는 것 같아요."),
                ("Guide", "That is right. Places like this help us remember the past.", "맞아요. 이런 장소는 우리가 과거를 기억하도록 도와줘요."),
                ("Me", "I want to learn more about Korean culture.", "한국 문화에 대해 더 배우고 싶어요."),
                ("Guide", "Good. When we understand the past, we can build a better future.", "좋아요. 과거를 이해할 때 더 나은 미래를 만들 수 있어요.")
            ],
            "key_expressions": [
                "It was first built in 1395.",
                "It was the main royal palace of Joseon.",
                "It shows Korean history and culture.",
                "History is alive here.",
                "Build a better future."
            ],
            "questions": [
                ("1. 경복궁은 처음 언제 지어졌나요?", ["1395", "1910", "2020", "1600"], "1395"),
                ("2. 경복궁은 어느 시대에 지어졌나요?", ["Joseon Dynasty", "Roman Empire", "Ming Dynasty", "British Empire"], "Joseon Dynasty"),
                ("3. 경복궁은 무엇을 보여 주나요?", ["Korean history and culture", "Only sports", "Only food", "Only music"], "Korean history and culture")
            ],
            "reflection_prompt": "Gyeongbokgung을 통해 내가 배울 점은 무엇인가요?"
        }
    }
,
    "교과서": {
        "📘 교과서": {
            "title": "교과서",
            "subtitle": "November 25th, 2075 · Future lunch and a new food machine",
            "video_url": "",
            "image_path": None,
            "facts": [
                "Date: November 25th, 2075",
                "Topic: a new food machine at school",
                "Key idea: future food can be fast, healthy, and personalized"
            ],
            "dialogue": [
                ("Textbook", "November 25th, 2075", "2075년 11월 25일"),
                ("Textbook", "Today's lunch was impressive.", "오늘의 점심은 인상적이었다."),
                ("Textbook", "A new food machine had just arrived, and I was the first student to try it.", "새로운 음식 기계가 막 도착했고, 나는 그것을 처음으로 사용해 본 학생이었다."),
                ("Textbook", "Once I chose a menu option, a healthy meal came out.", "내가 메뉴 선택지를 고르자마자 건강한 식사가 나왔다."),
                ("Textbook", "Whatever meal I chose, it contained all the nutrients I needed.", "내가 어떤 식사를 고르든, 그것에는 내가 필요로 하는 모든 영양소가 들어 있었다."),
                ("Textbook", "I was excited to be the first to press the button for the various options.", "나는 다양한 선택지를 위한 버튼을 처음으로 누르게 되어 신이 났다."),
                ("Textbook", "Today, I chose a hamburger made from lab-grown beef.", "오늘 나는 실험실에서 배양한 소고기로 만든 햄버거를 선택했다."),
                ("Textbook", "It contained all the nutrients needed for a teenager like me, including protein and minerals.", "그것에는 나 같은 십 대에게 필요한 단백질과 미네랄을 포함한 모든 영양소가 들어 있었다."),
                ("Textbook", "Of course, it was also very delicious.", "물론 그것은 아주 맛있기도 했다."),
                ("Textbook", "I tried low-fat ice cream for dessert which contained healthy nutrients.", "나는 디저트로 건강한 영양소가 들어 있는 저지방 아이스크림을 먹어 보았다."),
                ("Textbook", "What surprised me more was the speed of service.", "나를 더 놀라게 한 것은 서비스의 속도였다."),
                ("Textbook", "I don't think I'll have to wait in lines anymore!", "나는 더 이상 줄을 서서 기다릴 필요가 없을 것 같다!"),
                ("Textbook", "I'm looking forward to trying spicy tteokbokki tomorrow.", "나는 내일 매운 떡볶이를 먹어 보는 것이 기대된다.")
            ],
            "key_expressions": [
                "Today's lunch was impressive.",
                "A new food machine had just arrived.",
                "Once I chose a menu option, a healthy meal came out.",
                "Whatever meal I chose, it contained all the nutrients I needed.",
                "What surprised me more was the speed of service.",
                "I'm looking forward to trying spicy tteokbokki tomorrow."
            ],
            "questions": [
                ("1. 새로 도착한 기계는 무엇이었나요?", ["A new food machine", "A new robot teacher", "A new school bus", "A new library"], "A new food machine"),
                ("2. 글쓴이가 오늘 선택한 음식은 무엇인가요?", ["hamburger", "tteokbokki", "ice cream", "pizza"], "hamburger"),
                ("3. 글쓴이가 선택한 음식에 포함된 영양소 2가지는 무엇인가요?", ["protein and minerals", "sugar and fat", "rice and salt", "water and oil"], "protein and minerals"),
                ("4. 글쓴이는 왜 기분이 들떴나요?", ["다양한 선택지를 위한 버튼을 처음으로 누르게 되었기 때문에", "점심시간이 평소보다 늦게 시작되었기 때문에", "친구가 대신 음식을 골라 주었기 때문에", "내일 시험이 없어졌기 때문에"], "다양한 선택지를 위한 버튼을 처음으로 누르게 되었기 때문에")
            ],
            "reflection_prompt": "교과서 지문을 통해 내가 배울 점은 무엇인가요?"
        }
    }

}


# =========================================================
# Key Expressions를 단어 중심으로 바꾸기 위한 자료
# - 활동 탭에서 영어 단어의 한국어 뜻을 쓰는 빈칸 문제로 사용합니다.
# =========================================================
key_word_bank = {
    "⚽ Ronaldo": [
        ("was born in", "~에서 태어났다"),
        ("Portugal", "포르투갈"),
        ("1985", "1985년"),
        ("grew up", "자랐다"),
        ("Madeira", "마데이라"),
        ("one brother and two sisters", "남자 형제 한 명과 여자 형제 두 명"),
        ("Hugo", "후고"),
        ("Elma and Katia", "엘마와 카티아"),
        ("Sporting CP", "스포르팅 CP"),
        ("Manchester United", "맨체스터 유나이티드"),
        ("England", "영국"),
        ("Ballon d'Or", "발롱도르"),
        ("Champions League", "챔피언스리그"),
        ("Euro 2016", "유로 2016"),
        ("good habits", "좋은 습관"),
    ],
    "🏀 Jordan": [
        ("basketball", "농구"),
        ("championship", "우승 / 선수권 대회"),
        ("Chicago Bulls", "시카고 불스"),
        ("failure", "실패"),
        ("motivation", "동기"),
        ("miss a shot", "슛을 놓치다"),
        ("mistake", "실수"),
        ("confidence", "자신감"),
        ("competitive", "승부욕이 강한"),
        ("competitiveness", "승부욕"),
        ("preparation", "준비"),
        ("focus", "집중"),
        ("responsibility", "책임감"),
        ("challenge", "도전"),
        ("effort", "노력"),
    ],
    "⚽ Son Heung-min": [
        ("soccer", "축구"),
        ("team", "팀"),
        ("respect", "존중"),
        ("communication", "소통"),
        ("hard work", "노력"),
        ("father", "아버지"),
        ("strong basics", "탄탄한 기본기"),
        ("ball control", "볼 컨트롤"),
        ("shooting", "슈팅"),
        ("real game", "실제 경기"),
        ("teammate", "팀 동료"),
        ("stay humble", "겸손함을 유지하다"),
        ("discipline", "훈련 / 절제"),
        ("attitude", "태도"),
    ],
    "🎤 IU": [
        ("music", "음악"),
        ("happy", "행복한"),
        ("warm message", "따뜻한 메시지"),
        ("comfort", "위로하다"),
        ("express", "표현하다"),
        ("feeling", "감정"),
        ("listen to your heart", "너의 마음에 귀 기울이다"),
        ("sentence", "문장"),
        ("honest", "솔직한"),
        ("powerful words", "힘 있는 말"),
        ("sincerity", "진심"),
        ("touch people", "사람들의 마음에 닿다"),
        ("trust your voice", "너의 목소리를 믿다"),
    ],
    "⛸️ Kim Yuna": [
        ("figure skating", "피겨스케이팅"),
        ("beautiful", "아름다운"),
        ("difficult", "어려운"),
        ("balance", "균형"),
        ("practice", "연습"),
        ("focus", "집중"),
        ("nervous", "긴장한"),
        ("competition", "경기 / 대회"),
        ("control your mind", "마음을 다스리다"),
        ("trust your training", "너의 훈련을 믿다"),
        ("worry", "걱정하다"),
        ("step by step", "차근차근"),
        ("under pressure", "압박감 속에서"),
        ("growth", "성장"),
    ],
    "🎤 BTS Jungkook": [
        ("music", "음악"),
        ("dancing", "춤"),
        ("singing", "노래하기"),
        ("performance", "공연"),
        ("practice", "연습하다 / 연습"),
        ("make a big difference", "큰 차이를 만들다"),
        ("nervous", "긴장한"),
        ("stage", "무대"),
        ("confident", "자신감 있는"),
        ("message", "메시지"),
        ("talent", "재능"),
        ("effort", "노력"),
        ("attitude", "태도"),
        ("compare", "비교하다"),
        ("growth", "성장"),
    ],
    "🏜️ Grand Canyon": [
        ("welcome", "환영하다"),
        ("huge", "거대한"),
        ("beautiful", "아름다운"),
        ("nature", "자연"),
        ("feel small", "작게 느끼다"),
        ("canyon", "협곡"),
        ("shape", "형성하다"),
        ("Colorado River", "콜로라도강"),
        ("erosion", "침식"),
        ("change the land", "땅을 바꾸다"),
        ("rock layer", "암석층"),
        ("Earth's history", "지구의 역사"),
        ("protect nature", "자연을 보호하다"),
        ("respect", "존중하다"),
    ],
    "🗽 New York": [
        ("New York", "뉴욕"),
        ("people", "사람들"),
        ("culture", "문화"),
        ("busy", "바쁜"),
        ("exciting", "신나는"),
        ("global city", "세계적인 도시"),
        ("idea", "생각 / 아이디어"),
        ("art", "예술"),
        ("Times Square", "타임스퀘어"),
        ("energy", "에너지"),
        ("Statue of Liberty", "자유의 여신상"),
        ("freedom", "자유"),
        ("expensive", "비싼"),
        ("competitive", "경쟁적인"),
        ("respect different cultures", "다양한 문화를 존중하다"),
    ],
    "🏯 Gyeongbokgung": [
        ("palace", "궁궐"),
        ("beautiful", "아름다운"),
        ("Joseon Dynasty", "조선 시대 / 조선 왕조"),
        ("old", "오래된"),
        ("main royal palace", "중심 궁궐"),
        ("mean", "뜻하다"),
        ("blessed by heaven", "하늘이 복을 내린"),
        ("impressive", "인상적인"),
        ("history", "역사"),
        ("architecture", "건축"),
        ("royal culture", "왕실 문화"),
        ("traditional color", "전통적인 색"),
        ("state event", "국가 행사"),
        ("remember the past", "과거를 기억하다"),
        ("better future", "더 나은 미래"),
    ],
    "📘 교과서": [
        ("impressive", "인상적인"),
        ("food machine", "음식 기계"),
        ("arrive", "도착하다"),
        ("first student", "첫 번째 학생"),
        ("try", "시도하다 / 먹어 보다"),
        ("menu option", "메뉴 선택지"),
        ("healthy meal", "건강한 식사"),
        ("whatever", "무엇이든 / 어떤 ~든"),
        ("contain", "포함하다 / 들어 있다"),
        ("nutrient", "영양소"),
        ("various", "다양한"),
        ("lab-grown beef", "실험실에서 배양한 소고기"),
        ("teenager", "십 대"),
        ("protein", "단백질"),
        ("mineral", "미네랄"),
        ("low-fat", "저지방의"),
        ("dessert", "디저트"),
        ("speed of service", "서비스의 속도"),
        ("wait in lines", "줄을 서서 기다리다"),
        ("look forward to", "기대하다"),
        ("spicy tteokbokki", "매운 떡볶이"),
    ],
}


def get_key_words(topic_name, data):
    """주제별 핵심 단어를 가져옵니다. 없으면 기존 key_expressions에서 간단히 추출합니다."""
    if topic_name in key_word_bank:
        return key_word_bank[topic_name]

    fallback = []
    for exp in data.get("key_expressions", []):
        word = str(exp).replace(".", "").strip()
        if word:
            fallback.append((word, ""))
    return fallback


def normalize_answer(text):
    """학생 답안 비교를 조금 관대하게 하기 위한 정리 함수입니다."""
    return str(text).strip().lower().replace(" ", "").replace("/", "")


def is_correct_korean_answer(user_answer, correct_answer):
    user_norm = normalize_answer(user_answer)
    correct_options = [part.strip() for part in str(correct_answer).split("/")]

    if not user_norm:
        return False

    for option in correct_options:
        option_norm = normalize_answer(option)
        if option_norm and (user_norm == option_norm or option_norm in user_norm or user_norm in option_norm):
            return True
    return False


def reset_keys_by_prefix(prefixes):
    """현재 주제의 특정 활동 입력값과 채점 결과를 초기화합니다."""
    if isinstance(prefixes, str):
        prefixes = [prefixes]

    for key in list(st.session_state.keys()):
        if any(str(key).startswith(prefix) for prefix in prefixes):
            del st.session_state[key]


def show_pass_status(score, total, checked, pass_ratio=0.7):
    """70% 이상이면 통과로 표시합니다. 아직 모두 확인하지 않았으면 진행 상황만 보여줍니다."""
    pass_count = max(1, int(total * pass_ratio + 0.9999))

    st.markdown(f"### 현재 정답 개수: {score}/{total}")
    st.caption(f"답 확인을 누른 문제: {checked}/{total} · 통과 기준: {pass_count}/{total} 이상")

    if checked < total:
        st.info("아직 답 확인을 누르지 않은 문제가 있습니다. 모든 문제의 답 확인을 누르면 통과 여부가 표시됩니다.")
    elif score >= pass_count:
        st.success(f"통과입니다! {score}/{total}개를 맞혔습니다.")
    else:
        st.warning(f"아직 통과 기준에 부족합니다. 다시 풀기를 눌러 한 번 더 도전해 보세요. 현재 점수: {score}/{total}")


# =========================================================
# 지문 읽고 답하기 문제
# =========================================================
pre_reading_questions_bank = {
    "⚽ Ronaldo": [
        ("1. 이 글에서 Ronaldo가 가장 중요하다고 말하는 것은 무엇일까요?", ["Daily habits", "Expensive shoes", "Watching games", "Being famous"], "Daily habits"),
        ("2. Ronaldo가 말한 좋은 습관에 들어가지 않는 것은 무엇일까요?", ["Watching TV all day", "Training", "Sleeping well", "Eating carefully"], "Watching TV all day"),
        ("3. 학생은 왜 Ronaldo를 좋아한다고 말할까요?", ["He is fast, strong, and hardworking", "He is a singer", "He cooks well", "He lives nearby"], "He is fast, strong, and hardworking"),
        ("4. Ronaldo는 작은 루틴이 학생을 어떻게 만든다고 말할까요?", ["Stronger", "Slower", "Sleepier", "Angrier"], "Stronger"),
        ("5. 학생은 가끔 무엇을 잃는다고 말할까요?", ["Confidence", "A textbook", "A phone", "A ticket"], "Confidence"),
        ("6. Ronaldo는 지쳤을 때 어떻게 하라고 말할까요?", ["Rest a little, and then try again", "Give up quickly", "Stop practicing forever", "Blame other people"], "Rest a little, and then try again"),
        ("7. Ronaldo가 말하는 좋은 연습 방법은 무엇일까요?", ["Practice with a clear goal", "Practice without thinking", "Only practice once", "Only copy others"], "Practice with a clear goal"),
        ("8. 이 글의 중심 교훈으로 가장 알맞은 것은 무엇일까요?", ["Believe in yourself and never give up", "Winning is only luck", "Do not make routines", "Talent is the only thing"], "Believe in yourself and never give up"),
    ],
    "🏀 Jordan": [
        ("1. Jordan은 어느 팀과 함께 NBA 챔피언십에서 여섯 번 우승했나요?", ["Chicago Bulls", "LA Lakers", "New York Knicks", "Miami Heat"], "Chicago Bulls"),
        ("2. Jordan은 훌륭한 선수들도 무엇을 겪는다고 말하나요?", ["Failure", "No practice", "Only luck", "No pressure"], "Failure"),
        ("3. Jordan은 실패를 무엇으로 사용할 수 있다고 말하나요?", ["Motivation", "Excuse", "Secret", "Homework"], "Motivation"),
        ("4. 쉬운 슛을 놓친 학생에게 Jordan은 그것이 어떻다고 말하나요?", ["Normal", "Impossible", "Funny", "Dangerous"], "Normal"),
        ("5. 실수한 뒤 해야 할 일로 알맞은 것은 무엇인가요?", ["Think, practice again, and take the next shot with confidence", "Never play again", "Get angry", "Forget practice"], "Think, practice again, and take the next shot with confidence"),
        ("6. 진짜 승부욕의 의미로 알맞은 것은 무엇인가요?", ["Preparation, focus, and responsibility", "Only wanting to win", "Being angry", "Never losing"], "Preparation, focus, and responsibility"),
        ("7. Jordan은 다음 도전을 어떻게 대하라고 말하나요?", ["Never be afraid of it", "Avoid it", "Forget it", "Laugh at it"], "Never be afraid of it"),
        ("8. 이 글의 중심 교훈으로 가장 알맞은 것은 무엇일까요?", ["Learn from failure and keep trying", "Great players never fail", "Mistakes are always bad", "Confidence is not important"], "Learn from failure and keep trying"),
    ],
    "⚽ Son Heung-min": [
        ("1. Son Heung-min은 축구가 무엇만의 경기가 아니라고 말하나요?", ["One player", "One ball", "One school", "One country"], "One player"),
        ("2. 팀에서 중요한 것으로 알맞은 것은 무엇인가요?", ["Respect, communication, and hard work", "Noise, luck, and speed", "Money, games, and phones", "Anger, silence, and fear"], "Respect, communication, and hard work"),
        ("3. 어릴 때 Son의 기본기를 도와준 사람은 누구인가요?", ["His father", "His friend", "His teacher", "His brother"], "His father"),
        ("4. Son이 반복해서 연습한 기본 기술은 무엇인가요?", ["Ball control and shooting", "Cooking and drawing", "Singing and dancing", "Reading and writing"], "Ball control and shooting"),
        ("5. 기본기는 실제 경기에서 무엇이 된다고 말하나요?", ["Power", "Problem", "Noise", "Luck"], "Power"),
        ("6. 팀을 돕는 방법으로 알맞은 것은 무엇인가요?", ["Listen to your teammates and move together", "Ignore teammates", "Play alone only", "Never pass the ball"], "Listen to your teammates and move together"),
        ("7. 좋은 선수는 무엇을 잃지 않는다고 말하나요?", ["Humility", "Anger", "Jealousy", "Laziness"], "Humility"),
        ("8. 이 글의 중심 교훈으로 가장 알맞은 것은 무엇일까요?", ["Discipline, teamwork, and attitude make great players", "Scoring alone is everything", "Basics are not important", "Losing means nothing to learn"], "Discipline, teamwork, and attitude make great players"),
    ],
    "🎤 IU": [
        ("1. 학생은 음악이 자신을 어떻게 만든다고 말하나요?", ["Happy", "Angry", "Tired", "Afraid"], "Happy"),
        ("2. 학생은 어떤 메시지가 있는 노래를 좋아하나요?", ["Warm messages", "Cold messages", "Fast rules", "Difficult numbers"], "Warm messages"),
        ("3. IU는 좋은 노래가 사람들에게 무엇을 줄 수 있다고 말하나요?", ["Comfort", "Homework", "Noise", "Money"], "Comfort"),
        ("4. 감정을 더 잘 표현하려면 무엇에 귀 기울여야 하나요?", ["Your heart", "Your phone", "A machine", "A map"], "Your heart"),
        ("5. IU는 처음에 무엇 하나를 써 보라고 말하나요?", ["One small sentence", "One long book", "One test paper", "One rule"], "One small sentence"),
        ("6. 솔직한 감정은 무엇이 될 수 있나요?", ["Powerful words", "A mistake", "A problem", "A game"], "Powerful words"),
        ("7. IU는 무엇이 사람들에게 닿는다고 말하나요?", ["Sincerity", "Silence", "Speed", "Luck"], "Sincerity"),
        ("8. 이 글의 중심 교훈으로 가장 알맞은 것은 무엇일까요?", ["Express yourself honestly and trust your voice", "Hide your feelings forever", "A song needs no feeling", "Writing is always useless"], "Express yourself honestly and trust your voice"),
    ],
    "⛸️ Kim Yuna": [
        ("1. 학생은 피겨스케이팅이 어떻게 보인다고 말하나요?", ["Beautiful and difficult", "Easy and boring", "Fast and noisy", "Small and simple"], "Beautiful and difficult"),
        ("2. 피겨스케이팅에 필요한 것으로 알맞은 것은 무엇인가요?", ["Balance, practice, and focus", "Only luck", "No practice", "A loud voice"], "Balance, practice, and focus"),
        ("3. Kim Yuna는 중요한 순간 전에 누구나 무엇을 느낄 수 있다고 말하나요?", ["Nervous", "Lazy", "Famous", "Perfect"], "Nervous"),
        ("4. Kim Yuna는 마음을 다스리기 위해 무엇에 집중했나요?", ["What she practiced", "Other people", "Only the result", "Her phone"], "What she practiced"),
        ("5. 시험 전에 걱정이 많은 학생에게 걱정만으로는 어떻다고 말하나요?", ["It does not help", "It is enough", "It is perfect", "It is the goal"], "It does not help"),
        ("6. 긴장될 때 해야 할 일로 알맞은 것은 무엇인가요?", ["Prepare step by step, breathe slowly, and focus on one thing", "Run away", "Forget everything", "Only worry"], "Prepare step by step, breathe slowly, and focus on one thing"),
        ("7. 침착함은 무엇에서 나온다고 말하나요?", ["Practice and trust in yourself", "Noise and luck", "Fear and anger", "Money and phones"], "Practice and trust in yourself"),
        ("8. 이 글의 중심 교훈으로 가장 알맞은 것은 무엇일까요?", ["Preparation helps control nervousness", "Worry is the best answer", "Pressure is impossible to handle", "Growth is not important"], "Preparation helps control nervousness"),
    ],
    "🎤 BTS Jungkook": [
        ("1. 학생은 무엇을 좋아한다고 말하나요?", ["Singing and watching performances", "Cooking and cleaning", "Drawing maps", "Sleeping only"], "Singing and watching performances"),
        ("2. Jungkook은 공연에는 무엇이 많이 필요하다고 말하나요?", ["Practice", "Money", "Homework", "Luck only"], "Practice"),
        ("3. 매일의 작은 연습은 무엇을 만들 수 있나요?", ["A big difference", "A big problem", "No change", "A loud sound"], "A big difference"),
        ("4. 사람들 앞에서 긴장하는 것은 어떻다고 말하나요?", ["Natural", "Wrong", "Impossible", "Strange"], "Natural"),
        ("5. 자신감을 가지기 위한 방법으로 알맞은 것은 무엇인가요?", ["Prepare well, breathe slowly, and focus on the message", "Compare yourself all day", "Give up quickly", "Never practice"], "Prepare well, breathe slowly, and focus on the message"),
        ("6. Jungkook은 재능 외에 무엇이 중요하다고 말하나요?", ["Effort and attitude", "Only height", "Only age", "Only luck"], "Effort and attitude"),
        ("7. Jungkook은 다른 사람과 너무 많이 무엇하지 말라고 말하나요?", ["Compare yourself", "Practice", "Sing", "Improve"], "Compare yourself"),
        ("8. 이 글의 중심 교훈으로 가장 알맞은 것은 무엇일까요?", ["Focus on your own growth and trust your own voice", "Only talented people can grow", "Practice does not matter", "Stage fear never changes"], "Focus on your own growth and trust your own voice"),
    ],
    "🏜️ Grand Canyon": [
        ("1. Grand Canyon은 어느 나라 어느 주에 있나요?", ["Arizona, USA", "Seoul, Korea", "Paris, France", "London, UK"], "Arizona, USA"),
        ("2. Grand Canyon을 보며 학생은 어떻게 느끼나요?", ["Amazed", "Angry", "Bored", "Sleepy"], "Amazed"),
        ("3. Grand Canyon은 무엇에 의해 천천히 만들어졌나요?", ["The Colorado River and erosion", "A machine", "Only people", "A building"], "The Colorado River and erosion"),
        ("4. 물과 같은 작은 힘은 오랜 시간 동안 무엇을 만들 수 있나요?", ["Huge changes", "No change", "Only noise", "A classroom"], "Huge changes"),
        ("5. 알록달록한 암석층은 무엇을 보여 주나요?", ["Different periods of Earth's history", "Only sports history", "A school rule", "Modern fashion"], "Different periods of Earth's history"),
        ("6. 학생은 Grand Canyon을 무엇에 비유하나요?", ["A book made of rocks", "A phone made of glass", "A school made of paper", "A game made of water"], "A book made of rocks"),
        ("7. 학생은 무엇을 보호하고 싶다고 말하나요?", ["Nature", "A phone", "A bus", "A classroom"], "Nature"),
        ("8. 이 글의 중심 교훈으로 가장 알맞은 것은 무엇일까요?", ["Nature has stories, so we should respect it", "Nature changes only in one day", "Rocks have no history", "Water cannot change land"], "Nature has stories, so we should respect it"),
    ],
    "🗽 New York": [
        ("1. New York에는 어떤 사람들이 살고 있나요?", ["People from many cultures", "Only one family", "Only students", "No people"], "People from many cultures"),
        ("2. New York은 종종 어떤 도시라고 불리나요?", ["A global city", "A small village", "A quiet farm", "A desert city"], "A global city"),
        ("3. Global city의 의미로 알맞은 것은 무엇인가요?", ["People, ideas, money, art, and culture from many countries meet", "Only one idea exists", "No culture exists", "Only farmers live there"], "People, ideas, money, art, and culture from many countries meet"),
        ("4. Times Square는 무엇을 보여 준다고 말하나요?", ["Energy", "Silence", "Fear", "Homework"], "Energy"),
        ("5. Statue of Liberty는 무엇을 보여 주나요?", ["Freedom", "Sports", "Food", "Noise"], "Freedom"),
        ("6. 큰 도시의 어려움으로 알맞은 것은 무엇인가요?", ["Life can be fast, expensive, and competitive", "Life is always slow and free", "There is no competition", "Everything is quiet"], "Life can be fast, expensive, and competitive"),
        ("7. Guide는 꿈을 따르려면 무엇을 존중하라고 말하나요?", ["Different cultures", "Only one opinion", "Only money", "Only speed"], "Different cultures"),
        ("8. 이 글의 중심 교훈으로 가장 알맞은 것은 무엇일까요?", ["Stay curious, keep learning, and respect diversity", "Avoid all big cities", "Freedom is not important", "Different cultures are a problem"], "Stay curious, keep learning, and respect diversity"),
    ],
    "🏯 Gyeongbokgung": [
        ("1. Gyeongbokgung은 처음 언제 지어졌나요?", ["1395", "1910", "2020", "1600"], "1395"),
        ("2. Gyeongbokgung은 어느 시대에 지어졌나요?", ["Joseon Dynasty", "Roman Empire", "British Empire", "Modern USA"], "Joseon Dynasty"),
        ("3. Gyeongbokgung은 조선의 어떤 궁궐이었나요?", ["Main royal palace", "Small market", "Old school", "Train station"], "Main royal palace"),
        ("4. Gyeongbokgung이라는 이름의 뜻은 무엇인가요?", ["A palace greatly blessed by heaven", "A house near a river", "A small mountain school", "A market for people"], "A palace greatly blessed by heaven"),
        ("5. Gyeongbokgung은 무엇을 보여 주나요?", ["Korean history, architecture, and royal culture", "Only sports", "Only food", "Only music"], "Korean history, architecture, and royal culture"),
        ("6. 중요한 국가 행사가 열렸던 건물은 무엇인가요?", ["Geunjeongjeon Hall", "Times Square", "Central Park", "Colorado River"], "Geunjeongjeon Hall"),
        ("7. 이런 장소는 우리가 무엇을 기억하도록 도와주나요?", ["The past", "Only homework", "A phone number", "A game rule"], "The past"),
        ("8. 이 글의 중심 교훈으로 가장 알맞은 것은 무엇일까요?", ["Understanding the past can help us build a better future", "History is not useful", "Palaces have no meaning", "Culture should be forgotten"], "Understanding the past can help us build a better future"),
    ],
    "📘 교과서": [
        ("1. 새로 도착한 기계는 무엇이었나요?", ["A new food machine", "A new robot teacher", "A new school bus", "A new library"], "A new food machine"),
        ("2. 글쓴이가 오늘 선택한 음식은 무엇인가요?", ["hamburger", "tteokbokki", "ice cream", "pizza"], "hamburger"),
        ("3. 글쓴이가 선택한 음식에 포함된 영양소 2가지는 무엇인가요?", ["protein and minerals", "sugar and fat", "rice and salt", "water and oil"], "protein and minerals"),
        ("4. 글쓴이는 왜 기분이 들떴나요?", ["다양한 선택지를 위한 버튼을 처음으로 누르게 되었기 때문에", "점심시간이 평소보다 늦게 시작되었기 때문에", "친구가 대신 음식을 골라 주었기 때문에", "내일 시험이 없어졌기 때문에"], "다양한 선택지를 위한 버튼을 처음으로 누르게 되었기 때문에"),
    ],
}


def get_pre_reading_questions(topic_name, data):
    """지문을 읽기 전에 볼 8개의 이해도 문제를 가져옵니다."""
    if topic_name in pre_reading_questions_bank:
        return pre_reading_questions_bank[topic_name]

    base_questions = data.get("questions", [])
    if len(base_questions) >= 8:
        return base_questions[:8]

    # 예비 자료가 부족한 경우에도 화면이 깨지지 않도록 기본 문제를 보충합니다.
    fallback = list(base_questions)
    fallback.append(("이 지문을 읽으며 가장 먼저 확인할 내용은 무엇인가요?", [data.get("title", "Main topic"), "Random topic", "Only grammar", "Only spelling"], data.get("title", "Main topic")))
    fallback.append(("이 지문에서 배울 수 있는 태도로 가장 알맞은 것은 무엇인가요?", ["Read carefully and find key ideas", "Ignore the text", "Guess without reading", "Stop learning"], "Read carefully and find key ideas"))

    while len(fallback) < 8:
        n = len(fallback) + 1
        fallback.append((f"{n}. 지문을 읽으며 핵심 내용을 찾아봅시다.", ["Key idea", "Wrong idea", "No idea", "Unrelated idea"], "Key idea"))

    return fallback[:8]


def show_pre_reading_questions(category, topic_name, data):
    """Reading 본문 바로 위에 지문을 읽고 답할 문제를 표시합니다."""
    pre_questions = get_pre_reading_questions(topic_name, data)
    pre_prefix = f"{category}_{topic_name}_pre_reading_"

    st.markdown(
        '<div class="section-box"><h3>🧭 해당 내용 지문을 읽고 답하세요</h3></div>',
        unsafe_allow_html=True
    )
    st.caption("문제를 먼저 확인한 뒤, 바로 아래 지문을 읽으면서 답을 찾아보세요.")

    if st.button("🔄 지문 문제 다시 풀기", key=f"reset_pre_reading_{category}_{topic_name}", use_container_width=True):
        reset_keys_by_prefix(pre_prefix)
        st.rerun()

    status_keys = []

    for q_idx, (question, options, answer) in enumerate(pre_questions, start=1):
        answer_key = f"{pre_prefix}answer_{q_idx}"
        status_key = f"{pre_prefix}status_{q_idx}"
        option_key = f"{pre_prefix}options_{q_idx}"
        status_keys.append(status_key)

        # 정답이 항상 1번에 나오지 않도록 보기 순서를 문제별로 섞습니다.
        # 단, Streamlit은 버튼을 누를 때마다 rerun되므로 한 번 정해진 보기 순서는 session_state에 저장합니다.
        if option_key not in st.session_state:
            distractors = [opt for opt in options if opt != answer]
            rnd = random.Random(f"pre-reading-{category}-{topic_name}-{q_idx}")
            rnd.shuffle(distractors)

            mixed_options = distractors[:]
            if answer in options:
                # 정답 위치를 2번, 3번, 4번, 1번 순으로 순환 배치합니다.
                answer_position = q_idx % max(1, len(options))
                answer_position = min(answer_position, len(mixed_options))
                mixed_options.insert(answer_position, answer)
            else:
                mixed_options = list(options)
                rnd.shuffle(mixed_options)

            st.session_state[option_key] = mixed_options

        mixed_options = st.session_state[option_key]

        st.markdown(
            f"""
            <div style="margin-top: 14px; margin-bottom: 8px; padding: 15px 17px; border-radius: 20px;
                        border: 1.5px solid #bbf7d0; background: rgba(255,255,255,0.92);
                        box-shadow: 0 4px 12px rgba(15,23,42,0.05);">
                <div style="font-size: 20px; font-weight: 950; color: #166534; line-height: 1.55;">
                    {question}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        selected = st.radio(
            "정답 선택",
            mixed_options,
            key=answer_key,
            horizontal=False,
            label_visibility="collapsed"
        )

        c_check, c_result = st.columns([1.2, 3])
        with c_check:
            if st.button("답 확인", key=f"{pre_prefix}check_{q_idx}", use_container_width=True):
                st.session_state[status_key] = selected == answer
        with c_result:
            if status_key in st.session_state:
                if st.session_state[status_key]:
                    st.success("정답입니다.")
                else:
                    st.error(f"정답: {answer}")

    score = sum(1 for key in status_keys if st.session_state.get(key) is True)
    checked = sum(1 for key in status_keys if key in st.session_state)
    show_pass_status(score, len(status_keys), checked)
    st.markdown("---")



# =========================================================
# 읽기 미션 / 카드 만들기 / 문자 보내기 활동
# =========================================================
story_card_hints = {
    "⚽ Ronaldo": {
        "Name": "Cristiano Ronaldo",
        "Feeling": "focused / hardworking",
        "Problem": "The text gives detailed facts about Ronaldo's country, family, teams, and achievements.",
        "Action": "Read the text carefully and find exact information such as Portugal, Madeira, Hugo, 2008, and 2016.",
        "Result": "Good habits are more important than talent."
    },
    "🏀 Jordan": {
        "Name": "Jordan",
        "Feeling": "nervous / disappointed after mistakes",
        "Problem": "The student misses shots and worries about failure.",
        "Action": "Learn from failure and take the next shot with confidence.",
        "Result": "Failure can become motivation."
    },
    "⚽ Son Heung-min": {
        "Name": "Son Heung-min",
        "Feeling": "angry when losing",
        "Problem": "The student wants to score alone and gets upset.",
        "Action": "Listen to teammates and move together.",
        "Result": "Discipline, teamwork, and attitude make a good player."
    },
    "🎤 IU": {
        "Name": "IU",
        "Feeling": "shy / unsure",
        "Problem": "The student does not know how to express feelings.",
        "Action": "Write one small sentence and express feelings honestly.",
        "Result": "Sincerity can touch people."
    },
    "⛸️ Kim Yuna": {
        "Name": "Kim Yuna",
        "Feeling": "nervous / worried",
        "Problem": "The student worries before an important moment.",
        "Action": "Prepare step by step and focus on one thing.",
        "Result": "Practice and trust can bring calmness."
    },
    "🎤 BTS Jungkook": {
        "Name": "Jungkook",
        "Feeling": "nervous / worried",
        "Problem": "The student feels nervous in front of people.",
        "Action": "Prepare well and focus on the message.",
        "Result": "Keep practicing and trust your own voice."
    },
    "🏜️ Grand Canyon": {
        "Name": "Grand Canyon",
        "Feeling": "amazed",
        "Problem": "The visitor wants to understand how the canyon was made.",
        "Action": "Learn about the Colorado River, erosion, and rock layers.",
        "Result": "We can respect and protect nature more."
    },
    "🗽 New York": {
        "Name": "New York",
        "Feeling": "excited",
        "Problem": "A big city can be fast, expensive, and competitive.",
        "Action": "Stay curious, keep learning, and respect different cultures.",
        "Result": "Many cultures and dreams meet in a global city."
    },
    "🏯 Gyeongbokgung": {
        "Name": "Gyeongbokgung",
        "Feeling": "impressed",
        "Problem": "The visitor wants to understand Korean history and culture.",
        "Action": "Learn about Joseon, the palace, and Geunjeongjeon Hall.",
        "Result": "Understanding the past helps build a better future."
    },
    "📘 교과서": {
        "Name": "The student",
        "Feeling": "impressed / excited",
        "Problem": "Students had to wait in line for lunch before.",
        "Action": "The student tries a new food machine.",
        "Result": "A fast, healthy meal comes out and the student looks forward to tomorrow."
    },
}


def get_story_card_hint(topic_name, data):
    """주제별 카드 만들기 예시를 가져옵니다. 없으면 기본값을 사용합니다."""
    if topic_name in story_card_hints:
        return story_card_hints[topic_name]

    clean_name = topic_name.split(" ", 1)[-1] if " " in topic_name else data.get("title", "Main character")
    return {
        "Name": clean_name,
        "Feeling": "interested / surprised",
        "Problem": "Find the main problem in the reading.",
        "Action": "Find the action or advice in the reading.",
        "Result": "Find the result or lesson in the reading."
    }


def get_message_target(topic_name, data):
    """문자 보내기 활동의 수신자 이름을 정합니다."""
    hint = get_story_card_hint(topic_name, data)
    return hint.get("Name", topic_name.split(" ", 1)[-1])


def show_mission_reading_activity(category, topic_name, data):
    """본문을 읽으면서 찾아야 할 미션을 간단하게 제시합니다."""
    hint = get_story_card_hint(topic_name, data)
    mission_key = f"{category}_{topic_name}_mission_"

    st.markdown(
        """
        <div class="mission-card">
            <div class="mission-title">🧭 Mission 1. 읽으면서 찾기</div>
            <div class="mission-guide">
                아래 5가지를 생각하면서 지문을 읽어 보세요. 답을 길게 쓰지 않아도 됩니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    missions = [
        ("Name", "누가/무엇이 중심인가요?", hint["Name"]),
        ("Feeling", "어떤 감정이 나오나요?", hint["Feeling"]),
        ("Problem", "어떤 문제나 어려움이 있나요?", hint["Problem"]),
        ("Action", "어떤 행동이나 조언이 나오나요?", hint["Action"]),
        ("Result", "마지막 결과나 교훈은 무엇인가요?", hint["Result"]),
    ]

    cols = st.columns(5)
    for idx, (label, question, example) in enumerate(missions):
        with cols[idx]:
            st.checkbox(
                f"{label}",
                key=f"{mission_key}check_{label}",
                help=question
            )
            st.caption(question)
            st.caption(f"예: {example}")


def show_story_card_activity(category, topic_name, data):
    """읽은 내용을 바탕으로 학생이 간단한 내용 카드를 완성합니다."""
    hint = get_story_card_hint(topic_name, data)
    card_key = f"{category}_{topic_name}_story_card_"

    st.markdown('<div class="section-box"><h3>활동 4. 내용 카드 만들기</h3></div>', unsafe_allow_html=True)
    st.caption("지문을 읽고 핵심 내용을 짧게 정리하세요. 영어로 써도 되고, 어려우면 한국어로 써도 됩니다.")

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Name / 중심 인물·대상", placeholder=hint["Name"], key=f"{card_key}name")
        feeling = st.text_input("Feeling / 감정", placeholder=hint["Feeling"], key=f"{card_key}feeling")
        problem = st.text_area("Problem / 문제·어려움", placeholder=hint["Problem"], height=90, key=f"{card_key}problem")
    with c2:
        action = st.text_area("Action / 행동·조언", placeholder=hint["Action"], height=90, key=f"{card_key}action")
        result = st.text_area("Result / 결과·교훈", placeholder=hint["Result"], height=90, key=f"{card_key}result")

    if st.button("📇 카드 완성하기", key=f"{card_key}submit", use_container_width=True):
        st.markdown(
            f"""
            <div class="story-card">
                <div class="story-card-title">📇 My Reading Card</div>
                <div class="message-line"><b>Name:</b> {name.strip() or hint["Name"]}</div>
                <div class="message-line"><b>Feeling:</b> {feeling.strip() or hint["Feeling"]}</div>
                <div class="message-line"><b>Problem:</b> {problem.strip() or hint["Problem"]}</div>
                <div class="message-line"><b>Action:</b> {action.strip() or hint["Action"]}</div>
                <div class="message-line"><b>Result:</b> {result.strip() or hint["Result"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.success("좋아요. 지문 내용을 카드로 정리했습니다.")


def make_message_feedback(line1, line2, target_name):
    """주인공에게 보내는 문자 2줄에 대한 간단한 피드백을 만듭니다."""
    full_text = f"{line1} {line2}".strip()
    if not full_text:
        return "먼저 문자 2줄을 써 보세요.", ""

    answer_lang = detect_language(full_text)
    if answer_lang == "ko":
        korean_feedback = "내용이 잘 전달됩니다. 다음에는 본문에서 나온 핵심 단어를 하나 넣으면 더 좋습니다."
        english_sample = f"Hi {target_name}, I learned a lot from you. I will remember your lesson and try my best."
    else:
        korean_feedback = "영어로 의미가 잘 전달됩니다. 더 자연스럽게 하려면 감사 표현과 앞으로의 다짐을 함께 넣으면 좋습니다."
        english_sample = f"Hi {target_name}, thank you for your advice. I will keep trying and use this lesson in my life."

    return korean_feedback, english_sample


def show_message_to_character_activity(category, topic_name, data):
    """마지막 활동: 주인공에게 문자 2줄 보내기."""
    target_name = get_message_target(topic_name, data)
    msg_key = f"{category}_{topic_name}_message_to_character_"

    st.markdown('<div class="section-box"><h3>활동 5. 주인공에게 문자 2줄 보내기</h3></div>', unsafe_allow_html=True)
    st.caption("지문을 읽고 주인공에게 짧은 문자 2줄을 보내 보세요. 한국어 또는 영어 모두 가능합니다.")

    line1 = st.text_input(
        "1번째 줄",
        placeholder=f"Hi {target_name}, thank you for your advice.",
        key=f"{msg_key}line1"
    )
    line2 = st.text_input(
        "2번째 줄",
        placeholder="I will keep trying and never give up.",
        key=f"{msg_key}line2"
    )

    if st.button("💬 문자 보내기", key=f"{msg_key}submit", use_container_width=True):
        if not line1.strip() and not line2.strip():
            st.warning("먼저 문자 2줄을 적어 주세요.")
        else:
            st.markdown(
                f"""
                <div class="message-card">
                    <div class="story-card-title">💬 To. {target_name}</div>
                    <div class="message-line">1. {line1.strip() or "..."}</div>
                    <div class="message-line">2. {line2.strip() or "..."}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            korean_feedback, english_sample = make_message_feedback(line1, line2, target_name)
            st.markdown("### 🇰🇷 피드백")
            st.info(korean_feedback)
            st.markdown("### 🇺🇸 예시 표현")
            st.success(english_sample)
            direct_tts_player(english_sample, lang="en")


def make_expression_completion_items(data, key_words, max_items=6):
    """활동 3용: 핵심 표현에서 중요한 영어 단어를 하나 비우고 고르게 합니다."""
    stop_words = {
        "the", "a", "an", "and", "or", "but", "to", "of", "in", "on", "at", "for", "with",
        "is", "are", "was", "were", "be", "am", "do", "does", "did", "can", "will", "should",
        "i", "you", "your", "my", "me", "it", "this", "that", "not", "from", "by", "as", "up"
    }

    default_pool = [
        "practice", "confidence", "respect", "focus", "effort", "attitude", "growth", "failure",
        "motivation", "nature", "history", "culture", "healthy", "nutrients", "future", "service",
        "freedom", "teamwork", "sincerity", "training", "goal", "voice", "basics", "routine"
    ]

    pool = []
    for word, meaning in key_words:
        pool.extend(re.findall(r"[A-Za-z][A-Za-z'-]*", str(word)))
    for exp in data.get("key_expressions", []):
        pool.extend(re.findall(r"[A-Za-z][A-Za-z'-]*", str(exp)))
    pool.extend(default_pool)

    cleaned_pool = []
    seen = set()
    for item in pool:
        item_clean = item.strip(".,!?;:()[]{}\"")
        low = item_clean.lower()
        if len(item_clean) >= 3 and low not in stop_words and low not in seen:
            cleaned_pool.append(item_clean)
            seen.add(low)

    items = []
    for exp in data.get("key_expressions", []):
        words = re.findall(r"[A-Za-z][A-Za-z'-]*", str(exp))
        candidates = [w for w in words if len(w) >= 4 and w.lower() not in stop_words]
        if not candidates:
            candidates = [w for w in words if len(w) >= 3 and w.lower() not in stop_words]
        if not candidates:
            continue

        # 짧은 기능어보다 의미어가 비도록 가장 긴 단어를 선택합니다.
        answer = sorted(candidates, key=len, reverse=True)[0]
        blank_sentence = re.sub(rf"\b{re.escape(answer)}\b", "______", str(exp), count=1, flags=re.IGNORECASE)

        distractors = [p for p in cleaned_pool if p.lower() != answer.lower()]
        rnd = random.Random(f"expression-completion-{exp}")
        rnd.shuffle(distractors)
        options = [answer] + distractors[:3]
        rnd.shuffle(options)

        items.append((blank_sentence, options, answer, exp))
        if len(items) >= max_items:
            break

    return items


def make_full_listening_text(dialogue):
    """
    전체 듣기용 텍스트:
    - 한 개의 긴 mp3로 처음부터 끝까지 재생되게 함
    - 음성에서는 화자 이름을 읽지 않음
    - 화자가 바뀔 때 약간 더 쉬도록 문장 사이에 pause 표현을 추가
    """
    parts = []
    previous_speaker = None

    for speaker, eng, kor in dialogue:
        sentence = str(eng).strip()

        if previous_speaker is not None and speaker != previous_speaker:
            # gTTS에서 약간의 쉼을 유도하기 위한 짧은 문장부호
            parts.append(".")

        parts.append(sentence)
        previous_speaker = speaker

    return " ... ".join(parts)



def play_dialogue_sequence_audio(dialogue, key, button_label="🎧 전체 듣기", lang="en"):
    """
    전체 듣기:
    - 화자 이름은 음성에서 읽지 않음
    - 문장별 mp3를 순서대로 재생
    - 화자가 바뀔 때 실제 대기 시간을 넣어 발화 간격을 확실히 늘림
    - 한국어 해석 보기 toggle로 rerun되어도 현재 문장과 재생 위치를 복원
    """
    audio_state_key = f"{key}_playlist"

    if st.button(button_label, use_container_width=True, key=f"{key}_btn"):
        try:
            playlist = []
            for idx, (speaker, eng, kor) in enumerate(dialogue):
                eng_text = str(eng).strip()
                audio_bytes = make_tts(eng_text, lang=lang)
                audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

                next_speaker = dialogue[idx + 1][0] if idx + 1 < len(dialogue) else None

                # 같은 화자가 이어지면 짧게, 화자가 바뀌면 확실히 길게 쉼
                pause_after = 1500 if next_speaker is not None and next_speaker != speaker else 300

                playlist.append({
                    "src": f"data:audio/mp3;base64,{audio_b64}",
                    "pauseAfter": pause_after
                })

            st.session_state[audio_state_key] = playlist

        except Exception as e:
            st.error("음성 파일을 만들지 못했습니다. requirements.txt에 gTTS가 있는지 확인해 주세요.")
            st.caption(f"오류 내용: {e}")

    if audio_state_key in st.session_state:
        playlist = st.session_state[audio_state_key]
        playlist_json = json.dumps(playlist, ensure_ascii=False)
        safe_audio_id = re.sub(r"[^a-zA-Z0-9_]+", "_", str(key))

        components.html(
            f"""
            <div style="width:100%;">
                <audio id="audio_{safe_audio_id}" controls style="width:100%;"></audio>
            </div>

            <script>
            const playlist_{safe_audio_id} = {playlist_json};
            const audio_{safe_audio_id} = document.getElementById("audio_{safe_audio_id}");

            const indexKey_{safe_audio_id} = "seq_audio_index_{safe_audio_id}";
            const timeKey_{safe_audio_id} = "seq_audio_time_{safe_audio_id}";
            const playingKey_{safe_audio_id} = "seq_audio_playing_{safe_audio_id}";

            let currentIndex_{safe_audio_id} = parseInt(localStorage.getItem(indexKey_{safe_audio_id}) || "0");
            if (currentIndex_{safe_audio_id} < 0 || currentIndex_{safe_audio_id} >= playlist_{safe_audio_id}.length) {{
                currentIndex_{safe_audio_id} = 0;
            }}

            let movingNext_{safe_audio_id} = false;
            let endTimer_{safe_audio_id} = null;

            function saveState_{safe_audio_id}() {{
                localStorage.setItem(indexKey_{safe_audio_id}, String(currentIndex_{safe_audio_id}));
                localStorage.setItem(timeKey_{safe_audio_id}, String(audio_{safe_audio_id}.currentTime || 0));
                localStorage.setItem(playingKey_{safe_audio_id}, String(!audio_{safe_audio_id}.paused));
            }}

            function loadTrack_{safe_audio_id}(idx, restoreTime=true, autoplay=false) {{
                currentIndex_{safe_audio_id} = idx;
                localStorage.setItem(indexKey_{safe_audio_id}, String(currentIndex_{safe_audio_id}));

                audio_{safe_audio_id}.src = playlist_{safe_audio_id}[currentIndex_{safe_audio_id}].src;
                audio_{safe_audio_id}.load();

                audio_{safe_audio_id}.onloadedmetadata = () => {{
                    if (restoreTime) {{
                        const savedTime = parseFloat(localStorage.getItem(timeKey_{safe_audio_id}) || "0");
                        if (!Number.isNaN(savedTime) && savedTime > 0 && savedTime < audio_{safe_audio_id}.duration) {{
                            audio_{safe_audio_id}.currentTime = savedTime;
                        }}
                    }} else {{
                        audio_{safe_audio_id}.currentTime = 0;
                    }}

                    if (autoplay) {{
                        audio_{safe_audio_id}.play().catch(() => {{}});
                    }}
                }};
            }}

            loadTrack_{safe_audio_id}(currentIndex_{safe_audio_id}, true, false);

            const wasPlaying_{safe_audio_id} = localStorage.getItem(playingKey_{safe_audio_id});
            if (wasPlaying_{safe_audio_id} === "true") {{
                setTimeout(() => {{
                    audio_{safe_audio_id}.play().catch(() => {{}});
                }}, 350);
            }}

            audio_{safe_audio_id}.addEventListener("timeupdate", () => {{
                localStorage.setItem(timeKey_{safe_audio_id}, String(audio_{safe_audio_id}.currentTime || 0));
            }});

            audio_{safe_audio_id}.addEventListener("play", () => {{
                if (endTimer_{safe_audio_id}) {{
                    clearTimeout(endTimer_{safe_audio_id});
                    endTimer_{safe_audio_id} = null;
                }}
                localStorage.setItem(playingKey_{safe_audio_id}, "true");
            }});

            audio_{safe_audio_id}.addEventListener("pause", () => {{
                if (!movingNext_{safe_audio_id}) {{
                    saveState_{safe_audio_id}();
                    localStorage.setItem(playingKey_{safe_audio_id}, "false");
                }}
            }});

            audio_{safe_audio_id}.addEventListener("ended", () => {{
                localStorage.setItem(timeKey_{safe_audio_id}, "0");

                const delay = playlist_{safe_audio_id}[currentIndex_{safe_audio_id}].pauseAfter || 300;

                if (currentIndex_{safe_audio_id} + 1 < playlist_{safe_audio_id}.length) {{
                    movingNext_{safe_audio_id} = true;
                    localStorage.setItem(playingKey_{safe_audio_id}, "true");

                    endTimer_{safe_audio_id} = setTimeout(() => {{
                        currentIndex_{safe_audio_id} += 1;
                        localStorage.setItem(indexKey_{safe_audio_id}, String(currentIndex_{safe_audio_id}));
                        localStorage.setItem(timeKey_{safe_audio_id}, "0");
                        loadTrack_{safe_audio_id}(currentIndex_{safe_audio_id}, false, true);
                        movingNext_{safe_audio_id} = false;
                    }}, delay);
                }} else {{
                    currentIndex_{safe_audio_id} = 0;
                    localStorage.setItem(indexKey_{safe_audio_id}, "0");
                    localStorage.setItem(timeKey_{safe_audio_id}, "0");
                    localStorage.setItem(playingKey_{safe_audio_id}, "false");
                    loadTrack_{safe_audio_id}(0, false, false);
                }}
            }});

            window.addEventListener("beforeunload", () => {{
                saveState_{safe_audio_id}();
            }});
            </script>
            """,
            height=85,
        )


# =========================================================
# 화면
# =========================================================
st.markdown("""
<div class="main-title">
    <h1>🌸 Fun English Reading 🌿</h1>
    <p>People · Places · Knowledge · English</p>
    <div class="garden-line">🌸 🌱 🌼 🌿 🌷</div>
</div>
""", unsafe_allow_html=True)

col_cat, col_topic = st.columns([1, 2])

with col_cat:
    category = st.selectbox("카테고리", list(data_bank.keys()))

with col_topic:
    topic_name = st.selectbox("주제 선택", list(data_bank[category].keys()))


st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 단순 정보형 지문 자료로 덮어쓰기
# - 모든 인물 지문은 짧은 정보형 본문으로 통일
# - 한국어 해석은 본문에 바로 보여 주지 않음
# - Mission 1은 지문을 읽어야 풀 수 있는 12문제로 구성
# =========================================================
def _info_lines(items):
    return [("Text", en, ko) for en, ko in items]

simple_reading_people = {
    "⚽ Ronaldo": {
        "title": "Cristiano Ronaldo",
        "subtitle": "Country, family, teams, awards, and habits",
        "dialogue": _info_lines([
            ("Cristiano Ronaldo was born in Portugal in 1985.", "크리스티아누 호날두는 1985년에 포르투갈에서 태어났다."),
            ("He grew up on the island of Madeira.", "그는 마데이라섬에서 자랐다."),
            ("He has one brother and two sisters.", "그에게는 남자 형제 한 명과 여자 형제 두 명이 있다."),
            ("His brother's name is Hugo.", "그의 남자 형제 이름은 후고이다."),
            ("His sisters' names are Elma and Katia.", "그의 여자 형제 이름은 엘마와 카티아이다."),
            ("Ronaldo first played for Sporting CP in Portugal.", "호날두는 포르투갈의 스포르팅 CP에서 처음 뛰었다."),
            ("Later, he moved to Manchester United in England.", "나중에 그는 영국의 맨체스터 유나이티드로 이적했다."),
            ("In 2008, he won his first Ballon d'Or.", "2008년에 그는 첫 발롱도르를 받았다."),
            ("In 2016, he won Euro 2016 with Portugal.", "2016년에 그는 포르투갈과 유로 2016에서 우승했다."),
            ("He believes that talent is helpful, but good habits are more important.", "그는 재능도 도움이 되지만 좋은 습관이 더 중요하다고 믿는다."),
        ]),
        "mission_questions": [
            ("1. Ronaldo가 태어난 나라는 어디인가요?", ["Spain", "Brazil", "Portugal", "England"], "Portugal"),
            ("2. Ronaldo가 태어난 해는 언제인가요?", ["1995", "2008", "2016", "1985"], "1985"),
            ("3. Ronaldo가 자란 섬은 어디인가요?", ["Jeju", "Hawaii", "Madeira", "Bali"], "Madeira"),
            ("4. Ronaldo에게는 남자 형제가 몇 명 있나요?", ["Two", "Three", "Four", "One"], "One"),
            ("5. Ronaldo에게는 여자 형제가 몇 명 있나요?", ["One", "Three", "Two", "Four"], "Two"),
            ("6. Ronaldo의 남자 형제 이름은 무엇인가요?", ["Messi", "Bruno", "Pepe", "Hugo"], "Hugo"),
            ("7. Ronaldo의 여자 형제 이름으로 알맞은 것은 무엇인가요?", ["Anna and Maria", "Rose and Lisa", "Elma and Katia", "Sofia and Bella"], "Elma and Katia"),
            ("8. Ronaldo가 처음 뛴 포르투갈 팀은 어디인가요?", ["Manchester United", "Real Madrid", "Juventus", "Sporting CP"], "Sporting CP"),
            ("9. Ronaldo가 나중에 이적한 영국 팀은 어디인가요?", ["Chelsea", "Liverpool", "Manchester United", "Arsenal"], "Manchester United"),
            ("10. Ronaldo가 첫 Ballon d'Or를 받은 해는 언제인가요?", ["2016", "1985", "2008", "2023"], "2008"),
            ("11. Ronaldo가 Portugal과 Euro에서 우승한 해는 언제인가요?", ["2008", "2010", "2018", "2016"], "2016"),
            ("12. Ronaldo가 talent보다 더 중요하다고 믿는 것은 무엇인가요?", ["Expensive shoes", "Famous friends", "Good habits", "Watching games"], "Good habits"),
        ],
        "matching_pairs": [("Ronaldo was born in Portugal.", "호날두는 포르투갈에서 태어났다."), ("He grew up on Madeira.", "그는 마데이라에서 자랐다."), ("He has one brother and two sisters.", "그에게는 남자 형제 한 명과 여자 형제 두 명이 있다."), ("He first played for Sporting CP.", "그는 스포르팅 CP에서 처음 뛰었다."), ("He won his first Ballon d'Or in 2008.", "그는 2008년에 첫 발롱도르를 받았다."), ("Good habits are more important than talent.", "좋은 습관은 재능보다 더 중요하다.")],
        "lie_cards": [("Ronaldo was born in Spain in 1995.", False), ("Ronaldo grew up on Madeira.", True), ("Ronaldo has one brother and two sisters.", True), ("Ronaldo first played for Sporting CP.", True), ("Ronaldo's brother's name is Messi.", False)],
        "reflection_prompt": "Ronaldo의 이야기를 통해 내가 배울 점은 무엇인가요?"
    },
    "🏀 Jordan": {
        "title": "Michael Jordan",
        "subtitle": "Family, team, championships, failure, and effort",
        "dialogue": _info_lines([
            ("Michael Jordan was born in Brooklyn, New York, in 1963.", "마이클 조던은 1963년에 뉴욕 브루클린에서 태어났다."),
            ("He grew up in Wilmington, North Carolina.", "그는 노스캐롤라이나의 윌밍턴에서 자랐다."),
            ("He has two brothers and two sisters.", "그에게는 남자 형제 두 명과 여자 형제 두 명이 있다."),
            ("Jordan played basketball at the University of North Carolina.", "조던은 노스캐롤라이나 대학교에서 농구를 했다."),
            ("In 1982, he made a famous winning shot in the college championship game.", "1982년에 그는 대학 결승전에서 유명한 결승 슛을 넣었다."),
            ("In 1984, he joined the Chicago Bulls.", "1984년에 그는 시카고 불스에 입단했다."),
            ("He won six NBA championships with the Chicago Bulls.", "그는 시카고 불스와 함께 NBA 챔피언십에서 여섯 번 우승했다."),
            ("He wore number 23 for most of his career.", "그는 선수 생활 대부분 동안 23번을 달았다."),
            ("He often said that failure helped him become better.", "그는 실패가 자신을 더 나아지게 했다고 자주 말했다."),
            ("His story shows that mistakes can become motivation.", "그의 이야기는 실수가 동기가 될 수 있음을 보여 준다."),
        ]),
        "mission_questions": [
            ("1. Jordan이 태어난 도시는 어디인가요?", ["Chicago", "Los Angeles", "Brooklyn", "Miami"], "Brooklyn"),
            ("2. Jordan이 자란 곳은 어디인가요?", ["Boston", "Seattle", "Dallas", "Wilmington"], "Wilmington"),
            ("3. Jordan이 태어난 해는 언제인가요?", ["1982", "1984", "1963", "1998"], "1963"),
            ("4. Jordan에게는 남자 형제가 몇 명 있나요?", ["One", "Three", "Four", "Two"], "Two"),
            ("5. Jordan에게는 여자 형제가 몇 명 있나요?", ["One", "Three", "Two", "Four"], "Two"),
            ("6. Jordan이 대학 농구를 한 학교는 어디인가요?", ["Harvard University", "Stanford University", "Oxford University", "University of North Carolina"], "University of North Carolina"),
            ("7. Jordan이 대학 결승전에서 유명한 결승 슛을 넣은 해는 언제인가요?", ["1963", "1984", "1982", "1996"], "1982"),
            ("8. Jordan이 Chicago Bulls에 입단한 해는 언제인가요?", ["1982", "1991", "2008", "1984"], "1984"),
            ("9. Jordan은 Chicago Bulls와 NBA에서 몇 번 우승했나요?", ["Two", "Three", "Six", "Ten"], "Six"),
            ("10. Jordan이 주로 달았던 등번호는 무엇인가요?", ["7", "10", "30", "23"], "23"),
            ("11. Jordan은 실패가 자신을 어떻게 만들었다고 말했나요?", ["weaker", "slower", "better", "sleepier"], "better"),
            ("12. Jordan의 이야기가 보여 주는 것은 무엇인가요?", ["Failure is always the end", "Practice is not useful", "Mistakes can become motivation", "Winning is only luck"], "Mistakes can become motivation"),
        ],
        "matching_pairs": [("Jordan was born in Brooklyn.", "조던은 브루클린에서 태어났다."), ("He grew up in Wilmington.", "그는 윌밍턴에서 자랐다."), ("He joined the Chicago Bulls in 1984.", "그는 1984년에 시카고 불스에 입단했다."), ("He won six NBA championships.", "그는 NBA에서 여섯 번 우승했다."), ("He wore number 23.", "그는 23번을 달았다."), ("Mistakes can become motivation.", "실수는 동기가 될 수 있다.")],
        "lie_cards": [("Jordan was born in Brooklyn in 1963.", True), ("Jordan grew up in Wilmington.", True), ("Jordan has one brother and three sisters.", False), ("Jordan joined the Chicago Bulls in 1984.", True), ("Jordan won three NBA championships.", False)],
        "reflection_prompt": "Jordan의 이야기를 통해 내가 배울 점은 무엇인가요?"
    },
    "⚽ Son Heung-min": {
        "title": "Son Heung-min",
        "subtitle": "Birthplace, training, teams, captaincy, and teamwork",
        "dialogue": _info_lines([
            ("Son Heung-min was born in Chuncheon, South Korea, in 1992.", "손흥민은 1992년에 대한민국 춘천에서 태어났다."),
            ("His father, Son Woong-jung, helped him train when he was young.", "그의 아버지 손웅정은 그가 어릴 때 훈련을 도왔다."),
            ("Son practiced basic skills again and again.", "손흥민은 기본 기술을 반복해서 연습했다."),
            ("He moved to Germany as a young player.", "그는 어린 선수 시절 독일로 갔다."),
            ("He played for Hamburger SV and Bayer Leverkusen in Germany.", "그는 독일에서 함부르크 SV와 바이어 레버쿠젠에서 뛰었다."),
            ("In 2015, he moved to Tottenham Hotspur in England.", "2015년에 그는 영국의 토트넘 홋스퍼로 이적했다."),
            ("In 2022, he won the Premier League Golden Boot.", "2022년에 그는 프리미어리그 득점왕을 차지했다."),
            ("He became the captain of the South Korean national team.", "그는 대한민국 국가대표팀의 주장이 되었다."),
            ("He is known for speed, finishing, and teamwork.", "그는 속도, 마무리 능력, 팀워크로 알려져 있다."),
            ("His story shows that basics and discipline are important.", "그의 이야기는 기본기와 절제가 중요하다는 것을 보여 준다."),
        ]),
        "mission_questions": [
            ("1. Son Heung-min이 태어난 도시는 어디인가요?", ["Seoul", "Busan", "Chuncheon", "Daegu"], "Chuncheon"),
            ("2. Son Heung-min이 태어난 해는 언제인가요?", ["1985", "2015", "2022", "1992"], "1992"),
            ("3. 어릴 때 Son의 훈련을 도운 사람은 누구인가요?", ["His friend", "His coach in England", "His father", "His brother"], "His father"),
            ("4. Son이 반복해서 연습한 것은 무엇인가요?", ["Singing", "Cooking", "Painting", "Basic skills"], "Basic skills"),
            ("5. Son은 어린 선수 시절 어느 나라로 갔나요?", ["England", "Spain", "Germany", "France"], "Germany"),
            ("6. Son이 독일에서 뛴 팀으로 알맞은 것은 무엇인가요?", ["Tottenham and Arsenal", "Hamburger SV and Bayer Leverkusen", "Seoul and Jeju", "Barcelona and Real Madrid"], "Hamburger SV and Bayer Leverkusen"),
            ("7. Son이 Tottenham Hotspur로 이적한 해는 언제인가요?", ["1992", "2022", "2015", "2008"], "2015"),
            ("8. Son이 2022년에 받은 상은 무엇인가요?", ["Ballon d'Or", "NBA championship", "Golden Boot", "Grammy Award"], "Golden Boot"),
            ("9. Son은 어느 국가대표팀의 주장이 되었나요?", ["Japan", "England", "Brazil", "South Korea"], "South Korea"),
            ("10. Son이 알려진 특징으로 알맞은 것은 무엇인가요?", ["Cooking and painting", "Speed, finishing, and teamwork", "Only singing", "Dancing and acting"], "Speed, finishing, and teamwork"),
            ("11. Son의 이야기가 보여 주는 중요한 것은 무엇인가요?", ["Money and luck", "Fear and anger", "Basics and discipline", "Only talent"], "Basics and discipline"),
            ("12. 이 글의 중심 인물은 누구인가요?", ["Ronaldo", "Jordan", "IU", "Son Heung-min"], "Son Heung-min"),
        ],
        "matching_pairs": [("Son was born in Chuncheon.", "손흥민은 춘천에서 태어났다."), ("His father helped him train.", "그의 아버지는 훈련을 도왔다."), ("He moved to Germany as a young player.", "그는 어린 선수 시절 독일로 갔다."), ("He moved to Tottenham in 2015.", "그는 2015년에 토트넘으로 이적했다."), ("He won the Golden Boot in 2022.", "그는 2022년에 득점왕을 차지했다."), ("Basics and discipline are important.", "기본기와 절제가 중요하다.")],
        "lie_cards": [("Son was born in Chuncheon in 1992.", True), ("His father helped him train.", True), ("Son first moved to Canada as a young player.", False), ("He moved to Tottenham in 2015.", True), ("Son is known only for cooking.", False)],
        "reflection_prompt": "Son Heung-min의 이야기를 통해 내가 배울 점은 무엇인가요?"
    },
    "🎤 IU": {
        "title": "IU",
        "subtitle": "Name, debut, music, lyrics, and sincere expression",
        "dialogue": _info_lines([
            ("IU's real name is Lee Ji-eun.", "아이유의 본명은 이지은이다."),
            ("She was born in Seoul, South Korea, in 1993.", "그녀는 1993년에 대한민국 서울에서 태어났다."),
            ("She debuted as a singer in 2008.", "그녀는 2008년에 가수로 데뷔했다."),
            ("Her stage name IU means I and You.", "그녀의 예명 IU는 나와 너를 뜻한다."),
            ("She became known for her clear voice and emotional songs.", "그녀는 맑은 목소리와 감성적인 노래로 알려지게 되었다."),
            ("IU also writes lyrics and tells stories through music.", "아이유는 가사를 쓰고 음악을 통해 이야기를 전하기도 한다."),
            ("Many people like her warm messages.", "많은 사람들은 그녀의 따뜻한 메시지를 좋아한다."),
            ("She has also acted in dramas.", "그녀는 드라마에서 연기하기도 했다."),
            ("Her story shows that sincere feelings can become powerful words.", "그녀의 이야기는 진심 어린 감정이 힘 있는 말이 될 수 있음을 보여 준다."),
            ("She teaches us to trust our own voice.", "그녀는 우리 자신의 목소리를 믿으라고 가르친다."),
        ]),
        "mission_questions": [
            ("1. IU의 본명은 무엇인가요?", ["Kim Ji-soo", "Park Min-young", "Lee Ji-eun", "Choi Yu-na"], "Lee Ji-eun"),
            ("2. IU가 태어난 도시는 어디인가요?", ["Busan", "Daegu", "Incheon", "Seoul"], "Seoul"),
            ("3. IU가 태어난 해는 언제인가요?", ["2008", "2013", "1993", "2023"], "1993"),
            ("4. IU가 가수로 데뷔한 해는 언제인가요?", ["1993", "2016", "2023", "2008"], "2008"),
            ("5. IU라는 예명은 무엇을 뜻하나요?", ["Ice and Umbrella", "I and You", "Inside Universe", "In Unit"], "I and You"),
            ("6. IU는 무엇으로 알려졌나요?", ["Fast running", "Clear voice and emotional songs", "Basketball shots", "Only cooking"], "Clear voice and emotional songs"),
            ("7. IU가 음악을 통해 하는 일은 무엇인가요?", ["Hides stories", "Writes lyrics and tells stories", "Stops singing", "Draws maps"], "Writes lyrics and tells stories"),
            ("8. 많은 사람들이 IU의 무엇을 좋아하나요?", ["Cold rules", "Loud noise", "Warm messages", "Sports records"], "Warm messages"),
            ("9. IU가 음악 외에 한 활동은 무엇인가요?", ["Acted in dramas", "Played in the NBA", "Worked as a pilot", "Won Euro 2016"], "Acted in dramas"),
            ("10. IU의 이야기는 sincere feelings가 무엇이 될 수 있음을 보여 주나요?", ["A problem", "A mistake", "Powerful words", "A secret"], "Powerful words"),
            ("11. IU는 우리에게 무엇을 믿으라고 가르치나요?", ["Only luck", "Money", "Other people only", "Our own voice"], "Our own voice"),
            ("12. 이 글의 중심 인물은 누구인가요?", ["Kim Yuna", "Jordan", "IU", "Ronaldo"], "IU"),
        ],
        "matching_pairs": [("IU's real name is Lee Ji-eun.", "아이유의 본명은 이지은이다."), ("She debuted in 2008.", "그녀는 2008년에 데뷔했다."), ("IU means I and You.", "IU는 나와 너를 뜻한다."), ("She writes lyrics.", "그녀는 가사를 쓴다."), ("Sincere feelings can become powerful words.", "진심 어린 감정은 힘 있는 말이 될 수 있다."), ("Trust your own voice.", "너 자신의 목소리를 믿어라.")],
        "lie_cards": [("IU's real name is Lee Ji-eun.", True), ("IU was born in Seoul in 1993.", True), ("IU debuted as a singer in 2018.", False), ("IU means I and You.", True), ("IU is famous only for basketball.", False)],
        "reflection_prompt": "IU의 이야기를 통해 내가 배울 점은 무엇인가요?"
    },
    "⛸️ Kim Yuna": {
        "title": "Kim Yuna",
        "subtitle": "Birthplace, skating, medals, pressure, and calmness",
        "dialogue": _info_lines([
            ("Kim Yuna was born in Bucheon, South Korea, in 1990.", "김연아는 1990년에 대한민국 부천에서 태어났다."),
            ("She started figure skating when she was six years old.", "그녀는 여섯 살 때 피겨스케이팅을 시작했다."),
            ("She practiced jumps, spins, and balance for many years.", "그녀는 여러 해 동안 점프, 스핀, 균형을 연습했다."),
            ("In 2010, she won the gold medal at the Vancouver Winter Olympics.", "2010년에 그녀는 밴쿠버 동계 올림픽에서 금메달을 땄다."),
            ("In 2014, she won the silver medal at the Sochi Winter Olympics.", "2014년에 그녀는 소치 동계 올림픽에서 은메달을 땄다."),
            ("Many people called her Queen Yuna.", "많은 사람들은 그녀를 퀸연아라고 불렀다."),
            ("She was famous for graceful movement and strong technique.", "그녀는 우아한 움직임과 강한 기술로 유명했다."),
            ("Before competitions, she focused on her training.", "경기 전 그녀는 자신의 훈련에 집중했다."),
            ("Her story shows that preparation can make the mind calmer.", "그녀의 이야기는 준비가 마음을 더 침착하게 만들 수 있음을 보여 준다."),
            ("She teaches us to trust steady practice.", "그녀는 꾸준한 연습을 믿으라고 가르친다."),
        ]),
        "mission_questions": [
            ("1. Kim Yuna가 태어난 도시는 어디인가요?", ["Seoul", "Daegu", "Bucheon", "Busan"], "Bucheon"),
            ("2. Kim Yuna가 태어난 해는 언제인가요?", ["2010", "2014", "1990", "2008"], "1990"),
            ("3. Kim Yuna는 몇 살 때 피겨스케이팅을 시작했나요?", ["Four", "Five", "Seven", "Six"], "Six"),
            ("4. Kim Yuna가 오랫동안 연습한 것으로 알맞은 것은 무엇인가요?", ["Cooking and singing", "Jumps, spins, and balance", "Soccer and tennis", "Painting and writing"], "Jumps, spins, and balance"),
            ("5. Kim Yuna가 Vancouver Winter Olympics에서 금메달을 딴 해는 언제인가요?", ["1990", "2014", "2010", "2022"], "2010"),
            ("6. Kim Yuna가 Sochi Winter Olympics에서 은메달을 딴 해는 언제인가요?", ["2010", "1990", "2020", "2014"], "2014"),
            ("7. 많은 사람들은 Kim Yuna를 무엇이라고 불렀나요?", ["Captain Yuna", "Teacher Yuna", "Queen Yuna", "Singer Yuna"], "Queen Yuna"),
            ("8. Kim Yuna가 유명했던 특징은 무엇인가요?", ["Only speed", "Graceful movement and strong technique", "Cooking skills", "Loud singing"], "Graceful movement and strong technique"),
            ("9. 경기 전 Kim Yuna는 무엇에 집중했나요?", ["Other people", "Her phone", "Her training", "Only luck"], "Her training"),
            ("10. Kim Yuna의 이야기는 preparation이 마음을 어떻게 만들 수 있음을 보여 주나요?", ["Angrier", "Sleepier", "Calmer", "Weaker"], "Calmer"),
            ("11. Kim Yuna는 우리에게 무엇을 믿으라고 가르치나요?", ["Steady practice", "Only luck", "Noise", "Fear"], "Steady practice"),
            ("12. 이 글의 중심 인물은 누구인가요?", ["IU", "Jungkook", "Kim Yuna", "Jordan"], "Kim Yuna"),
        ],
        "matching_pairs": [("Kim Yuna was born in Bucheon.", "김연아는 부천에서 태어났다."), ("She started skating at six.", "그녀는 여섯 살 때 스케이트를 시작했다."), ("She won gold in 2010.", "그녀는 2010년에 금메달을 땄다."), ("She won silver in 2014.", "그녀는 2014년에 은메달을 땄다."), ("She focused on her training.", "그녀는 자신의 훈련에 집중했다."), ("Preparation can make the mind calmer.", "준비는 마음을 더 침착하게 만들 수 있다.")],
        "lie_cards": [("Kim Yuna was born in Bucheon in 1990.", True), ("She started figure skating when she was six.", True), ("She won gold at the Vancouver Winter Olympics in 2010.", True), ("She won silver at the Sochi Winter Olympics in 2020.", False), ("She trusted only luck before competitions.", False)],
        "reflection_prompt": "Kim Yuna의 이야기를 통해 내가 배울 점은 무엇인가요?"
    },
    "🎤 BTS Jungkook": {
        "title": "BTS Jungkook",
        "subtitle": "Birthplace, group, songs, practice, and growth",
        "dialogue": _info_lines([
            ("Jungkook was born in Busan, South Korea, in 1997.", "정국은 1997년에 대한민국 부산에서 태어났다."),
            ("His full name is Jeon Jung-kook.", "그의 전체 이름은 전정국이다."),
            ("He is a member of BTS.", "그는 BTS의 멤버이다."),
            ("BTS debuted in 2013.", "BTS는 2013년에 데뷔했다."),
            ("Jungkook is known for singing, dancing, and stage performances.", "정국은 노래, 춤, 무대 공연으로 알려져 있다."),
            ("He practiced often to improve his skills.", "그는 기술을 향상시키기 위해 자주 연습했다."),
            ("In 2023, he released the song Seven.", "2023년에 그는 Seven이라는 노래를 발표했다."),
            ("In 2023, he also released his solo album Golden.", "2023년에 그는 솔로 앨범 Golden도 발표했다."),
            ("Many fans like his clear voice and energetic performances.", "많은 팬들은 그의 맑은 목소리와 에너지 넘치는 공연을 좋아한다."),
            ("His story shows that effort and attitude are important.", "그의 이야기는 노력과 태도가 중요하다는 것을 보여 준다."),
        ]),
        "mission_questions": [
            ("1. Jungkook이 태어난 도시는 어디인가요?", ["Seoul", "Daegu", "Busan", "Incheon"], "Busan"),
            ("2. Jungkook이 태어난 해는 언제인가요?", ["2013", "2023", "1993", "1997"], "1997"),
            ("3. Jungkook의 전체 이름은 무엇인가요?", ["Kim Nam-joon", "Park Ji-min", "Jeon Jung-kook", "Min Yoon-gi"], "Jeon Jung-kook"),
            ("4. Jungkook은 어떤 그룹의 멤버인가요?", ["Blackpink", "NewJeans", "EXO", "BTS"], "BTS"),
            ("5. BTS가 데뷔한 해는 언제인가요?", ["1997", "2023", "2013", "2008"], "2013"),
            ("6. Jungkook은 무엇으로 알려져 있나요?", ["Soccer and tennis", "Cooking and fishing", "Singing, dancing, and stage performances", "Only acting"], "Singing, dancing, and stage performances"),
            ("7. Jungkook은 왜 자주 연습했나요?", ["To sleep more", "To avoid music", "To stop dancing", "To improve his skills"], "To improve his skills"),
            ("8. Jungkook이 2023년에 발표한 노래는 무엇인가요?", ["Good Day", "Imagine", "Seven", "Dynamite"], "Seven"),
            ("9. Jungkook이 2023년에 발표한 솔로 앨범은 무엇인가요?", ["Palette", "Thriller", "Purpose", "Golden"], "Golden"),
            ("10. 많은 팬들은 Jungkook의 무엇을 좋아하나요?", ["Only quiet reading", "Basketball shots", "Clear voice and energetic performances", "Painting skills"], "Clear voice and energetic performances"),
            ("11. Jungkook의 이야기는 무엇이 중요하다는 것을 보여 주나요?", ["Money and height", "Fear and anger", "Effort and attitude", "Only talent"], "Effort and attitude"),
            ("12. 이 글의 중심 인물은 누구인가요?", ["Jordan", "IU", "Kim Yuna", "BTS Jungkook"], "BTS Jungkook"),
        ],
        "matching_pairs": [("Jungkook was born in Busan.", "정국은 부산에서 태어났다."), ("His full name is Jeon Jung-kook.", "그의 전체 이름은 전정국이다."), ("BTS debuted in 2013.", "BTS는 2013년에 데뷔했다."), ("He released Seven in 2023.", "그는 2023년에 Seven을 발표했다."), ("He released Golden in 2023.", "그는 2023년에 Golden을 발표했다."), ("Effort and attitude are important.", "노력과 태도가 중요하다.")],
        "lie_cards": [("Jungkook was born in Busan in 1997.", True), ("His full name is Jeon Jung-kook.", True), ("BTS debuted in 2003.", False), ("Jungkook released Seven in 2023.", True), ("His story shows that effort is not important.", False)],
        "reflection_prompt": "Jungkook의 이야기를 통해 내가 배울 점은 무엇인가요?"
    }
}
# 인물 자료 덮어쓰기
if "인물" in data_bank:
    for _topic, _new in simple_reading_people.items():
        if _topic in data_bank["인물"]:
            data_bank["인물"][_topic].update(_new)

# 핵심 표현은 고유명사/날짜가 아니라 품사별 중요 어휘 중심으로 학습
key_word_bank.update({
    "⚽ Ronaldo": [("talent", "재능 · 명사"), ("habit", "습관 · 명사"), ("routine", "규칙적인 습관 · 명사"), ("practice", "연습하다 / 연습 · 동사/명사"), ("focus", "집중하다 / 집중 · 동사/명사"), ("strong", "강한 · 형용사"), ("helpful", "도움이 되는 · 형용사"), ("important", "중요한 · 형용사"), ("carefully", "조심스럽게 · 부사"), ("later", "나중에 · 부사")],
    "🏀 Jordan": [("failure", "실패 · 명사"), ("mistake", "실수 · 명사"), ("motivation", "동기 · 명사"), ("confidence", "자신감 · 명사"), ("focus", "집중 · 명사"), ("compete", "경쟁하다 · 동사"), ("practice", "연습하다 · 동사"), ("famous", "유명한 · 형용사"), ("strong", "강한 · 형용사"), ("again", "다시 · 부사")],
    "⚽ Son Heung-min": [("skill", "기술 · 명사"), ("basic", "기본적인 · 형용사"), ("teamwork", "팀워크 · 명사"), ("captain", "주장 · 명사"), ("respect", "존중하다 / 존중 · 동사/명사"), ("train", "훈련하다 · 동사"), ("move", "이적하다 / 이동하다 · 동사"), ("steady", "꾸준한 · 형용사"), ("young", "어린 · 형용사"), ("again and again", "반복해서 · 부사구")],
    "🎤 IU": [("voice", "목소리 · 명사"), ("feeling", "감정 · 명사"), ("lyrics", "가사 · 명사"), ("message", "메시지 · 명사"), ("express", "표현하다 · 동사"), ("trust", "믿다 · 동사"), ("clear", "맑은 / 분명한 · 형용사"), ("emotional", "감성적인 · 형용사"), ("sincere", "진심 어린 · 형용사"), ("warmly", "따뜻하게 · 부사")],
    "⛸️ Kim Yuna": [("balance", "균형 · 명사"), ("pressure", "압박감 · 명사"), ("training", "훈련 · 명사"), ("growth", "성장 · 명사"), ("prepare", "준비하다 · 동사"), ("focus", "집중하다 · 동사"), ("graceful", "우아한 · 형용사"), ("calm", "침착한 · 형용사"), ("steadily", "꾸준히 · 부사"), ("slowly", "천천히 · 부사")],
    "🎤 BTS Jungkook": [("performance", "공연 · 명사"), ("skill", "기술 · 명사"), ("effort", "노력 · 명사"), ("attitude", "태도 · 명사"), ("improve", "향상시키다 · 동사"), ("release", "발표하다 · 동사"), ("energetic", "에너지 넘치는 · 형용사"), ("clear", "맑은 · 형용사"), ("often", "자주 · 부사"), ("step by step", "차근차근 · 부사구")],
})

data = data_bank[category][topic_name]
dialogue = data["dialogue"]
st.markdown(f"""
<div class="info-card">
    <h2>🌿 {data["title"]}</h2>
    <p>{data["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)



# =========================================================
# 새 Reading 흐름 활동: 미션 객관식 → 순서 맞추기 → 거짓말 찾기 → 단어 테스트 → 편지쓰기
# =========================================================
def _stable_shuffle(items, seed_text):
    items = list(items)
    rnd = random.Random(seed_text)
    rnd.shuffle(items)
    return items


story_card_hints_ko = {
    "⚽ Ronaldo": {
        "Name": "크리스티아누 호날두",
        "Feeling": "집중함 / 성실함",
        "Problem": "본문에는 호날두의 출생 국가, 가족, 팀, 우승 연도 같은 세부 정보가 나온다.",
        "Action": "Portugal, Madeira, Hugo, 2008, 2016 같은 정확한 정보를 찾아 읽는다.",
        "Result": "재능도 도움이 되지만 좋은 습관이 더 중요하다."
    },
    "🏀 Jordan": {
        "Name": "조던",
        "Feeling": "실수 뒤 긴장함 / 실망함",
        "Problem": "학생은 슛을 놓치고 실패를 걱정한다.",
        "Action": "실패에서 배우고 자신 있게 다음 슛을 던진다.",
        "Result": "실패는 동기가 될 수 있다."
    },
    "⚽ Son Heung-min": {
        "Name": "손흥민",
        "Feeling": "질 때 화가 남",
        "Problem": "학생은 혼자 골을 넣고 싶어 하고 질 때 속상해한다.",
        "Action": "팀 동료의 말을 듣고 함께 움직인다.",
        "Result": "훈련, 팀워크, 태도가 좋은 선수를 만든다."
    },
    "🎤 IU": {
        "Name": "아이유",
        "Feeling": "부끄러움 / 확신이 없음",
        "Problem": "학생은 감정을 어떻게 표현해야 할지 모른다.",
        "Action": "짧은 문장 하나를 쓰고 감정을 솔직하게 표현한다.",
        "Result": "진심은 사람들의 마음에 닿을 수 있다."
    },
    "⛸️ Kim Yuna": {
        "Name": "김연아",
        "Feeling": "긴장함 / 걱정함",
        "Problem": "학생은 중요한 순간 전에 걱정한다.",
        "Action": "차근차근 준비하고 한 번에 하나에 집중한다.",
        "Result": "연습과 믿음은 침착함을 가져올 수 있다."
    },
    "🎤 BTS Jungkook": {
        "Name": "정국",
        "Feeling": "긴장함 / 걱정함",
        "Problem": "학생은 사람들 앞에서 긴장한다.",
        "Action": "잘 준비하고 전하고 싶은 메시지에 집중한다.",
        "Result": "계속 연습하고 자신의 목소리를 믿는다."
    },
    "🏜️ Grand Canyon": {
        "Name": "그랜드캐니언",
        "Feeling": "경이로움",
        "Problem": "방문자는 협곡이 어떻게 만들어졌는지 알고 싶어 한다.",
        "Action": "콜로라도강, 침식, 암석층에 대해 배운다.",
        "Result": "우리는 자연을 더 존중하고 보호할 수 있다."
    },
    "🗽 New York": {
        "Name": "뉴욕",
        "Feeling": "신남",
        "Problem": "큰 도시는 빠르고 비싸며 경쟁적일 수 있다.",
        "Action": "호기심을 갖고 계속 배우며 다양한 문화를 존중한다.",
        "Result": "세계적인 도시에서 많은 문화와 꿈이 만난다."
    },
    "🏯 Gyeongbokgung": {
        "Name": "경복궁",
        "Feeling": "인상 깊음",
        "Problem": "방문자는 한국의 역사와 문화를 이해하고 싶어 한다.",
        "Action": "조선, 궁궐, 근정전에 대해 배운다.",
        "Result": "과거를 이해하면 더 나은 미래를 만들 수 있다."
    },
    "📘 교과서": {
        "Name": "학생",
        "Feeling": "인상 깊음 / 신남",
        "Problem": "학생들은 전에는 점심시간에 줄을 서서 기다려야 했다.",
        "Action": "학생은 새로운 음식 기계를 사용해 본다.",
        "Result": "빠르고 건강한 식사가 나오고 학생은 내일을 기대한다."
    },
}


def _ko_hint(topic_name, field):
    return story_card_hints_ko.get(topic_name, {}).get(field, '')


def _bi_option(topic_name, field, english_text):
    korean_text = _ko_hint(topic_name, field)
    if korean_text:
        return f"{english_text} ({korean_text})"
    return str(english_text)


def show_mission_preview(category, topic_name, data):
    """지문을 읽기 전에 오늘의 미션을 먼저 보여줍니다."""
    st.markdown(
        """
        <div class="mission-card">
            <div class="mission-title">🧭 Mission 1. 읽으면서 찾기</div>
            <div class="mission-guide">
                아래 5가지를 생각하면서 지문을 읽어 보세요. 읽은 뒤 바로 아래에서 4지선다 문제를 풉니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    mission_items = [
        "1. 중심 인물 또는 중심 대상은 누구/무엇인가요?",
        "2. 글 속 인물은 어떤 감정을 느끼나요?",
        "3. 어떤 문제나 어려움이 나오나요?",
        "4. 어떤 행동이나 조언이 나오나요?",
        "5. 마지막 결과나 교훈은 무엇인가요?",
    ]
    for item in mission_items:
        st.markdown(f"<div class='expression'>{item}</div>", unsafe_allow_html=True)


mission1_questions_bank = {
    "⚽ Ronaldo": [
        ("1. Ronaldo는 어느 나라에서 태어났나요?", ["Spain", "Portugal", "Brazil", "England"], "Portugal"),
        ("2. Ronaldo는 몇 년에 태어났나요?", ["1985", "1995", "2008", "2016"], "1985"),
        ("3. Ronaldo는 어느 섬에서 자랐나요?", ["Jeju", "Madeira", "Hawaii", "Bali"], "Madeira"),
        ("4. Ronaldo의 가족 설명으로 맞는 것은 무엇인가요?", ["One brother and two sisters", "Two brothers and one sister", "Three brothers", "Three sisters"], "One brother and two sisters"),
        ("5. Ronaldo의 남자 형제 이름은 무엇인가요?", ["Hugo", "Messi", "Bruno", "Pepe"], "Hugo"),
        ("6. Ronaldo가 처음 뛴 포르투갈 축구팀은 어디인가요?", ["Sporting CP", "Manchester United", "Real Madrid", "Juventus"], "Sporting CP"),
        ("7. Ronaldo는 나중에 어느 나라의 Manchester United로 이적했나요?", ["Spain", "Portugal", "England", "France"], "England"),
        ("8. Ronaldo가 첫 Ballon d'Or를 받은 해는 언제인가요?", ["1985", "2008", "2016", "2023"], "2008"),
        ("9. Ronaldo가 Manchester United와 함께 Champions League에서 우승한 해는 언제인가요?", ["2002", "2008", "2016", "2018"], "2008"),
        ("10. Ronaldo가 Portugal과 함께 Euro 대회에서 우승한 해는 언제인가요?", ["2008", "2010", "2016", "2018"], "2016"),
        ("11. Ronaldo는 talent보다 무엇이 더 중요하다고 말하나요?", ["Money", "Luck", "Good habits", "Famous friends"], "Good habits"),
    ],
    "🏀 Jordan": [
        ("1. Jordan은 어느 팀과 함께 NBA에서 여섯 번 우승했나요?", ["시카고 불스", "LA 레이커스", "마이애미 히트", "뉴욕 닉스"], "시카고 불스"),
        ("2. Jordan은 훌륭한 선수들도 무엇을 겪는다고 말하나요?", ["실패", "연습 없음", "항상 쉬운 경기", "항상 행운"], "실패"),
        ("3. Jordan은 실패를 무엇으로 사용할 수 있다고 말하나요?", ["동기", "핑계", "비밀", "숙제"], "동기"),
        ("4. 쉬운 슛을 놓친 학생에게 Jordan은 그것이 어떻다고 말하나요?", ["자연스러운 일", "절대 일어나면 안 되는 일", "운동을 그만둘 이유", "웃긴 일"], "자연스러운 일"),
        ("5. Jordan이 말한 진짜 승부욕의 의미는 무엇인가요?", ["준비, 집중, 책임감", "화내기, 소리치기, 이기기", "운, 돈, 유명함", "혼자만 잘하기"], "준비, 집중, 책임감"),
    ],
    "⚽ Son Heung-min": [
        ("1. 손흥민은 축구가 무엇만의 경기가 아니라고 말하나요?", ["한 사람", "한 공", "한 학교", "한 나라"], "한 사람"),
        ("2. 손흥민이 팀에서 중요하다고 말한 것은 무엇인가요?", ["존중, 소통, 노력", "운, 소음, 속도", "휴대폰, 게임, 돈", "분노, 침묵, 두려움"], "존중, 소통, 노력"),
        ("3. 손흥민이 어릴 때 기본기를 만들도록 도와준 사람은 누구인가요?", ["아버지", "친구", "영화감독", "요리사"], "아버지"),
        ("4. 손흥민이 반복해서 연습한 기본 기술은 무엇인가요?", ["볼 컨트롤과 슈팅", "노래와 춤", "요리와 그림", "잠자기와 쉬기"], "볼 컨트롤과 슈팅"),
        ("5. 손흥민이 말한 좋은 선수의 중요한 태도는 무엇인가요?", ["겸손함을 유지하고 팀을 존중하기", "혼자만 골 넣기", "질 때마다 화내기", "팀 동료를 무시하기"], "겸손함을 유지하고 팀을 존중하기"),
    ],
    "🎤 IU": [
        ("1. 학생은 음악이 자신을 어떻게 만든다고 말하나요?", ["행복하게 만든다", "화나게 만든다", "무섭게 만든다", "졸리게 만든다"], "행복하게 만든다"),
        ("2. 학생은 어떤 노래를 좋아한다고 말하나요?", ["따뜻한 메시지가 있는 노래", "아무 뜻 없는 노래", "너무 빠른 노래만", "소리가 없는 노래"], "따뜻한 메시지가 있는 노래"),
        ("3. IU는 감정을 표현하려면 먼저 무엇을 하라고 말하나요?", ["자기 마음에 귀 기울이기", "감정을 계속 숨기기", "다른 사람의 글만 베끼기", "아무 말도 하지 않기"], "자기 마음에 귀 기울이기"),
        ("4. IU는 작은 문장이 무엇이 될 수 있다고 말하나요?", ["노래", "문제", "게임", "비밀"], "노래"),
        ("5. IU가 마지막에 학생에게 말한 조언은 무엇인가요?", ["솔직해지고 계속 쓰며 자신의 목소리를 믿기", "늘 감정을 숨기기", "글쓰기를 포기하기", "다른 사람 말만 따라 하기"], "솔직해지고 계속 쓰며 자신의 목소리를 믿기"),
    ],
    "⛸️ Kim Yuna": [
        ("1. 김연아는 피겨스케이팅에 무엇이 필요하다고 말하나요?", ["균형, 연습, 집중", "운만 있으면 됨", "큰 목소리", "휴대폰"], "균형, 연습, 집중"),
        ("2. 김연아는 경기 전 긴장에 대해 어떻게 말하나요?", ["누구나 긴장할 수 있다", "훌륭한 사람은 절대 긴장하지 않는다", "긴장은 항상 나쁜 것이다", "긴장하면 바로 포기해야 한다"], "누구나 긴장할 수 있다"),
        ("3. 김연아는 마음을 다스리기 위해 무엇에 집중했다고 말하나요?", ["자신이 연습한 것", "다른 사람의 실수", "관중의 소리", "경기 결과만"], "자신이 연습한 것"),
        ("4. 시험 전 걱정하는 학생에게 김연아는 어떻게 하라고 말하나요?", ["차근차근 준비하고 한 번에 하나에 집중하기", "걱정만 계속하기", "모든 것을 잊기", "바로 포기하기"], "차근차근 준비하고 한 번에 하나에 집중하기"),
        ("5. 김연아가 말한 침착함은 어디에서 나온다고 하나요?", ["연습과 자신에 대한 믿음", "운과 소문", "잠을 안 자는 것", "걱정만 하는 것"], "연습과 자신에 대한 믿음"),
    ],
    "🎤 BTS Jungkook": [
        ("1. 학생은 무엇을 좋아한다고 말하나요?", ["노래하기와 공연 보기", "잠만 자기", "혼자 요리하기", "지도 읽기"], "노래하기와 공연 보기"),
        ("2. 정국은 공연에 대해 무엇이 필요하다고 말하나요?", ["많은 연습", "아무 준비 없음", "운만 믿기", "무대 피하기"], "많은 연습"),
        ("3. 정국은 매일의 작은 연습이 무엇을 만들 수 있다고 말하나요?", ["큰 차이", "아무 변화 없음", "연습의 실패", "두려움만"], "큰 차이"),
        ("4. 사람들 앞에서 긴장하는 학생에게 정국은 어떻게 하라고 말하나요?", ["잘 준비하고 천천히 숨 쉬며 메시지에 집중하기", "무대를 피하기", "다른 사람과 계속 비교하기", "말하지 않기"], "잘 준비하고 천천히 숨 쉬며 메시지에 집중하기"),
        ("5. 정국이 마지막에 강조한 것은 무엇인가요?", ["계속 연습하고 과정을 즐기며 자신의 목소리를 믿기", "다른 사람보다 무조건 이기기", "재능만 믿기", "연습을 멈추기"], "계속 연습하고 과정을 즐기며 자신의 목소리를 믿기"),
    ],
    "🏜️ Grand Canyon": [
        ("1. Grand Canyon을 본 학생은 처음에 어떻게 느끼나요?", ["크고 아름답다고 느낀다", "작고 평범하다고 느낀다", "무섭기만 하다고 느낀다", "아무 감정이 없다고 느낀다"], "크고 아름답다고 느낀다"),
        ("2. 안내자는 자연이 우리를 어떻게 느끼게 할 수 있다고 말하나요?", ["작게 느끼게 한다", "항상 화나게 한다", "잠들게 한다", "배고프게 한다"], "작게 느끼게 한다"),
        ("3. Grand Canyon은 무엇에 의해 오랜 시간 형성되었나요?", ["콜로라도강과 침식 작용", "사람들이 하루 만에 만든 공사", "큰 기계 하나", "눈사람"], "콜로라도강과 침식 작용"),
        ("4. 알록달록한 암석층은 무엇을 보여 주나요?", ["지구의 역사", "현대 패션", "학교 규칙", "스포츠 기록"], "지구의 역사"),
        ("5. 이 글의 마지막 교훈으로 알맞은 것은 무엇인가요?", ["자연을 이해하면 더 존중할 수 있다", "자연은 배울 것이 없다", "강은 아무 변화도 만들 수 없다", "협곡은 중요하지 않다"], "자연을 이해하면 더 존중할 수 있다"),
    ],
    "🗽 New York": [
        ("1. New York에는 어떤 사람들이 산다고 설명하나요?", ["다양한 문화의 사람들", "한 문화의 사람들만", "아무도 살지 않음", "운동선수만"], "다양한 문화의 사람들"),
        ("2. 안내자는 New York을 어떤 도시라고 부르나요?", ["세계적인 도시", "조용한 농장", "작은 마을", "사막"], "세계적인 도시"),
        ("3. 자유의 여신상은 무엇을 보여 준다고 하나요?", ["자유", "숙제", "침묵", "두려움"], "자유"),
        ("4. 큰 도시의 어려움으로 글에 나온 것은 무엇인가요?", ["빠르고 비싸며 경쟁적일 수 있음", "항상 조용하고 느림", "사람이 전혀 없음", "문화가 하나뿐임"], "빠르고 비싸며 경쟁적일 수 있음"),
        ("5. 꿈을 따라가고 싶은 학생에게 안내자는 무엇을 조언하나요?", ["호기심을 갖고 배우며 다양한 문화를 존중하기", "새로운 문화를 피하기", "배움을 멈추기", "꿈을 포기하기"], "호기심을 갖고 배우며 다양한 문화를 존중하기"),
    ],
    "🏯 Gyeongbokgung": [
        ("1. Gyeongbokgung은 처음 언제 지어졌나요?", ["1395년", "1910년", "2020년", "1600년"], "1395년"),
        ("2. Gyeongbokgung은 어느 시대의 중심 궁궐이었나요?", ["조선", "로마 제국", "영국 제국", "현대 미국"], "조선"),
        ("3. Gyeongbokgung이라는 이름의 의미는 무엇에 가깝나요?", ["하늘이 크게 복을 내린 궁궐", "가장 높은 산", "빠른 강", "작은 시장"], "하늘이 크게 복을 내린 궁궐"),
        ("4. 근정전에서는 무엇이 열렸다고 설명하나요?", ["중요한 국가 행사", "축구 경기", "요리 대회", "영화 촬영만"], "중요한 국가 행사"),
        ("5. 이 글의 마지막 교훈은 무엇인가요?", ["과거를 이해하면 더 나은 미래를 만들 수 있다", "역사는 필요 없다", "궁궐은 재미없다", "문화는 배울 필요가 없다"], "과거를 이해하면 더 나은 미래를 만들 수 있다"),
    ],
    "📘 교과서": [
        ("1. 새로 도착한 기계는 무엇이었나요?", ["새로운 음식 기계", "새로운 로봇 선생님", "새로운 버스", "새로운 도서관"], "새로운 음식 기계"),
        ("2. 글쓴이가 오늘 선택한 음식은 무엇인가요?", ["햄버거", "떡볶이", "아이스크림", "피자"], "햄버거"),
        ("3. 글쓴이가 선택한 음식에 포함된 영양소 2가지는 무엇인가요?", ["단백질과 미네랄", "설탕과 지방", "쌀과 소금", "물과 기름"], "단백질과 미네랄"),
        ("4. 글쓴이는 왜 기분이 들떴나요?", ["다양한 선택지를 위한 버튼을 처음으로 누르게 되었기 때문에", "점심시간이 평소보다 늦게 시작되었기 때문에", "친구가 대신 음식을 골라 주었기 때문에", "내일 시험이 없어졌기 때문에"], "다양한 선택지를 위한 버튼을 처음으로 누르게 되었기 때문에"),
    ],
}


def build_mission_questions(topic_name, data):
    """주제별로 서로 다른 Mission 1 객관식 문제를 반환합니다. 보기는 한국어로만 제시합니다."""
    if topic_name in mission1_questions_bank:
        return mission1_questions_bank[topic_name]

    # 예비 처리: 새 주제가 추가되었을 때도 앱이 멈추지 않도록 기본 문제를 만듭니다.
    hint = story_card_hints_ko.get(topic_name, {})
    return [
        ("1. 이 글의 중심 인물 또는 대상은 무엇인가요?", [hint.get("Name", "중심 인물"), "전혀 다른 인물", "장소와 관계없는 대상", "본문에 없는 대상"], hint.get("Name", "중심 인물")),
        ("2. 글 속 인물의 감정으로 알맞은 것은 무엇인가요?", [hint.get("Feeling", "감정"), "아무 감정 없음", "화만 남", "본문에 나오지 않음"], hint.get("Feeling", "감정")),
        ("3. 글에서 나타난 문제나 어려움은 무엇인가요?", [hint.get("Problem", "문제"), "아무 문제가 없음", "쇼핑만 하는 이야기", "본문과 관련 없음"], hint.get("Problem", "문제")),
        ("4. 글에서 제시된 행동이나 조언은 무엇인가요?", [hint.get("Action", "행동"), "바로 포기하기", "모두 무시하기", "아무것도 하지 않기"], hint.get("Action", "행동")),
        ("5. 마지막 결과나 교훈으로 알맞은 것은 무엇인가요?", [hint.get("Result", "교훈"), "교훈이 없음", "노력을 멈추기", "아무 변화 없음"], hint.get("Result", "교훈")),
    ]

def show_mission_quiz(category, topic_name, data):
    """지문 바로 아래에서 미션 답을 4지선다로 한 번에 제출합니다."""
    questions = build_mission_questions(topic_name, data)
    prefix = f"{category}_{topic_name}_mission_quiz_"

    st.markdown('<div class="section-box"><h3>🧭 Mission 1 문제 풀기</h3></div>', unsafe_allow_html=True)
    pass_need = len(questions)
    st.caption(f"방금 읽은 지문을 떠올리며 {len(questions)}문제를 모두 푼 뒤 한 번에 제출하세요. 정답은 바로 공개하지 않고 정답 개수만 보여줍니다. {pass_need}문제를 모두 맞히면 통과입니다.")

    # 제출 후에는 개별 문항만 바꿔서 다시 제출하지 못하게 잠급니다.
    # 다시 풀 때는 아래의 'Mission 1 전체 다시 풀기' 버튼으로 모든 문항을 한꺼번에 초기화합니다.
    submitted = st.session_state.get(f"{prefix}submitted", False)

    answers = []
    for i, (question, options, answer) in enumerate(questions, start=1):
        answer_key = f"{prefix}answer_{i}"
        option_key = f"{prefix}options_{i}"

        if option_key not in st.session_state:
            st.session_state[option_key] = _stable_shuffle(options, f"mission-{category}-{topic_name}-{i}")

        st.markdown(
            f"""
            <div style="margin-top: 12px; margin-bottom: 8px; padding: 15px 17px; border-radius: 20px;
                        border: 1.5px solid #bfdbfe; background: rgba(255,255,255,0.92);
                        box-shadow: 0 4px 12px rgba(15,23,42,0.05);">
                <div style="font-size: 20px; font-weight: 950; color: #1d4ed8; line-height: 1.55;">
                    {question}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        choice = st.radio(
            "정답 선택",
            st.session_state[option_key],
            index=None,
            key=answer_key,
            label_visibility="collapsed",
            disabled=submitted
        )
        answers.append((choice, answer))

    if submitted:
        st.info("이미 제출했습니다. 한 문제씩 고쳐서 다시 제출할 수는 없습니다. 다시 도전하려면 아래 버튼으로 Mission 1 전체를 다시 풀어 주세요.")

    submit_disabled = submitted
    if st.button("✅ Mission 1 제출하기", key=f"{prefix}submit", use_container_width=True, disabled=submit_disabled):
        unanswered = sum(1 for choice, _ in answers if choice is None)
        if unanswered > 0:
            st.session_state[f"{prefix}submitted"] = False
            st.session_state[f"{prefix}message"] = f"아직 선택하지 않은 문제가 {unanswered}개 있습니다. 모든 문제를 선택한 뒤 제출하세요."
        else:
            score = sum(1 for choice, answer in answers if choice == answer)
            st.session_state[f"{prefix}submitted"] = True
            st.session_state[f"{prefix}score"] = score
            st.session_state[f"{prefix}message"] = ""
            st.rerun()

    if st.session_state.get(f"{prefix}message"):
        st.warning(st.session_state[f"{prefix}message"])

    if st.session_state.get(f"{prefix}submitted"):
        score = st.session_state.get(f"{prefix}score", 0)
        st.markdown(f"### Mission 1 정답 개수: {score}/{len(questions)}")
        if score == len(questions):
            st.success(f"통과했습니다! Mission 1의 {len(questions)}문제를 모두 맞혔습니다.")
        else:
            st.warning("아직 통과하지 못했습니다. 정답은 공개하지 않습니다. 다시 풀기를 눌러 새로 도전하세요.")

    if st.session_state.get(f"{prefix}submitted") or st.session_state.get(f"{prefix}message"):
        if st.button("🔄 Mission 1 전체 다시 풀기", key=f"{prefix}reset", use_container_width=True):
            # 버튼 자체의 key는 건드리지 않고, Mission 1 답안/결과/보기만 초기화합니다.
            keys_to_delete = [
                key for key in list(st.session_state.keys())
                if key.startswith(prefix)
                and key not in {f"{prefix}reset", f"{prefix}submit"}
            ]
            for key in keys_to_delete:
                del st.session_state[key]
            st.rerun()

def get_sequence_events(topic_name, data):
    """본문에서 5개의 서로 다른 흐름을 뽑아 문장 매칭 자료를 만듭니다."""
    dialogue = data.get('dialogue', [])
    if not dialogue:
        return []

    if topic_name == "⚽ Ronaldo":
        selected = [
            (0, 1),
            (2, 3),
            (5, 6),
            (7, 8),
            (9, 10),
        ]
        events = []
        for a, b in selected:
            speaker1, eng1, kor1 = dialogue[a]
            speaker2, eng2, kor2 = dialogue[b]
            events.append({
                "speaker1": "", "eng1": eng1, "kor1": kor1,
                "speaker2": "", "eng2": eng2, "kor2": kor2,
            })
        return events

    # 5개의 위치를 고르게 뽑되, 각 위치의 문장과 바로 다음 문장을 한 카드에 묶습니다.
    max_start = max(0, len(dialogue) - 2)
    raw_positions = [0, len(dialogue)//5, (len(dialogue)*2)//5, (len(dialogue)*3)//5, (len(dialogue)*4)//5]

    starts = []
    for p in raw_positions:
        p = min(max(p, 0), max_start)
        # 대화가 인물-나 형태일 때는 가능하면 인물 발화에서 시작하도록 조정합니다.
        if p > 0 and dialogue[p][0] == "Me":
            p -= 1
        if p not in starts:
            starts.append(p)

    for p in range(0, max_start + 1):
        if len(starts) >= min(5, len(dialogue)):
            break
        if p not in starts and dialogue[p][0] != "Me":
            starts.append(p)

    events = []
    for p in starts[:5]:
        speaker1, eng1, kor1 = dialogue[p]
        if p + 1 < len(dialogue):
            speaker2, eng2, kor2 = dialogue[p + 1]
            events.append({
                "speaker1": speaker1, "eng1": eng1, "kor1": kor1,
                "speaker2": speaker2, "eng2": eng2, "kor2": kor2,
            })
        else:
            events.append({
                "speaker1": speaker1, "eng1": eng1, "kor1": kor1,
                "speaker2": "", "eng2": "", "kor2": "",
            })
    return events

def show_sequence_matching_activity(category, topic_name, data):
    """순서 찾기 대신 사용하는 문장 매칭 게임: 영어 카드와 한국어 뜻 카드를 바로 클릭해 짝을 맞춥니다."""
    events = get_sequence_events(topic_name, data)
    prefix = f"{category}_{topic_name}_sequence_match_"

    pairs = []
    for i, event in enumerate(events, start=1):
        en_lines = []
        ko_lines = []

        if event.get("eng1"):
            if event.get("speaker1"):
                en_lines.append(f"{event['speaker1']}: {event['eng1']}")
                ko_lines.append(f"{event['speaker1']}: {event['kor1']}")
            else:
                en_lines.append(event["eng1"])
                ko_lines.append(event["kor1"])

        if event.get("eng2"):
            if event.get("speaker2"):
                en_lines.append(f"{event['speaker2']}: {event['eng2']}")
                ko_lines.append(f"{event['speaker2']}: {event['kor2']}")
            else:
                en_lines.append(event["eng2"])
                ko_lines.append(event["kor2"])

        pairs.append({
            "id": f"pair_{i}",
            "en": "<br>".join(en_lines),
            "ko": "<br>".join(ko_lines),
        })

    en_cards = [{"id": p["id"], "text": p["en"]} for p in pairs]
    ko_cards = [{"id": p["id"], "text": p["ko"]} for p in pairs]

    en_cards = _stable_shuffle(en_cards, f"{prefix}en")
    ko_cards = _stable_shuffle(ko_cards, f"{prefix}ko")

    payload = {
        "en": en_cards,
        "ko": ko_cards,
        "total": len(pairs),
    }

    data_json = json.dumps(payload, ensure_ascii=False)
    component_id = "reading_match_" + uuid.uuid4().hex

    components.html(
        f"""
        <div id="{component_id}" class="match-app">
            <div class="match-head">
                <div class="match-title">🧩 문장 매칭 게임</div>
                <div class="match-guide">
                    왼쪽 영어 대화 카드와 오른쪽 한국어 뜻 카드를 바로 클릭해 짝을 맞추세요.<br>
                    선택한 카드는 색칠되고, 정답이면 두 카드가 반짝이며 함께 사라집니다.
                </div>
            </div>

            <div class="match-status">
                <div id="status_{component_id}">먼저 영어 또는 한국어 카드를 하나 선택하세요.</div>
                <div id="score_{component_id}">맞춘 개수: 0 / {len(pairs)}</div>
            </div>

            <div class="match-board">
                <div class="match-col">
                    <div class="col-title">English</div>
                    <div id="en_{component_id}" class="card-wrap"></div>
                </div>
                <div class="match-col">
                    <div class="col-title">Korean</div>
                    <div id="ko_{component_id}" class="card-wrap"></div>
                </div>
            </div>

            <div class="progress-outer">
                <div id="bar_{component_id}" class="progress-inner"></div>
            </div>

            <button id="reset_{component_id}" class="reset-btn">매칭 게임 다시 시작</button>
        </div>

        <style>
            #{component_id}.match-app {{
                font-family: Arial, sans-serif;
                width: 100%;
                box-sizing: border-box;
                background: linear-gradient(135deg,#eef2ff 0%,#f0f9ff 50%,#fdf2f8 100%);
                border: 1px solid #c7d2fe;
                border-radius: 22px;
                padding: 22px;
                margin: 8px 0 22px 0;
                color: #1e293b;
            }}

            #{component_id} .match-head {{
                background: rgba(255,255,255,0.72);
                border: 1px solid #dbeafe;
                border-radius: 18px;
                padding: 18px 20px;
                margin-bottom: 16px;
            }}

            #{component_id} .match-title {{
                font-size: 30px;
                font-weight: 1000;
                color: #4338ca;
                margin-bottom: 8px;
            }}

            #{component_id} .match-guide {{
                font-size: 16px;
                font-weight: 800;
                color: #475569;
                line-height: 1.7;
            }}

            #{component_id} .match-status {{
                display: grid;
                grid-template-columns: 1.5fr 0.8fr;
                gap: 10px;
                margin-bottom: 14px;
                align-items: center;
            }}

            #{component_id} .match-status > div {{
                background: #ffffff;
                border: 1px solid #dbeafe;
                border-radius: 14px;
                padding: 12px 14px;
                font-size: 15px;
                font-weight: 900;
                color: #1d4ed8;
                min-height: 24px;
            }}

            #{component_id} .match-board {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 14px;
            }}

            #{component_id} .match-col {{
                background: rgba(255,255,255,0.72);
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                padding: 14px;
            }}

            #{component_id} .col-title {{
                font-size: 22px;
                font-weight: 1000;
                color: #111827;
                margin-bottom: 12px;
            }}

            #{component_id} .card-wrap {{
                display: flex;
                flex-direction: column;
                gap: 10px;
            }}

            #{component_id} .match-card {{
                width: 100%;
                text-align: left;
                border: 2px solid #c7d2fe;
                background: #ffffff;
                color: #1e293b;
                border-radius: 16px;
                padding: 14px 15px;
                font-size: 17px;
                font-weight: 900;
                line-height: 1.55;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(15,23,42,0.06);
                transition: transform .16s ease, background .16s ease, border-color .16s ease, box-shadow .16s ease;
                position: relative;
                overflow: hidden;
            }}

            #{component_id} .match-card:hover {{
                transform: translateY(-2px);
                border-color: #818cf8;
                box-shadow: 0 8px 18px rgba(99,102,241,0.16);
            }}

            #{component_id} .match-card.selected {{
                background: linear-gradient(135deg,#fef3c7 0%,#fde68a 100%);
                border-color: #f59e0b;
                color: #78350f;
                box-shadow: 0 0 0 4px rgba(245,158,11,0.18), 0 8px 20px rgba(245,158,11,0.22);
                transform: scale(1.015);
            }}

            #{component_id} .match-card.wrong {{
                animation: shake_{component_id} .28s ease-in-out;
                background: #fee2e2;
                border-color: #ef4444;
                color: #7f1d1d;
            }}

            #{component_id} .match-card.correct {{
                background: linear-gradient(135deg,#dcfce7,#bbf7d0);
                border-color: #22c55e;
                color: #14532d;
                animation: sparkleDisappear_{component_id} .68s ease forwards;
            }}

            #{component_id} .match-card.correct::after {{
                content: "✨";
                position: absolute;
                inset: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 34px;
                background: radial-gradient(circle, rgba(255,255,255,0.95), rgba(255,255,255,0.20), rgba(255,255,255,0));
                animation: sparkleFlash_{component_id} .68s ease forwards;
                pointer-events: none;
            }}

            @keyframes sparkleDisappear_{component_id} {{
                0% {{ opacity: 1; transform: scale(1); max-height: 260px; margin-bottom: 0; }}
                35% {{ opacity: 1; transform: scale(1.04); }}
                70% {{ opacity: .55; transform: scale(.96); max-height: 260px; }}
                100% {{ opacity: 0; transform: scale(.86); max-height: 0; padding-top: 0; padding-bottom: 0; border-width: 0; margin: 0; }}
            }}

            @keyframes sparkleFlash_{component_id} {{
                0% {{ opacity: 0; transform: scale(.6) rotate(0deg); }}
                35% {{ opacity: 1; transform: scale(1.25) rotate(8deg); }}
                100% {{ opacity: 0; transform: scale(1.7) rotate(-10deg); }}
            }}

            @keyframes shake_{component_id} {{
                0%, 100% {{ transform: translateX(0); }}
                25% {{ transform: translateX(-5px); }}
                50% {{ transform: translateX(5px); }}
                75% {{ transform: translateX(-3px); }}
            }}

            #{component_id} .progress-outer {{
                width: 100%;
                height: 14px;
                background: #e5e7eb;
                border-radius: 999px;
                overflow: hidden;
                margin: 16px 0 12px 0;
            }}

            #{component_id} .progress-inner {{
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg,#60a5fa,#a78bfa,#f472b6);
                border-radius: 999px;
                transition: width .28s ease;
            }}

            #{component_id} .reset-btn {{
                width: 100%;
                border: 1px solid #c7d2fe;
                background: #ffffff;
                color: #4338ca;
                border-radius: 999px;
                min-height: 46px;
                font-size: 16px;
                font-weight: 1000;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(15,23,42,0.05);
            }}

            #{component_id} .reset-btn:hover {{
                background: #eef2ff;
            }}

            #{component_id} .done-message {{
                background: linear-gradient(135deg,#dcfce7,#bbf7d0);
                border: 1px solid #86efac;
                color: #14532d;
                border-radius: 16px;
                padding: 16px;
                margin-top: 14px;
                font-size: 20px;
                font-weight: 1000;
                text-align: center;
                animation: pop_{component_id} .45s ease;
            }}

            @keyframes pop_{component_id} {{
                0% {{ transform: scale(.92); opacity: 0; }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}

            @media (max-width: 720px) {{
                #{component_id} .match-board {{
                    grid-template-columns: 1fr;
                }}
                #{component_id} .match-status {{
                    grid-template-columns: 1fr;
                }}
                #{component_id} .match-card {{
                    font-size: 15px;
                }}
            }}
        </style>

        <script>
            const data_{component_id} = {data_json};
            const root_{component_id} = document.getElementById("{component_id}");
            const enBox_{component_id} = document.getElementById("en_{component_id}");
            const koBox_{component_id} = document.getElementById("ko_{component_id}");
            const status_{component_id} = document.getElementById("status_{component_id}");
            const score_{component_id} = document.getElementById("score_{component_id}");
            const bar_{component_id} = document.getElementById("bar_{component_id}");
            const reset_{component_id} = document.getElementById("reset_{component_id}");

            let selected_{component_id} = null;
            let done_{component_id} = new Set();
            let locked_{component_id} = false;

            function escapeHtml_{component_id}(str) {{
                return String(str)
                    .replaceAll("&", "&amp;")
                    .replaceAll("<br>", "__BR__")
                    .replaceAll("<", "&lt;")
                    .replaceAll(">", "&gt;")
                    .replaceAll('"', "&quot;")
                    .replaceAll("'", "&#039;")
                    .replaceAll("__BR__", "<br>");
            }}

            function makeCard_{component_id}(card, kind) {{
                const btn = document.createElement("button");
                btn.className = "match-card";
                btn.dataset.id = card.id;
                btn.dataset.kind = kind;
                btn.innerHTML = escapeHtml_{component_id}(card.text);
                btn.addEventListener("click", () => handleClick_{component_id}(btn, card, kind));
                return btn;
            }}

            function render_{component_id}() {{
                enBox_{component_id}.innerHTML = "";
                koBox_{component_id}.innerHTML = "";

                data_{component_id}.en.forEach(card => {{
                    if (!done_{component_id}.has(card.id)) {{
                        enBox_{component_id}.appendChild(makeCard_{component_id}(card, "en"));
                    }}
                }});

                data_{component_id}.ko.forEach(card => {{
                    if (!done_{component_id}.has(card.id)) {{
                        koBox_{component_id}.appendChild(makeCard_{component_id}(card, "ko"));
                    }}
                }});

                updateScore_{component_id}();
            }}

            function updateScore_{component_id}() {{
                const count = done_{component_id}.size;
                const total = data_{component_id}.total;
                score_{component_id}.textContent = "맞춘 개수: " + count + " / " + total;
                bar_{component_id}.style.width = ((count / total) * 100) + "%";

                if (count === total) {{
                    status_{component_id}.textContent = "모든 문장을 맞췄습니다! 훌륭합니다. 🎉";
                    if (!root_{component_id}.querySelector(".done-message")) {{
                        const msg = document.createElement("div");
                        msg.className = "done-message";
                        msg.textContent = "🎉 모든 문장을 맞췄습니다!";
                        root_{component_id}.appendChild(msg);
                    }}
                }}
            }}

            function clearSelection_{component_id}() {{
                root_{component_id}.querySelectorAll(".match-card.selected").forEach(el => el.classList.remove("selected"));
                selected_{component_id} = null;
            }}

            function handleClick_{component_id}(el, card, kind) {{
                if (locked_{component_id}) return;
                if (done_{component_id}.has(card.id)) return;

                if (!selected_{component_id}) {{
                    selected_{component_id} = {{ el, card, kind }};
                    el.classList.add("selected");
                    status_{component_id}.textContent = kind === "en"
                        ? "오른쪽에서 알맞은 한국어 뜻을 고르세요."
                        : "왼쪽에서 알맞은 영어 문장을 고르세요.";
                    return;
                }}

                if (selected_{component_id}.el === el) {{
                    clearSelection_{component_id}();
                    status_{component_id}.textContent = "선택을 취소했습니다. 다시 하나를 고르세요.";
                    return;
                }}

                if (selected_{component_id}.card.id === card.id && selected_{component_id}.kind !== kind) {{
                    locked_{component_id} = true;
                    selected_{component_id}.el.classList.remove("selected");
                    el.classList.remove("selected");

                    selected_{component_id}.el.classList.add("correct");
                    el.classList.add("correct");
                    status_{component_id}.textContent = "정답입니다! 두 카드가 함께 사라집니다. ✅";

                    const matchedId = card.id;

                    setTimeout(() => {{
                        done_{component_id}.add(matchedId);
                        selected_{component_id} = null;
                        locked_{component_id} = false;
                        render_{component_id}();

                        if (done_{component_id}.size < data_{component_id}.total) {{
                            status_{component_id}.textContent = "좋아요. 다음 문장을 맞춰 보세요.";
                        }}
                    }}, 680);
                }} else {{
                    locked_{component_id} = true;
                    selected_{component_id}.el.classList.add("wrong");
                    el.classList.add("wrong");
                    status_{component_id}.textContent = "아쉬워요. 다시 짝을 맞춰 보세요. ❌";

                    setTimeout(() => {{
                        selected_{component_id}.el.classList.remove("selected", "wrong");
                        el.classList.remove("wrong");
                        selected_{component_id} = null;
                        locked_{component_id} = false;
                    }}, 360);
                }}
            }}

            reset_{component_id}.addEventListener("click", () => {{
                selected_{component_id} = null;
                done_{component_id} = new Set();
                locked_{component_id} = false;

                const doneMsg = root_{component_id}.querySelector(".done-message");
                if (doneMsg) doneMsg.remove();

                status_{component_id}.textContent = "먼저 영어 또는 한국어 카드를 하나 선택하세요.";
                render_{component_id}();
            }});

            render_{component_id}();
        </script>
        """,
        height=780,
        scrolling=True
    )


def _statement_bilingual(en, ko):
    return f"{en} ({ko})"


def show_lie_finding_activity(category, topic_name, data):
    """거짓말 찾기 활동: 카드 문장 자체를 버튼처럼 클릭합니다. 두 개를 고른 뒤 정답이면 동시에 반짝하고 사라집니다."""
    hint = get_story_card_hint(topic_name, data)
    ko_hint = story_card_hints_ko.get(topic_name, {})
    prefix = f"{category}_{topic_name}_lie_"

    if topic_name == "⚽ Ronaldo":
        true_statements = [
            (_statement_bilingual("Ronaldo was born in Portugal in 1985.", "호날두는 1985년에 포르투갈에서 태어났다."), True),
            (_statement_bilingual("Ronaldo grew up on the island of Madeira.", "호날두는 마데이라 섬에서 자랐다."), True),
            (_statement_bilingual("Ronaldo has one brother and two sisters.", "호날두에게는 남자 형제 한 명과 여자 형제 두 명이 있다."), True),
            (_statement_bilingual("Ronaldo first played for Sporting CP.", "호날두는 처음에 스포르팅 CP에서 뛰었다."), True),
            (_statement_bilingual("Ronaldo won Euro 2016 with Portugal.", "호날두는 포르투갈과 함께 유로 2016에서 우승했다."), True),
        ]
        false_statements = [
            (_statement_bilingual("Ronaldo was born in Spain in 1995.", "호날두는 1995년에 스페인에서 태어났다."), False),
            (_statement_bilingual("Ronaldo's brother's name is Messi.", "호날두의 남자 형제 이름은 메시이다."), False),
        ]
    else:
        true_statements = [
            (_statement_bilingual(f"The main character or topic is {hint['Name']}.", f"중심 인물 또는 대상은 {ko_hint.get('Name', hint['Name'])}이다."), True),
            (_statement_bilingual(f"One feeling in the text is {hint['Feeling']}.", f"글 속 감정 중 하나는 {ko_hint.get('Feeling', hint['Feeling'])}이다."), True),
            (_statement_bilingual(f"One problem is: {hint['Problem']}", f"문제 또는 어려움은 {ko_hint.get('Problem', hint['Problem'])}"), True),
            (_statement_bilingual(f"One action or advice is: {hint['Action']}", f"행동 또는 조언은 {ko_hint.get('Action', hint['Action'])}"), True),
            (_statement_bilingual(f"One lesson is: {hint['Result']}", f"교훈은 {ko_hint.get('Result', hint['Result'])}"), True),
        ]
        false_statements = [
            (_statement_bilingual("The text says the best answer is to give up and stop trying.", "이 글은 포기하고 노력을 멈추는 것이 가장 좋다고 말한다."), False),
            (_statement_bilingual("The text says practice, learning, or effort is not important at all.", "이 글은 연습, 배움, 노력이 전혀 중요하지 않다고 말한다."), False),
        ]

    statements = true_statements + false_statements
    option_key = f"{prefix}options"
    selected_key = f"{prefix}selected_cards"
    success_key = f"{prefix}success"
    message_key = f"{prefix}message"

    if option_key not in st.session_state:
        shuffled = _stable_shuffle(statements, f"lie-{category}-{topic_name}")
        letters = list("ABCDEFG")
        st.session_state[option_key] = [
            {"letter": letters[i], "text": text, "truth": truth}
            for i, (text, truth) in enumerate(shuffled)
        ]

    st.session_state.setdefault(selected_key, [])
    st.session_state.setdefault(success_key, False)
    st.session_state.setdefault(message_key, "")

    st.markdown(
        """
        <style>
        @keyframes sparkleDisappear {
            0% { opacity: 1; transform: scale(1); box-shadow: 0 0 0 rgba(250,204,21,0); }
            35% { opacity: 1; transform: scale(1.03); box-shadow: 0 0 28px rgba(250,204,21,0.95); }
            70% { opacity: 0.45; transform: scale(0.97); }
            100% { opacity: 0; transform: scale(0.88); height: 0; margin: 0; padding: 0; overflow: hidden; }
        }
        .lie-click-card {
            margin-bottom: 12px;
        }
        .lie-click-card div[data-testid="stButton"] > button {
            width: 100%;
            min-height: 86px;
            justify-content: flex-start;
            text-align: left;
            white-space: normal;
            line-height: 1.65;
            padding: 16px 18px;
            border-radius: 22px;
            border: 2px solid #fde68a;
            background: linear-gradient(135deg, #ffffff 0%, #fff7ed 100%);
            color: #92400e;
            font-size: 19px;
            font-weight: 900;
            box-shadow: 0 5px 14px rgba(15,23,42,0.07);
        }
        .lie-click-card div[data-testid="stButton"] > button:hover {
            border: 2.5px solid #38bdf8;
            background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
            color: #1d4ed8;
        }
        .lie-selected-card div[data-testid="stButton"] > button {
            border: 3px solid #38bdf8;
            background: linear-gradient(135deg, #dbeafe 0%, #ffffff 100%);
            color: #1d4ed8;
            box-shadow: 0 0 0 5px rgba(56,189,248,0.16), 0 6px 16px rgba(15,23,42,0.08);
        }
        .lie-card-vanish {
            animation: sparkleDisappear 1.15s ease-in-out forwards;
            margin-bottom: 12px;
            padding: 16px 18px;
            border-radius: 22px;
            border: 2.5px solid #facc15;
            background: linear-gradient(135deg, #fef9c3 0%, #ffffff 45%, #dcfce7 100%);
            color: #92400e;
            font-size: 19px;
            font-weight: 950;
            line-height: 1.65;
            box-shadow: 0 0 25px rgba(250,204,21,0.55);
        }
        .lie-normal-card {
            margin-bottom: 12px;
            padding: 16px 18px;
            border-radius: 22px;
            border: 2px solid #fde68a;
            background: linear-gradient(135deg, #ffffff 0%, #fff7ed 100%);
            color: #92400e;
            font-size: 19px;
            font-weight: 950;
            line-height: 1.65;
            box-shadow: 0 5px 14px rgba(15,23,42,0.07);
        }
        .lie-mission-success {
            margin-top: 14px;
            padding: 22px 24px;
            border-radius: 26px;
            background: linear-gradient(135deg, #dcfce7 0%, #ffffff 55%, #fef9c3 100%);
            border: 2px solid #86efac;
            text-align: center;
            font-size: 28px;
            font-weight: 950;
            color: #166534;
            box-shadow: 0 10px 24px rgba(15,23,42,0.10);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-box"><h3>🕵️ 거짓말 찾기</h3></div>', unsafe_allow_html=True)
    st.caption("A~G 보기 중 지문 내용과 맞지 않는 거짓말 카드 2개를 누르세요. 카드 문장 자체가 버튼입니다. 정답 2개를 모두 고르면 카드가 동시에 사라집니다.")

    false_letters = {item["letter"] for item in st.session_state[option_key] if not item["truth"]}
    selected_letters = st.session_state[selected_key]

    # 성공한 뒤에는 정답 카드 2개가 반짝하고 사라지는 효과를 보여줍니다.
    if st.session_state[success_key]:
        for item in st.session_state[option_key]:
            if item["letter"] in selected_letters:
                st.markdown(
                    f"""
                    <div class="lie-card-vanish">
                        {item['letter']}. {item['text']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="lie-normal-card">
                        {item['letter']}. {item['text']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown('<div class="lie-mission-success">✨ 정답입니다! 미션 성공!</div>', unsafe_allow_html=True)
        if st.button("🔄 거짓말 찾기 다시 풀기", key=f"{prefix}reset_success", use_container_width=True):
            reset_keys_by_prefix(prefix)
            st.rerun()
        return

    # 아직 성공 전이면 카드 문장 자체를 클릭합니다.
    for item in st.session_state[option_key]:
        is_selected = item["letter"] in selected_letters
        wrapper_class = "lie-click-card lie-selected-card" if is_selected else "lie-click-card"
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)

        # 별도의 "A 카드 선택" 버튼을 만들지 않고, 카드 문장 자체가 버튼이 되도록 합니다.
        btn_label = f"✅ {item['letter']}. {item['text']}" if is_selected else f"{item['letter']}. {item['text']}"

        if st.button(btn_label, key=f"{prefix}pick_{item['letter']}", use_container_width=True):
            current = list(st.session_state[selected_key])

            # 이미 선택한 카드를 다시 누르면 선택 취소
            if item["letter"] in current:
                current.remove(item["letter"])
                st.session_state[message_key] = ""

            # 아직 2개 미만이면 선택 추가
            elif len(current) < 2:
                current.append(item["letter"])
                st.session_state[message_key] = ""

            st.session_state[selected_key] = current

            # 2개가 선택되면 바로 판정
            if len(current) == 2:
                if set(current) == false_letters:
                    st.session_state[success_key] = True
                    st.session_state[message_key] = ""
                else:
                    # 오답이면 정답을 공개하지 않고 선택을 바로 풀어 다시 고르게 합니다.
                    st.session_state[selected_key] = []
                    st.session_state[message_key] = "아직 정답이 아닙니다. 정답은 공개하지 않습니다. 다시 두 카드를 골라 보세요."
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.caption(f"현재 선택: {len(selected_letters)}/2개")

    if st.session_state.get(message_key):
        st.warning(st.session_state[message_key])

    if selected_letters or st.session_state.get(message_key):
        if st.button("🔄 거짓말 찾기 다시 풀기", key=f"{prefix}reset_try", use_container_width=True):
            reset_keys_by_prefix(prefix)
            st.rerun()


def show_key_expression_word_test(category, topic_name, data, max_words=10):
    """Key Expressions 학습: 테스트가 아니라 듣고 뜻을 확인하는 학습용 카드입니다."""
    key_words = get_key_words(topic_name, data)[:max_words]

    st.markdown('<div class="section-box"><h3>⭐ Key Expressions 듣기 & 뜻 학습</h3></div>', unsafe_allow_html=True)
    st.caption("시험처럼 뜻을 적는 활동이 아니라, 영어 표현을 듣고 한국어 뜻을 확인하는 학습 활동입니다. 표현을 여러 번 듣고 따라 말해 보세요.")

    if not key_words:
        st.info("이 주제에는 아직 핵심 표현이 없습니다.")
        return

    for i, (word, meaning) in enumerate(key_words, start=1):
        c1, c_audio, c2 = st.columns([2.2, 1.0, 2.4])
        with c1:
            st.markdown(
                f"""
                <div style="padding: 14px 16px; border-radius: 18px; background: #eff6ff;
                            border: 1.5px solid #bfdbfe; font-size: 21px; font-weight: 950;
                            color: #1d4ed8; margin-top: 4px; line-height: 1.55;">
                    {i}. {word}
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_audio:
            direct_tts_player(word, lang="en")
        with c2:
            st.markdown(
                f"""
                <div style="padding: 14px 16px; border-radius: 18px; background: #f0fdf4;
                            border: 1.5px solid #bbf7d0; font-size: 20px; font-weight: 900;
                            color: #166534; margin-top: 4px; line-height: 1.55;">
                    뜻: {meaning}
                </div>
                """,
                unsafe_allow_html=True
            )

    all_words_text = " ... ".join([word for word, _ in key_words])
    play_persistent_full_audio(
        all_words_text,
        key=f"{category}_{topic_name}_key_expression_all_audio",
        button_label="🎧 핵심 표현 전체 듣기",
        lang="en"
    )


def get_english_sentences(text):
    """영어 편지에서 문장 단위로 나눕니다. 마침표, 물음표, 느낌표를 기준으로 4문장 이상인지 확인합니다."""
    cleaned = str(text).strip()
    raw_sentences = re.split(r"(?<=[.!?])\s+|\n+", cleaned)
    sentences = []
    for sentence in raw_sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        # 영어 단어가 2개 이상 들어간 것만 실제 문장으로 봅니다.
        if len(re.findall(r"[A-Za-z']+", sentence)) >= 2:
            sentences.append(sentence)
    return sentences


def normalize_sentence_for_repeat(sentence):
    """복사·붙여넣기 반복 여부를 확인하기 위해 문장을 단순화합니다."""
    return re.sub(r"[^a-z]+", "", str(sentence).lower())


def has_repeated_sentence(sentences):
    """똑같은 영어 문장을 반복해서 붙여 넣었는지 확인합니다."""
    normalized = [normalize_sentence_for_repeat(s) for s in sentences]
    normalized = [s for s in normalized if s]
    return len(normalized) != len(set(normalized))


def make_character_reply(answer, target_name, topic_name):
    """학생 편지에 대한 주인공의 짧은 영어 답장을 만듭니다."""
    lower = answer.lower()
    if any(w in lower for w in ["give up", "try", "practice", "effort", "hard", "goal"]):
        core_message = "Your words remind me that effort and patience are very important."
    elif any(w in lower for w in ["sad", "sorry", "worry", "nervous", "tired", "feel"]):
        core_message = "Thank you for understanding my feelings and cheering me up."
    elif any(w in lower for w in ["dream", "future", "hope", "believe"]):
        core_message = "I am happy that my story helped you think about your dream and future."
    elif any(w in lower for w in ["team", "friend", "respect", "together"]):
        core_message = "Your letter shows that you understand the value of respect and teamwork."
    else:
        core_message = "Thank you for reading my story carefully and writing a kind letter to me."

    return (
        f"Dear Me,\n\n"
        f"Thank you for your warm letter. {core_message} "
        f"I hope you keep learning from this story and use the lesson in your own life. "
        f"Even small steps can help you grow, so keep trying and believe in yourself.\n\n"
        f"From,\n{target_name}"
    )


def make_letter_feedback(answer, target_name):
    """주인공에게 쓰는 편지에 대해 한국어/영어 피드백과 개선 예시를 만듭니다."""
    text = answer.strip()
    lower = text.lower()

    ko_strengths = []
    en_strengths = []
    ko_advice = []
    en_advice = []

    if any(w in lower for w in ["dear", "hello", "hi"]):
        ko_strengths.append("편지의 시작이 자연스럽습니다. 주인공을 직접 부르는 표현이 있어서 진짜 편지를 쓰는 느낌이 납니다.")
        en_strengths.append("Your opening sounds natural because you directly address the main character.")
    else:
        ko_advice.append(f"처음에 'Dear {target_name},'처럼 주인공을 부르는 말을 넣으면 편지 형식이 더 분명해집니다.")
        en_advice.append(f"Try starting with 'Dear {target_name},' to make your writing look more like a real letter.")

    if any(w in lower for w in ["sorry", "sad", "hard", "difficult", "tired", "worry", "nervous", "feel"]):
        ko_strengths.append("주인공의 감정을 이해하려는 태도가 잘 드러납니다. 단순한 칭찬이 아니라 상대의 마음을 헤아리는 편지라서 더 따뜻하게 느껴집니다.")
        en_strengths.append("You show empathy by thinking about the character's feelings.")

    if any(w in lower for w in ["proud", "great", "good", "amazing", "wonderful", "impressive"]):
        ko_strengths.append("주인공을 칭찬하는 표현이 잘 들어갔습니다. 읽는 사람이 힘을 얻을 수 있는 긍정적인 분위기가 만들어졌습니다.")
        en_strengths.append("Your compliment creates a positive and encouraging tone.")

    if any(w in lower for w in ["cheer", "support", "believe", "keep", "try", "never give up", "do not give up", "don't give up"]):
        ko_strengths.append("응원과 격려의 메시지가 분명합니다. 특히 계속 노력하라는 내용은 이 활동의 주제와 잘 연결됩니다.")
        en_strengths.append("Your message of encouragement is clear and meaningful.")

    if any(w in lower for w in ["because", "so", "when", "if"]):
        ko_strengths.append("이유나 상황을 설명하려는 연결어를 사용한 점이 좋습니다. 문장이 단순한 나열에서 벗어나 조금 더 논리적으로 이어집니다.")
        en_strengths.append("You used connecting words, so your ideas flow more logically.")
    else:
        ko_advice.append("다음에는 'because'를 사용해서 왜 그렇게 생각하는지 이유를 한 문장 더 붙여 보세요. 그러면 편지가 훨씬 풍부해집니다.")
        en_advice.append("Add one sentence with 'because' to explain your reason more clearly.")

    word_count = len(re.findall(r"[A-Za-z']+", text))
    if word_count >= 35:
        ko_strengths.append("분량도 충분합니다. 짧은 문장 몇 개로 마음을 전달하는 수준을 넘어, 자신의 생각을 조금 더 자세히 표현했습니다.")
        en_strengths.append("Your letter has enough detail, and it expresses your thoughts more fully.")
    else:
        ko_advice.append("조금 더 길게 쓰고 싶다면 '내가 너에게 말해 주고 싶은 것', '그 이유', '마지막 응원' 순서로 한 문장씩 추가하면 좋습니다.")
        en_advice.append("To make it longer, add one sentence for your message, one for the reason, and one for final encouragement.")

    if not ko_strengths:
        ko_strengths.append("주인공에게 직접 말을 건네려는 시도가 좋습니다. 아직 문장이 짧더라도, 자신의 생각을 영어로 표현하려고 한 점이 중요합니다.")
        en_strengths.append("It is good that you tried to express your own message in English.")

    korean_feedback = (
        "좋은 점: " + " ".join(ko_strengths[:4]) + "\n\n"
        "더 발전시키기: " + " ".join(ko_advice[:3] if ko_advice else ["현재 편지는 전체적으로 따뜻하고 분명합니다. 다음에는 본문에서 배운 핵심 표현을 하나 넣고, 마지막에 앞으로의 다짐이나 응원을 덧붙이면 더 완성도 높은 편지가 됩니다."])
    )

    english_feedback = (
        "Good points: " + " ".join(en_strengths[:4]) + "\n\n"
        "To improve: " + " ".join(en_advice[:3] if en_advice else ["Your letter is warm and clear. Next time, try adding one key expression from the reading and one final sentence of encouragement."])
    )

    improved_english = (
        f"Dear {target_name},\n"
        "I want to tell you that your story was meaningful to me. "
        "I could understand your feelings, and I learned something important from your effort. "
        "Please keep believing in yourself because small steps can make a big difference. "
        "I will remember your story and try harder in my own life, too.\n"
        "Sincerely,\nMe"
    )

    return korean_feedback, english_feedback, improved_english

def get_display_target_name(topic_name, target_name):
    """화면에 보여 줄 한국어 이름을 정합니다."""
    name_map = {
        "⚽ Ronaldo": "호날두",
        "🏀 Jordan": "조던",
        "⚽ Son Heung-min": "손흥민",
        "🎤 IU": "아이유",
        "⛸️ Kim Yuna": "김연아",
        "🎤 BTS Jungkook": "정국",
        "🏜️ Grand Canyon": "그랜드캐니언",
        "🗽 New York": "뉴욕",
        "🏯 Gyeongbokgung": "경복궁",
        "📘 교과서": "교과서 속 주인공",
    }
    return name_map.get(topic_name, target_name)


def show_letter_to_character_activity(category, topic_name, data):
    """마지막 활동: 한국어 초안 → 구글 번역 → 영어 편지 작성 → 영어 답장 → 답장 한국어 이해 확인."""
    hint = get_story_card_hint(topic_name, data)
    target_name = hint.get('Name', 'the main character')
    display_name = get_display_target_name(topic_name, target_name)
    prefix = f"{category}_{topic_name}_letter_to_character_"

    st.markdown(
        f'<div class="section-box"><h3>💌 {display_name}에게 편지 보내기</h3></div>',
        unsafe_allow_html=True
    )
    st.caption(
        "한국어로 먼저 생각을 쓰고 구글 번역으로 영어를 확인한 뒤, 영어 편지를 4문장 이상 적어 보내세요. "
        "답장을 받은 뒤에는 답장도 구글 번역으로 한국어 뜻을 확인하고, 직접 한국어로 적어 넣습니다."
    )

    korean_draft = st.text_area(
        "1단계: 한국어로 먼저 쓰기",
        placeholder=f"예: {display_name}에게 하고 싶은 말을 한국어로 먼저 써 보세요.\n힘들어도 포기하지 말고 계속 도전했으면 좋겠어.",
        height=120,
        key=f"{prefix}korean_draft"
    )

    if korean_draft.strip():
        translate_url = (
            "https://translate.google.com/?sl=ko&tl=en&op=translate&text="
            + quote(korean_draft.strip())
        )

        st.markdown(
            """
            <div class="message-card">
                <div class="story-card-title">🌐 번역 도움</div>
                <div class="message-line">
                    아래 버튼을 눌러 한국어 문장을 영어로 번역한 뒤,<br>
                    번역된 영어 문장을 복사해서 2단계 영어 편지 칸에 붙여 넣으세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.link_button("🌐 구글 번역으로 영어 편지 만들기", translate_url, use_container_width=True)

    answer = st.text_area(
        "2단계: 영어로 번역한 편지 적기",
        placeholder=f"예: Dear {target_name},\nYou did a great job. I learned many things from you. I want to practice every day. I will not give up easily.",
        height=170,
        key=f"{prefix}answer"
    )

    if st.button(f"💌 {display_name}에게 편지 보내기", key=f"{prefix}submit", use_container_width=True):
        sentences = get_english_sentences(answer)
        if not answer.strip():
            if korean_draft.strip():
                st.warning("구글 번역에서 영어 문장을 확인한 뒤, 2단계 영어 편지 칸에 붙여 넣어 주세요.")
            else:
                st.warning("먼저 한국어 초안을 쓰거나, 2단계에 영어 편지를 직접 써 주세요.")
        elif detect_language(answer) == "ko":
            st.warning("편지는 영어로 보내야 합니다. 구글 번역 버튼을 눌러 영어로 바꾼 뒤 2단계에 영어로 적어 주세요.")
        elif len(sentences) < 4:
            st.warning(f"영어로 최소 4문장 이상 써 주세요. 현재 확인된 영어 문장 수: {len(sentences)}/4")
        elif has_repeated_sentence(sentences):
            st.warning("똑같은 문장을 반복해서 복사·붙여넣기하면 답장을 받을 수 없습니다. 서로 다른 내용의 영어 문장 4개 이상을 써 주세요.")
        else:
            ko_feedback, en_feedback, improved_letter = make_letter_feedback(answer, target_name)
            reply_letter = make_character_reply(answer, target_name, topic_name)
            st.session_state[f"{prefix}sent_letter"] = answer
            st.session_state[f"{prefix}reply_letter_value"] = reply_letter
            st.session_state[f"{prefix}ko_feedback_value"] = ko_feedback
            st.session_state[f"{prefix}en_feedback_value"] = en_feedback
            st.session_state[f"{prefix}improved_letter_value"] = improved_letter
            st.session_state[f"{prefix}reply_translation_done"] = False
            st.success(f"편지를 보냈습니다. {display_name}의 답장을 확인해 보세요.")

    sent_letter = st.session_state.get(f"{prefix}sent_letter", "")
    reply_letter = st.session_state.get(f"{prefix}reply_letter_value", "")
    ko_feedback = st.session_state.get(f"{prefix}ko_feedback_value", "")
    en_feedback = st.session_state.get(f"{prefix}en_feedback_value", "")
    improved_letter = st.session_state.get(f"{prefix}improved_letter_value", "")

    if sent_letter and reply_letter:
        st.markdown(
            f"""
            <div class="message-card">
                <div class="story-card-title">💌 {display_name}에게 보낸 편지</div>
                <div class="message-line">{sent_letter.replace(chr(10), '<br>')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(f"### 📬 {display_name}의 답장")
        st.text_area(
            f"{display_name}에게서 온 영어 답장",
            value=reply_letter,
            height=180,
            key=f"{prefix}reply_letter"
        )

        reply_translate_url = (
            "https://translate.google.com/?sl=en&tl=ko&op=translate&text="
            + quote(reply_letter.strip())
        )
        st.link_button(f"🌐 {display_name}의 답장 구글 번역으로 보기", reply_translate_url, use_container_width=True)

        reply_korean = st.text_area(
            f"3단계: {display_name}의 답장을 한국어로 적어 넣기",
            placeholder="구글 번역으로 뜻을 확인한 뒤, 답장의 한국어 뜻을 여기에 적어 보세요.",
            height=130,
            key=f"{prefix}reply_korean_understanding"
        )

        if reply_korean.strip():
            if st.button("✅ 편지를 모두 이해했습니다", key=f"{prefix}understood_btn", use_container_width=True):
                st.session_state[f"{prefix}reply_translation_done"] = True
                st.success("좋습니다! 영어 편지와 답장의 의미까지 모두 확인했습니다.")
        else:
            st.info("답장의 한국어 뜻을 적어 넣으면 ‘편지를 모두 이해했습니다’ 버튼이 나타납니다.")

        if st.session_state.get(f"{prefix}reply_translation_done", False):
            st.success("✅ 편지를 모두 이해했습니다.")

        st.markdown("### 🇰🇷 한국어 피드백")
        st.info(ko_feedback)
        st.markdown("### 🇺🇸 English Feedback")
        st.info(en_feedback)
        st.markdown("### ✨ 더 자연스러운 영어 편지 예시")
        st.text_area(
            "복사해서 참고할 수 있는 개선 예시",
            value=improved_letter,
            height=180,
            key=f"{prefix}improved_letter"
        )


# =========================================================
# 단순 Reading 활동 함수 덮어쓰기
# =========================================================
def build_mission_questions(topic_name, data):
    """Mission 1: 중복 filler 문제를 만들지 않고, 준비된 문제만 사용합니다."""
    if data.get("mission_questions"):
        source_questions = list(data["mission_questions"])
    else:
        source_questions = list(data.get("questions", []))

    questions = []
    seen = set()
    for item in source_questions:
        q, options, answer = item
        clean_q = re.sub(r"^\d+\.\s*", "", str(q)).strip()
        if not clean_q:
            continue
        if clean_q in seen:
            continue
        seen.add(clean_q)
        n = len(questions) + 1
        questions.append((f"{n}. {clean_q}", options, answer))

    return questions


def show_mission_quiz(category, topic_name, data):
    questions = build_mission_questions(topic_name, data)
    total = len(questions)
    pass_need = max(1, int(total * 0.8 + 0.9999)) if total else 0
    prefix = f"{category}_{topic_name}_mission_"
    attempts = st.session_state.get(f"{prefix}attempts", 0)
    locked = st.session_state.get(f"{prefix}locked", False)

    st.markdown('<div class="section-box"><h3>🧭 Mission 1. 지문 읽고 문제 풀기</h3></div>', unsafe_allow_html=True)
    if total == 0:
        st.info("아직 준비된 문제가 없습니다. 지문을 읽고 다음 활동으로 넘어가 주세요.")
        return
    st.caption(f"총 {total}문제입니다. {pass_need}문제 이상 맞히면 통과하셨습니다. 풀 수 있는 기회는 총 2번입니다.")

    answers = []
    for i, (question, options, answer) in enumerate(questions, start=1):
        answer_key = f"{prefix}answer_{i}"
        option_key = f"{prefix}options_{i}"
        if option_key not in st.session_state:
            st.session_state[option_key] = _stable_shuffle(options, f"mission12-{category}-{topic_name}-{i}")
        st.markdown(
            f"""
            <div style="margin-top: 12px; margin-bottom: 8px; padding: 14px 16px; border-radius: 16px;
                        border: 1px solid #e5e7eb; background: #ffffff;">
                <div style="font-size: 19px; font-weight: 850; color: #111827; line-height: 1.55;">{question}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        choice = st.radio("정답 선택", st.session_state[option_key], index=None, key=answer_key, label_visibility="collapsed", disabled=locked)
        answers.append((choice, answer))

    if not locked and attempts < 2:
        if st.button("✅ Mission 1 제출하기", key=f"{prefix}submit_{attempts}", use_container_width=True):
            unanswered = [i for i, (choice, _) in enumerate(answers, start=1) if choice is None]
            if unanswered:
                st.warning(f"아직 선택하지 않은 문제가 있습니다: {', '.join(map(str, unanswered))}")
            else:
                wrong_nums = [i for i, (choice, answer) in enumerate(answers, start=1) if choice != answer]
                score = total - len(wrong_nums)
                attempts += 1
                st.session_state[f"{prefix}attempts"] = attempts
                st.session_state[f"{prefix}score"] = score
                st.session_state[f"{prefix}wrong_nums"] = wrong_nums
                if score >= pass_need or attempts >= 2:
                    st.session_state[f"{prefix}locked"] = True
                st.rerun()

    attempts = st.session_state.get(f"{prefix}attempts", 0)
    score = st.session_state.get(f"{prefix}score", None)
    wrong_nums = st.session_state.get(f"{prefix}wrong_nums", [])
    locked = st.session_state.get(f"{prefix}locked", False)

    if attempts > 0 and score is not None:
        st.markdown(f"### 제출 결과: {score}/{total}")
        if score >= pass_need:
            st.success("통과하셨습니다.")
        else:
            st.warning("아직 통과하지 못했습니다.")

        if attempts == 1 and score < pass_need:
            st.info("1차 제출 후에는 정답을 보여 주지 않습니다. 오답 문항 번호만 확인하고 다시 읽어 보세요.")
            st.markdown("**오답 문항:** " + ", ".join(map(str, wrong_nums)))
            if st.button("🔄 2번째 기회로 다시 풀기", key=f"{prefix}retry", use_container_width=True):
                for k in list(st.session_state.keys()):
                    if k.startswith(prefix + "answer_"):
                        del st.session_state[k]
                st.rerun()

        if attempts >= 2 or (locked and score >= pass_need):
            if attempts >= 2:
                st.info("2차 제출 후에는 정답을 확인할 수 있습니다.")
                st.markdown("### 정답")
                for i, (_, _, answer) in enumerate(questions, start=1):
                    st.markdown(f"{i}. **{answer}**")
            st.caption("이 주제의 Mission 1 기회는 종료되었습니다.")


def show_sequence_matching_activity(category, topic_name, data):
    """문장 매칭: 영어 카드와 한국어 카드를 직접 클릭해서 맞추는 방식입니다."""
    pairs = data.get("matching_pairs") or [(eng, kor) for _, eng, kor in data.get("dialogue", [])[:6]]
    pairs = pairs[:6]

    en_cards = [{"id": f"p{i}", "text": en} for i, (en, ko) in enumerate(pairs, start=1)]
    ko_cards = [{"id": f"p{i}", "text": ko} for i, (en, ko) in enumerate(pairs, start=1)]
    en_cards = _stable_shuffle(en_cards, f"match-en-{category}-{topic_name}")
    ko_cards = _stable_shuffle(ko_cards, f"match-ko-{category}-{topic_name}")

    payload = json.dumps({"en": en_cards, "ko": ko_cards, "total": len(pairs)}, ensure_ascii=False)
    component_id = "click_match_" + uuid.uuid4().hex

    components.html(
        f"""
        <div id="{component_id}" class="match-app">
            <div class="match-title">🧩 문장 매칭</div>
            <div class="match-guide">영어 카드와 한국어 카드를 직접 클릭하세요. 정답이면 두 카드가 반짝이며 사라집니다.</div>
            <div class="match-status" id="status_{component_id}">먼저 카드 하나를 고르세요.</div>
            <div class="match-board">
                <div class="match-col"><div class="col-title">English</div><div id="en_{component_id}"></div></div>
                <div class="match-col"><div class="col-title">Korean</div><div id="ko_{component_id}"></div></div>
            </div>
            <div class="progress"><div id="bar_{component_id}"></div></div>
            <button class="reset-btn" id="reset_{component_id}">다시 시작</button>
        </div>
        <style>
            #{component_id}.match-app {{background:#ffffff;border:1px solid #e5e7eb;border-radius:18px;padding:18px;font-family:Arial,sans-serif;color:#111827;}}
            #{component_id} .match-title {{font-size:26px;font-weight:900;margin-bottom:6px;}}
            #{component_id} .match-guide {{font-size:15px;font-weight:700;color:#475569;margin-bottom:12px;line-height:1.6;}}
            #{component_id} .match-status {{background:#f8fafc;border:1px solid #e5e7eb;border-radius:12px;padding:10px 12px;margin-bottom:12px;font-weight:800;color:#1d4ed8;}}
            #{component_id} .match-board {{display:grid;grid-template-columns:1fr 1fr;gap:12px;}}
            #{component_id} .match-col {{background:#f9fafb;border:1px solid #e5e7eb;border-radius:14px;padding:12px;}}
            #{component_id} .col-title {{font-size:20px;font-weight:900;margin-bottom:10px;}}
            #{component_id} .card {{width:100%;margin-bottom:10px;text-align:left;white-space:normal;line-height:1.55;border:2px solid #dbeafe;background:#fff;color:#111827;border-radius:14px;padding:14px;font-size:17px;font-weight:850;cursor:pointer;box-shadow:0 3px 10px rgba(15,23,42,.05);transition:.15s;}}
            #{component_id} .card:hover {{transform:translateY(-1px);border-color:#93c5fd;}}
            #{component_id} .selected {{background:#fef3c7;border-color:#f59e0b;color:#78350f;}}
            #{component_id} .wrong {{background:#fee2e2;border-color:#ef4444;}}
            #{component_id} .correct {{background:#dcfce7;border-color:#22c55e;animation:vanish_{component_id} .7s ease forwards;}}
            @keyframes vanish_{component_id} {{0%{{opacity:1;transform:scale(1);}}40%{{opacity:1;transform:scale(1.04);box-shadow:0 0 24px rgba(250,204,21,.9);}}100%{{opacity:0;transform:scale(.85);height:0;padding:0;margin:0;border-width:0;overflow:hidden;}}}}
            #{component_id} .progress {{height:12px;background:#e5e7eb;border-radius:99px;overflow:hidden;margin:12px 0;}}
            #{component_id} .progress div {{height:100%;width:0%;background:#60a5fa;}}
            #{component_id} .reset-btn {{width:100%;border:1px solid #d1d5db;border-radius:12px;background:#f9fafb;padding:12px;font-weight:900;cursor:pointer;}}
            @media(max-width:700px){{#{component_id} .match-board{{grid-template-columns:1fr;}}}}
        </style>
        <script>
            const data_{component_id} = {payload};
            const root_{component_id} = document.getElementById("{component_id}");
            const enBox_{component_id} = document.getElementById("en_{component_id}");
            const koBox_{component_id} = document.getElementById("ko_{component_id}");
            const status_{component_id} = document.getElementById("status_{component_id}");
            const bar_{component_id} = document.getElementById("bar_{component_id}");
            let selected_{component_id} = null;
            let done_{component_id} = new Set();
            let locked_{component_id} = false;
            function esc_{component_id}(x) {{ return String(x).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#039;'); }}
            function makeCard_{component_id}(card, kind) {{
                const b=document.createElement('button'); b.className='card'; b.dataset.id=card.id; b.dataset.kind=kind; b.innerHTML=esc_{component_id}(card.text);
                b.onclick=()=>clickCard_{component_id}(b, card, kind); return b;
            }}
            function render_{component_id}() {{
                enBox_{component_id}.innerHTML=''; koBox_{component_id}.innerHTML='';
                data_{component_id}.en.forEach(c=>{{ if(!done_{component_id}.has(c.id)) enBox_{component_id}.appendChild(makeCard_{component_id}(c,'en')); }});
                data_{component_id}.ko.forEach(c=>{{ if(!done_{component_id}.has(c.id)) koBox_{component_id}.appendChild(makeCard_{component_id}(c,'ko')); }});
                bar_{component_id}.style.width=(done_{component_id}.size/data_{component_id}.total*100)+'%';
                if(done_{component_id}.size===data_{component_id}.total) status_{component_id}.textContent='모든 문장을 맞췄습니다! 🎉';
            }}
            function clear_{component_id}() {{ root_{component_id}.querySelectorAll('.selected').forEach(e=>e.classList.remove('selected')); selected_{component_id}=null; }}
            function clickCard_{component_id}(el, card, kind) {{
                if(locked_{component_id} || done_{component_id}.has(card.id)) return;
                if(!selected_{component_id}) {{ selected_{component_id}={{el,card,kind}}; el.classList.add('selected'); status_{component_id}.textContent = kind==='en' ? '알맞은 한국어 카드를 고르세요.' : '알맞은 영어 카드를 고르세요.'; return; }}
                if(selected_{component_id}.el===el) {{ clear_{component_id}(); status_{component_id}.textContent='선택을 취소했습니다.'; return; }}
                locked_{component_id}=true;
                if(selected_{component_id}.card.id===card.id && selected_{component_id}.kind!==kind) {{
                    selected_{component_id}.el.classList.remove('selected'); el.classList.remove('selected');
                    selected_{component_id}.el.classList.add('correct'); el.classList.add('correct'); status_{component_id}.textContent='정답입니다!';
                    const id=card.id; setTimeout(()=>{{done_{component_id}.add(id); selected_{component_id}=null; locked_{component_id}=false; render_{component_id}();}},700);
                }} else {{
                    selected_{component_id}.el.classList.add('wrong'); el.classList.add('wrong'); status_{component_id}.textContent='다시 골라 보세요.';
                    setTimeout(()=>{{selected_{component_id}.el.classList.remove('selected','wrong'); el.classList.remove('wrong'); selected_{component_id}=null; locked_{component_id}=false;}},420);
                }}
            }}
            document.getElementById('reset_{component_id}').onclick=()=>{{selected_{component_id}=null;done_{component_id}=new Set();locked_{component_id}=false;status_{component_id}.textContent='먼저 카드 하나를 고르세요.';render_{component_id}();}};
            render_{component_id}();
        </script>
        """,
        height=700,
        scrolling=True,
    )


def show_lie_finding_activity(category, topic_name, data):
    """거짓말 찾기: 5개 카드 중 거짓말 2개를 직접 클릭합니다."""
    cards = data.get("lie_cards")
    if not cards:
        cards = [(eng, True) for _, eng, _ in data.get("dialogue", [])[:3]] + [("This sentence is not true.", False), ("This detail is different from the text.", False)]
    cards = cards[:5]
    prefix = f"{category}_{topic_name}_lie_click5_"
    option_key = f"{prefix}options"
    selected_key = f"{prefix}selected"
    success_key = f"{prefix}success"
    message_key = f"{prefix}message"

    if option_key not in st.session_state:
        shuffled = _stable_shuffle(cards, f"lie5-{category}-{topic_name}")
        letters = list("ABCDE")
        st.session_state[option_key] = [{"letter": letters[i], "text": text, "truth": truth} for i, (text, truth) in enumerate(shuffled)]
    st.session_state.setdefault(selected_key, [])
    st.session_state.setdefault(success_key, False)
    st.session_state.setdefault(message_key, "")

    st.markdown("""
    <style>
    @keyframes lieVanish {0%{opacity:1;transform:scale(1);}40%{opacity:1;transform:scale(1.04);box-shadow:0 0 24px rgba(250,204,21,.9);}100%{opacity:0;transform:scale(.86);height:0;margin:0;padding:0;border-width:0;overflow:hidden;}}
    .lie-card-wrap{margin-bottom:10px;}
    .lie-card-wrap div[data-testid="stButton"]>button{width:100%;min-height:72px;text-align:left;justify-content:flex-start;white-space:normal;line-height:1.55;padding:14px 16px;border-radius:16px;border:2px solid #e5e7eb;background:#fff;color:#111827;font-size:17px;font-weight:850;}
    .lie-card-selected div[data-testid="stButton"]>button{border:3px solid #3b82f6;background:#dbeafe;color:#1e3a8a;}
    .lie-card-gone{animation:lieVanish .9s ease forwards;margin-bottom:10px;padding:14px 16px;border-radius:16px;border:2px solid #facc15;background:#fef9c3;color:#78350f;font-size:17px;font-weight:900;line-height:1.55;}
    .lie-card-left{margin-bottom:10px;padding:14px 16px;border-radius:16px;border:2px solid #e5e7eb;background:#fff;color:#111827;font-size:17px;font-weight:850;line-height:1.55;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-box"><h3>🕵️ 거짓말 찾기</h3></div>', unsafe_allow_html=True)
    st.caption("카드 5개 중 지문 내용과 맞지 않는 거짓말 카드 2개를 고르세요. 카드 문장 자체를 클릭하면 됩니다.")

    false_letters = {item["letter"] for item in st.session_state[option_key] if not item["truth"]}
    selected = list(st.session_state[selected_key])

    if st.session_state[success_key]:
        for item in st.session_state[option_key]:
            if item["letter"] in selected:
                st.markdown(f'<div class="lie-card-gone">{item["letter"]}. {item["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="lie-card-left">{item["letter"]}. {item["text"]}</div>', unsafe_allow_html=True)
        st.success("정답입니다! 거짓말 2개를 모두 찾았습니다.")
        if st.button("🔄 거짓말 찾기 다시 풀기", key=f"{prefix}reset_success", use_container_width=True):
            reset_keys_by_prefix(prefix)
            st.rerun()
        return

    for item in st.session_state[option_key]:
        is_selected = item["letter"] in selected
        cls = "lie-card-wrap lie-card-selected" if is_selected else "lie-card-wrap"
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        label = f"✅ {item['letter']}. {item['text']}" if is_selected else f"{item['letter']}. {item['text']}"
        if st.button(label, key=f"{prefix}pick_{item['letter']}", use_container_width=True):
            current = list(st.session_state[selected_key])
            if item["letter"] in current:
                current.remove(item["letter"])
            elif len(current) < 2:
                current.append(item["letter"])
            st.session_state[selected_key] = current
            if len(current) == 2:
                if set(current) == false_letters:
                    st.session_state[success_key] = True
                    st.session_state[message_key] = ""
                else:
                    st.session_state[selected_key] = []
                    st.session_state[message_key] = "아직 아닙니다. 정답은 공개하지 않습니다. 다시 두 카드를 골라 보세요."
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get(message_key):
        st.warning(st.session_state[message_key])


def show_reading_blocks(dialogue, category, topic_name):
    full_english = make_full_listening_text(dialogue)
    play_persistent_full_audio(full_english, key=f"{category}_{topic_name}_full_only_audio_v1", button_label="🎧 전체 듣기", lang="en")
    lines = [eng for _, eng, _ in dialogue]
    chunk_size = 4
    for block_idx in range(0, len(lines), chunk_size):
        chunk = lines[block_idx:block_idx + chunk_size]
        html_lines = "<br>".join(chunk)
        st.markdown(
            f"""
            <div style="margin-bottom: 16px; padding: 20px 22px; border-radius: 18px;
                        border: 1px solid #e5e7eb; background: #ffffff;
                        box-shadow: 0 3px 10px rgba(15,23,42,0.04);">
                <div style="font-size: 21px; font-weight: 750; color: #000000; line-height: 1.85;">
                    {html_lines}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


tab_video, tab_reading = st.tabs([
    "🎬 동영상",
    "📖 Reading"
])

# =========================================================
# 동영상
# =========================================================
with tab_video:
    st.markdown("## 🎬 동영상")

    video_url = data["video_url"]

    if video_url and str(video_url).startswith("http"):
        # YouTube Shorts 링크는 st.video에서 잘 안 보일 수 있어 iframe으로 직접 넣습니다.
        if "youtube.com/shorts/" in video_url:
            video_id = video_url.rstrip("/").split("/")[-1].split("?")[0]
            components.html(
                f"""
                <div style="display:flex; justify-content:center; width:100%;">
                    <iframe
                        width="360"
                        height="640"
                        src="https://www.youtube.com/embed/{video_id}"
                        title="YouTube Shorts video player"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                        allowfullscreen>
                    </iframe>
                </div>
                """,
                height=680,
            )
        else:
            st.video(video_url)
    else:
        st.info("동영상 링크가 없는 자료입니다.")

# =========================================================
# Reading: 본문 → Mission 1 → 문장 매칭 → 거짓말 찾기 → 편지쓰기 → Key Expressions
# =========================================================
with tab_reading:
    st.markdown("## 📖 Reading")
    st.caption("본문을 먼저 읽고, 아래 Mission 1 문제를 풉니다. 한국어 해석 보기는 제공하지 않습니다.")

    st.markdown('<div class="section-box"><h3>📖 본문 읽기</h3></div>', unsafe_allow_html=True)
    show_reading_blocks(dialogue, category, topic_name)

    st.markdown("---")
    show_mission_quiz(category, topic_name, data)

    st.markdown("---")
    show_sequence_matching_activity(category, topic_name, data)

    st.markdown("---")
    show_lie_finding_activity(category, topic_name, data)

    st.markdown("---")
    show_letter_to_character_activity(category, topic_name, data)

    st.markdown("---")
    show_key_expression_word_test(category, topic_name, data, max_words=10)
