import streamlit as st
import streamlit.components.v1 as components
import random
import html
import re
import json
import uuid
import io
import os
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


def show_mission_pdf_download(song_choice, activity_name, mission_key, detail_text=""):
    """완료 메시지와 인증 PDF 다운로드 버튼을 보여 줍니다."""
    activity_label = clean_text_for_display(activity_name)
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#dcfce7,#bbf7d0); padding:20px; border-radius:18px; border:2px solid #86efac; margin-top:18px; text-align:center;">
            <div style="font-size:1.45rem; font-weight:1000; color:#14532d;">🎉 {activity_label} 임무를 완성하셨습니다.</div>
            <div style="font-size:1.02rem; font-weight:850; color:#166534; margin-top:6px;">PDF에는 완료한 활동명이 <b>{activity_label}</b>로 기록됩니다. 아래 버튼을 눌러 완료 인증 PDF를 저장하고, 나중에 선생님께 보여 주세요.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    pdf_bytes = make_mission_pdf(song_choice, activity_name, detail_text)
    if pdf_bytes:
        file_name = f"mission_complete_{safe_key(song_choice)}_{safe_key(activity_name)}.pdf"
        st.download_button(
            "📄 완료 인증 PDF 저장",
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
            show_mission_pdf_download(
                song_choice,
                "가사 이해도 퀴즈",
                f"{key_key}_lyrics_quiz_now",
                st.session_state.get(f"mission_{key_key}_lyrics_quiz_detail", "")
            )
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



def check_target_grammar_sentence(target, sentence):
    """학생이 직접 쓴 문장이 오늘의 오늘 배운 표현을 포함하는지 간단히 검사합니다.
    너무 엄격한 문법 채점기가 아니라, 핵심 구조가 들어갔는지 확인하는 용도입니다.
    """
    raw = str(sentence).strip()
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



    if target == "Let's + 동사":
        if re.search(r"\blet's\s+(?!to\b)\w+", low) or re.search(r"\blet\s+us\s+(?!to\b)\w+", low):
            return ok("좋아요. 함께 하자고 제안하는 Let's + 동사 형태를 잘 썼습니다.")
        if re.search(r"\blet's\s+to\s+\w+", low):
            return no("Let's 뒤에는 to를 쓰지 않고 동사를 바로 씁니다. 예: Let's skip the club.")
        return no("Let's + 동사 구조를 써 보세요. 예: Let's study English.")

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



GRAMMAR_POINTS = {'1. Let It Go - Frozen OST': {'target': 'Let + 사람/명사 + 동사',
                               'examples': ['Let it go.',
                                            'Let the storm rage on.',
                                            "Don't let them in.",
                                            "Don't let them see.",
                                            "Don't let them know."],
                               'frequent_options': ['will', 'can', 'let', 'have been'],
                               'frequent_answer': 'let',
                               'form_options': ['Let + 사람/명사 + 과거형',
                                                'Let + 사람/명사 + to + 동사',
                                                'Let + 사람/명사 + -ing 형태',
                                                'Let + 사람/명사 + 동사'],
                               'form_answer': 'Let + 사람/명사 + 동사',
                               'meaning_examples': [('Let it go.', '그것을 놓아버려.'),
                                                    ('Let them in.', '그들을 들어오게 해.'),
                                                    ('Let the storm rage on.', '폭풍이 계속 몰아치게 둬.')],
                               'meaning_options': ['어제 ...했다', '곧 ...할 것이다', '~가 ...하게 두다 / ...하게 하다', '...하고 있는 중이다'],
                               'meaning_answer': '~가 ...하게 두다 / ...하게 하다',
                               'rule_answer': 'Let + 사람/명사 + 동사 = ~가 ...하게 두다 / ...하게 하다',
                               'rule_options': ['Let + 사람/명사 + 과거형 = 어제 ~했다',
                                                'Let + 사람/명사 + to + 동사 = 반드시 ~해야 한다',
                                                'Let + 사람/명사 + -ing 형태 = ~하는 중이다',
                                                'Let + 사람/명사 + 동사 = ~가 ...하게 두다 / ...하게 하다'],
                               'practice': [('빈칸에 알맞은 것은? Let it _____.',
                                             ['goes', 'went', 'go', 'going'],
                                             'go',
                                             'Let 뒤에는 동사가 옵니다.'),
                                            ('맞는 문장은?',
                                             ['Let the storm rages on.',
                                              'Let the storm to rage on.',
                                              'Let the storm raging on.',
                                              'Let the storm rage on.'],
                                             'Let the storm rage on.',
                                             'Let + 사람/명사 + 동사'),
                                            ("Don't let them _____.",
                                             ['sees', 'saw', 'see', 'seeing'],
                                             'see',
                                             "Don't let + 사람/명사 + 동사"),
                                            ('Let it go.의 뜻은?',
                                             ['그것은 갔다.', '그것이 가고 있다.', '그것은 갈 것이다.', '그것을 놓아버려.'],
                                             '그것을 놓아버려.',
                                             'let it go는 놓아버리라는 뜻입니다.'),
                                            ('문장 완성: Let me _____.',
                                             ['tries', 'try', 'tried', 'trying'],
                                             'try',
                                             'Let me + 동사')],
                               'sentence_prefix': 'Let me',
                               'sentence_choices': ['try', 'speak', 'think', 'go', 'help you'],
                               'sentence_suffix': ''},
 '2. Hello - Adele': {'target': "I'm sorry for + 명사 또는 -ing 형태",
                      'examples': ["I'm sorry for everything that I've done.",
                                   "I'm sorry for breaking your heart.",
                                   "I'm sorry for being late.",
                                   "I'm sorry for making a mistake.",
                                   "I'm sorry for calling you late."],
                      'frequent_options': ['I can', 'I will', "I'm sorry for", 'Let it'],
                      'frequent_answer': "I'm sorry for",
                      'form_options': ["I'm sorry for + 동사",
                                       "I'm sorry for + will",
                                       "I'm sorry for + can",
                                       "I'm sorry for + 명사 또는 -ing 형태"],
                      'form_answer': "I'm sorry for + 명사 또는 -ing 형태",
                      'meaning_examples': [("I'm sorry for breaking your heart.", '네 마음을 아프게 해서 미안해.'),
                                           ("I'm sorry for being late.", '늦어서 미안해.'),
                                           ("I'm sorry for everything.", '모든 것에 대해 미안해.')],
                      'meaning_options': ['미래 계획을 말한다', '능력을 말한다', '미안한 이유를 말한다', '명령을 말한다'],
                      'meaning_answer': '미안한 이유를 말한다',
                      'rule_answer': "I'm sorry for + 명사 또는 -ing 형태 = ~해서 미안해",
                      'rule_options': ["I'm sorry for + 동사 = 나는 곧 ~할 거야",
                                       "I'm sorry for + can = 나는 ~할 수 있어",
                                       "I'm sorry for + will = 나는 ~해야 해",
                                       "I'm sorry for + 명사 또는 -ing 형태 = ~해서 미안해"],
                      'practice': [("빈칸에 알맞은 것은? I'm sorry for _____ your heart.",
                                    ['break', 'broke', 'breaking', 'breaks'],
                                    'breaking',
                                    'for 뒤에 행동을 넣을 때 -ing 형태를 씁니다.'),
                                   ('맞는 문장은?',
                                    ["I'm sorry for be late.",
                                     "I'm sorry for was late.",
                                     "I'm sorry for am late.",
                                     "I'm sorry for being late."],
                                    "I'm sorry for being late.",
                                    'be는 being으로 씁니다.'),
                                   ("I'm sorry for everything.의 뜻은?",
                                    ['나는 모든 것을 원해.', '모든 것이 좋아.', '모든 것에 대해 미안해.', '나는 모든 것을 할 수 있어.'],
                                    '모든 것에 대해 미안해.',
                                    'sorry for는 미안한 이유를 나타냅니다.'),
                                   ("빈칸: I'm sorry for _____ you late.",
                                    ['call', 'called', 'calls', 'calling'],
                                    'calling',
                                    'for + -ing 형태'),
                                   ('가장 알맞은 구조는?',
                                    ["I'm sorry for + 동사",
                                     "I'm sorry for + -ing 형태",
                                     "I'm sorry for + will",
                                     "I'm sorry for + 과거형만"],
                                    "I'm sorry for + -ing 형태",
                                    '미안한 행동은 -ing 형태로 표현할 수 있습니다.')],
                      'sentence_prefix': "I'm sorry for",
                      'sentence_choices': ['being late',
                                           'making a mistake',
                                           'calling you late',
                                           'breaking the rule',
                                           'not listening'],
                      'sentence_suffix': ''},
 '3. A Whole New World - Aladdin OST': {'target': 'can + 동사',
                                        'examples': ['I can show you the world.',
                                                     'I can open your eyes.',
                                                     'I can take you there.',
                                                     'I can help you.',
                                                     'I can see a whole new world.'],
                                        'frequent_options': ['I was', 'I have', 'I can', 'I used to'],
                                        'frequent_answer': 'I can',
                                        'form_options': ['can + 과거형',
                                                         'can + to + 동사',
                                                         'can + -ing 형태',
                                                         'can + 동사'],
                                        'form_answer': 'can + 동사',
                                        'meaning_examples': [('I can show you the world.', '나는 너에게 세상을 보여 줄 수 있어.'),
                                                             ('I can open your eyes.', '나는 너의 눈을 뜨게 해 줄 수 있어.'),
                                                             ('I can help you.', '나는 너를 도울 수 있어.')],
                                        'meaning_options': ['~했었다', '~하고 있는 중이다', '~할 수 있다', '~하지 마라'],
                                        'meaning_answer': '~할 수 있다',
                                        'rule_answer': 'can + 동사 = ~할 수 있다',
                                        'rule_options': ['can + 과거형 = 어제 ~했다',
                                                         'can + to + 동사 = ~해야 한다',
                                                         'can + ing = ~하고 있다',
                                                         'can + 동사 = ~할 수 있다'],
                                        'practice': [('빈칸: I can _____ you the world.',
                                                      ['shows', 'showed', 'show', 'showing'],
                                                      'show',
                                                      'can 뒤에는 동사가 옵니다.'),
                                                     ('맞는 문장은?',
                                                      ['I can opens your eyes.',
                                                       'I can to open your eyes.',
                                                       'I can opening your eyes.',
                                                       'I can open your eyes.'],
                                                      'I can open your eyes.',
                                                      'can + 동사'),
                                                     ('I can help you.의 뜻은?',
                                                      ['나는 너를 도왔다.',
                                                       '나는 너를 돕고 있다.',
                                                       '나는 너를 도울 수 있어.',
                                                       '나는 너를 도울 수 없다.'],
                                                      '나는 너를 도울 수 있어.',
                                                      'can은 능력/가능을 나타냅니다.'),
                                                     ('빈칸: We can _____ together.',
                                                      ['goes', 'went', 'going', 'go'],
                                                      'go',
                                                      'can + 동사'),
                                                     ('알맞은 구조는?',
                                                      ['can + to + 동사',
                                                       'can + 동사',
                                                       'can + 과거형',
                                                       'can + ing'],
                                                      'can + 동사',
                                                      'can 뒤에는 동사입니다.')],
                                        'sentence_prefix': 'I can',
                                        'sentence_choices': ['show you the world',
                                                             'help you',
                                                             'open the door',
                                                             'speak English',
                                                             'try again'],
                                        'sentence_suffix': ''},
 '4. Stand By Me - Ben E. King': {'target': "won't + 동사",
                                  'examples': ["I won't be afraid.",
                                               "I won't cry.",
                                               "I won't shed a tear.",
                                               "I won't give up.",
                                               "I won't run away."],
                                  'frequent_options': ['I was', 'I have', "I won't", 'I used to'],
                                  'frequent_answer': "I won't",
                                  'form_options': ["won't + 과거형",
                                                   "won't + to + 동사",
                                                   "won't + -ing 형태",
                                                   "won't + 동사"],
                                  'form_answer': "won't + 동사",
                                  'meaning_examples': [("I won't be afraid.", '나는 두려워하지 않을 거야.'),
                                                       ("I won't cry.", '나는 울지 않을 거야.'),
                                                       ("I won't give up.", '나는 포기하지 않을 거야.')],
                                  'meaning_options': ['~할 수 있다', '~했었다', '~하지 않을 것이다', '~하는 중이다'],
                                  'meaning_answer': '~하지 않을 것이다',
                                  'rule_answer': "won't + 동사 = ~하지 않을 것이다",
                                  'rule_options': ["won't + 과거형 = 어제 ~하지 않았다",
                                                   "won't + ing = ~하지 않는 중이다",
                                                   "won't + to + 동사 = ~할 수 있다",
                                                   "won't + 동사 = ~하지 않을 것이다"],
                                  'practice': [("빈칸: I won't _____ afraid.",
                                                ['am', 'was', 'be', 'being'],
                                                'be',
                                                "won't 뒤에는 동사 be가 옵니다."),
                                               ('맞는 문장은?',
                                                ["I won't cried.",
                                                 "I won't crying.",
                                                 "I won't to cry.",
                                                 "I won't cry."],
                                                "I won't cry.",
                                                "won't + 동사"),
                                               ("I won't shed a tear.의 뜻은?",
                                                ['나는 지금 울고 있다.', '나는 어제 울었다.', '나는 눈물 한 방울도 흘리지 않을 거야.', '나는 울 수 있다.'],
                                                '나는 눈물 한 방울도 흘리지 않을 거야.',
                                                "won't는 미래 부정입니다."),
                                               ("빈칸: I won't _____ up.",
                                                ['gave', 'gives', 'giving', 'give'],
                                                'give',
                                                "won't + 동사"),
                                               ('알맞은 구조는?',
                                                ["won't + 과거형",
                                                 "won't + 동사",
                                                 "won't + ing",
                                                 "won't + to + 동사"],
                                                "won't + 동사",
                                                '미래에 하지 않을 일을 말합니다.')],
                                  'sentence_prefix': "I won't",
                                  'sentence_choices': ['be afraid', 'cry', 'give up', 'run away', 'forget you'],
                                  'sentence_suffix': ''},
 "5. Don't Know Why - Norah Jones": {'target': "I don't know why + 문장",
                                     'examples': ["I don't know why I didn't come.",
                                                  "Don't know why I didn't come.",
                                                  "I don't know why I feel this way.",
                                                  "I don't know why I waited.",
                                                  "I don't know why she left."],
                                     'frequent_options': ['I can', 'I will', "I don't know why", 'Let me'],
                                     'frequent_answer': "I don't know why",
                                     'form_options': ["I don't know why + 동사만",
                                                      "I don't know why + can만",
                                                      "I don't know why + 명사만",
                                                      "I don't know why + 주어 + 동사/상태"],
                                     'form_answer': "I don't know why + 주어 + 동사/상태",
                                     'meaning_examples': [("I don't know why I didn't come.", '나는 왜 내가 가지 않았는지 모르겠어.'),
                                                          ("I don't know why I feel this way.", '나는 왜 이렇게 느끼는지 모르겠어.'),
                                                          ("I don't know why she left.", '나는 왜 그녀가 떠났는지 모르겠어.')],
                                     'meaning_options': ['능력을 말한다', '명령한다', '이유를 모른다고 말한다', '미래 계획을 말한다'],
                                     'meaning_answer': '이유를 모른다고 말한다',
                                     'rule_answer': "I don't know why + 주어 + 동사/상태 = 왜 ~인지 모르겠다",
                                     'rule_options': ["I don't know why + 동사 = ~할 수 있다",
                                                      "I don't know why + will = ~할 것이다",
                                                      "I don't know why + ing = ~하는 중이다",
                                                      "I don't know why + 주어 + 동사/상태 = 왜 ~인지 모르겠다"],
                                     'practice': [("빈칸: I don't know why I _____ come.",
                                                   ["don't", 'can', "didn't", 'will'],
                                                   "didn't",
                                                   'why 뒤에는 하나의 문장이 올 수 있습니다.'),
                                                  ('맞는 문장은?',
                                                   ["I don't know why feel sad.",
                                                    "I don't know why to feel sad.",
                                                    "I don't know why feeling sad.",
                                                    "I don't know why I feel sad."],
                                                   "I don't know why I feel sad.",
                                                   'why 뒤에는 주어 + 동사/상태를 넣습니다.'),
                                                  ("I don't know why she left.의 뜻은?",
                                                   ['나는 그녀가 떠날 수 있어.',
                                                    '나는 그녀를 떠나게 했다.',
                                                    '나는 왜 그녀가 떠났는지 모르겠어.',
                                                    '나는 그녀가 떠나길 원해.'],
                                                   '나는 왜 그녀가 떠났는지 모르겠어.',
                                                   '이유를 모른다는 뜻입니다.'),
                                                  ("빈칸: I don't know why he _____ angry.",
                                                   ['be', 'to be', 'being', 'is'],
                                                   'is',
                                                   'why 뒤에는 문장 형태가 옵니다.'),
                                                  ('알맞은 구조는?',
                                                   ["I don't know why + 동사만",
                                                    "I don't know why + 주어 + 동사/상태",
                                                    "I don't know why + to + 동사",
                                                    "I don't know why + 명사만"],
                                                   "I don't know why + 주어 + 동사/상태",
                                                   '왜 ~인지 모르겠다고 말합니다.')],
                                     'sentence_prefix': "I don't know why",
                                     'sentence_choices': ['I feel this way',
                                                          'I waited',
                                                          'she left',
                                                          'I am tired',
                                                          'he is angry'],
                                     'sentence_suffix': ''},
 '6. Fix You - Coldplay': {'target': 'When + 주어 + 동사/상태',
                           'examples': ['When you try your best.',
                                        'When you get what you want.',
                                        'When you feel so tired.',
                                        'When you lose something.',
                                        'When you love someone.'],
                           'frequent_options': ['I can', 'I will', 'When you', 'Let it'],
                           'frequent_answer': 'When you',
                           'form_options': ['When + 동사만',
                                            'When + will만',
                                            'When + 명사만',
                                            'When + 주어 + 동사/상태'],
                           'form_answer': 'When + 주어 + 동사/상태',
                           'meaning_examples': [('When you try your best.', '네가 최선을 다할 때.'),
                                                ('When you feel tired.', '네가 피곤함을 느낄 때.'),
                                                ('When you lose something.', '네가 무언가를 잃을 때.')],
                           'meaning_options': ['~할 수 있다', '~하지 않을 것이다', '~할 때', '~해야 한다'],
                           'meaning_answer': '~할 때',
                           'rule_answer': 'When + 주어 + 동사/상태 = ~할 때',
                           'rule_options': ['When + 동사 = ~할 수 있다',
                                            'When + will = ~하지 않을 것이다',
                                            'When + ing = ~하고 있다',
                                            'When + 주어 + 동사/상태 = ~할 때'],
                           'practice': [('빈칸: When you _____ your best.',
                                         ['tries', 'tried', 'try', 'trying'],
                                         'try',
                                         'you 뒤에는 동사 try가 옵니다.'),
                                        ('맞는 문장은?',
                                         ['When feel tired.',
                                          'When you to feel tired.',
                                          'When you feeling tired.',
                                          'When you feel tired.'],
                                         'When you feel tired.',
                                         'When + 주어 + 동사/상태'),
                                        ('When you lose something.의 뜻은?',
                                         ['너는 무언가를 잃을 수 있다', '너는 무언가를 잃지 않을 것이다', '네가 무언가를 잃을 때', '너는 무언가를 잃었다'],
                                         '네가 무언가를 잃을 때',
                                         'When은 ~할 때입니다.'),
                                        ('빈칸: When you _____ someone.',
                                         ['loves', 'loved', 'loving', 'love'],
                                         'love',
                                         'When you + 동사'),
                                        ('알맞은 구조는?',
                                         ['When + 동사만',
                                          'When + 주어 + 동사/상태',
                                          'When + to + 동사',
                                          'When + 어려운 문법 형태'],
                                         'When + 주어 + 동사/상태',
                                         '상황을 말할 때 씁니다.')],
                           'sentence_prefix': 'When I',
                           'sentence_choices': ['try my best',
                                                'feel tired',
                                                'need help',
                                                'lose something',
                                                'love someone'],
                           'sentence_suffix': ''},
 '7. The Scientist - Coldplay': {'target': 'Tell + 사람 + 내용',
                                 'examples': ["Tell you I'm sorry.",
                                              'Tell you I need you.',
                                              'Tell me your secrets.',
                                              'Tell me your questions.',
                                              'Tell me you love me.'],
                                 'frequent_options': ['I will', 'I can', 'Tell me / Tell you', 'I used to'],
                                 'frequent_answer': 'Tell me / Tell you',
                                 'form_options': ['Tell + 사람 + to be만',
                                                  'Tell + 과거형만',
                                                  'Tell + ing만',
                                                  'Tell + 사람 + 내용'],
                                 'form_answer': 'Tell + 사람 + 내용',
                                 'meaning_examples': [("Tell you I'm sorry.", '너에게 미안하다고 말하다.'),
                                                      ('Tell you I need you.', '너에게 네가 필요하다고 말하다.'),
                                                      ('Tell me your secrets.', '나에게 너의 비밀을 말해 줘.')],
                                 'meaning_options': ['누군가를 볼 수 있다', '미래에 하지 않을 것이다', '누구에게 어떤 내용을 말하다', '계속 하고 있다'],
                                 'meaning_answer': '누구에게 어떤 내용을 말하다',
                                 'rule_answer': 'Tell + 사람 + 내용 = 누구에게 ~을 말하다',
                                 'rule_options': ['Tell + 사람 + ing = ~하는 중이다',
                                                  'Tell + 사람 + will = ~할 것이다',
                                                  'Tell + 사람 + can = ~할 수 있다',
                                                  'Tell + 사람 + 내용 = 누구에게 ~을 말하다'],
                                 'practice': [('빈칸: Tell me your _____.',
                                               ['secretly', 'secreted', 'secrets', 'secreting'],
                                               'secrets',
                                               'Tell me + 내용'),
                                              ('맞는 문장은?',
                                               ['Tell you am sorry.',
                                                "Tell you to I'm sorry.",
                                                'Tell you sorrying.',
                                                "Tell you I'm sorry."],
                                               "Tell you I'm sorry.",
                                               'Tell + 사람 + 내용'),
                                              ('Tell me your secrets.의 뜻은?',
                                               ['나에게 노래를 불러 줘.', '나를 도와줄 수 있어.', '나에게 너의 비밀을 말해 줘.', '나는 비밀을 몰라.'],
                                               '나에게 너의 비밀을 말해 줘.',
                                               'Tell me는 나에게 말해 줘입니다.'),
                                              ('빈칸: Tell me you _____ me.',
                                               ['loves', 'loving', 'to love', 'love'],
                                               'love',
                                               'Tell me + 문장'),
                                              ('알맞은 구조는?',
                                               ['Tell + 사람 + ing만', 'Tell + 사람 + 내용', 'Tell + 과거형만', 'Tell + will만'],
                                               'Tell + 사람 + 내용',
                                               '말하는 상대와 내용을 함께 씁니다.')],
                                 'sentence_prefix': 'Tell me',
                                 'sentence_choices': ['your name',
                                                      'your dream',
                                                      'you need help',
                                                      'you are okay',
                                                      'the truth'],
                                 'sentence_suffix': ''},
 '8. My Heart Will Go On - Celine Dion': {'target': 'will + 동사',
                                          'examples': ['My heart will go on.',
                                                       'We will stay forever.',
                                                       'I will remember you.',
                                                       'Love will last.',
                                                       'I will see you in my dreams.'],
                                          'frequent_options': ['can', 'used to', 'will', 'let'],
                                          'frequent_answer': 'will',
                                          'form_options': ['will + 과거형',
                                                           'will + to + 동사',
                                                           'will + -ing 형태',
                                                           'will + 동사'],
                                          'form_answer': 'will + 동사',
                                          'meaning_examples': [('My heart will go on.', '내 마음은 계속될 거야.'),
                                                               ('We will stay forever.', '우리는 영원히 머물 거야.'),
                                                               ('I will remember you.', '나는 너를 기억할 거야.')],
                                          'meaning_options': ['~할 수 있다', '예전에 ~하곤 했다', '앞으로 ~할 것이다', '~하지 마라'],
                                          'meaning_answer': '앞으로 ~할 것이다',
                                          'rule_answer': 'will + 동사 = 앞으로 ~할 것이다',
                                          'rule_options': ['will + 과거형 = 어제 ~했다',
                                                           'will + ing = ~하고 있다',
                                                           'will + to + 동사 = ~할 수 있다',
                                                           'will + 동사 = 앞으로 ~할 것이다'],
                                          'practice': [('빈칸: My heart will _____ on.',
                                                        ['goes', 'went', 'go', 'going'],
                                                        'go',
                                                        'will 뒤에는 동사입니다.'),
                                                       ('맞는 문장은?',
                                                        ['We will stays forever.',
                                                         'We will stayed forever.',
                                                         'We will to stay forever.',
                                                         'We will stay forever.'],
                                                        'We will stay forever.',
                                                        'will + 동사'),
                                                       ('I will remember you.의 뜻은?',
                                                        ['나는 너를 기억했다.',
                                                         '나는 너를 기억하고 있다.',
                                                         '나는 너를 기억할 거야.',
                                                         '나는 너를 기억할 수 없다.'],
                                                        '나는 너를 기억할 거야.',
                                                        'will은 미래를 나타냅니다.'),
                                                       ('빈칸: Love will _____.',
                                                        ['lasts', 'lasted', 'lasting', 'last'],
                                                        'last',
                                                        'will + 동사'),
                                                       ('알맞은 구조는?',
                                                        ['will + 과거형',
                                                         'will + 동사',
                                                         'will + ing',
                                                         'will + to + 동사'],
                                                        'will + 동사',
                                                        '미래 표현입니다.')],
                                          'sentence_prefix': 'I will',
                                          'sentence_choices': ['remember you',
                                                               'try again',
                                                               'study English',
                                                               'help my friend',
                                                               'go on'],
                                          'sentence_suffix': ''},
 '9. Alex Sampson - Play Pretend': {'target': "It's hard to + 동사",
                                    'examples': ["It's hard to watch you fall again.",
                                                 "It's hard to play pretend.",
                                                 "It's hard to say goodbye.",
                                                 "It's hard to wait.",
                                                 "It's hard to tell the truth."],
                                    'frequent_options': ['I can', 'I will', "It's hard to", 'Let me'],
                                    'frequent_answer': "It's hard to",
                                    'form_options': ["It's hard to + 과거형",
                                                     "It's hard to + ing",
                                                     "It's hard to + can",
                                                     "It's hard to + 동사"],
                                    'form_answer': "It's hard to + 동사",
                                    'meaning_examples': [("It's hard to watch you fall again.",
                                                          '네가 다시 상처받는 걸 보는 것은 힘들어.'),
                                                         ("It's hard to say goodbye.", '작별 인사를 하는 것은 힘들어.'),
                                                         ("It's hard to wait.", '기다리는 것은 힘들어.')],
                                    'meaning_options': ['~할 수 있다', '~하지 않을 것이다', '~하는 것은 힘들다', '~하곤 했다'],
                                    'meaning_answer': '~하는 것은 힘들다',
                                    'rule_answer': "It's hard to + 동사 = ~하는 것은 힘들다",
                                    'rule_options': ["It's hard to + ing = ~하고 있다",
                                                     "It's hard to + 과거형 = 어제 ~했다",
                                                     "It's hard to + will = ~할 것이다",
                                                     "It's hard to + 동사 = ~하는 것은 힘들다"],
                                    'practice': [("빈칸: It's hard to _____ you fall again.",
                                                  ['watches', 'watched', 'watch', 'watching'],
                                                  'watch',
                                                  'to 뒤에는 동사가 옵니다.'),
                                                 ('맞는 문장은?',
                                                  ["It's hard to saying goodbye.",
                                                   "It's hard to said goodbye.",
                                                   "It's hard to says goodbye.",
                                                   "It's hard to say goodbye."],
                                                  "It's hard to say goodbye.",
                                                  'hard to + 동사'),
                                                 ("It's hard to wait.의 뜻은?",
                                                  ['기다릴 수 있다.', '기다리지 않을 것이다.', '기다리는 것은 힘들다.', '기다리곤 했다.'],
                                                  '기다리는 것은 힘들다.',
                                                  'It is hard to는 ~하기 어렵다는 뜻입니다.'),
                                                 ("빈칸: It's hard to _____ the truth.",
                                                  ['tells', 'told', 'telling', 'tell'],
                                                  'tell',
                                                  'to + 동사'),
                                                 ('알맞은 구조는?',
                                                  ["It's hard to + ing",
                                                   "It's hard to + 동사",
                                                   "It's hard to + 과거형",
                                                   "It's hard to + can"],
                                                  "It's hard to + 동사",
                                                  '어려운 행동을 말할 때 씁니다.')],
                                    'sentence_prefix': "It's hard to",
                                    'sentence_choices': ['say goodbye',
                                                         'wait',
                                                         'study every day',
                                                         'tell the truth',
                                                         'play pretend'],
                                    'sentence_suffix': ''},
 '10. Older - Sasha Alex Sloan': {'target': 'used to + 동사',
                                  'examples': ['I used to shut my door.',
                                               'I used to listen to music.',
                                               'I used to be a kid.',
                                               'I used to play outside.',
                                               'I used to cry sometimes.'],
                                  'frequent_options': ['will', 'can', 'used to', 'let'],
                                  'frequent_answer': 'used to',
                                  'form_options': ['used to + 과거형',
                                                   'used to + ing',
                                                   'used to + will',
                                                   'used to + 동사'],
                                  'form_answer': 'used to + 동사',
                                  'meaning_examples': [('I used to shut my door.', '나는 예전에 방문을 닫곤 했다.'),
                                                       ('I used to play outside.', '나는 예전에 밖에서 놀곤 했다.'),
                                                       ('I used to be a kid.', '나는 예전에는 아이였다.')],
                                  'meaning_options': ['지금 ~하고 있다', '앞으로 ~할 것이다', '예전에 ~하곤 했다', '~할 수 있다'],
                                  'meaning_answer': '예전에 ~하곤 했다',
                                  'rule_answer': 'used to + 동사 = 예전에 ~하곤 했다',
                                  'rule_options': ['used to + ing = 지금 ~하고 있다',
                                                   'used to + 과거형 = 내일 ~할 것이다',
                                                   'used to + can = ~할 수 있다',
                                                   'used to + 동사 = 예전에 ~하곤 했다'],
                                  'practice': [('빈칸: I used to _____ my door.',
                                                ['shuts', 'shutting', 'shut', 'shutted'],
                                                'shut',
                                                'used to 뒤에는 동사가 옵니다.'),
                                               ('맞는 문장은?',
                                                ['I used to played outside.',
                                                 'I used to playing outside.',
                                                 'I used to plays outside.',
                                                 'I used to play outside.'],
                                                'I used to play outside.',
                                                'used to + 동사'),
                                               ('I used to be a kid.의 뜻은?',
                                                ['나는 지금 아이가 되고 있다.', '나는 아이가 될 것이다.', '나는 예전에는 아이였다.', '나는 아이일 수 있다.'],
                                                '나는 예전에는 아이였다.',
                                                'used to는 과거의 습관/상태입니다.'),
                                               ('빈칸: I used to _____ music.',
                                                ['listened to', 'listening to', 'listens to', 'listen to'],
                                                'listen to',
                                                'used to + 동사'),
                                               ('알맞은 구조는?',
                                                ['used to + 과거형',
                                                 'used to + 동사',
                                                 'used to + ing',
                                                 'used to + will'],
                                                'used to + 동사',
                                                '예전 습관을 말합니다.')],
                                  'sentence_prefix': 'I used to',
                                  'sentence_choices': ['play outside',
                                                       'listen to music',
                                                       'be shy',
                                                       'watch cartoons',
                                                       'cry sometimes'],
                                  'sentence_suffix': ''},
 '11. No One Else Like You - Adam Levine': {'target': 'like + 명사',
                                            'examples': ['Looks like you.',
                                                         'Feels like you.',
                                                         'Smiles like you.',
                                                         'Someone just like you.',
                                                         'No one else like you.'],
                                            'frequent_options': ['will be', 'have been', 'like you', 'used to'],
                                            'frequent_answer': 'like you',
                                            'form_options': ['like + 과거형',
                                                             'like + to + 동사',
                                                             'like + will',
                                                             'like + 명사'],
                                            'form_answer': 'like + 명사',
                                            'meaning_examples': [('Looks like you.', '너처럼 보여.'),
                                                                 ('Feels like you.', '너 같은 느낌이야.'),
                                                                 ('Someone just like you.', '너와 꼭 같은 사람.')],
                                            'meaning_options': ['~할 것이다', '~하지 않을 것이다', '~처럼 / ~같은', '예전에 ~했다'],
                                            'meaning_answer': '~처럼 / ~같은',
                                            'rule_answer': 'like + 명사 = ~처럼 / ~같은',
                                            'rule_options': ['like + 동사 = ~해야 한다',
                                                             'like + will = ~할 것이다',
                                                             'like + 과거형 = ~했다',
                                                             'like + 명사 = ~처럼 / ~같은'],
                                            'practice': [('빈칸: Someone just _____ you.',
                                                          ['likes', 'liked', 'like', 'liking'],
                                                          'like',
                                                          'like you는 너 같은이라는 뜻입니다.'),
                                                         ('맞는 표현은?',
                                                          ['Looks likes you.',
                                                           'Looks liked you.',
                                                           'Looks liking you.',
                                                           'Looks like you.'],
                                                          'Looks like you.',
                                                          'like + 명사'),
                                                         ('No one else like you.의 뜻은?',
                                                          ['너는 다른 사람을 좋아해.',
                                                           '너는 곧 올 거야.',
                                                           '너 같은 사람은 아무도 없어.',
                                                           '너는 예전에 그랬어.'],
                                                          '너 같은 사람은 아무도 없어.',
                                                          'like는 ~같은의 뜻입니다.'),
                                                         ('빈칸: It feels _____ home.',
                                                          ['likes', 'liked', 'liking', 'like'],
                                                          'like',
                                                          'like + 명사'),
                                                         ('알맞은 구조는?',
                                                          ['like + will',
                                                           'like + 명사',
                                                           'like + 과거형',
                                                           'like + to + 동사'],
                                                          'like + 명사',
                                                          '비슷함을 말할 때 씁니다.')],
                                            'sentence_prefix': 'It feels like',
                                            'sentence_choices': ['home', 'a dream', 'a movie', 'summer', 'a new start'],
                                            'sentence_suffix': ''},
 '12. Out of Time - The Weeknd': {'target': "I'll + 동사",
                                  'examples': ["I'll treat you right.",
                                               "I'll love you.",
                                               "I'll care for you.",
                                               "I'll be there for you.",
                                               "I'll try again."],
                                  'frequent_options': ['I used to', 'Let me', "I'll", "I don't know why"],
                                  'frequent_answer': "I'll",
                                  'form_options': ["I'll + 과거형",
                                                   "I'll + to + 동사",
                                                   "I'll + -ing 형태",
                                                   "I'll + 동사"],
                                  'form_answer': "I'll + 동사",
                                  'meaning_examples': [("I'll treat you right.", '나는 너를 잘 대해 줄 거야.'),
                                                       ("I'll love you.", '나는 너를 사랑할 거야.'),
                                                       ("I'll care for you.", '나는 너를 아껴 줄 거야.')],
                                  'meaning_options': ['예전에 ~하곤 했다', '~할 수 있다', '앞으로 ~할 것이다', '~하지 마라'],
                                  'meaning_answer': '앞으로 ~할 것이다',
                                  'rule_answer': "I'll + 동사 = 나는 ~할 것이다",
                                  'rule_options': ["I'll + 과거형 = 나는 어제 ~했다",
                                                   "I'll + ing = 나는 ~하고 있다",
                                                   "I'll + to + 동사 = 나는 ~할 수 있다",
                                                   "I'll + 동사 = 나는 ~할 것이다"],
                                  'practice': [("빈칸: I'll _____ you right.",
                                                ['treats', 'treated', 'treat', 'treating'],
                                                'treat',
                                                "I'll 뒤에는 동사입니다."),
                                               ('맞는 문장은?',
                                                ["I'll loves you.",
                                                 "I'll loved you.",
                                                 "I'll loving you.",
                                                 "I'll love you."],
                                                "I'll love you.",
                                                "I'll + 동사"),
                                               ("I'll care for you.의 뜻은?",
                                                ['나는 너를 아꼈어.', '나는 너를 아끼고 있어.', '나는 너를 아껴 줄 거야.', '나는 너를 아낄 수 없어.'],
                                                '나는 너를 아껴 줄 거야.',
                                                "I'll은 I will의 짧은 형태입니다."),
                                               ("빈칸: I'll _____ again.",
                                                ['tries', 'tried', 'trying', 'try'],
                                                'try',
                                                "I'll + 동사"),
                                               ('알맞은 구조는?',
                                                ["I'll + 과거형", "I'll + 동사", "I'll + ing", "I'll + to + 동사"],
                                                "I'll + 동사",
                                                '미래의 약속/의지를 말합니다.')],
                                  'sentence_prefix': "I'll",
                                  'sentence_choices': ['try again',
                                                       'help you',
                                                       'study hard',
                                                       'be there',
                                                       'care for you'],
                                  'sentence_suffix': ''},
 "13. I Don't Think So - Priscilla Ahn": {'target': "I think + 문장 / I don't think so",
                                          'examples': ["I don't think so.",
                                                       'I think I should go.',
                                                       'I think you know it.',
                                                       "I don't think I can stay.",
                                                       'I think this is wrong.'],
                                          'frequent_options': ['I will', 'Let it', 'I think', 'used to'],
                                          'frequent_answer': 'I think',
                                          'form_options': ['I think + 동사만',
                                                           'I think + to + 동사',
                                                           'I think + ing만',
                                                           'I think + 문장'],
                                          'form_answer': 'I think + 문장',
                                          'meaning_examples': [("I don't think so.", '나는 그렇게 생각하지 않아.'),
                                                               ('I think I should go.', '나는 가야 할 것 같아.'),
                                                               ('I think this is wrong.', '나는 이것이 잘못됐다고 생각해.')],
                                          'meaning_options': ['능력을 말한다', '과거 습관을 말한다', '내 생각을 말한다', '명령한다'],
                                          'meaning_answer': '내 생각을 말한다',
                                          'rule_answer': 'I think + 문장 = 나는 ~라고 생각한다',
                                          'rule_options': ['I think + 동사 = ~할 수 있다',
                                                           'I think + ing = ~하는 중이다',
                                                           'I think + will만 = ~하지 마라',
                                                           'I think + 문장 = 나는 ~라고 생각한다'],
                                          'practice': [('빈칸: I think I _____ go.',
                                                        ['can to', 'am to', 'should', 'going'],
                                                        'should',
                                                        'I think 뒤에 문장이 올 수 있습니다.'),
                                                       ('맞는 문장은?',
                                                        ['I think this wrong.',
                                                         'I think to this is wrong.',
                                                         'I think wronging.',
                                                         'I think this is wrong.'],
                                                        'I think this is wrong.',
                                                        'I think + 문장'),
                                                       ("I don't think so.의 뜻은?",
                                                        ['나는 그렇게 할 수 있어.',
                                                         '나는 그렇게 했어.',
                                                         '나는 그렇게 생각하지 않아.',
                                                         '나는 그렇게 할 거야.'],
                                                        '나는 그렇게 생각하지 않아.',
                                                        '의견을 말하는 표현입니다.'),
                                                       ("빈칸: I don't think I _____ stay.",
                                                        ['to can', 'canning', 'canned', 'can'],
                                                        'can',
                                                        'I think 뒤에는 문장을 씁니다.'),
                                                       ('알맞은 구조는?',
                                                        ['I think + 동사만',
                                                         'I think + 문장',
                                                         'I think + to + 동사',
                                                         'I think + ing만'],
                                                        'I think + 문장',
                                                        '생각/의견을 말합니다.')],
                                          'sentence_prefix': 'I think',
                                          'sentence_choices': ['I should go',
                                                               'this is important',
                                                               'English is fun',
                                                               'I can do it',
                                                               'we need time'],
                                          'sentence_suffix': ''},
 '14. New York City - Norah Jones': {'target': "can't + 동사",
                                     'examples': ["I can't remember what I planned.",
                                                  "I can't remember when it's time to go.",
                                                  "I can't sleep tonight.",
                                                  "I can't forget the city.",
                                                  "I can't find my way."],
                                     'frequent_options': ['I used to', 'I will', "I can't", 'Let me'],
                                     'frequent_answer': "I can't",
                                     'form_options': ["can't + 과거형",
                                                      "can't + to + 동사",
                                                      "can't + -ing 형태",
                                                      "can't + 동사"],
                                     'form_answer': "can't + 동사",
                                     'meaning_examples': [("I can't remember.", '나는 기억할 수 없어.'),
                                                          ("I can't sleep.", '나는 잠을 잘 수 없어.'),
                                                          ("I can't forget the city.", '나는 그 도시를 잊을 수 없어.')],
                                     'meaning_options': ['~할 것이다', '~하곤 했다', '~할 수 없다', '~하게 두다'],
                                     'meaning_answer': '~할 수 없다',
                                     'rule_answer': "can't + 동사 = ~할 수 없다",
                                     'rule_options': ["can't + 과거형 = 어제 ~하지 않았다",
                                                      "can't + ing = ~하는 중이 아니다",
                                                      "can't + to + 동사 = ~해야 한다",
                                                      "can't + 동사 = ~할 수 없다"],
                                     'practice': [("빈칸: I can't _____ what I planned.",
                                                   ['remembers', 'remembered', 'remember', 'remembering'],
                                                   'remember',
                                                   "can't 뒤에는 동사입니다."),
                                                  ('맞는 문장은?',
                                                   ["I can't sleeps tonight.",
                                                    "I can't slept tonight.",
                                                    "I can't sleeping tonight.",
                                                    "I can't sleep tonight."],
                                                   "I can't sleep tonight.",
                                                   "can't + 동사"),
                                                  ("I can't forget the city.의 뜻은?",
                                                   ['나는 그 도시를 잊었어.',
                                                    '나는 그 도시를 잊을 거야.',
                                                    '나는 그 도시를 잊을 수 없어.',
                                                    '나는 그 도시를 좋아해.'],
                                                   '나는 그 도시를 잊을 수 없어.',
                                                   "can't는 할 수 없다는 뜻입니다."),
                                                  ("빈칸: I can't _____ my way.",
                                                   ['finds', 'found', 'finding', 'find'],
                                                   'find',
                                                   "can't + 동사"),
                                                  ('알맞은 구조는?',
                                                   ["can't + 과거형",
                                                    "can't + 동사",
                                                    "can't + ing",
                                                    "can't + to + 동사"],
                                                   "can't + 동사",
                                                   '불가능을 말합니다.')],
                                     'sentence_prefix': "I can't",
                                     'sentence_choices': ['remember',
                                                          'sleep',
                                                          'forget you',
                                                          'find my way',
                                                          'stop thinking'],
                                     'sentence_suffix': ''},
 '15. Counting Stars - OneRepublic': {'target': 'I have been + -ing 형태',
                                      'examples': ["Lately, I've been losing sleep.",
                                                   "Baby, I've been praying hard.",
                                                   "I've been dreaming about the things that we could be.",
                                                   "Lately, I've been thinking about my future.",
                                                   "Lately, I've been practicing English."],
                                      'frequent_options': ['I can', 'I will', "I've been", 'I used to'],
                                      'frequent_answer': "I've been",
                                      'form_options': ['I have been + 동사',
                                                       'I have been + 과거형',
                                                       'I have been + 명사',
                                                       'I have been + -ing 형태'],
                                      'form_answer': 'I have been + -ing 형태',
                                      'meaning_examples': [('Lately, I have been losing sleep.', '요즘 잠을 잘 못 자고 있다.'),
                                                           ('Lately, I have been thinking about my dream.',
                                                            '요즘 내 꿈에 대해 계속 생각하고 있다.'),
                                                           ('Lately, I have been practicing English.',
                                                            '요즘 영어를 계속 연습하고 있다.')],
                                      'meaning_options': ['어제 한 번 끝난 행동',
                                                          '내일 새로 시작할 행동',
                                                          '최근부터 지금까지 이어지는 행동이나 상태',
                                                          '항상 변하지 않는 일반 사실'],
                                      'meaning_answer': '최근부터 지금까지 이어지는 행동이나 상태',
                                      'rule_answer': 'I have been + -ing 형태 = 최근부터 지금까지 계속 ~하고 있다',
                                      'rule_options': ['I have been + 동사 = 내일 ~할 것이다',
                                                       'I am + -ing 형태 = 어제 ~했다',
                                                       'I will + 동사 = 지금까지 계속 ~하고 있다',
                                                       'I have been + -ing 형태 = 최근부터 지금까지 계속 ~하고 있다'],
                                      'practice': [('I’ve been의 긴 형태로 알맞은 것은?',
                                                    ['I am been', 'I will been', 'I have been', 'I did been'],
                                                    'I have been',
                                                    'I’ve been = I have been'),
                                                   ('맞는 문장은?',
                                                    ['I have been study English.',
                                                     'I have studying English.',
                                                     'I been studying English.',
                                                     'I have been studying English.'],
                                                    'I have been studying English.',
                                                    'have been + -ing 형태'),
                                                   ('빈칸: Lately, I have been _____ soccer.',
                                                    ['play', 'played', 'playing', 'plays'],
                                                    'playing',
                                                    'I have been playing soccer.'),
                                                   ('I have been losing sleep.의 뜻은?',
                                                    ['나는 지금 자고 있다.',
                                                     '나는 어제 잠을 많이 잤다.',
                                                     '나는 내일 일찍 잘 것이다.',
                                                     '나는 요즘 잠을 잘 못 자고 있다.'],
                                                    '나는 요즘 잠을 잘 못 자고 있다.',
                                                    '최근부터 지금까지 이어지는 상태입니다.'),
                                                   ('빈칸: I’ve been _____ about my future.',
                                                    ['think', 'thinking', 'thought', 'thinks'],
                                                    'thinking',
                                                    'I’ve been thinking about my future.')],
                                      'sentence_prefix': 'Lately, I have been',
                                      'sentence_choices': ['studying English',
                                                           'playing soccer',
                                                           'thinking about my dream',
                                                           'feeling tired',
                                                           'practicing singing'],
                                      'sentence_suffix': ''},
 '16. Fly to the Moon - Peder Elias': {'target': "can't + 동사",
                                       'examples': ["Ain't nothing we can't do.",
                                                    "There's nothing we can't do.",
                                                    "We can't give up.",
                                                    "We can't stop dreaming.",
                                                    "We can't lose hope."],
                                       'frequent_options': ['we can', "we can't", 'used to', 'will be'],
                                       'frequent_answer': "we can't",
                                       'form_options': ["can't + 과거형",
                                                        "can't + to + 동사",
                                                        "can't + -ing 형태",
                                                        "can't + 동사"],
                                       'form_answer': "can't + 동사",
                                       'meaning_examples': [("Ain't nothing we can't do.", '우리가 하지 못할 일은 없어.'),
                                                            ("There's nothing we can't do.", '우리가 할 수 없는 것은 없어.'),
                                                            ("We can't give up.", '우리는 포기할 수 없어.')],
                                       'meaning_options': ['~할 수 없다', '~했었다', '~하고 있는 중이다', '~해야 한다'],
                                       'meaning_answer': '~할 수 없다',
                                       'rule_answer': "can't + 동사 = ~할 수 없다",
                                       'rule_options': ["can't + 과거형 = 어제 ~했다",
                                                        "can't + ing = ~하는 중이다",
                                                        "can't + to + 동사 = ~해야 한다",
                                                        "can't + 동사 = ~할 수 없다"],
                                       'practice': [("빈칸: There is nothing we can't _____.",
                                                     ['does', 'did', 'do', 'doing'],
                                                     'do',
                                                     "can't 뒤에는 동사입니다."),
                                                    ('맞는 문장은?',
                                                     ["We can't gives up.",
                                                      "We can't to give up.",
                                                      "We can't giving up.",
                                                      "We can't give up."],
                                                     "We can't give up.",
                                                     "can't + 동사"),
                                                    ("Ain't nothing we can't do.의 뜻은?",
                                                     ['우리는 아무것도 할 수 없어.',
                                                      '우리가 하지 못할 일은 없어.',
                                                      '우리는 어제 달에 갔어.',
                                                      '우리는 규칙을 따라야 해.'],
                                                     '우리가 하지 못할 일은 없어.',
                                                     "Ain't nothing we can't do는 매우 구어적인 표현으로, 할 수 없는 일이 없다는 뜻입니다."),
                                                    ("빈칸: We can't _____ hope.",
                                                     ['loses', 'lost', 'losing', 'lose'],
                                                     'lose',
                                                     "can't + 동사"),
                                                    ('알맞은 구조는?',
                                                     ["can't + 과거형",
                                                      "can't + 동사",
                                                      "can't + ing",
                                                      "can't + to + 동사"],
                                                     "can't + 동사",
                                                     '할 수 없다는 뜻을 나타냅니다.')],
                                       'sentence_prefix': "We can't",
                                       'sentence_choices': ['give up',
                                                            'lose hope',
                                                            'stop dreaming',
                                                            'forget our dream',
                                                            'stop trying'],
                                       'sentence_suffix': ''},
 '17. My Universe - Coldplay X BTS': {'target': 'want + 명사 / want to + 동사',
                                      'examples': ['I want love.',
                                                   'I want peace.',
                                                   'I want time.',
                                                   'I just want to put you first.',
                                                   'I want to help you.',
                                                   'I want to see you.'],
                                      'frequent_options': ['I can', 'You are', 'I want / I want to', 'Let it'],
                                      'frequent_answer': 'I want / I want to',
                                      'form_options': ['want + 명사 / want to + 동사',
                                                       'want to + 명사 / want + 동사',
                                                       'want + to + 명사 / want + to + 동사',
                                                       'want 뒤에는 항상 to를 쓴다'],
                                      'form_answer': 'want + 명사 / want to + 동사',
                                      'meaning_examples': [('I want love.', '나는 사랑을 원해.'),
                                                           ('I want peace.', '나는 평화를 원해.'),
                                                           ('I want time.', '나는 시간이 필요해.'),
                                                           ('I want to put you first.', '나는 너를 가장 먼저 생각하고 싶어.'),
                                                           ('I want to help you.', '나는 너를 돕고 싶어.')],
                                      'meaning_options': ['명사를 원할 때도 항상 to를 쓴다',
                                                          '동사가 올 때는 want to를 쓰고, 명사가 올 때는 want를 쓴다',
                                                          'want 뒤에는 항상 동사만 온다',
                                                          'want to 뒤에는 항상 명사만 온다'],
                                      'meaning_answer': '동사가 올 때는 want to를 쓰고, 명사가 올 때는 want를 쓴다',
                                      'rule_answer': 'want + 명사 = ~을 원하다 / want to + 동사 = ~하고 싶다',
                                      'rule_options': ['want + 명사 = ~하고 싶다 / want to + 동사 = ~을 원하다',
                                                       'want + 명사 = ~을 원하다 / want to + 동사 = ~하고 싶다',
                                                       'want + 동사 = ~하고 싶다 / want to + 명사 = ~을 원하다',
                                                       'want 뒤에는 명사와 동사 모두 항상 to를 쓴다'],
                                      'practice': [('다음 중 뒤에 명사가 온 문장은?',
                                                    ['I want to help you.', 'I want peace.', 'I want to see you.', 'I want to try again.'],
                                                    'I want peace.',
                                                    'peace는 명사입니다. 명사가 올 때는 want + 명사 형태을 씁니다.'),
                                                   ('다음 중 뒤에 동사가 온 문장은?',
                                                    ['I want love.', 'I want time.', 'I want to help you.', 'I want peace.'],
                                                    'I want to help you.',
                                                    'help는 동사입니다. 동사가 올 때는 want to + 동사 형태을 씁니다.'),
                                                   ('빈칸: I want _____ put you first.',
                                                    ['', 'to', 'for', 'at'],
                                                    'to',
                                                    'put은 동사입니다. 동사가 올 때는 want to를 씁니다.'),
                                                   ('빈칸: I want _____ peace.',
                                                    ['to', 'for', 'at', ''],
                                                    '',
                                                    'peace는 명사입니다. 명사가 올 때는 want 뒤에 바로 씁니다.'),
                                                   ('알맞은 규칙은?',
                                                    ['뒤에 명사가 오면 want to를 쓴다',
                                                     '뒤에 동사가 오면 want to를 쓴다',
                                                     'want 뒤에는 항상 to를 쓴다',
                                                     'want 뒤에는 항상 -ing를 쓴다'],
                                                    '뒤에 동사가 오면 want to를 쓴다',
                                                    'I want love. / I want to help you.를 비교하면 규칙을 찾을 수 있습니다.')],
                                      'sentence_prefix': 'I want to',
                                      'sentence_choices': ['put you first',
                                                           'help my friend',
                                                           'study English',
                                                           'see my family',
                                                           'try again'],
                                      'sentence_suffix': ''},
 '18. Golden - KPop Demon Hunters': {'target': 'gonna be + 형용사',
                                     'examples': ["We're gonna be golden.",
                                                  'Gonna be golden.',
                                                  "We're gonna be glowin'.",
                                                  "You're gonna be strong.",
                                                  "I'm gonna be brave."],
                                     'frequent_options': ['I used to', 'gonna be', 'I have been', 'let me'],
                                     'frequent_answer': 'gonna be',
                                     'form_options': ['gonna be + 과거형',
                                                      'gonna be + 형용사',
                                                      'gonna be + to + 동사',
                                                      'gonna be + can'],
                                     'form_answer': 'gonna be + 형용사',
                                     'meaning_examples': [("We're gonna be golden.", '우리는 빛나는 존재가 될 거야.'),
                                                          ("We're gonna be glowin'.", '우리는 빛나게 될 거야.'),
                                                          ("I'm gonna be brave.", '나는 용감해질 거야.')],
                                     'meaning_options': ['예전에 ~했다', '지금 숨어 있다', '앞으로 ~한 모습이 될 것이다', '~할 수 없다'],
                                     'meaning_answer': '앞으로 ~한 모습이 될 것이다',
                                     'rule_answer': 'gonna be + 형용사 = 앞으로 ~한 모습이 될 것이다',
                                     'rule_options': ['gonna be + 과거형 = 어제 ~했다',
                                                      'gonna be + 형용사 = 앞으로 ~한 모습이 될 것이다',
                                                      'gonna be + can = ~할 수 있다',
                                                      'gonna be + to + 동사 = ~해야 한다'],
                                     'practice': [("빈칸: We're gonna be _____.",
                                                   ['golden', 'gold', 'to golden', 'golds'],
                                                   'golden',
                                                   'gonna be 뒤에는 어떤 모습인지 나타내는 말을 쓸 수 있습니다.'),
                                                  ('맞는 문장은?',
                                                   ["We're gonna to be golden.",
                                                    "We're gonna be golden.",
                                                    "We're gonna being golden.",
                                                    "We're gonna golden."],
                                                   "We're gonna be golden.",
                                                   'gonna be + 형용사'),
                                                  ("Gonna be golden.의 뜻은?",
                                                   ['빛나는 존재가 될 거야.', '어제 빛났다.', '빛나지 못한다.', '숨어 있을 거야.'],
                                                   '빛나는 존재가 될 거야.',
                                                   'gonna be는 앞으로 어떤 모습이 될지 말할 때 씁니다.'),
                                                  ("빈칸: We're gonna be _____.",
                                                   ['glow', 'glowin', 'to glow', 'glows'],
                                                   'glowin',
                                                   "가사에서는 glowin'처럼 말하듯 짧게 표현했습니다."),
                                                  ('알맞은 규칙은?',
                                                   ['gonna be 뒤에는 항상 과거 표현만 온다',
                                                    'gonna be는 앞으로 어떤 모습이 될지 말한다',
                                                    'gonna be 뒤에는 항상 to를 쓴다',
                                                    'gonna be는 이유를 모른다는 뜻이다'],
                                                   'gonna be는 앞으로 어떤 모습이 될지 말한다',
                                                   "We're gonna be golden.을 보면 앞으로 빛나는 모습이 될 것이라는 뜻입니다.")],
                                     'sentence_prefix': "We're gonna be",
                                     'sentence_choices': ['golden', 'strong', 'brave', 'happy', 'ready'],
                                     'sentence_suffix': ''},
 '19. Cowboy in LA - LANY': {'target': "Let's + 동사",
                             'examples': ["Let's skip the club.",
                                          "Let's skip the crowd.",
                                          "Let's take it slow.",
                                          "Let's go on a date.",
                                          "Let's dance under the moon."],
                             'frequent_options': ['I can', "Let's", "I've been", 'used to'],
                             'frequent_answer': "Let's",
                             'form_options': ["Let's + 과거형", "Let's + to + 동사", "Let's + -ing 형태", "Let's + 동사"],
                             'form_answer': "Let's + 동사",
                             'meaning_examples': [("Let's skip the club.", '클럽은 건너뛰자.'),
                                                  ("Let's skip the crowd.", '사람 많은 곳은 피하자.'),
                                                  ("Let's take it slow.", '천천히 해 보자.')],
                             'meaning_options': ['혼자 할 수 없다고 말한다', '함께 ~하자고 제안한다', '예전에 하곤 했다고 말한다', '이미 끝난 일을 말한다'],
                             'meaning_answer': '함께 ~하자고 제안한다',
                             'rule_answer': "Let's + 동사 = 함께 ~하자",
                             'rule_options': ["Let's + 과거형 = 어제 ~했다",
                                              "Let's + to + 동사 = ~해야 한다",
                                              "Let's + ing = ~하고 있는 중이다",
                                              "Let's + 동사 = 함께 ~하자"],
                             'practice': [("빈칸: Let's _____ the club.",
                                           ['skips', 'skipped', 'skip', 'skipping'],
                                           'skip',
                                           "Let's 뒤에는 동사가 바로 옵니다."),
                                          ('맞는 문장은?',
                                           ["Let's to take it slow.",
                                            "Let's taking it slow.",
                                            "Let's takes it slow.",
                                            "Let's take it slow."],
                                           "Let's take it slow.",
                                           "Let's + 동사"),
                                          ("Let's skip the crowd.의 뜻은?",
                                           ['사람 많은 곳은 피하자.', '사람 많은 곳에 갔다.', '사람들이 춤을 춘다.', '나는 혼자 있고 싶다.'],
                                           '사람 많은 곳은 피하자.',
                                           "Let's는 함께 하자는 제안입니다."),
                                          ("빈칸: Let's _____ under the moon.",
                                           ['dances', 'danced', 'dancing', 'dance'],
                                           'dance',
                                           "Let's + 동사"),
                                          ('알맞은 구조는?',
                                           ["Let's + to + 동사", "Let's + 동사", "Let's + 과거형", "Let's + ing"],
                                           "Let's + 동사",
                                           '함께 하자고 제안할 때 씁니다.')],
                             'sentence_prefix': "Let's",
                             'sentence_choices': ['skip the crowd',
                                                  'take it slow',
                                                  'go on a date',
                                                  'dance under the moon',
                                                  'study English'],
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
            if check_key not in st.session_state:
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

    if st.session_state.get(f"mission_{grammar_key}_grammar"):
        show_mission_pdf_download(
            song_choice,
            "Grammar",
            f"{grammar_key}_grammar",
            f"Grammar 활동 완료 / Grammar Practice 점수: {score}/{len(questions)}"
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


SONGS = {'1. Let It Go - Frozen OST': {'video_url': 'https://www.youtube.com/watch?v=RgGRyssdJvw',
                               'bg': '\n'
                                     '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#be185d;">\n'
                                     '        ❄️ Let It Go: 숨겨 왔던 자신을 받아들이는 순간\n'
                                     '    </h3>\n'
                                     '\n'
                                     '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                     '        <b>Let It Go</b>는 영화 <i>Frozen</i>의 대표곡으로,\n'
                                     '        엘사가 더 이상 자신의 능력과 감정을 숨기지 않고\n'
                                     '        스스로를 받아들이는 장면에서 나오는 노래입니다.\n'
                                     '    </p>\n'
                                     '\n'
                                     '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                     '        엘사는 어릴 때부터 자신의 얼음 마법이 다른 사람을 다치게 할 수 있다는\n'
                                     '        두려움 속에서 살아왔습니다. 그래서 감정을 숨기고,\n'
                                     '        능력을 감추며, 언제나 조심해야 했습니다.\n'
                                     '        하지만 대관식 날 엘사의 능력이 사람들 앞에서 드러나고,\n'
                                     '        사람들은 엘사를 두려워합니다.\n'
                                     '    </p>\n'
                                     '\n'
                                     '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                     '        엘사는 모든 것을 피해 눈 덮인 산으로 도망치고,\n'
                                     '        그곳에서 처음으로 자신의 진짜 모습을 마주합니다.\n'
                                     '        이 노래는 단순히 “다 잊어버리자”는 의미가 아니라,\n'
                                     '        그동안 억눌렀던 두려움, 책임감, 타인의 시선에서 벗어나\n'
                                     '        자기 자신을 받아들이는 과정을 보여줍니다.\n'
                                     '    </p>\n'
                                     '\n'
                                     '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                     '        수업에서는 <b>let it go</b>, <b>conceal</b>, <b>hold back</b>,\n'
                                     "        <b>storm inside</b>, <b>I'm free</b>, <b>the past is in the past</b>\n"
                                     '        같은 표현을 중심으로 배울 수 있습니다.\n'
                                     '        특히 이 노래는 자유, 두려움, 자기표현, 자신감에 대해\n'
                                     '        함께 생각해 볼 수 있는 좋은 자료입니다.\n'
                                     '    </p>\n'
                                     '    ',
                               'lyrics': [('The snow glows white on the mountain tonight / Not a footprint to be seen',
                                           '오늘 밤 산 위에는 눈이 하얗게 빛나고 / 발자국 하나 보이지 않아요'),
                                          ("A kingdom of isolation / And it looks like I'm the queen",
                                           '고립된 왕국 / 그리고 내가 그곳의 여왕인 것 같아요'),
                                          ("The wind is howling like this swirling storm inside / Couldn't keep it in, "
                                           'heaven knows I tried',
                                           '바람은 내 안에서 휘몰아치는 폭풍처럼 울부짖고 / 더는 감출 수 없었어요, 하늘은 내가 얼마나 노력했는지 알 거예요'),
                                          ("Don't let them in, don't let them see / Be the good girl you always have "
                                           'to be',
                                           '그들을 들이지 마, 보여주지 마 / 언제나 그래야만 했던 착한 소녀가 되어라'),
                                          ("Conceal, don't feel, don't let them know / Well, now they know",
                                           '숨기고, 느끼지 말고, 그들이 알게 하지 마 / 하지만 이제 그들이 알아버렸어요'),
                                          ("Let it go, let it go / Can't hold it back anymore",
                                           '놓아버려, 놓아버려 / 더 이상 붙잡아 둘 수 없어'),
                                          ('Let it go, let it go / Turn away and slam the door',
                                           '놓아버려, 놓아버려 / 돌아서서 문을 세게 닫아버려'),
                                          ("I don't care what they're going to say / Let the storm rage on",
                                           '사람들이 뭐라고 하든 상관없어 / 폭풍이 계속 몰아치게 둬'),
                                          ('The cold never bothered me anyway', '어차피 추위는 나를 괴롭힌 적이 없으니까'),
                                          ("It's funny how some distance makes everything seem small / And the fears "
                                           "that once controlled me can't get to me at all",
                                           '거리를 두고 보니 모든 것이 작아 보이는 게 참 이상해 / 한때 나를 지배했던 두려움도 이제는 나에게 닿지 못해'),
                                          ("It's time to see what I can do / To test the limits and break through",
                                           '이제 내가 무엇을 할 수 있는지 볼 시간이야 / 한계를 시험하고 그것을 깨고 나아갈 시간이야'),
                                          ("No right, no wrong, no rules for me / I'm free",
                                           '옳고 그름도, 나를 묶는 규칙도 없어 / 나는 자유로워'),
                                          ('Let it go, let it go / I am one with the wind and sky',
                                           '놓아버려, 놓아버려 / 나는 바람과 하늘과 하나가 되었어'),
                                          ("Let it go, let it go / You'll never see me cry",
                                           '놓아버려, 놓아버려 / 너희는 다시는 내가 우는 모습을 보지 못할 거야'),
                                          ('Here I stand and here I stay / Let the storm rage on',
                                           '나는 여기 서 있고, 여기 머물 거야 / 폭풍이 계속 몰아치게 둬'),
                                          ('My power flurries through the air into the ground / My soul is spiraling '
                                           'in frozen fractals all around',
                                           '내 힘은 공기를 지나 땅속으로 흩날려 퍼지고 / 내 영혼은 사방의 얼어붙은 결정 속에서 소용돌이쳐'),
                                          ("And one thought crystallizes like an icy blast / I'm never going back, the "
                                           'past is in the past',
                                           '그리고 하나의 생각이 얼음바람처럼 선명하게 굳어져 / 나는 절대 돌아가지 않아, 과거는 과거일 뿐이야'),
                                          ("Let it go, let it go / And I'll rise like the break of dawn",
                                           '놓아버려, 놓아버려 / 나는 새벽이 밝아오듯 다시 일어설 거야'),
                                          ('Let it go, let it go / That perfect girl is gone',
                                           '놓아버려, 놓아버려 / 그 완벽한 소녀는 이제 없어'),
                                          ('Here I stand in the light of day / Let the storm rage on',
                                           '나는 밝은 낮의 빛 속에 서 있어 / 폭풍이 계속 몰아치게 둬'),
                                          ('The cold never bothered me anyway', '어차피 추위는 나를 괴롭힌 적이 없으니까')],
                               'quiz': [{'q': '1. 이 노래를 부르는 인물은 누구인가요?',
                                         'options': ['Anna', 'Olaf', 'Kristoff', 'Elsa'],
                                         'answer': 'Elsa'},
                                        {'q': '2. 엘사는 어디에서 이 노래를 부르나요?',
                                         'options': ['교실', '바닷가', '눈 덮인 산', '도시 거리'],
                                         'answer': '눈 덮인 산'},
                                        {'q': '3. 엘사가 더 이상 하지 않으려는 것은 무엇인가요?',
                                         'options': ['음식을 먹는 것', '학교에 가는 것', '동물과 이야기하는 것', '자신을 숨기는 것'],
                                         'answer': '자신을 숨기는 것'},
                                        {'q': '4. 이 노래의 중심 감정으로 가장 알맞은 것은 무엇인가요?',
                                         'options': ['배고픔', '지루함', '자유와 해방감', '질투'],
                                         'answer': '자유와 해방감'},
                                        {'q': "5. 'conceal'의 뜻으로 가장 알맞은 것은 무엇인가요?",
                                         'options': ['숨기다', '달리다', '노래하다', '웃다'],
                                         'answer': '숨기다'},
                                        {'q': "6. 'Can't hold it back anymore'는 어떤 의미에 가깝나요?",
                                         'options': ['더 이상 문을 열 수 없다',
                                                     '더 이상 노래할 수 없다',
                                                     '더 이상 걸을 수 없다',
                                                     '더 이상 억누를 수 없다'],
                                         'answer': '더 이상 억누를 수 없다'},
                                        {'q': "7. 'I'm free'에서 엘사가 느끼는 감정은 무엇인가요?",
                                         'options': ['두려움', '부끄러움', '자유로움', '배고픔'],
                                         'answer': '자유로움'},
                                        {'q': "8. 'the past is in the past'는 어떤 의미인가요?",
                                         'options': ['과거로 돌아가고 싶다', '과거는 과거일 뿐이다', '과거가 가장 중요하다', '과거를 다시 만들 수 있다'],
                                         'answer': '과거는 과거일 뿐이다'}],
                               'key_expressions': [('Let it go', '놓아버려'),
                                                   ("Can't hold it back anymore", '더 이상 억누를 수 없어'),
                                                   ("Conceal, don't feel", '숨기고, 느끼지 마'),
                                                   ('Let the storm rage on', '폭풍이 계속 몰아치게 둬'),
                                                   ("I'm free", '나는 자유로워'),
                                                   ('The past is in the past', '과거는 과거일 뿐이야'),
                                                   ('Here I stand', '나는 여기 서 있어'),
                                                   ('The cold never bothered me anyway', '어차피 추위는 나를 괴롭힌 적이 없어'),
                                                   ('Test the limits', '한계를 시험하다'),
                                                   ('Break through', '뚫고 나아가다')],
                               'matching': [('Let it go', '놓아버려'),
                                            ("Can't hold it back anymore", '더 이상 억누를 수 없어'),
                                            ("I'm free", '나는 자유로워'),
                                            ('The past is in the past', '과거는 과거일 뿐이야'),
                                            ('Here I stand', '나는 여기 서 있어'),
                                            ('The cold never bothered me anyway', '어차피 추위는 나를 괴롭힌 적이 없어')],
                               'reflect_questions': ['다른 사람의 시선 때문에 나 자신을 숨긴 적이 있나요?',
                                                     '내가 더 이상 붙잡고 싶지 않은 두려움이나 걱정은 무엇인가요?',
                                                     '이 노래처럼 “나는 자유로워”라고 말하고 싶은 순간은 언제인가요?']},
 '2. Hello - Adele': {'video_url': 'https://www.youtube.com/watch?v=h7NBamHcX58',
                      'bg': '\n'
                            '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#4338ca;">\n'
                            '        ☎️ Hello: 과거의 누군가에게 건네는 늦은 안부\n'
                            '    </h3>\n'
                            '\n'
                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                            '        Adele의 <b>Hello</b>는 시간이 많이 흐른 뒤, 과거의 누군가에게 다시 연락하고 싶은 마음을 담은 노래입니다.\n'
                            '        노래 속 화자는 상대에게 전화를 걸며 오래전의 관계, 미안함, 후회,\n'
                            '        그리고 아직 완전히 치유되지 않은 감정을 떠올립니다.\n'
                            '    </p>\n'
                            '\n'
                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                            '        이 노래에서 화자는 단순히 “안녕”이라고 말하는 것이 아니라,\n'
                            '        과거에 하지 못했던 사과를 전하고 싶어 합니다.\n'
                            '        하지만 두 사람 사이에는 시간의 거리, 마음의 거리, 그리고 실제 거리까지 생겨 있습니다.\n'
                            '        그래서 반복되는 <b>Hello</b>라는 말은 인사이면서 동시에 조심스러운 사과의 시작처럼 들립니다.\n'
                            '    </p>\n'
                            '\n'
                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                            "        수업에서는 <b>I'm sorry</b>, <b>I tried</b>, <b>after all these years</b>,\n"
                            '        <b>used to be</b>, <b>the other side</b> 같은 표현을 중심으로 배울 수 있습니다.\n'
                            '        특히 이 노래는 속도가 비교적 느리고 감정이 분명하게 드러나기 때문에,\n'
                            '        학생들이 가사를 읽으며 화자의 감정과 영어 표현을 함께 이해하기에 좋습니다.\n'
                            '    </p>\n'
                            '    ',
                      'lyrics': [("Hello, it's me / I was wondering if after all these years you'd like to meet, to go "
                                  'over everything',
                                  '안녕, 나야 / 이 모든 세월이 흐른 뒤에 네가 만나서 모든 일을 다시 이야기해 보고 싶어 할지 궁금했어'),
                                 ("They say that time's supposed to heal ya / But I ain't done much healing",
                                  '사람들은 시간이 너를 치유해 줄 거라고 말하지만 / 나는 별로 치유되지 않은 것 같아'),
                                 ("Hello, can you hear me? / I'm in California dreaming about who we used to be",
                                  '여보세요, 내 말 들리니? / 나는 캘리포니아에서 예전의 우리 모습을 떠올리고 있어'),
                                 ("When we were younger and free / I've forgotten how it felt before the world fell at "
                                  'our feet',
                                  '우리가 더 어리고 자유로웠을 때 / 세상이 우리 발아래 있는 것 같았던 그 느낌을 나는 잊어버렸어'),
                                 ("There's such a difference between us / And a million miles",
                                  '우리 사이에는 너무 큰 차이가 있어 / 그리고 백만 마일만큼의 거리도 있어'),
                                 ("Hello from the other side / I must've called a thousand times to tell you",
                                  '저편에서 안녕이라고 말해 / 너에게 말하려고 나는 아마 천 번은 전화했을 거야'),
                                 ("I'm sorry, for everything that I've done / But when I call you never seem to be "
                                  'home',
                                  '내가 했던 모든 일에 대해 미안해 / 하지만 내가 전화할 때 너는 늘 집에 없는 것 같아'),
                                 ("Hello from the outside / At least I can say that I've tried to tell you",
                                  '바깥쪽에서 안녕이라고 말해 / 적어도 나는 너에게 말하려고 노력했다고는 말할 수 있어'),
                                 ("I'm sorry, for breaking your heart / But it don't matter, it clearly doesn't tear "
                                  'you apart anymore',
                                  '네 마음을 아프게 해서 미안해 / 하지만 이제는 상관없는 것 같아, 더 이상 너를 아프게 하지 않는 것 같아'),
                                 ("Hello, how are you? / It's so typical of me to talk about myself",
                                  '안녕, 어떻게 지내? / 내 이야기만 하는 건 정말 나다운 일이야'),
                                 ("I'm sorry, I hope that you're well / Did you ever make it out of that town where "
                                  'nothing ever happened?',
                                  '미안해, 네가 잘 지내길 바라 / 아무 일도 일어나지 않던 그 마을에서 벗어났니?'),
                                 ("It's no secret that the both of us are running out of time",
                                  '우리 둘 다 시간이 얼마 남지 않았다는 건 비밀도 아니야'),
                                 ("Hello from the other side / I must've called a thousand times to tell you",
                                  '저편에서 안녕이라고 말해 / 너에게 말하려고 나는 아마 천 번은 전화했을 거야'),
                                 ("I'm sorry, for everything that I've done / But when I call you never seem to be "
                                  'home',
                                  '내가 했던 모든 일에 대해 미안해 / 하지만 내가 전화할 때 너는 늘 집에 없는 것 같아'),
                                 ("Hello from the outside / At least I can say that I've tried to tell you",
                                  '바깥쪽에서 안녕이라고 말해 / 적어도 나는 너에게 말하려고 노력했다고는 말할 수 있어'),
                                 ("I'm sorry, for breaking your heart / But it don't matter, it clearly doesn't tear "
                                  'you apart anymore',
                                  '네 마음을 아프게 해서 미안해 / 하지만 이제는 상관없는 것 같아, 더 이상 너를 아프게 하지 않는 것 같아'),
                                 ('Ooooohh, anymore / Ooooohh, anymore / Ooooohh, anymore / Anymore',
                                  '오, 더 이상 / 오, 더 이상 / 오, 더 이상 / 더 이상'),
                                 ("Hello from the other side / I must've called a thousand times to tell you",
                                  '저편에서 안녕이라고 말해 / 너에게 말하려고 나는 아마 천 번은 전화했을 거야'),
                                 ("I'm sorry, for everything that I've done / But when I call you never seem to be "
                                  'home',
                                  '내가 했던 모든 일에 대해 미안해 / 하지만 내가 전화할 때 너는 늘 집에 없는 것 같아'),
                                 ("Hello from the outside / At least I can say that I've tried to tell you",
                                  '바깥쪽에서 안녕이라고 말해 / 적어도 나는 너에게 말하려고 노력했다고는 말할 수 있어'),
                                 ("I'm sorry, for breaking your heart / But it don't matter, it clearly doesn't tear "
                                  'you apart anymore',
                                  '네 마음을 아프게 해서 미안해 / 하지만 이제는 상관없는 것 같아, 더 이상 너를 아프게 하지 않는 것 같아')],
                      'quiz': [{'q': '1. 이 노래에서 화자는 누구에게 연락하려고 하나요?',
                                'options': ['새로 만난 선생님', '유명한 가수', '캘리포니아의 낯선 사람', '과거에 알던 사람'],
                                'answer': '과거에 알던 사람'},
                               {'q': '2. 화자가 상대에게 가장 말하고 싶어 하는 것은 무엇인가요?',
                                'options': ['고맙다는 말', '미안하다는 말', '생일 축하한다는 말', '여행을 가자는 말'],
                                'answer': '미안하다는 말'},
                               {'q': '3. 노래에서 사람들은 시간이 무엇을 해 준다고 말하나요?',
                                'options': ['사람을 부자로 만들어 준다', '과거를 완전히 바꿔 준다', '상처를 치유해 준다', '슬픔을 바로 없애 준다'],
                                'answer': '상처를 치유해 준다'},
                               {'q': '4. 화자는 어디에서 예전의 자신들을 떠올리고 있나요?',
                                'options': ['런던', '캘리포니아', '뉴욕', '파리'],
                                'answer': '캘리포니아'},
                               {'q': "5. 'I must've called a thousand times'는 어떤 의미에 가깝나요?",
                                'options': ['정확히 천 번만 전화했다', '한 번도 전화하지 않았다', '전화번호를 잊어버렸다', '정말 여러 번 연락하려고 했다'],
                                'answer': '정말 여러 번 연락하려고 했다'},
                               {'q': "6. 'Hello from the other side'에서 'the other side'는 무엇을 상징한다고 볼 수 있나요?",
                                'options': ['학교의 반대편 교실', '가수가 사는 집', '멀어진 시간과 마음의 거리', '무대의 왼쪽'],
                                'answer': '멀어진 시간과 마음의 거리'},
                               {'q': "7. 화자가 'I tried'라고 말하는 이유는 무엇인가요?",
                                'options': ['노래 대회에 나가려고 했기 때문에',
                                            '캘리포니아로 여행을 가고 싶었기 때문에',
                                            '새로운 친구를 만들고 싶었기 때문에',
                                            '상대에게 사과하려고 노력했기 때문에'],
                                'answer': '상대에게 사과하려고 노력했기 때문에'},
                               {'q': '8. 이 노래의 중심 감정으로 가장 알맞은 것은 무엇인가요?',
                                'options': ['여행의 설렘', '후회와 사과', '복수심과 분노', '시험에 대한 걱정'],
                                'answer': '후회와 사과'}],
                      'key_expressions': [("Hello, it's me", '안녕, 나야'),
                                          ('After all these years', '이 모든 세월이 흐른 뒤에'),
                                          ("Time's supposed to heal you", '시간이 너를 치유해 줄 거라고 여겨진다'),
                                          ('Can you hear me?', '내 말 들리니?'),
                                          ('Who we used to be', '예전의 우리 모습'),
                                          ('Hello from the other side', '저편에서 전하는 안녕'),
                                          ("I must've called a thousand times", '정말 여러 번 전화했을 거야'),
                                          ("I'm sorry", '미안해'),
                                          ("At least I can say that I've tried", '적어도 노력했다고 말할 수 있어'),
                                          ("I hope that you're well", '네가 잘 지내길 바라')],
                      'matching': [("Hello, it's me", '안녕, 나야'),
                                   ("I'm sorry", '미안해'),
                                   ('I tried', '나는 노력했어'),
                                   ('Hello from the other side', '저편에서 안녕이라고 말해'),
                                   ('Can you hear me?', '내 말 들리니?'),
                                   ("I hope that you're well", '네가 잘 지내길 바라')],
                      'reflect_questions': ['오랫동안 연락하지 못했지만 다시 이야기하고 싶은 사람이 있나요?',
                                            '누군가에게 미안하다고 말하지 못했던 경험이 있나요?',
                                            '시간이 지나면서 치유된 감정이나 아직 남아 있는 감정이 있나요?']},
 '3. A Whole New World - Aladdin OST': {'video_url': 'https://www.youtube.com/watch?v=9FJssSUxI88',
                                        'bg': '\n'
                                              '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#4338ca;">\n'
                                              '        🕌 A Whole New World: 새로운 세상을 바라보는 순간\n'
                                              '    </h3>\n'
                                              '\n'
                                              '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                              '        <b>A Whole New World</b>는 영화 <i>Aladdin</i>의 대표곡으로,\n'
                                              '        알라딘과 자스민이 마법 양탄자를 타고 밤하늘을 날며\n'
                                              '        새로운 세상을 바라보는 장면에서 나오는 노래입니다.\n'
                                              '    </p>\n'
                                              '\n'
                                              '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                              '        자스민은 궁전 안에서 공주로 살아가지만,\n'
                                              '        정해진 규칙과 역할 속에서 자유롭게 세상을 경험하지 못합니다.\n'
                                              '        알라딘은 그런 자스민에게 궁전 밖의 넓은 세상을 보여 주고,\n'
                                              '        자스민은 처음으로 자신이 알지 못했던 새로운 풍경과 가능성을 마주하게 됩니다.\n'
                                              '    </p>\n'
                                              '\n'
                                              '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                              '        이 노래에서 <b>a whole new world</b>는 단순히 새로운 장소만을 뜻하지 않습니다.\n'
                                              '        새로운 시선, 새로운 경험, 그리고 스스로 선택할 수 있는 자유를 의미합니다.\n'
                                              '        두 사람은 마법 양탄자를 타고 하늘을 날며,\n'
                                              '        두려움보다 설렘이 더 큰 새로운 세계로 함께 나아갑니다.\n'
                                              '    </p>\n'
                                              '\n'
                                              '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                              '        수업에서는 <b>I can show you the world</b>, <b>open your eyes</b>,\n'
                                              '        <b>point of view</b>, <b>crystal clear</b>, <b>new '
                                              'horizons</b>\n'
                                              '        같은 표현을 중심으로 배울 수 있습니다.\n'
                                              '        특히 이 노래는 속도가 비교적 부드럽고 장면이 분명해서,\n'
                                              '        학생들이 영어 표현과 함께 설렘, 자유, 새로운 경험의 감정을 이해하기에 좋습니다.\n'
                                              '    </p>\n'
                                              '    ',
                                        'lyrics': [('I can show you the world / Shining, shimmering, splendid',
                                                    '내가 너에게 세상을 보여 줄 수 있어 / 빛나고, 반짝이고, 눈부신 세상을'),
                                                   ('Tell me, princess, now when did / You last let your heart decide?',
                                                    '말해 봐요, 공주님, 언제였나요 / 마지막으로 마음이 원하는 대로 선택했던 때가?'),
                                                   ('I can open your eyes / Take you wonder by wonder',
                                                    '내가 너의 눈을 뜨게 해 줄 수 있어 / 놀라움에서 또 다른 놀라움으로 데려가며'),
                                                   ('Over, sideways and under / On a magic carpet ride',
                                                    '위로, 옆으로, 아래로 날아가며 / 마법 양탄자를 타고'),
                                                   ('A whole new world / A new fantastic point of view',
                                                    '완전히 새로운 세상 / 새롭고 환상적인 시선'),
                                                   ('No one to tell us no / Or where to go',
                                                    '아무도 우리에게 안 된다고 말하지 않고 / 어디로 가라고 하지도 않아'),
                                                   ("Or say we're only dreaming", '우리가 그저 꿈꾸고 있을 뿐이라고 말하지도 않아'),
                                                   ('A whole new world / A dazzling place I never knew',
                                                    '완전히 새로운 세상 / 내가 전에는 알지 못했던 눈부신 곳'),
                                                   ("But when I'm way up here, it's crystal clear / That now I'm in a "
                                                    'whole new world with you',
                                                    '하지만 이렇게 높은 곳에 올라오니 모든 것이 분명해 / 지금 나는 너와 함께 완전히 새로운 세상에 있어'),
                                                   ("(Now I'm in a whole new world with you)",
                                                    '이제 나는 너와 함께 완전히 새로운 세상에 있어'),
                                                   ('Unbelievable sights / Indescribable feeling',
                                                    '믿기 어려운 풍경들 / 말로 표현할 수 없는 감정'),
                                                   ('Soaring, tumbling, freewheeling / Through an endless diamond sky',
                                                    '솟아오르고, 구르고, 자유롭게 날아가며 / 끝없이 펼쳐진 다이아몬드 같은 하늘을 지나'),
                                                   ("A whole new world / Don't you dare close your eyes",
                                                    '완전히 새로운 세상 / 절대 눈 감지 마'),
                                                   ('A hundred thousand things to see / Hold your breath, it gets '
                                                    'better',
                                                    '볼 것이 셀 수 없이 많아 / 숨을 참고 봐, 더 좋아질 거야'),
                                                   ("I'm like a shooting star, I've come so far / I can't go back to "
                                                    'where I used to be',
                                                    '나는 별똥별 같아, 정말 멀리까지 왔어 / 예전의 내가 있던 곳으로 돌아갈 수 없어'),
                                                   ('A whole new world / Every turn a surprise',
                                                    '완전히 새로운 세상 / 방향을 틀 때마다 놀라움이 있어'),
                                                   ('With new horizons to pursue / Every moment, red-letter',
                                                    '따라갈 새로운 지평선들이 있고 / 모든 순간이 특별해'),
                                                   ("I'll chase them anywhere, there's time to spare / Let me share "
                                                    'this whole new world with you',
                                                    '나는 어디든 그것들을 따라갈 거야, 시간은 충분해 / 이 완전히 새로운 세상을 너와 함께 나누게 해 줘'),
                                                   ('A whole new world / A whole new world', '완전히 새로운 세상 / 완전히 새로운 세상'),
                                                   ("That's where we'll be / That's where we'll be",
                                                    '그곳이 우리가 있을 곳이야 / 그곳이 우리가 있을 곳이야'),
                                                   ('A thrilling chase / A wondrous place', '짜릿한 모험 / 놀라운 곳'),
                                                   ('For you and me', '너와 나를 위한')],
                                        'quiz': [{'q': '1. 이 노래에서 두 사람은 무엇을 타고 있나요?',
                                                  'options': ['기차', '자전거', '배', '마법 양탄자'],
                                                  'answer': '마법 양탄자'},
                                                 {'q': '2. 이 노래에서 알라딘은 자스민에게 무엇을 보여 주고 싶어 하나요?',
                                                  'options': ['학교 교실', '시험 문제', '새로운 세상', '휴대전화'],
                                                  'answer': '새로운 세상'},
                                                 {'q': "3. 'A whole new world'가 상징하는 것으로 가장 알맞은 것은 무엇인가요?",
                                                  'options': ['낡은 방', '어려운 시험', '혼자 있는 시간', '새로운 시선과 경험'],
                                                  'answer': '새로운 시선과 경험'},
                                                 {'q': "4. 'I can open your eyes'는 어떤 의미에 가깝나요?",
                                                  'options': ['잠에서 깨우다', '눈을 감게 하다', '새로운 것을 보게 해 주다', '멀리 보내다'],
                                                  'answer': '새로운 것을 보게 해 주다'},
                                                 {'q': "5. 'point of view'의 뜻으로 가장 알맞은 것은 무엇인가요?",
                                                  'options': ['문', '속도', '약속', '관점'],
                                                  'answer': '관점'},
                                                 {'q': '6. 노래의 중심 감정으로 가장 알맞은 것은 무엇인가요?',
                                                  'options': ['후회와 슬픔', '분노와 복수', '설렘과 자유로움', '지루함'],
                                                  'answer': '설렘과 자유로움'},
                                                 {'q': "7. 'I can't go back to where I used to be'는 어떤 의미인가요?",
                                                  'options': ['집에 갈 길을 잃었다',
                                                              '예전의 모습으로 돌아갈 수 없다',
                                                              '학교에 다시 가야 한다',
                                                              '여행을 취소했다'],
                                                  'answer': '예전의 모습으로 돌아갈 수 없다'},
                                                 {'q': '8. 이 노래의 주요 배경으로 가장 알맞은 것은 무엇인가요?',
                                                  'options': ['교실에서 보는 시험',
                                                              '바닷가에서 하는 운동',
                                                              '시장 안의 장면',
                                                              '밤하늘을 나는 마법 양탄자 여행'],
                                                  'answer': '밤하늘을 나는 마법 양탄자 여행'}],
                                        'key_expressions': [('I can show you the world', '내가 너에게 세상을 보여 줄 수 있어'),
                                                            ('Shining, shimmering, splendid', '빛나고 반짝이고 눈부신'),
                                                            ('Let your heart decide', '마음이 결정하게 하다'),
                                                            ('Open your eyes', '눈을 뜨게 하다'),
                                                            ('A whole new world', '완전히 새로운 세상'),
                                                            ('Point of view', '관점'),
                                                            ('No one to tell us no', '아무도 안 된다고 말하지 않음'),
                                                            ('Unbelievable sights', '믿기 어려운 풍경들'),
                                                            ('Indescribable feeling', '말로 표현할 수 없는 감정'),
                                                            ('New horizons to pursue', '따라갈 새로운 지평선들')],
                                        'matching': [('I can show you the world', '내가 너에게 세상을 보여 줄 수 있어'),
                                                     ('A whole new world', '완전히 새로운 세상'),
                                                     ('A new fantastic point of view', '새롭고 환상적인 시선'),
                                                     ("Don't you dare close your eyes", '절대 눈 감지 마'),
                                                     ('Open your eyes', '눈을 떠 봐'),
                                                     ('Every turn a surprise', '방향을 틀 때마다 놀라움이 있어')],
                                        'reflect_questions': ['내가 경험해 보고 싶은 “완전히 새로운 세상”은 무엇인가요?',
                                                              '누군가가 나에게 새로운 관점을 보여 준 적이 있나요?',
                                                              '두려움보다 설렘이 더 컸던 경험이 있나요?']},
 '4. Stand By Me - Ben E. King': {'video_url': 'https://www.youtube.com/watch?v=c5hDjpi_HM0',
                                  'bg': '\n'
                                        '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#15803d;">\n'
                                        '        🤝 Stand By Me: 곁에 있어 주는 힘\n'
                                        '    </h3>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        <b>Stand By Me</b>는 어둡고 불안한 순간에도\n'
                                        '        누군가가 내 곁에 있어 준다면 두렵지 않다는 메시지를 담은 노래입니다.\n'
                                        '        제목의 <b>stand by me</b>는 단순히 “내 옆에 서 있어”라는 뜻을 넘어,\n'
                                        '        “내 곁에 있어 줘”, “나를 지켜 줘”, “함께해 줘”라는 의미로 이해할 수 있습니다.\n'
                                        '    </p>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        노래 속 화자는 밤이 찾아오고 세상이 어두워지는 장면을 떠올립니다.\n'
                                        '        하지만 그는 혼자가 아니라는 믿음 때문에 두려워하지 않습니다.\n'
                                        '        달빛만 보이는 어두운 상황, 하늘이 무너지고 산이 바다로 무너져 내리는 듯한\n'
                                        '        극단적인 상황에서도 사랑하는 사람이 곁에 있다면 괜찮다고 말합니다.\n'
                                        '    </p>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        이 노래는 어려운 단어가 많지 않고,\n'
                                        "        <b>I won't be afraid</b>, <b>I won't cry</b>, <b>stand by me</b>처럼\n"
                                        '        짧고 반복적인 표현이 많아 학생들이 듣고 따라 부르기에 좋습니다.\n'
                                        '        또한 친구, 가족, 사랑하는 사람의 존재가 주는 안정감과 용기를\n'
                                        '        자연스럽게 이야기해 볼 수 있는 노래입니다.\n'
                                        '    </p>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        "        수업에서는 <b>stand by me</b>, <b>I won't be afraid</b>,\n"
                                        "        <b>I won't cry</b>, <b>shed a tear</b>, <b>whenever you're in "
                                        'trouble</b>\n'
                                        '        같은 표현을 중심으로 배울 수 있습니다.\n'
                                        '        특히 이 노래는 느린 속도와 반복 구조 덕분에\n'
                                        '        기초 학습자도 영어 표현을 소리로 익히기에 적합합니다.\n'
                                        '    </p>\n'
                                        '    ',
                                  'lyrics': [('When the night has come / And the land is dark', '밤이 찾아오고 / 세상이 어두워질 때'),
                                             ("And the moon is the only light we'll see", '달빛만이 우리가 볼 수 있는 유일한 빛일 때'),
                                             ("No, I won't be afraid / Oh, I won't be afraid",
                                              '아니, 나는 두려워하지 않을 거야 / 오, 나는 두려워하지 않을 거야'),
                                             ('Just as long as you stand / Stand by me', '네가 곁에 있어 준다면 / 내 곁에 있어 준다면'),
                                             ("So darlin', darlin' / Stand by me, oh, stand by me",
                                              '그러니 사랑하는 사람아 / 내 곁에 있어 줘, 오, 내 곁에 있어 줘'),
                                             ('Oh, stand, stand by me / Stand by me', '오, 있어 줘, 내 곁에 있어 줘 / 내 곁에 있어 줘'),
                                             ('If the sky that we look upon / Should tumble and fall',
                                              '우리가 바라보는 하늘이 / 무너져 내린다 해도'),
                                             ('Or the mountain should crumble to the sea', '산이 부서져 바다로 무너져 내린다 해도'),
                                             ("I won't cry, I won't cry / No, I won't shed a tear",
                                              '나는 울지 않을 거야, 울지 않을 거야 / 아니, 눈물 한 방울도 흘리지 않을 거야'),
                                             ('Just as long as you stand / Stand by me', '네가 곁에 있어 준다면 / 내 곁에 있어 준다면'),
                                             ("And darlin', darlin' / Stand by me, oh, stand by me",
                                              '그리고 사랑하는 사람아 / 내 곁에 있어 줘, 오, 내 곁에 있어 줘'),
                                             ('Oh, stand now, stand by me / Stand by me',
                                              '오, 지금 곁에 있어 줘, 내 곁에 있어 줘 / 내 곁에 있어 줘'),
                                             ("Darlin', darlin' / Stand by me, oh, stand by me",
                                              '사랑하는 사람아, 사랑하는 사람아 / 내 곁에 있어 줘, 오, 내 곁에 있어 줘'),
                                             ('Oh, stand now, stand by me / Stand by me',
                                              '오, 지금 곁에 있어 줘, 내 곁에 있어 줘 / 내 곁에 있어 줘'),
                                             ("Whenever you're in trouble / Won't you stand by me?",
                                              '네가 힘든 순간에 / 내 곁에 있어 주지 않을래?'),
                                             ("Oh, stand by me / Won't you stand now?",
                                              '오, 내 곁에 있어 줘 / 지금 내 곁에 있어 주지 않을래?'),
                                             ('Oh, stand, stand by me', '오, 있어 줘, 내 곁에 있어 줘')],
                                  'quiz': [{'q': '1. 이 노래는 어떤 시간적 배경으로 시작하나요?',
                                            'options': ['아침', '밤', '점심시간', '학교 수업 시간'],
                                            'answer': '밤'},
                                           {'q': '2. 노래에서 보이는 유일한 빛은 무엇인가요?',
                                            'options': ['햇빛', '달빛', '휴대전화 불빛', '촛불'],
                                            'answer': '달빛'},
                                           {'q': '3. 화자는 두려움에 대해 무엇이라고 말하나요?',
                                            'options': ['나는 두려워하지 않을 거야', '나는 항상 두려워', '나는 두려움을 좋아해', '나는 학교가 두려워'],
                                            'answer': '나는 두려워하지 않을 거야'},
                                           {'q': "4. 'Stand by me'의 의미로 가장 알맞은 것은 무엇인가요?",
                                            'options': ['멀리 도망가', '앉아 있어', '집에 가', '내 곁에 있어 줘'],
                                            'answer': '내 곁에 있어 줘'},
                                           {'q': '5. 이 노래의 중심 주제로 가장 알맞은 것은 무엇인가요?',
                                            'options': ['쇼핑', '경쟁', '요리', '함께 있어 주는 힘과 위로'],
                                            'answer': '함께 있어 주는 힘과 위로'},
                                           {'q': '6. 화자가 두려워하지 않는 이유는 무엇인가요?',
                                            'options': ['돈이 많기 때문에', '날씨가 맑기 때문에', '누군가가 곁에 있어 주기 때문에', '잠을 자고 있기 때문에'],
                                            'answer': '누군가가 곁에 있어 주기 때문에'},
                                           {'q': "7. 'I won't shed a tear'의 의미로 가장 알맞은 것은 무엇인가요?",
                                            'options': ['눈물 한 방울도 흘리지 않겠다', '많이 웃겠다', '잠을 자겠다', '멀리 떠나겠다'],
                                            'answer': '눈물 한 방울도 흘리지 않겠다'},
                                           {'q': "8. 'Whenever you're in trouble'은 어떤 뜻인가요?",
                                            'options': ['네가 여행을 갈 때마다',
                                                        '네가 노래할 때마다',
                                                        '네가 힘든 순간에는 언제든지',
                                                        '네가 밥을 먹을 때마다'],
                                            'answer': '네가 힘든 순간에는 언제든지'}],
                                  'key_expressions': [('Stand by me', '내 곁에 있어 줘'),
                                                      ('The night has come', '밤이 찾아왔다'),
                                                      ('The land is dark', '세상이 어둡다'),
                                                      ('The only light', '유일한 빛'),
                                                      ("I won't be afraid", '나는 두려워하지 않을 거야'),
                                                      ('Just as long as', '~하는 한'),
                                                      ('Tumble and fall', '무너져 내리다'),
                                                      ('Crumble to the sea', '바다로 무너져 내리다'),
                                                      ("I won't shed a tear", '눈물 한 방울도 흘리지 않을 거야'),
                                                      ("Whenever you're in trouble", '네가 힘든 순간에는 언제든지')],
                                  'matching': [('Stand by me', '내 곁에 있어 줘'),
                                               ("I won't be afraid", '나는 두려워하지 않을 거야'),
                                               ("I won't cry", '나는 울지 않을 거야'),
                                               ("Whenever you're in trouble", '네가 힘든 순간에는 언제든지'),
                                               ('The land is dark', '세상이 어두워'),
                                               ('The moon is the only light', '달빛만이 유일한 빛이야')],
                                  'reflect_questions': ['내가 힘들 때 곁에 있어 주었던 사람은 누구인가요?',
                                                        '누군가에게 “내 곁에 있어 줘”라고 말하고 싶었던 순간이 있나요?',
                                                        '나도 누군가에게 힘이 되어 준 경험이 있나요?']},
 "5. Don't Know Why - Norah Jones": {'video_url': 'https://www.youtube.com/watch?v=nhLdJeLTM48',
                                     'bg': '\n'
                                           '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#7c3aed;">\n'
                                           "        🌙 Don't Know Why: 이유를 알 수 없는 마음\n"
                                           '    </h3>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           "        <b>Don't Know Why</b>는 Norah Jones의 대표곡으로,\n"
                                           '        조용하고 부드러운 멜로디 속에 설명하기 어려운 아쉬움과 후회를 담고 있는 노래입니다.\n'
                                           '        노래 속 화자는 누군가에게 가지 않았던 자신의 행동을 떠올리며,\n'
                                           '        왜 그렇게 했는지 스스로도 알 수 없다고 말합니다.\n'
                                           '    </p>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           '        이 노래는 큰 사건을 직접적으로 설명하기보다,\n'
                                           '        마음속에 남아 있는 감정의 흔적을 천천히 보여 줍니다.\n'
                                           '        해가 뜰 때까지 기다렸지만 결국 가지 못했고,\n'
                                           '        새벽이 밝아오는 순간에는 차라리 멀리 날아가 버리고 싶어 합니다.\n'
                                           '        그래서 이 노래에는 후회, 망설임, 외로움, 그리움이 조용하게 섞여 있습니다.\n'
                                           '    </p>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           "        특히 <b>I don't know why I didn't come</b>이라는 문장이 반복되면서,\n"
                                           '        화자가 자신의 마음을 명확히 설명하지 못하는 상태가 잘 드러납니다.\n'
                                           '        이 반복 표현은 학생들이 듣고 따라 말하기 좋고,\n'
                                           "        <b>I don't know why</b>, <b>I wished that I could</b>,\n"
                                           '        <b>on my mind</b>, <b>empty as a drum</b> 같은 표현을 배우기에도 좋습니다.\n'
                                           '    </p>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           '        수업에서는 이 노래를 통해 느린 영어 발음, 감정 표현,\n'
                                           '        후회와 그리움을 나타내는 문장을 함께 배울 수 있습니다.\n'
                                           '        속도가 빠르지 않고 분위기가 차분해서,\n'
                                           '        학생들이 영어 소리를 듣고 가사의 의미를 천천히 따라가기에 적합합니다.\n'
                                           '    </p>\n'
                                           '    ',
                                     'lyrics': [("I waited 'til I saw the sun / I don't know why I didn't come",
                                                 '나는 해가 보일 때까지 기다렸어 / 왜 내가 가지 않았는지 모르겠어'),
                                                ("I left you by the house of fun / Don't know why I didn't come",
                                                 '나는 너를 즐거움의 집 곁에 남겨 두었어 / 왜 내가 가지 않았는지 모르겠어'),
                                                ("Don't know why I didn't come", '왜 내가 가지 않았는지 모르겠어'),
                                                ('When I saw the break of day / I wished that I could fly away',
                                                 '새벽이 밝아오는 것을 보았을 때 / 나는 날아가 버릴 수 있기를 바랐어'),
                                                ('Instead of kneeling in the sand / Catching tear-drops in my hand',
                                                 '모래 위에 무릎 꿇고 있는 대신 / 손으로 눈물방울을 받으며'),
                                                ("My heart is drenched in wine / But you'll be on my mind forever",
                                                 '내 마음은 와인에 흠뻑 젖어 있지만 / 너는 영원히 내 마음속에 있을 거야'),
                                                ('Out across the endless sea / I would die in ecstasy',
                                                 '끝없는 바다 저편으로 / 나는 황홀함 속에서 죽을 수도 있을 것 같아'),
                                                ("But I'll be a bag of bones / Driving down the road alone",
                                                 '하지만 나는 뼈만 남은 사람처럼 / 혼자 길을 따라 운전하게 되겠지'),
                                                ("My heart is drenched in wine / But you'll be on my mind forever",
                                                 '내 마음은 와인에 흠뻑 젖어 있지만 / 너는 영원히 내 마음속에 있을 거야'),
                                                ("Something has to make you run / I don't know why I didn't come",
                                                 '무언가가 너를 떠나게 만들었겠지 / 왜 내가 가지 않았는지 모르겠어'),
                                                ("I feel as empty as a drum / I don't know why I didn't come",
                                                 '나는 북처럼 텅 빈 기분이야 / 왜 내가 가지 않았는지 모르겠어'),
                                                ("Don't know why I didn't come / I don't know why I didn't come",
                                                 '왜 내가 가지 않았는지 모르겠어 / 왜 내가 가지 않았는지 모르겠어')],
                                     'quiz': [{'q': '1. 화자는 무엇을 볼 때까지 기다렸나요?',
                                               'options': ['버스', '해', '선생님', '전화'],
                                               'answer': '해'},
                                              {'q': '2. 화자가 계속 모르겠다고 말하는 것은 무엇인가요?',
                                               'options': ['무엇을 먹을지', '학교가 어디인지', '왜 자신이 가지 않았는지', '어떻게 읽는지'],
                                               'answer': '왜 자신이 가지 않았는지'},
                                              {'q': "3. 'break of day'의 뜻으로 가장 알맞은 것은 무엇인가요?",
                                               'options': ['한밤중', '점심시간', '새벽', '겨울'],
                                               'answer': '새벽'},
                                              {'q': '4. 화자는 새벽을 보았을 때 무엇을 바랐나요?',
                                               'options': ['일찍 자는 것', '차를 사는 것', '수학을 공부하는 것', '날아가 버리는 것'],
                                               'answer': '날아가 버리는 것'},
                                              {'q': '5. 이 노래의 분위기로 가장 알맞은 것은 무엇인가요?',
                                               'options': ['조용하고 후회스러운 분위기',
                                                           '화나고 시끄러운 분위기',
                                                           '빠르고 웃긴 분위기',
                                                           '신나고 거친 분위기'],
                                               'answer': '조용하고 후회스러운 분위기'},
                                              {'q': "6. 'You'll be on my mind forever'는 어떤 의미인가요?",
                                               'options': ['너는 곧 잊혀질 거야',
                                                           '너는 영원히 내 마음속에 있을 거야',
                                                           '너는 나와 함께 여행할 거야',
                                                           '너는 노래를 부를 거야'],
                                               'answer': '너는 영원히 내 마음속에 있을 거야'},
                                              {'q': "7. 'I feel as empty as a drum'은 어떤 감정에 가깝나요?",
                                               'options': ['배부름', '자신감', '공허함', '분노'],
                                               'answer': '공허함'},
                                              {'q': '8. 이 노래에서 반복되는 핵심 문장은 무엇인가요?',
                                               'options': ['Stand by me',
                                                           'Let it go',
                                                           'A whole new world',
                                                           "I don't know why I didn't come"],
                                               'answer': "I don't know why I didn't come"}],
                                     'key_expressions': [("I don't know why", '나는 왜 그런지 모르겠어'),
                                                         ("I didn't come", '나는 가지 않았어'),
                                                         ('The break of day', '새벽'),
                                                         ('I wished that I could fly away', '나는 날아가 버릴 수 있기를 바랐어'),
                                                         ('Tear-drops', '눈물방울'),
                                                         ('On my mind', '마음속에 있는'),
                                                         ('Forever', '영원히'),
                                                         ('Endless sea', '끝없는 바다'),
                                                         ('Driving down the road alone', '혼자 길을 따라 운전하며'),
                                                         ('Empty as a drum', '북처럼 텅 빈')],
                                     'matching': [("I don't know why", '나는 왜 그런지 모르겠어'),
                                                  ('I wished that I could fly away', '나는 날아가 버릴 수 있기를 바랐어'),
                                                  ("You'll be on my mind forever", '너는 영원히 내 마음속에 있을 거야'),
                                                  ('I feel as empty as a drum', '나는 북처럼 텅 빈 기분이야'),
                                                  ('I waited till I saw the sun', '나는 해가 보일 때까지 기다렸어'),
                                                  ('Driving down the road alone', '혼자 길을 따라 운전하며')],
                                     'reflect_questions': ['왜 그랬는지 스스로도 잘 설명할 수 없는 선택을 한 적이 있나요?',
                                                           '마음속에 오래 남아 있는 사람이나 기억이 있나요?',
                                                           '후회가 남는 일을 지금 다시 바라본다면 어떤 생각이 드나요?']},
 '6. Fix You - Coldplay': {'video_url': 'https://www.youtube.com/watch?v=Z0IZ3MjGFEo',
                           'bg': '\n'
                                 '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#2563eb;">\n'
                                 '        💡 Fix You: 힘든 순간에 건네는 위로\n'
                                 '    </h3>\n'
                                 '\n'
                                 '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                 '        Coldplay의 <b>Fix You</b>는 실패, 상실, 지침, 슬픔을 겪는 사람에게\n'
                                 '        따뜻한 위로를 건네는 노래입니다. 노래 속 화자는 상대가 최선을 다했지만\n'
                                 '        원하는 결과를 얻지 못했을 때, 그리고 잃어버린 것을 되돌릴 수 없을 때의\n'
                                 '        아픔을 조용히 바라봅니다.\n'
                                 '    </p>\n'
                                 '\n'
                                 '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                 '        이 노래에서 반복되는 <b>Lights will guide you home</b>은\n'
                                 '        어두운 순간에도 길을 비춰 주는 희망을 상징합니다.\n'
                                 '        또한 <b>I will try to fix you</b>는 상대를 완벽하게 고쳐 주겠다는 뜻이라기보다,\n'
                                 '        힘든 시간을 혼자 견디지 않도록 곁에서 도와주고 싶다는 마음으로 이해할 수 있습니다.\n'
                                 '    </p>\n'
                                 '\n'
                                 '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                 "        수업에서는 <b>try your best</b>, <b>don't succeed</b>,\n"
                                 '        <b>what you want / what you need</b>, <b>stuck in reverse</b>,\n'
                                 '        <b>learn from my mistakes</b> 같은 표현을 중심으로 배울 수 있습니다.\n'
                                 '        특히 이 노래는 속도가 비교적 느리고 감정선이 분명해서,\n'
                                 '        학생들이 영어 표현과 함께 위로, 희망, 회복의 의미를 이해하기에 좋습니다.\n'
                                 '    </p>\n'
                                 '    ',
                           'lyrics': [("When you try your best, but you don't succeed / When you get what you want, "
                                       'but not what you need',
                                       '네가 최선을 다했지만 성공하지 못할 때 / 원하는 것을 얻었지만 정작 필요한 것은 얻지 못할 때'),
                                      ("When you feel so tired, but you can't sleep / Stuck in reverse",
                                       '너무 지쳤지만 잠들 수 없을 때 / 거꾸로 갇혀 있는 것처럼 느껴질 때'),
                                      ('And the tears come streaming down your face / When you lose something you '
                                       "can't replace",
                                       '눈물이 네 얼굴을 타고 흘러내릴 때 / 대신할 수 없는 무언가를 잃었을 때'),
                                      ('When you love someone, but it goes to waste / Could it be worse?',
                                       '누군가를 사랑했지만 그 마음이 헛되어 버렸을 때 / 이보다 더 나쁠 수 있을까?'),
                                      ('Lights will guide you home / And ignite your bones',
                                       '빛이 너를 집으로 인도할 거야 / 그리고 네 안의 힘을 다시 밝혀 줄 거야'),
                                      ('And I will try to fix you', '그리고 나는 너를 다시 일으켜 주려고 노력할 거야'),
                                      ("And high up above or down below / When you're too in love to let it go",
                                       '저 높은 곳에 있든 아주 낮은 곳에 있든 / 너무 사랑해서 놓아주기 어려울 때'),
                                      ("But if you never try, you'll never know / Just what you're worth",
                                       '하지만 시도하지 않으면 절대 알 수 없어 / 네가 얼마나 소중한 사람인지'),
                                      ('Lights will guide you home / And ignite your bones',
                                       '빛이 너를 집으로 인도할 거야 / 그리고 네 안의 힘을 다시 밝혀 줄 거야'),
                                      ('And I will try to fix you', '그리고 나는 너를 다시 일으켜 주려고 노력할 거야'),
                                      ('Tears stream down your face / When you lose something you cannot replace',
                                       '눈물이 네 얼굴을 타고 흘러내려 / 대신할 수 없는 무언가를 잃었을 때'),
                                      ('Tears stream down your face, and I / Tears stream down your face',
                                       '눈물이 네 얼굴을 타고 흘러내리고, 나는 / 눈물이 네 얼굴을 타고 흘러내려'),
                                      ('I promise you I will learn from my mistakes / Tears stream down your face, and '
                                       'I',
                                       '나는 내 실수에서 배우겠다고 약속할게 / 눈물이 네 얼굴을 타고 흘러내리고, 나는'),
                                      ('Lights will guide you home / And ignite your bones',
                                       '빛이 너를 집으로 인도할 거야 / 그리고 네 안의 힘을 다시 밝혀 줄 거야'),
                                      ('And I will try to fix you', '그리고 나는 너를 다시 일으켜 주려고 노력할 거야')],
                           'quiz': [{'q': '1. 이 노래에서 화자는 어떤 사람을 위로하고 있나요?',
                                     'options': ['시험을 준비하는 사람', '여행을 떠나는 사람', '힘들고 지친 사람', '운동을 시작한 사람'],
                                     'answer': '힘들고 지친 사람'},
                                    {'q': "2. 'When you try your best, but you don't succeed'의 의미로 가장 알맞은 것은 무엇인가요?",
                                     'options': ['최선을 다했지만 성공하지 못할 때',
                                                 '아무 노력도 하지 않았을 때',
                                                 '원하는 것을 모두 얻었을 때',
                                                 '잠을 충분히 잤을 때'],
                                     'answer': '최선을 다했지만 성공하지 못할 때'},
                                    {'q': "3. 'what you want'와 'what you need'의 차이로 알맞은 것은 무엇인가요?",
                                     'options': ['둘 다 항상 같은 뜻이다',
                                                 'want는 원하는 것, need는 정말 필요한 것이다',
                                                 'want는 먹는 것, need는 노래하는 것이다',
                                                 'need는 필요 없는 것이다'],
                                     'answer': 'want는 원하는 것, need는 정말 필요한 것이다'},
                                    {'q': "4. 'Lights will guide you home'은 무엇을 상징한다고 볼 수 있나요?",
                                     'options': ['휴대전화 불빛', '가게의 간판', '어두운 길에서의 희망과 방향', '자동차 헤드라이트만'],
                                     'answer': '어두운 길에서의 희망과 방향'},
                                    {'q': "5. 'If you never try, you'll never know'의 의미로 가장 알맞은 것은 무엇인가요?",
                                     'options': ['절대 시도하면 안 된다', '시도하지 않으면 알 수 없다', '모든 것을 이미 알고 있다', '실패하면 끝이다'],
                                     'answer': '시도하지 않으면 알 수 없다'},
                                    {'q': "6. 'I will learn from my mistakes'는 어떤 태도를 보여 주나요?",
                                     'options': ['실수를 숨기려는 태도', '남을 탓하려는 태도', '포기하려는 태도', '실수에서 배우려는 태도'],
                                     'answer': '실수에서 배우려는 태도'},
                                    {'q': '7. 이 노래의 중심 감정으로 가장 알맞은 것은 무엇인가요?',
                                     'options': ['위로와 희망', '웃음과 장난', '분노와 복수', '경쟁과 승리'],
                                     'answer': '위로와 희망'},
                                    {'q': "8. 'I will try to fix you'는 어떤 의미에 가깝나요?",
                                     'options': ['너를 혼내겠다', '너를 완전히 바꾸겠다', '너를 떠나겠다', '너를 도와 다시 일어서게 하고 싶다'],
                                     'answer': '너를 도와 다시 일어서게 하고 싶다'}],
                           'key_expressions': [('Try your best', '최선을 다하다'),
                                               ("Don't succeed", '성공하지 못하다'),
                                               ('What you want', '네가 원하는 것'),
                                               ('What you need', '네게 필요한 것'),
                                               ('Stuck in reverse', '거꾸로 갇힌 듯한'),
                                               ('Tears stream down your face', '눈물이 얼굴을 타고 흐르다'),
                                               ("You can't replace", '대신할 수 없다'),
                                               ('Lights will guide you home', '빛이 너를 집으로 인도할 거야'),
                                               ('Ignite your bones', '네 안의 힘을 다시 밝혀 주다'),
                                               ('Learn from my mistakes', '내 실수에서 배우다')],
                           'matching': [('When you try your best', '네가 최선을 다할 때'),
                                        ('Lights will guide you home', '빛이 너를 집으로 인도할 거야'),
                                        ('I will try to fix you', '나는 너를 다시 일으켜 주려고 노력할 거야'),
                                        ("If you never try, you'll never know", '시도하지 않으면 절대 알 수 없어'),
                                        ('Tears stream down your face', '눈물이 네 얼굴을 타고 흘러내려'),
                                        ('I will learn from my mistakes', '나는 내 실수에서 배울 거야')],
                           'reflect_questions': ['최선을 다했지만 원하는 결과를 얻지 못했던 경험이 있나요?',
                                                 '힘들 때 나를 다시 일으켜 준 사람이나 말이 있었나요?',
                                                 '나도 누군가를 위로하거나 도와주고 싶었던 적이 있나요?']},
 '7. The Scientist - Coldplay': {'video_url': 'https://www.youtube.com/watch?v=kV82ahVRPFg&list=RDkV82ahVRPFg&start_radio=1',
                                 'bg': '<h3 style="font-size:2.2rem; margin-bottom:20px; color:#2563eb;">🔬 The '
                                       'Scientist: 처음으로 돌아가고 싶은 마음</h3>\n'
                                       '<p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">Coldplay의 <b>The '
                                       'Scientist</b>는 지나간 관계와 후회를 돌아보며, 처음으로 돌아가 다시 말하고 싶은 마음을 담은 노래입니다.</p>\n'
                                       '<p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">노래 속 화자는 사랑과 이별을 '
                                       '과학처럼 분석하려 하지만, 마음은 숫자와 공식처럼 쉽게 설명되지 않는다는 것을 깨닫습니다.</p>',
                                 'lyrics': [('Come up to meet you, tell you I′m sorry', '너를 만나러 와서 미안하다고 말하려 해'),
                                            ("You don't know how lovely you are", '너는 네가 얼마나 사랑스러운지 몰라'),
                                            ('I had to find you, tell you I need you', '나는 너를 찾아야 했고, 네가 필요하다고 말해야 했어'),
                                            ('Tell you I set you apart', '네가 나에게 특별하다고 말해야 했어'),
                                            ('Tell me your secrets and ask me your questions',
                                             '네 비밀을 말해 주고, 내게 질문을 해 줘'),
                                            ('Oh, let′s go back to the start', '오, 처음으로 돌아가자'),
                                            ("Runnin' in circles, comin' up tails", '빙빙 돌며, 계속 좋지 않은 결과가 나오고 있어'),
                                            ('Heads on a science apart', '머리는 과학처럼 따로 떨어져 있어'),
                                            ('Nobody said it was easy', '아무도 그것이 쉽다고 말하지 않았어'),
                                            ('It′s such a shame for us to part', '우리가 헤어진다는 건 정말 안타까운 일이야'),
                                            ('Nobody said it was easy', '아무도 그것이 쉽다고 말하지 않았어'),
                                            ('No one ever said it would be this hard', '아무도 이렇게 힘들 거라고 말하지 않았어'),
                                            ('Oh, take me back to the start', '오, 나를 처음으로 데려가 줘'),
                                            ('I was just guessing at numbers and figures', '나는 그저 숫자와 수치를 추측하고 있었어'),
                                            ('Pulling the puzzles apart', '퍼즐을 하나하나 떼어 내며'),
                                            ('Questions of science, science and progress', '과학의 질문들, 과학과 진보는'),
                                            ('Do not speak as loud as my heart', '내 마음만큼 크게 말하지 못해'),
                                            ('But tell me you love me, come back and haunt me',
                                             '하지만 나를 사랑한다고 말해 줘, 돌아와 나를 계속 맴돌아 줘'),
                                            ('Oh, and I rush to the start', '오, 나는 서둘러 처음으로 돌아가'),
                                            ("Runnin′ in circles, chasin' our tails", '빙빙 돌며, 우리의 꼬리를 쫓듯 같은 자리를 맴돌아'),
                                            ('Coming back as we are', '있는 그대로의 우리로 돌아오며'),
                                            ('Nobody said it was easy', '아무도 그것이 쉽다고 말하지 않았어'),
                                            ('Oh, it′s such a shame for us to part', '오, 우리가 헤어진다는 건 정말 안타까운 일이야'),
                                            ('Nobody said it was easy', '아무도 그것이 쉽다고 말하지 않았어'),
                                            ('No one ever said it would be so hard', '아무도 이렇게 힘들 거라고 말하지 않았어'),
                                            ("I'm going back to the start", '나는 처음으로 돌아가고 있어')],
                                 'quiz': [{'q': '1. 화자가 상대에게 가장 먼저 말하고 싶은 것은 무엇인가요?',
                                           'options': ['미안하다는 말', '축하한다는 말', '화났다는 말', '떠나자는 말'],
                                           'answer': '미안하다는 말'},
                                          {'q': "2. “You don't know how lovely you are”의 의미는 무엇인가요?",
                                           'options': ['너는 네가 얼마나 사랑스러운지 모른다',
                                                       '너는 나를 전혀 모른다',
                                                       '너는 과학을 좋아한다',
                                                       '너는 돌아오지 않는다'],
                                           'answer': '너는 네가 얼마나 사랑스러운지 모른다'},
                                          {'q': "3. “Let's go back to the start”의 의미는 무엇인가요?",
                                           'options': ['처음으로 돌아가자', '학교로 가자', '과학을 공부하자', '집에 가자'],
                                           'answer': '처음으로 돌아가자'},
                                          {'q': '4. “Running in circles”는 어떤 상태를 나타내나요?',
                                           'options': ['같은 자리를 맴도는 상태', '빠르게 성공하는 상태', '잠을 자는 상태', '완전히 잊은 상태'],
                                           'answer': '같은 자리를 맴도는 상태'},
                                          {'q': '5. “Nobody said it was easy”의 의미는 무엇인가요?',
                                           'options': ['아무도 쉽다고 말하지 않았다', '모두 쉽다고 말했다', '과학은 쉽다', '사랑은 항상 쉽다'],
                                           'answer': '아무도 쉽다고 말하지 않았다'},
                                          {'q': '6. “Do not speak as loud as my heart”는 어떤 뜻에 가깝나요?',
                                           'options': ['이성과 과학보다 마음의 소리가 더 크다',
                                                       '심장이 실제로 소리를 낸다',
                                                       '과학이 가장 중요하다',
                                                       '말을 하지 말라는 뜻이다'],
                                           'answer': '이성과 과학보다 마음의 소리가 더 크다'},
                                          {'q': '7. 화자가 반복해서 돌아가고 싶어 하는 곳은 어디인가요?',
                                           'options': ['처음', '학교', '바다', '무대'],
                                           'answer': '처음'},
                                          {'q': '8. 이 노래의 중심 감정은 무엇인가요?',
                                           'options': ['후회와 그리움', '분노와 복수', '승리와 환호', '웃음과 장난'],
                                           'answer': '후회와 그리움'}],
                                 'key_expressions': [("Tell you I'm sorry", '미안하다고 말하다'),
                                                     ('How lovely you are', '네가 얼마나 사랑스러운지'),
                                                     ('I had to find you', '나는 너를 찾아야 했어'),
                                                     ('I need you', '네가 필요해'),
                                                     ('I set you apart', '나는 너를 특별하게 여겨'),
                                                     ('Tell me your secrets', '네 비밀을 말해 줘'),
                                                     ("Let's go back to the start", '처음으로 돌아가자'),
                                                     ('Running in circles', '빙빙 돌다'),
                                                     ('Nobody said it was easy', '아무도 그것이 쉽다고 말하지 않았어'),
                                                     ('Take me back to the start', '나를 처음으로 데려가 줘')],
                                 'matching': [("Tell you I'm sorry", '미안하다고 말하다'),
                                              ("You don't know how lovely you are", '너는 네가 얼마나 사랑스러운지 몰라'),
                                              ('Tell you I need you', '네가 필요하다고 말하다'),
                                              ("Let's go back to the start", '처음으로 돌아가자'),
                                              ('Nobody said it was easy', '아무도 그것이 쉽다고 말하지 않았어'),
                                              ("I'm going back to the start", '나는 처음으로 돌아가고 있어')],
                                 'reflect_questions': ['당신도 가수처럼 그리운 옛 연인이나 다시 이야기하고 싶은 사람이 있나요?',
                                                       '처음으로 돌아갈 수 있다면 다시 말하고 싶은 말은 무엇인가요?',
                                                       '사랑이나 관계가 생각보다 쉽지 않았다고 느낀 경험이 있나요?']},
 '8. My Heart Will Go On - Celine Dion': {'video_url': 'https://www.youtube.com/watch?v=qHtcHxx6UfQ&list=RDqHtcHxx6UfQ&start_radio=1',
                                          'bg': '\n'
                                                '    <h3 style="font-size:2.2rem; margin-bottom:20px; '
                                                'color:#0f766e;">\n'
                                                '        🚢 My Heart Will Go On: 마음속에 계속 살아 있는 사랑\n'
                                                '    </h3>\n'
                                                '\n'
                                                '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                                '        Celine Dion의 <b>My Heart Will Go On</b>은 영화 <i>Titanic</i>의 '
                                                '대표곡으로,\n'
                                                '        사랑하는 사람이 멀리 있거나 더 이상 곁에 없더라도\n'
                                                '        그 사랑과 기억은 마음속에서 계속 이어진다는 메시지를 담은 노래입니다.\n'
                                                '    </p>\n'
                                                '\n'
                                                '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                                '        노래 속 화자는 매일 밤 꿈속에서 사랑하는 사람을 보고 느낍니다.\n'
                                                '        두 사람 사이에는 먼 거리와 공간이 있지만,\n'
                                                '        그 사람은 여전히 마음속에 살아 있고 사랑은 계속된다고 믿습니다.\n'
                                                '    </p>\n'
                                                '\n'
                                                '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                                '        반복되는 <b>my heart will go on</b>은 단순히 심장이 계속 뛴다는 뜻이 아니라,\n'
                                                '        사랑과 기억이 사라지지 않고 계속 이어진다는 의미로 이해할 수 있습니다.\n'
                                                '        상실과 그리움 속에서도 사랑했던 기억은 한 사람의 마음속에 안전하게 남아 있습니다.\n'
                                                '    </p>\n'
                                                '\n'
                                                '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                                '        수업에서는 <b>in my dreams</b>, <b>wherever you are</b>,\n'
                                                '        <b>the heart does go on</b>, <b>open the door</b>, <b>safe in '
                                                'my heart</b>\n'
                                                '        같은 표현을 중심으로 배울 수 있습니다.\n'
                                                '        특히 이 노래는 느린 속도와 반복되는 표현이 많아,\n'
                                                '        학생들이 사랑, 기억, 그리움, 위로의 감정을 영어로 이해하기에 좋습니다.\n'
                                                '    </p>\n'
                                                '    ',
                                          'lyrics': [('Every night in my dreams / I see you, I feel you',
                                                      '매일 밤 꿈속에서 / 나는 너를 보고, 너를 느껴'),
                                                     ('That is how I know you go on', '그래서 나는 네가 계속 존재한다는 것을 알아'),
                                                     ('Far across the distance / And spaces between us',
                                                      '우리 사이의 먼 거리와 / 공간을 넘어'),
                                                     ('You have come to show you go on', '너는 네가 계속 존재한다는 것을 보여 주러 왔어'),
                                                     ('Near, far, wherever you are', '가까이 있든, 멀리 있든, 네가 어디에 있든'),
                                                     ('I believe that the heart does go on', '나는 마음이 계속 이어진다고 믿어'),
                                                     ("Once more, you open the door / And you're here in my heart",
                                                      '다시 한 번, 너는 문을 열고 / 내 마음속에 있어'),
                                                     ('And my heart will go on and on', '그리고 내 마음은 계속 이어질 거야'),
                                                     ('Love can touch us one time / And last for a lifetime',
                                                      '사랑은 한 번 우리에게 닿아 / 평생 지속될 수 있어'),
                                                     ("And never let go 'til we're gone", '그리고 우리가 사라질 때까지 절대 놓지 않아'),
                                                     ("Love was when I loved you / One true time I'd hold to",
                                                      '사랑은 내가 너를 사랑했던 그때였어 / 내가 붙잡고 싶은 단 하나의 진실한 순간'),
                                                     ("In my life, we'll always go on", '내 삶 속에서 우리는 언제나 계속 이어질 거야'),
                                                     ('Near, far, wherever you are', '가까이 있든, 멀리 있든, 네가 어디에 있든'),
                                                     ('I believe that the heart does go on (why does the heart go on?)',
                                                      '나는 마음이 계속 이어진다고 믿어 / 왜 마음은 계속 이어질까?'),
                                                     ("Once more, you open the door / And you're here in my heart",
                                                      '다시 한 번, 너는 문을 열고 / 내 마음속에 있어'),
                                                     ('And my heart will go on and on', '그리고 내 마음은 계속 이어질 거야'),
                                                     ("You're here, there's nothing I fear", '네가 여기 있으니, 나는 두려운 것이 없어'),
                                                     ('And I know that my heart will go on',
                                                      '그리고 나는 내 마음이 계속 이어질 것을 알아'),
                                                     ("We'll stay forever this way", '우리는 영원히 이렇게 머물 거야'),
                                                     ('You are safe in my heart and / My heart will go on and on',
                                                      '너는 내 마음속에 안전하게 있고 / 내 마음은 계속 이어질 거야')],
                                          'quiz': [{'q': '1. 이 노래에서 화자는 매일 밤 어디에서 사랑하는 사람을 보나요?',
                                                    'options': ['학교에서', '꿈속에서', '바닷가에서', '기차 안에서'],
                                                    'answer': '꿈속에서'},
                                                   {'q': '2. 화자는 사랑하는 사람이 어디에 있다고 느끼나요?',
                                                    'options': ['내 마음속에', '교실 뒤에', '먼 도시의 가게에', '배 위의 식당에'],
                                                    'answer': '내 마음속에'},
                                                   {'q': "3. 'Near, far, wherever you are'의 의미로 가장 알맞은 것은 무엇인가요?",
                                                    'options': ['가까이 있든 멀리 있든 네가 어디에 있든',
                                                                '항상 가까이에만 있어야 한다',
                                                                '멀리 가면 잊어야 한다',
                                                                '길을 잃었다'],
                                                    'answer': '가까이 있든 멀리 있든 네가 어디에 있든'},
                                                   {'q': "4. 'My heart will go on'은 어떤 의미에 가깝나요?",
                                                    'options': ['내 마음과 사랑은 계속 이어질 것이다',
                                                                '나는 빨리 달릴 것이다',
                                                                '나는 문을 닫을 것이다',
                                                                '나는 노래를 멈출 것이다'],
                                                    'answer': '내 마음과 사랑은 계속 이어질 것이다'},
                                                   {'q': '5. 이 노래의 중심 감정으로 가장 알맞은 것은 무엇인가요?',
                                                    'options': ['그리움과 영원한 사랑', '분노와 복수', '시험에 대한 걱정', '승리의 기쁨'],
                                                    'answer': '그리움과 영원한 사랑'},
                                                   {'q': "6. 'Love can touch us one time and last for a lifetime'의 의미는 "
                                                         '무엇인가요?',
                                                    'options': ['사랑은 한 번 닿아도 평생 남을 수 있다',
                                                                '사랑은 항상 바로 사라진다',
                                                                '사랑은 한 번도 중요하지 않다',
                                                                '사랑은 시험 점수와 같다'],
                                                    'answer': '사랑은 한 번 닿아도 평생 남을 수 있다'},
                                                   {'q': "7. 'There’s nothing I fear'는 어떤 의미인가요?",
                                                    'options': ['나는 두려운 것이 없다',
                                                                '나는 모든 것이 무섭다',
                                                                '나는 아무것도 보지 못한다',
                                                                '나는 노래를 싫어한다'],
                                                    'answer': '나는 두려운 것이 없다'},
                                                   {'q': '8. 이 노래가 전하려는 메시지로 가장 알맞은 것은 무엇인가요?',
                                                    'options': ['사랑과 기억은 마음속에서 계속 이어질 수 있다',
                                                                '사람은 절대 꿈을 꾸지 않는다',
                                                                '멀리 있으면 모든 감정은 사라진다',
                                                                '사랑은 항상 쉬운 일이다'],
                                                    'answer': '사랑과 기억은 마음속에서 계속 이어질 수 있다'}],
                                          'key_expressions': [('In my dreams', '내 꿈속에서'),
                                                              ('I see you, I feel you', '나는 너를 보고, 너를 느껴'),
                                                              ('You go on', '너는 계속 존재해'),
                                                              ('Far across the distance', '먼 거리를 넘어'),
                                                              ('Spaces between us', '우리 사이의 공간'),
                                                              ('Wherever you are', '네가 어디에 있든'),
                                                              ('The heart does go on', '마음은 계속 이어진다'),
                                                              ('Open the door', '문을 열다'),
                                                              ('Here in my heart', '내 마음속 여기에'),
                                                              ('Safe in my heart', '내 마음속에 안전하게')],
                                          'matching': [('In my dreams', '내 꿈속에서'),
                                                       ('I see you, I feel you', '나는 너를 보고, 너를 느껴'),
                                                       ('Wherever you are', '네가 어디에 있든'),
                                                       ('The heart does go on', '마음은 계속 이어진다'),
                                                       ('You are safe in my heart', '너는 내 마음속에 안전하게 있어'),
                                                       ('My heart will go on and on', '내 마음은 계속 이어질 거야')],
                                          'reflect_questions': ['멀리 떨어져 있어도 마음속에 남아 있는 사람이 있나요?',
                                                                '나에게 오래도록 기억에 남는 사랑이나 우정은 무엇인가요?',
                                                                '힘든 이별이나 그리움을 겪었을 때 나를 위로해 준 기억이 있나요?']},
 '9. Alex Sampson - Play Pretend': {'video_url': 'https://www.youtube.com/watch?v=9xbbSiWyiQY&list=RD9xbbSiWyiQY&start_radio=1',
                                    'bg': '\n'
                                          '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#db2777;">\n'
                                          '        🎭 Play Pretend: 좋아하지만 숨겨야 하는 마음\n'
                                          '    </h3>\n'
                                          '\n'
                                          '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                          '        Alex Sampson의 <b>Play Pretend</b>는 가까운 사람을 좋아하지만,\n'
                                          '        그 마음을 쉽게 드러내지 못하고 친구처럼 아무렇지 않은 척해야 하는 상황을 담은 노래입니다.\n'
                                          '        제목의 <b>play pretend</b>는 “괜찮은 척하다”, “아무렇지 않은 척하다”라는 의미로 이해할 수 '
                                          '있습니다.\n'
                                          '    </p>\n'
                                          '\n'
                                          '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                          '        노래 속 화자는 상대를 특별한 사람이라고 생각하고,\n'
                                          '        상대가 자신이 얼마나 소중한 사람인지 알았으면 좋겠다고 말합니다.\n'
                                          '        하지만 상대가 또다시 상처받는 모습을 보면서도 자신의 마음을 솔직하게 말하지 못하고,\n'
                                          '        그저 괜찮은 척해야 하는 아픔을 느낍니다.\n'
                                          '    </p>\n'
                                          '\n'
                                          '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                          '        이 노래에는 좋아하는 사람의 행복을 바라면서도,\n'
                                          '        동시에 그 사람을 향한 자신의 마음 때문에 힘들어하는 복잡한 감정이 담겨 있습니다.\n'
                                          "        특히 <b>I want you to be happy</b>와 <b>it's hard to watch you fall "
                                          'again</b>은\n'
                                          '        상대를 걱정하는 마음과 자신의 아픔이 함께 드러나는 표현입니다.\n'
                                          '    </p>\n'
                                          '\n'
                                          '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                          '        수업에서는 <b>someone special</b>, <b>settle</b>, <b>break the '
                                          'rules</b>,\n'
                                          '        <b>take this the wrong way</b>, <b>play pretend</b>, <b>fine '
                                          'line</b>,\n'
                                          '        <b>like the back of my hand</b> 같은 표현을 중심으로 배울 수 있습니다.\n'
                                          '        특히 이 노래는 짝사랑, 우정, 걱정, 솔직하지 못한 마음을 주제로 생각을 적기에 좋습니다.\n'
                                          '    </p>\n'
                                          '    ',
                                    'lyrics': [("Let me tell you 'bout someone special / She's kinda perfect and I "
                                                'wish she knew',
                                                '내가 특별한 사람에 대해 말해 줄게 / 그녀는 거의 완벽하고, 그녀가 그걸 알았으면 좋겠어'),
                                               ("Told me that she thinks she has to settle / But I know that ain't "
                                                'true',
                                                '그녀는 자신이 적당히 만족해야 한다고 생각한다고 말했어 / 하지만 나는 그게 사실이 아니라는 걸 알아'),
                                               ('She used to laugh at all the trouble we got in / Always finding ways '
                                                'to break the rules',
                                                '그녀는 우리가 저지른 모든 말썽에 웃곤 했어 / 늘 규칙을 깨는 방법을 찾으면서'),
                                               ("Lately I don't see her smile as often / I think you know it's you",
                                                '요즘 나는 그녀의 미소를 자주 보지 못해 / 너도 그게 너라는 걸 알고 있을 것 같아'),
                                               ("Don't take this the wrong way / I want you to be happy",
                                                '이 말을 오해하지는 마 / 나는 네가 행복했으면 좋겠어'),
                                               ("But it's hard to watch you fall again / 'Cause now I gotta play "
                                                'pretend',
                                                '하지만 네가 다시 상처받는 모습을 보는 건 힘들어 / 이제 나는 괜찮은 척해야 하니까'),
                                               ('Spending all of my time / Dancing on this fine line',
                                                '내 모든 시간을 보내며 / 이 아슬아슬한 선 위에서 춤추고 있어'),
                                               ("It's hard to watch you fall again / 'Cause now I gotta play pretend",
                                                '네가 다시 상처받는 모습을 보는 건 힘들어 / 이제 나는 괜찮은 척해야 하니까'),
                                               ('I know you like the back of my hand / I want you more every day and',
                                                '나는 너를 내 손등처럼 잘 알아 / 그리고 매일 너를 더 원하게 돼'),
                                               ("It's hard to watch you fall again / 'Cause now I gotta play pretend",
                                                '네가 다시 상처받는 모습을 보는 건 힘들어 / 이제 나는 괜찮은 척해야 하니까'),
                                               ("We can talk until three in the morning / The sun'll rise, I never "
                                                'want it to',
                                                '우리는 새벽 세 시까지 이야기할 수 있어 / 해가 뜨겠지만, 나는 그러길 원하지 않아'),
                                               ("Feelings for you came without warning / Ever since we met it's only "
                                                'you',
                                                '너를 향한 감정은 예고 없이 찾아왔어 / 우리가 만난 이후로 오직 너뿐이야'),
                                               ("Don't take this the wrong way / I want you to be happy",
                                                '이 말을 오해하지는 마 / 나는 네가 행복했으면 좋겠어'),
                                               ("But it's hard to watch you fall again / 'Cause now I gotta play "
                                                'pretend',
                                                '하지만 네가 다시 상처받는 모습을 보는 건 힘들어 / 이제 나는 괜찮은 척해야 하니까'),
                                               ('Spending all of my time / Dancing on this fine line',
                                                '내 모든 시간을 보내며 / 이 아슬아슬한 선 위에서 춤추고 있어'),
                                               ("It's hard to watch you fall again / 'Cause now I gotta play pretend",
                                                '네가 다시 상처받는 모습을 보는 건 힘들어 / 이제 나는 괜찮은 척해야 하니까'),
                                               ('I know you like the back of my hand / I want you more every day and',
                                                '나는 너를 내 손등처럼 잘 알아 / 그리고 매일 너를 더 원하게 돼'),
                                               ("It's hard to watch you fall again / 'Cause now I gotta play pretend",
                                                '네가 다시 상처받는 모습을 보는 건 힘들어 / 이제 나는 괜찮은 척해야 하니까'),
                                               ('All you gotta do is let me be your man / Got a hold on me like quick '
                                                'sand',
                                                '네가 해야 할 일은 내가 너의 사람이 되게 해 주는 것뿐이야 / 너는 모래늪처럼 나를 붙잡고 있어'),
                                               ("It's hard to watch you fall again / 'Cause now I gotta play pretend",
                                                '네가 다시 상처받는 모습을 보는 건 힘들어 / 이제 나는 괜찮은 척해야 하니까'),
                                               ("Don't take this the wrong way / I want you to be happy",
                                                '이 말을 오해하지는 마 / 나는 네가 행복했으면 좋겠어'),
                                               ("But it's hard to watch you fall again / 'Cause now I gotta play "
                                                'pretend',
                                                '하지만 네가 다시 상처받는 모습을 보는 건 힘들어 / 이제 나는 괜찮은 척해야 하니까')],
                                    'quiz': [{'q': '1. 이 노래에서 화자가 말하는 특별한 사람은 어떤 사람인가요?',
                                              'options': ['화자가 좋아하고 아끼는 사람', '처음 만난 낯선 사람', '학교 선생님', '유명한 배우'],
                                              'answer': '화자가 좋아하고 아끼는 사람'},
                                             {'q': '2. 화자는 상대가 무엇을 알았으면 좋겠다고 생각하나요?',
                                              'options': ['자신이 소중하고 완벽에 가까운 사람이라는 것',
                                                          '노래를 못한다는 것',
                                                          '규칙을 절대 어기면 안 된다는 것',
                                                          '멀리 떠나야 한다는 것'],
                                              'answer': '자신이 소중하고 완벽에 가까운 사람이라는 것'},
                                             {'q': "3. 'I want you to be happy'의 의미로 가장 알맞은 것은 무엇인가요?",
                                              'options': ['나는 네가 행복했으면 좋겠어',
                                                          '나는 네가 떠났으면 좋겠어',
                                                          '나는 네가 화났으면 좋겠어',
                                                          '나는 네가 조용했으면 좋겠어'],
                                              'answer': '나는 네가 행복했으면 좋겠어'},
                                             {'q': "4. 'play pretend'는 이 노래에서 어떤 의미에 가깝나요?",
                                              'options': ['괜찮은 척하다', '게임을 하다', '노래를 부르다', '규칙을 만들다'],
                                              'answer': '괜찮은 척하다'},
                                             {'q': "5. 'Dancing on this fine line'은 어떤 상황을 나타내나요?",
                                              'options': ['아슬아슬한 관계와 감정 사이에 있는 상황',
                                                          '무대에서 춤추는 상황',
                                                          '운동장에서 달리는 상황',
                                                          '시험을 준비하는 상황'],
                                              'answer': '아슬아슬한 관계와 감정 사이에 있는 상황'},
                                             {'q': "6. 'I know you like the back of my hand'의 의미는 무엇인가요?",
                                              'options': ['나는 너를 아주 잘 안다', '나는 네 손을 잡고 싶다', '나는 길을 잃었다', '나는 아무것도 모른다'],
                                              'answer': '나는 너를 아주 잘 안다'},
                                             {'q': '7. 이 노래의 중심 감정으로 가장 알맞은 것은 무엇인가요?',
                                              'options': ['숨겨야 하는 사랑과 안타까움', '승리의 기쁨', '분노와 복수', '여행의 설렘'],
                                              'answer': '숨겨야 하는 사랑과 안타까움'},
                                             {'q': '8. 화자가 보기 힘들어하는 것은 무엇인가요?',
                                              'options': ['상대가 다시 상처받는 모습', '비가 오는 날씨', '학교 시험', '아침에 일어나는 일'],
                                              'answer': '상대가 다시 상처받는 모습'}],
                                    'key_expressions': [('Someone special', '특별한 사람'),
                                                        ('I wish she knew', '그녀가 알았으면 좋겠어'),
                                                        ('Settle', '적당히 만족하다'),
                                                        ("That ain't true", '그건 사실이 아니야'),
                                                        ('Break the rules', '규칙을 깨다'),
                                                        ("Don't take this the wrong way", '이 말을 오해하지 마'),
                                                        ('I want you to be happy', '나는 네가 행복했으면 좋겠어'),
                                                        ('Play pretend', '괜찮은 척하다'),
                                                        ('Fine line', '아슬아슬한 경계선'),
                                                        ('Like the back of my hand', '아주 잘 아는')],
                                    'matching': [('Someone special', '특별한 사람'),
                                                 ('I want you to be happy', '나는 네가 행복했으면 좋겠어'),
                                                 ('Play pretend', '괜찮은 척하다'),
                                                 ('Fine line', '아슬아슬한 경계선'),
                                                 ('Like the back of my hand', '아주 잘 아는'),
                                                 ('Break the rules', '규칙을 깨다')],
                                    'reflect_questions': ['좋아하지만 솔직하게 말하지 못한 마음이 있었나요?',
                                                          '친구의 행복을 바라면서도 마음이 복잡했던 경험이 있나요?',
                                                          '괜찮은 척했지만 사실은 힘들었던 순간이 있나요?']},
 '10. Older - Sasha Alex Sloan': {'video_url': 'https://www.youtube.com/watch?v=M5WwinAObDA&list=RDM5WwinAObDA&start_radio=1',
                                  'bg': '\n'
                                        '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#9333ea;">\n'
                                        '        🌙 Older: 나이가 들며 이해하게 되는 것\n'
                                        '    </h3>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        Sasha Alex Sloan의 <b>Older</b>는 어린 시절에는 이해할 수 없었던 가족의 갈등과 부모의 모습을,\n'
                                        '        시간이 흐른 뒤 조금씩 다르게 바라보게 되는 마음을 담은 노래입니다.\n'
                                        '        제목의 <b>older</b>는 단순히 나이가 많아진다는 뜻을 넘어, 경험을 통해 사람과 관계를 더 깊이 이해하게 되는 '
                                        '과정을 의미합니다.\n'
                                        '    </p>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        노래 속 화자는 어릴 때 부모님의 다툼을 들으며 방 안에서 음악을 크게 틀고,\n'
                                        '        그 소리를 듣지 않으려 했던 기억을 떠올립니다.\n'
                                        '        그때는 부모님이 왜 행복하지 못한지 이해하지 못했고,\n'
                                        '        자신은 절대 부모님처럼 되지 않겠다고 생각했습니다.\n'
                                        '    </p>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        하지만 나이가 들수록 화자는 부모님도 완벽한 영웅이 아니라,\n'
                                        '        자신처럼 상처받고 실수하고 사랑을 어려워하는 한 사람이라는 것을 깨닫습니다.\n'
                                        '        그래서 이 노래는 원망에서 이해로, 분노에서 받아들임으로 변해 가는 감정을 보여 줍니다.\n'
                                        '    </p>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        수업에서는 <b>I used to</b>, <b>the older I get</b>, <b>heroes</b>,\n'
                                        '        <b>loving is hard</b>, <b>try your best</b>, <b>let someone go</b> 같은 '
                                        '표현을 중심으로 배울 수 있습니다.\n'
                                        '        특히 이 노래는 가족, 성장, 이해, 용서, 관계의 어려움을 주제로 생각을 적기에 좋습니다.\n'
                                        '    </p>\n'
                                        '    ',
                                  'lyrics': [('I used to shut my door while my mother screamed in the kitchen',
                                              '엄마가 부엌에서 소리칠 때 나는 방문을 닫곤 했어'),
                                             ("I'd turn the music up, get high and try not to listen",
                                              '나는 음악을 크게 틀고, 정신을 흐리게 한 채 듣지 않으려 했어'),
                                             ("To every little fight, 'cause neither one was right",
                                              '사소한 싸움 하나하나를 듣지 않으려고 했어, 어느 쪽도 맞지 않았으니까'),
                                             ("I swore I'd never be like them / But I was just a kid back then",
                                              '나는 절대 그들처럼 되지 않겠다고 맹세했어 / 하지만 그때 나는 그저 아이였어'),
                                             ('The older I get the more that I see', '나이가 들수록 더 많이 보이게 돼'),
                                             ("My parents aren't heroes, they're just like me",
                                              '내 부모님은 영웅이 아니라, 그저 나와 같은 사람이야'),
                                             ("And loving is hard, it don't always work", '그리고 사랑은 어렵고, 항상 잘되는 것은 아니야'),
                                             ('You just try your best not to get hurt', '그저 상처받지 않으려고 최선을 다할 뿐이야'),
                                             ('I used to be mad but now I know', '나는 예전에는 화가 났지만 이제는 알아'),
                                             ("Sometimes it's better to let someone go",
                                              '때로는 누군가를 놓아주는 것이 더 나을 때도 있다는 것을'),
                                             ("It just hadn't hit me yet / The older I get",
                                              '그게 아직 내 마음에 와닿지 않았을 뿐이야 / 나이가 들수록'),
                                             ('I used to wonder why, why they could never be happy',
                                              '나는 왜, 왜 그들이 결코 행복할 수 없었는지 궁금해하곤 했어'),
                                             ("I used to close my eyes and pray for a whole 'nother family",
                                              '나는 눈을 감고 완전히 다른 가족을 달라고 기도하곤 했어'),
                                             ('Where everything was fine, one that felt like mine',
                                              '모든 것이 괜찮고, 내 것처럼 느껴지는 가족을'),
                                             ("I swore I'd never be like them / But I was just a kid back then",
                                              '나는 절대 그들처럼 되지 않겠다고 맹세했어 / 하지만 그때 나는 그저 아이였어'),
                                             ('The older I get the more that I see', '나이가 들수록 더 많이 보이게 돼'),
                                             ("My parents aren't heroes, they're just like me",
                                              '내 부모님은 영웅이 아니라, 그저 나와 같은 사람이야'),
                                             ("And loving is hard, it don't always work", '그리고 사랑은 어렵고, 항상 잘되는 것은 아니야'),
                                             ('You just try your best not to get hurt', '그저 상처받지 않으려고 최선을 다할 뿐이야'),
                                             ('I used to be mad but now I know', '나는 예전에는 화가 났지만 이제는 알아'),
                                             ("Sometimes it's better to let someone go",
                                              '때로는 누군가를 놓아주는 것이 더 나을 때도 있다는 것을'),
                                             ("It just hadn't hit me yet / The older I get",
                                              '그게 아직 내 마음에 와닿지 않았을 뿐이야 / 나이가 들수록'),
                                             ('The older I get the more that I see', '나이가 들수록 더 많이 보이게 돼'),
                                             ("My parents aren't heroes, they're just like me",
                                              '내 부모님은 영웅이 아니라, 그저 나와 같은 사람이야'),
                                             ("And loving is hard, it don't always work", '그리고 사랑은 어렵고, 항상 잘되는 것은 아니야'),
                                             ('You just try your best not to get hurt', '그저 상처받지 않으려고 최선을 다할 뿐이야'),
                                             ('I used to be mad but now I know', '나는 예전에는 화가 났지만 이제는 알아'),
                                             ("Sometimes it's better to let someone go",
                                              '때로는 누군가를 놓아주는 것이 더 나을 때도 있다는 것을'),
                                             ("It just hadn't hit me yet / The older I get",
                                              '그게 아직 내 마음에 와닿지 않았을 뿐이야 / 나이가 들수록')],
                                  'quiz': [{'q': '1. 이 노래에서 화자는 어릴 때 무엇을 듣지 않으려고 했나요?',
                                            'options': ['부모님의 싸움', '친구의 웃음소리', '선생님의 설명', '바닷소리'],
                                            'answer': '부모님의 싸움'},
                                           {'q': '2. 화자는 어릴 때 어떤 가족을 바라곤 했나요?',
                                            'options': ['모든 것이 괜찮은 다른 가족', '유명한 가수의 가족', '운동선수 가족', '외국에 사는 가족'],
                                            'answer': '모든 것이 괜찮은 다른 가족'},
                                           {'q': "3. 'The older I get the more that I see'의 의미로 가장 알맞은 것은 무엇인가요?",
                                            'options': ['나이가 들수록 더 많이 이해하게 된다',
                                                        '나이가 들수록 아무것도 보이지 않는다',
                                                        '나이가 들수록 음악을 싫어한다',
                                                        '나이가 들수록 항상 화만 난다'],
                                            'answer': '나이가 들수록 더 많이 이해하게 된다'},
                                           {'q': "4. 'My parents aren't heroes, they're just like me'는 어떤 의미인가요?",
                                            'options': ['부모님도 완벽하지 않은 한 사람이라는 뜻',
                                                        '부모님은 실제 영웅이라는 뜻',
                                                        '부모님은 나와 전혀 다르다는 뜻',
                                                        '부모님은 항상 옳다는 뜻'],
                                            'answer': '부모님도 완벽하지 않은 한 사람이라는 뜻'},
                                           {'q': "5. 'Loving is hard, it don't always work'의 의미는 무엇인가요?",
                                            'options': ['사랑은 어렵고 항상 잘되는 것은 아니다',
                                                        '사랑은 언제나 쉽다',
                                                        '사랑은 필요 없다',
                                                        '사랑은 공부와 같다'],
                                            'answer': '사랑은 어렵고 항상 잘되는 것은 아니다'},
                                           {'q': "6. 'Sometimes it's better to let someone go'의 의미로 가장 알맞은 것은 무엇인가요?",
                                            'options': ['때로는 누군가를 놓아주는 것이 더 나을 수 있다',
                                                        '항상 붙잡아야 한다',
                                                        '절대 헤어지면 안 된다',
                                                        '누군가를 무조건 미워해야 한다'],
                                            'answer': '때로는 누군가를 놓아주는 것이 더 나을 수 있다'},
                                           {'q': '7. 이 노래에서 화자의 감정 변화로 가장 알맞은 것은 무엇인가요?',
                                            'options': ['원망에서 이해로 변해 감',
                                                        '기쁨에서 질투로 변해 감',
                                                        '자신감에서 두려움으로 변해 감',
                                                        '무관심에서 승리감으로 변해 감'],
                                            'answer': '원망에서 이해로 변해 감'},
                                           {'q': '8. 이 노래의 중심 주제로 가장 알맞은 것은 무엇인가요?',
                                            'options': ['성장하며 부모와 사랑을 이해하게 되는 마음',
                                                        '여행의 즐거움',
                                                        '학교 시험의 어려움',
                                                        '친구와 규칙을 깨는 재미'],
                                            'answer': '성장하며 부모와 사랑을 이해하게 되는 마음'}],
                                  'key_expressions': [('I used to', '나는 ~하곤 했다'),
                                                      ('Shut my door', '방문을 닫다'),
                                                      ('Turn the music up', '음악을 크게 틀다'),
                                                      ('Try not to listen', '듣지 않으려고 하다'),
                                                      ('I swore', '나는 맹세했다'),
                                                      ('The older I get', '나이가 들수록'),
                                                      ("My parents aren't heroes", '내 부모님은 영웅이 아니다'),
                                                      ('Loving is hard', '사랑은 어렵다'),
                                                      ('Try your best', '최선을 다하다'),
                                                      ('Let someone go', '누군가를 놓아주다')],
                                  'matching': [('I used to', '나는 ~하곤 했다'),
                                               ('The older I get', '나이가 들수록'),
                                               ("My parents aren't heroes", '내 부모님은 영웅이 아니다'),
                                               ('Loving is hard', '사랑은 어렵다'),
                                               ('Try your best', '최선을 다하다'),
                                               ('Let someone go', '누군가를 놓아주다')],
                                  'reflect_questions': ['나이가 들면서 부모님이나 가족을 다르게 이해하게 된 경험이 있나요?',
                                                        '어릴 때는 이해하지 못했지만 지금은 조금 이해되는 일이 있나요?',
                                                        '누군가를 붙잡기보다 놓아주는 것이 더 낫다고 느낀 적이 있나요?']},
 '11. No One Else Like You - Adam Levine': {'video_url': 'https://www.youtube.com/watch?v=llpw7u3X11M&list=RDllpw7u3X11M&start_radio=1',
                                            'bg': '\n'
                                                  '    <h3 style="font-size:2.2rem; margin-bottom:20px; '
                                                  'color:#db2777;">\n'
                                                  '        💘 No One Else Like You: 너 같은 사람은 없다는 마음\n'
                                                  '    </h3>\n'
                                                  '\n'
                                                  '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                                  '        노래 속 화자는 상대가 이미 다른 사람과 함께 있는 상황에서도,\n'
                                                  '        자신이 원하는 사람은 오직 그 사람뿐이라고 말합니다.\n'
                                                  '        상대를 닮은 사람, 상대처럼 웃는 사람, 상대처럼 느껴지는 사람을 원한다고 반복하면서,\n'
                                                  '        결국 누구도 그 사람을 대신할 수 없다는 마음을 표현합니다.\n'
                                                  '    </p>\n'
                                                  '\n'
                                                  '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                                  '        수업에서는 <b>someone just like you</b>, <b>through and '
                                                  'through</b>,\n'
                                                  '        <b>physical attraction</b>, <b>man of action</b>, <b>in my '
                                                  'dreams</b>,\n'
                                                  '        <b>no one else</b> 같은 표현을 중심으로 배울 수 있습니다.\n'
                                                  '        특히 이 노래는 좋아하는 사람을 향한 마음, 고백, 기다림, 진심을 주제로 생각을 적기에 좋습니다.\n'
                                                  '    </p>\n'
                                                  '    ',
                                            'lyrics': [('Oh, woah-oh / Woah-woah-oh-oh / Oh, yeah',
                                                        '오, 워-oh / 워-워-oh-oh / 오, 그래'),
                                                       ("Is everything just right / Don't want you thinking that I'm "
                                                        'in a hurry',
                                                        '모든 것이 괜찮은 걸까 / 내가 서두르고 있다고 네가 생각하길 원하지 않아'),
                                                       ("I won't stay afraid / I have this vision and it's got me "
                                                        'worried',
                                                        '나는 계속 두려워하고만 있지 않을 거야 / 내게 이런 상상이 있고, 그것이 나를 걱정하게 해'),
                                                       ("'Cause everyone wants someone / That's one cliché that's true",
                                                        '왜냐하면 누구나 누군가를 원하니까 / 그것은 흔한 말이지만 사실이야'),
                                                       ("The sad truth's, I want no one / Unless that someone's you",
                                                        '슬픈 진실은, 나는 아무도 원하지 않아 / 그 누군가가 네가 아니라면'),
                                                       ('And looks like you / Feels like you / Smiles like you',
                                                        '그리고 너처럼 보이고 / 너처럼 느껴지고 / 너처럼 웃는 사람'),
                                                       ('I want someone just like you / Through and through',
                                                        '나는 너와 꼭 같은 사람을 원해 / 처음부터 끝까지'),
                                                       ("I'm forever blue / 'Cause there's no one else like",
                                                        '나는 영원히 우울할 거야 / 왜냐하면 그런 사람은 아무도 없으니까'),
                                                       ("I hope that you're not mad / You always said you want a man "
                                                        'of action',
                                                        '네가 화나지 않았으면 좋겠어 / 너는 항상 행동하는 남자를 원한다고 말했지'),
                                                       ("I'm not the hottest lad, no / There's more to life than "
                                                        'physical attraction',
                                                        '나는 가장 멋진 남자는 아니야 / 삶에는 외적인 끌림보다 더 중요한 것이 있어'),
                                                       ('You got your special someone / But between me and him, guess '
                                                        'who',
                                                        '너에게는 특별한 누군가가 있어 / 하지만 나와 그 사람 사이에서, 누가'),
                                                       ('Will spend their whole life waiting / For someone just like '
                                                        'you',
                                                        '평생을 기다리며 보낼까 / 너 같은 사람을'),
                                                       ('That looks like you / That feels like you / That smiles like '
                                                        'you',
                                                        '너처럼 보이고 / 너처럼 느껴지고 / 너처럼 웃는 사람을'),
                                                       ('I need someone just like you / Love me true',
                                                        '나는 너와 꼭 같은 사람이 필요해 / 나를 진심으로 사랑해 줘'),
                                                       ("I'm forever blue / 'Cause there's no one else like",
                                                        '나는 영원히 우울할 거야 / 왜냐하면 그런 사람은 아무도 없으니까'),
                                                       ('Hoo, woah-woah-oh-oh, hoo-ooh', '후, 워-워-oh-oh, 후-ooh'),
                                                       ('I want you in my arms / I see you in my dreams',
                                                        '나는 너를 내 품에 안고 싶어 / 나는 꿈속에서 너를 봐'),
                                                       ("I'm gonna make you mine / As crazy as it seems",
                                                        '나는 너를 내 사람으로 만들 거야 / 미친 말처럼 들리겠지만'),
                                                       ('Girl, you, yes you / I need someone just like you',
                                                        '너야, 바로 너 / 나는 너와 꼭 같은 사람이 필요해'),
                                                       ("Love me true / I'm forever blue",
                                                        '나를 진심으로 사랑해 줘 / 나는 영원히 우울할 거야'),
                                                       ("'Cause there's no one else / There's no one else",
                                                        '왜냐하면 다른 사람은 없으니까 / 다른 사람은 없으니까'),
                                                       ("There's no one else / There's no one else",
                                                        '다른 사람은 없어 / 다른 사람은 없어'),
                                                       ("There's no one else / There's no one else",
                                                        '다른 사람은 없어 / 다른 사람은 없어'),
                                                       ("There's no one else I need to have", '내게 필요한 다른 사람은 아무도 없어'),
                                                       ("'Cause you're so fine / You're so fine",
                                                        '왜냐하면 너는 정말 멋지니까 / 너는 정말 멋지니까'),
                                                       ("'Cause you're so fine / You're so fine",
                                                        '왜냐하면 너는 정말 멋지니까 / 너는 정말 멋지니까'),
                                                       ("'Cause you're so fine / You're so fine",
                                                        '왜냐하면 너는 정말 멋지니까 / 너는 정말 멋지니까'),
                                                       ("'Cause you're so fine / You're so fine",
                                                        '왜냐하면 너는 정말 멋지니까 / 너는 정말 멋지니까'),
                                                       ("'Cause you're so fine / You're so fine",
                                                        '왜냐하면 너는 정말 멋지니까 / 너는 정말 멋지니까')],
                                            'quiz': [{'q': '1. 이 노래에서 화자가 원하는 사람은 누구와 같은 사람인가요?',
                                                      'options': ['상대와 같은 사람', '전혀 모르는 사람', '유명한 배우', '오래된 친구가 아닌 사람'],
                                                      'answer': '상대와 같은 사람'},
                                                     {'q': '2. 화자는 자신이 서두르고 있다고 상대가 생각하길 원하나요?',
                                                      'options': ['아니요, 그렇게 생각하지 않길 원한다',
                                                                  '네, 빨리 고백하고 싶다',
                                                                  '전혀 관심이 없다',
                                                                  '상대를 피하고 싶다'],
                                                      'answer': '아니요, 그렇게 생각하지 않길 원한다'},
                                                     {'q': "3. 'I want no one unless that someone's you'의 의미로 가장 알맞은 "
                                                           '것은 무엇인가요?',
                                                      'options': ['그 사람이 네가 아니라면 아무도 원하지 않는다',
                                                                  '아무나 괜찮다',
                                                                  '너를 잊고 싶다',
                                                                  '혼자 있는 것이 가장 좋다'],
                                                      'answer': '그 사람이 네가 아니라면 아무도 원하지 않는다'},
                                                     {'q': "4. 'I want someone just like you'는 어떤 뜻인가요?",
                                                      'options': ['너와 꼭 같은 사람을 원해',
                                                                  '너와 전혀 다른 사람을 원해',
                                                                  '아무도 필요 없어',
                                                                  '친구가 되고 싶지 않아'],
                                                      'answer': '너와 꼭 같은 사람을 원해'},
                                                     {'q': "5. 'physical attraction'의 뜻으로 가장 알맞은 것은 무엇인가요?",
                                                      'options': ['외적인 끌림', '학교 성적', '운동 능력', '가족 관계'],
                                                      'answer': '외적인 끌림'},
                                                     {'q': "6. 'I see you in my dreams'는 어떤 의미인가요?",
                                                      'options': ['꿈속에서 너를 본다',
                                                                  '너를 전혀 생각하지 않는다',
                                                                  '잠을 자지 못한다',
                                                                  '꿈을 싫어한다'],
                                                      'answer': '꿈속에서 너를 본다'},
                                                     {'q': '7. 이 노래의 중심 감정으로 가장 알맞은 것은 무엇인가요?',
                                                      'options': ['특별한 사람을 향한 간절한 마음',
                                                                  '시험에 대한 긴장',
                                                                  '여행의 설렘',
                                                                  '친구와의 장난'],
                                                      'answer': '특별한 사람을 향한 간절한 마음'},
                                                     {'q': "8. 반복되는 'There's no one else'는 무엇을 강조하나요?",
                                                      'options': ['상대를 대신할 사람은 없다는 마음',
                                                                  '사람이 너무 많다는 사실',
                                                                  '혼자 있는 것이 좋다는 마음',
                                                                  '노래를 멈추고 싶다는 마음'],
                                                      'answer': '상대를 대신할 사람은 없다는 마음'}],
                                            'key_expressions': [('No one else like you', '너 같은 사람은 아무도 없어'),
                                                                ('Just right', '딱 맞는'),
                                                                ("I'm in a hurry", '나는 서두르고 있어'),
                                                                ('Someone just like you', '너와 꼭 같은 사람'),
                                                                ('Through and through', '처음부터 끝까지'),
                                                                ("I'm forever blue", '나는 영원히 우울해'),
                                                                ('Man of action', '행동하는 사람'),
                                                                ('Physical attraction', '외적인 끌림'),
                                                                ('In my dreams', '내 꿈속에서'),
                                                                ('Love me true', '나를 진심으로 사랑해 줘')],
                                            'matching': [('No one else like you', '너 같은 사람은 아무도 없어'),
                                                         ('Someone just like you', '너와 꼭 같은 사람'),
                                                         ('Through and through', '처음부터 끝까지'),
                                                         ('Physical attraction', '외적인 끌림'),
                                                         ('I see you in my dreams', '나는 꿈속에서 너를 봐'),
                                                         ('Love me true', '나를 진심으로 사랑해 줘')],
                                            'reflect_questions': ['나에게 “너 같은 사람은 없다”고 느껴지는 사람이 있나요?',
                                                                  '좋아하는 마음을 쉽게 말하지 못했던 경험이 있나요?',
                                                                  '외적인 모습보다 더 중요하다고 생각하는 매력은 무엇인가요?']},
 '12. Out of Time - The Weeknd': {'video_url': 'https://www.youtube.com/watch?v=S0eUa8QTsFQ&list=RDS0eUa8QTsFQ&start_radio=1',
                                  'bg': '\n'
                                        '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#7c2d12;">\n'
                                        '        ⏳ Out of Time: 너무 늦게 깨달은 후회\n'
                                        '    </h3>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        The Weeknd의 <b>Out of Time</b>은 사랑하는 사람에게 상처를 주고 난 뒤,\n'
                                        '        뒤늦게 자신의 잘못을 깨닫지만 이미 너무 늦어 버린 상황을 담은 노래입니다.\n'
                                        '        제목의 <b>out of time</b>은 “시간이 다 되었다”, “이미 늦었다”라는 뜻으로,\n'
                                        '        후회와 미련이 섞인 화자의 마음을 잘 보여 줍니다.\n'
                                        '    </p>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        노래 속 화자는 지난 몇 달 동안 자기 자신을 돌아보고 있었다고 말합니다.\n'
                                        '        자신의 삶에 많은 상처가 있었고, 그 상처 때문에 자신을 사랑해 준 사람들에게 차갑게 대했다는 사실을 깨닫습니다.\n'
                                        '        하지만 그 깨달음은 이미 상대가 다른 사람을 선택한 뒤에 찾아옵니다.\n'
                                        '    </p>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        "        반복되는 <b>I'm out of time</b>은 사랑한다고 말하고 싶고, 곁에 있어 주고 싶고,\n"
                                        '        잘해 주고 싶지만 이미 기회를 놓쳤다는 고백입니다.\n'
                                        '        화자는 다시 한 번만 기회를 달라고 말하지만, 동시에 상대가 이미 마음을 정했다는 사실도 알고 있습니다.\n'
                                        '    </p>\n'
                                        '\n'
                                        '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                        '        수업에서는 <b>working on me</b>, <b>trauma</b>, <b>look back</b>,\n'
                                        '        <b>I regret</b>, <b>made up your mind</b>, <b>out of time</b>,\n'
                                        '        <b>give me one chance</b> 같은 표현을 중심으로 배울 수 있습니다.\n'
                                        '        특히 이 노래는 후회, 자기 성찰, 놓친 기회, 관계에서의 책임을 주제로 생각을 적기에 좋습니다.\n'
                                        '    </p>\n'
                                        '    ',
                                  'lyrics': [("Yeah, yeah / The last few months, I've been working on me, baby",
                                              '그래, 그래 / 지난 몇 달 동안 나는 나 자신을 돌아보고 있었어'),
                                             ("There's so much trauma in my life", '내 삶에는 너무 많은 상처가 있어'),
                                             ("I've been so cold to the ones who loved me, baby",
                                              '나는 나를 사랑해 준 사람들에게 너무 차갑게 굴었어'),
                                             ('I look back now and I realize', '이제 돌아보니 나는 깨닫게 돼'),
                                             ('I remember when I held you', '내가 너를 안았던 때가 기억나'),
                                             ('You begged me with your drowning eyes to stay',
                                              '너는 물에 잠길 듯한 눈으로 내게 머물러 달라고 애원했어'),
                                             ("And I regret I didn't tell you", '그리고 내가 너에게 말하지 않았던 것을 후회해'),
                                             ("Now I can't keep you from loving him, you made up your mind",
                                              '이제 나는 네가 그를 사랑하는 것을 막을 수 없어, 너는 이미 마음을 정했으니까'),
                                             ("Say I love you, girl, but I'm out of time", '사랑한다고 말하고 싶지만, 나는 이미 늦었어'),
                                             ("Say I'm there for you, but I'm out of time",
                                              '네 곁에 있겠다고 말하고 싶지만, 나는 이미 늦었어'),
                                             ("Say that I'll care for you, but I'm out of time",
                                              '널 아껴 주겠다고 말하고 싶지만, 나는 이미 늦었어'),
                                             ("Said, I'm too late to make you mine, out of time",
                                              '너를 내 사람으로 만들기에는 너무 늦었어, 시간이 다 됐어'),
                                             ('If he mess up just a little, baby, you know my line',
                                              '그가 조금이라도 잘못하면, 내 연락처를 알잖아'),
                                             ("If you don't trust him a little, then come right back, girl, come right "
                                              'back',
                                              '그를 조금이라도 믿지 못하겠다면, 다시 돌아와 줘'),
                                             ("Gimme one chance, just a little, baby, I'll treat you right",
                                              '나에게 한 번만 기회를 줘, 내가 너를 잘 대해 줄게'),
                                             ("And I'll love you like I should've loved you all the time",
                                              '그리고 내가 처음부터 그랬어야 했던 것처럼 너를 사랑할게'),
                                             ('And I remember when I held you', '그리고 내가 너를 안았던 때가 기억나'),
                                             ('You begged me with your drowning eyes to stay',
                                              '너는 물에 잠길 듯한 눈으로 내게 머물러 달라고 애원했어'),
                                             ("And I regret I didn't tell you", '그리고 내가 너에게 말하지 않았던 것을 후회해'),
                                             ("Now I can't keep you from loving him, you made up your mind",
                                              '이제 나는 네가 그를 사랑하는 것을 막을 수 없어, 너는 이미 마음을 정했으니까'),
                                             ("Say I love you, girl, but I'm out of time", '사랑한다고 말하고 싶지만, 나는 이미 늦었어'),
                                             ("Say I'm there for you, but I'm out of time",
                                              '네 곁에 있겠다고 말하고 싶지만, 나는 이미 늦었어'),
                                             ("Say that I'll care for you, but I'm out of time",
                                              '널 아껴 주겠다고 말하고 싶지만, 나는 이미 늦었어'),
                                             ("Said, I'm too late to make you mine, out of time",
                                              '너를 내 사람으로 만들기에는 너무 늦었어, 시간이 다 됐어'),
                                             ("Said, I had you to myself, but I'm out of time",
                                              '한때 너는 내 곁에 있었지만, 이제 나는 이미 늦었어'),
                                             ("Say that I'll care for you, but I'm out of time",
                                              '널 아껴 주겠다고 말하고 싶지만, 나는 이미 늦었어'),
                                             ("But I'm too late to make you mine, out of time",
                                              '하지만 너를 내 사람으로 만들기에는 너무 늦었어, 시간이 다 됐어'),
                                             ('Out of time, out of time', '시간이 다 됐어, 이미 늦었어'),
                                             ("Don't you dare touch that dial", '채널을 돌릴 생각은 하지 마'),
                                             ('Because like the song says, you are out of time',
                                              '노래가 말하듯, 당신은 시간이 다 되었으니까'),
                                             ("You're almost there, but don't panic", '거의 다 왔지만, 당황하지 마'),
                                             ("There's still more music to come before you're completely engulfed",
                                              '완전히 휩싸이기 전에 아직 더 많은 음악이 남아 있어'),
                                             ('In the blissful embrace of that little light you see in the distance',
                                              '멀리 보이는 작은 빛의 평온한 품 안으로'),
                                             ("Soon you'll be healed, forgiven, and refreshed, free from all trauma, "
                                              'pain, guilt, and shame',
                                              '곧 당신은 치유되고, 용서받고, 새로워져 모든 상처와 고통, 죄책감과 수치심에서 자유로워질 거야'),
                                             ('You may even forget your own name, but before you dwell in that house '
                                              'forever',
                                              '어쩌면 자신의 이름도 잊을 수 있어, 하지만 그 집에 영원히 머물기 전에'),
                                             ("Here's 30 minutes of easy listening to some slow tracks, on 103.5 Dawn "
                                              'FM',
                                              '103.5 Dawn FM에서 편안히 들을 수 있는 느린 음악 30분을 들려줄게')],
                                  'quiz': [{'q': '1. 이 노래에서 화자는 지난 몇 달 동안 무엇을 하고 있었다고 말하나요?',
                                            'options': ['자기 자신을 돌아보고 있었다',
                                                        '여행을 준비하고 있었다',
                                                        '새로운 학교에 다니고 있었다',
                                                        '운동을 배우고 있었다'],
                                            'answer': '자기 자신을 돌아보고 있었다'},
                                           {'q': '2. 화자는 자신을 사랑해 준 사람들에게 어떻게 대했다고 말하나요?',
                                            'options': ['차갑게 대했다', '항상 친절하게 대했다', '아무 말도 하지 않았다', '선물을 많이 주었다'],
                                            'answer': '차갑게 대했다'},
                                           {'q': "3. 'I regret I didn't tell you'의 의미로 가장 알맞은 것은 무엇인가요?",
                                            'options': ['말하지 않았던 것을 후회한다', '너를 잊었다', '나는 시간이 많다', '아무것도 느끼지 않는다'],
                                            'answer': '말하지 않았던 것을 후회한다'},
                                           {'q': "4. 'You made up your mind'는 어떤 의미인가요?",
                                            'options': ['너는 이미 마음을 정했다', '너는 길을 잃었다', '너는 노래를 만들었다', '너는 생각이 없다'],
                                            'answer': '너는 이미 마음을 정했다'},
                                           {'q': "5. 'I'm out of time'의 의미로 가장 알맞은 것은 무엇인가요?",
                                            'options': ['나는 이미 늦었다', '나는 시간이 아주 많다', '나는 밖에 있다', '나는 시간을 만들었다'],
                                            'answer': '나는 이미 늦었다'},
                                           {'q': '6. 화자가 원하는 것은 무엇인가요?',
                                            'options': ['다시 한 번 기회를 얻는 것',
                                                        '상대를 완전히 잊는 것',
                                                        '다른 도시로 떠나는 것',
                                                        '노래를 그만두는 것'],
                                            'answer': '다시 한 번 기회를 얻는 것'},
                                           {'q': '7. 이 노래의 중심 감정으로 가장 알맞은 것은 무엇인가요?',
                                            'options': ['후회와 늦은 깨달음', '승리와 자신감', '여행의 설렘', '분노와 복수'],
                                            'answer': '후회와 늦은 깨달음'},
                                           {'q': '8. 이 노래가 보여 주는 관계의 상황으로 가장 알맞은 것은 무엇인가요?',
                                            'options': ['화자가 뒤늦게 후회하지만 상대는 이미 마음을 정한 상황',
                                                        '두 사람이 처음 만나는 상황',
                                                        '친구들이 함께 여행하는 상황',
                                                        '가족이 화해하는 상황'],
                                            'answer': '화자가 뒤늦게 후회하지만 상대는 이미 마음을 정한 상황'}],
                                  'key_expressions': [('Working on me', '나 자신을 돌아보고 노력하는 중'),
                                                      ('Trauma', '상처, 트라우마'),
                                                      ('Look back', '돌아보다'),
                                                      ('I realize', '나는 깨닫다'),
                                                      ('I regret', '나는 후회하다'),
                                                      ('Made up your mind', '마음을 정했다'),
                                                      ("I'm out of time", '나는 이미 늦었다'),
                                                      ('Gimme one chance', '나에게 한 번만 기회를 줘'),
                                                      ("I'll treat you right", '내가 너를 잘 대해 줄게'),
                                                      ('Too late', '너무 늦은')],
                                  'matching': [('Working on me', '나 자신을 돌아보고 노력하는 중'),
                                               ('I regret', '나는 후회하다'),
                                               ('Made up your mind', '마음을 정했다'),
                                               ("I'm out of time", '나는 이미 늦었다'),
                                               ('Gimme one chance', '나에게 한 번만 기회를 줘'),
                                               ('Too late', '너무 늦은')],
                                  'reflect_questions': ['뒤늦게 후회했던 말이나 행동이 있나요?',
                                                        '시간이 지나고 나서야 소중함을 깨달은 사람이 있나요?',
                                                        '다시 기회가 주어진다면 다르게 행동하고 싶은 순간이 있나요?']},
 "13. I Don't Think So - Priscilla Ahn": {'video_url': 'https://www.youtube.com/watch?v=19bUY3sRqqI&list=RD19bUY3sRqqI&start_radio=1',
                                          'bg': '\n'
                                                '    <h3 style="font-size:2.2rem; margin-bottom:20px; '
                                                'color:#be123c;">\n'
                                                "        🚪 I Don't Think So: 이용당하지 않겠다는 단호한 마음\n"
                                                '    </h3>\n'
                                                '\n'
                                                '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                                "        Priscilla Ahn의 <b>I Don't Think So</b>는 관계 속에서 애매한 태도와 상처를 느낀 "
                                                '화자가\n'
                                                '        더 이상 이용당하지 않겠다고 말하는 노래입니다.\n'
                                                "        제목의 <b>I don't think so</b>는 단순히 “나는 그렇게 생각하지 않아”라는 뜻을 넘어,\n"
                                                '        “그건 아닌 것 같아”, “나는 받아들이지 않겠어”라는 단호한 거절의 의미로 이해할 수 있습니다.\n'
                                                '    </p>\n'
                                                '\n'
                                                '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                                '        노래 속 화자는 상대가 자신에게 확실한 마음을 보이지 않으면서도\n'
                                                '        자신을 곁에 두려는 듯한 태도를 느낍니다.\n'
                                                '        그래서 처음에는 너무 친절하게 대해 왔지만, 이제는 그 관계가 자신을 혼란스럽게 만들고 있다는 것을 '
                                                '깨닫습니다.\n'
                                                '        <b>I can take a hint</b>, <b>I can take a clue</b>는 상대의 눈치와 '
                                                '신호를 알아차렸다는 뜻이고,\n'
                                                '        <b>I am not here for you to use</b>는 더 이상 이용당하지 않겠다는 자기 존중의 '
                                                '표현입니다.\n'
                                                '    </p>\n'
                                                '\n'
                                                '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                                "        수업에서는 <b>I don't think so</b>, <b>I think I should go</b>,\n"
                                                '        <b>take a hint</b>, <b>take a clue</b>, <b>utterly '
                                                'confused</b>,\n'
                                                '        <b>I am not here for you to use</b> 같은 표현을 중심으로 배울 수 있습니다.\n'
                                                '        이 노래는 짧은 문장과 반복 표현이 많아, 학생들이 관계 속 감정과 단호한 자기표현을 영어로 익히기에 '
                                                '좋습니다.\n'
                                                '    </p>\n'
                                                '    ',
                                          'lyrics': [('Girl, you were looking at him a little too long for me / To be '
                                                      'your friend',
                                                      '너는 그를 너무 오래 바라보고 있었어 / 내가 너의 친구로 있기에는 말이야'),
                                                     ('And boy, you were looking at her a little too short / For me to '
                                                      'be yours',
                                                      '그리고 너는 그녀를 너무 짧게 바라보고 있었어 / 내가 너의 사람이 되기에는 말이야'),
                                                     ("And I've been really too nice, I know",
                                                      '그리고 나는 정말 너무 친절했어, 나도 알아'),
                                                     ('You probably thought that we were just a show',
                                                      '너는 아마 우리가 그저 보여 주기 위한 관계라고 생각했겠지'),
                                                     ('But you better listen up / You better listen close',
                                                      '하지만 너는 잘 들어야 해 / 아주 가까이서 잘 들어야 해'),
                                                     ("I don't think so", '나는 그렇게 생각하지 않아 / 그건 아닌 것 같아'),
                                                     ('I think I should go', '나는 가야 할 것 같아'),
                                                     ('I can feel your eyes look at me and the door',
                                                      '네 시선이 나와 문을 바라보는 것이 느껴져'),
                                                     ('Oh, I can take a hint / Oh, I can take a clue',
                                                      '오, 나는 눈치를 챌 수 있어 / 오, 나는 단서를 알아차릴 수 있어'),
                                                     ("You're giving me the go, sir / You're giving me the boot",
                                                      '너는 나에게 가라는 신호를 주고 있어 / 너는 나를 쫓아내고 있어'),
                                                     ("And I've been really too nice, I know",
                                                      '그리고 나는 정말 너무 친절했어, 나도 알아'),
                                                     ('You probably thought that we were just a show',
                                                      '너는 아마 우리가 그저 보여 주기 위한 관계라고 생각했겠지'),
                                                     ('But you left me utterly confused', '하지만 너는 나를 완전히 혼란스럽게 만들었어'),
                                                     ('I am not here for you to use', '나는 네가 이용하라고 여기 있는 게 아니야'),
                                                     ('So you better listen up / You better listen close',
                                                      '그러니 너는 잘 들어야 해 / 아주 가까이서 잘 들어야 해'),
                                                     ("I don't think so", '나는 그렇게 생각하지 않아 / 그건 아닌 것 같아')],
                                          'quiz': [{'q': '1. 이 노래에서 화자가 느끼는 중심 감정으로 가장 알맞은 것은 무엇인가요?',
                                                    'options': ['설렘과 기대', '혼란과 단호한 거절', '여행의 즐거움', '승리의 자신감'],
                                                    'answer': '혼란과 단호한 거절'},
                                                   {'q': '2. 화자는 자신이 너무 어떻게 행동했다고 말하나요?',
                                                    'options': ['너무 조용했다', '너무 친절했다', '너무 빨리 달렸다', '너무 늦게 왔다'],
                                                    'answer': '너무 친절했다'},
                                                   {'q': "3. 'I don't think so'의 의미로 가장 알맞은 것은 무엇인가요?",
                                                    'options': ['나는 배가 고프다',
                                                                '나는 그렇게 생각하지 않는다 / 그건 아닌 것 같다',
                                                                '나는 집에 있다',
                                                                '나는 노래하고 싶다'],
                                                    'answer': '나는 그렇게 생각하지 않는다 / 그건 아닌 것 같다'},
                                                   {'q': "4. 'I think I should go'는 어떤 의미인가요?",
                                                    'options': ['나는 가야 할 것 같다',
                                                                '나는 기다려야 한다',
                                                                '나는 잠을 자야 한다',
                                                                '나는 웃어야 한다'],
                                                    'answer': '나는 가야 할 것 같다'},
                                                   {'q': "5. 'I can take a hint'의 의미로 가장 알맞은 것은 무엇인가요?",
                                                    'options': ['힌트를 줄 수 있다', '눈치를 챌 수 있다', '문을 열 수 있다', '친구를 부를 수 있다'],
                                                    'answer': '눈치를 챌 수 있다'},
                                                   {'q': "6. 'You left me utterly confused'는 어떤 의미인가요?",
                                                    'options': ['너는 나를 완전히 혼란스럽게 만들었다',
                                                                '너는 나를 아주 행복하게 만들었다',
                                                                '너는 나를 빨리 걷게 했다',
                                                                '너는 나를 도와주었다'],
                                                    'answer': '너는 나를 완전히 혼란스럽게 만들었다'},
                                                   {'q': "7. 'I am not here for you to use'는 어떤 태도를 보여 주나요?",
                                                    'options': ['자기 존중과 단호함', '장난스러움', '무관심', '운동 의지'],
                                                    'answer': '자기 존중과 단호함'},
                                                   {'q': '8. 이 노래의 관계 상황으로 가장 알맞은 것은 무엇인가요?',
                                                    'options': ['화자가 상대의 애매한 태도에 혼란을 느끼고 떠나려는 상황',
                                                                '두 사람이 함께 여행을 떠나는 상황',
                                                                '가족이 다시 만나는 상황',
                                                                '친구들이 시험을 준비하는 상황'],
                                                    'answer': '화자가 상대의 애매한 태도에 혼란을 느끼고 떠나려는 상황'}],
                                          'key_expressions': [("I don't think so", '나는 그렇게 생각하지 않아 / 그건 아닌 것 같아'),
                                                              ('I think I should go', '나는 가야 할 것 같아'),
                                                              ('Listen up', '잘 들어'),
                                                              ('Listen close', '가까이서 잘 들어'),
                                                              ('Take a hint', '눈치를 채다'),
                                                              ('Take a clue', '단서를 알아차리다'),
                                                              ('Give me the boot', '나를 쫓아내다 / 떠나게 하다'),
                                                              ('Really too nice', '정말 너무 친절한'),
                                                              ('Utterly confused', '완전히 혼란스러운'),
                                                              ('I am not here for you to use',
                                                               '나는 네가 이용하라고 여기 있는 게 아니야')],
                                          'matching': [("I don't think so", '그건 아닌 것 같아'),
                                                       ('I think I should go', '나는 가야 할 것 같아'),
                                                       ('Listen up', '잘 들어'),
                                                       ('Take a hint', '눈치를 채다'),
                                                       ('Utterly confused', '완전히 혼란스러운'),
                                                       ('I am not here for you to use', '나는 이용당하려고 여기 있는 게 아니야')],
                                          'reflect_questions': ['상대의 애매한 태도 때문에 혼란스러웠던 경험이 있나요?',
                                                                '누군가에게 단호하게 “그건 아닌 것 같아”라고 말하고 싶었던 순간이 있나요?',
                                                                '나를 지키기 위해 관계에서 선을 그어야 했던 경험이 있나요?']},
 '14. New York City - Norah Jones': {'video_url': 'https://www.youtube.com/watch?v=LpbHEO_kLwc&list=RDLpbHEO_kLwc&start_radio=1',
                                     'bg': '\n'
                                           '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#0f766e;">\n'
                                           '        🗽 New York City: 아름답지만 아픈 도시의 기억\n'
                                           '    </h3>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           '        Norah Jones의 <b>New York City</b>는 화려하고 아름다운 도시가 주는 꿈과 환상,\n'
                                           '        그리고 그 안에 숨어 있는 상처와 외로움을 함께 담고 있는 노래입니다.\n'
                                           '        제목의 <b>New York City</b>는 단순한 장소 이름이 아니라,\n'
                                           '        사람을 끌어당기지만 동시에 지치게 만드는 복잡한 감정의 공간으로 이해할 수 있습니다.\n'
                                           '    </p>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           '        노래 속 화자는 기억이 흐릿해지고, 거울 속 자신의 모습을 바라보며 과거의 일들을 떠올립니다.\n'
                                           '        사랑이 영원할 것이라고 믿고 싶었지만, 상대의 눈빛에서 빛이 사라지는 순간을 보며\n'
                                           '        어떤 사랑은 끝까지 살아남지 못한다는 사실을 깨닫습니다.\n'
                                           '    </p>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           '        반복되는 <b>such a beautiful disease</b>는 매우 인상적인 표현입니다.\n'
                                           '        New York City가 아름답지만 동시에 병처럼 사람을 아프게 할 수 있다는 의미로 볼 수 있습니다.\n'
                                           '        이 표현은 꿈, 사랑, 도시의 환상, 성공에 대한 욕망이 때로는 사람을 강하게 끌어당기면서도\n'
                                           '        상처를 남길 수 있다는 양면성을 보여 줍니다.\n'
                                           '    </p>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           "        수업에서는 <b>I can't remember</b>, <b>look in the mirror</b>, "
                                           '<b>endless love</b>,\n'
                                           '        <b>in the dead of the night</b>, <b>things could get better</b>,\n'
                                           '        <b>no regrets</b>, <b>pass me by</b>, <b>beautiful disease</b> 같은 '
                                           '표현을 중심으로 배울 수 있습니다.\n'
                                           '        또한 학생들에게 ‘꿈을 좇는 도시’, ‘아름답지만 힘들었던 경험’,\n'
                                           '        ‘겉보기와 실제가 달랐던 순간’을 주제로 생각을 적게 할 수 있습니다.\n'
                                           '    </p>\n'
                                           '    ',
                                     'lyrics': [("I can't remember what I planned tomorrow", '나는 내일 무엇을 계획했는지 기억나지 않아'),
                                                ("I can't remember when it's time to go", '언제 떠나야 하는지도 기억나지 않아'),
                                                ('When I look in the mirror', '거울을 바라볼 때'),
                                                ('Tracing lines with a pencil', '연필로 선을 따라 그리며'),
                                                ('I remember what came before', '나는 이전에 있었던 일을 기억해'),
                                                ('I wanted to think there was endless love', '나는 끝없는 사랑이 있다고 믿고 싶었어'),
                                                ('Until I saw the light dim in your eyes',
                                                 '네 눈빛에서 빛이 희미해지는 것을 보기 전까지는'),
                                                ('In the dead of the night I found out', '깊은 밤에 나는 알게 되었어'),
                                                ("Sometimes there's love that won't survive",
                                                 '때로는 살아남지 못하는 사랑도 있다는 것을'),
                                                ('New York City', '뉴욕 시티'),
                                                ('Such a beautiful disease', '참 아름다운 병 같은 곳'),
                                                ('New York City', '뉴욕 시티'),
                                                ('Such a beautiful,', '참 아름다운,'),
                                                ('Such a beautiful disease', '참 아름다운 병 같은 곳'),
                                                ('Laura kept all her disappointments', '로라는 자신의 모든 실망을 간직했어'),
                                                ('Locked up in a box behind her closet door', '옷장 문 뒤 상자 안에 잠가 둔 채로'),
                                                ('She pulled the blinds', '그녀는 블라인드를 내리고'),
                                                ('and listened to the thunder', '천둥소리를 들었어'),
                                                ('With no way out from the family store', '가족 가게에서 벗어날 길도 없이'),
                                                ('We all told her things could get better',
                                                 '우리는 모두 그녀에게 상황이 나아질 수 있다고 말했어'),
                                                ('When you just say goodbye', '그저 작별 인사를 하면 된다고'),
                                                ("I'll lay awake one more night", '나는 또 하룻밤을 잠 못 이루고 누워 있을 거야'),
                                                ('Caught in a vision I want to deny', '부정하고 싶은 환상에 사로잡힌 채'),
                                                ('And did I mention the note that I found', '그리고 내가 발견한 쪽지 이야기를 했던가'),
                                                ('Taped to my locked front door', '잠긴 현관문에 붙어 있던 쪽지'),
                                                ('It talked about no regrets', '그 쪽지에는 후회는 없다는 말이 적혀 있었어'),
                                                ('As it slipped from my hand', '그것이 내 손에서 미끄러져'),
                                                ('to the scuffed tile floor', '긁힌 타일 바닥으로 떨어졌을 때'),
                                                ('I rode the train for hours on end', '나는 몇 시간이고 계속 기차를 탔어'),
                                                ('And watched the people pass me by', '그리고 사람들이 내 곁을 지나가는 것을 바라보았어'),
                                                ('It could be that it has no end', '어쩌면 이것은 끝이 없을지도 몰라'),
                                                ("Just an action junkie's lullaby", '그저 행동에 중독된 사람의 자장가처럼'),
                                                ('New York City', '뉴욕 시티'),
                                                ('Such a beautiful disease', '참 아름다운 병 같은 곳'),
                                                ('New York City', '뉴욕 시티'),
                                                ('Such a beautiful,', '참 아름다운,'),
                                                ('Such a beautiful disease', '참 아름다운 병 같은 곳'),
                                                ('New York City', '뉴욕 시티'),
                                                ('We were full of the stuff', '우리는 그런 것들로 가득 차 있었어'),
                                                ('that every dream rested', '모든 꿈이 기대고 있던 것들로'),
                                                ('As if floating on a lumpy pillow sky', '울퉁불퉁한 베개 같은 하늘 위를 떠다니는 것처럼'),
                                                ('Caught up in the whole illusion', '그 모든 환상에 사로잡힌 채'),
                                                ('That dreams never pass us by', '꿈은 결코 우리를 지나쳐 가지 않는다는 환상에'),
                                                ('Came to a tattoed conclusion', '지워지지 않는 결론에 이르렀어'),
                                                ('That the big one was knocking on the door', '큰일이 문을 두드리고 있다는 결론에'),
                                                ('What started as a mass delusion', '집단적인 착각으로 시작된 것이'),
                                                ('Would take me far from the place I adore',
                                                 '내가 사랑하는 곳에서 나를 멀리 데려가리라는 것을'),
                                                ('New York City', '뉴욕 시티'),
                                                ('Such a beautiful disease', '참 아름다운 병 같은 곳'),
                                                ('New York City', '뉴욕 시티'),
                                                ('You are my beautiful,', '너는 나의 아름다운,'),
                                                ('Such a beautiful disease', '참 아름다운 병 같은 곳')],
                                     'quiz': [{'q': '1. 이 노래에서 반복해서 등장하는 도시는 어디인가요?',
                                               'options': ['London', 'New York City', 'Paris', 'Seoul'],
                                               'answer': 'New York City'},
                                              {'q': "2. 'I can't remember'가 반복되며 보여 주는 화자의 상태로 가장 알맞은 것은 무엇인가요?",
                                               'options': ['기억이 또렷하고 자신감 있는 상태',
                                                           '혼란스럽고 지친 상태',
                                                           '매우 신나는 상태',
                                                           '화가 나서 소리치는 상태'],
                                               'answer': '혼란스럽고 지친 상태'},
                                              {'q': "3. 'look in the mirror'의 뜻으로 가장 알맞은 것은 무엇인가요?",
                                               'options': ['거울을 보다', '창문을 열다', '문을 잠그다', '기차를 타다'],
                                               'answer': '거울을 보다'},
                                              {'q': "4. 'endless love'는 어떤 뜻인가요?",
                                               'options': ['끝없는 사랑', '짧은 여행', '깊은 잠', '낡은 가게'],
                                               'answer': '끝없는 사랑'},
                                              {'q': "5. 'in the dead of the night'의 의미로 가장 알맞은 것은 무엇인가요?",
                                               'options': ['아침 일찍', '한낮에', '깊은 밤에', '수업 시간에'],
                                               'answer': '깊은 밤에'},
                                              {'q': "6. 'things could get better'는 어떤 의미인가요?",
                                               'options': ['상황이 나아질 수 있다', '모든 것이 끝났다', '도시는 사라졌다', '기억이 완전히 없어졌다'],
                                               'answer': '상황이 나아질 수 있다'},
                                              {'q': "7. 'Such a beautiful disease'는 어떤 의미로 이해할 수 있나요?",
                                               'options': ['아름답지만 사람을 아프게 할 수 있는 것',
                                                           '완전히 건강한 상태',
                                                           '아주 쉬운 숙제',
                                                           '단순히 예쁜 건물'],
                                               'answer': '아름답지만 사람을 아프게 할 수 있는 것'},
                                              {'q': '8. 이 노래의 중심 분위기로 가장 알맞은 것은 무엇인가요?',
                                               'options': ['밝고 단순한 축하 분위기',
                                                           '도시의 아름다움과 상처가 섞인 분위기',
                                                           '운동 경기의 긴장감',
                                                           '코미디 같은 장난스러움'],
                                               'answer': '도시의 아름다움과 상처가 섞인 분위기'}],
                                     'key_expressions': [("I can't remember", '나는 기억나지 않아'),
                                                         ('Time to go', '떠날 시간'),
                                                         ('Look in the mirror', '거울을 보다'),
                                                         ('Endless love', '끝없는 사랑'),
                                                         ('The light dim in your eyes', '네 눈빛의 빛이 희미해지다'),
                                                         ('In the dead of the night', '깊은 밤에'),
                                                         ("Love that won't survive", '살아남지 못하는 사랑'),
                                                         ('Things could get better', '상황이 나아질 수 있다'),
                                                         ('No regrets', '후회 없음'),
                                                         ('Such a beautiful disease', '참 아름다운 병 같은 것')],
                                     'matching': [("I can't remember", '나는 기억나지 않아'),
                                                  ('Look in the mirror', '거울을 보다'),
                                                  ('Endless love', '끝없는 사랑'),
                                                  ('In the dead of the night', '깊은 밤에'),
                                                  ('Things could get better', '상황이 나아질 수 있다'),
                                                  ('Such a beautiful disease', '참 아름다운 병 같은 것')],
                                     'reflect_questions': ['겉으로는 아름다워 보였지만 실제로는 힘들었던 경험이 있나요?',
                                                           '꿈을 좇는 과정에서 외로움이나 혼란을 느낀 적이 있나요?',
                                                           'New York City처럼 나에게 복잡한 감정을 주는 장소가 있나요?']},
 '15. Counting Stars - OneRepublic': {'video_url': 'https://www.youtube.com/watch?v=k03uV71OP8E&list=RDk03uV71OP8E&start_radio=1',
                                      'bg': '\n'
                                            '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#f59e0b;">\n'
                                            '        🌟 Counting Stars: 돈보다 꿈을 세고 싶은 마음\n'
                                            '    </h3>\n'
                                            '\n'
                                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                            '        OneRepublic의 <b>Counting Stars</b>는 돈, 성공, 규칙적인 삶보다\n'
                                            '        자신이 진짜 꿈꾸는 삶을 따라가고 싶은 마음을 담은 노래입니다.\n'
                                            '        제목의 <b>counting stars</b>는 단순히 별을 센다는 뜻이 아니라,\n'
                                            '        돈을 세는 삶에서 벗어나 꿈과 희망을 바라보겠다는 의미로 이해할 수 있습니다.\n'
                                            '    </p>\n'
                                            '\n'
                                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                            '        노래 속 화자는 요즘 잠을 이루지 못하고,\n'
                                            '        자신과 상대가 앞으로 무엇이 될 수 있을지 계속 꿈꿉니다.\n'
                                            '        하지만 단순히 돈을 많이 버는 삶이 아니라,\n'
                                            '        더 큰 희망과 가능성을 따라가고 싶어 합니다.\n'
                                            "        그래서 <b>no more counting dollars, we'll be counting stars</b>라는 "
                                            '문장은\n'
                                            '        물질적인 성공보다 꿈과 의미를 더 중요하게 보겠다는 선언처럼 들립니다.\n'
                                            '    </p>\n'
                                            '\n'
                                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                            '        이 노래에는 <b>right</b>와 <b>wrong</b>, <b>old</b>와 <b>young</b>,\n'
                                            '        <b>money</b>와 <b>stars</b>처럼 서로 대비되는 표현이 많이 나옵니다.\n'
                                            '        화자는 세상이 시키는 대로만 사는 것에 의문을 느끼고,\n'
                                            '        때로는 자신을 힘들게 하는 경험조차 살아 있음을 느끼게 한다고 말합니다.\n'
                                            '    </p>\n'
                                            '\n'
                                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                            '        수업에서는 <b>losing sleep</b>, <b>dreaming about</b>, <b>counting '
                                            'dollars</b>,\n'
                                            "        <b>counting stars</b>, <b>seek it out</b>, <b>do what we're "
                                            'told</b>,\n'
                                            '        <b>makes me feel alive</b> 같은 표현을 중심으로 배울 수 있습니다.\n'
                                            '        또한 학생들에게 돈보다 중요하게 생각하는 것, 내가 꿈꾸는 미래,\n'
                                            '        남들이 정한 길이 아니라 내가 선택하고 싶은 길을 주제로 생각을 적게 할 수 있습니다.\n'
                                            '    </p>\n'
                                            '    ',
                                      'lyrics': [("Lately, I been, I been losin' sleep", '요즘 나는 잠을 이루지 못하고 있어'),
                                                 ("Dreamin' about the things that we could be", '우리가 될 수 있는 모습들을 꿈꾸면서'),
                                                 ("But, baby, I been, I been prayin' hard", '하지만 나는 간절히 기도해 왔어'),
                                                 ("Said, no more countin' dollars, we'll be countin' stars",
                                                  '이제 돈을 세는 대신 별을 세게 될 거라고 말했지'),
                                                 ("Yeah, we'll be countin' stars", '그래, 우리는 별을 세게 될 거야'),
                                                 ("I see this life like a swingin' vine", '나는 이 삶을 흔들리는 덩굴처럼 봐'),
                                                 ('Swing my heart across the line', '내 마음을 선 너머로 흔들어 보내'),
                                                 ("In my face is flashin' signs", '내 앞에는 신호들이 번쩍이고 있어'),
                                                 ('Seek it out and ye shall find', '찾으면 발견하게 될 거야'),
                                                 ("Old, but I'm not that old", '나이가 들었지만 그렇게 늙지는 않았어'),
                                                 ("Young, but I'm not that bold", '젊지만 그렇게 대담하지도 않아'),
                                                 ("And I don't think the world is sold",
                                                  '그리고 나는 세상이 완전히 설득되었다고 생각하지 않아'),
                                                 ("On just doin' what we're told", '그저 시키는 대로만 사는 것에 말이야'),
                                                 ("I feel somethin' so right doin' the wrong thing",
                                                  '잘못된 일을 하면서도 뭔가 너무 옳은 느낌이 들어'),
                                                 ("And I feel somethin' so wrong doin' the right thing",
                                                  '옳은 일을 하면서도 뭔가 너무 잘못된 느낌이 들어'),
                                                 ("I couldn't lie, couldn't lie, couldn't lie", '나는 거짓말할 수 없어'),
                                                 ('Everything that kills me makes me feel alive',
                                                  '나를 힘들게 하는 모든 것이 오히려 살아 있음을 느끼게 해'),
                                                 ("Lately, I been, I been losin' sleep (hey!)", '요즘 나는 잠을 이루지 못하고 있어'),
                                                 ("Dreamin' about the things that we could be", '우리가 될 수 있는 모습들을 꿈꾸면서'),
                                                 ("But, baby, I been, I been prayin' hard (hey!)", '하지만 나는 간절히 기도해 왔어'),
                                                 ("Said, no more countin' dollars, we'll be countin' stars",
                                                  '이제 돈을 세는 대신 별을 세게 될 거라고 말했지'),
                                                 ("Lately, I been, I been losin' sleep (hey!)", '요즘 나는 잠을 이루지 못하고 있어'),
                                                 ("Dreamin' about the things that we could be", '우리가 될 수 있는 모습들을 꿈꾸면서'),
                                                 ("But, baby, I been, I been prayin' hard", '하지만 나는 간절히 기도해 왔어'),
                                                 ("Said, no more countin' dollars, we'll be, we'll be countin' stars, "
                                                  'yeah',
                                                  '이제 돈을 세는 대신, 우리는 별을 세게 될 거야'),
                                                 ('I feel your love, and I feel it burn',
                                                  '나는 너의 사랑을 느끼고, 그것이 타오르는 것도 느껴'),
                                                 ('Down this river, every turn', '이 강을 따라 내려가며, 모든 굽이마다'),
                                                 ('"Hope" is our four-letter word', '"희망"은 우리에게 가장 중요한 말이야'),
                                                 ('Make that money, watch it burn', '그 돈을 벌고, 그것이 타는 것을 지켜봐'),
                                                 ("Old, but I'm not that old", '나이가 들었지만 그렇게 늙지는 않았어'),
                                                 ("Young, but I'm not that bold", '젊지만 그렇게 대담하지도 않아'),
                                                 ("And I don't think the world is sold",
                                                  '그리고 나는 세상이 완전히 설득되었다고 생각하지 않아'),
                                                 ("On just doin' what we're told", '그저 시키는 대로만 사는 것에 말이야'),
                                                 ("And I feel somethin' so wrong doin' the right thing",
                                                  '옳은 일을 하면서도 뭔가 너무 잘못된 느낌이 들어'),
                                                 ("I couldn't lie, couldn't lie, couldn't lie", '나는 거짓말할 수 없어'),
                                                 ('Everything that drowns me makes me wanna fly',
                                                  '나를 가라앉게 하는 모든 것이 오히려 날고 싶게 만들어'),
                                                 ("Lately, I been, I been losin' sleep (hey!)", '요즘 나는 잠을 이루지 못하고 있어'),
                                                 ("Dreamin' about the things that we could be", '우리가 될 수 있는 모습들을 꿈꾸면서'),
                                                 ("But, baby, I been, I been prayin' hard (hey!)", '하지만 나는 간절히 기도해 왔어'),
                                                 ("Said, no more countin' dollars, we'll be countin' stars (ooh)",
                                                  '이제 돈을 세는 대신 별을 세게 될 거라고 말했지'),
                                                 ("Lately, I been, I been losin' sleep (ooh, ooh, hey)",
                                                  '요즘 나는 잠을 이루지 못하고 있어'),
                                                 ("Dreamin' about the things that we could be (ooh, ooh)",
                                                  '우리가 될 수 있는 모습들을 꿈꾸면서'),
                                                 ("But, baby, I been, I been prayin' hard (ooh, ooh)",
                                                  '하지만 나는 간절히 기도해 왔어'),
                                                 ("Said, no more countin' dollars, we'll be, we'll be countin' stars "
                                                  '(ooh, ooh)',
                                                  '이제 돈을 세는 대신, 우리는 별을 세게 될 거야'),
                                                 ('Oh, take that money, watch it burn', '오, 그 돈을 가져가고 타는 것을 지켜봐'),
                                                 ('Sink in the river the lessons I learned', '내가 배운 교훈들을 강물 속으로 가라앉혀'),
                                                 ('Take that money, watch it burn', '그 돈을 가져가고 타는 것을 지켜봐'),
                                                 ('Sink in the river the lessons I learned', '내가 배운 교훈들을 강물 속으로 가라앉혀'),
                                                 ('Take that money, watch it burn', '그 돈을 가져가고 타는 것을 지켜봐'),
                                                 ('Sink in the river the lessons I learned', '내가 배운 교훈들을 강물 속으로 가라앉혀'),
                                                 ('Take that money, watch it burn', '그 돈을 가져가고 타는 것을 지켜봐'),
                                                 ('Sink in the river the lessons I learned', '내가 배운 교훈들을 강물 속으로 가라앉혀'),
                                                 ('Everything that kills me makes me feel alive',
                                                  '나를 힘들게 하는 모든 것이 오히려 살아 있음을 느끼게 해'),
                                                 ("Lately, I been, I been losin' sleep (hey!)", '요즘 나는 잠을 이루지 못하고 있어'),
                                                 ("Dreamin' about the things that we could be", '우리가 될 수 있는 모습들을 꿈꾸면서'),
                                                 ("But, baby, I been, I been prayin' hard (hey!)", '하지만 나는 간절히 기도해 왔어'),
                                                 ("Said, no more countin' dollars, we'll be countin' stars (ooh)",
                                                  '이제 돈을 세는 대신 별을 세게 될 거라고 말했지'),
                                                 ("Lately, I been, I been losin' sleep (ooh, ooh hey!)",
                                                  '요즘 나는 잠을 이루지 못하고 있어'),
                                                 ("Dreamin' about the things that we could be (ooh, ooh)",
                                                  '우리가 될 수 있는 모습들을 꿈꾸면서'),
                                                 ("But, baby, I been, I been prayin' hard (ooh, ooh)",
                                                  '하지만 나는 간절히 기도해 왔어'),
                                                 ("Said, no more countin' dollars, we'll be, we'll be countin' stars "
                                                  '(ooh, ooh)',
                                                  '이제 돈을 세는 대신, 우리는 별을 세게 될 거야'),
                                                 ('Take that money, watch it burn (ooh)', '그 돈을 가져가고 타는 것을 지켜봐'),
                                                 ('Sink in the river, the lessons I learned (ooh)',
                                                  '내가 배운 교훈들을 강물 속으로 가라앉혀'),
                                                 ('Take that money, watch it burn (ooh)', '그 돈을 가져가고 타는 것을 지켜봐'),
                                                 ('Sink in the river, the lessons I learned (ooh)',
                                                  '내가 배운 교훈들을 강물 속으로 가라앉혀'),
                                                 ('Take that money, watch it burn (ooh)', '그 돈을 가져가고 타는 것을 지켜봐'),
                                                 ('Sink in the river, the lessons I learned (ooh)',
                                                  '내가 배운 교훈들을 강물 속으로 가라앉혀'),
                                                 ('Take that money, watch it burn (ooh)', '그 돈을 가져가고 타는 것을 지켜봐'),
                                                 ('Sink in the river, the lessons I learned',
                                                  '내가 배운 교훈들을 강물 속으로 가라앉혀')],
                                      'quiz': [{'q': '1. 이 노래에서 화자는 요즘 무엇을 잃고 있다고 말하나요?',
                                                'options': ['돈', '잠', '친구', '길'],
                                                'answer': '잠'},
                                               {'q': '2. 화자는 무엇에 대해 꿈꾸고 있나요?',
                                                'options': ['우리가 될 수 있는 모습', '어제 먹은 음식', '학교 시험지', '비 오는 날씨'],
                                                'answer': '우리가 될 수 있는 모습'},
                                               {'q': "3. 'no more counting dollars'의 의미로 가장 알맞은 것은 무엇인가요?",
                                                'options': ['더 이상 돈만 세지 않겠다', '돈을 더 많이 세겠다', '별을 팔겠다', '잠을 자지 않겠다'],
                                                'answer': '더 이상 돈만 세지 않겠다'},
                                               {'q': "4. 'counting stars'가 상징하는 의미로 가장 알맞은 것은 무엇인가요?",
                                                'options': ['밤하늘 숙제', '꿈과 희망을 바라보는 삶', '수학 문제', '돈을 숨기는 행동'],
                                                'answer': '꿈과 희망을 바라보는 삶'},
                                               {'q': "5. 'doing what we're told'는 어떤 의미인가요?",
                                                'options': ['시키는 대로 하는 것', '노래를 크게 부르는 것', '별을 세는 것', '강을 건너는 것'],
                                                'answer': '시키는 대로 하는 것'},
                                               {'q': "6. 'Everything that kills me makes me feel alive'는 어떤 의미에 가깝나요?",
                                                'options': ['힘든 경험도 살아 있음을 느끼게 한다',
                                                            '잠을 많이 자고 싶다',
                                                            '돈이 가장 중요하다',
                                                            '아무것도 느끼지 못한다'],
                                                'answer': '힘든 경험도 살아 있음을 느끼게 한다'},
                                               {'q': '7. 이 노래의 중심 주제로 가장 알맞은 것은 무엇인가요?',
                                                'options': ['돈보다 꿈과 가능성을 좇는 삶', '시험 공부 방법', '친구와의 싸움', '도시 여행'],
                                                'answer': '돈보다 꿈과 가능성을 좇는 삶'},
                                               {'q': "8. 'Hope is our four-letter word'에서 hope의 의미는 무엇인가요?",
                                                'options': ['희망', '분노', '후회', '잠'],
                                                'answer': '희망'}],
                                      'key_expressions': [('Losing sleep', '잠을 이루지 못하다'),
                                                          ('Dreaming about', '~에 대해 꿈꾸다'),
                                                          ('Things that we could be', '우리가 될 수 있는 모습들'),
                                                          ('Praying hard', '간절히 기도하다'),
                                                          ('Counting dollars', '돈을 세다'),
                                                          ('Counting stars', '별을 세다, 꿈을 바라보다'),
                                                          ('Seek it out', '그것을 찾아내다'),
                                                          ("Do what we're told", '시키는 대로 하다'),
                                                          ('Feel alive', '살아 있음을 느끼다'),
                                                          ('Lessons I learned', '내가 배운 교훈들')],
                                      'matching': [('Losing sleep', '잠을 이루지 못하다'),
                                                   ('Counting stars', '별을 세다, 꿈을 바라보다'),
                                                   ('Counting dollars', '돈을 세다'),
                                                   ('Dreaming about the things that we could be',
                                                    '우리가 될 수 있는 모습들을 꿈꾸다'),
                                                   ("Do what we're told", '시키는 대로 하다'),
                                                   ('Everything that kills me makes me feel alive',
                                                    '힘든 경험이 오히려 살아 있음을 느끼게 하다')],
                                      'reflect_questions': ['돈보다 더 중요하다고 생각하는 꿈이나 가치는 무엇인가요?',
                                                            '남들이 시키는 대로가 아니라 내가 선택하고 싶은 길이 있나요?',
                                                            '힘들었지만 오히려 나를 성장하게 만든 경험이 있나요?']},
 '16. Fly to the Moon - Peder Elias': {'video_url': 'https://www.youtube.com/watch?v=-tnfxljOn8A&list=RD-tnfxljOn8A&start_radio=1',
                                       'bg': '\n'
                                             '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#7c3aed;">\n'
                                             '        🌙 Fly to the Moon: 작은 아이들이 큰 세상으로 날아오르는 노래\n'
                                             '    </h3>\n'
                                             '\n'
                                             '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                             '        <b>Fly to the Moon</b>는 Peder Elias의 노래로, 외롭고 작게 느껴졌던 어린 시절을 지나 '
                                             '서로의 가능성을 믿으며 더 큰 세상으로 나아가는 마음을 담고 있습니다.\n'
                                             '    </p>\n'
                                             '\n'
                                             '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                             '        노래 속 두 사람은 어릴 때 큰 세상 속의 작은 전사들처럼 살아갑니다. 혼자 학교에 가고, 외롭게 점심을 먹던 '
                                             '기억도 있지만, 시간이 흐른 뒤에는 달로 날아가고 바다를 건너며 산을 움직이는 사람들로 성장합니다.\n'
                                             '    </p>\n'
                                             '\n'
                                             '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                             "        반복되는 <b>There is nothing we can't do</b>와 <b>spread our "
                                             'wings</b>는 학생들에게 자신감과 성장의 이미지를 쉽게 전달할 수 있습니다. 특히 애벌레가 나비가 된다는 표현은 변화와 '
                                             '성장, 가능성을 상징합니다.\n'
                                             '    </p>\n'
                                             '\n'
                                             '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                             '        수업에서는 <b>fly to the moon</b>, <b>sail across the ocean</b>, '
                                             '<b>move mountains</b>, <b>spread our wings</b>, <b>There is nothing we '
                                             "can't do</b> 같은 표현을 중심으로 배울 수 있습니다. 또한 학생들에게 어린 시절의 나, 지금의 나, 앞으로 날개를 펴고 "
                                             '도전하고 싶은 일을 주제로 생각을 적게 할 수 있습니다.\n'
                                             '    </p>\n'
                                             '    ',
                                       'lyrics': [('Back when we were little kids', '우리가 어린아이였던 그때'),
                                                  ('Two warriors in a world so big', '커다란 세상 속의 두 전사였어'),
                                                  ('Hopeful eyes', '희망 가득한 눈으로'),
                                                  ('We dreamed at night', '우리는 밤마다 꿈을 꾸었어'),
                                                  ('By ourselves we walked to school', '우리끼리 학교에 걸어갔고'),
                                                  ('And ate our lunch in the bathroom', '화장실에서 점심을 먹었어'),
                                                  ('All alone', '완전히 혼자였지'),
                                                  ('But now they know', '하지만 이제 사람들도 알아'),
                                                  ('Look at us fly to the moon', '우리가 달까지 날아가는 걸 봐'),
                                                  ('See us sail across the ocean', '우리가 바다를 건너 항해하는 걸 봐'),
                                                  ('All the mountains we move', '우리가 움직이는 모든 산들을 봐'),
                                                  ('With a heart so kind and open', '친절하고 열린 마음으로'),
                                                  ('Shooting stars upon the skyline', '하늘 끝에 떠오르는 별똥별처럼'),
                                                  ('When we start to dance', '우리가 춤추기 시작할 때'),
                                                  ("Ain't nothing we can't do", '우리가 하지 못할 일은 없어'),
                                                  ('See us spread our wings and fly to the moon',
                                                   '우리가 날개를 펴고 달까지 날아가는 걸 봐'),
                                                  ("Follow rules do as you're told", '규칙을 따르고 시키는 대로 하라고 했지'),
                                                  ("And walk the path it's set in stone", '이미 정해진 길을 걸으라고 했어'),
                                                  ("It's what they said", '그게 사람들이 한 말이었어'),
                                                  ('But now instead', '하지만 이제는 달라'),
                                                  ('Look at us fly to the moon', '우리가 달까지 날아가는 걸 봐'),
                                                  ('See us sail across the ocean', '우리가 바다를 건너 항해하는 걸 봐'),
                                                  ('All the mountains we move', '우리가 움직이는 모든 산들을 봐'),
                                                  ('With a heart so kind and open', '친절하고 열린 마음으로'),
                                                  ('Shooting stars upon the skyline', '하늘 끝에 떠오르는 별똥별처럼'),
                                                  ('When we start to dance', '우리가 춤추기 시작할 때'),
                                                  ("Ain't nothing we can't do", '우리가 하지 못할 일은 없어'),
                                                  ('See us spread our wings and fly to the moon',
                                                   '우리가 날개를 펴고 달까지 날아가는 걸 봐'),
                                                  ('Look at us fly to the moon', '우리가 달까지 날아가는 걸 봐'),
                                                  ('See us dance into the fire', '우리가 불꽃 속으로 춤추며 들어가는 걸 봐'),
                                                  ('What a wonderful view', '정말 멋진 풍경이야'),
                                                  ('We just keep on going in higher', '우리는 계속 더 높이 올라가'),
                                                  ("For every little caterpillar, there's a butterfly",
                                                   '모든 작은 애벌레에게는 나비가 될 가능성이 있어'),
                                                  ("There's nothing we can't do", '우리가 할 수 없는 것은 없어'),
                                                  ('See us spread our wings and fly to the moon',
                                                   '우리가 날개를 펴고 달까지 날아가는 걸 봐')],
                                       'quiz': [{'q': '1. 이 노래에서 어린 시절 두 사람은 무엇처럼 표현되나요?',
                                                 'options': ['두 전사', '두 선생님', '두 별', '두 여행자'],
                                                 'answer': '두 전사'},
                                                {'q': '2. 두 사람은 어린 시절 어디에서 점심을 먹었다고 하나요?',
                                                 'options': ['교실', '운동장', '화장실', '도서관'],
                                                 'answer': '화장실'},
                                                {'q': '3. 후렴에서 두 사람은 어디까지 날아간다고 하나요?',
                                                 'options': ['태양', '달', '바다', '산'],
                                                 'answer': '달'},
                                                {'q': '4. See us sail across the ocean의 의미로 알맞은 것은?',
                                                 'options': ['우리가 바다를 건너 항해하는 걸 봐',
                                                             '우리가 산을 오르는 걸 봐',
                                                             '우리가 학교에 가는 걸 봐',
                                                             '우리가 별을 세는 걸 봐'],
                                                 'answer': '우리가 바다를 건너 항해하는 걸 봐'},
                                                {'q': '5. 사람들이 하라고 했던 것은 무엇인가요?',
                                                 'options': ['규칙을 따르고 정해진 길을 걷기', '춤을 추고 노래하기', '바다를 건너기', '달까지 날아가기'],
                                                 'answer': '규칙을 따르고 정해진 길을 걷기'},
                                                {'q': '6. Ain’t nothing we can’t do의 뜻으로 가장 알맞은 것은?',
                                                 'options': ['우리는 아무것도 할 수 없다',
                                                             '우리가 하지 못할 일은 없다',
                                                             '우리는 지금 잠을 자고 있다',
                                                             '우리는 길을 잃었다'],
                                                 'answer': '우리가 하지 못할 일은 없다'},
                                                {'q': '7. 애벌레와 나비의 이미지는 무엇을 상징하나요?',
                                                 'options': ['실패와 포기', '변화와 성장', '규칙과 명령', '외로움과 두려움'],
                                                 'answer': '변화와 성장'},
                                                {'q': '8. 이 노래의 중심 메시지로 가장 알맞은 것은?',
                                                 'options': ['정해진 길만 따라야 한다',
                                                             '혼자 있으면 아무것도 할 수 없다',
                                                             '우리는 성장하며 더 큰 가능성으로 나아갈 수 있다',
                                                             '어린 시절은 항상 행복하기만 하다'],
                                                 'answer': '우리는 성장하며 더 큰 가능성으로 나아갈 수 있다'}],
                                       'key_expressions': [('Back when we were little kids', '우리가 어린아이였던 그때'),
                                                           ('Two warriors', '두 전사'),
                                                           ('Hopeful eyes', '희망 가득한 눈'),
                                                           ('Fly to the moon', '달까지 날아가다'),
                                                           ('Sail across the ocean', '바다를 건너 항해하다'),
                                                           ('Move mountains', '큰 어려움을 해내다'),
                                                           ('A heart so kind and open', '친절하고 열린 마음'),
                                                           ('Do as you are told', '시키는 대로 하다'),
                                                           ('Spread our wings', '날개를 펴다 / 도전하다'),
                                                           ("There is nothing we can't do", '우리가 할 수 없는 것은 없다')],
                                       'matching': [('Fly to the moon', '달까지 날아가다'),
                                                    ('Sail across the ocean', '바다를 건너 항해하다'),
                                                    ('Move mountains', '큰 어려움을 해내다'),
                                                    ('Spread our wings', '날개를 펴다 / 도전하다'),
                                                    ('Do as you are told', '시키는 대로 하다'),
                                                    ("There is nothing we can't do", '우리가 할 수 없는 것은 없다')],
                                       'reflect_questions': ['어릴 때는 외롭거나 작게 느껴졌지만 지금은 성장했다고 느끼는 경험이 있나요?',
                                                             '남들이 정해 준 길이 아니라 내가 선택하고 싶은 길은 무엇인가요?',
                                                             '앞으로 내가 날개를 펴고 도전하고 싶은 일은 무엇인가요?']},
 '17. My Universe - Coldplay X BTS': {'video_url': 'https://www.youtube.com/watch?v=MjHD7jTgV9s&list=RDMjHD7jTgV9s&start_radio=1',
                                      'bg': '\n'
                                            '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#2563eb;">\n'
                                            '        🌌 My Universe: 서로 다른 세계가 만나 하나의 우주가 되는 노래\n'
                                            '    </h3>\n'
                                            '\n'
                                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                            '        <b>My Universe</b>는 Coldplay와 BTS가 함께 부른 노래로, 서로 다른 배경과 세계를 가진 '
                                            '사람들이 사랑과 믿음으로 연결되는 마음을 담고 있습니다.\n'
                                            '    </p>\n'
                                            '\n'
                                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                            '        노래 속 화자는 상대를 자신의 우주라고 부릅니다. 밤에는 상대를 올려다보고, 아침에는 상대가 떠오르는 모습을 '
                                            '바라보며, 상대가 자신의 세상을 밝게 만들어 준다고 말합니다.\n'
                                            '    </p>\n'
                                            '\n'
                                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                            '        특히 <b>we come from different sides</b>라는 표현은 서로 다른 편, 다른 배경, 다른 '
                                            '세계에서 왔지만 함께하고 싶은 마음을 보여 줍니다. 그래서 이 노래는 차이와 장벽을 넘어 서로를 소중히 여기는 메시지를 '
                                            '전달합니다.\n'
                                            '    </p>\n'
                                            '\n'
                                            '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                            '        수업에서는 <b>my universe</b>, <b>put you first</b>, <b>light up '
                                            'inside</b>, <b>different sides</b>, <b>made of each other</b> 같은 표현을 중심으로 '
                                            '배울 수 있습니다. 학생들에게 나의 세상을 밝혀 주는 사람이나 서로 다른 사람과 함께하는 경험을 생각하게 할 수 있습니다.\n'
                                            '    </p>\n'
                                            '    ',
                                      'lyrics': [('You (you), you are (you are) my universe', '너는, 너는 나의 우주야'),
                                                 ('And I (I) just want (just want) to put you first',
                                                  '그리고 나는 너를 가장 먼저 생각하고 싶어'),
                                                 ('And you (you), you are (you are) my universe, and I',
                                                  '그리고 너는 나의 우주야, 그리고 나는'),
                                                 ('In the night, I lie and look up at you', '밤이 되면 나는 누워서 너를 올려다봐'),
                                                 ('When the morning comes, I watch you rise',
                                                  '아침이 오면 나는 네가 떠오르는 모습을 바라봐'),
                                                 ("There's a paradise they couldn't capture", '그들이 담아낼 수 없는 낙원이 있어'),
                                                 ('That bright infinity inside your eyes', '너의 눈 안에 있는 밝은 무한함'),
                                                 ('매일 밤 네게 날아가 (가)', '매일 밤 너에게 날아가'),
                                                 ('꿈이란 것도 잊은 채', '꿈이라는 것도 잊은 채'),
                                                 ('나 웃으며 너를 만나 (나)', '나는 웃으며 너를 만나'),
                                                 ('Never ending forever, baby', '끝없이 영원히, baby'),
                                                 ('You (you), you are (you are) my universe', '너는, 너는 나의 우주야'),
                                                 ('And I (I) just want (just want) to put you first',
                                                  '그리고 나는 너를 가장 먼저 생각하고 싶어'),
                                                 ('And you (you), you are (you are) my universe', '그리고 너는 나의 우주야'),
                                                 ('And you make my world light up inside', '그리고 너는 내 세상을 안에서부터 밝혀 줘'),
                                                 ('어둠이 내겐 더 편했었지', '어둠이 내게는 더 편했었지'),
                                                 ('길어진 그림자 속에서 (eyes)', '길어진 그림자 속에서'),
                                                 ("And they said that we can't be together",
                                                  '그리고 그들은 우리가 함께할 수 없다고 말했어'),
                                                 ('Because, because we come from different sides',
                                                  '왜냐하면 우리는 서로 다른 편에서 왔기 때문이야'),
                                                 ('You (you), you are (you are) my universe', '너는, 너는 나의 우주야'),
                                                 ('And I (I) just want (just want) to put you first',
                                                  '그리고 나는 너를 가장 먼저 생각하고 싶어'),
                                                 ('And you (you), you are (you are) my universe', '그리고 너는 나의 우주야'),
                                                 ('And you make my world light up inside', '그리고 너는 내 세상을 안에서부터 밝혀 줘'),
                                                 ('My universe (doo-doo, doo-doo)', '나의 우주'),
                                                 ('My universe (doo-doo, doo-doo)', '나의 우주'),
                                                 ('My universe (doo-doo, doo-doo)', '나의 우주'),
                                                 ('(You make my world)', '너는 내 세상을'),
                                                 ('You make my world light up inside', '너는 내 세상을 안에서부터 밝혀 줘'),
                                                 ('Make my world light up inside', '내 세상을 안에서부터 밝혀 줘'),
                                                 ('나를 밝혀주는 건', '나를 밝혀 주는 것은'),
                                                 ('너란 사랑으로 수 놓아진 별', '너라는 사랑으로 수놓아진 별'),
                                                 ('내 우주의 넌', '내 우주 속의 너는'),
                                                 ('또 다른 세상을 만들어 주는 걸', '또 다른 세상을 만들어 줘'),
                                                 ('너는 내 별이자 나의 우주니까', '너는 내 별이자 나의 우주니까'),
                                                 ('지금 이 시련도 결국엔 잠시니까', '지금 이 시련도 결국에는 잠시니까'),
                                                 ('너는 언제까지나 지금처럼 밝게만 빛나줘', '너는 언제까지나 지금처럼 밝게만 빛나 줘'),
                                                 ('우리는 너를 따라 이 긴 밤을 수놓을 거야', '우리는 너를 따라 이 긴 밤을 수놓을 거야'),
                                                 ('너와 함께 날아가 (가)', '너와 함께 날아가'),
                                                 ("When I'm without you, I'm crazy", '내가 너 없이 있으면 나는 미칠 것 같아'),
                                                 ('자 어서 내 손을 잡아 (아)', '자, 어서 내 손을 잡아'),
                                                 ('We are made of each other, baby', '우리는 서로로 이루어져 있어, baby'),
                                                 ('You (you), you are (you are) my universe', '너는, 너는 나의 우주야'),
                                                 ('And I (I) just want (just want) to put you first',
                                                  '그리고 나는 너를 가장 먼저 생각하고 싶어'),
                                                 ('And you (you), you are (you are) my universe', '그리고 너는 나의 우주야'),
                                                 ('And you make my world light up inside', '그리고 너는 내 세상을 안에서부터 밝혀 줘'),
                                                 ('My universe (you, you are)', '나의 우주, 너는'),
                                                 ('My universe (I just want)', '나의 우주, 나는 원해'),
                                                 ('My universe (you, you are my universe, and I)',
                                                  '나의 우주, 너는 나의 우주야, 그리고 나는'),
                                                 ('My universe', '나의 우주')],
                                      'quiz': [{'q': '1. 이 노래에서 상대는 무엇으로 표현되나요?',
                                                'options': ['나의 우주', '나의 바다', '나의 길', '나의 학교'],
                                                'answer': '나의 우주'},
                                               {'q': '2. 화자는 밤에 무엇을 한다고 하나요?',
                                                'options': ['누워서 상대를 올려다본다', '바다를 건넌다', '학교에 간다', '편지를 쓴다'],
                                                'answer': '누워서 상대를 올려다본다'},
                                               {'q': '3. When the morning comes의 의미로 알맞은 것은?',
                                                'options': ['아침이 오면', '밤이 깊어지면', '비가 내리면', '노래가 끝나면'],
                                                'answer': '아침이 오면'},
                                               {'q': '4. And I just want to put you first의 뜻으로 알맞은 것은?',
                                                'options': ['나는 너를 가장 먼저 생각하고 싶어',
                                                            '나는 너를 잊고 싶어',
                                                            '나는 먼저 집에 가고 싶어',
                                                            '나는 혼자 있고 싶어'],
                                                'answer': '나는 너를 가장 먼저 생각하고 싶어'},
                                               {'q': '5. 상대는 화자의 세상을 어떻게 만든다고 하나요?',
                                                'options': ['안에서부터 밝게 만든다', '조용하게 만든다', '멀어지게 만든다', '어둡게 만든다'],
                                                'answer': '안에서부터 밝게 만든다'},
                                               {'q': '6. 사람들이 두 사람이 함께할 수 없다고 말한 이유는 무엇인가요?',
                                                'options': ['서로 다른 편에서 왔기 때문에',
                                                            '서로 말을 하지 않기 때문에',
                                                            '서로 노래를 모르게 때문에',
                                                            '서로 같은 학교가 아니기 때문에'],
                                                'answer': '서로 다른 편에서 왔기 때문에'},
                                               {'q': '7. We are made of each other의 의미로 가장 알맞은 것은?',
                                                'options': ['우리는 서로로 이루어져 있다',
                                                            '우리는 서로를 모른다',
                                                            '우리는 서로 멀리 있다',
                                                            '우리는 서로 경쟁한다'],
                                                'answer': '우리는 서로로 이루어져 있다'},
                                               {'q': '8. 이 노래의 중심 메시지로 가장 알맞은 것은?',
                                                'options': ['서로 다른 세계의 사람도 사랑과 믿음으로 연결될 수 있다',
                                                            '혼자 있는 것이 가장 편하다',
                                                            '아침에는 항상 운동을 해야 한다',
                                                            '다른 사람과 함께할 수 없다'],
                                                'answer': '서로 다른 세계의 사람도 사랑과 믿음으로 연결될 수 있다'}],
                                      'key_expressions': [('My universe', '나의 우주'),
                                                          ('Put you first', '너를 가장 먼저 생각하다'),
                                                          ('In the night', '밤에'),
                                                          ('When the morning comes', '아침이 오면'),
                                                          ("There's a paradise", '낙원이 있다'),
                                                          ('Light up inside', '안에서부터 밝히다'),
                                                          ('Different sides', '서로 다른 편'),
                                                          ('Without you', '너 없이'),
                                                          ('Take my hand', '내 손을 잡아'),
                                                          ('Made of each other', '서로로 이루어진')],
                                      'matching': [('My universe', '나의 우주'),
                                                   ('Put you first', '너를 가장 먼저 생각하다'),
                                                   ('When the morning comes', '아침이 오면'),
                                                   ('Light up inside', '안에서부터 밝히다'),
                                                   ('Different sides', '서로 다른 편'),
                                                   ('Made of each other', '서로로 이루어진')],
                                      'reflect_questions': ['나의 세상을 밝게 만들어 주는 사람이나 존재가 있나요?',
                                                            '서로 다른 배경을 가진 사람과 가까워진 경험이 있나요?',
                                                            '내가 가장 먼저 소중히 여기고 싶은 사람이나 가치는 무엇인가요?']},
 '18. Golden - KPop Demon Hunters': {'video_url': 'https://www.youtube.com/watch?v=-NXmMj7RQUc&list=RD-NXmMj7RQUc&start_radio=1',
                                     'bg': '\n'
                                           '    <h3 style="font-size:2.2rem; margin-bottom:20px; color:#ca8a04;">\n'
                                           '        ✨ Golden: 숨어 있던 나를 드러내고 빛나는 노래\n'
                                           '    </h3>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           '        <b>Golden</b>은 어둡고 외로웠던 과거를 지나, 이제는 자신의 목소리와 존재를 숨기지 않고 빛나겠다고 말하는 노래입니다.\n'
                                           '    </p>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           '        노래 속 화자는 예전에는 ghost처럼 혼자였고, 자신의 자리를 찾지 못했습니다. 하지만 이제는 숨는 것을 멈추고 무대 위에서 자신이 태어난 모습대로 빛나려 합니다.\n'
                                           '    </p>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           '        반복되는 <b>gonna be golden</b>은 앞으로 더 밝고 단단한 존재가 되겠다는 다짐입니다. <b>no fear, no lies</b>는 두려움과 거짓 없이 진짜 나로 살아가겠다는 의미로 볼 수 있습니다.\n'
                                           '    </p>\n'
                                           '\n'
                                           '    <p style="font-size:1.35rem; line-height:2.0; color:#1e293b;">\n'
                                           '        수업에서는 <b>ghost</b>, <b>alone</b>, <b>throne</b>, <b>queen</b>, <b>done hiding</b>, <b>shining</b>, <b>golden</b>, <b>born to be</b> 같은 표현을 중심으로 배울 수 있습니다. 학생들에게 숨기고 싶었던 모습, 자신감을 되찾은 순간, 앞으로 빛나고 싶은 나의 모습을 생각하게 할 수 있습니다.\n'
                                           '    </p>\n'
                                           '    ',
                                     'lyrics': [('I was a ghost, I was alone, hah', '나는 유령 같았고, 혼자였어'),
                                                ('어두워진, hah, 앞길속에 (Ah)', '어두워진 앞길 속에서'),
                                                ("Given the throne, I didn't know how to believe", '왕좌를 받았지만, 어떻게 믿어야 할지 몰랐어'),
                                                ("I was the queen that I'm meant to be", '나는 원래 되어야 했던 여왕이었어'),
                                                ('I lived two lives, tried to play both sides', '나는 두 삶을 살며 양쪽 모두를 맞추려 했어'),
                                                ("But I couldn't find my own place", '하지만 내 자리를 찾을 수 없었어'),
                                                ("Called a problem child 'cause I got too wild", '너무 거칠다고 문제아라고 불렸어'),
                                                ("But now that's how I'm getting paid, 끝없이 on stage", '하지만 이제 그 모습으로 인정받고 있어, 끝없이 무대 위에서'),
                                                ("I'm done hidin', now I'm shinin' like I'm born to be", '나는 더 이상 숨지 않아, 태어난 모습대로 빛나고 있어'),
                                                ("We dreamin' hard, we came so far, now I believe", '우리는 크게 꿈꿨고, 여기까지 왔고, 이제 나는 믿어'),
                                                ("We're goin' up, up, up, it's our moment", '우리는 올라가고 있어, 지금이 우리의 순간이야'),
                                                ("You know together we're glowing", '알잖아, 함께라서 우리는 빛나고 있어'),
                                                ('Gonna be, gonna be golden', '우리는 빛나는 존재가 될 거야'),
                                                ('Oh, up, up, up with our voices', '우리의 목소리로 더 높이 올라가'),
                                                ('영원히 깨질 수 없는', '영원히 깨질 수 없는'),
                                                ('Gonna be, gonna be golden', '우리는 빛나는 존재가 될 거야'),
                                                ("Oh, I'm done hidin' now I'm shinin' like I'm born to be", '나는 더 이상 숨지 않아, 태어난 모습대로 빛나고 있어'),
                                                ('Oh, our time, no fear, no lies', '지금은 우리의 시간, 두려움도 거짓도 없어'),
                                                ("That's who we're born to be", '그것이 우리가 원래 태어난 모습이야'),
                                                ('Waited so long to break these walls down', '이 벽들을 무너뜨리기 위해 오랫동안 기다렸어'),
                                                ('To wake up and feel like me', '깨어나서 진짜 나처럼 느끼기 위해'),
                                                ('Put these patterns all in the past now', '이제 이런 반복된 모습을 모두 과거에 두고'),
                                                ('And finally live like the girl they all see', '마침내 모두가 보는 그 소녀처럼 살아가'),
                                                ("No more hiding, I'll be shining like I'm born to be", '더 이상 숨지 않아, 태어난 모습대로 빛날 거야'),
                                                ("'Cause we are hunters, voices strong, and I know I believe", '우리는 헌터이고, 목소리는 강하며, 나는 믿어'),
                                                ("We're goin' up, up, up, it's our moment", '우리는 올라가고 있어, 지금이 우리의 순간이야'),
                                                ("You know together we're glowing", '알잖아, 함께라서 우리는 빛나고 있어'),
                                                ('Gonna be, gonna be golden', '우리는 빛나는 존재가 될 거야'),
                                                ('Oh, up, up, up, with our voices', '우리의 목소리로 더 높이 올라가'),
                                                ('영원히 깨질 수 없는', '영원히 깨질 수 없는'),
                                                ('Gonna be, gonna be golden', '우리는 빛나는 존재가 될 거야'),
                                                ("Oh, I'm done hidin', now I'm shining like I'm born to be", '나는 더 이상 숨지 않아, 태어난 모습대로 빛나고 있어'),
                                                ('Oh, our time, no fears, no lies', '지금은 우리의 시간, 두려움도 거짓도 없어'),
                                                ("That's who we're born to be", '그것이 우리가 원래 태어난 모습이야'),
                                                ("You know we're gonna be, gonna be golden", '알잖아, 우리는 빛나는 존재가 될 거야'),
                                                ("We're gonna be, gonna be", '우리는 그렇게 될 거야'),
                                                ("Born to be, born to be glowin'", '빛나도록 태어났어'),
                                                ('밝게 빛나는 우린', '밝게 빛나는 우리는'),
                                                ("You know that it's our time, no fears, no lies", '알잖아, 지금은 우리의 시간, 두려움도 거짓도 없어'),
                                                ("That's who we're born to be", '그것이 우리가 원래 태어난 모습이야')],
                                     'quiz': [{'q': '1. 화자는 처음에 자신을 무엇 같다고 표현하나요?',
                                               'options': ['유령', '별', '왕자', '학생'],
                                               'answer': '유령'},
                                              {'q': '2. 화자는 무엇을 받았지만 믿는 방법을 몰랐다고 하나요?',
                                               'options': ['왕좌', '편지', '지도', '책'],
                                               'answer': '왕좌'},
                                              {'q': '3. 화자는 자신이 원래 어떤 존재였다고 말하나요?',
                                               'options': ['여왕', '선생님', '여행자', '가수만'],
                                               'answer': '여왕'},
                                              {'q': '4. I could not find my own place의 뜻으로 알맞은 것은?',
                                               'options': ['내 자리를 찾을 수 없었다', '내 집을 샀다', '내 길을 다 외웠다', '내 친구를 만났다'],
                                               'answer': '내 자리를 찾을 수 없었다'},
                                              {'q': '5. 이제 화자는 숨는 것을 멈추고 어떻게 된다고 하나요?',
                                               'options': ['빛난다', '잠든다', '떠난다', '잊는다'],
                                               'answer': '빛난다'},
                                              {'q': '6. We came so far의 의미로 알맞은 것은?',
                                               'options': ['우리는 여기까지 왔다', '우리는 멀리 가지 않았다', '우리는 다시 시작하지 않았다', '우리는 집에 있었다'],
                                               'answer': '우리는 여기까지 왔다'},
                                              {'q': '7. gonna be golden의 의미로 가장 알맞은 것은?',
                                               'options': ['빛나는 존재가 될 것이다', '금으로 물건을 살 것이다', '혼자 숨어 있을 것이다', '다시 과거로 갈 것이다'],
                                               'answer': '빛나는 존재가 될 것이다'},
                                              {'q': '8. 이 노래의 중심 메시지로 가장 알맞은 것은?',
                                               'options': ['두려움 없이 진짜 나로 빛나자는 마음', '항상 혼자 숨어 있어야 한다는 마음', '과거만 계속 생각하자는 마음', '목소리를 숨겨야 한다는 마음'],
                                               'answer': '두려움 없이 진짜 나로 빛나자는 마음'}],
                                     'key_expressions': [('I was alone', '나는 혼자였어'),
                                                         ('Given the throne', '왕좌를 받았지만'),
                                                         ('Meant to be', '원래 그렇게 될 운명의'),
                                                         ('Find my own place', '내 자리를 찾다'),
                                                         ('Problem child', '문제아'),
                                                         ("I'm done hiding", '나는 숨는 것을 끝냈어'),
                                                         ("I'm shining", '나는 빛나고 있어'),
                                                         ("It's our moment", '지금은 우리의 순간이야'),
                                                         ('Gonna be golden', '빛나는 존재가 될 거야'),
                                                         ('No fear, no lies', '두려움도 거짓도 없이')],
                                     'matching': [('I was alone', '나는 혼자였어'),
                                                  ('Given the throne', '왕좌를 받았지만'),
                                                  ('Find my own place', '내 자리를 찾다'),
                                                  ("I'm done hiding", '나는 숨는 것을 끝냈어'),
                                                  ('Gonna be golden', '빛나는 존재가 될 거야'),
                                                  ('No fear, no lies', '두려움도 거짓도 없이')],
                                     'reflect_questions': ['내가 예전에는 숨기고 싶었지만 이제는 드러내고 싶은 모습이 있나요?',
                                                           '내가 내 자리를 찾았다고 느낀 순간이나 앞으로 찾고 싶은 자리는 무엇인가요?',
                                                           '앞으로 내가 golden처럼 빛나고 싶은 모습은 어떤 모습인가요?']},
 '19. Cowboy in LA - LANY': {'video_url': 'https://www.youtube.com/watch?v=_P0XDjaZAAA&list=RD_P0XDjaZAAA&start_radio=1',
                             'lyrics': [('Palm trees, square dancing under the moon', '야자수, 달빛 아래에서 추는 스퀘어 댄스'),
                                        ("Sunsets, they ain't got nothing on you", '노을도 너와는 비교가 안 돼'),
                                        ("And the purple in the sky ain't as pretty as your eyes", '하늘의 보랏빛도 네 눈만큼 예쁘지는 않아'),
                                        ('Tell me what I gotta do', '내가 뭘 해야 하는지 말해 줘'),
                                        ("When you're with me it's better than Malibu", '네가 나와 함께 있으면 말리부보다 더 좋아'),
                                        ("Let's skip the club, let's skip the crowd", '클럽은 건너뛰고, 사람 많은 곳도 피하자'),
                                        ('Wanna take you on a date', '너를 데이트에 데려가고 싶어'),
                                        ("I'll hold your hand, I'll hold the door", '네 손을 잡아 주고, 문도 잡아 줄게'),
                                        ("'Cause that's how I was raised", '왜냐하면 나는 그렇게 자랐으니까'),
                                        ('And all the other boys in town all look and talk the same', '이 도시의 다른 남자들은 모두 비슷하게 보이고 말해'),
                                        ('But I got a different kind of heart', '하지만 나는 다른 마음을 가지고 있어'),
                                        ("I'm a cowboy", '나는 카우보이야'),
                                        ('A cowboy in LA', 'LA에 있는 카우보이'),
                                        ('Thunder, pickups and cheap gasoline', '천둥, 픽업트럭, 그리고 싼 휘발유'),
                                        ("Lightning, best show that I've ever seen", '번개, 내가 본 최고의 쇼'),
                                        ('And you get up every day and you work hard for your pay', '너는 매일 일어나 월급을 위해 열심히 일해'),
                                        ('Happy in a pair of jeans', '청바지 한 벌에도 행복해하지'),
                                        ('Oklahoma, it made a man out of me', '오클라호마는 나를 진짜 어른으로 만들어 줬어'),
                                        ("Let's skip the club, let's skip the crowd", '클럽은 건너뛰고, 사람 많은 곳도 피하자'),
                                        ('Wanna take you on a date', '너를 데이트에 데려가고 싶어'),
                                        ("I'll hold your hand, I'll hold the door", '네 손을 잡아 주고, 문도 잡아 줄게'),
                                        ("'Cause that's how I was raised", '왜냐하면 나는 그렇게 자랐으니까'),
                                        ('Yeah, all the other boys in town all look and talk the same',
                                         '그래, 이 도시의 다른 남자들은 모두 비슷하게 보이고 말해'),
                                        ('But I got a different kind of heart', '하지만 나는 다른 마음을 가지고 있어'),
                                        ("I'm a cowboy", '나는 카우보이야'),
                                        ('A cowboy in LA', 'LA에 있는 카우보이'),
                                        ('And we can take it slow', '그리고 우리는 천천히 해도 돼'),
                                        ("This ain't a rodeo", '이건 로데오가 아니야'),
                                        ('I can show you something new', '나는 너에게 새로운 것을 보여 줄 수 있어'),
                                        ("Let's skip the club, let's skip the crowd", '클럽은 건너뛰고, 사람 많은 곳도 피하자'),
                                        ('Wanna take you on a date', '너를 데이트에 데려가고 싶어'),
                                        ("I'll hold your hand, I'll hold the door", '네 손을 잡아 주고, 문도 잡아 줄게'),
                                        ("'Cause that's how I was raised", '왜냐하면 나는 그렇게 자랐으니까'),
                                        ("And all the other girls in town won't look at you the same",
                                         '이 도시의 다른 여자들은 너를 같은 방식으로 보지 않을 거야'),
                                        ("'Cause I got a different kind of heart", '왜냐하면 나는 다른 마음을 가지고 있으니까'),
                                        ("I'm a cowboy", '나는 카우보이야'),
                                        ('They got a cowboy in LA', '그들에게는 LA의 카우보이가 있어'),
                                        ('A cowboy in LA', 'LA에 있는 카우보이'),
                                        ('Palm trees, square dancing under the moon', '야자수, 달빛 아래에서 추는 스퀘어 댄스')],
                             'quiz': [{'q': '1. 이 노래에서 화자는 자신을 무엇이라고 표현하나요?',
                                       'options': ['a cowboy in LA',
                                                   'a singer in New York',
                                                   'a dancer in Malibu',
                                                   'a driver in Oklahoma'],
                                       'answer': 'a cowboy in LA'},
                                      {'q': "2. 'Let's skip the club, let's skip the crowd'의 의미로 알맞은 것은?",
                                       'options': ['클럽과 사람 많은 곳은 피하자', '클럽에서 춤추자', '모두를 초대하자', '혼자 집에 있자'],
                                       'answer': '클럽과 사람 많은 곳은 피하자'},
                                      {'q': '3. 화자는 상대에게 무엇을 하고 싶어 하나요?',
                                       'options': ['데이트에 데려가고 싶어 한다', '차를 팔고 싶어 한다', '노래를 멈추고 싶어 한다', '도시를 떠나고 싶어 한다'],
                                       'answer': '데이트에 데려가고 싶어 한다'},
                                      {'q': "4. 'I'll hold your hand, I'll hold the door'가 보여 주는 태도는?",
                                       'options': ['상대를 배려하고 예의 있게 대하는 태도', '상대를 무시하는 태도', '혼자 있고 싶은 태도', '서두르는 태도'],
                                       'answer': '상대를 배려하고 예의 있게 대하는 태도'},
                                      {'q': "5. 'that's how I was raised'의 뜻으로 알맞은 것은?",
                                       'options': ['나는 그렇게 자랐다', '나는 길을 잃었다', '나는 춤을 배웠다', '나는 도시를 싫어한다'],
                                       'answer': '나는 그렇게 자랐다'},
                                      {'q': '6. Oklahoma made a man out of me의 의미로 알맞은 것은?',
                                       'options': ['오클라호마가 나를 성숙하게 만들었다', '오클라호마가 나를 LA로 보냈다', '오클라호마가 나를 유명하게 만들었다', '오클라호마가 나를 춤추게 했다'],
                                       'answer': '오클라호마가 나를 성숙하게 만들었다'},
                                      {'q': "7. This ain't a rodeo가 암시하는 분위기로 알맞은 것은?",
                                       'options': ['서두르지 않고 천천히 가도 된다는 분위기', '위험하게 경쟁해야 한다는 분위기', '말을 타야 한다는 뜻만 있다', '모두가 화난 분위기'],
                                       'answer': '서두르지 않고 천천히 가도 된다는 분위기'},
                                      {'q': '8. 이 노래의 중심 메시지로 가장 알맞은 것은?',
                                       'options': ['화려함보다 진심과 배려가 더 중요하다는 마음',
                                                   '항상 클럽에 가야 한다는 마음',
                                                   '도시를 무조건 떠나야 한다는 마음',
                                                   '모두가 똑같이 행동해야 한다는 마음'],
                                       'answer': '화려함보다 진심과 배려가 더 중요하다는 마음'}],
                             'key_expressions': [('square dancing', '스퀘어 댄스'),
                                                 ("ain't got nothing on you", '너와는 비교가 안 돼'),
                                                 ('Tell me what I gotta do', '내가 뭘 해야 하는지 말해 줘'),
                                                 ("Let's skip the club", '클럽은 건너뛰자'),
                                                 ('skip the crowd', '사람 많은 곳을 피하다'),
                                                 ('take you on a date', '너를 데이트에 데려가다'),
                                                 ('hold the door', '문을 잡아 주다'),
                                                 ('how I was raised', '내가 자란 방식'),
                                                 ('a different kind of heart', '다른 종류의 마음'),
                                                 ('take it slow', '천천히 하다')],
                             'matching': [("ain't got nothing on you", '너와는 비교가 안 돼'),
                                          ("Let's skip the club", '클럽은 건너뛰자'),
                                          ('take you on a date', '너를 데이트에 데려가다'),
                                          ('hold the door', '문을 잡아 주다'),
                                          ('a different kind of heart', '다른 종류의 마음'),
                                          ('take it slow', '천천히 하다')],
                             'reflect_questions': ['화려한 장소보다 조용하고 진심 있는 시간이 더 좋았던 경험이 있나요?',
                                                   '내가 누군가에게 예의나 배려를 보여 줄 수 있는 작은 행동은 무엇인가요?',
                                                   '다른 사람들과 조금 다르지만 내가 소중하게 생각하는 나만의 마음이나 태도는 무엇인가요?']}}

BACKGROUND_CONTENT = {'1. Let It Go - Frozen OST': {'title': '❄️ Let It Go: 숨겨 왔던 자신을 받아들이는 순간',
                               'paragraphs': ['Let It Go는 영화 Frozen의 대표곡으로, 엘사가 더 이상 자신의 능력과 감정을 숨기지 않고 스스로를 받아들이는 '
                                              '장면에서 나오는 노래입니다. 엘사는 왕국의 공주이지만, 자신의 얼음 마법이 다른 사람을 다치게 할 수 있다는 두려움 때문에 늘 '
                                              '조심하며 살아왔습니다.',
                                              '어릴 때부터 엘사는 감정을 숨기고, 능력을 감추고, ‘착한 아이’처럼 행동해야 한다는 압박을 받았습니다. 하지만 대관식 날 '
                                              '능력이 사람들 앞에서 드러나자, 사람들은 엘사를 이해하기보다 두려워합니다. 결국 엘사는 모든 시선과 책임을 피해 눈 덮인 산으로 '
                                              '도망칩니다.',
                                              '산 위에서 엘사는 처음으로 자신의 진짜 모습을 마주합니다. 이 노래는 단순히 ‘다 잊어버리자’는 의미가 아니라, 그동안 억눌렀던 '
                                              '두려움, 책임감, 타인의 시선에서 벗어나 자기 자신을 받아들이는 과정을 보여 줍니다.',
                                              "수업에서는 let it go, conceal, hold back, storm inside, I'm free, the past "
                                              'is in the past 같은 표현을 중심으로 배울 수 있습니다. 특히 이 노래는 자유, 두려움, 자기표현, 자신감에 대해 '
                                              '학생들과 이야기하기 좋은 자료입니다.']},
 '2. Hello - Adele': {'title': '☎️ Hello: 과거의 누군가에게 건네는 늦은 안부',
                      'paragraphs': ['Adele의 Hello는 시간이 많이 흐른 뒤, 과거의 누군가에게 다시 연락하고 싶은 마음을 담은 노래입니다. 노래 속 화자는 상대에게 전화를 '
                                     '걸며 오래전의 관계, 미안함, 후회, 그리고 아직 완전히 치유되지 않은 감정을 떠올립니다.',
                                     '이 노래에서 화자는 단순히 ‘안녕’이라고 말하는 것이 아닙니다. 과거에 하지 못했던 사과를 조심스럽게 꺼내고 싶어 합니다. 하지만 두 사람 '
                                     '사이에는 시간의 거리, 마음의 거리, 그리고 실제 거리까지 생겨 있습니다.',
                                     '반복되는 Hello라는 말은 인사이면서 동시에 사과의 시작처럼 들립니다. 화자는 내가 너무 늦은 것은 아닐까, 상대는 이미 괜찮아진 것은 아닐까 '
                                     '생각하면서도, 적어도 자신은 말하려고 노력했다고 고백합니다.',
                                     "수업에서는 I'm sorry, I tried, after all these years, used to be, the other side 같은 "
                                     '표현을 중심으로 배울 수 있습니다. 학생들은 이 노래를 통해 사과, 후회, 시간의 흐름, 그리고 관계의 거리감을 영어 표현과 함께 이해할 수 '
                                     '있습니다.']},
 '3. A Whole New World - Aladdin OST': {'title': '🕌 A Whole New World: 새로운 세상을 바라보는 순간',
                                        'paragraphs': ['A Whole New World는 영화 Aladdin의 대표곡으로, 알라딘과 자스민이 마법 양탄자를 타고 '
                                                       '밤하늘을 날며 새로운 세상을 바라보는 장면에서 나오는 노래입니다. 이 장면은 단순한 낭만적인 비행이 아니라, '
                                                       '자스민이 처음으로 궁전 밖의 세상을 직접 경험하는 순간입니다.',
                                                       '자스민은 공주로서 화려한 삶을 살지만, 정해진 규칙과 역할 속에서 자유롭게 세상을 경험하지 못했습니다. 알라딘은 '
                                                       '그런 자스민에게 궁전 밖의 넓은 세상과 새로운 가능성을 보여 줍니다.',
                                                       '이 노래에서 a whole new world는 새로운 장소만을 뜻하지 않습니다. 새로운 시선, 새로운 경험, '
                                                       '그리고 스스로 선택할 수 있는 자유를 의미합니다. 두 사람은 두려움보다 설렘이 더 큰 세계로 함께 나아갑니다.',
                                                       '수업에서는 I can show you the world, open your eyes, point of view, '
                                                       'crystal clear, new horizons 같은 표현을 중심으로 배울 수 있습니다. 학생들에게 ‘내가 '
                                                       '경험해 보고 싶은 새로운 세상’이나 ‘나에게 새로운 관점을 보여 준 사람’을 생각하게 할 수 있습니다.']},
 '4. Stand By Me - Ben E. King': {'title': '🤝 Stand By Me: 곁에 있어 주는 힘',
                                  'paragraphs': ['Stand By Me는 어둡고 불안한 순간에도 누군가가 내 곁에 있어 준다면 두렵지 않다는 메시지를 담은 노래입니다. '
                                                 '제목의 stand by me는 단순히 ‘내 옆에 서 있어’가 아니라, ‘내 곁에 있어 줘’, ‘나를 지켜 줘’, ‘함께해 '
                                                 '줘’라는 의미로 이해할 수 있습니다.',
                                                 '노래는 밤이 찾아오고 세상이 어두워지는 장면으로 시작합니다. 달빛만 보이는 상황은 불안과 두려움을 상징하지만, 화자는 '
                                                 '혼자가 아니라는 믿음 때문에 두려워하지 않겠다고 말합니다.',
                                                 '하늘이 무너지고 산이 바다로 무너져 내리는 듯한 극단적인 표현은 삶에서 마주할 수 있는 큰 어려움을 나타냅니다. 하지만 '
                                                 '사랑하는 사람이 곁에 있다면 그 모든 상황도 견딜 수 있다고 노래합니다.',
                                                 "수업에서는 I won't be afraid, I won't cry, shed a tear, whenever you're "
                                                 'in trouble 같은 표현을 중심으로 배울 수 있습니다. 친구, 가족, 사랑하는 사람이 주는 안정감과 용기를 '
                                                 '이야기하기에 좋은 노래입니다.']},
 "5. Don't Know Why - Norah Jones": {'title': "🌙 Don't Know Why: 이유를 알 수 없는 마음",
                                     'paragraphs': ["Don't Know Why는 Norah Jones의 대표곡으로, 조용하고 부드러운 멜로디 속에 설명하기 어려운 "
                                                    '아쉬움과 후회를 담고 있는 노래입니다. 노래 속 화자는 누군가에게 가지 않았던 자신의 행동을 떠올리며, 왜 그렇게 '
                                                    '했는지 스스로도 알 수 없다고 말합니다.',
                                                    '이 노래는 큰 사건을 직접적으로 설명하지 않습니다. 대신 마음속에 남아 있는 감정의 흔적을 천천히 보여 줍니다. 해가 '
                                                    '뜰 때까지 기다렸지만 결국 가지 못했고, 새벽이 밝아오는 순간에는 차라리 멀리 날아가 버리고 싶어 합니다.',
                                                    "I don't know why I didn't come이라는 문장이 반복되면서, 화자가 자신의 마음을 명확히 설명하지 "
                                                    '못하는 상태가 잘 드러납니다. 이 반복 속에는 후회, 망설임, 외로움, 그리움이 조용하게 섞여 있습니다.',
                                                    "수업에서는 I don't know why, I wished that I could, on my mind, empty "
                                                    'as a drum 같은 표현을 중심으로 배울 수 있습니다. 학생들이 이유를 설명하기 어려운 감정과 후회를 영어로 '
                                                    '표현해 보는 활동으로 연결하기 좋습니다.']},
 '6. Fix You - Coldplay': {'title': '💡 Fix You: 힘든 순간에 건네는 위로',
                           'paragraphs': ['Coldplay의 Fix You는 실패, 상실, 지침, 슬픔을 겪는 사람에게 따뜻한 위로를 건네는 노래입니다. 노래 속 화자는 상대가 '
                                          '최선을 다했지만 원하는 결과를 얻지 못했을 때, 그리고 잃어버린 것을 되돌릴 수 없을 때의 아픔을 조용히 바라봅니다.',
                                          '반복되는 Lights will guide you home은 어두운 순간에도 길을 비춰 주는 희망을 상징합니다. 또한 I will try '
                                          'to fix you는 상대를 완벽하게 고쳐 주겠다는 뜻이라기보다, 힘든 시간을 혼자 견디지 않도록 곁에서 도와주고 싶다는 마음으로 '
                                          '이해할 수 있습니다.',
                                          '이 노래는 실패를 부끄러운 것으로만 보지 않습니다. 오히려 실수에서 배우고, 무너진 자리에서 다시 일어설 수 있다는 가능성을 보여 '
                                          '줍니다. 그래서 이 노래는 위로와 회복의 메시지를 전달합니다.',
                                          "수업에서는 try your best, don't succeed, what you want / what you need, stuck in "
                                          'reverse, learn from my mistakes 같은 표현을 중심으로 배울 수 있습니다. 학생들에게 ‘나를 다시 일으켜 준 '
                                          '사람’이나 ‘내가 누군가에게 해 줄 수 있는 위로’를 생각하게 할 수 있습니다.']},
 '7. The Scientist - Coldplay': {'title': '🔬 The Scientist: 처음으로 돌아가고 싶은 마음',
                                 'paragraphs': ['Coldplay의 The Scientist는 지나간 관계와 후회를 돌아보며, 처음으로 돌아가 다시 말하고 싶은 마음을 담은 '
                                                '노래입니다. 노래 속 화자는 사랑과 이별을 과학처럼 분석하려 하지만, 마음은 숫자와 공식처럼 쉽게 설명되지 않는다는 것을 '
                                                '깨닫습니다.',
                                                "Come up to meet you, tell you I'm sorry는 상대를 다시 만나 사과하고 싶은 마음을 보여 "
                                                '줍니다. Tell you I need you, Tell you I set you apart는 상대가 자신에게 얼마나 특별한 '
                                                '존재였는지를 뒤늦게 깨닫는 표현입니다.',
                                                "반복되는 Let's go back to the start와 Take me back to the start는 단순히 과거로 "
                                                '돌아가고 싶다는 뜻을 넘어, 관계가 어긋나기 전의 순수한 순간으로 돌아가고 싶은 마음을 나타냅니다. 이 노래의 핵심 감정은 '
                                                '후회, 그리움, 미안함, 그리고 다시 시작하고 싶은 마음입니다.',
                                                "수업에서는 tell you I'm sorry, I need you, set you apart, go back to the "
                                                'start, nobody said it was easy 같은 표현을 중심으로 배울 수 있습니다. 또한 ‘다시 돌아가고 싶은 '
                                                '순간’, ‘그때 하지 못한 말’, ‘관계가 왜 생각보다 어려운가’를 주제로 reflective writing을 하기에 '
                                                '좋습니다.']},
 '8. My Heart Will Go On - Celine Dion': {'title': '🚢 My Heart Will Go On: 마음속에 계속 살아 있는 사랑',
                                          'paragraphs': ['My Heart Will Go On은 영화 Titanic의 대표곡으로, 사랑하는 사람이 멀리 있거나 더 이상 '
                                                         '곁에 없더라도 그 사랑과 기억은 마음속에서 계속 이어진다는 메시지를 담은 노래입니다. 노래 속 화자는 매일 '
                                                         '밤 꿈속에서 사랑하는 사람을 보고 느끼며, 그 사람이 여전히 마음속에 살아 있다고 믿습니다.',
                                                         '이 노래에서 distance와 spaces between us는 단순한 물리적 거리만을 뜻하지 않습니다. 두 '
                                                         '사람 사이를 갈라놓은 시간, 상황, 이별, 상실까지 함께 상징합니다. 하지만 화자는 그 거리와 공간을 넘어 '
                                                         '사랑이 계속된다고 말합니다.',
                                                         '반복되는 my heart will go on은 ‘내 심장이 계속 뛴다’는 문자 그대로의 뜻을 넘어, 사랑과 '
                                                         '기억이 사라지지 않고 계속 이어진다는 의미로 이해할 수 있습니다. 사랑했던 한 순간이 평생 마음속에 남아 한 '
                                                         '사람의 삶을 지탱해 주는 힘이 되는 것입니다.',
                                                         '수업에서는 in my dreams, wherever you are, the heart does go on, '
                                                         'open the door, safe in my heart 같은 표현을 중심으로 배울 수 있습니다. 또한 '
                                                         '학생들에게 ‘마음속에 오래 남아 있는 사람’, ‘멀리 있어도 기억나는 관계’, ‘그리움이 주는 위로’를 '
                                                         '주제로 생각을 적게 할 수 있습니다.']},
 '9. Alex Sampson - Play Pretend': {'title': '🎭 Play Pretend: 좋아하지만 숨겨야 하는 마음',
                                    'paragraphs': ['Alex Sampson의 Play Pretend는 가까운 사람을 좋아하지만 그 마음을 쉽게 드러내지 못하고, 친구처럼 '
                                                   '아무렇지 않은 척해야 하는 상황을 담은 노래입니다. 제목의 play pretend는 ‘괜찮은 척하다’, ‘아무렇지 않은 '
                                                   '척하다’라는 의미로 이해할 수 있습니다.',
                                                   '노래 속 화자는 상대를 특별한 사람이라고 생각합니다. 상대가 자신이 얼마나 소중한 사람인지 알았으면 좋겠지만, 동시에 '
                                                   '그 마음을 직접 말하지 못합니다. 상대가 다시 상처받는 모습을 보는 것도 힘들고, 자신의 마음을 숨기는 것도 힘든 '
                                                   '상황입니다.',
                                                   '반복되는 I want you to be happy는 상대의 행복을 진심으로 바라는 마음을 보여 줍니다. 하지만 it’s '
                                                   'hard to watch you fall again과 I gotta play pretend는 그 마음이 단순한 우정만은 '
                                                   '아니라는 점, 그리고 솔직하지 못한 감정이 화자에게 아픔을 준다는 점을 보여 줍니다.',
                                                   '수업에서는 someone special, settle, break the rules, don’t take this '
                                                   'the wrong way, play pretend, fine line, like the back of my hand '
                                                   '같은 표현을 중심으로 배울 수 있습니다. 또한 학생들에게 ‘좋아하지만 말하지 못한 마음’, ‘친구의 행복을 바라보는 '
                                                   '마음’, ‘괜찮은 척했던 순간’을 주제로 생각을 적게 할 수 있습니다.']},
 '10. Older - Sasha Alex Sloan': {'title': '🌙 Older: 나이가 들며 이해하게 되는 것',
                                  'paragraphs': ['Older는 Sasha Alex Sloan의 노래로, 어린 시절에는 이해할 수 없었던 부모님의 갈등과 가족의 모습을 시간이 '
                                                 '흐른 뒤 조금씩 다르게 바라보게 되는 마음을 담고 있습니다. 화자는 어릴 때 부모님의 싸움을 들으며 방 안에서 음악을 크게 '
                                                 '틀고, 그 상황을 피하려 했던 기억을 떠올립니다.',
                                                 '어릴 때 화자는 부모님이 왜 행복하지 못한지 이해하지 못했고, 자신은 절대 부모님처럼 되지 않겠다고 생각했습니다. 하지만 '
                                                 '나이가 들면서 부모님도 완벽한 영웅이 아니라, 자신처럼 상처받고 실수하고 사랑을 어려워하는 한 사람이라는 것을 깨닫게 '
                                                 '됩니다.',
                                                 '반복되는 The older I get the more that I see는 나이가 들수록 더 많이 이해하게 된다는 '
                                                 '뜻입니다. 이 노래는 단순히 가족의 아픔을 말하는 것이 아니라, 시간이 지나며 원망이 이해로 바뀌고, 사랑이 항상 쉽지 '
                                                 '않다는 사실을 받아들이는 성장의 과정을 보여 줍니다.',
                                                 "수업에서는 I used to, the older I get, my parents aren't heroes, loving "
                                                 'is hard, try your best, let someone go 같은 표현을 중심으로 배울 수 있습니다. 또한 '
                                                 '학생들에게 ‘어릴 때는 몰랐지만 지금은 이해되는 일’, ‘가족을 바라보는 시선의 변화’, ‘누군가를 놓아주는 마음’을 '
                                                 '주제로 생각을 적게 할 수 있습니다.']},
 '11. No One Else Like You - Adam Levine': {'title': '💘 No One Else Like You: 너 같은 사람은 없다는 마음',
                                            'paragraphs': ['No One Else Like You는 영화 Begin Again에 나오는 Adam Levine의 '
                                                           '노래로, 마음속에 특별한 사람이 있지만 그 마음을 쉽게 드러내지 못하는 화자의 감정을 담고 있습니다. '
                                                           '제목의 no one else like you는 ‘너 같은 사람은 아무도 없어’라는 뜻으로, 상대가 '
                                                           '자신에게 얼마나 특별한 존재인지 보여 줍니다.',
                                                           '영화 Begin Again은 음악을 통해 상처 입은 사람들이 다시 삶을 시작하는 이야기입니다. 주인공 '
                                                           '그레타는 남자친구 데이브와 함께 뉴욕에 오지만, 데이브가 가수로 성공하면서 두 사람의 관계는 점점 '
                                                           '멀어집니다. 결국 데이브의 배신으로 그레타는 큰 상처를 받게 됩니다.',
                                                           '한편, 과거에는 잘나가던 음반 프로듀서였지만 지금은 일도 가정도 무너진 댄은 우연히 작은 바에서 그레타의 '
                                                           '노래를 듣게 됩니다. 그는 그레타의 음악에서 진심과 가능성을 발견하고, 함께 음반을 만들자고 제안합니다. '
                                                           '하지만 이들에게는 돈도, 제대로 된 스튜디오도 없습니다. 그래서 뉴욕 거리, 골목, 지하철역, 건물 옥상 '
                                                           '등 도시 곳곳을 녹음 장소로 삼아 음악을 만들어 갑니다.',
                                                           '이 과정에서 그레타는 이별의 상처를 조금씩 극복하고, 댄도 잃어버렸던 열정과 삶의 방향을 되찾습니다. 이 '
                                                           '영화는 단순한 사랑 이야기가 아니라, 상처받은 사람들이 음악을 통해 자신을 회복하고 다시 시작하는 '
                                                           '이야기입니다. 제목 Begin Again처럼, 실패와 이별 뒤에도 삶은 다시 시작될 수 있다는 메시지를 '
                                                           '담고 있습니다.',
                                                           '노래 속 화자는 상대가 이미 다른 사람과 함께 있는 상황에서도, 자신이 원하는 사람은 오직 그 '
                                                           '사람뿐이라고 말합니다. 상대를 닮은 사람, 상대처럼 웃는 사람, 상대처럼 느껴지는 사람을 원한다고 '
                                                           '반복하면서, 결국 누구도 그 사람을 대신할 수 없다는 마음을 표현합니다.']},
 '12. Out of Time - The Weeknd': {'title': '⏳ Out of Time: 너무 늦게 깨달은 후회',
                                  'paragraphs': ['Out of Time은 The Weeknd의 노래로, 사랑하는 사람에게 상처를 주고 난 뒤 뒤늦게 자신의 잘못을 깨닫지만 '
                                                 '이미 너무 늦어 버린 상황을 담고 있습니다. 제목의 out of time은 ‘시간이 다 되었다’, ‘이미 늦었다’라는 '
                                                 '뜻으로, 후회와 미련이 섞인 화자의 마음을 보여 줍니다.',
                                                 '노래 속 화자는 지난 몇 달 동안 자기 자신을 돌아보고 있었다고 말합니다. 자신의 삶에 많은 상처가 있었고, 그 상처 '
                                                 '때문에 자신을 사랑해 준 사람들에게 차갑게 대했다는 사실을 깨닫습니다. 하지만 그 깨달음은 이미 상대가 다른 사람을 선택한 '
                                                 '뒤에 찾아옵니다.',
                                                 '반복되는 I’m out of time은 사랑한다고 말하고 싶고, 곁에 있어 주고 싶고, 잘해 주고 싶지만 이미 기회를 '
                                                 '놓쳤다는 고백입니다. 화자는 다시 한 번만 기회를 달라고 말하지만, 동시에 상대가 이미 마음을 정했다는 사실도 알고 '
                                                 '있습니다.',
                                                 '수업에서는 working on me, trauma, look back, I regret, made up your mind, '
                                                 'out of time, give me one chance 같은 표현을 중심으로 배울 수 있습니다. 또한 학생들에게 ‘뒤늦게 '
                                                 '후회한 순간’, ‘시간이 지나고 깨달은 소중함’, ‘다시 기회가 주어진다면 하고 싶은 말’을 주제로 생각을 적게 할 수 '
                                                 '있습니다.']},
 "13. I Don't Think So - Priscilla Ahn": {'title': "🚪 I Don't Think So: 이용당하지 않겠다는 단호한 마음",
                                          'paragraphs': ["Priscilla Ahn의 I Don't Think So는 관계 속에서 애매한 태도와 상처를 느낀 화자가 더 "
                                                         "이상 이용당하지 않겠다고 말하는 노래입니다. 제목의 I don't think so는 단순히 ‘나는 그렇게 "
                                                         '생각하지 않아’라는 뜻을 넘어, ‘그건 아닌 것 같아’, ‘나는 받아들이지 않겠어’라는 단호한 거절의 의미로 '
                                                         '이해할 수 있습니다.',
                                                         '노래 속 화자는 상대가 자신에게 확실한 마음을 보이지 않으면서도 자신을 곁에 두려는 듯한 태도를 느낍니다. '
                                                         '그래서 처음에는 너무 친절하게 대해 왔지만, 이제는 그 관계가 자신을 혼란스럽게 만들고 있다는 것을 '
                                                         '깨닫습니다.',
                                                         'I can take a hint와 I can take a clue는 상대의 눈치와 신호를 알아차렸다는 '
                                                         "뜻입니다. You're giving me the boot는 상대가 자신을 밀어내고 있다는 느낌을 표현하며, "
                                                         'I am not here for you to use는 더 이상 이용당하지 않겠다는 자기 존중의 표현입니다.',
                                                         "수업에서는 I don't think so, I think I should go, listen up, take "
                                                         'a hint, take a clue, utterly confused, I am not here for you '
                                                         'to use 같은 표현을 중심으로 배울 수 있습니다. 또한 학생들에게 ‘관계에서 선을 긋는 순간’, ‘애매한 '
                                                         '태도 때문에 혼란스러웠던 경험’, ‘나를 지키기 위한 단호한 말’을 주제로 생각을 적게 할 수 있습니다.']},
 '14. New York City - Norah Jones': {'title': '🗽 New York City: 아름답지만 아픈 도시의 기억',
                                     'paragraphs': ['Norah Jones의 New York City는 화려하고 아름다운 도시가 주는 꿈과 환상, 그리고 그 안에 숨어 '
                                                    '있는 상처와 외로움을 함께 담고 있는 노래입니다. 제목의 New York City는 단순한 장소 이름이 아니라, '
                                                    '사람을 끌어당기지만 동시에 지치게 만드는 복잡한 감정의 공간으로 이해할 수 있습니다.',
                                                    '노래 속 화자는 기억이 흐릿해지고, 거울 속 자신의 모습을 바라보며 과거의 일들을 떠올립니다. 사랑이 영원할 것이라고 '
                                                    '믿고 싶었지만, 상대의 눈빛에서 빛이 사라지는 순간을 보며 어떤 사랑은 끝까지 살아남지 못한다는 사실을 깨닫습니다.',
                                                    '반복되는 such a beautiful disease는 매우 인상적인 표현입니다. New York City가 '
                                                    '아름답지만 동시에 병처럼 사람을 아프게 할 수 있다는 의미로 볼 수 있습니다. 이 표현은 꿈, 사랑, 도시의 환상, '
                                                    '성공에 대한 욕망이 때로는 사람을 강하게 끌어당기면서도 상처를 남길 수 있다는 양면성을 보여 줍니다.',
                                                    "수업에서는 I can't remember, look in the mirror, endless love, in the "
                                                    'dead of the night, things could get better, no regrets, pass me '
                                                    'by, beautiful disease 같은 표현을 중심으로 배울 수 있습니다. 또한 학생들에게 꿈을 좇는 도시, '
                                                    '아름답지만 힘들었던 경험, 겉보기와 실제가 달랐던 순간을 주제로 생각을 적게 할 수 있습니다.']},
 '15. Counting Stars - OneRepublic': {'title': '🌟 Counting Stars: 돈보다 꿈을 세고 싶은 마음',
                                      'paragraphs': ['OneRepublic의 Counting Stars는 돈, 성공, 규칙적인 삶보다 자신이 진짜 꿈꾸는 삶을 따라가고 '
                                                     '싶은 마음을 담은 노래입니다. 제목의 counting stars는 단순히 별을 센다는 뜻이 아니라, 돈을 세는 '
                                                     '삶에서 벗어나 꿈과 희망을 바라보겠다는 의미로 이해할 수 있습니다.',
                                                     '노래 속 화자는 요즘 잠을 이루지 못하고, 자신과 상대가 앞으로 무엇이 될 수 있을지 계속 꿈꿉니다. 하지만 단순히 '
                                                     '돈을 많이 버는 삶이 아니라, 더 큰 희망과 가능성을 따라가고 싶어 합니다.',
                                                     "no more counting dollars, we'll be counting stars라는 문장은 물질적인 "
                                                     '성공보다 꿈과 의미를 더 중요하게 보겠다는 선언처럼 들립니다. 또한 right와 wrong, old와 young, '
                                                     'money와 stars처럼 서로 대비되는 표현을 통해 혼란스럽지만 살아 있는 감정을 보여 줍니다.',
                                                     '수업에서는 losing sleep, dreaming about, counting dollars, counting '
                                                     "stars, seek it out, do what we're told, makes me feel alive 같은 "
                                                     '표현을 중심으로 배울 수 있습니다. 또한 학생들에게 돈보다 중요하게 생각하는 것, 내가 꿈꾸는 미래, 남들이 정한 '
                                                     '길이 아니라 내가 선택하고 싶은 길을 주제로 생각을 적게 할 수 있습니다.']},
 '16. Fly to the Moon - Peder Elias': {'title': '🌙 Fly to the Moon: 작은 아이들이 큰 세상으로 날아오르는 노래',
                                       'paragraphs': ['Fly to the Moon은 Peder Elias의 노래로, 외롭고 작게 느껴졌던 어린 시절을 지나 서로의 '
                                                      '가능성을 믿으며 더 큰 세상으로 나아가는 마음을 담고 있습니다. 노래 속 두 사람은 큰 세상 속의 작은 전사들처럼 '
                                                      '시작하지만, 결국 달까지 날아가고 바다를 건너는 존재로 성장합니다.',
                                                      '초반부의 by ourselves, ate our lunch in the bathroom, all alone 같은 '
                                                      '표현은 외로움과 소외감을 보여 줍니다. 하지만 후렴에서는 fly to the moon, sail across '
                                                      'the ocean, move mountains 같은 표현이 반복되며, 예전의 외로움이 자신감과 도전으로 바뀌는 '
                                                      '모습을 보여 줍니다.',
                                                      'Follow rules, do as you are told, walk the path it is set in '
                                                      'stone은 사회가 정해 준 길을 그대로 따르라는 말을 나타냅니다. 하지만 화자는 이제 그 길만 따르지 않고, '
                                                      '자신만의 방식으로 춤추고 더 높이 올라가려 합니다.',
                                                      'For every little caterpillar, there is a butterfly라는 표현은 이 노래의 '
                                                      '핵심 이미지입니다. 작고 눈에 띄지 않는 애벌레도 언젠가 나비가 되듯이, 학생들도 지금은 부족해 보여도 성장하고 '
                                                      '변화할 수 있다는 메시지를 전달합니다. 수업에서는 자신감, 성장, 우정, 도전, 자기만의 길을 주제로 생각을 적게 '
                                                      '할 수 있습니다.']},
 '17. My Universe - Coldplay X BTS': {'title': '🌌 My Universe: 서로 다른 세계가 만나 하나의 우주가 되는 노래',
                                      'paragraphs': ['My Universe는 Coldplay와 BTS가 함께 부른 노래로, 서로 다른 배경과 세계를 가진 사람들이 사랑과 '
                                                     '믿음으로 연결되는 마음을 담고 있습니다. 제목의 my universe는 상대가 단순히 좋아하는 사람이 아니라, 내 '
                                                     '삶과 세상을 밝혀 주는 아주 소중한 존재라는 뜻으로 이해할 수 있습니다.',
                                                     '노래 속 화자는 밤에는 상대를 올려다보고, 아침에는 상대가 떠오르는 모습을 바라봅니다. 이 이미지는 상대가 별이나 '
                                                     '태양처럼 화자의 세계를 비추는 존재임을 보여 줍니다. You make my world light up '
                                                     'inside라는 표현도 상대가 마음속 세상을 밝게 만들어 준다는 의미입니다.',
                                                     'And they said that we can’t be together, because we come from '
                                                     'different sides라는 부분은 두 사람이 서로 다른 편, 다른 배경, 다른 세계에서 왔기 때문에 주변의 '
                                                     '장벽을 마주한다는 뜻입니다. 하지만 노래는 그 차이보다 서로를 향한 믿음과 연결이 더 크다고 말합니다.',
                                                     '수업에서는 my universe, put you first, light up inside, different '
                                                     'sides, without you, made of each other 같은 표현을 중심으로 배울 수 있습니다. '
                                                     '학생들은 나의 세상을 밝혀 주는 사람, 서로 다른 사람과 함께하는 경험, 그리고 내가 가장 먼저 소중히 여기고 싶은 '
                                                     '가치를 생각해 볼 수 있습니다.']},
 '18. Golden - KPop Demon Hunters': {'title': '✨ Golden: 숨어 있던 나를 드러내고 빛나는 노래',
                                     'paragraphs': ['Golden은 어둡고 외로웠던 과거를 지나, 이제는 자신의 목소리와 존재를 숨기지 않고 빛나겠다고 말하는 노래입니다. 노래 속 화자는 처음에는 ghost처럼 혼자였고, 자신이 원래 어떤 존재인지 믿지 못했습니다.',
                                                    'I lived two lives, tried to play both sides와 I could not find my own place는 다른 사람의 기대에 맞추려 했지만 자기 자리를 찾지 못했던 마음을 보여 줍니다. 하지만 이제 화자는 더 이상 숨지 않고, 자신이 태어난 모습대로 빛나려 합니다.',
                                                    '반복되는 gonna be golden은 앞으로 더 밝고 단단한 존재가 되겠다는 다짐입니다. no fear, no lies는 두려움과 거짓 없이 진짜 나로 살아가겠다는 의미로 이해할 수 있습니다.',
                                                    '수업에서는 I was alone, given the throne, meant to be, find my own place, problem child, done hiding, shining, gonna be golden, born to be 같은 표현을 중심으로 배울 수 있습니다. 학생들은 숨기고 싶었던 모습, 자신감을 되찾은 순간, 그리고 앞으로 빛나고 싶은 나의 모습을 주제로 생각을 적을 수 있습니다.']},
 '19. Cowboy in LA - LANY': {'title': '🤠 Cowboy in LA: 화려한 도시 속에서도 진심을 지키는 노래',
                             'paragraphs': ['Cowboy in LA는 LANY의 노래로, 화려한 LA의 분위기 속에서도 자신만의 진심과 예의를 지키고 싶은 화자의 마음을 담고 있습니다. 노래에는 palm '
                                            'trees, sunsets, Malibu처럼 도시적이고 낭만적인 이미지가 나오지만, 화자는 그 화려함보다 상대와 함께하는 시간이 더 좋다고 말합니다.',
                                            "반복되는 Let's skip the club, let's skip the crowd는 시끄럽고 복잡한 장소보다 조용하고 진심 있는 데이트를 하고 싶다는 뜻입니다. "
                                            "I'll hold your hand, I'll hold the door는 상대를 배려하고 예의 있게 대하는 모습을 보여 줍니다.",
                                            'Oklahoma, it made a man out of me라는 표현은 화자가 자신의 성장 배경을 소중하게 생각한다는 것을 보여 줍니다. LA에 있지만 마음은 '
                                            'cowboy처럼 솔직하고 단단하며, 다른 사람들과 똑같이 보이고 말하기보다 different kind of heart를 가진 사람으로 자신을 표현합니다.',
                                            "수업에서는 palm trees, square dancing, ain't got nothing on you, let's skip, take you on a date, "
                                            'hold the door, how I was raised, different kind of heart, take it slow 같은 표현을 중심으로 배울 수 '
                                            '있습니다. 학생들은 진심, 배려, 나만의 태도, 그리고 화려함보다 중요한 가치에 대해 생각을 적을 수 있습니다.']}}


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

tabs_list = ["🎬 배경 학습", "📖 가사 & 이해도 퀴즈", "🎯 Grammar", "🧩 문장 매칭 게임", "✍️ 생각 적기", "⭐ Key Expression 학습"]
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


elif selected_tab == "📖 가사 & 이해도 퀴즈":
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


elif selected_tab == "🎯 Grammar":
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

                status_{component_id}.textContent = "먼저 영어 또는 한국어 박스를 하나 선택하세요.";
                render_{component_id}();
            }});

            render_{component_id}();
        </script>
        """,
        height=760,
        scrolling=True
    )

    st.markdown("---")
    st.markdown("### 📄 문장 매칭 게임 완료 인증")
    st.info("문장 매칭 게임을 끝까지 완료한 뒤 아래 버튼을 누르면 ‘문장 매칭 게임 임무를 완성하셨습니다’ PDF를 저장할 수 있습니다.")
    if st.button("문장 매칭을 모두 끝냈습니다", key=f"matching_done_{match_key}", use_container_width=True):
        st.session_state[f"mission_{match_key}_matching"] = True

    if st.session_state.get(f"mission_{match_key}_matching"):
        show_mission_pdf_download(
            song_choice,
            "문장 매칭 게임",
            f"{match_key}_matching",
            "문장 매칭 게임 활동 완료"
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



elif selected_tab == "⭐ Key Expression 학습":
    show_key_expression_learning_in_lyrics(song_choice, data, max_words=10)
