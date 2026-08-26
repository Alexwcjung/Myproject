import streamlit as st
import streamlit.components.v1 as components
import random
import io
import os
import json
import uuid
import base64
from datetime import datetime
from gtts import gTTS

st.set_page_config(page_title="Batman English Mission", page_icon="🦇", layout="wide")

VIDEO_URL = "https://www.youtube.com/watch?v=U4fhEziQsc8"


# =========================
# TTS
# =========================

@st.cache_data(show_spinner=False)
def make_tts_audio(text):
    safe_text = str(text).strip()
    if not safe_text:
        return b""

    fp = io.BytesIO()
    tts = gTTS(text=safe_text, lang="en", slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def show_tts_audio(text):
    """가로 폭이 짧은 미니 TTS 오디오 플레이어"""
    try:
        audio_bytes = make_tts_audio(text)
        if audio_bytes:
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

            components.html(
                f"""
                <div style="
                    width:320px;
                    max-width:100%;
                    margin:4px 0 10px 0;
                ">
                    <audio
                        controls
                        preload="metadata"
                        style="
                            width:320px;
                            max-width:100%;
                            height:34px;
                            display:block;
                        "
                    >
                        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                    </audio>
                </div>
                """,
                height=48
            )
    except Exception as e:
        st.warning("음성을 불러오지 못했습니다. requirements.txt에 gTTS가 있는지 확인해 주세요.")
        st.caption(f"오류 내용: {e}")



# =========================
# PDF CERTIFICATE
# =========================

def get_korean_font_path():
    """Streamlit Cloud/리눅스 환경에서 사용할 수 있는 한글 폰트를 찾습니다."""
    candidates = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for path in candidates:
        try:
            if os.path.exists(path):
                return path
        except Exception:
            pass
    return None


def make_batman_mission_pdf():
    """배트맨 3개 미션 완료 인증 PDF를 만듭니다."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfgen import canvas
    except Exception:
        return None

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    font_name = "Helvetica"
    bold_font_name = "Helvetica-Bold"

    try:
        pdfmetrics.registerFont(UnicodeCIDFont("HYGothic-Medium"))
        font_name = "HYGothic-Medium"
        bold_font_name = "HYGothic-Medium"
    except Exception:
        font_path = get_korean_font_path()
        if font_path and "DejaVuSans" not in font_path:
            try:
                pdfmetrics.registerFont(TTFont("KoreanFont", font_path))
                font_name = "KoreanFont"
                bold_font_name = "KoreanFont"
            except Exception:
                pass

    c.setFillColor(colors.HexColor("#eef2ff"))
    c.roundRect(
        18 * mm, 24 * mm,
        width - 36 * mm, height - 48 * mm,
        10 * mm, fill=1, stroke=0
    )

    c.setFillColor(colors.white)
    c.roundRect(
        28 * mm, 38 * mm,
        width - 56 * mm, height - 76 * mm,
        8 * mm, fill=1, stroke=0
    )

    c.setStrokeColor(colors.HexColor("#6366f1"))
    c.setLineWidth(2)
    c.roundRect(
        28 * mm, 38 * mm,
        width - 56 * mm, height - 76 * mm,
        8 * mm, fill=0, stroke=1
    )

    c.setFillColor(colors.HexColor("#14532d"))
    c.setFont(bold_font_name, 27)
    c.drawCentredString(
        width / 2,
        height - 72 * mm,
        "Batman English Mission 임무 완성"
    )

    c.setFillColor(colors.HexColor("#3730a3"))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(
        width / 2,
        height - 86 * mm,
        "MISSION COMPLETE"
    )

    c.setFillColor(colors.HexColor("#14532d"))
    c.setFont(bold_font_name, 18)
    c.drawCentredString(
        width / 2,
        height - 103 * mm,
        "배트맨 영어 미션을 모두 완성하셨습니다."
    )

    c.setFillColor(colors.HexColor("#1e293b"))
    c.setFont(font_name, 15)
    c.drawCentredString(width / 2, height - 126 * mm, "완료 활동: 대사 빈칸")
    c.drawCentredString(width / 2, height - 139 * mm, "완료 활동: 대사 연결")
    c.drawCentredString(width / 2, height - 152 * mm, "완료 활동: 문법")

    c.setFillColor(colors.HexColor("#475569"))
    c.setFont(font_name, 12)
    c.drawCentredString(
        width / 2,
        height - 169 * mm,
        "You are Gotham's English Guardian!"
    )

    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont(font_name, 11)
    now_text = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.drawCentredString(width / 2, 62 * mm, f"완료 시간: {now_text}")
    c.drawCentredString(
        width / 2,
        52 * mm,
        "이 PDF를 저장한 뒤 선생님께 보여 주세요."
    )

    c.setStrokeColor(colors.HexColor("#6366f1"))
    c.setLineWidth(2.5)
    c.circle(width / 2, 86 * mm, 16 * mm, fill=0, stroke=1)
    c.line(width / 2 - 7 * mm, 86 * mm, width / 2 - 2 * mm, 80 * mm)
    c.line(width / 2 - 2 * mm, 80 * mm, width / 2 + 8 * mm, 93 * mm)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def show_batman_pdf_download():
    """배트맨 3개 미션 완료 PDF 다운로드 버튼을 보여 줍니다."""
    st.markdown(
        """
        <div style="
            background:linear-gradient(135deg,#eef2ff,#f0f9ff,#fdf2f8);
            padding:24px;
            border-radius:22px;
            border:2px solid #6366f1;
            margin-top:18px;
            text-align:center;
        ">
            <div style="
                font-size:1.55rem;
                font-weight:1000;
                color:#3730a3;
            ">
                📄 Batman English Mission PDF 인증서 저장
            </div>
            <div style="
                font-size:1.05rem;
                font-weight:850;
                color:#475569;
                margin-top:8px;
            ">
                아래 버튼을 눌러 배트맨 영어 미션 완료 인증서를 저장하세요.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    pdf_bytes = make_batman_mission_pdf()

    if pdf_bytes:
        st.markdown(
            """
            <style>
            div[data-testid="stDownloadButton"] button {
                min-height:68px !important;
                font-size:1.25rem !important;
                font-weight:1000 !important;
                border-radius:18px !important;
                border:2px solid #4f46e5 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            "📄 PDF 인증서 다운받기",
            data=pdf_bytes,
            file_name="Batman_English_Mission_Complete.pdf",
            mime="application/pdf",
            key="download_batman_complete_pdf",
            use_container_width=True
        )
    else:
        st.warning(
            "PDF 저장 기능을 사용하려면 requirements.txt에 "
            "reportlab을 추가해 주세요. 예: reportlab>=4.0.0"
        )



# =========================
# CSS
# =========================

st.markdown("""
<style>
.stApp {
    background: #ffffff;
    color: #111827;
}

.main-title {
    font-size: 46px;
    font-weight: 1000;
    color: #111827;
    margin-bottom: 4px;
}

.sub-title {
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 24px;
}

.hero-box {
    background: linear-gradient(135deg,#fef3c7 0%,#e0f2fe 55%,#f3e8ff 100%);
    border: 1px solid #fde68a;
    border-radius: 28px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(251,191,36,0.18);
}

.hero-title {
    font-size: 31px;
    font-weight: 1000;
    color: #0f172a;
    margin-bottom: 8px;
}

.hero-sub {
    font-size: 17px;
    color: #475569;
    line-height: 1.7;
}

.section-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    padding: 24px;
    margin: 18px 0;
    box-shadow: 0 6px 18px rgba(15,23,42,0.06);
}

.section-title {
    font-size: 26px;
    font-weight: 900;
    color: #111827;
    margin-bottom: 10px;
}

.small-guide {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 14px;
}

.line-box {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px;
    line-height: 1.8;
    font-size: 17px;
    margin-bottom: 12px;
}

.script-box {
    background: #ffffff;
    border: 1px solid #bfdbfe;
    border-radius: 18px;
    padding: 16px;
    line-height: 1.75;
    font-size: 16px;
    margin-bottom: 10px;
}

.kor {
    color: #6b7280;
    font-size: 15px;
}

.time-tag {
    display: inline-block;
    background: #facc15;
    color: #111827;
    font-weight: 900;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 13px;
    margin-bottom: 8px;
}

.success-box {
    background: #dcfce7;
    border: 1px solid #86efac;
    border-radius: 18px;
    padding: 16px;
    color: #166534;
    font-weight: 900;
    margin-top: 14px;
}

.fail-box {
    background: #fee2e2;
    border: 1px solid #fecaca;
    border-radius: 18px;
    padding: 16px;
    color: #991b1b;
    font-weight: 900;
    margin-top: 14px;
}

.info-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 18px;
    padding: 16px;
    color: #1e3a8a;
    font-weight: 800;
    margin-bottom: 12px;
}

.game-card {
    background: linear-gradient(135deg,#eef2ff,#f8fafc);
    border:1px solid #c7d2fe;
    border-radius:18px;
    padding:20px;
    margin-bottom:18px;
}

.big-guide {
    font-size:1.12rem;
    font-weight:800;
    color:#475569;
    line-height:1.7;
}

.score-box {
    background:linear-gradient(135deg,#dcfce7,#bbf7d0);
    padding:18px;
    border-radius:18px;
    border:1px solid #86efac;
    margin-top:18px;
    text-align:center;
    font-size:1.15rem;
    font-weight:900;
}

.wrong-box {
    background:#fff7ed;
    padding:15px;
    border-radius:14px;
    border:1px solid #fdba74;
    margin-top:10px;
}

.cert-box {
    background: linear-gradient(135deg,#fff7ed,#fefce8,#eff6ff);
    border: 2px solid #f59e0b;
    border-radius: 24px;
    padding: 26px;
    margin-top: 18px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(245,158,11,.14);
}

div[data-testid="stButton"] button {
    border: 1px solid #bfdbfe;
    background: #ffffff;
    color: #111827;
    border-radius: 14px;
    padding: 14px 16px;
    font-weight: 900;
    text-align: left;
    min-height: 46px;
}

div[data-testid="stButton"] button:hover {
    background: #eff6ff;
    border: 1px solid #60a5fa;
    color: #111827;
}

button[kind="primary"] {
    background: #facc15 !important;
    color: #111827 !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 900 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# DATA
# =========================

full_script = [
    {"time": "0:02", "en": "I killed those people. That's what I can be.", "ko": "내가 그 사람들을 죽였어. 나는 그런 사람이 될 수 있어."},
    {"time": "0:09", "en": "No, no. You can't. You're not.", "ko": "아니, 안 돼. 넌 그럴 수 없어. 넌 그런 사람이 아니야."},
    {"time": "0:12", "en": "I'm whatever Gotham needs me to be.", "ko": "나는 고담시가 필요로 하는 무엇이든 될 거야."},
    {"time": "0:16", "en": "A hero. Not the hero we deserved, but the hero we needed.", "ko": "영웅. 우리가 받을 자격이 있던 영웅은 아니지만, 우리에게 필요했던 영웅."},
    {"time": "0:20", "en": "Nothing less than a knight.", "ko": "그는 진정한 기사와 같은 존재야."},
    {"time": "0:28", "en": "You heard me. You can tell them.", "ko": "내 말 들었지. 사람들에게 그렇게 말해."},
    {"time": "0:32", "en": "You set the dogs on me.", "ko": "개들을 나에게 풀어."},
    {"time": "0:37", "en": "The truth isn't good enough.", "ko": "진실만으로는 충분하지 않아."},
    {"time": "0:48", "en": "Sometimes people deserve more.", "ko": "때로 사람들은 더 많은 것을 받을 자격이 있어."},
    {"time": "0:53", "en": "Sometimes people deserve to have their faith rewarded.", "ko": "때로 사람들은 자신의 믿음이 보상받을 자격이 있어."},
    {"time": "1:42", "en": "He's the hero Gotham deserves, but not the one it needs right now.", "ko": "그는 고담시가 받을 자격이 있는 영웅이지만, 지금 고담시에 필요한 영웅은 아니야."},
    {"time": "1:48", "en": "So we'll hunt him.", "ko": "그래서 우리는 그를 쫓을 거야."},
    {"time": "1:52", "en": "Because he can take it.", "ko": "왜냐하면 그는 그것을 감당할 수 있으니까."},
    {"time": "1:56", "en": "Because he's not our hero.", "ko": "왜냐하면 그는 우리의 영웅이 아니니까."},
    {"time": "2:06", "en": "He's a silent guardian, a watchful protector.", "ko": "그는 조용한 수호자이자, 늘 지켜보는 보호자야."}
]

key_lines = [
    {"time": "0:12", "en": "I'm whatever Gotham needs me to be.", "ko": "나는 고담시가 필요로 하는 무엇이든 될 거야.", "easy": "Batman will become what Gotham needs."},
    {"time": "0:16", "en": "Not the hero we deserved, but the hero we needed.", "ko": "우리가 받을 자격이 있던 영웅은 아니지만, 우리에게 필요했던 영웅.", "easy": "Batman is not a perfect public hero, but he is necessary."},
    {"time": "0:37", "en": "The truth isn't good enough.", "ko": "진실만으로는 충분하지 않아.", "easy": "Sometimes truth alone is not enough."},
    {"time": "0:48", "en": "Sometimes people deserve more.", "ko": "때로 사람들은 더 많은 것을 받을 자격이 있다.", "easy": "People sometimes need more than truth."},
    {"time": "0:53", "en": "Sometimes people deserve to have their faith rewarded.", "ko": "때로 사람들은 자신의 믿음이 보상받을 자격이 있다.", "easy": "People's hope should be protected."},
    {"time": "1:42", "en": "He's the hero Gotham deserves, but not the one it needs right now.", "ko": "그는 고담시가 받을 자격이 있는 영웅이지만, 지금 필요한 영웅은 아니다.", "easy": "Batman cannot be the public hero right now."},
    {"time": "1:52", "en": "Because he can take it.", "ko": "왜냐하면 그는 그것을 감당할 수 있으니까.", "easy": "Batman can endure blame."},
    {"time": "2:06", "en": "He's a silent guardian, a watchful protector.", "ko": "그는 조용한 수호자이자, 늘 지켜보는 보호자이다.", "easy": "Batman protects Gotham quietly."}
]

key_expressions = [
    {"word": "whatever", "ko": "무엇이든, 어떤 것이든", "example": "I'm whatever Gotham needs me to be."},
    {"word": "deserve", "ko": "~할 자격이 있다, ~을 받을 만하다", "example": "Sometimes people deserve more."},
    {"word": "hero", "ko": "영웅", "example": "He's the hero Gotham deserves."},
    {"word": "truth", "ko": "진실", "example": "The truth isn't good enough."},
    {"word": "faith", "ko": "믿음, 신뢰", "example": "People deserve to have their faith rewarded."},
    {"word": "reward", "ko": "보상하다", "example": "Their faith is rewarded."},
    {"word": "hunt", "ko": "쫓다, 추적하다", "example": "So we'll hunt him."},
    {"word": "take it", "ko": "그것을 감당하다, 견디다", "example": "Because he can take it."},
    {"word": "guardian", "ko": "수호자", "example": "He's a silent guardian."},
    {"word": "watchful", "ko": "주의 깊게 지켜보는", "example": "A watchful protector."},
    {"word": "protector", "ko": "보호자", "example": "A watchful protector."},
    {"word": "need", "ko": "필요로 하다", "example": "Gotham needs me."}
]

hero_questions = [
    {"q": "Q1. At first, what do people think Batman is?", "options": ["A hero", "A criminal", "A singer", "A teacher"], "answer": "A criminal"},
    {"q": "Q2. What is Batman really doing?", "options": ["Taking the blame", "Running away", "Making money", "Singing a song"], "answer": "Taking the blame"},
    {"q": "Q3. What kind of person is Batman in this scene?", "options": ["Sacrificing", "Lazy", "Selfish", "Funny"], "answer": "Sacrificing"},
    {"q": "Q4. Why can Batman endure it?", "options": ["Because he can take it", "Because he is tired", "Because he wants money", "Because he forgot"], "answer": "Because he can take it"}
]

blank_questions = [
    {"audio": "I'm whatever Gotham needs me to be.", "sentence": "I'm whatever Gotham ______ me to be.", "options": ["needs", "follows", "remembers"], "answer": "needs"},
    {"audio": "Not the hero we deserved, but the hero we needed.", "sentence": "Not the hero we ______, but the hero we ______.", "options": ["deserved / needed", "found / lost", "saw / followed"], "answer": "deserved / needed"},
    {"audio": "Sometimes people deserve more.", "sentence": "Sometimes people ______ more.", "options": ["deserve", "forget", "hide"], "answer": "deserve"},
    {"audio": "Because he can take it.", "sentence": "Because he can ______ it.", "options": ["take", "find", "change"], "answer": "take"},
    {"audio": "A silent guardian, a watchful protector.", "sentence": "A silent ______, a watchful ______.", "options": ["guardian / protector", "student / teacher", "singer / dancer"], "answer": "guardian / protector"}
]

correct_map = {
    "I'm whatever Gotham needs me to be.": "나는 고담시가 필요로 하는 무엇이든 될 거야.",
    "The truth isn't good enough.": "진실만으로는 충분하지 않아.",
    "Sometimes people deserve more.": "때로 사람들은 더 많은 것을 받을 자격이 있다.",
    "Because he can take it.": "왜냐하면 그는 그것을 감당할 수 있으니까.",
    "A silent guardian.": "조용한 수호자.",
    "A watchful protector.": "늘 지켜보는 보호자."
}

grammar_questions = [
    {"q": "He can ___ it.", "options": ["take", "takes", "took"], "answer": "take", "explain": "can 뒤에는 동사원형을 씁니다. 그래서 can take가 맞습니다."},
    {"q": "You can't ___ that.", "options": ["do", "does", "did"], "answer": "do", "explain": "can't 뒤에도 동사원형을 씁니다."},
    {"q": "Gotham ___ me.", "options": ["need", "needs", "needed"], "answer": "needs", "explain": "Gotham은 단수 주어이므로 현재시제에서는 needs를 씁니다."},
    {"q": "People deserve ___ more.", "options": ["have", "to have", "having"], "answer": "to have", "explain": "deserve 뒤에 동사가 올 때는 deserve to + 동사 형태를 쓸 수 있습니다."}
]


# =========================
# SESSION STATE
# =========================

# 코드 구조가 바뀐 뒤에도 이전 세션의 완료값이 남아
# 새 활동이 건너뛰어지는 문제를 막기 위한 버전 초기화입니다.
BATMAN_STATE_VERSION = "2026-08-26-v3"

if st.session_state.get("batman_state_version") != BATMAN_STATE_VERSION:
    st.session_state.batman_state_version = BATMAN_STATE_VERSION

    st.session_state.batman_complete = {
        "blank": False,
        "matching": False,
        "grammar": False
    }

    st.session_state.blank_current = 0
    st.session_state.blank_checked = False
    st.session_state.blank_last_correct = None

    st.session_state.matching_completed_ids = []
    st.session_state.matching_selected_en = None
    st.session_state.matching_feedback = ""

    # 이전 버전의 문법 결과도 함께 초기화
    st.session_state.grammar_status = [None] * len(grammar_questions)

if "batman_complete" not in st.session_state:
    st.session_state.batman_complete = {
        "blank": False,
        "matching": False,
        "grammar": False
    }

# 대사 빈칸: 한 문제씩 풀기
if "blank_current" not in st.session_state:
    st.session_state.blank_current = 0

if "blank_checked" not in st.session_state:
    st.session_state.blank_checked = False

if "blank_last_correct" not in st.session_state:
    st.session_state.blank_last_correct = None

# 대사 연결: Streamlit이 실제 완료 상태를 직접 관리
if "matching_completed_ids" not in st.session_state:
    st.session_state.matching_completed_ids = []

if "matching_selected_en" not in st.session_state:
    st.session_state.matching_selected_en = None

if "matching_feedback" not in st.session_state:
    st.session_state.matching_feedback = ""

# =========================
# HEADER
# =========================

st.markdown('<div class="main-title">🦇 Batman English Mission</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Video-based English Activity · Bright Classroom Version</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-title">Hero or Villain?</div>
    <div class="hero-sub">
        Watch the Batman scene, read the subtitles,
        listen and fill in key lines, match quotes, and discover grammar rules.
        <br>
        <span class="kor">영상을 본 뒤 대사 빈칸 · 대사 연결 · 문법 활동을 완성해 봅시다.</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎬 영상",
    "🎧 대사 빈칸",
    "🧩 대사 연결",
    "📘 문법",
    "💬 핵심 대사 & 표현",
    "🏆 인증서"
])


# =========================
# TAB 1 VIDEO
# =========================

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎬 Watch the Video</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-guide">영상을 보면서 아래 영어 자막과 한국어 해석을 함께 확인하세요.</div>', unsafe_allow_html=True)

    st.video(VIDEO_URL)

    st.markdown("""
    <div class="line-box">
        <b>Today's Question</b><br>
        Is Batman a hero, a villain, or both?
        <br>
        <span class="kor">오늘의 질문: 배트맨은 영웅인가, 악당인가, 아니면 둘 다인가?</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📖 Full Script & Meaning")

    for line in full_script:
        st.markdown(f"""
        <div class="script-box">
            <span class="time-tag">{line["time"]}</span><br>
            <b>{line["en"]}</b><br>
            <span class="kor">{line["ko"]}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 2 LINE BLANKS
# =========================

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎧 대사 빈칸</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="game-card"><div class="big-guide">'
        '대사를 듣고 빈칸에 들어갈 말을 고르세요.<br>'
        '한 문제씩 <b>답 확인</b>을 누르면 정답 여부와 정답이 표시됩니다. '
        '확인한 뒤 다음 문제로 넘어가세요.'
        '</div></div>',
        unsafe_allow_html=True
    )

    total_blank = len(blank_questions)
    current_blank = min(st.session_state.blank_current, total_blank - 1)

    if not st.session_state.batman_complete["blank"]:
        item = blank_questions[current_blank]

        st.markdown(
            f"""
            <div class="score-box">
                대사 빈칸 {current_blank + 1} / {total_blank}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="line-box">
            <b>{current_blank + 1}. {item["sentence"]}</b>
        </div>
        """, unsafe_allow_html=True)

        show_tts_audio(item["audio"])

        options = item["options"].copy()
        random.Random(f"batman_blank_single_{current_blank}").shuffle(options)

        answer_key = f"blank_single_answer_{current_blank}"

        selected_answer = st.radio(
            "정답을 고르세요.",
            options,
            key=answer_key,
            index=None,
            label_visibility="collapsed",
            disabled=st.session_state.blank_checked
        )

        if not st.session_state.blank_checked:
            if st.button(
                "✅ 답 확인",
                key=f"blank_check_{current_blank}",
                type="primary",
                use_container_width=True
            ):
                if selected_answer is None:
                    st.warning("먼저 답을 하나 고르세요.")
                else:
                    st.session_state.blank_last_correct = (
                        selected_answer == item["answer"]
                    )
                    st.session_state.blank_checked = True
                    st.rerun()

        else:
            if st.session_state.blank_last_correct:
                st.success("정답입니다. ✅")
            else:
                st.error("오답입니다. ❌")

            st.markdown(
                f"""
                <div class="feedback-ko">
                    <b>정답:</b> {item["answer"]}<br>
                    <b>전체 대사:</b> {item["audio"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            if current_blank < total_blank - 1:
                if st.button(
                    "➡️ 다음 문제",
                    key=f"blank_next_{current_blank}",
                    type="primary",
                    use_container_width=True
                ):
                    st.session_state.blank_current += 1
                    st.session_state.blank_checked = False
                    st.session_state.blank_last_correct = None
                    st.rerun()
            else:
                if st.button(
                    "🎉 대사 빈칸 완료",
                    key="blank_finish_all",
                    type="primary",
                    use_container_width=True
                ):
                    st.session_state.batman_complete["blank"] = True
                    st.rerun()

    else:
        st.markdown(
            '<div class="success-box">🎧 대사 빈칸의 모든 문제를 확인했습니다. 미션 완료! ✅</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 3 MATCHING
# =========================

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 대사 연결</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="game-card"><div class="big-guide">'
        '왼쪽 영어 대사 1개를 클릭한 뒤 오른쪽 한국어 뜻 1개를 클릭하세요.<br>'
        '맞으면 해당 두 카드가 사라지고, 틀리면 다시 고를 수 있습니다.<br>'
        '<b>6쌍을 모두 실제로 맞혀야 대사 연결 미션이 완료됩니다.</b>'
        '</div></div>',
        unsafe_allow_html=True
    )

    matching_pairs = [
        {"id": f"pair_{i}", "en": en, "ko": ko}
        for i, (en, ko) in enumerate(correct_map.items(), start=1)
    ]

    completed_ids = set(st.session_state.matching_completed_ids)
    total_matching = len(matching_pairs)

    if len(completed_ids) >= total_matching:
        st.session_state.batman_complete["matching"] = True

    if st.session_state.batman_complete["matching"]:
        st.markdown(
            '<div class="success-box">🧩 모든 대사를 정확히 연결했습니다. 매칭 미션 완료! ✅</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="score-box">
                맞춘 개수: {len(completed_ids)} / {total_matching}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.matching_feedback:
            if st.session_state.matching_feedback.startswith("✅"):
                st.success(st.session_state.matching_feedback)
            else:
                st.error(st.session_state.matching_feedback)

        remaining_pairs = [
            p for p in matching_pairs
            if p["id"] not in completed_ids
        ]

        en_cards = remaining_pairs.copy()
        ko_cards = remaining_pairs.copy()

        random.Random("batman_native_match_en").shuffle(en_cards)
        random.Random("batman_native_match_ko").shuffle(ko_cards)

        col_en, col_ko = st.columns(2)

        with col_en:
            st.markdown("### 🇺🇸 English")
            for pair in en_cards:
                is_selected = (
                    st.session_state.matching_selected_en == pair["id"]
                )

                label = (
                    f"🟡 {pair['en']}"
                    if is_selected
                    else pair["en"]
                )

                if st.button(
                    label,
                    key=f"match_en_{pair['id']}",
                    use_container_width=True
                ):
                    st.session_state.matching_selected_en = pair["id"]
                    st.session_state.matching_feedback = (
                        "영어 대사를 선택했습니다. 오른쪽에서 뜻을 고르세요."
                    )
                    st.rerun()

        with col_ko:
            st.markdown("### 🇰🇷 Korean")
            for pair in ko_cards:
                if st.button(
                    pair["ko"],
                    key=f"match_ko_{pair['id']}",
                    use_container_width=True
                ):
                    selected_id = st.session_state.matching_selected_en

                    if selected_id is None:
                        st.session_state.matching_feedback = (
                            "❌ 먼저 왼쪽에서 영어 대사를 선택하세요."
                        )

                    elif selected_id == pair["id"]:
                        if pair["id"] not in st.session_state.matching_completed_ids:
                            st.session_state.matching_completed_ids.append(pair["id"])

                        st.session_state.matching_selected_en = None

                        if len(st.session_state.matching_completed_ids) >= total_matching:
                            st.session_state.batman_complete["matching"] = True
                            st.session_state.matching_feedback = (
                                "✅ 마지막 대사까지 맞혔습니다!"
                            )
                        else:
                            st.session_state.matching_feedback = (
                                "✅ 정답입니다! 맞힌 카드가 사라졌습니다."
                            )

                    else:
                        st.session_state.matching_selected_en = None
                        st.session_state.matching_feedback = (
                            "❌ 연결이 맞지 않습니다. 다시 선택해 보세요."
                        )

                    st.rerun()

        st.markdown("---")

        if st.button(
            "🔄 대사 연결 처음부터 다시 하기",
            key="matching_reset_native",
            use_container_width=True
        ):
            st.session_state.matching_completed_ids = []
            st.session_state.matching_selected_en = None
            st.session_state.matching_feedback = ""
            st.session_state.batman_complete["matching"] = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 4 GRAMMAR
# =========================

with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📘 문법</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-guide">'
        '문제는 항상 그대로 유지됩니다. 답을 고르고 채점하면 각 문제 아래에 '
        '정답 또는 오답만 표시됩니다. 정답 자체는 공개하지 않습니다. '
        '오답은 답을 바꿔 다시 채점할 수 있습니다.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="line-box">
        <b>Look at these lines.</b><br><br>
        1. He <b>can take</b> it.<br>
        2. You <b>can't do</b> that.<br>
        3. Gotham <b>needs</b> me.<br>
        4. People deserve <b>to have</b> more.
    </div>
    """, unsafe_allow_html=True)

    if "grammar_status" not in st.session_state:
        st.session_state.grammar_status = [None] * len(grammar_questions)

    grammar_answers = {}

    # 모든 문제를 항상 그대로 표시
    for idx, item in enumerate(grammar_questions):
        st.markdown(f"**Q{idx + 1}. {item['q']}**")

        grammar_answers[idx] = st.radio(
            "하나를 고르세요.",
            item["options"],
            key=f"grammar_fixed_{idx}",
            index=None,
            horizontal=True
        )

        # 채점 결과만 문제 바로 아래 표시
        if st.session_state.grammar_status[idx] is True:
            st.success("정답입니다. ✅")

        elif st.session_state.grammar_status[idx] is False:
            st.error("오답입니다. ❌ 다시 생각해 보세요.")

        st.write("")

    if st.button(
        "문법 채점",
        key="check_grammar_fixed",
        type="primary"
    ):
        unanswered = [
            idx
            for idx in range(len(grammar_questions))
            if grammar_answers.get(idx) is None
        ]

        if unanswered:
            st.warning(
                "모든 문제에 답한 뒤 채점하세요. "
                f"선택하지 않은 문제: {', '.join(str(i + 1) for i in unanswered)}번"
            )

        else:
            for idx, item in enumerate(grammar_questions):
                st.session_state.grammar_status[idx] = (
                    grammar_answers[idx] == item["answer"]
                )

            if all(st.session_state.grammar_status):
                st.session_state.batman_complete["grammar"] = True
            else:
                st.session_state.batman_complete["grammar"] = False

            st.rerun()

    # 모두 맞힌 경우에만 완료 메시지
    if all(status is True for status in st.session_state.grammar_status):
        st.markdown("""
        <div class="success-box">
            📘 모든 문법 문제를 맞혔습니다! 문법 미션 완료! 🎉
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="line-box">
            <b>Grammar Rule</b><br><br>
            1. <b>can + 동사원형</b><br>
            예: He can take it.<br><br>
            2. <b>can't + 동사원형</b><br>
            예: You can't do that.<br><br>
            3. 단수 주어 현재동사에는 보통 <b>-s</b>를 붙입니다.<br>
            예: Gotham needs me.<br><br>
            4. <b>deserve to + 동사</b>는 '~할 자격이 있다'라는 뜻입니다.<br>
            예: People deserve to have more.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 5 KEY LINES & EXPRESSIONS
# =========================

with tab5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 핵심 대사 & 핵심 표현</div>', unsafe_allow_html=True)

    st.markdown("### 💬 핵심 대사")

    for line in key_lines:
        st.markdown(f"""
        <div class="line-box">
            <span class="time-tag">{line["time"]}</span><br>
            <b>{line["en"]}</b><br>
            <span class="kor">{line["ko"]}</span><br><br>
            <b>Easy Meaning:</b> {line["easy"]}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔑 핵심 표현")

    for i, item in enumerate(key_expressions, start=1):
        st.markdown(f"""
        <div class="line-box">
            <b>{i}. {item["word"]}</b><br>
            <span class="kor">{item["ko"]}</span><br><br>
            <b>Example:</b> {item["example"]}
        </div>
        """, unsafe_allow_html=True)

        st.caption("🔊 TTS 듣기")
        show_tts_audio(item["word"])

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TAB 6 CERTIFICATE
# =========================

with tab6:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏆 인증서</div>', unsafe_allow_html=True)

    certificate_missions = ["blank", "matching", "grammar"]

    completed_count = sum(
        1
        for mission in certificate_missions
        if st.session_state.batman_complete.get(mission, False)
    )

    mission_labels = {
        "blank": "🎧 대사 빈칸",
        "matching": "🧩 대사 연결",
        "grammar": "📘 문법"
    }

    st.markdown(
        f"""
        <div class="line-box">
            <b>Mission Progress:</b> {completed_count} / 3 completed<br>
            <span class="kor">
                대사 빈칸의 모든 문제 확인 · 대사 연결 6쌍 완성 · 문법 전체 정답을 모두 완료하면
                PDF 인증서를 저장할 수 있습니다.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    for mission in certificate_missions:
        if st.session_state.batman_complete.get(mission, False):
            st.success(f"{mission_labels[mission]} 완료 ✅")
        else:
            st.info(f"{mission_labels[mission]} 미완료")

    if completed_count == 3:
        st.markdown(
            """
            <div class="success-box">
                🎉 Batman English Mission 임무를 완성하셨습니다.<br>
                🦇 You are Gotham's English Guardian!
            </div>
            """,
            unsafe_allow_html=True
        )

        st.balloons()
        show_batman_pdf_download()

    else:
        st.warning(
            "대사 빈칸, 대사 연결, 문법 활동을 모두 완료하면 "
            "PDF 인증서 다운로드 버튼이 나타납니다."
        )

    st.markdown('</div>', unsafe_allow_html=True)
