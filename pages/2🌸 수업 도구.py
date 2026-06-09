import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import qrcode
from wordcloud import WordCloud
import streamlit.components.v1 as components
from streamlit_drawable_canvas import st_canvas
import random
import html
import urllib.parse

st.set_page_config(
    page_title="Classroom Tools",
    page_icon="🧰",
    layout="wide"
)

# =========================================================
# 기본 함수
# =========================================================
def create_wordcloud(text, max_words=120, bg="white", colormap="viridis"):
    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color=bg,
        max_words=max_words,
        colormap=colormap
    ).generate(text)
    return wordcloud


# =========================================================
# 상단 안내
# =========================================================
st.title("🧰 수업 도구 모음")

st.markdown("""
<div style="
    background: linear-gradient(135deg, #eef7ff, #f7fbff);
    border: 1px solid #d6e9ff;
    border-radius: 18px;
    padding: 22px 24px;
    margin-bottom: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
">
    <p style="font-size:18px; line-height:1.7; margin-bottom:12px;">
        이 앱은 수업 시간에 바로 사용할 수 있는 간단한 도구 모음입니다.
        위의 탭을 눌러 필요한 기능을 선택하세요.
    </p>
    <ul style="font-size:16px; line-height:1.8; margin-bottom:0;">
        <li><b>칠판</b>: 칠판처럼 글을 크게 보여줍니다.</li>
        <li><b>그림판</b>: 화면에 자유롭게 그림을 그릴 수 있습니다.</li>
        <li><b>QR 코드</b>: 인터넷 주소를 QR 코드로 바꿉니다.</li>
        <li><b>타이머</b>: 활동 시간을 정하고 타이머를 사용할 수 있습니다.</li>
        <li><b>워드클라우드</b>: 입력한 글에서 중요한 단어를 구름 모양으로 보여줍니다.</li>
        <li><b>이모지</b>: 수업 자료에 사용할 이모지를 쉽게 찾을 수 있습니다.</li>
        <li><b>조 편성</b>: 학생들을 무작위로 조 편성할 수 있습니다.</li>
        <li><b>번역기</b>: 영어↔한국어 번역을 하고, 영어 문장의 발음도 들을 수 있습니다.</li>
        <li><b>선생님께 부탁해요</b>: 희망곡, 수업 요청, 질문, 건의사항을 구글 문서에 자유롭게 적을 수 있습니다.</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 탭 구성
# =========================================================
tabs = st.tabs([
    "✏️ 칠판",
    "🎨 그림판",
    "🔳 QR 코드",
    "⏳ 타이머",
    "☁️ 워드클라우드",
    "😀 이모지",
    "👥 조 편성",
    "🌐 번역기",
    "🙋 선생님께 부탁해요"
])


# =========================================================
# Tab 0: Blackboard
# =========================================================
with tabs[0]:
    st.subheader("📚 칠판")

    c1, c2 = st.columns([1, 1])
    with c1:
        font_size = st.slider("글자 크기", 12, 124, 32, 2)
    with c2:
        text_color = st.color_picker("글자 색", "#ffffff")

    board_text = st.text_area(
        "✍️ 칠판에 쓸 내용을 입력하세요",
        height=120,
        placeholder="수업 안내, 핵심 표현, 질문 등을 입력하세요.",
        key="board_text"
    )

    safe_board_text = html.escape(board_text).replace("\n", "<br>")

    st.markdown(
        f"""
        <div style="
            background-color:#006666;
            padding:1.5rem;
            border-radius:12px;
            min-height:350px;
            font-size:{font_size}px;
            color:{text_color};
            line-height:1.6;
            white-space:normal;
            box-shadow:0 4px 14px rgba(0,0,0,0.12);
        ">
            {safe_board_text if board_text.strip() else "&nbsp;"}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# Tab 1: Drawing
# =========================================================
with tabs[1]:
    st.subheader("🎨 그림판")
    st.caption("아래 그림판에 자유롭게 그림을 그릴 수 있습니다. 펜 두께와 색을 바꿀 수 있습니다.")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        stroke_width = st.slider("✏️ 펜 두께", 1, 10, 5)

    with col2:
        stroke_color = st.color_picker("🖌 펜 색", "#000000")

    with col3:
        bg_color = st.color_picker("🖼 배경색", "#FFFFFF")

    if "clear_canvas" not in st.session_state:
        st.session_state["clear_canvas"] = False

    st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=400,
        width=700,
        drawing_mode="freedraw",
        key="main_canvas" if not st.session_state["clear_canvas"] else "new_canvas"
    )

    if st.button("🗑️ 그림판 지우기", use_container_width=True):
        st.session_state["clear_canvas"] = not st.session_state["clear_canvas"]
        st.rerun()


