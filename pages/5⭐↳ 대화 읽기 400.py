import streamlit as st
from gtts import gTTS
import io
import re
import html
import json
import uuid
import base64
import streamlit.components.v1 as components

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="Daily English 400 Dialogues",
    page_icon="🌱",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 1000;
        color: #111827;
        margin-bottom: 4px;
    }

    .sub-title {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 22px;
    }

    .dialogue-header {
        background: linear-gradient(135deg, #dbeafe 0%, #fce7f3 50%, #fef3c7 100%);
        border-radius: 26px;
        padding: 24px 28px;
        margin-bottom: 22px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    }

    .dialogue-title {
        font-size: 33px;
        font-weight: 1000;
        color: #111827;
        margin-bottom: 8px;
    }

    .dialogue-desc {
        font-size: 17px;
        font-weight: 800;
        color: #374151;
        line-height: 1.6;
    }

    .line-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }

    .en-line {
        font-size: 23px;
        font-weight: 900;
        color: #111827;
        line-height: 1.45;
    }

    .ko-line {
        font-size: 17px;
        font-weight: 700;
        color: #6b7280;
        margin-top: 6px;
        line-height: 1.5;
    }

    .word-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 14px 16px;
        margin-top: 14px;
        font-size: 15px;
        color: #475569;
        line-height: 1.7;
    }

    .audio-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e3a8a;
        border-radius: 18px;
        padding: 14px 16px;
        margin: 10px 0 18px 0;
        font-size: 15px;
        font-weight: 800;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 900;
        min-height: 48px;
        border: 1px solid #d1d5db;
    }

    .stButton > button:hover {
        border-color: #8b5cf6;
        color: #8b5cf6;
    }

    div[data-testid="stTabs"] button[role="tab"] p {
        font-size: 18px !important;
        font-weight: 900 !important;
    }


    .matching-box {
        background: linear-gradient(135deg,#eef2ff 0%,#f0f9ff 50%,#fdf2f8 100%);
        padding: 22px 24px;
        border-radius: 20px;
        border: 1px solid #c7d2fe;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 5px 16px rgba(99,102,241,0.08);
    }

    .matching-title {
        font-size: 28px;
        font-weight: 1000;
        color: #4338ca;
        margin-bottom: 8px;
    }

    .matching-guide {
        font-size: 16px;
        font-weight: 800;
        color: #475569;
        line-height: 1.7;
    }

    .selected-card-notice {
        background-color: #fef3c7;
        padding: 13px 15px;
        border-radius: 14px;
        border: 1px solid #facc15;
        color: #92400e;
        font-size: 15px;
        font-weight: 900;
        margin-bottom: 14px;
        line-height: 1.5;
    }

    .match-progress-box {
        background: linear-gradient(135deg,#dcfce7,#dbeafe);
        border: 1px solid #bbf7d0;
        border-radius: 16px;
        padding: 13px 15px;
        margin: 12px 0 16px 0;
        font-size: 17px;
        font-weight: 900;
        color: #14532d;
        text-align: center;
    }

    div[data-testid="stTabs"] button[role="tab"] p {
        font-size: 18px !important;
        font-weight: 900 !important;
    }

    @media (max-width: 520px) {
        .main-title {
            font-size: 33px;
        }
        .dialogue-title {
            font-size: 27px;
        }
        .en-line {
            font-size: 19px;
        }
        .ko-line {
            font-size: 15px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# TTS 함수
# =========================
def remove_speaker_label(sentence):
    """
    음성에서는 A:, B:를 빼고 자연스럽게 읽게 합니다.
    """
    return re.sub(r"^[A-Z]:\s*", "", sentence).strip()


def make_dialogue_tts_text(lines):
    """
    대화 전체를 하나의 음성 텍스트로 만듭니다.
    Google TTS URL 방식이 아니라 gTTS를 사용하므로 긴 대화에서도 더 안정적입니다.
    """
    clean_lines = []

    for line in lines:
        text = remove_speaker_label(line["en"])
        clean_lines.append(text)

    return " ".join(clean_lines)


@st.cache_data(show_spinner=False)
def make_gtts_audio(text):
    """
    대화 전체 mp3 생성
    """
    fp = io.BytesIO()
    tts = gTTS(text=text, lang="en", tld="com", slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def play_dialogue_audio(lines, key):
    """
    대화 전체 듣기:
    - st.audio() 대신 HTML audio 사용
    - 한국어 해석 보기 toggle을 눌러도 재생 위치를 localStorage에 저장/복원
    - rerun 후에도 가능하면 이어서 재생
    """

    audio_state_key = f"{key}_audio_bytes"

    if st.button("🔊 대화 전체 듣기", key=key, use_container_width=True):
        try:
            dialogue_text = make_dialogue_tts_text(lines)
            audio_bytes = make_gtts_audio(dialogue_text)

            # rerun 이후에도 오디오가 사라지지 않도록 session_state에 저장
            st.session_state[audio_state_key] = audio_bytes

        except Exception as e:
            st.error("음성 파일을 만들지 못했습니다. requirements.txt에 gTTS가 있는지 확인해 주세요.")
            st.caption(f"오류 내용: {e}")

    # 한 번 만든 오디오는 계속 표시
    if audio_state_key in st.session_state:
        audio_bytes = st.session_state[audio_state_key]
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        # key를 안전한 id로 변환
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

            const timeKey = "dialogue_audio_time_{safe_audio_id}";
            const playingKey = "dialogue_audio_playing_{safe_audio_id}";

            // 저장된 재생 위치 복원
            const savedTime = localStorage.getItem(timeKey);
            if (savedTime !== null) {{
                audio.currentTime = parseFloat(savedTime);
            }}

            // 이전에 재생 중이었다면 rerun 후 다시 재생 시도
            const wasPlaying = localStorage.getItem(playingKey);
            if (wasPlaying === "true") {{
                setTimeout(() => {{
                    audio.play().catch(() => {{
                        // 브라우저 정책상 자동재생이 막힐 수 있음
                    }});
                }}, 300);
            }}

            // 재생 위치 계속 저장
            audio.addEventListener("timeupdate", () => {{
                localStorage.setItem(timeKey, audio.currentTime);
            }});

            // 재생 상태 저장
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

            // Streamlit rerun 직전에도 위치 저장
            window.addEventListener("beforeunload", () => {{
                localStorage.setItem(timeKey, audio.currentTime);
                localStorage.setItem(playingKey, !audio.paused);
            }});
            </script>
            """,
            height=95,
        )



# =========================
# 문장 매칭 활동 함수
# =========================
def clean_text_for_display(text):
    return html.escape(str(text).strip())


def safe_key(text):
    return re.sub(r"[^a-zA-Z0-9가-힣_]+", "_", str(text))


def shuffle_options(options, seed):
    import random
    rng = random.Random(seed)
    options = list(options)
    rng.shuffle(options)
    return options


def show_sentence_matching_activity(dialogue_data, key_prefix):
    """
    문장 매칭 게임:
    - Streamlit 버튼 방식이 아니라 HTML/JS 컴포넌트로 구현
    - 클릭한 박스 자체가 색칠됨
    - 영어 박스와 한국어 박스를 맞게 고르면 두 박스가 동시에 반짝이며 사라짐
    - 나머지 대화문/듣기/한국어 보기/탭 구조는 그대로 유지
    """
    pairs = []
    for i, line in enumerate(dialogue_data["lines"], start=1):
        pairs.append({
            "id": f"pair_{i}",
            "en": line["en"],
            "ko": line["ko"],
        })

    # 매번 같은 순서로 섞이도록 key_prefix를 seed로 사용
    en_cards = [{"id": p["id"], "text": p["en"]} for p in pairs]
    ko_cards = [{"id": p["id"], "text": p["ko"]} for p in pairs]

    en_cards = shuffle_options(en_cards, seed=f"{key_prefix}_en")
    ko_cards = shuffle_options(ko_cards, seed=f"{key_prefix}_ko")

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
                    왼쪽 영어 문장과 오른쪽 한국어 해석을 차례로 눌러 짝을 맞추세요.<br>
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
                        ? "오른쪽에서 알맞은 한국어 해석을 고르세요."
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
        height=900,
        scrolling=True
    )


# =========================
# Daily English 400 단어 활용 대화문 20개
# - 각 주제별 20단어를 대화문 안에 포함
# - 생존 160 대화문 파일처럼 대화문 + 문장 매칭 게임 제공
# =========================
dialogues = [{'title': '1. School Life Vocabulary Talk',
  'ko_title': '학교생활',
  'words': 'subject, math, science, history, music, art, P.E., club, schedule, semester, assignment, '
           'project, presentation, report, textbook, workbook, library, cafeteria, hallway, attendance',
  'lines': [{'en': 'A: What subjects do you usually study at school?',
             'ko': 'A: 오늘 Daily English 연습에서 subject(과목)와/과 math(수학)를 사용해.'},
            {'en': 'B: I study math, science, and history, and each subject helps me understand the world in '
                   'a different way.',
             'ko': 'B: 좋아. science은/는 과학, history은/는 역사라는 뜻이야.'},
            {'en': 'A: I enjoy music and art because they let me express my ideas freely.',
             'ko': 'A: 오늘 Daily English 연습에서 music(음악)와/과 art(미술)를 사용해.'},
            {'en': 'B: I like P.E. because I can move my body, and my club activity helps me make new '
                   'friends.',
             'ko': 'B: 좋아. P.E.은/는 체육, club은/는 동아리라는 뜻이야.'},
            {'en': 'A: I check my schedule every morning before class starts.',
             'ko': 'A: 오늘 Daily English 연습에서 schedule(일정표)와/과 semester(학기)를 사용해.'},
            {'en': 'B: This semester, I want to finish every assignment on time and work hard on my project.',
             'ko': 'B: 좋아. assignment은/는 과제, project은/는 프로젝트라는 뜻이야.'},
            {'en': 'A: Next week, I have to give a presentation and write a short report.',
             'ko': 'A: 오늘 Daily English 연습에서 presentation(발표)와/과 report(보고서)를 사용해.'},
            {'en': 'B: Then you should read your textbook first and use your workbook for extra practice.',
             'ko': 'B: 좋아. textbook은/는 교과서, workbook은/는 문제집라는 뜻이야.'},
            {'en': 'A: After lunch, I sometimes study in the library or meet my friends in the cafeteria.',
             'ko': 'A: 오늘 Daily English 연습에서 library(도서관)와/과 cafeteria(급식소, 식당)를 사용해.'},
            {'en': 'B: Before class begins, students walk through the hallway and check their attendance.',
             'ko': 'B: 좋아. hallway은/는 복도, attendance은/는 출석라는 뜻이야.'}]},
 {'title': '2. Classroom Action Talk',
  'ko_title': '교실 활동',
  'words': 'copy, repeat, underline, circle, choose, check, match, complete, fill, spell, pronounce, review, '
           'explain, describe, compare, discuss, present, take notes, turn in, hand out',
  'lines': [{'en': 'A: Please copy the sentence first, and then repeat it aloud with your partner.',
             'ko': 'A: 오늘 Daily English 연습에서 copy(베껴 쓰다)와/과 repeat(반복하다)를 사용해.'},
            {'en': 'B: After that, underline the key word and circle the answer you think is correct.',
             'ko': 'B: 좋아. underline은/는 밑줄 치다, circle은/는 동그라미 치다라는 뜻이야.'},
            {'en': 'A: I will choose one expression and check my answer carefully.',
             'ko': 'A: 오늘 Daily English 연습에서 choose(고르다)와/과 check(확인하다)를 사용해.'},
            {'en': 'B: Good. Now match the sentence parts and complete the short dialogue.',
             'ko': 'B: 좋아. match은/는 연결하다, 맞추다, complete은/는 완성하다라는 뜻이야.'},
            {'en': 'A: Can I fill in the blank and spell the word for the class?',
             'ko': 'A: 오늘 Daily English 연습에서 fill(채우다)와/과 spell(철자를 말하다)를 사용해.'},
            {'en': 'B: Yes, and try to pronounce it clearly before we review the lesson.',
             'ko': 'B: 좋아. pronounce은/는 발음하다, review은/는 복습하다라는 뜻이야.'},
            {'en': 'A: I can explain my answer, but it is hard to describe the picture in English.',
             'ko': 'A: 오늘 Daily English 연습에서 explain(설명하다)와/과 describe(묘사하다)를 사용해.'},
            {'en': "B: Let's compare two examples and discuss the difference together.",
             'ko': 'B: 좋아. compare은/는 비교하다, discuss은/는 토론하다라는 뜻이야.'},
            {'en': 'A: Later, I will present my idea and take notes while others speak.',
             'ko': 'A: 오늘 Daily English 연습에서 present(발표하다)와/과 take notes(필기하다)를 사용해.'},
            {'en': 'B: At the end of class, turn in your paper, and I will hand out the next worksheet.',
             'ko': 'B: 좋아. turn in은/는 제출하다, hand out은/는 나누어 주다라는 뜻이야.'}]},
 {'title': '3. Home and Daily Living Talk',
  'ko_title': '집과 생활',
  'words': 'living room, bedroom, kitchen, balcony, floor, wall, roof, garden, yard, sofa, television, '
           'refrigerator, microwave, blanket, pillow, towel, soap, mirror, closet, trash',
  'lines': [{'en': 'A: In my house, the living room is bright, and my bedroom is small but comfortable.',
             'ko': 'A: 오늘 Daily English 연습에서 living room(거실)와/과 bedroom(침실)를 사용해.'},
            {'en': 'B: My family talks in the kitchen, and we sometimes sit on the balcony at night.',
             'ko': 'B: 좋아. kitchen은/는 부엌, balcony은/는 발코니라는 뜻이야.'},
            {'en': 'A: I cleaned the floor today because there was dust near the wall.',
             'ko': 'A: 오늘 Daily English 연습에서 floor(바닥, 층)와/과 wall(벽)를 사용해.'},
            {'en': 'B: The roof is old, but the garden in front of the house is beautiful.',
             'ko': 'B: 좋아. roof은/는 지붕, garden은/는 정원라는 뜻이야.'},
            {'en': 'A: My dog likes running around the yard, and I like resting on the sofa.',
             'ko': 'A: 오늘 Daily English 연습에서 yard(마당)와/과 sofa(소파)를 사용해.'},
            {'en': 'B: In the evening, we watch television and take drinks from the refrigerator.',
             'ko': 'B: 좋아. television은/는 텔레비전, refrigerator은/는 냉장고라는 뜻이야.'},
            {'en': 'A: I warm up food in the microwave and sleep with a soft blanket.',
             'ko': 'A: 오늘 Daily English 연습에서 microwave(전자레인지)와/과 blanket(담요)를 사용해.'},
            {'en': 'B: I need a new pillow and a clean towel after my shower.',
             'ko': 'B: 좋아. pillow은/는 베개, towel은/는 수건라는 뜻이야.'},
            {'en': 'A: There is soap by the sink and a mirror above it.',
             'ko': 'A: 오늘 Daily English 연습에서 soap(비누)와/과 mirror(거울)를 사용해.'},
            {'en': 'B: I put my clothes in the closet and throw trash away before bed.',
             'ko': 'B: 좋아. closet은/는 옷장, trash은/는 쓰레기라는 뜻이야.'}]},
 {'title': '4. Daily Routine Talk',
  'ko_title': '하루 일과',
  'words': 'routine, wake up, get up, brush, shower, dress, leave, arrive, return, finish, relax, weekday, '
           'weekend, usually, often, sometimes, always, never, habit, lifestyle',
  'lines': [{'en': 'A: My morning routine starts when I wake up early.',
             'ko': 'A: 오늘 Daily English 연습에서 routine(일과)와/과 wake up(잠에서 깨다)를 사용해.'},
            {'en': 'B: I get up, brush my teeth, and try not to waste time.',
             'ko': 'B: 좋아. get up은/는 일어나다, brush은/는 닦다라는 뜻이야.'},
            {'en': 'A: Then I shower quickly and dress for school.',
             'ko': 'A: 오늘 Daily English 연습에서 shower(샤워하다)와/과 dress(옷을 입다)를 사용해.'},
            {'en': 'B: I leave home at seven thirty and arrive before the first bell.',
             'ko': 'B: 좋아. leave은/는 떠나다, arrive은/는 도착하다라는 뜻이야.'},
            {'en': 'A: After school, I return home and finish my homework.',
             'ko': 'A: 오늘 Daily English 연습에서 return(돌아오다)와/과 finish(끝내다)를 사용해.'},
            {'en': 'B: I relax for a short time on each weekday evening.',
             'ko': 'B: 좋아. relax은/는 쉬다, weekday은/는 평일라는 뜻이야.'},
            {'en': 'A: On the weekend, I usually sleep a little longer.',
             'ko': 'A: 오늘 Daily English 연습에서 weekend(주말)와/과 usually(보통)를 사용해.'},
            {'en': 'B: I often exercise, and sometimes I meet my friends.',
             'ko': 'B: 좋아. often은/는 자주, sometimes은/는 가끔라는 뜻이야.'},
            {'en': 'A: I always prepare my bag at night, and I never skip breakfast.',
             'ko': 'A: 오늘 Daily English 연습에서 always(항상)와/과 never(절대 ~않다)를 사용해.'},
            {'en': 'B: That habit makes your lifestyle healthier and more organized.',
             'ko': 'B: 좋아. habit은/는 습관, lifestyle은/는 생활 방식라는 뜻이야.'}]},
 {'title': '5. Hobby and Free Time Talk',
  'ko_title': '취미와 여가',
  'words': 'hobby, movie, drama, song, concert, dance, drawing, painting, comic, novel, photography, '
           'cooking, baking, camping, hiking, fishing, free time, favorite, popular, relaxing',
  'lines': [{'en': 'A: My favorite hobby is watching a movie on Friday night.',
             'ko': 'A: 오늘 Daily English 연습에서 hobby(취미)와/과 movie(영화)를 사용해.'},
            {'en': 'B: I like a good drama, but I also listen to a song when I want to relax.',
             'ko': 'B: 좋아. drama은/는 드라마, song은/는 노래라는 뜻이야.'},
            {'en': 'A: Last month, I went to a concert and learned a new dance with my friends.',
             'ko': 'A: 오늘 Daily English 연습에서 concert(콘서트)와/과 dance(춤)를 사용해.'},
            {'en': 'B: I prefer drawing, and my sister enjoys painting quiet scenes.',
             'ko': 'B: 좋아. drawing은/는 그림 그리기, painting은/는 그림, 회화라는 뜻이야.'},
            {'en': 'A: Sometimes I read a comic, and sometimes I read a novel before bed.',
             'ko': 'A: 오늘 Daily English 연습에서 comic(만화)와/과 novel(소설)를 사용해.'},
            {'en': 'B: Photography is fun because cooking and beautiful food can become memories.',
             'ko': 'B: 좋아. photography은/는 사진 촬영, cooking은/는 요리라는 뜻이야.'},
            {'en': 'A: My brother likes baking bread and camping near the river.',
             'ko': 'A: 오늘 Daily English 연습에서 baking(빵 굽기)와/과 camping(캠핑)를 사용해.'},
            {'en': 'B: I enjoy hiking in the mountains, but my uncle likes fishing by the sea.',
             'ko': 'B: 좋아. hiking은/는 하이킹, fishing은/는 낚시라는 뜻이야.'},
            {'en': 'A: In my free time, I choose my favorite relaxing activity.',
             'ko': 'A: 오늘 Daily English 연습에서 free time(여가 시간)와/과 favorite(가장 좋아하는)를 사용해.'},
            {'en': 'B: These days, short videos are popular, but quiet hobbies can be relaxing too.',
             'ko': 'B: 좋아. popular은/는 인기 있는, relaxing은/는 편안한라는 뜻이야.'}]},
 {'title': '6. Sports and Activities Talk',
  'ko_title': '운동과 활동',
  'words': 'soccer, baseball, basketball, volleyball, tennis, badminton, swimming, cycling, skating, boxing, '
           'taekwondo, yoga, fitness, field, court, stadium, coach, match, competition, medal',
  'lines': [{'en': 'A: I played soccer yesterday, and my brother practiced baseball after school.',
             'ko': 'A: 오늘 Daily English 연습에서 soccer(축구)와/과 baseball(야구)를 사용해.'},
            {'en': 'B: Our class likes basketball, but another class is better at volleyball.',
             'ko': 'B: 좋아. basketball은/는 농구, volleyball은/는 배구라는 뜻이야.'},
            {'en': 'A: I enjoy tennis because it is fast, and badminton is easy to play with friends.',
             'ko': 'A: 오늘 Daily English 연습에서 tennis(테니스)와/과 badminton(배드민턴)를 사용해.'},
            {'en': 'B: Swimming is good for health, and cycling is a fun way to travel.',
             'ko': 'B: 좋아. swimming은/는 수영, cycling은/는 자전거 타기라는 뜻이야.'},
            {'en': 'A: In winter, skating looks exciting, but boxing looks very difficult.',
             'ko': 'A: 오늘 Daily English 연습에서 skating(스케이트 타기)와/과 boxing(복싱)를 사용해.'},
            {'en': 'B: Taekwondo teaches discipline, and yoga helps people stay calm.',
             'ko': 'B: 좋아. taekwondo은/는 태권도, yoga은/는 요가라는 뜻이야.'},
            {'en': 'A: I go to the fitness room before I practice on the field.',
             'ko': 'A: 오늘 Daily English 연습에서 fitness(체력 운동)와/과 field(경기장, 들판)를 사용해.'},
            {'en': 'B: The tennis court is near the big stadium behind our school.',
             'ko': 'B: 좋아. court은/는 코트, stadium은/는 경기장라는 뜻이야.'},
            {'en': 'A: Our coach said the next match will be important.',
             'ko': 'A: 오늘 Daily English 연습에서 coach(코치)와/과 match(경기)를 사용해.'},
            {'en': 'B: If we do well in the competition, maybe we can win a medal.',
             'ko': 'B: 좋아. competition은/는 대회, medal은/는 메달라는 뜻이야.'}]},
 {'title': '7. Weather and Seasons Talk',
  'ko_title': '날씨와 계절',
  'words': 'season, spring, summer, fall, winter, cloudy, rainy, snowy, windy, stormy, foggy, dry, wet, '
           'humid, temperature, degree, forecast, umbrella, raincoat, rainbow',
  'lines': [{'en': 'A: Which season do you like most, spring or summer?',
             'ko': 'A: 오늘 Daily English 연습에서 season(계절)와/과 spring(봄)를 사용해.'},
            {'en': 'B: I like fall, but my sister loves winter because she enjoys cold weather.',
             'ko': 'B: 좋아. summer은/는 여름, fall은/는 가을라는 뜻이야.'},
            {'en': 'A: The sky is cloudy today, so it may become rainy later.',
             'ko': 'A: 오늘 Daily English 연습에서 winter(겨울)와/과 cloudy(흐린)를 사용해.'},
            {'en': 'B: If it gets snowy and windy, we should stay inside.',
             'ko': 'B: 좋아. rainy은/는 비 오는, snowy은/는 눈 오는라는 뜻이야.'},
            {'en': 'A: Last night was stormy, and this morning was foggy near the river.',
             'ko': 'A: 오늘 Daily English 연습에서 windy(바람 부는)와/과 stormy(폭풍우 치는)를 사용해.'},
            {'en': 'B: The air is dry in winter, but it can be wet after heavy rain.',
             'ko': 'B: 좋아. foggy은/는 안개 낀, dry은/는 건조한라는 뜻이야.'},
            {'en': 'A: Summer in Korea is often humid and uncomfortable.',
             'ko': 'A: 오늘 Daily English 연습에서 wet(젖은)와/과 humid(습한)를 사용해.'},
            {'en': 'B: I checked the temperature, and it is thirty degrees today.',
             'ko': 'B: 좋아. temperature은/는 온도, degree은/는 도라는 뜻이야.'},
            {'en': 'A: The forecast says we should bring an umbrella tomorrow.',
             'ko': 'A: 오늘 Daily English 연습에서 forecast(일기예보)와/과 umbrella(우산)를 사용해.'},
            {'en': 'B: I will wear a raincoat, and maybe we can see a rainbow after the rain.',
             'ko': 'B: 좋아. raincoat은/는 비옷, rainbow은/는 무지개라는 뜻이야.'}]},
 {'title': '8. Nature and Environment Talk',
  'ko_title': '자연과 환경',
  'words': 'nature, environment, plant, forest, lake, ocean, island, desert, field, farm, village, leaf, '
           'root, stone, sand, soil, plastic, recycle, protect, pollution',
  'lines': [{'en': 'A: I love nature because it makes me feel peaceful.',
             'ko': 'A: 오늘 Daily English 연습에서 nature(자연)와/과 environment(환경)를 사용해.'},
            {'en': 'B: We should care about the environment and protect every plant around us.',
             'ko': 'B: 좋아. plant은/는 식물, forest은/는 숲라는 뜻이야.'},
            {'en': 'A: A quiet forest near a lake is my favorite place to walk.',
             'ko': 'A: 오늘 Daily English 연습에서 lake(호수)와/과 ocean(대양)를 사용해.'},
            {'en': 'B: I want to see the ocean, visit an island, and cross a desert someday.',
             'ko': 'B: 좋아. island은/는 섬, desert은/는 사막라는 뜻이야.'},
            {'en': 'A: My grandparents live near a field and a small farm.',
             'ko': 'A: 오늘 Daily English 연습에서 field(들판)와/과 farm(농장)를 사용해.'},
            {'en': 'B: Their village is peaceful, and every leaf looks fresh in spring.',
             'ko': 'B: 좋아. village은/는 마을, leaf은/는 잎라는 뜻이야.'},
            {'en': 'A: A tree needs a strong root, just like a house needs a strong stone wall.',
             'ko': 'A: 오늘 Daily English 연습에서 root(뿌리)와/과 stone(돌)를 사용해.'},
            {'en': 'B: At the beach, sand is soft, but soil on a farm is rich and dark.',
             'ko': 'B: 좋아. sand은/는 모래, soil은/는 흙라는 뜻이야.'},
            {'en': 'A: We should use less plastic and recycle bottles every day.',
             'ko': 'A: 오늘 Daily English 연습에서 plastic(플라스틱)와/과 recycle(재활용하다)를 사용해.'},
            {'en': 'B: Small actions can protect nature and reduce pollution.',
             'ko': 'B: 좋아. protect은/는 보호하다, pollution은/는 오염라는 뜻이야.'}]},
 {'title': '9. Restaurant and Ordering Talk',
  'ko_title': '식당과 주문',
  'words': 'restaurant, menu, seat, waiter, waitress, order, dish, meal, soup, salad, steak, pizza, pasta, '
           'burger, sandwich, dessert, spicy, sweet, bill, receipt',
  'lines': [{'en': 'A: This restaurant has a big menu, so I need more time to choose.',
             'ko': 'A: 오늘 Daily English 연습에서 restaurant(식당)와/과 menu(메뉴)를 사용해.'},
            {'en': "B: Let's find a seat before the waiter comes to our table.",
             'ko': 'B: 좋아. seat은/는 자리, waiter은/는 남자 종업원라는 뜻이야.'},
            {'en': 'A: The waitress is kind, and I am ready to order now.',
             'ko': 'A: 오늘 Daily English 연습에서 waitress(여자 종업원)와/과 order(주문하다)를 사용해.'},
            {'en': 'B: What dish do you want for your main meal?',
             'ko': 'B: 좋아. dish은/는 요리, 접시, meal은/는 식사라는 뜻이야.'},
            {'en': 'A: I might start with soup and a small salad.',
             'ko': 'A: 오늘 Daily English 연습에서 soup(수프)와/과 salad(샐러드)를 사용해.'},
            {'en': 'B: I want steak, but the pizza also looks delicious.',
             'ko': 'B: 좋아. steak은/는 스테이크, pizza은/는 피자라는 뜻이야.'},
            {'en': 'A: My friend ordered pasta, and my brother chose a burger.',
             'ko': 'A: 오늘 Daily English 연습에서 pasta(파스타)와/과 burger(버거)를 사용해.'},
            {'en': 'B: I usually like a sandwich for lunch and dessert after dinner.',
             'ko': 'B: 좋아. sandwich은/는 샌드위치, dessert은/는 디저트라는 뜻이야.'},
            {'en': 'A: This sauce is spicy, but the cake is very sweet.',
             'ko': 'A: 오늘 Daily English 연습에서 spicy(매운)와/과 sweet(단)를 사용해.'},
            {'en': 'B: After we finish eating, we should ask for the bill and keep the receipt.',
             'ko': 'B: 좋아. bill은/는 계산서, receipt은/는 영수증라는 뜻이야.'}]},
 {'title': '10. Shopping and Prices Talk',
  'ko_title': '쇼핑과 가격',
  'words': 'shop, market, mall, supermarket, cashier, customer, price, sale, discount, coupon, change, coin, '
           'bill, expensive, cheap, size, color, brand, exchange, refund',
  'lines': [{'en': 'A: I went to a small shop near the market after school.',
             'ko': 'A: 오늘 Daily English 연습에서 shop(가게)와/과 market(시장)를 사용해.'},
            {'en': 'B: I usually go to the mall, but the supermarket is cheaper for food.',
             'ko': 'B: 좋아. mall은/는 쇼핑몰, supermarket은/는 슈퍼마켓라는 뜻이야.'},
            {'en': 'A: The cashier was friendly, and every customer waited quietly.',
             'ko': 'A: 오늘 Daily English 연습에서 cashier(계산원)와/과 customer(손님)를 사용해.'},
            {'en': 'B: I checked the price because there was a big sale today.',
             'ko': 'B: 좋아. price은/는 가격, sale은/는 할인 판매라는 뜻이야.'},
            {'en': 'A: I used a discount coupon to buy a notebook.',
             'ko': 'A: 오늘 Daily English 연습에서 discount(할인)와/과 coupon(쿠폰)를 사용해.'},
            {'en': 'B: The clerk gave me change with one coin and one small bill.',
             'ko': 'B: 좋아. change은/는 거스름돈, coin은/는 동전라는 뜻이야.'},
            {'en': 'A: This jacket is expensive, but that T-shirt is cheap.',
             'ko': 'A: 오늘 Daily English 연습에서 bill(지폐, 계산서)와/과 expensive(비싼)를 사용해.'},
            {'en': 'B: I need the right size and a brighter color.',
             'ko': 'B: 좋아. cheap은/는 싼, size은/는 크기라는 뜻이야.'},
            {'en': 'A: This brand is famous, but I am not sure about the quality.',
             'ko': 'A: 오늘 Daily English 연습에서 color(색깔)와/과 brand(상표)를 사용해.'},
            {'en': 'B: If it does not fit, you can exchange it or ask for a refund.',
             'ko': 'B: 좋아. exchange은/는 교환하다, refund은/는 환불라는 뜻이야.'}]},
 {'title': '11. Clothes and Appearance Talk',
  'ko_title': '옷과 외모',
  'words': 'T-shirt, pants, jeans, shorts, skirt, dress, jacket, coat, sweater, hoodie, uniform, socks, '
           'sneakers, boots, sandals, scarf, gloves, belt, glasses, comfortable',
  'lines': [{'en': 'A: I usually wear a T-shirt and pants on warm days.',
             'ko': 'A: 오늘 Daily English 연습에서 T-shirt(티셔츠)와/과 pants(바지)를 사용해.'},
            {'en': 'B: I like jeans, but shorts are better in summer.',
             'ko': 'B: 좋아. jeans은/는 청바지, shorts은/는 반바지라는 뜻이야.'},
            {'en': 'A: My sister bought a skirt, and my cousin chose a dress.',
             'ko': 'A: 오늘 Daily English 연습에서 skirt(치마)와/과 dress(드레스, 원피스)를 사용해.'},
            {'en': 'B: In winter, I need a jacket or a thick coat.',
             'ko': 'B: 좋아. jacket은/는 재킷, coat은/는 코트라는 뜻이야.'},
            {'en': 'A: This sweater is warm, and that hoodie looks casual.',
             'ko': 'A: 오늘 Daily English 연습에서 sweater(스웨터)와/과 hoodie(후드티)를 사용해.'},
            {'en': 'B: We wear a uniform at school, and I always bring extra socks.',
             'ko': 'B: 좋아. uniform은/는 교복, 제복, socks은/는 양말라는 뜻이야.'},
            {'en': 'A: I use sneakers for running and boots when it rains.',
             'ko': 'A: 오늘 Daily English 연습에서 sneakers(운동화)와/과 boots(부츠)를 사용해.'},
            {'en': 'B: At the beach, sandals are useful, but a scarf is not necessary.',
             'ko': 'B: 좋아. sandals은/는 샌들, scarf은/는 목도리라는 뜻이야.'},
            {'en': 'A: My mother bought gloves and a belt for my father.',
             'ko': 'A: 오늘 Daily English 연습에서 gloves(장갑)와/과 belt(벨트)를 사용해.'},
            {'en': 'B: These glasses are light, and they feel comfortable.',
             'ko': 'B: 좋아. glasses은/는 안경, comfortable은/는 편안한라는 뜻이야.'}]},
 {'title': '12. Transportation and Directions Talk',
  'ko_title': '교통과 길 찾기',
  'words': 'bus stop, subway, airport, terminal, platform, route, direction, straight, corner, block, '
           'traffic, crosswalk, sidewalk, bridge, tunnel, entrance, exit, transfer, lost, guide',
  'lines': [{'en': 'A: The bus stop is next to the subway station.',
             'ko': 'A: 오늘 Daily English 연습에서 bus stop(버스 정류장)와/과 subway(지하철)를 사용해.'},
            {'en': "B: We need to go to the airport terminal before six o'clock.",
             'ko': 'B: 좋아. airport은/는 공항, terminal은/는 터미널라는 뜻이야.'},
            {'en': 'A: Which platform should we use for this route?',
             'ko': 'A: 오늘 Daily English 연습에서 platform(승강장)와/과 route(경로)를 사용해.'},
            {'en': 'B: Look at the direction sign and walk straight for two minutes.',
             'ko': 'B: 좋아. direction은/는 방향, straight은/는 똑바로라는 뜻이야.'},
            {'en': 'A: Turn left at the corner and walk one more block.',
             'ko': 'A: 오늘 Daily English 연습에서 corner(모퉁이)와/과 block(구역, 블록)를 사용해.'},
            {'en': 'B: Be careful because traffic is heavy near the crosswalk.',
             'ko': 'B: 좋아. traffic은/는 교통, crosswalk은/는 횡단보도라는 뜻이야.'},
            {'en': 'A: Stay on the sidewalk until you reach the bridge.',
             'ko': 'A: 오늘 Daily English 연습에서 sidewalk(인도)와/과 bridge(다리)를 사용해.'},
            {'en': 'B: After the tunnel, you will see the entrance on your right.',
             'ko': 'B: 좋아. tunnel은/는 터널, entrance은/는 입구라는 뜻이야.'},
            {'en': 'A: If you miss the exit, you may need to transfer to another bus.',
             'ko': 'A: 오늘 Daily English 연습에서 exit(출구)와/과 transfer(갈아타다)를 사용해.'},
            {'en': 'B: When you feel lost, ask a guide for help.',
             'ko': 'B: 좋아. lost은/는 길을 잃은, guide은/는 안내하다, 안내자라는 뜻이야.'}]},
 {'title': '13. Travel and Accommodation Talk',
  'ko_title': '여행과 숙박',
  'words': 'travel, trip, vacation, tourist, guide, passport, flight, hotel, motel, hostel, reservation, '
           'check in, check out, luggage, suitcase, backpack, souvenir, museum, famous, local',
  'lines': [{'en': 'A: I want to travel during winter vacation.',
             'ko': 'A: 오늘 Daily English 연습에서 travel(여행하다)와/과 trip(여행)를 사용해.'},
            {'en': 'B: That sounds like a great trip for a young tourist.',
             'ko': 'B: 좋아. vacation은/는 방학, 휴가, tourist은/는 관광객라는 뜻이야.'},
            {'en': 'A: I will ask a guide and check my passport first.',
             'ko': 'A: 오늘 Daily English 연습에서 guide(안내자)와/과 passport(여권)를 사용해.'},
            {'en': 'B: Then you should book your flight and choose a hotel.',
             'ko': 'B: 좋아. flight은/는 항공편, hotel은/는 호텔라는 뜻이야.'},
            {'en': 'A: A motel is cheaper, but a hostel is better for meeting people.',
             'ko': 'A: 오늘 Daily English 연습에서 motel(모텔)와/과 hostel(호스텔)를 사용해.'},
            {'en': 'B: Make a reservation before you check in.',
             'ko': 'B: 좋아. reservation은/는 예약, check in은/는 체크인하다라는 뜻이야.'},
            {'en': 'A: After I check out, I will carry my luggage to the station.',
             'ko': 'A: 오늘 Daily English 연습에서 check out(체크아웃하다)와/과 luggage(짐)를 사용해.'},
            {'en': 'B: A suitcase is good for clothes, but a backpack is easier to carry.',
             'ko': 'B: 좋아. suitcase은/는 여행 가방, backpack은/는 배낭라는 뜻이야.'},
            {'en': 'A: I want to buy a souvenir and visit a museum.',
             'ko': 'A: 오늘 Daily English 연습에서 souvenir(기념품)와/과 museum(박물관)를 사용해.'},
            {'en': 'B: Try famous food and talk with local people while you travel.',
             'ko': 'B: 좋아. famous은/는 유명한, local은/는 현지의라는 뜻이야.'}]},
 {'title': '14. Friendship Talk',
  'ko_title': '친구 관계',
  'words': 'friendship, best friend, teammate, partner, message, call, chat, invite, visit, meet, hang out, '
           'laugh, share, trust, promise, secret, joke, together, alone, forgive',
  'lines': [{'en': 'A: Friendship is important, and my best friend always listens to me.',
             'ko': 'A: 오늘 Daily English 연습에서 friendship(우정)와/과 best friend(가장 친한 친구)를 사용해.'},
            {'en': 'B: A good teammate can also become a strong partner.',
             'ko': 'B: 좋아. teammate은/는 팀 동료, partner은/는 짝, 파트너라는 뜻이야.'},
            {'en': 'A: I sent a message, but I forgot to call him yesterday.',
             'ko': 'A: 오늘 Daily English 연습에서 message(메시지)와/과 call(전화하다)를 사용해.'},
            {'en': 'B: We can chat online and invite him to dinner.',
             'ko': 'B: 좋아. chat은/는 채팅하다, invite은/는 초대하다라는 뜻이야.'},
            {'en': 'A: I want to visit his house and meet his family.',
             'ko': 'A: 오늘 Daily English 연습에서 visit(방문하다)와/과 meet(만나다)를 사용해.'},
            {'en': 'B: We often hang out after school and laugh about silly stories.',
             'ko': 'B: 좋아. hang out은/는 어울려 놀다, laugh은/는 웃다라는 뜻이야.'},
            {'en': 'A: Real friends share problems and trust each other.',
             'ko': 'A: 오늘 Daily English 연습에서 share(나누다, 공유하다)와/과 trust(믿다)를 사용해.'},
            {'en': 'B: They keep a promise and never tell a secret.',
             'ko': 'B: 좋아. promise은/는 약속, secret은/는 비밀라는 뜻이야.'},
            {'en': 'A: A simple joke can make us feel happy together.',
             'ko': 'A: 오늘 Daily English 연습에서 joke(농담)와/과 together(함께)를 사용해.'},
            {'en': 'B: Even when someone feels alone, a true friend can forgive and stay close.',
             'ko': 'B: 좋아. alone은/는 혼자, forgive은/는 용서하다라는 뜻이야.'}]},
 {'title': '15. Feelings and Emotions Talk',
  'ko_title': '감정 표현 확장',
  'words': 'excited, nervous, bored, surprised, confused, embarrassed, proud, disappointed, lonely, relaxed, '
           'calm, upset, interested, satisfied, thankful, hopeful, mood, stress, confidence, courage',
  'lines': [{'en': 'A: I felt excited before the game, but my friend was nervous.',
             'ko': 'A: 오늘 Daily English 연습에서 excited(신난)와/과 nervous(긴장한)를 사용해.'},
            {'en': 'B: I was bored at first, and then I was surprised by the ending.',
             'ko': 'B: 좋아. bored은/는 지루한, surprised은/는 놀란라는 뜻이야.'},
            {'en': 'A: The instructions were confusing, so I felt embarrassed when I made a mistake.',
             'ko': 'A: 오늘 Daily English 연습에서 confused(혼란스러운)와/과 embarrassed(당황한)를 사용해.'},
            {'en': 'B: You should be proud of your effort, not disappointed by one result.',
             'ko': 'B: 좋아. proud은/는 자랑스러운, disappointed은/는 실망한라는 뜻이야.'},
            {'en': 'A: Sometimes I feel lonely, but music helps me feel relaxed.',
             'ko': 'A: 오늘 Daily English 연습에서 lonely(외로운)와/과 relaxed(편안한)를 사용해.'},
            {'en': 'B: Take a deep breath and stay calm when you are upset.',
             'ko': 'B: 좋아. calm은/는 차분한, upset은/는 속상한라는 뜻이야.'},
            {'en': 'A: I am interested in English, and I feel satisfied when I improve.',
             'ko': 'A: 오늘 Daily English 연습에서 interested(관심 있는)와/과 satisfied(만족한)를 사용해.'},
            {'en': 'B: I am thankful for my teacher and hopeful about my future.',
             'ko': 'B: 좋아. thankful은/는 감사하는, hopeful은/는 희망적인라는 뜻이야.'},
            {'en': 'A: My mood changes when I have too much stress.',
             'ko': 'A: 오늘 Daily English 연습에서 mood(기분)와/과 stress(스트레스)를 사용해.'},
            {'en': 'B: Confidence and courage can help you try again.',
             'ko': 'B: 좋아. confidence은/는 자신감, courage은/는 용기라는 뜻이야.'}]},
 {'title': '16. Thoughts and Opinions Talk',
  'ko_title': '생각과 의견',
  'words': 'think, believe, guess, remember, forget, mean, agree, disagree, opinion, idea, reason, example, '
           'fact, choice, decision, advice, suggestion, possible, impossible, confusing',
  'lines': [{'en': 'A: I think practice is important, and I believe anyone can improve.',
             'ko': 'A: 오늘 Daily English 연습에서 think(생각하다)와/과 believe(믿다)를 사용해.'},
            {'en': 'B: I guess you are right, but I sometimes forget what I should remember.',
             'ko': 'B: 좋아. guess은/는 추측하다, remember은/는 기억하다라는 뜻이야.'},
            {'en': 'A: What does this word mean in this sentence?',
             'ko': 'A: 오늘 Daily English 연습에서 forget(잊다)와/과 mean(의미하다)를 사용해.'},
            {'en': 'B: I agree with your answer, but some students may disagree.',
             'ko': 'B: 좋아. agree은/는 동의하다, disagree은/는 동의하지 않다라는 뜻이야.'},
            {'en': 'A: In my opinion, your idea is clear and useful.',
             'ko': 'A: 오늘 Daily English 연습에서 opinion(의견)와/과 idea(생각, 아이디어)를 사용해.'},
            {'en': 'B: Please give one reason and one example to support it.',
             'ko': 'B: 좋아. reason은/는 이유, example은/는 예시라는 뜻이야.'},
            {'en': 'A: The fact is simple, but the choice is difficult.',
             'ko': 'A: 오늘 Daily English 연습에서 fact(사실)와/과 choice(선택)를 사용해.'},
            {'en': 'B: A careful decision is better than quick advice.',
             'ko': 'B: 좋아. decision은/는 결정, advice은/는 조언라는 뜻이야.'},
            {'en': 'A: Do you have a suggestion for a possible solution?',
             'ko': 'A: 오늘 Daily English 연습에서 suggestion(제안)와/과 possible(가능한)를 사용해.'},
            {'en': 'B: Nothing is impossible, but the first step may feel confusing.',
             'ko': 'B: 좋아. impossible은/는 불가능한, confusing은/는 혼란스러운라는 뜻이야.'}]},
 {'title': '17. Plans and Appointments Talk',
  'ko_title': '계획과 약속',
  'words': 'plan, appointment, promise, meeting, date, event, party, festival, deadline, calendar, next '
           'week, message, join, prepare, decide, change, cancel, on time, available, reminder',
  'lines': [{'en': 'A: I made a plan for our appointment after school.',
             'ko': 'A: 오늘 Daily English 연습에서 plan(계획)와/과 appointment(약속, 예약)를 사용해.'},
            {'en': 'B: Please keep your promise and come to the meeting on time.',
             'ko': 'B: 좋아. promise은/는 약속, meeting은/는 모임, 회의라는 뜻이야.'},
            {'en': 'A: What date is the school event this month?',
             'ko': 'A: 오늘 Daily English 연습에서 date(날짜, 데이트)와/과 event(행사)를 사용해.'},
            {'en': 'B: The party is on Friday, and the festival starts next week.',
             'ko': 'B: 좋아. party은/는 파티, festival은/는 축제라는 뜻이야.'},
            {'en': 'A: I wrote the deadline on my calendar.',
             'ko': 'A: 오늘 Daily English 연습에서 deadline(마감일)와/과 calendar(달력)를 사용해.'},
            {'en': 'B: Send me a message next week so I do not forget.',
             'ko': 'B: 좋아. next week은/는 다음 주, message은/는 메시지라는 뜻이야.'},
            {'en': 'A: Can I join your group and prepare the poster with you?',
             'ko': 'A: 오늘 Daily English 연습에서 join(참여하다)와/과 prepare(준비하다)를 사용해.'},
            {'en': 'B: Sure, but we need to decide the topic and change the title.',
             'ko': 'B: 좋아. decide은/는 결정하다, change은/는 바꾸다라는 뜻이야.'},
            {'en': 'A: If it rains, we may cancel the outdoor activity.',
             'ko': 'A: 오늘 Daily English 연습에서 cancel(취소하다)와/과 on time(시간 맞춰)를 사용해.'},
            {'en': 'B: I am available tomorrow, and I will set a reminder tonight.',
             'ko': 'B: 좋아. available은/는 시간이 되는, 이용 가능한, reminder은/는 알림라는 뜻이야.'}]},
 {'title': '18. Healthy Life Talk',
  'ko_title': '건강한 생활',
  'words': 'health, body, eye, ear, nose, mouth, tooth, hand, arm, leg, foot, stomach, back, heart, clinic, '
           'vitamin, diet, cough, flu, breathe',
  'lines': [{'en': 'A: Good health begins with taking care of your body.',
             'ko': 'A: 오늘 Daily English 연습에서 health(건강)와/과 body(몸)를 사용해.'},
            {'en': 'B: Rest your eye and ear when you study for a long time.',
             'ko': 'B: 좋아. eye은/는 눈, ear은/는 귀라는 뜻이야.'},
            {'en': 'A: I have a runny nose and a dry mouth today.',
             'ko': 'A: 오늘 Daily English 연습에서 nose(코)와/과 mouth(입)를 사용해.'},
            {'en': 'B: If your tooth hurts, wash your hand and call a clinic.',
             'ko': 'B: 좋아. tooth은/는 이, hand은/는 손라는 뜻이야.'},
            {'en': 'A: My arm feels fine, but my leg hurts after soccer practice.',
             'ko': 'A: 오늘 Daily English 연습에서 arm(팔)와/과 leg(다리)를 사용해.'},
            {'en': 'B: My foot is sore, and my stomach feels strange.',
             'ko': 'B: 좋아. foot은/는 발, stomach은/는 배, 위라는 뜻이야.'},
            {'en': 'A: I stretched my back and checked my heart rate after running.',
             'ko': 'A: 오늘 Daily English 연습에서 back(등, 허리)와/과 heart(심장)를 사용해.'},
            {'en': 'B: The clinic doctor told me to take a vitamin every morning.',
             'ko': 'B: 좋아. clinic은/는 의원, 진료소, vitamin은/는 비타민라는 뜻이야.'},
            {'en': 'A: A balanced diet can help when you have a cough.',
             'ko': 'A: 오늘 Daily English 연습에서 diet(식단)와/과 cough(기침)를 사용해.'},
            {'en': 'B: If you have the flu, breathe slowly and get enough rest.',
             'ko': 'B: 좋아. flu은/는 독감, breathe은/는 숨 쉬다라는 뜻이야.'}]},
 {'title': '19. Media and Smartphone Talk',
  'ko_title': '미디어와 스마트폰',
  'words': 'smartphone, screen, app, website, internet, Wi-Fi, password, text, video call, gallery, news, '
           'channel, post, comment, upload, download, search, click, battery, notification',
  'lines': [{'en': 'A: My smartphone screen is too bright at night.',
             'ko': 'A: 오늘 Daily English 연습에서 smartphone(스마트폰)와/과 screen(화면)를 사용해.'},
            {'en': 'B: You can use an app or a website to change your settings.',
             'ko': 'B: 좋아. app은/는 앱, website은/는 웹사이트라는 뜻이야.'},
            {'en': 'A: The internet is slow because the Wi-Fi signal is weak.',
             'ko': 'A: 오늘 Daily English 연습에서 internet(인터넷)와/과 Wi-Fi(와이파이)를 사용해.'},
            {'en': 'B: Check the password before you send a text message.',
             'ko': 'B: 좋아. password은/는 비밀번호, text은/는 문자 메시지라는 뜻이야.'},
            {'en': 'A: I had a video call with my cousin and saved pictures in my gallery.',
             'ko': 'A: 오늘 Daily English 연습에서 video call(영상 통화)와/과 gallery(사진첩)를 사용해.'},
            {'en': 'B: I watched the news on my favorite channel this morning.',
             'ko': 'B: 좋아. news은/는 뉴스, channel은/는 채널라는 뜻이야.'},
            {'en': 'A: I wrote a post, and my friend left a comment.',
             'ko': 'A: 오늘 Daily English 연습에서 post(게시물)와/과 comment(댓글)를 사용해.'},
            {'en': 'B: You can upload your homework, but do not download strange files.',
             'ko': 'B: 좋아. upload은/는 업로드하다, download은/는 다운로드하다라는 뜻이야.'},
            {'en': 'A: I will search for the answer and click the first result.',
             'ko': 'A: 오늘 Daily English 연습에서 search(검색하다)와/과 click(클릭하다)를 사용해.'},
            {'en': 'B: My battery is low, and I just got an important notification.',
             'ko': 'B: 좋아. battery은/는 배터리, notification은/는 알림라는 뜻이야.'}]},
 {'title': '20. Jobs and Future Talk',
  'ko_title': '직업과 미래',
  'words': 'job, work, company, office, factory, engineer, mechanic, chef, firefighter, farmer, designer, '
           'singer, actor, athlete, dream, future, goal, skill, interview, experience',
  'lines': [{'en': 'A: I want a job that makes my work meaningful.',
             'ko': 'A: 오늘 Daily English 연습에서 job(직업)와/과 work(일하다)를 사용해.'},
            {'en': 'B: Some people work at a company, and others work in an office.',
             'ko': 'B: 좋아. company은/는 회사, office은/는 사무실라는 뜻이야.'},
            {'en': 'A: My uncle works in a factory, and my cousin wants to be an engineer.',
             'ko': 'A: 오늘 Daily English 연습에서 factory(공장)와/과 engineer(기술자, 엔지니어)를 사용해.'},
            {'en': 'B: A mechanic fixes cars, and a chef cooks delicious food.',
             'ko': 'B: 좋아. mechanic은/는 정비사, chef은/는 요리사라는 뜻이야.'},
            {'en': 'A: A firefighter helps people, and a farmer grows food.',
             'ko': 'A: 오늘 Daily English 연습에서 firefighter(소방관)와/과 farmer(농부)를 사용해.'},
            {'en': 'B: My sister wants to be a designer, but my brother dreams of becoming a singer.',
             'ko': 'B: 좋아. designer은/는 디자이너, singer은/는 가수라는 뜻이야.'},
            {'en': 'A: An actor performs on stage, and an athlete trains every day.',
             'ko': 'A: 오늘 Daily English 연습에서 actor(배우)와/과 athlete(운동선수)를 사용해.'},
            {'en': 'B: Your dream can shape your future if you keep trying.',
             'ko': 'B: 좋아. dream은/는 꿈, future은/는 미래라는 뜻이야.'},
            {'en': 'A: I need a clear goal and a useful skill.',
             'ko': 'A: 오늘 Daily English 연습에서 goal(목표)와/과 skill(기술, 능력)를 사용해.'},
            {'en': 'B: An interview is easier when you have real experience.',
             'ko': 'B: 좋아. interview은/는 면접, experience은/는 경험라는 뜻이야.'}]}]

# =========================
# 화면 구성
# =========================
st.markdown("<div class='main-title'>🌱 Daily English 400 Dialogues</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>Daily English 400 단어를 활용한 일상 대화체 연습입니다. 영어만 먼저 보고, 필요하면 한국어 해석을 확인하세요.</div>",
    unsafe_allow_html=True
)

tab_names = [f"{i + 1}. {d['ko_title']}" for i, d in enumerate(dialogues)]
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        d = dialogues[i]

        sub_dialogue_tab, sub_matching_tab = st.tabs(["📖 대화문", "🧩 문장 매칭"])

        with sub_dialogue_tab:
            st.markdown(
                f"""
                <div class="dialogue-header">
                    <div class="dialogue-title">{d['title']}</div>
                    <div class="dialogue-desc">{d['ko_title']} · Daily English 400 단어 활용 대화 연습</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2 = st.columns([1, 1])

            with c1:
                play_dialogue_audio(d["lines"], key=f"daily400_dialogue_audio_{i}")

            with c2:
                show_korean = st.toggle(
                    "🇰🇷 한국어 해석 보기",
                    value=False,
                    key=f"daily400_show_korean_{i}"
                )

            st.divider()

            for line in d["lines"]:
                st.markdown('<div class="line-card">', unsafe_allow_html=True)

                st.markdown(
                    f"<div class='en-line'>{line['en']}</div>",
                    unsafe_allow_html=True
                )

                if show_korean:
                    st.markdown(
                        f"<div class='ko-line'>{line['ko']}</div>",
                        unsafe_allow_html=True
                    )

                st.markdown('</div>', unsafe_allow_html=True)

            with st.expander("사용된 단어 보기"):
                st.markdown(
                    f"""
                    <div class="word-box">
                        {d['words']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with sub_matching_tab:
            st.markdown(
                f"""
                <div class="dialogue-header">
                    <div class="dialogue-title">🧩 {d['ko_title']} 문장 매칭</div>
                    <div class="dialogue-desc">대화문을 보지 않고 영어 문장과 한국어 해석을 맞춰 봅시다.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            show_sentence_matching_activity(d, key_prefix=f"daily400_dialogue_matching_{i}_{d['ko_title']}")
