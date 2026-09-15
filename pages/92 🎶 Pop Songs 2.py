import streamlit as st
import streamlit.components.v1 as components
import random
import html
import re
import json
import uuid
import io
import os
import base64
from datetime import datetime
from gtts import gTTS
from urllib.parse import quote

st.set_page_config(page_title="Pop Song Master Class", page_icon="🎵", layout="wide")

st.markdown("""
<style>
.stApp { background-color:#ffffff; color:#1e293b; }
.main-title {
    background: linear-gradient(135deg,#eef2ff,#f0f9ff,#fdf2f8);
    padding: 25px;
    border-radius: 18px;
    border: 2px solid #6366f1;
    text-align: center;
    color: #3730a3;
    margin-bottom: 22px;
}
.info-box {
    background-color:#f8fafc;
    padding:34px 38px;
    border-radius:22px;
    border:2px solid #cbd5e1;
    line-height:2.1;
    margin-bottom:26px;
    font-size:1.35rem;
}
.info-box h3 {
    color:#4338ca;
    border-bottom:4px solid #6366f1;
    padding-bottom:14px;
    margin-bottom:22px;
    font-size:2.4rem;
    font-weight:900;
}
.info-box p {
    font-size:1.35rem;
    line-height:2.1;
    color:#1e293b;
    margin-bottom:20px;
}
.info-box p {
    font-size:1.35rem;
    line-height:2.1;
    color:#1e293b;
    margin-bottom:20px;
}
.lyrics-container {
    padding:14px 20px;
    border-left:5px solid #6366f1;
    margin-bottom:10px;
    background-color:#f8fafc;
    border-radius:0 12px 12px 0;
}
.eng-line { font-size:1.08rem; font-weight:800; color:#1e3a8a; }
.kor-sub { font-size:0.95rem; color:#64748b; margin-top:5px; line-height:1.6; }
.quiz-box { background-color:#f0f9ff; padding:20px; border-radius:18px; border:1px solid #bae6fd; margin-top:22px; margin-bottom:20px; }
.score-box { background:linear-gradient(135deg,#dcfce7,#bbf7d0); padding:18px; border-radius:18px; border:1px solid #86efac; margin-top:18px; text-align:center; font-size:1.15rem; font-weight:900; }
.wrong-box { background:#fff7ed; padding:15px; border-radius:14px; border:1px solid #fdba74; margin-top:10px; }
.game-card { background:linear-gradient(135deg,#eef2ff,#f8fafc); border:1px solid #c7d2fe; border-radius:18px; padding:20px; margin-bottom:18px; }
.big-guide { font-size:1.12rem; font-weight:800; color:#475569; line-height:1.7; }
.matching-box { background:linear-gradient(135deg,#eef2ff 0%,#f0f9ff 50%,#fdf2f8 100%); padding:24px; border-radius:20px; border:1px solid #c7d2fe; margin-top:18px; margin-bottom:22px; }
.matching-title { font-size:2rem; font-weight:900; color:#4338ca; margin-bottom:10px; }
.selected-card-notice { background-color:#fef3c7; padding:14px 16px; border-radius:14px; border:1px solid #facc15; color:#92400e; font-size:1.05rem; font-weight:900; margin-bottom:16px; }
.feedback-ko { background:#fefce8; border:1px solid #fde68a; padding:18px; border-radius:16px; line-height:1.8; margin-top:14px; }
.feedback-en { background:#eff6ff; border:1px solid #bfdbfe; padding:18px; border-radius:16px; line-height:1.8; margin-top:14px; }
.advice-box { background:#f0fdf4; border:1px solid #bbf7d0; padding:18px; border-radius:16px; line-height:1.8; margin-top:14px; }

/* 배경 학습 전용 큰 글씨 카드 */
.bg-card {
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
    padding: 34px 38px;
    border-radius: 24px;
    border: 2px solid #c7d2fe;
    margin-bottom: 26px;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.08);
}
.bg-title {
    font-size: 2.35rem;
    font-weight: 900;
    color: #3730a3;
    margin-bottom: 22px;
    padding-bottom: 14px;
    border-bottom: 4px solid #6366f1;
}
.bg-p {
    font-size: 1.35rem;
    line-height: 2.05;
    color: #1e293b;
    margin-bottom: 18px;
    font-weight: 560;
}
.bg-key {
    color: #1e3a8a;
    font-weight: 900;
}

</style>
""", unsafe_allow_html=True)


def clean_text_for_display(text):
    return html.escape(str(text).strip())

def safe_key(text):
    return re.sub(r"[^a-zA-Z0-9가-힣_]+", "_", text)

def shuffle_options(options, seed):
    rng = random.Random(seed)
    options = list(options)
    rng.shuffle(options)
    return options


def normalize_answer(text):
    """학생 답안 비교를 조금 관대하게 하기 위한 정리 함수입니다."""
    return str(text).strip().lower().replace(" ", "").replace("/", "")


def is_correct_korean_answer(user_answer, correct_answer):
    """한국어 뜻 입력을 너무 빡빡하지 않게 비교합니다."""
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
    """현재 활동 입력값과 채점 결과를 초기화합니다."""
    if isinstance(prefixes, str):
        prefixes = [prefixes]

    for key in list(st.session_state.keys()):
        if any(str(key).startswith(prefix) for prefix in prefixes):
            del st.session_state[key]