# =========================================================
# Tab 2: QR
# =========================================================
with tabs[2]:
    st.subheader("🔳 QR 코드 생성기")
    st.caption("인터넷 주소를 QR 코드로 바꿀 수 있습니다.")

    col1, col2, col3 = st.columns([3, 3, 2])

    with col1:
        qr_link = st.text_input("📌 인터넷 주소를 입력하세요", key="qr_link")

    with col2:
        caption = st.text_input("설명을 입력하세요. 선택 사항입니다", key="qr_caption")

    with col3:
        st.write("")
        st.write("")
        generate_qr_button = st.button("🔆 QR 코드 만들기", key="generate_qr", use_container_width=True)

    if generate_qr_button:
        if not qr_link.strip():
            st.warning("인터넷 주소를 먼저 입력해 주세요.")
        else:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_link.strip())
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB").resize((600, 600))
            st.image(qr_img, caption=caption if caption else "QR Code", width=400)


# =========================================================
# Tab 3: Timer
# =========================================================
with tabs[3]:
    st.subheader("⏳ 수업 타이머")
    st.caption("시간을 설정한 뒤 시작 버튼을 누르세요.")

    col1, col2, col3 = st.columns(3)

    with col1:
        timer_min = st.number_input("분", min_value=0, max_value=180, value=5, step=1)

    with col2:
        timer_sec = st.number_input("초", min_value=0, max_value=59, value=0, step=5)

    with col3:
        st.write("")
        st.write("")
        st.info(f"설정 시간: {timer_min:02d}:{timer_sec:02d}")

    total_seconds = int(timer_min * 60 + timer_sec)

    timer_html = f"""
    <div style="
        width:100%;
        max-width:700px;
        margin:20px auto;
        padding:30px;
        border-radius:20px;
        background:linear-gradient(135deg,#f8fbff,#eef5ff);
        box-shadow:0 4px 16px rgba(0,0,0,0.12);
        text-align:center;
        font-family:Arial, sans-serif;
    ">
        <div id="timerDisplay" style="
            font-size:90px;
            font-weight:800;
            color:#1f4e79;
            margin-bottom:25px;
        ">
            {timer_min:02d}:{timer_sec:02d}
        </div>

        <button onclick="startTimer()" style="
            font-size:24px;
            padding:12px 28px;
            margin:8px;
            border:none;
            border-radius:12px;
            background-color:#2e86de;
            color:white;
            cursor:pointer;
        ">시작</button>

        <button onclick="pauseTimer()" style="
            font-size:24px;
            padding:12px 28px;
            margin:8px;
            border:none;
            border-radius:12px;
            background-color:#f39c12;
            color:white;
            cursor:pointer;
        ">일시정지</button>

        <button onclick="resetTimer()" style="
            font-size:24px;
            padding:12px 28px;
            margin:8px;
            border:none;
            border-radius:12px;
            background-color:#e74c3c;
            color:white;
            cursor:pointer;
        ">초기화</button>

        <p id="message" style="
            margin-top:25px;
            font-size:28px;
            font-weight:bold;
            color:#d63031;
        "></p>
    </div>

    <script>
        let initialTime = {total_seconds};
        let remainingTime = initialTime;
        let timerInterval = null;

        function updateDisplay() {{
            let minutes = Math.floor(remainingTime / 60);
            let seconds = remainingTime % 60;
            document.getElementById("timerDisplay").innerHTML =
                String(minutes).padStart(2, "0") + ":" + String(seconds).padStart(2, "0");
        }}

        function startTimer() {{
            if (timerInterval !== null) return;
            document.getElementById("message").innerHTML = "";

            timerInterval = setInterval(function() {{
                if (remainingTime > 0) {{
                    remainingTime--;
                    updateDisplay();
                }} else {{
                    clearInterval(timerInterval);
                    timerInterval = null;
                    document.getElementById("message").innerHTML = "Time's up!";
                    let audio = new Audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg");
                    audio.play();
                }}
            }}, 1000);
        }}

        function pauseTimer() {{
            clearInterval(timerInterval);
            timerInterval = null;
        }}

        function resetTimer() {{
            clearInterval(timerInterval);
            timerInterval = null;
            remainingTime = initialTime;
            document.getElementById("message").innerHTML = "";
            updateDisplay();
        }}

        updateDisplay();
    </script>
    """

    components.html(timer_html, height=450)


# =========================================================
# Tab 4: WordCloud
# =========================================================
with tabs[4]:
    st.subheader("☁️ 워드클라우드 만들기")
    st.caption("아래에 글을 붙여 넣고 워드클라우드를 만들 수 있습니다.")

    wc_text = st.text_area(
        "📋 글을 붙여 넣으세요",
        height=220,
        placeholder="여기에 글을 붙여 넣으세요...",
        key="wc_text"
    )

    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        max_words = st.slider("최대 단어 수", 30, 300, 120, 10)

    with c2:
        bg = st.selectbox("배경색", ["white", "black"], index=0)

    with c3:
        colormap = st.selectbox("색상 스타일", ["viridis", "plasma", "inferno", "magma", "cividis"], index=0)

    if st.button("✨ 워드클라우드 만들기", key="btn_wc", use_container_width=True):
        if not wc_text.strip():
            st.warning("먼저 글을 붙여 넣어 주세요.")
        else:
            wc = create_wordcloud(wc_text, max_words=max_words, bg=bg, colormap=colormap)

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)


# =========================================================
# Tab 5: Emoji
# =========================================================
with tabs[5]:
    st.subheader("😀 이모지 모음")
    st.caption("큰 이모지 박스에서 필요한 부분을 드래그해서 복사한 뒤 수업 자료, 칠판, 활동지에 붙여 넣으세요.")

    EMOJI_CATEGORIES = {
        "😀 감정/표정": "😀 😃 😄 😁 😆 😅 😂 🤣 🙂 🙃 😉 😊 😇 😍 🥰 😘 😋 😛 😜 🤪 😝 🤗 🤔 😐 😑 😮 😲 😳 🥺 😢 😭 😱 😴 😎 🤓 😡 🤯 👍 👎 👏 🙌 🙏 👌 ✌️ 💪 👀 👂 🧠 🗣️ 👤 👥",
        "📚 수업/학습": "📚 📖 📕 📗 📘 📙 📔 📒 📓 📝 ✏️ 🖊️ 🖍️ 📐 📏 📌 📍 📎 🗂️ 📁 📂 📋 📊 📈 🎓 🏫 🧑‍🏫 👩‍🏫 👨‍🏫 🧑‍🎓 💡 🔍 🔎 🧪 🔬 💻 🖥️ ⌨️ 📱 🎤 🎧",
        "🎯 활동/평가": "🎯 ✅ ☑️ ✔️ ❌ ❎ ⭕ ⭐ 🌟 💯 🏆 🥇 🥈 🥉 🎲 🎮 🧩 🃏 🔔 ⏰ ⏳ 🚀 🔥 🎉 🎊 👏 💬 ❓ ❗ 📢 📣 📝 📋 📌",
        "🌍 장소/세계": "🌍 🌎 🌏 🗺️ 🧭 🏠 🏡 🏫 🏢 🏥 🏦 🏪 🏬 🏭 🏛️ 🏰 🗼 🗽 ⛪ 🕌 🛕 🌉 🌃 🏞️ 🏝️ 🏖️ ⛰️ 🇰🇷 🇺🇸 🇬🇧 🇯🇵 🇨🇳 🇫🇷 🇩🇪 🇨🇦",
        "🚗 교통/여행": "🚗 🚕 🚙 🚌 🚎 🚓 🚑 🚒 🚐 🚚 🛵 🏍️ 🚲 🛴 🚂 🚆 🚇 🚊 🚉 ✈️ 🛫 🛬 🚁 🚀 ⛵ 🚢 ⚓ 🧳 🎒 🛣️ ⛽ 🚦 🚧 🛑 🎫",
        "🍎 음식/생활": "🍎 🍏 🍊 🍋 🍌 🍉 🍇 🍓 🍒 🍑 🍍 🍕 🍔 🍟 🌭 🥪 🍞 🥐 🥚 🍗 🍖 🍜 🍝 🍚 🍱 🍣 🍰 🍪 🍫 ☕ 🥤 🧃 🍽️",
        "🌱 자연/날씨": "☀️ 🌤️ ⛅ 🌥️ ☁️ 🌧️ ⛈️ 🌩️ 🌨️ ❄️ 🌈 💧 🌊 🔥 ⭐ ✨ ⚡ 🌙 🌳 🌲 🌴 🌵 🌱 🌿 🍀 🍁 🍂 🌸 🌻 🐶 🐱 🐻 🐼 🐯 🦁 🐦 🐢 🐟 🐬",
        "🏺 역사/사회": "🏺 🪨 ⚔️ 🛡️ 👑 🏛️ 📜 🕯️ 🪖 🗳️ 🇰🇷 🐻 🌅 🦅 🚢 🏭 🌐 🤝 ⚖️ 🕊️ 📚 📖 📝 🔍 🗺️ 🧭 ⏳",
        "🔢 숫자/기호": "0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟 ⬅️ ➡️ ⬆️ ⬇️ ↗️ ↘️ ↔️ 🔁 🔄 ▶️ ⏸️ ⏹️ ➕ ➖ ✖️ ➗ 🔴 🟠 🟡 🟢 🔵 🟣 ⚫ ⚪"
    }

    emoji_tabs = st.tabs(list(EMOJI_CATEGORIES.keys()))

    def show_big_emoji_box(emojis, height=360):
        safe_emojis = html.escape(emojis.strip())
        emoji_html = f"""
        <html>
        <head>
        <style>
            body {{
                margin:0;
                padding:0;
                background:transparent;
                font-family:Arial, sans-serif;
            }}
            .emoji-box {{
                background:linear-gradient(135deg,#ffffff 0%,#f8fafc 100%);
                border:2px solid #e2e8f0;
                border-radius:22px;
                padding:22px 24px;
                font-size:34px;
                line-height:1.75;
                word-spacing:9px;
                box-shadow:0 5px 14px rgba(0,0,0,0.06);
                user-select:text;
                white-space:pre-wrap;
                overflow-y:auto;
                height:{height - 40}px;
                box-sizing:border-box;
            }}
            @media (max-width: 768px) {{
                .emoji-box {{
                    font-size:28px;
                    line-height:1.7;
                    padding:18px;
                }}
            }}
        </style>
        </head>
        <body>
            <div class="emoji-box">{safe_emojis}</div>
        </body>
        </html>
        """
        components.html(emoji_html, height=height, scrolling=False)

    for tab, (category, emojis) in zip(emoji_tabs, EMOJI_CATEGORIES.items()):
        with tab:
            st.markdown(f"### {category}")
            show_big_emoji_box(emojis, height=390)