@st.cache_data(show_spinner=False)
def make_key_expression_tts(text, lang="en"):
    """Key Expression 듣기용 mp3 bytes를 만듭니다.
    Google Translate TTS URL을 직접 걸면 Streamlit Cloud/브라우저에서 재생이 막히는 경우가 있어
    gTTS로 mp3를 생성한 뒤 st.audio로 재생합니다.
    """
    safe_text = str(text).strip()
    if not safe_text:
        return b""
    fp = io.BytesIO()
    tts = gTTS(text=safe_text, lang=lang, slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def show_key_expression_audio(text, lang="en"):
    """Key Expression 오디오 플레이어를 안정적으로 표시합니다."""
    safe_text = str(text).strip()
    if not safe_text:
        return
    try:
        audio_bytes = make_key_expression_tts(safe_text, lang=lang)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.warning("음성 재생을 준비하지 못했습니다. requirements.txt에 gTTS가 있는지 확인해 주세요.")
        st.caption(f"오류 내용: {e}")




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


def make_mission_pdf(song_title, activity_name, detail_text=""):
    """활동 완료 인증 PDF를 만듭니다. reportlab이 없으면 앱 화면에 안내를 띄웁니다."""
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

    # PDF에서 한글이 네모(□□□)로 깨지지 않도록 ReportLab 내장 CJK CID 폰트를 먼저 사용합니다.
    # Streamlit Cloud에 별도 한글 폰트 파일이 없어도 HYGothic-Medium은 한글 표시가 안정적입니다.
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
                font_name = "Helvetica"
                bold_font_name = "Helvetica-Bold"

    activity_name = str(activity_name).strip()
    mission_title = f"{activity_name} 임무 완성"
    mission_sentence = f"{activity_name} 임무를 완성하셨습니다."

    c.setFillColor(colors.HexColor("#eef2ff"))
    c.roundRect(18 * mm, 24 * mm, width - 36 * mm, height - 48 * mm, 10 * mm, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.roundRect(28 * mm, 38 * mm, width - 56 * mm, height - 76 * mm, 8 * mm, fill=1, stroke=0)

    c.setStrokeColor(colors.HexColor("#6366f1"))
    c.setLineWidth(2)
    c.roundRect(28 * mm, 38 * mm, width - 56 * mm, height - 76 * mm, 8 * mm, fill=0, stroke=1)

    # 학생이 저장한 PDF만 봐도 어떤 활동 완료증인지 바로 알 수 있도록
    # 영어 MISSION COMPLETE보다 활동명을 가장 크게 보여 줍니다.
    c.setFillColor(colors.HexColor("#14532d"))
    c.setFont(bold_font_name, 27)
    c.drawCentredString(width / 2, height - 72 * mm, mission_title)

    c.setFillColor(colors.HexColor("#3730a3"))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 86 * mm, "MISSION COMPLETE")

    c.setFillColor(colors.HexColor("#14532d"))
    c.setFont(bold_font_name, 18)
    c.drawCentredString(width / 2, height - 103 * mm, mission_sentence)

    c.setFillColor(colors.HexColor("#1e293b"))
    c.setFont(font_name, 15)
    c.drawCentredString(width / 2, height - 126 * mm, f"노래: {song_title}")
    c.drawCentredString(width / 2, height - 139 * mm, f"완료 활동: {activity_name}")

    if detail_text:
        c.setFillColor(colors.HexColor("#475569"))
        c.setFont(font_name, 12)
        safe_detail = str(detail_text).replace("\n", " ")[:90]
        c.drawCentredString(width / 2, height - 154 * mm, safe_detail)

    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont(font_name, 11)
    now_text = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.drawCentredString(width / 2, 62 * mm, f"완료 시간: {now_text}")
    c.drawCentredString(width / 2, 52 * mm, "이 PDF를 저장한 뒤 선생님께 보여 주세요.")

    c.setStrokeColor(colors.HexColor("#6366f1"))
    c.setLineWidth(2.5)
    c.circle(width / 2, 86 * mm, 16 * mm, fill=0, stroke=1)
    # 폰트와 관계없이 체크 표시가 보이도록 선으로 직접 그립니다.
    c.line(width / 2 - 7 * mm, 86 * mm, width / 2 - 2 * mm, 80 * mm)
    c.line(width / 2 - 2 * mm, 80 * mm, width / 2 + 8 * mm, 93 * mm)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def show_mission_pdf_download(song_choice, activity_name, mission_key, detail_text="", big=False, show_message=True):
    """완료 인증 PDF 다운로드 버튼을 보여 줍니다."""
    activity_label = clean_text_for_display(activity_name)

    if show_message:
        st.markdown(
            f"""
            <div style="background:linear-gradient(135deg,#dcfce7,#bbf7d0); padding:20px; border-radius:18px; border:2px solid #86efac; margin-top:18px; text-align:center;">
                <div style="font-size:1.45rem; font-weight:1000; color:#14532d;">🎉 {activity_label} 임무를 완성하셨습니다.</div>
                <div style="font-size:1.02rem; font-weight:850; color:#166534; margin-top:6px;">
                    PDF에는 완료한 활동명이 <b>{activity_label}</b>로 기록됩니다. 아래 버튼을 눌러 완료 인증 PDF를 저장하고, 나중에 선생님께 보여 주세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background:linear-gradient(135deg,#eef2ff,#f0f9ff,#fdf2f8); padding:24px; border-radius:22px; border:2px solid #6366f1; margin-top:18px; text-align:center;">
                <div style="font-size:1.55rem; font-weight:1000; color:#3730a3;">📄 {activity_label} PDF 인증서 저장</div>
                <div style="font-size:1.05rem; font-weight:850; color:#475569; margin-top:8px;">
                    아래 버튼을 눌러 <b>{activity_label}</b> 완료 인증서를 저장하세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    pdf_bytes = make_mission_pdf(song_choice, activity_name, detail_text)

    if pdf_bytes:
        file_name = f"mission_complete_{safe_key(song_choice)}_{safe_key(activity_name)}.pdf"

        if big:
            st.markdown(
                """
                <style>
                div[data-testid="stDownloadButton"] button {
                    min-height: 68px !important;
                    font-size: 1.25rem !important;
                    font-weight: 1000 !important;
                    border-radius: 18px !important;
                    border: 2px solid #4f46e5 !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

        st.download_button(
            "📄 PDF 인증서 다운받기" if big else "📄 완료 인증 PDF 저장",
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf",
            key=f"download_{mission_key}",
            use_container_width=True
        )
    else:
        st.warning("PDF 저장 기능을 사용하려면 requirements.txt에 reportlab을 추가해 주세요. 예: reportlab>=4.0.0")



def show_key_expression_learning_in_lyrics(song_choice, data, max_words=10):
    """Key Expression을 문제 없이 학습 자료로 보여주고 듣기를 제공합니다."""
    expressions = list(data.get("key_expressions", []))[:max_words]

    if not expressions:
        return

    st.markdown("---")
    st.subheader("⭐ Key Expression 학습")
    st.markdown(
        '<div class="game-card"><div class="big-guide">'
        '중요 표현의 뜻을 먼저 확인하고, 영어 표현을 들어 보세요.<br>'
        '여기서는 문제를 풀지 않고, 듣기와 뜻 확인만 합니다.'
        '</div></div>',
        unsafe_allow_html=True
    )

    all_text = " . ".join(en for en, _ in expressions)
    st.markdown("#### 🎧 전체 표현 듣기")
    show_key_expression_audio(all_text, lang="en")

    for i, (en, ko) in enumerate(expressions, start=1):
        st.markdown(
            f"""
            <div style="background:linear-gradient(135deg,#f8fafc,#eff6ff); padding:18px 20px; border-radius:18px; border:1px solid #bfdbfe; margin-bottom:14px;">
                <div style="font-size:1.18rem; font-weight:950; color:#1e3a8a; margin-bottom:6px;">
                    {i}. {clean_text_for_display(en)}
                </div>
                <div style="font-size:1.02rem; font-weight:850; color:#475569; margin-bottom:8px;">
                    {clean_text_for_display(ko)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        show_key_expression_audio(en, lang="en")


def build_integrated_quiz(song_choice, data, total_questions=15):
    """내용 이해 문제 8개 + Key Expression 문제 7개를 합쳐 15문항 종합 퀴즈를 만듭니다."""
    quiz_key = safe_key(song_choice)
    combined = []

    for i, item in enumerate(data.get("quiz", []), start=1):
        q = item["q"]
        q_text = q if str(q).strip().startswith(str(i)) else f"{i}. {q}"
        combined.append({
            "kind": "내용 이해",
            "q": q_text,
            "options": item["options"],
            "answer": item["answer"],
            "explain": "가사와 배경 내용을 다시 확인해 보세요."
        })

    expressions = list(data.get("key_expressions", []))
    all_english_options = [en for en, _ in expressions]
    all_korean_options = [ko for _, ko in expressions]
    need_key_count = max(0, total_questions - len(combined))

    for i, (en, ko) in enumerate(expressions[:need_key_count], start=1):
        direction_rng = random.Random(f"{quiz_key}_integrated_direction_{i}")
        direction = direction_rng.choice(["en_to_ko", "ko_to_en"])
        rng = random.Random(f"{quiz_key}_integrated_key_{i}")

        if direction == "en_to_ko":
            distractors = [x for x in all_korean_options if x != ko]
            wrongs = rng.sample(distractors, k=min(3, len(distractors)))
            options = wrongs + [ko]
            combined.append({
                "kind": "Key Expression",
                "q": f"'{en}'의 뜻으로 알맞은 것은?",
                "options": options,
                "answer": ko,
                "explain": f"{en} = {ko}"
            })
        else:
            distractors = [x for x in all_english_options if x != en]
            wrongs = rng.sample(distractors, k=min(3, len(distractors)))
            options = wrongs + [en]
            combined.append({
                "kind": "Key Expression",
                "q": f"'{ko}'에 맞는 영어 표현은?",
                "options": options,
                "answer": en,
                "explain": f"{en} = {ko}"
            })

    return combined[:total_questions]


def show_integrated_quiz_tab(song_choice, data):
    """가사 뒤에 나오는 이해도 퀴즈입니다. 기존 종합 퀴즈 문항을 모두 사용합니다."""
    st.subheader("✅ 이해도 퀴즈")
    st.markdown(
        '<div class="game-card"><div class="big-guide">'
        '가사를 읽은 뒤 문제를 풀어 보세요.<br>'
        '기존 종합 퀴즈 문항을 모두 넣었습니다. 총 15문제 중 12문제 이상 맞히면 통과입니다.'
        '</div></div>',
        unsafe_allow_html=True
    )

    key_key = safe_key(song_choice)
    pass_score = 12
    questions = build_integrated_quiz(song_choice, data, total_questions=15)
    user_answers = []

    for i, item in enumerate(questions, start=1):
        # item['q'] 안에 이미 1. / 2. 같은 번호가 들어 있어도
        # 화면에는 번호가 한 번만 보이도록 기존 번호를 제거한 뒤 다시 붙입니다.
        question_text = re.sub(r"^\s*\d+\s*[\.\)]\s*", "", str(item["q"]).strip())

        st.markdown(
            f"""
            <div style="background:#ffffff; padding:16px 18px; border-radius:18px; border:1px solid #e2e8f0; margin-top:18px;">
                <div style="font-size:0.95rem; font-weight:900; color:#6366f1; margin-bottom:6px;">{clean_text_for_display(item['kind'])}</div>
                <div style="font-size:1.12rem; font-weight:950; color:#1e293b; line-height:1.6;">{i}. {clean_text_for_display(question_text)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        options = shuffle_options(item["options"], seed=f"{key_key}_integrated_options_{i}")
        picked = st.radio(
            "정답을 고르세요.",
            options,
            key=f"integrated_quiz_{key_key}_{i}",
            index=None,
            label_visibility="collapsed"
        )
        user_answers.append((item, picked))

    c1, c2 = st.columns(2)
    with c1:
        submit_quiz = st.button("종합 퀴즈 정답 확인", key=f"integrated_quiz_submit_{key_key}", use_container_width=True)
    with c2:
        if st.button("종합 퀴즈 다시 풀기", key=f"integrated_quiz_reset_{key_key}", use_container_width=True):
            for k in list(st.session_state.keys()):
                if k.startswith(f"integrated_quiz_{key_key}_"):
                    del st.session_state[k]
            st.rerun()

    if submit_quiz:
        score = sum(1 for item, picked in user_answers if picked == item["answer"])
        st.markdown(f'<div class="score-box">점수: {score} / {len(questions)}</div>', unsafe_allow_html=True)

        if score >= pass_score:
            st.success(f"통과했습니다! {len(questions)}문제 중 {score}문제를 맞혔습니다.")
            st.session_state[f"mission_{key_key}_lyrics_quiz"] = True
            st.session_state[f"mission_{key_key}_lyrics_quiz_detail"] = f"가사 이해도 퀴즈 완료 / 점수: {score}/{len(questions)}"
            st.balloons()
        else:
            st.warning(f"아직 통과 기준에 부족합니다. 통과 기준은 {pass_score}/{len(questions)} 이상입니다.")

        for idx, (item, picked) in enumerate(user_answers, start=1):
            answer = item["answer"]
            explain = item.get("explain", "")
            if picked == answer:
                st.success(f"{idx}번 정답입니다. ✅")
            else:
                st.markdown(
                    f'<div class="wrong-box"><b>{idx}번</b> 다시 확인해 보세요.<br>'
                    f'내가 고른 답: {clean_text_for_display(picked) if picked else "선택 안 함"}<br>'
                    f'정답: <b>{clean_text_for_display(answer)}</b><br>'
                    f'{clean_text_for_display(explain)}</div>',
                    unsafe_allow_html=True
                )


    if st.session_state.get(f"mission_{key_key}_lyrics_quiz"):
        st.markdown("---")
        st.markdown("## 📄 가사와 이해도 퀴즈 PDF 인증서")

        show_mission_pdf_download(
            song_choice,
            "가사 이해도 퀴즈",
            f"{key_key}_lyrics_quiz_bottom",
            st.session_state.get(
                f"mission_{key_key}_lyrics_quiz_detail",
                "가사 이해도 퀴즈 활동 완료"
            ),
            big=True,
            show_message=False
        )


def check_target_grammar_sentence(target, sentence):
    """학생이 직접 쓴 문장이 오늘의 오늘 배운 표현을 포함하는지 간단히 검사합니다.
    너무 엄격한 문법 채점기가 아니라, 핵심 구조가 들어갔는지 확인하는 용도입니다.
    """
    raw = str(sentence).strip()
    raw = raw.replace("’", "'").replace("‘", "'").replace("`", "'")
    s = re.sub(r"\s+", " ", raw)
    low = s.lower().strip()

    if not raw:
        return False, "먼저 영어 문장을 써 보세요.", "오늘 배운 문법 표현을 넣어 한 문장으로 써 보세요."

    if re.search(r"[가-힣]", raw):
        return False, "영어 문장으로 써 보세요.", "한국어가 섞여 있습니다. 오늘 배운 영어 표현을 사용해 보세요."

    if len(re.findall(r"[a-zA-Z']+", raw)) < 3:
        return False, "문장이 너무 짧습니다.", "주어, 동사, 내용을 넣어 조금 더 완전한 문장으로 써 보세요."

    def ok(msg="좋아요. 오늘 배운 표현 형태이 문장 안에 잘 들어갔습니다."):
        return True, msg, "철자와 대문자, 마침표만 한 번 더 확인해 보세요."

    def no(hint):
        return False, "오늘 배운 표현 형태이 아직 분명하게 보이지 않습니다.", hint

    target = str(target).strip()

    if target == "Let + 사람/명사 + 동사":
        if re.search(r"^(do not|don't)\s+let\s+\w+\s+\w+", low) or re.search(r"^let\s+\w+\s+\w+", low):
            if re.search(r"\blet\s+\w+\s+to\s+", low):
                return no("Let 뒤에는 'to + 동사'가 아니라 동사를 바로 씁니다. 예: Let me try.")
            return ok()
        return no("Let + 사람/명사 + 동사 구조를 써 보세요. 예: Let me try.")

    if target == "I'm sorry for + 명사 또는 -ing 형태":
        if re.search(r"\b(i am|i'm)\s+sorry\s+for\s+", low):
            after = re.split(r"\bsorry\s+for\s+", low, maxsplit=1)[-1]
            if after and not re.match(r"(go|do|make|break|call|be|come|say|tell|play|study)\b", after):
                return ok()
            return no("for 뒤에는 명사나 -ing 형태를 쓰는 것이 자연스럽습니다. 예: I'm sorry for being late.")
        return no("I'm sorry for + 명사 또는 -ing 형태 구조를 써 보세요. 예: I'm sorry for making a mistake.")

    if target == "can + 동사":
        if re.search(r"\bcan\s+(?!to\b)\w+", low):
            return ok()
        return no("can 뒤에는 동사를 씁니다. 예: I can help you.")

    if target == "won't + 동사":
        if re.search(r"\bwon't\s+(?!to\b)\w+", low):
            return ok()
        return no("won't + 동사 구조를 써 보세요. 예: I won't give up.")

    if target == "I don't know why + 문장":
        if re.search(r"\bi\s+don't\s+know\s+why\s+\w+\s+\w+", low):
            return ok()
        return no("I don't know why 뒤에는 주어 + 동사/상태가 이어집니다. 예: I don't know why I feel sad.")

    if target == "When + 주어 + 동사/상태":
        if re.search(r"\bwhen\s+\w+\s+\w+", low):
            return ok()
        return no("When + 주어 + 동사/상태 구조를 써 보세요. 예: When I feel tired, I rest.")

    if target == "Tell + 사람 + 내용":
        if re.search(r"\btell\s+(me|you|him|her|us|them|[a-z]+)\s+\w+", low):
            return ok()
        return no("Tell + 사람 + 내용 구조를 써 보세요. 예: Tell me your dream.")

    if target == "will + 동사":
        if re.search(r"\bwill\s+(?!to\b)\w+", low):
            return ok()
        return no("will + 동사 구조를 써 보세요. 예: I will remember you.")

    if target == "It's hard to + 동사":
        if re.search(r"\b(it is|it's)\s+hard\s+to\s+\w+", low):
            return ok()
        return no("It's hard to + 동사 구조를 써 보세요. 예: It's hard to say goodbye.")

    if target == "used to + 동사":
        if re.search(r"\bused\s+to\s+\w+", low):
            return ok()
        return no("used to + 동사 구조를 써 보세요. 예: I used to play outside.")

    if target == "like + 명사":
        if re.search(r"\blike\s+\w+", low):
            if re.search(r"\b(i|you|we|they)\s+like\s+", low):
                return no("여기서는 '좋아하다'가 아니라 '~처럼/~같은' 뜻의 like를 연습합니다. 예: It feels like home.")
            return ok()
        return no("~처럼/~같은 의미의 like + 명사 구조를 써 보세요. 예: It feels like home.")

    if target == "I'll + 동사":
        if re.search(r"\b(i'll|i\s+will)\s+(?!to\b)\w+", low):
            return ok()
        return no("I'll + 동사 구조를 써 보세요. 예: I'll try again.")

    if target == "I think + 문장 / I don't think so":
        if re.search(r"\bi\s+don't\s+think\s+so\b", low) or re.search(r"\bi\s+think\s+\w+\s+\w+", low):
            return ok()
        return no("I think + 문장 또는 I don't think so를 써 보세요. 예: I think English is fun.")

    if target == "can't + 동사":
        if re.search(r"\b(can't|cannot)\s+(?!to\b)\w+", low):
            return ok()
        return no("can't + 동사 구조를 써 보세요. 예: I can't sleep tonight.")

    if target == "I have been + -ing 형태":
        if re.search(r"\b(i\s+have|i've)\s+been\s+\w+ing\b", low):
            return ok()
        return no("I have been + -ing 형태 구조를 써 보세요. 예: I have been studying English.")

    if target == "want + 명사 / want to + 동사":
        if re.search(r"\bwant\s+to\s+\w+", low):
            return ok("좋아요. 뒤에 동사가 올 때 want to + 동사 형태를 잘 썼습니다.")
        if re.search(r"\bwant\s+(love|peace|money|time|help|food|water|a\s+\w+|the\s+\w+|my\s+\w+|your\s+\w+)\b", low):
            return ok("좋아요. 뒤에 명사가 올 때 want + 명사 형태를 잘 썼습니다.")
        if re.search(r"\bwant\s+(put|help|see|go|study|try|meet|play|make|watch|listen|eat|drink|be|do)\b", low):
            return no("뒤에 동사가 올 때는 want 뒤에 to를 넣어 보세요. 예: I want to help you.")
        if re.search(r"\bwant\s+to\s+(love|peace|money|time|food|water)\b", low):
            return no("love, peace, time 같은 명사가 바로 올 때는 want 뒤에 to를 쓰지 않습니다. 예: I want peace.")
        return no("want + 명사 또는 want to + 동사 구조를 써 보세요. 예: I want peace. / I want to help you.")




    if target == "Every + 명사 + 주어 + 동사":
        if re.search(r"^every\s+\w+(?:\s+\w+)?\s+(i|you|we|they|he|she|it|[a-z]+)\s+\w+", low):
            return ok("좋아요. Every + 명사 + 주어 + 동사 형태를 잘 썼습니다.")
        if re.search(r"^every\s+\w+\s+to\s+\w+", low):
            return no("Every 뒤에는 'to + 동사'가 아니라 명사와 문장 형태를 이어 씁니다. 예: Every word you say.")
        return no("Every + 명사 + 주어 + 동사 구조를 써 보세요. 예: Every word you say.")

    if target == "Let's + 동사":
        if re.search(r"\b(let's|let us)\s+(?!to\b)[a-zA-Z']+", low):
            return ok("좋아요. 함께 하자고 제안하는 Let's + 동사 형태를 잘 썼습니다.")
        if re.search(r"\b(let's|let us)\s+to\s+[a-zA-Z']+", low):
            return no("Let's 뒤에는 to를 쓰지 않고 동사를 바로 씁니다. 예: Let's skip the club.")
        return no("Let's + 동사 구조를 써 보세요. 예: Let's study English. / Let's skip the club.")

    if target == "gonna be + 형용사":
        if re.search(r"\b(gonna|going\s+to)\s+be\s+\w+", low):
            return ok("좋아요. 앞으로 어떤 모습이 될지 말하는 gonna be + 형용사 형태를 잘 썼습니다.")
        return no("gonna be + 형용사 구조를 써 보세요. 예: We're gonna be golden.")

    if target == "make + 사람/명사 + 형용사/동사":
        if re.search(r"\b(make|makes|made)\s+\w+(?:\s+\w+)?\s+to\s+\w+", low):
            return no("make 뒤에는 '사람/명사 + to + 동사'가 아니라 사람/명사 + 형용사 또는 동사를 씁니다. 예: You make me smile.")
        if re.search(r"\b(make|makes|made)\s+(me|you|him|her|us|them|my\s+\w+|your\s+\w+|our\s+\w+|the\s+\w+|[a-z]+)\s+(?!to\b)\w+", low):
            return ok()
        return no("make + 사람/명사 + 형용사/동사 구조를 써 보세요. 예: You make me happy. / You make me smile.")

    return True, "문장을 확인했습니다.", "오늘 배운 표현이 자연스럽게 들어갔는지 한 번 더 읽어 보세요."



GRAMMAR_POINTS = {'22. Die for You - The Weeknd': {'target': 'would + 동사',
                                  'examples': ['I would die for you.',
                                               'I would stay for you.',
                                               'I would wait for you.',
                                               'I would help you.',
                                               'I would be there for you.'],
                                  'frequent_options': ['would', 'can', 'used to', 'will'],
                                  'frequent_answer': 'would',
                                  'form_options': ['would + 동사', 'would + to + 동사', 'would + -ing', 'would + 과거형'],
                                  'form_answer': 'would + 동사',
                                  'meaning_examples': [('I would die for you.', '나는 너를 위해서라면 죽을 수도 있어.'),
                                                       ('I would help you.', '나는 너를 위해서라면 도울 거야.')],
                                  'meaning_options': ['~할 것이다 / ~할 수도 있다', '~할 수 있다', '예전에 ~했다', '~하고 있다'],
                                  'meaning_answer': '~할 것이다 / ~할 수도 있다',
                                  'rule_answer': 'would + 동사 = ~할 것이다 / ~할 수도 있다',
                                  'rule_options': ['would + 동사 = ~할 것이다 / ~할 수도 있다',
                                                   'would + 과거형 = 어제 ~했다',
                                                   'would + ing = ~하고 있다',
                                                   'would + to + 동사 = ~해야 한다'],
                                  'practice': [('빈칸: I would _____ for you.',
                                                ['dies', 'died', 'die', 'dying'],
                                                'die',
                                                'would 뒤에는 동사원형이 옵니다.'),
                                               ('맞는 문장은?',
                                                ['I would to die for you.',
                                                 'I would dying for you.',
                                                 'I would died for you.',
                                                 'I would die for you.'],
                                                'I would die for you.',
                                                'would + 동사원형'),
                                               ('I would die for you.의 뜻은?',
                                                ['나는 너를 위해서라면 죽을 수도 있어.', '나는 너를 잊고 싶어.', '나는 너와 멀리 떨어져 있어.', '나는 너를 사랑하지 않아.'],
                                                '나는 너를 위해서라면 죽을 수도 있어.',
                                                '강한 사랑과 헌신을 나타냅니다.'),
                                               ('빈칸: I would _____ you.',
                                                ['helps', 'helped', 'help', 'helping'],
                                                'help',
                                                'would + 동사원형'),
                                               ('알맞은 구조는?',
                                                ['would + 과거형', 'would + 동사', 'would + ing', 'would + to + 동사'],
                                                'would + 동사',
                                                'would 뒤에는 동사가 옵니다.')],
                                  'sentence_prefix': 'I would',
                                  'sentence_choices': ['help you',
                                                       'stay with you',
                                                       'wait for you',
                                                       'be there for you',
                                                       'die for you'],
                                  'sentence_suffix': ''},
 '15. Counting Stars - OneRepublic': {'target': 'would + 동사',
                                      'examples': ['I would die for you.',
                                                   'I would stay for you.',
                                                   'I would wait for you.',
                                                   'I would help you.',
                                                   'I would be there for you.'],
                                      'frequent_options': ['would', 'can', 'used to', 'will'],
                                      'frequent_answer': 'would',
                                      'form_options': ['would + 동사', 'would + to + 동사', 'would + -ing', 'would + 과거형'],
                                      'form_answer': 'would + 동사',
                                      'meaning_examples': [('I would die for you.', '나는 너를 위해서라면 죽을 수도 있어.'),
                                                           ('I would help you.', '나는 너를 위해서라면 도울 거야.')],
                                      'meaning_options': ['~할 것이다 / ~할 수도 있다', '~할 수 있다', '예전에 ~했다', '~하고 있다'],
                                      'meaning_answer': '~할 것이다 / ~할 수도 있다',
                                      'rule_answer': 'would + 동사 = ~할 것이다 / ~할 수도 있다',
                                      'rule_options': ['would + 동사 = ~할 것이다 / ~할 수도 있다',
                                                       'would + 과거형 = 어제 ~했다',
                                                       'would + ing = ~하고 있다',
                                                       'would + to + 동사 = ~해야 한다'],
                                      'practice': [('빈칸: I would _____ for you.',
                                                    ['dies', 'died', 'die', 'dying'],
                                                    'die',
                                                    'would 뒤에는 동사원형이 옵니다.'),
                                                   ('맞는 문장은?',
                                                    ['I would to die for you.',
                                                     'I would dying for you.',
                                                     'I would died for you.',
                                                     'I would die for you.'],
                                                    'I would die for you.',
                                                    'would + 동사원형'),
                                                   ('I would die for you.의 뜻은?',
                                                    ['나는 너를 위해서라면 죽을 수도 있어.',
                                                     '나는 너를 잊고 싶어.',
                                                     '나는 너와 멀리 떨어져 있어.',
                                                     '나는 너를 사랑하지 않아.'],
                                                    '나는 너를 위해서라면 죽을 수도 있어.',
                                                    '강한 사랑과 헌신을 나타냅니다.'),
                                                   ('빈칸: I would _____ you.',
                                                    ['helps', 'helped', 'help', 'helping'],
                                                    'help',
                                                    'would + 동사원형'),
                                                   ('알맞은 구조는?',
                                                    ['would + 과거형', 'would + 동사', 'would + ing', 'would + to + 동사'],
                                                    'would + 동사',
                                                    'would 뒤에는 동사가 옵니다.')],
                                      'sentence_prefix': 'I would',
                                      'sentence_choices': ['help you',
                                                           'stay with you',
                                                           'wait for you',
                                                           'be there for you',
                                                           'die for you'],
                                      'sentence_suffix': ''}}



def show_song_grammar_tab(song_choice, data):
    """각 노래별로 자주 등장하고 쉬운 문법 포인트를 발견하게 하는 탭입니다."""
    grammar_key = safe_key(song_choice)
    prefix = f"song_grammar_{grammar_key}_"
    g = GRAMMAR_POINTS.get(song_choice, GRAMMAR_POINTS["15. Counting Stars - OneRepublic"])

    st.subheader("🎯 Grammar")

    st.markdown("### 1. 표현 찾기")
    example_html = "<br>".join(clean_text_for_display(x) for x in g["examples"])
    st.markdown(
        f"""
        <div style="background:#f8fafc; padding:22px; border-radius:18px; border-left:6px solid #6366f1; line-height:2.15; font-size:1.22rem;">
            {example_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    frequent = st.radio(
        "자주 등장하거나 비슷하게 반복되는 표현은 무엇인가요?",
        g["frequent_options"],
        key=f"{prefix}frequent",
        horizontal=True
    )

    if st.button("확인", key=f"{prefix}frequent_check", use_container_width=True):
        if frequent == g["frequent_answer"]:
            st.success("정답입니다.")
        else:
            st.error("다시 보세요. 여러 문장에 반복되는 표현이 있습니다.")

    st.markdown("---")
    st.markdown("### 2. 표현 형태 찾기")

    form = st.radio(
        "위 표현들의 공통 형태은 무엇인가요?",
        g["form_options"],
        key=f"{prefix}form",
        horizontal=False
    )

    if st.button("확인", key=f"{prefix}form_check", use_container_width=True):
        if form == g["form_answer"]:
            st.success("정답입니다.")
        else:
            st.error("다시 보세요. 반복되는 표현 뒤의 단어 형태을 비교해 보세요.")

    st.markdown("---")
    st.markdown("### 3. 의미 찾기")
    meaning_lines = "<br>".join(
        f"{clean_text_for_display(en)} → {clean_text_for_display(ko)}"
        for en, ko in g["meaning_examples"]
    )
    st.markdown(
        f"""
        <div style="background:#f0f9ff; padding:22px; border-radius:18px; border:1px solid #bae6fd; line-height:2.1; font-size:1.12rem;">
            {meaning_lines}
        </div>
        """,
        unsafe_allow_html=True
    )

    meaning = st.radio(
        "위 문장들의 공통 의미로 가장 알맞은 것은 무엇인가요?",
        g["meaning_options"],
        key=f"{prefix}meaning",
        horizontal=False
    )

    if st.button("확인", key=f"{prefix}meaning_check", use_container_width=True):
        if meaning == g["meaning_answer"]:
            st.success("정답입니다.")
        else:
            st.error("다시 생각해 보세요. 영어 문장과 한국어 뜻을 함께 비교해 보세요.")

    st.markdown("---")
    st.markdown("### 4. 규칙 정리")

    rule = st.radio(
        "지금까지 발견한 말의 규칙을 가장 잘 정리한 것은 무엇인가요?",
        g["rule_options"],
        key=f"{prefix}rule",
        horizontal=False
    )

    if st.button("확인", key=f"{prefix}rule_check", use_container_width=True):
        if rule == g["rule_answer"]:
            st.success("정답입니다.")
            st.balloons()
        else:
            st.error("다시 보세요. 앞에서 찾은 표현과 의미를 연결해 보세요.")

    if st.session_state.get(f"{prefix}rule") == g["rule_answer"]:
        st.markdown(
            f"""
            <div style="background:#f0fdf4; padding:22px; border-radius:20px; border:2px solid #bbf7d0; margin-top:18px;">
                <div style="font-size:1.35rem; font-weight:900; color:#166534; margin-bottom:10px;">
                    발견한 규칙
                </div>
                <div style="font-size:1.2rem; line-height:1.8; color:#1e293b; font-weight:850;">
                    {clean_text_for_display(g['rule_answer'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### 📝 Controlled Practice")

    score = 0
    checked = 0
    questions = g["practice"]

    for i, item in enumerate(questions, start=1):
        q, options, answer, explain = item
        q_key = f"{prefix}cp_{i}"
        check_key = f"{prefix}cp_checked_{i}"
        st.markdown(
            f"""
            <div style="background:#ffffff; padding:16px 18px; border-radius:18px; border:1px solid #e2e8f0; margin-top:16px;">
                <div style="font-size:1.12rem; font-weight:900; color:#1e293b;">{clean_text_for_display(q)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        choice = st.radio(
            "정답을 고르세요.",
            options,
            key=q_key,
            label_visibility="collapsed"
        )
        if st.button("정답 확인", key=f"{prefix}cp_check_btn_{i}"):
            st.session_state[check_key] = choice == answer

        if check_key in st.session_state:
            checked += 1
            if st.session_state[check_key]:
                score += 1
                st.success(f"정답입니다. {explain}")
            else:
                st.error(f"정답: {answer} / {explain}")

    st.markdown(f"### 📊 Grammar Practice 점수: {score}/{len(questions)}")
    st.caption(f"정답 확인을 누른 문제: {checked}/{len(questions)} · 통과 기준: 4/{len(questions)} 이상")

    if checked == len(questions):
        if score >= 4:
            st.success("통과했습니다.")
        else:
            st.warning("다시 풀기로 한 번 더 도전해 보세요.")
    else:
        st.info("모든 문제의 정답 확인을 누르면 점수가 표시됩니다.")

    if checked > 0:
        if st.button("🔄 Grammar Practice 다시 풀기", key=f"{prefix}reset", use_container_width=True):
            reset_keys_by_prefix(prefix)
            st.rerun()

    st.markdown("---")
    st.markdown("### ✍️ My Sentence")

    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#f8fafc,#eff6ff); padding:22px; border-radius:20px; border:1px solid #bfdbfe; margin-bottom:16px;">
            <div style="font-size:1.1rem; font-weight:850; color:#475569; margin-bottom:8px;">
                오늘의 target grammar를 사용해서 영어 문장을 직접 써 보세요.
            </div>
            <div style="font-size:1.35rem; font-weight:950; color:#1e3a8a;">
                {clean_text_for_display(g['target'])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    user_sentence = st.text_area(
        "학생이 직접 쓴 문장",
        placeholder="예: I can help my friend. / I'm sorry for being late.",
        key=f"{prefix}user_sentence",
        height=110
    )

    c_check, c_clear = st.columns([2, 1])
    with c_check:
        if st.button("문법성 검사", key=f"{prefix}my_sentence_check", use_container_width=True):
            is_ok, feedback, advice = check_target_grammar_sentence(g["target"], user_sentence)
            st.session_state[f"{prefix}my_sentence_result"] = {
                "is_ok": is_ok,
                "feedback": feedback,
                "advice": advice,
                "sentence": user_sentence,
            }
    with c_clear:
        if st.button("다시 쓰기", key=f"{prefix}my_sentence_clear", use_container_width=True):
            for k in [f"{prefix}my_sentence_result", f"{prefix}user_sentence"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    result_key = f"{prefix}my_sentence_result"
    if result_key in st.session_state:
        result = st.session_state[result_key]
        if result["is_ok"]:
            st.success(result["feedback"])
            st.balloons()
        else:
            st.error(result["feedback"])
        st.info(result["advice"])

    grammar_complete = (
        st.session_state.get(f"{prefix}frequent") == g["frequent_answer"]
        and st.session_state.get(f"{prefix}form") == g["form_answer"]
        and st.session_state.get(f"{prefix}meaning") == g["meaning_answer"]
        and st.session_state.get(f"{prefix}rule") == g["rule_answer"]
        and checked == len(questions)
        and score >= 4
        and st.session_state.get(result_key, {}).get("is_ok")
    )
    if grammar_complete:
        st.session_state[f"mission_{grammar_key}_grammar"] = True
        st.session_state[f"mission_{grammar_key}_grammar_detail"] = (
            f"Grammar 활동 완료 / Grammar Practice 점수: {score}/{len(questions)}"
        )

    if st.session_state.get(f"mission_{grammar_key}_grammar"):
        st.markdown("---")
        st.markdown("## 📄 Grammar PDF 인증서")

        show_mission_pdf_download(
            song_choice,
            "Grammar",
            f"{grammar_key}_grammar_big",
            st.session_state.get(
                f"mission_{grammar_key}_grammar_detail",
                "Grammar 활동 완료"
            ),
            big=True,
            show_message=False
        )

def try_translate_ko_to_en(korean_text):
    korean_text = str(korean_text).strip()
    if not korean_text:
        return ""
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source="ko", target="en").translate(korean_text)
        translated = str(translated).strip()
        if re.search(r"[가-힣]", translated):
            raise ValueError("Korean remained")
        return translated
    except Exception:
        return (
            "While listening to this song, I looked back on my own memories and emotions. "
            "This reflection was not just about the past; it helped me think about my relationships, choices, and feelings more deeply. "
            "The song reminds me that difficult memories can become meaningful when we try to understand them honestly."
        )


def try_translate_en_to_ko(english_text):
    english_text = str(english_text).strip()
    if not english_text:
        return ""
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source="en", target="ko").translate(english_text)
        translated = str(translated).strip()
        if not re.search(r"[가-힣]", translated):
            raise ValueError("Korean not produced")
        return translated
    except Exception:
        return (
            "이 노래를 들으며 나는 내 기억과 감정을 다시 떠올렸습니다. "
            "처음에는 짧은 생각이었지만, 그 감정을 조금 더 자세히 바라보니 나의 관계, 선택, 그리고 마음을 더 깊이 이해할 수 있었습니다. "
            "이 노래는 음악이 단순한 감상이 아니라 나의 삶을 돌아보게 하는 계기가 될 수 있다는 점을 느끼게 해 줍니다."
        )

def clean_student_korean_answer(text):
    """학생 한국어 원문을 보존하되, 글로 보여 줄 때 어색한 공백과 문장부호만 정리합니다."""
    s = str(text).strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"([.!?。！？])\s*", r"\1 ", s).strip()
    if s and s[-1] not in ".!?。！？요다함음임됨됨다":
        s += "."
    return s


def detect_korean_reflection_focus(text, question="", song_title=""):
    """학생 글과 질문에서 중심 소재와 감정을 추출해 반복 피드백을 줄입니다."""
    raw = f"{text} {question} {song_title}"

    if any(k in raw for k in ["친구", "우정", "짝", "동료", "같이"]):
        topic = "친구와의 관계"
        topic_en = "my friendship"
    elif any(k in raw for k in ["가족", "엄마", "아빠", "부모", "동생", "형", "누나", "언니"]):
        topic = "가족과의 관계"
        topic_en = "my family"
    elif any(k in raw for k in ["꿈", "미래", "진로", "목표", "직업", "성공"]):
        topic = "나의 꿈과 미래"
        topic_en = "my dreams and future"
    elif any(k in raw for k in ["사랑", "좋아", "고백", "이별", "관계"]):
        topic = "사랑과 관계"
        topic_en = "love and relationships"
    elif any(k in raw for k in ["학교", "공부", "영어", "수업", "학생"]):
        topic = "학교생활과 배움"
        topic_en = "my school life and learning"
    elif any(k in raw for k in ["기억", "추억", "옛날", "과거", "예전", "그때"]):
        topic = "과거의 기억"
        topic_en = "an old memory"
    else:
        topic = "내 마음속 감정"
        topic_en = "my own feelings"

    if any(k in raw for k in ["슬프", "아쉽", "후회", "눈물", "그립", "외롭", "힘들", "미안"]):
        feeling = "아쉬움과 그리움"
        feeling_en = "sad and reflective"
    elif any(k in raw for k in ["행복", "기쁘", "좋", "신나", "즐거", "밝"]):
        feeling = "따뜻하고 밝은 감정"
        feeling_en = "warm and happy"
    elif any(k in raw for k in ["위로", "편안", "괜찮", "힘", "응원"]):
        feeling = "위로와 안정감"
        feeling_en = "comforted and encouraged"
    elif any(k in raw for k in ["희망", "용기", "도전", "할 수", "포기"]):
        feeling = "희망과 용기"
        feeling_en = "hopeful and encouraged"
    elif any(k in raw for k in ["걱정", "불안", "무섭", "긴장"]):
        feeling = "걱정과 불안"
        feeling_en = "worried but thoughtful"
    else:
        feeling = "차분한 성찰"
        feeling_en = "thoughtful"

    return topic, topic_en, feeling, feeling_en


def song_reflection_bridge_ko(song_title):
    if "Let It Go" in song_title:
        return "이 노래는 남의 시선 때문에 숨겨 두었던 마음을 조금씩 인정하고, 스스로를 받아들이는 용기를 떠올리게 합니다."
    if "Hello" in song_title:
        return "이 노래는 미처 전하지 못한 말과 시간이 지난 뒤에야 선명해지는 후회의 감정을 떠올리게 합니다."
    if "A Whole New World" in song_title:
        return "이 노래는 익숙한 곳을 벗어나 새로운 세상을 바라볼 때 느끼는 설렘과 두려움을 함께 떠올리게 합니다."
    if "Stand By Me" in song_title:
        return "이 노래는 힘든 순간에도 곁에 있어 주는 사람의 소중함을 생각하게 합니다."
    if "Don't Know Why" in song_title:
        return "이 노래는 이유를 정확히 설명하기 어려운 감정과 선택을 조용히 돌아보게 합니다."
    if "Fix You" in song_title:
        return "이 노래는 지치고 힘든 사람에게 건네는 위로처럼 들리며, 누군가의 응원이 얼마나 큰 힘이 되는지 느끼게 합니다."
    if "Scientist" in song_title:
        return "이 노래는 처음으로 돌아가고 싶은 마음, 그리고 그때 다르게 말하거나 행동했더라면 어땠을까 하는 생각을 떠올리게 합니다."
    if "My Heart Will Go On" in song_title:
        return "이 노래는 떠나간 뒤에도 마음속에 남아 있는 사람과 기억의 힘을 생각하게 합니다."
    if "Counting Stars" in song_title:
        return "이 노래는 돈이나 현실적인 걱정 너머에 있는 꿈, 선택, 미래에 대한 고민을 떠올리게 합니다."
    if "My Universe" in song_title:
        return "이 노래는 서로 다른 세계에 있는 사람도 누군가에게는 가장 특별한 존재가 될 수 있다는 메시지를 전합니다."
    if "Every Breath You Take" in song_title:
        return "이 노래는 그리움과 관심이 지나칠 때 관계에서 어떤 부담이 될 수 있는지, 그리고 건강한 거리와 배려가 왜 중요한지 생각하게 합니다."
    return "이 노래는 단순히 듣고 끝나는 음악이 아니라, 내 경험과 감정을 연결해 볼 수 있는 계기가 됩니다."


def make_polished_feedback(song_title, question, student_answer):
    """한국어 생각 적기: 학생 원문을 반영해 내용이 매번 달라지도록 풍부하게 고쳐 줍니다."""
    answer = clean_student_korean_answer(student_answer)
    question = str(question).strip()
    topic, topic_en, feeling, feeling_en = detect_korean_reflection_focus(answer, question, song_title)
    bridge = song_reflection_bridge_ko(song_title)

    if len(answer.replace(" ", "")) < 5:
        core = (
            f"이 노래를 들으며 나는 {topic}에 대해 생각해 보게 되었습니다. "
            f"아직 긴 글로 정리하지는 못했지만, 마음속에는 {feeling}이 남았습니다."
        )
    else:
        core = (
            f"이 노래를 들으며 나는 {topic}에 대해 다시 생각하게 되었습니다. "
            f"처음 떠오른 생각은 ‘{answer}’였습니다. "
            f"이 짧은 생각 안에는 {feeling}이 담겨 있습니다."
        )

    polished_ko = (
        f"{core} "
        f"{bridge} "
        f"그래서 이 글은 단순히 노래가 좋았다는 감상에서 끝나지 않고, 내가 어떤 사람을 떠올렸는지, 왜 그런 감정을 느꼈는지, 그리고 지금의 나는 그 경험을 어떻게 바라보는지까지 생각해 보게 합니다. "
        f"앞으로 비슷한 순간을 다시 만난다면, 내 마음을 조금 더 솔직하게 표현하고 상대의 마음도 더 천천히 이해하려고 노력하고 싶습니다."
    )

    english_translation = try_translate_ko_to_en(polished_ko)
    if re.search(r"[가-힣]", english_translation) or len(english_translation.strip()) < 40:
        english_translation = (
            f"While listening to this song, I thought about {topic_en}. "
            f"My first thought was: {answer} "
            f"This short reflection shows that I felt {feeling_en}. "
            f"The song helped me connect the lyrics with my own life, not just enjoy the melody. "
            f"It made me think about who came to my mind, why I felt that way, and how I understand that experience now. "
            f"If I face a similar moment again, I want to express my feelings more honestly and try to understand the other person more carefully."
        )

    advice = (
        "쓰기 조언: 학생이 쓴 핵심 내용을 살려서 글을 더 풍부하게 만들었습니다. "
        "더 좋은 글이 되려면 ① 떠오른 사람이나 장면, ② 그때 느낀 감정, ③ 지금 다시 생각하며 깨달은 점을 한 문장씩 추가하면 됩니다."
    )
    return polished_ko, english_translation, advice

def sentence_case(s):
    """문장 첫 글자와 I를 정리합니다."""
    s = str(s).strip()
    if not s:
        return s
    s = re.sub(r"\bi\b", "I", s)
    return s[0].upper() + s[1:]


def split_student_sentences(text):
    """학생 입력을 문장 단위로 나눕니다."""
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+|[;\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def detect_keywords_for_revision(text):
    """학생 원문에서 의미를 잡아 수정문에 반영합니다."""
    low = str(text).lower()

    feelings = []
    for key, value in [
        ("sad", "sad"),
        ("happy", "happy"),
        ("lonely", "lonely"),
        ("miss", "sad"),
        ("cry", "sad"),
        ("comfort", "comforted"),
        ("touch", "touched"),
        ("move", "moved"),
        ("hope", "hopeful"),
        ("dream", "hopeful"),
        ("future", "hopeful"),
        ("worry", "worried"),
        ("nervous", "nervous"),
        ("stress", "stressed"),
    ]:
        if key in low and value not in feelings:
            feelings.append(value)

    topics = []
    for key, value in [
        ("friend", "my friend"),
        ("family", "my family"),
        ("mother", "my family"),
        ("father", "my family"),
        ("parent", "my family"),
        ("love", "love"),
        ("relationship", "a relationship"),
        ("memory", "an old memory"),
        ("past", "the past"),
        ("dream", "my dream"),
        ("future", "my future"),
        ("school", "my school life"),
        ("english", "learning English"),
        ("lyrics", "the lyrics"),
        ("melody", "the melody"),
        ("song", "this song"),
    ]:
        if key in low and value not in topics:
            topics.append(value)

    feeling = feelings[0] if feelings else "thoughtful"
    topic = topics[0] if topics else "my own feelings"
    return feeling, topic


def simple_fragment_revision(sentence):
    """문장이 아니라 단어 조각만 쓴 경우 의미 기반 문장으로 바꿉니다."""
    low = str(sentence).strip().lower()
    feeling, topic = detect_keywords_for_revision(low)

    if low in ["sad", "i sad", "i am sad", "i feel sad"]:
        return "I felt sad while listening to this song."
    if low in ["happy", "i happy", "i am happy", "i feel happy"]:
        return "I felt happy while listening to this song."
    if low in ["good", "very good", "good song"]:
        return "I thought this song was good."
    if low in ["my friend", "friend"]:
        return "This song reminded me of my friend."
    if low in ["my family", "family"]:
        return "This song reminded me of my family."
    if low in ["old memory", "memory", "my memory"]:
        return "This song reminded me of an old memory."
    if len(re.findall(r"[A-Za-z']+", low)) <= 3:
        return f"This song made me feel {feeling} and think about {topic}."
    return ""


def strong_correct_sentence(sentence):
    """
    학생 문장을 원문 의미를 유지하면서 강하게 문법 수정합니다.
    수업용 기초 오류가 결과에서 확실히 고쳐져 보이도록 설계했습니다.
    """
    original = str(sentence).strip()
    if not original:
        return ""

    frag = simple_fragment_revision(original)
    if frag:
        return frag

    s = original.strip()
    s = re.sub(r"[.!?]+$", "", s).strip()
    s = re.sub(r"\s+", " ", s)

    replacements = [
        (r"\bi\b", "I"),
        (r"\bim\b", "I'm"),
        (r"\bi'm\b", "I'm"),
        (r"\biam\b", "I am"),
        (r"\bdont\b", "don't"),
        (r"\bdidnt\b", "didn't"),
        (r"\bcant\b", "can't"),
        (r"\bwont\b", "won't"),
        (r"\benglish\b", "English"),
        (r"\bkorean\b", "Korean"),
        (r"\bkorea\b", "Korea"),
        (r"\byoutube\b", "YouTube"),
    ]
    for pat, repl in replacements:
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)

    low = s.lower()
    feeling, topic = detect_keywords_for_revision(s)

    # 의미 기반 강제 수정: make/remind 계열
    if re.search(r"\bthis song\b", low) and re.search(r"\b(make|makes|made)\b", low):
        if "felt" in low or "feel" in low:
            s = re.sub(r"\bthis song\s+(make|makes|made)\s+me\s+(felt|feel)\b", "This song made me feel", s, flags=re.IGNORECASE)
        elif any(w in low for w in ["sad", "happy", "lonely", "comfort", "touched", "moved", "hopeful", "worried", "angry"]):
            s = f"This song made me feel {feeling}"
            if topic != "this song":
                s += f" and think about {topic}"
        else:
            s = re.sub(r"\bthis song\s+make\s+me\b", "This song makes me", s, flags=re.IGNORECASE)

    if re.search(r"\bthis song\b", low) and re.search(r"\bremind\b", low):
        if re.search(r"\b(remind|reminds|reminded)\s+me\b", low):
            if "friend" in low:
                s = "This song reminded me of my friend"
            elif "family" in low:
                s = "This song reminded me of my family"
            elif "memory" in low or "past" in low or "old" in low:
                s = "This song reminded me of an old memory"
            elif "dream" in low or "future" in low:
                s = "This song reminded me of my dream and future"
            else:
                s = re.sub(r"\bthis song\s+remind\s+me\b", "This song reminded me of", s, flags=re.IGNORECASE)
                s = re.sub(r"\bthis song\s+reminds\s+me\s+about\b", "This song reminded me of", s, flags=re.IGNORECASE)
                s = re.sub(r"\bthis song\s+reminded\s+me\s+about\b", "This song reminded me of", s, flags=re.IGNORECASE)

    # listen 계열
    s = re.sub(r"\blisten this song\b", "listen to this song", s, flags=re.IGNORECASE)
    s = re.sub(r"\blistened this song\b", "listened to this song", s, flags=re.IGNORECASE)
    s = re.sub(r"\blistening this song\b", "listening to this song", s, flags=re.IGNORECASE)
    s = re.sub(r"\blisten the song\b", "listen to the song", s, flags=re.IGNORECASE)
    s = re.sub(r"\blistened the song\b", "listened to the song", s, flags=re.IGNORECASE)
    s = re.sub(r"\blistening the song\b", "listening to the song", s, flags=re.IGNORECASE)

    s = re.sub(r"^when listen to this song", "When I listen to this song", s, flags=re.IGNORECASE)
    s = re.sub(r"^listen to this song", "When I listen to this song", s, flags=re.IGNORECASE)

    # I + be/feel/think 오류
    s = re.sub(r"\bI am feel\b", "I feel", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI was feel\b", "I felt", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI feel like sad\b", "I feel sad", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI felt like sad\b", "I felt sad", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI feel touching\b", "I feel touched", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI felt touching\b", "I felt touched", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI feel boring\b", "I feel bored", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI felt boring\b", "I felt bored", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI thinks\b", "I think", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI feels\b", "I feel", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI likes\b", "I like", s, flags=re.IGNORECASE)

    # be 동사 빠짐
    s = re.sub(r"\bI think this song good\b", "I think this song is good", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI think this song sad\b", "I think this song is sad", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI think this song beautiful\b", "I think this song is beautiful", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI think this song meaningful\b", "I think this song is meaningful", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI think it good\b", "I think it is good", s, flags=re.IGNORECASE)
    s = re.sub(r"\bI think it sad\b", "I think it is sad", s, flags=re.IGNORECASE)

    s = re.sub(r"\bthis song very good\b", "this song is very good", s, flags=re.IGNORECASE)
    s = re.sub(r"\bthis song good\b", "this song is good", s, flags=re.IGNORECASE)
    s = re.sub(r"\bthis song sad\b", "this song is sad", s, flags=re.IGNORECASE)
    s = re.sub(r"\bthis song meaningful\b", "this song is meaningful", s, flags=re.IGNORECASE)
    s = re.sub(r"\bthis song beautiful\b", "this song is beautiful", s, flags=re.IGNORECASE)

    # because 뒤 조각 보정
    s = re.sub(r"\bbecause good\b", "because it is good", s, flags=re.IGNORECASE)
    s = re.sub(r"\bbecause sad\b", "because it is sad", s, flags=re.IGNORECASE)
    s = re.sub(r"\bbecause meaningful\b", "because it is meaningful", s, flags=re.IGNORECASE)
    s = re.sub(r"\bbecause beautiful\b", "because it is beautiful", s, flags=re.IGNORECASE)
    s = re.sub(r"\bbecause old memory\b", "because it reminded me of an old memory", s, flags=re.IGNORECASE)
    s = re.sub(r"\bbecause my friend\b", "because it reminded me of my friend", s, flags=re.IGNORECASE)
    s = re.sub(r"\bbecause lyrics good\b", "because the lyrics are good", s, flags=re.IGNORECASE)
    s = re.sub(r"\bbecause melody good\b", "because the melody is good", s, flags=re.IGNORECASE)

    # 관사와 표현
    s = re.sub(r"\bgood song\b", "a good song", s, flags=re.IGNORECASE)
    s = re.sub(r"\bsad song\b", "a sad song", s, flags=re.IGNORECASE)
    s = re.sub(r"\bold memory\b", "an old memory", s, flags=re.IGNORECASE)
    s = re.sub(r"\bmy old memory\b", "an old memory", s, flags=re.IGNORECASE)
    s = re.sub(r"\bremember my old memory\b", "remember an old memory", s, flags=re.IGNORECASE)
    s = re.sub(r"\blook back my memory\b", "look back on my memory", s, flags=re.IGNORECASE)

    # 구조가 너무 부족하면 의미 기반 재구성
    word_count = len(re.findall(r"[A-Za-z']+", s))
    has_subject = bool(re.search(r"\b(I|This song|It|The song|When I|My|We|You|He|She|They)\b", s))
    if word_count <= 8 and not has_subject:
        s = f"This song made me feel {feeling} and think about {topic}"

    s = sentence_case(s)
    s = re.sub(r"\s+([,.!?])", r"\1", s)
    return s.strip() + "."


def detect_english_reflection_focus(text, question="", song_title=""):
    """학생 영어 원문에서 소재와 감정을 잡아 풍부한 글에 반영합니다."""
    low = f"{text} {question} {song_title}".lower()

    if any(k in low for k in ["friend", "friendship", "classmate"]):
        topic = "my friendship"
        detail = "a person who stayed in my mind"
    elif any(k in low for k in ["family", "mother", "father", "parents", "brother", "sister"]):
        topic = "my family"
        detail = "the people who have supported me"
    elif any(k in low for k in ["dream", "future", "job", "career", "goal"]):
        topic = "my dreams and future"
        detail = "the kind of person I want to become"
    elif any(k in low for k in ["love", "relationship", "break", "miss", "boyfriend", "girlfriend"]):
        topic = "love and relationships"
        detail = "feelings that are not always easy to say"
    elif any(k in low for k in ["school", "study", "english", "class", "teacher"]):
        topic = "my school life and learning"
        detail = "my own effort and growth"
    elif any(k in low for k in ["memory", "past", "old", "child", "remember"]):
        topic = "an old memory"
        detail = "a moment from the past that still feels meaningful"
    else:
        topic = "my own feelings"
        detail = "what this song made me think about"

    if any(k in low for k in ["sad", "sorry", "regret", "miss", "cry", "lonely", "hard", "hurt"]):
        feeling = "sad and reflective"
        feeling_sentence = "It also made me think about feelings I could not express clearly before."
    elif any(k in low for k in ["happy", "good", "joy", "smile", "fun", "bright"]):
        feeling = "warm and happy"
        feeling_sentence = "It also reminded me that small memories can make me feel warm and thankful."
    elif any(k in low for k in ["comfort", "hope", "courage", "support", "strong"]):
        feeling = "comforted and encouraged"
        feeling_sentence = "It gave me comfort and made me want to keep going even when things are difficult."
    elif any(k in low for k in ["worry", "nervous", "afraid", "scared", "stress"]):
        feeling = "worried but thoughtful"
        feeling_sentence = "It helped me look at my worries more honestly instead of hiding them."
    else:
        feeling = "thoughtful"
        feeling_sentence = "It helped me look inside my mind more carefully."

    return topic, detail, feeling, feeling_sentence


def song_reflection_bridge_en(song_title):
    if "Let It Go" in song_title:
        return "The message of the song is connected to courage, freedom, and accepting myself."
    if "Hello" in song_title:
        return "The mood of the song is connected to regret and words that were not said at the right time."
    if "A Whole New World" in song_title:
        return "The song is connected to the excitement of seeing a new world and trying something unfamiliar."
    if "Stand By Me" in song_title:
        return "The song is connected to the importance of someone who stays beside me in difficult moments."
    if "Don't Know Why" in song_title:
        return "The quiet mood of the song is connected to choices and emotions that are hard to explain."
    if "Fix You" in song_title:
        return "The song sounds like comfort from someone who wants to help me when I am tired."
    if "Scientist" in song_title:
        return "The song is connected to the wish to go back and understand the past again."
    if "My Heart Will Go On" in song_title:
        return "The song is connected to memories and feelings that remain even after time passes."
    if "Counting Stars" in song_title:
        return "The song is connected to dreams, worries, and the future I want to choose for myself."
    if "My Universe" in song_title:
        return "The song is connected to the idea that one person can become a very special universe to someone else."
    return "The song helped me connect the lyrics with my own life."


def make_richer_expansion(corrected_text, original_text, song_title="", question=""):
    """학생 수정문을 바탕으로, 원문 핵심어가 반복문처럼 사라지지 않게 풍부한 영어 글을 만듭니다."""
    corrected_text = str(corrected_text).strip()
    original_text = str(original_text).strip()
    topic, detail, feeling, feeling_sentence = detect_english_reflection_focus(original_text + " " + corrected_text, question, song_title)
    bridge = song_reflection_bridge_en(song_title)

    if corrected_text:
        first_part = corrected_text
    else:
        first_part = f"While listening to this song, I thought about {topic}."

    richer = (
        f"{first_part} "
        f"This thought is connected to {topic}, especially {detail}. "
        f"At first, my idea was simple, but I can make it deeper by explaining why it stayed in my mind. "
        f"I felt {feeling} because the song made my own experience feel connected to the lyrics. "
        f"{feeling_sentence} "
        f"{bridge} "
        f"Because of this, my reflection is not only about the song. It is also about my memory, my emotions, and what I can learn from them now."
    )
    return re.sub(r"\s+", " ", richer).strip()

def polish_student_english_text(student_answer, song_title="", question=""):
    """학생 원문을 문장별로 강하게 문법 수정하고, 풍부한 영어 글도 함께 생성합니다."""
    original = str(student_answer).strip()
    if not original:
        return "", ""

    sentences = split_student_sentences(original)
    corrected_sentences = [strong_correct_sentence(s) for s in sentences]
    corrected = " ".join([s for s in corrected_sentences if s]).strip()

    corrected = re.sub(r"\.\s*\.", ".", corrected)
    corrected = re.sub(r"\s+", " ", corrected).strip()

    richer = make_richer_expansion(corrected, original, song_title, question)
    return corrected, richer


def make_english_only_feedback(song_title, question, student_answer):
    """영어 생각 적기 제출 시 문법 수정문과 풍부한 영어 버전만 제공합니다."""
    answer = str(student_answer).strip()

    if re.search(r"[가-힣]", answer):
        corrected_en = (
            "Please try to write your reflection in English. "
            "You can start with a simple sentence such as: While listening to this song, I thought about my memories."
        )
        richer_en = (
            "While listening to this song, I thought about my memories and feelings. "
            "The song helped me connect the lyrics with my own life. "
            "Next time, I want to express my ideas in English more clearly."
        )
        advice_en = (
            "Writing tip: Use easy English sentence patterns first. "
            "For example: I felt ~. / This song reminds me of ~. / I think ~ because ~."
        )
        return corrected_en, richer_en, advice_en

    corrected_en, richer_en = polish_student_english_text(answer, song_title, question)
    advice_en = (
        "Good effort. I corrected your grammar and expanded your ideas in English. "
        "Try to include three parts in your reflection: "
        "1) what the song reminded you of, 2) how you felt, and 3) what you learned or realized."
    )

    return corrected_en, richer_en, advice_en


# =========================================================
# 생각 적기 개인화 피드백 엔진 개선판
# - 학생 글의 핵심어를 먼저 추출한 뒤, 그 내용에 맞게 문장을 확장합니다.
# - 영어 입력: 문법 교정문 + 풍부한 영어 글 + 영어 쓰기 조언만 출력합니다.
# - 한국어 입력: 다듬은 한국어 글 + 영어 표현 + 한국어 쓰기 조언을 출력합니다.
# =========================================================


def _stable_pick(options, seed_text):
    if not options:
        return ""
    seed_text = str(seed_text)
    return options[sum(ord(ch) for ch in seed_text) % len(options)]


def _safe_original_quote(text, max_len=80):
    s = str(text).strip()
    s = re.sub(r"\s+", " ", s)
    if len(s) > max_len:
        s = s[:max_len].rstrip() + "..."
    return s


def _extract_ko_details(text, question="", song_title=""):
    raw = f"{text} {question} {song_title}"
    details = {
        "topic": "내 마음속 감정",
        "topic_en": "my own feelings",
        "person": "나 자신",
        "person_en": "myself",
        "scene": "노래를 듣는 순간",
        "scene_en": "the moment when I listened to the song",
        "feeling": "차분한 감정",
        "feeling_en": "thoughtful",
        "realization": "내 마음을 조금 더 솔직하게 바라볼 수 있다는 점",
        "realization_en": "I can look at my feelings more honestly",
    }

    topic_rules = [
        (("친구", "우정", "동료", "짝", "같이", "함께"), ("친구와의 관계", "my friendship", "친구", "my friend", "친구와 함께했던 장면", "a moment I shared with my friend")),
        (("가족", "엄마", "아빠", "부모", "동생", "형", "누나", "언니", "오빠"), ("가족과의 관계", "my family", "가족", "my family", "가족과 함께한 시간", "time with my family")),
        (("꿈", "미래", "진로", "목표", "직업", "성공", "취업"), ("나의 꿈과 미래", "my dreams and future", "미래의 나", "my future self", "앞으로의 삶을 상상하는 순간", "the moment when I imagined my future")),
        (("사랑", "좋아", "고백", "이별", "연애", "관계"), ("사랑과 관계", "love and relationships", "마음속에 있는 사람", "a person in my heart", "솔직하게 말하지 못했던 순간", "a moment when I could not express myself honestly")),
        (("학교", "공부", "영어", "수업", "학생", "선생"), ("학교생활과 배움", "my school life and learning", "학교에서의 나", "myself at school", "수업이나 학교생활 속 장면", "a moment from school life")),
        (("기억", "추억", "옛날", "과거", "예전", "그때"), ("과거의 기억", "an old memory", "예전의 나", "my past self", "아직 마음에 남아 있는 장면", "a memory that still stays in my mind")),
    ]
    for keys, vals in topic_rules:
        if any(k in raw for k in keys):
            details["topic"], details["topic_en"], details["person"], details["person_en"], details["scene"], details["scene_en"] = vals
            break

    feeling_rules = [
        (("슬프", "아쉽", "후회", "눈물", "그립", "외롭", "힘들", "미안", "보고 싶"), ("아쉬움과 그리움", "sad and reflective", "그 감정을 피하지 않고 천천히 바라보는 것이 중요하다는 점", "it is important to face those feelings slowly instead of avoiding them")),
        (("행복", "기쁘", "좋", "신나", "즐거", "밝", "웃"), ("따뜻하고 밝은 감정", "warm and happy", "작은 기억도 나에게 큰 힘이 될 수 있다는 점", "even a small memory can give me strength")),
        (("위로", "편안", "괜찮", "힘", "응원", "안정"), ("위로와 안정감", "comforted and encouraged", "누군가의 말이나 노래가 지친 마음을 다시 일으킬 수 있다는 점", "a song or someone's words can lift my tired heart")),
        (("희망", "용기", "도전", "할 수", "포기", "노력"), ("희망과 용기", "hopeful and encouraged", "쉽지 않아도 계속 앞으로 나아갈 수 있다는 점", "I can keep moving forward even when things are not easy")),
        (("걱정", "불안", "무섭", "긴장", "스트레스"), ("걱정과 불안", "worried but thoughtful", "불안한 마음도 글로 표현하면 조금 더 정리될 수 있다는 점", "writing about my worries can help me understand them better")),
    ]
    for keys, vals in feeling_rules:
        if any(k in raw for k in keys):
            details["feeling"], details["feeling_en"], details["realization"], details["realization_en"] = vals
            break

    return details


def _extract_en_details(text, question="", song_title=""):
    low = f"{text} {question} {song_title}".lower()
    details = {
        "topic": "my own feelings",
        "person": "myself",
        "scene": "the moment when I listened to the song",
        "feeling": "thoughtful",
        "realization": "I can understand my feelings more honestly",
        "because": "the song helped me connect the lyrics with my own life",
    }

    topic_rules = [
        (("friend", "friendship", "classmate", "together"), ("my friendship", "my friend", "a moment I shared with my friend", "that friendship is meaningful to me")),
        (("family", "mother", "mom", "father", "dad", "parent", "brother", "sister"), ("my family", "my family", "time with my family", "my family is important in my life")),
        (("dream", "future", "job", "career", "goal", "success"), ("my dreams and future", "my future self", "the moment when I imagined my future", "I should keep trying for my dream")),
        (("love", "relationship", "miss", "break", "boyfriend", "girlfriend"), ("love and relationships", "a person in my heart", "a moment when I could not express my feelings clearly", "honest feelings are not always easy to say")),
        (("school", "study", "english", "class", "teacher"), ("my school life and learning", "myself at school", "a moment from school life", "learning can become meaningful when it connects to my life")),
        (("memory", "past", "old", "child", "remember"), ("an old memory", "my past self", "a memory that still stays in my mind", "old memories can still teach me something")),
        (("lyrics", "melody", "voice", "song"), ("this song", "myself as a listener", "the moment when the lyrics and melody touched me", "music can express feelings that are hard to say")),
    ]
    for keys, vals in topic_rules:
        if any(k in low for k in keys):
            details["topic"], details["person"], details["scene"], details["realization"] = vals
            break

    feeling_rules = [
        (("sad", "sorry", "regret", "miss", "cry", "lonely", "hard", "hurt"), ("sad and reflective", "it reminded me of feelings I could not express clearly before")),
        (("happy", "good", "joy", "smile", "fun", "bright", "excited"), ("warm and happy", "it reminded me that small moments can make me feel thankful")),
        (("comfort", "hope", "courage", "support", "strong", "brave"), ("comforted and encouraged", "it gave me comfort and made me want to keep going")),
        (("worry", "nervous", "afraid", "scared", "stress", "anxious"), ("worried but thoughtful", "it helped me look at my worries instead of hiding them")),
        (("special", "universe", "star", "light"), ("special and warm", "it made me think that one person can be very important to someone else")),
    ]
    for keys, vals in feeling_rules:
        if any(k in low for k in keys):
            details["feeling"], details["because"] = vals
            break
    return details


def _fix_common_english_errors(sentence):
    s = str(sentence).strip()
    s = re.sub(r"\s+", " ", s)
    if not s:
        return ""

    replacements = [
        (r"\bthis song make me\b", "This song makes me"),
        (r"\bthis song makes me to\b", "This song makes me"),
        (r"\bit make me\b", "It makes me"),
        (r"\bit makes me to\b", "It makes me"),
        (r"\bi think my friend\b", "I think of my friend"),
        (r"\bi remember my friend\b", "I remember my friend"),
        (r"\bi am think\b", "I think"),
        (r"\bi think about my future\b", "I think about my future"),
        (r"\bi feel sad because my friend\b", "I feel sad because it reminds me of my friend"),
        (r"\bi feel happy because my friend\b", "I feel happy because it reminds me of my friend"),
        (r"\bthis song is make me\b", "This song makes me"),
        (r"\bthis song very good\b", "This song is very good"),
        (r"\bthis song good\b", "This song is good"),
        (r"\bthis song sad\b", "This song is sad"),
        (r"\bi like this song because good\b", "I like this song because it is good"),
        (r"\bi like this song because sad\b", "I like this song because it feels sad"),
        (r"\bbecause good\b", "because it is good"),
        (r"\bbecause sad\b", "because it feels sad"),
        (r"\bbecause my friend\b", "because it reminds me of my friend"),
        (r"\bremind me my friend\b", "reminds me of my friend"),
        (r"\breminds me my friend\b", "reminds me of my friend"),
        (r"\bremember old memory\b", "remember an old memory"),
        (r"\blook back my memory\b", "look back on my memory"),
    ]
    for pattern, repl in replacements:
        s = re.sub(pattern, repl, s, flags=re.IGNORECASE)

    # very short fragments become complete sentences
    low = s.lower().strip(" .!?')(")
    fragment_map = {
        "sad": "I felt sad while listening to this song",
        "happy": "I felt happy while listening to this song",
        "good": "I thought this song was good",
        "good song": "I thought this was a good song",
        "my friend": "This song reminded me of my friend",
        "friend": "This song reminded me of my friend",
        "family": "This song made me think of my family",
        "future": "This song made me think about my future",
        "dream": "This song made me think about my dream",
    }
    if low in fragment_map:
        s = fragment_map[low]

    # If the student wrote a noun-like fragment, build a sentence from detected meaning.
    words = re.findall(r"[A-Za-z']+", s)
    has_verbish = bool(re.search(r"\b(am|is|are|was|were|feel|felt|think|thought|like|liked|make|makes|made|remind|reminds|remember|miss|want|hope|need|love|listen|heard)\b", s, flags=re.IGNORECASE))
    if len(words) <= 5 and not has_verbish:
        d = _extract_en_details(s)
        s = f"This song made me feel {d['feeling']} and think about {d['topic']}"

    # Capitalization and punctuation
    s = re.sub(r"\bi\b", "I", s)
    s = s.strip()
    if s:
        s = s[0].upper() + s[1:]
    if s and s[-1] not in ".!?":
        s += "."
    return s


def polish_student_english_text(student_answer, song_title="", question=""):
    original = str(student_answer).strip()
    if not original:
        return "", ""
    parts = split_student_sentences(original)
    if not parts:
        parts = [original]
    corrected_parts = [_fix_common_english_errors(p) for p in parts if str(p).strip()]
    corrected = " ".join(p for p in corrected_parts if p).strip()
    corrected = re.sub(r"\s+", " ", corrected)
    richer = make_richer_expansion(corrected, original, song_title, question)
    return corrected, richer


def make_richer_expansion(corrected_text, original_text, song_title="", question=""):
    original = str(original_text).strip()
    corrected = str(corrected_text).strip()
    d = _extract_en_details(original + " " + corrected, question, song_title)
    bridge = song_reflection_bridge_en(song_title)
    quote = _safe_original_quote(original, 70)

    sentence_bank = {
        "my friendship": [
            "When I listened to the song, I thought about my friend and the time we shared.",
            "The song made me remember a friend who is still meaningful to me.",
        ],
        "my family": [
            "When I listened to the song, I thought about my family and the support they have given me.",
            "The song reminded me of my family and made me feel thankful.",
        ],
        "my dreams and future": [
            "When I listened to the song, I thought about my future and the kind of person I want to become.",
            "The song made me think about my dream, even though the future is not always clear.",
        ],
        "love and relationships": [
            "When I listened to the song, I thought about feelings that are not easy to say directly.",
            "The song made me think about how complicated but meaningful relationships can be.",
        ],
        "my school life and learning": [
            "When I listened to the song, I connected it with my school life and my own effort.",
            "The song made me think that learning can become more meaningful when it connects to my feelings.",
        ],
        "an old memory": [
            "When I listened to the song, an old memory came back to my mind.",
            "The song made me remember a moment from the past that still feels important.",
        ],
        "this song": [
            "When I listened to the song, the lyrics and melody stayed in my mind.",
            "The song made me feel something before I could explain it clearly.",
        ],
    }
    first = corrected if corrected else _stable_pick(sentence_bank.get(d["topic"], sentence_bank["this song"]), original)
    personalized = _stable_pick(sentence_bank.get(d["topic"], sentence_bank["this song"]), original + song_title)

    richer = (
        f"{first} "
        f"In my first writing, I wrote, '{quote}' This idea can become richer because it shows a real feeling, not just a simple answer. "
        f"{personalized} "
        f"I felt {d['feeling']} because {d['because']}. "
        f"This reflection is connected to {d['scene']}, and it helped me realize that {d['realization']}. "
        f"{bridge} "
        f"Because of this, my writing is not only about the song. It is also about my own experience, memory, and feelings."
    )
    return re.sub(r"\s+", " ", richer).strip()


def make_english_only_feedback(song_title, question, student_answer):
    answer = str(student_answer).strip()
    if re.search(r"[가-힣]", answer):
        corrected_en = "Please write this part in English. For example: This song makes me think of my friend."
        richer_en = (
            "This song makes me think of my own feelings. "
            "When I listen to it, I can connect the lyrics with my life. "
            "Next time, I want to express my idea in English with more details."
        )
        advice_en = "Writing tip: Start with easy patterns: This song makes me feel ~. / It reminds me of ~. / I think ~ because ~."
        return corrected_en, richer_en, advice_en

    corrected_en, richer_en = polish_student_english_text(answer, song_title, question)
    d = _extract_en_details(answer + " " + corrected_en, question, song_title)
    advice_options = [
        f"Writing tip: Your idea is about {d['topic']}. Add one sentence about a specific person, memory, or moment to make it clearer.",
        f"Writing tip: You expressed a {d['feeling']} feeling. Add because + reason to make your writing stronger.",
        "Writing tip: A good reflection has three parts: what I remembered, how I felt, and what I realized.",
        "Writing tip: Try to use simple but complete sentences. For example: This song made me feel ~ because ~.",
    ]
    advice_en = _stable_pick(advice_options, answer + song_title + question)
    return corrected_en, richer_en, advice_en


def make_polished_feedback(song_title, question, student_answer):
    answer = clean_student_korean_answer(student_answer)
    d = _extract_ko_details(answer, question, song_title)
    bridge = song_reflection_bridge_ko(song_title)
    quote = _safe_original_quote(answer, 70)

    opener_bank = {
        "친구와의 관계": [
            "이 노래를 들으며 나는 친구와 함께했던 장면을 떠올렸습니다.",
            "이 노래는 나에게 친구와의 관계가 얼마나 소중한지 다시 생각하게 했습니다.",
        ],
        "가족과의 관계": [
            "이 노래를 들으며 나는 가족과 함께한 시간과 고마움을 떠올렸습니다.",
            "이 노래는 가족이 내 삶에서 어떤 의미인지 다시 생각하게 했습니다.",
        ],
        "나의 꿈과 미래": [
            "이 노래를 들으며 나는 나의 꿈과 미래를 다시 생각해 보았습니다.",
            "이 노래는 아직 분명하지 않은 미래라도 계속 노력해야겠다는 마음을 떠올리게 했습니다.",
        ],
        "사랑과 관계": [
            "이 노래를 들으며 나는 쉽게 말하지 못했던 마음과 관계를 떠올렸습니다.",
            "이 노래는 누군가를 좋아하거나 그리워하는 마음이 얼마나 복잡한지 생각하게 했습니다.",
        ],
        "학교생활과 배움": [
            "이 노래를 들으며 나는 학교생활과 내가 조금씩 성장하는 과정을 떠올렸습니다.",
            "이 노래는 공부와 배움도 내 감정과 연결될 때 더 의미 있어질 수 있다는 생각을 하게 했습니다.",
        ],
        "과거의 기억": [
            "이 노래를 들으며 나는 아직 마음에 남아 있는 과거의 한 장면을 떠올렸습니다.",
            "이 노래는 시간이 지나도 사라지지 않는 기억의 의미를 다시 생각하게 했습니다.",
        ],
        "내 마음속 감정": [
            "이 노래를 들으며 나는 내 마음속에 남아 있던 감정을 바라보게 되었습니다.",
            "이 노래는 말로 다 정리하지 못했던 내 감정을 천천히 생각하게 했습니다.",
        ],
    }
    opener = _stable_pick(opener_bank.get(d["topic"], opener_bank["내 마음속 감정"]), answer + song_title)

    if len(answer.replace(" ", "")) < 5:
        source_sentence = f"처음에는 생각을 길게 쓰지 못했지만, 그 짧은 표현 안에도 {d['feeling']}이 담겨 있었습니다."
    else:
        source_sentence = f"처음 쓴 생각은 ‘{quote}’였습니다. 이 말 안에는 {d['person']}에 대한 생각과 {d['feeling']}이 함께 담겨 있었습니다."

    polished_ko = (
        f"{opener} "
        f"{source_sentence} "
        f"특히 {d['scene']}이 떠오르면서, 이 노래가 단순히 듣기 좋은 음악이 아니라 내 경험과 연결될 수 있다는 것을 느꼈습니다. "
        f"{bridge} "
        f"그래서 이 글은 노래에 대한 감상에서 끝나지 않고, 내가 왜 그런 감정을 느꼈는지, 그 감정이 지금의 나에게 어떤 의미가 있는지 생각해 보는 글이 되었습니다. "
        f"이 경험을 통해 나는 {d['realization']}을 알게 되었습니다."
    )

    english_translation = (
        f"While listening to this song, I thought about {d['topic_en']}. "
        f"My first idea was: '{quote}' This idea shows that I felt {d['feeling_en']} and thought about {d['person_en']}. "
        f"The song reminded me of {d['scene_en']}. It was not just a song to enjoy; it became connected to my own experience. "
        f"It helped me think about why I felt that way and what that feeling means to me now. "
        f"Through this reflection, I realized that {d['realization_en']}."
    )

    advice = (
        f"쓰기 조언: 학생이 쓴 핵심 내용인 '{quote}'를 바탕으로 글을 확장했습니다. "
        f"다음에는 ① 떠오른 사람이나 장면, ② 느낀 감정, ③ 지금 깨달은 점을 한 문장씩 더 쓰면 훨씬 자연스러운 글이 됩니다."
    )
    return polished_ko, english_translation, advice


SONGS = {'22. Die for You - The Weeknd': {'video_url': 'https://www.youtube.com/results?search_query=The+Weeknd+Die+For+You',
                                  'lyrics': [("I'm findin' ways to articulate the feelin' I'm goin' through",
                                              '내가 겪고 있는 감정을 표현할 방법을 찾고 있어'),
                                             ("I just can't say I don't love you (Yeah)", '나는 너를 사랑하지 않는다고는 도저히 말할 수 없어 (Yeah)'),
                                             ("'Cause I love you, yeah", '왜냐하면 나는 너를 사랑하니까, yeah'),
                                             ("It's hard for me to communicate the thoughts that I hold",
                                              '내가 품고 있는 생각을 말로 전하는 건 어려워'),
                                             ("But tonight, I'm gon' let you know", '하지만 오늘 밤에는 네게 알려 줄게'),
                                             ('Let me tell the truth', '내가 진실을 말하게 해 줘'),
                                             ('Baby, let me tell the truth, yeah', 'Baby, 내가 진실을 말하게 해 줘, yeah'),
                                             ("You know what I'm thinkin', see it in your eyes",
                                              '내가 무슨 생각을 하는지 너는 알고 있어, 네 눈을 보면 알 수 있어'),
                                             ('You hate that you want me, hate it when you cry',
                                              '너는 나를 원한다는 사실을 싫어하고, 네가 울 때도 싫어해'),
                                             ("You're scared to be lonely, 'specially in the night", '너는 혼자가 되는 게 두려워, 특히 밤에는'),
                                             ("I'm scared that I'll miss you, happens every time", '나는 네가 그리워질까 봐 두려워, 매번 그렇게 돼'),
                                             ("I don't want this feelin', I can't afford love", '나는 이런 감정을 원하지 않아, 사랑을 감당할 수 없어'),
                                             ('I try to find a reason to pull us apart', '나는 우리를 떼어 놓을 이유를 찾으려고 해'),
                                             ("It ain't workin' 'cause you're perfect", '그건 통하지 않아, 네가 완벽하니까'),
                                             ("And I know that you're worth it", '그리고 나는 네가 그럴 가치가 있다는 걸 알아'),
                                             ("I can't walk away, oh", '나는 떠날 수 없어, oh'),
                                             ("Even though we're goin' through it", '비록 우리가 힘든 시간을 겪고 있어도'),
                                             ('And it makes you feel alone', '그리고 그것 때문에 네가 외롭다고 느껴도'),
                                             ('Just know that I would die for you', '내가 너를 위해서라면 죽을 수도 있다는 것만 알아 줘'),
                                             ('Baby, I would die for you, yeah', 'Baby, 나는 너를 위해서라면 죽을 수도 있어, yeah'),
                                             ('The distance and the time between us', '우리 사이의 거리와 시간도'),
                                             ("It'll never change my mind 'cause", '내 마음을 절대 바꾸지 못할 거야, 왜냐하면'),
                                             ('Baby, I would die for you', 'Baby, 나는 너를 위해서라면 죽을 수도 있어'),
                                             ('Baby, I would die for you, yeah (Say)', 'Baby, 나는 너를 위해서라면 죽을 수도 있어, yeah (Say)')],
                                  'quiz': [{'q': '1. 화자는 자신의 감정을 어떻게 표현하려고 하나요?',
                                            'options': ['감정을 말로 표현할 방법을 찾고 있다',
                                                        '모든 감정을 숨기려고 한다',
                                                        '상대를 완전히 잊으려고 한다',
                                                        '새로운 도시로 떠나려고 한다'],
                                            'answer': '감정을 말로 표현할 방법을 찾고 있다'},
                                           {'q': '2. 화자가 말하기 어렵다고 하는 것은 무엇인가요?',
                                            'options': ['자신이 품고 있는 생각', '학교 숙제', '여행 계획', '친구의 이름'],
                                            'answer': '자신이 품고 있는 생각'},
                                           {'q': '3. 화자는 언제 진실을 말하겠다고 하나요?',
                                            'options': ['오늘 밤', '내일 아침', '다음 주', '몇 년 뒤'],
                                            'answer': '오늘 밤'},
                                           {'q': '4. 상대는 특히 언제 혼자가 되는 것을 두려워하나요?',
                                            'options': ['밤에', '아침에', '학교에서', '여행할 때'],
                                            'answer': '밤에'},
                                           {'q': "5. 'pull us apart'의 뜻은?",
                                            'options': ['우리를 갈라놓다', '우리를 만나게 하다', '우리를 웃게 하다', '우리를 도와주다'],
                                            'answer': '우리를 갈라놓다'},
                                           {'q': '6. 화자는 상대를 어떻게 평가하나요?',
                                            'options': ['perfect하고 worth it하다고 생각한다', '무섭다고 생각한다', '재미없다고 생각한다', '낯설다고 생각한다'],
                                            'answer': 'perfect하고 worth it하다고 생각한다'},
                                           {'q': "7. 'I can't walk away'의 의미는?",
                                            'options': ['나는 떠날 수 없어', '나는 걸을 수 없어', '나는 집에 갈 수 없어', '나는 말을 할 수 없어'],
                                            'answer': '나는 떠날 수 없어'},
                                           {'q': '8. 후렴에서 가장 강하게 드러나는 마음은?',
                                            'options': ['상대를 위해 큰 희생도 할 만큼 사랑한다', '상대를 잊고 싶다', '혼자 있고 싶다', '여행을 떠나고 싶다'],
                                            'answer': '상대를 위해 큰 희생도 할 만큼 사랑한다'}],
                                  'key_expressions': [('articulate the feeling', '감정을 분명하게 표현하다'),
                                                      ('go through', '겪다'),
                                                      ('communicate', '의사소통하다'),
                                                      ('let you know', '네게 알려 주다'),
                                                      ('tell the truth', '진실을 말하다'),
                                                      ('scared to be lonely', '혼자가 되는 것이 두렵다'),
                                                      ("can't afford love", '사랑을 감당할 수 없다'),
                                                      ('pull us apart', '우리를 갈라놓다'),
                                                      ('worth it', '그럴 가치가 있다'),
                                                      ('die for you', '너를 위해서라면 죽을 수도 있다')],
                                  'matching': [('articulate the feeling', '감정을 분명하게 표현하다'),
                                               ('go through', '겪다'),
                                               ('let you know', '네게 알려 주다'),
                                               ('tell the truth', '진실을 말하다'),
                                               ('pull us apart', '우리를 갈라놓다'),
                                               ('I would die for you', '나는 너를 위해서라면 죽을 수도 있다')],
                                  'reflect_questions': ['내 감정을 말로 표현하기 어려웠던 경험이 있나요?',
                                                        '거리나 시간이 관계에 영향을 준다고 생각하나요?',
                                                        '사랑하는 사람에게 진심을 전할 때 가장 중요한 것은 무엇이라고 생각하나요?']}}

BACKGROUND_CONTENT = {'22. Die for You - The Weeknd': {'title': '❤️ Die for You: 멀어져도 변하지 않는 마음',
                                  'paragraphs': ['Die for You는 자신의 감정을 말로 표현하기 어려워하면서도 상대를 여전히 사랑하고 있다는 마음을 솔직하게 드러내는 노래입니다.',
                                                 '노래 속 화자는 서로가 외로움과 이별을 두려워하고 있다는 것을 알고 있습니다. 관계가 힘든 상황에서도 상대를 쉽게 떠나지 못하는 복잡한 '
                                                 '감정이 나타납니다.',
                                                 '후렴의 핵심 표현은 I would die for you입니다. would + 동사 구조를 통해 상대를 위해 큰 희생도 할 수 있을 만큼 강한 '
                                                 '마음을 강조합니다.',
                                                 '수업에서는 articulate the feeling, go through, communicate, let you know, tell the '
                                                 'truth, scared to be lonely, pull us apart, worth it, die for you 같은 표현을 중심으로 '
                                                 '배울 수 있습니다.']}}


def show_background(song_choice, data):
    """배경 학습 탭만 HTML/컴포넌트 없이 안정적으로 크게 출력합니다."""
    bg = BACKGROUND_CONTENT.get(song_choice)
    if bg is None:
        bg = {
            "title": "🎵 배경 학습",
            "paragraphs": [str(data.get("bg", "")).replace("<br>", " ").replace("<p>", "").replace("</p>", "")]
        }

    st.markdown('<div class="bg-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="bg-title">{bg["title"]}</div>', unsafe_allow_html=True)
    for p in bg["paragraphs"]:
        st.markdown(f'<div class="bg-p">{p}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


if "selected_song" not in st.session_state:
    st.session_state.selected_song = list(SONGS.keys())[0]
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "🎬 배경 학습"

def sync_song():
    for k in list(st.session_state.keys()):
        if k.startswith(("quiz_", "keygame_", "match_", "reflect_", "integrated_quiz_", "song_grammar_", "mission_")):
            del st.session_state[k]

st.markdown('<div class="main-title"><h1>🎵 Pop Song English Learning</h1></div>', unsafe_allow_html=True)
song_options = list(SONGS.keys())
song_choice = st.selectbox("👉 학습할 노래를 선택하세요", song_options, index=song_options.index(st.session_state.selected_song) if st.session_state.selected_song in song_options else 0, on_change=sync_song, key="song_selector")
st.session_state.selected_song = song_choice
data = SONGS[song_choice]

tabs_list = ["🎬 배경 학습", "📖 가사 퀴즈", "🎯 문법", "🧩 문장 매칭 게임", "✍️ 생각 적기", "⭐ 핵심 표현 듣기"]
selected_tab = st.radio("학습 단계", tabs_list, horizontal=True, key="current_tab")

if selected_tab == "🎬 배경 학습":
    show_background(song_choice, data)
    video_url = str(data.get("video_url", "")).strip()
    if video_url:
        st.video(video_url)
    else:
        st.info("이 노래의 영상 주소가 아직 입력되지 않았습니다. video_url에 YouTube 주소를 넣으면 영상이 표시됩니다.")
    st.markdown(
        """
        <div class="game-card">
            <div class="big-guide">
            노래를 듣기 전에 배경을 먼저 읽고, 화자의 감정과 상황을 생각해 보세요.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


elif selected_tab == "📖 가사 퀴즈":
    st.subheader("🎬 노래 영상")
    video_url = str(data.get("video_url", "")).strip()
    if video_url:
        st.video(video_url)
    else:
        st.info("이 노래의 영상 주소가 아직 입력되지 않았습니다. video_url에 YouTube 주소를 넣으면 영상이 표시됩니다.")
    st.markdown("---")
    st.subheader("📖 전체 가사와 한국어 해석")
    for en, ko in data["lyrics"]:
        st.markdown(f"""
        <div class="lyrics-container">
            <div class="eng-line">{clean_text_for_display(en)}</div>
            <div class="kor-sub">{clean_text_for_display(ko)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    show_integrated_quiz_tab(song_choice, data)


elif selected_tab == "🎯 문법":
    show_song_grammar_tab(song_choice, data)


elif selected_tab == "🧩 문장 매칭 게임":
    match_key = safe_key(song_choice)

    pairs = [
        {
            "id": f"pair_{i}",
            "en": en,
            "ko": ko
        }
        for i, (en, ko) in enumerate(data["matching"], start=1)
    ]

    en_cards = [{"id": p["id"], "text": p["en"]} for p in pairs]
    ko_cards = [{"id": p["id"], "text": p["ko"]} for p in pairs]

    en_cards = shuffle_options(en_cards, seed=f"{match_key}_en")
    ko_cards = shuffle_options(ko_cards, seed=f"{match_key}_ko")

    payload = {
        "en": en_cards,
        "ko": ko_cards,
        "total": len(pairs),
    }

    data_json = json.dumps(payload, ensure_ascii=False)
    component_id = "match_" + uuid.uuid4().hex

    matching_pdf_bytes = make_mission_pdf(song_choice, "문장 매칭 게임", "문장 매칭 게임 활동 완료")
    matching_pdf_filename = f"mission_complete_{safe_key(song_choice)}_{safe_key('문장 매칭 게임')}.pdf"
    if matching_pdf_bytes:
        matching_pdf_b64 = base64.b64encode(matching_pdf_bytes).decode("utf-8")
        certificate_html = f'''
            <div id="cert_{component_id}" class="certificate-box" style="display:none;">
                <div class="certificate-title">📄 문장 매칭 게임 PDF 인증서</div>
                <div class="certificate-guide">
                    모든 문장을 성공적으로 맞췄습니다. 아래 버튼을 눌러 완료 인증서를 저장하세요.
                </div>
                <a class="cert-download" href="data:application/pdf;base64,{matching_pdf_b64}" download="{matching_pdf_filename}">
                    📄 PDF 인증서 다운받기
                </a>
            </div>
        '''
    else:
        certificate_html = f'''
            <div id="cert_{component_id}" class="certificate-box" style="display:none;">
                <div class="certificate-title">📄 문장 매칭 게임 PDF 인증서</div>
                <div class="certificate-guide">
                    PDF 저장 기능을 사용하려면 requirements.txt에 reportlab을 추가해 주세요. 예: reportlab>=4.0.0
                </div>
            </div>
        '''

    components.html(
        f"""
        <div id="{component_id}" class="match-app">
            <div class="match-head">
                <div class="match-title">🧩 문장 매칭 게임</div>
                <div class="match-guide">
                    왼쪽 영어 표현과 오른쪽 한국어 뜻을 차례로 눌러 짝을 맞추세요.<br>
                    선택한 박스는 색칠되고, 정답이면 두 박스가 반짝이며 함께 사라집니다.
                </div>
            </div>

            <div class="match-status">
                <div id="status_{component_id}">먼저 영어 또는 한국어 박스를 하나 선택하세요.</div>
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

            {certificate_html}
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
                0% {{ opacity: 1; transform: scale(1); max-height: 220px; margin-bottom: 0; }}
                35% {{ opacity: 1; transform: scale(1.04); }}
                70% {{ opacity: .55; transform: scale(.96); max-height: 220px; }}
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

            #{component_id} .certificate-box {{
                background: linear-gradient(135deg,#eef2ff,#f0f9ff,#fdf2f8);
                border: 2px solid #6366f1;
                border-radius: 22px;
                padding: 24px;
                margin-top: 18px;
                text-align: center;
                animation: pop_{component_id} .45s ease;
            }}

            #{component_id} .certificate-title {{
                font-size: 25px;
                font-weight: 1000;
                color: #3730a3;
                margin-bottom: 8px;
            }}

            #{component_id} .certificate-guide {{
                font-size: 16px;
                font-weight: 850;
                color: #475569;
                line-height: 1.7;
                margin-bottom: 14px;
            }}

            #{component_id} .cert-download {{
                display: block;
                width: 100%;
                box-sizing: border-box;
                min-height: 68px;
                line-height: 68px;
                background: #ffffff;
                color: #3730a3;
                border: 2px solid #4f46e5;
                border-radius: 18px;
                text-decoration: none;
                font-size: 20px;
                font-weight: 1000;
            }}

            #{component_id} .cert-download:hover {{
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
            const certBox_{component_id} = document.getElementById("cert_{component_id}");

            let selected_{component_id} = null;
            let done_{component_id} = new Set();
            let locked_{component_id} = false;

            function escapeHtml_{component_id}(str) {{
                return String(str)
                    .replaceAll("&", "&amp;")
                    .replaceAll("<", "&lt;")
                    .replaceAll(">", "&gt;")
                    .replaceAll('"', "&quot;")
                    .replaceAll("'", "&#039;");
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
                        msg.textContent = "🎉 모든 문장을 맞췄습니다! 이제 PDF 인증서를 저장하세요.";
                        root_{component_id}.appendChild(msg);
                    }}
                    if (certBox_{component_id}) {{
                        certBox_{component_id}.style.display = "block";
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
                        : "왼쪽에서 알맞은 영어 표현을 고르세요.";
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
                    status_{component_id}.textContent = "정답입니다! 두 박스가 함께 사라집니다. ✅";

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

                if (certBox_{component_id}) {{
                    certBox_{component_id}.style.display = "none";
                }}

                status_{component_id}.textContent = "먼저 영어 또는 한국어 박스를 하나 선택하세요.";
                render_{component_id}();
            }});

            render_{component_id}();
        </script>
        """,
        height=760,
        scrolling=True
    )

elif selected_tab == "✍️ 생각 적기":
    st.subheader("✍️ 생각 적기: Reflective Writing")
    st.markdown(
        '<div class="game-card"><div class="big-guide">'
        '질문을 하나 고르고, 노래를 들으며 떠오른 생각을 자유롭게 적어 보세요.<br>'
        '학생이 짧게 쓰더라도 내용을 조금 더 풍부하게 다듬어 줍니다.<br>'
        '한국어로 쓰면 <b>다듬은 한국어 글</b>과 <b>영어 표현</b>을 함께 보여 주고, 영어로 쓰면 <b>문법을 고친 영어 문장</b>과 <b>풍부한 영어 글</b>만 보여 줍니다.'
        '</div></div>',
        unsafe_allow_html=True
    )

    reflect_key = safe_key(song_choice)
    questions = data["reflect_questions"][:3]
    selected_question = st.radio("질문을 선택하세요.", questions, key=f"reflect_question_{reflect_key}", index=0)

    write_ko_tab, write_en_tab = st.tabs(["🇰🇷 한국어로 적고 싶은 사람", "🇺🇸 영어로 적고 싶은 사람"])

    with write_ko_tab:
        answer_ko = st.text_area(
            "내 생각을 한국어로 적어 보세요.",
            placeholder="예: 이 노래를 들으며 예전에 좋아했던 사람이 떠올랐다. 그때는 내 마음을 잘 표현하지 못했고, 지금 생각하면 조금 아쉽다...",
            height=180,
            key=f"reflect_answer_ko_{reflect_key}"
        )

        if st.button("쓰기 결과 제출", key=f"reflect_submit_ko_{reflect_key}", use_container_width=True):
            if not answer_ko.strip():
                st.warning("먼저 자신의 생각을 한두 문장이라도 적어 보세요.")
            else:
                ko_feedback, en_feedback, advice = make_polished_feedback(song_choice, selected_question, answer_ko)
                st.session_state[f"mission_{reflect_key}_reflection"] = True
                st.session_state[f"mission_{reflect_key}_reflection_detail"] = "생각 적기 활동 완료 / 한국어 생각 적기 제출 완료"
                st.markdown("### 🇰🇷 다듬고 풍부하게 만든 한국어 글")
                st.markdown(f'<div class="feedback-ko">{clean_text_for_display(ko_feedback)}</div>', unsafe_allow_html=True)
                st.markdown("### 🇺🇸 풍부하게 만든 영어 글")
                st.markdown(f'<div class="feedback-en">{clean_text_for_display(en_feedback)}</div>', unsafe_allow_html=True)
                st.markdown("### ✨ 쓰기 조언")
                st.markdown(f'<div class="advice-box">{clean_text_for_display(advice)}</div>', unsafe_allow_html=True)
                show_mission_pdf_download(
                    song_choice,
                    "생각 적기",
                    f"{reflect_key}_reflection_ko_now",
                    st.session_state.get(f"mission_{reflect_key}_reflection_detail", "")
                )

    with write_en_tab:
        answer_en = st.text_area(
            "Write your reflection in English.",
            placeholder="Example: This song make me sad. I think my friend. → 문법이 틀려도 괜찮습니다. 앱이 고쳐 줍니다.",
            height=180,
            key=f"reflect_answer_en_{reflect_key}"
        )

        if st.button("쓰기 결과 제출", key=f"reflect_submit_en_{reflect_key}", use_container_width=True):
            if not answer_en.strip():
                st.warning("Please write at least one or two sentences first.")
            else:
                corrected_en, richer_en, advice_en = make_english_only_feedback(song_choice, selected_question, answer_en)
                st.session_state[f"mission_{reflect_key}_reflection"] = True
                st.session_state[f"mission_{reflect_key}_reflection_detail"] = "생각 적기 활동 완료 / 영어 생각 적기 제출 완료"
                st.markdown("### ✅ 문법을 고친 영어 문장")
                st.markdown(f'<div class="feedback-en">{clean_text_for_display(corrected_en)}</div>', unsafe_allow_html=True)
                st.markdown("### 🌱 내용을 풍부하게 만든 영어 글")
                st.markdown(f'<div class="feedback-en">{clean_text_for_display(richer_en)}</div>', unsafe_allow_html=True)
                st.markdown("### ✨ English Feedback")
                st.markdown(f'<div class="advice-box">{clean_text_for_display(advice_en)}</div>', unsafe_allow_html=True)
                show_mission_pdf_download(
                    song_choice,
                    "생각 적기",
                    f"{reflect_key}_reflection_en_now",
                    st.session_state.get(f"mission_{reflect_key}_reflection_detail", "")
                )



elif selected_tab == "⭐ 핵심 표현 듣기":
    show_key_expression_learning_in_lyrics(song_choice, data, max_words=10)