# =========================================================
# Tab 6: Grouping
# =========================================================
with tabs[6]:
    st.subheader("👥 조 편성 도구")
    st.caption("CSV를 올리지 않아도 기본 명단으로 조 편성을 할 수 있습니다.")
    st.caption("CSV를 올릴 경우, 반드시 `Course`, `Names` 열이 있어야 합니다.")

    default_data = pd.DataFrame({
        "Course": ["Class 1"] * 10 + ["Class 2"] * 10,
        "Names": [
            "Student 1", "Student 2", "Student 3", "Student 4", "Student 5",
            "Student 6", "Student 7", "Student 8", "Student 9", "Student 10",
            "Student 11", "Student 12", "Student 13", "Student 14", "Student 15",
            "Student 16", "Student 17", "Student 18", "Student 19", "Student 20"
        ]
    })

    uploaded_file = st.file_uploader("🌱 1단계: CSV 파일 올리기. 선택 사항입니다.", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        source_label = "✅ 업로드한 CSV 자료 사용 중"
    else:
        df = default_data
        source_label = "📂 기본 예시 자료 사용 중"

    if all(col in df.columns for col in ["Course", "Names"]):
        st.markdown("### 📋 현재 학생 명단")
        st.dataframe(df, use_container_width=True)

        course_list = df["Course"].dropna().unique().tolist()
        selected_course = st.selectbox("🌱 2단계: 조 편성할 반 선택", course_list)

        course_df = df[df["Course"] == selected_course]
        names = course_df["Names"].dropna().tolist()
        total_students = len(names)

        st.info(
            f"{source_label} | 🎓 **{selected_course}**: "
            f"Total **{total_students}** students available for grouping."
        )

        st.markdown("##### 🌱 3단계: 조 편성 설정")

        col_in1, col_in2 = st.columns(2)

        with col_in1:
            num_group3 = st.number_input("3명 조 개수", min_value=0, value=0, step=1)

        with col_in2:
            num_group4 = st.number_input("4명 조 개수", min_value=0, value=0, step=1)

        needed_students = num_group3 * 3 + num_group4 * 4

        st.write(f"필요한 학생 수: **{needed_students}**")
        st.write(f"현재 학생 수: **{total_students}**")

        if needed_students > total_students:
            st.warning("설정한 조 인원 수가 현재 학생 수보다 많습니다. 조 개수를 줄여 주세요.")

        if st.button("🌱 4단계: 조 편성하기", use_container_width=True):
            if total_students == 0:
                st.warning("조 편성할 학생이 없습니다.")
            elif num_group3 == 0 and num_group4 == 0:
                st.warning("조 개수를 하나 이상 입력해 주세요.")
            else:
                names_for_grouping = names.copy()
                random.shuffle(names_for_grouping)

                grouped_data = []
                group_num = 1
                assigned_count = 0

                for _ in range(num_group3):
                    if len(names_for_grouping) >= 3:
                        members = names_for_grouping[:3]
                        names_for_grouping = names_for_grouping[3:]
                        group_row = {"Group": f"Group {group_num}"}
                        for i, member in enumerate(members):
                            group_row[f"Member{i+1}"] = member
                        grouped_data.append(group_row)
                        group_num += 1
                        assigned_count += 3

                for _ in range(num_group4):
                    if len(names_for_grouping) >= 4:
                        members = names_for_grouping[:4]
                        names_for_grouping = names_for_grouping[4:]
                        group_row = {"Group": f"Group {group_num}"}
                        for i, member in enumerate(members):
                            group_row[f"Member{i+1}"] = member
                        grouped_data.append(group_row)
                        group_num += 1
                        assigned_count += 4

                if names_for_grouping:
                    group_row = {"Group": f"Group {group_num} (Remainder)"}
                    for i, member in enumerate(names_for_grouping):
                        group_row[f"Member{i+1}"] = member
                    grouped_data.append(group_row)
                    assigned_count += len(names_for_grouping)

                if not grouped_data:
                    st.warning("조가 만들어지지 않았습니다. 설정을 확인해 주세요.")
                else:
                    grouped_df = pd.DataFrame(grouped_data)
                    cols = ["Group"] + [c for c in grouped_df.columns if c.startswith("Member")]
                    grouped_df = grouped_df[cols].fillna("")

                    st.success(
                        f"✅ Grouping Complete! "
                        f"Total {assigned_count} students assigned to {len(grouped_data)} groups."
                    )

                    st.dataframe(grouped_df, use_container_width=True)

                    csv_text = grouped_df.to_csv(index=False)
                    csv_bytes = csv_text.encode("utf-8-sig")

                    st.download_button(
                        label="📥 조 편성 결과 CSV 다운로드",
                        data=csv_bytes,
                        file_name=f"grouped_{selected_course.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
    else:
        st.error("파일에는 반드시 `Course`, `Names` 열이 있어야 합니다.")


# =========================================================
# Tab 7: Translation
# =========================================================
with tabs[7]:
    st.subheader("🌐 번역기")
    st.caption("앱 안에서 번역 패키지를 실행하지 않고, 구글 번역 페이지로 연결합니다. 발음도 구글 번역에서 들을 수 있습니다.")

    lang_options = {
        "영어 English": "en",
        "한국어 Korean": "ko",
        "일본어 Japanese": "ja",
        "중국어 Chinese Simplified": "zh-CN",
        "스페인어 Spanish": "es",
        "프랑스어 French": "fr",
        "독일어 German": "de",
        "러시아어 Russian": "ru",
        "베트남어 Vietnamese": "vi",
        "태국어 Thai": "th",
        "인도네시아어 Indonesian": "id",
        "아랍어 Arabic": "ar",
        "힌디어 Hindi": "hi",
        "이탈리아어 Italian": "it",
        "포르투갈어 Portuguese": "pt",
    }

    col1, col2 = st.columns(2)

    with col1:
        source_lang_label = st.selectbox(
            "원문 언어",
            ["자동 감지 Auto"] + list(lang_options.keys()),
            index=0,
            key="source_lang_label_link_only"
        )

    with col2:
        target_lang_label = st.selectbox(
            "번역할 언어",
            list(lang_options.keys()),
            index=0,
            key="target_lang_label_link_only"
        )

    source_text = st.text_area(
        "번역할 문장을 입력하세요",
        height=180,
        placeholder="예: 나는 축구를 좋아합니다. / I like soccer.",
        key="translation_source_input_link_only"
    )

    source_code = "auto" if source_lang_label == "자동 감지 Auto" else lang_options[source_lang_label]
    target_code = lang_options[target_lang_label]

    if source_text.strip():
        encoded_text = urllib.parse.quote(source_text.strip())

        google_translate_url = (
            "https://translate.google.com/?sl="
            + source_code
            + "&tl="
            + target_code
            + "&text="
            + encoded_text
            + "&op=translate"
        )

        safe_url = html.escape(google_translate_url, quote=True)

        st.markdown(
            f"""
            <div style="
                background:linear-gradient(135deg,#ffffff,#f1f7ff);
                border:1px solid #d8e8ff;
                border-radius:18px;
                padding:22px 24px;
                margin-top:16px;
                margin-bottom:16px;
                box-shadow:0 4px 12px rgba(0,0,0,0.06);
            ">
                <div style="font-size:18px; font-weight:800; color:#1f2937; margin-bottom:10px;">
                    🌐 구글 번역으로 이동
                </div>
                <div style="font-size:15px; line-height:1.7; color:#374151; margin-bottom:16px;">
                    아래 버튼을 누르면 입력한 문장이 구글 번역에 자동으로 들어갑니다.<br>
                    이동한 뒤 스피커 아이콘을 누르면 발음도 들을 수 있습니다.
                </div>
                <a href="{safe_url}" target="_blank" style="
                    display:block;
                    text-align:center;
                    background:#2563eb;
                    color:white;
                    text-decoration:none;
                    font-size:20px;
                    font-weight:800;
                    padding:14px 18px;
                    border-radius:14px;
                ">
                    🔊 구글 번역에서 번역하고 발음 듣기
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("🔗 링크가 열리지 않을 때 사용할 주소 보기"):
            st.write(google_translate_url)
            st.caption("위 주소를 복사해서 새 창에 붙여 넣어도 됩니다.")
    else:
        st.info("번역할 문장을 입력하면 구글 번역으로 이동하는 버튼이 나타납니다.")


# =========================================================
# Tab 8: Teacher Request
# =========================================================
with tabs[8]:
    st.subheader("🙋 선생님께 부탁해요")

    safe_doc_url = html.escape(
        "https://docs.google.com/document/d/1kjXveuOIiRQnrcWiyvSsS0DeXSqEe4bphDr0_DSkQyk/edit?tab=t.0",
        quote=True
    )

    st.markdown(
        f"""
        <div style="
            background:linear-gradient(135deg,#eff6ff 0%,#fdf4ff 45%,#fff7ed 100%);
            border:1.5px solid #c4b5fd;
            border-radius:28px;
            padding:26px 24px;
            margin-top:8px;
            margin-bottom:20px;
            box-shadow:0 8px 22px rgba(124,58,237,0.12);
        ">
            <div style="font-size:34px; font-weight:900; color:#312e81; margin-bottom:10px;">
                🙋 선생님께 부탁해요
            </div>
            <div style="font-size:18px; font-weight:800; color:#475569; line-height:1.7;">
                수업 중 듣고 싶은 노래, 하고 싶은 활동, 선생님께 부탁하고 싶은 내용을 자유롭게 적어 주세요.<br>
                아래 버튼을 누르면 구글 문서로 이동합니다.
            </div>
        </div>

        <div style="
            background:#ffffff;
            border:1px solid #e5e7eb;
            border-radius:22px;
            padding:26px;
            text-align:center;
            box-shadow:0 5px 14px rgba(0,0,0,0.06);
            margin-bottom:16px;
        ">
            <a href="{safe_doc_url}" target="_blank" style="
                display:block;
                width:100%;
                box-sizing:border-box;
                background:linear-gradient(135deg,#2563eb,#7c3aed);
                color:white;
                text-decoration:none;
                font-size:22px;
                font-weight:900;
                padding:18px 22px;
                border-radius:18px;
                box-shadow:0 8px 18px rgba(37,99,235,0.22);
            ">
                📝 선생님께 부탁하러 가기
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("🔗 링크가 열리지 않을 때 사용할 주소 보기"):
        st.write("https://docs.google.com/document/d/1kjXveuOIiRQnrcWiyvSsS0DeXSqEe4bphDr0_DSkQyk/edit?tab=t.0")
        st.caption("위 주소를 복사해서 새 창에 붙여 넣어도 됩니다.")

    st.info("구글 문서 공유 설정이 '링크가 있는 모든 사용자 편집 가능'이어야 학생들이 쓸 수 있습니다.")
