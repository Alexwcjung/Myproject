# Pop Song Master Class 수정용 전체 교체 블록
# 아래 블록들을 기존 코드의 해당 위치에 그대로 교체/삽입하세요.
# 변경 내용:
# 1) 문장 매칭 게임: 완료 버튼 없이 PDF 인증서 버튼 바로 표시
# 2) Grammar: 완료 시 PDF 인증서 바로 표시
# 3) 가사와 이해도 퀴즈: 통과 후 제일 밑에 큰 PDF 버튼 표시
# 4) Let's / Let’s / Let us 인식 오류 수정
# 5) Grammar Practice에서 틀린 뒤 다시 맞히면 점수 갱신되도록 수정


# =========================================================
# 1. show_mission_pdf_download 함수 전체 교체
# =========================================================

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


# =========================================================
# 2. show_integrated_quiz_tab 함수 안 수정
# =========================================================
# show_integrated_quiz_tab(song_choice, data) 함수 안에서
# score >= pass_score 부분을 아래처럼 바꾸세요.
#
# 기존:
# if score >= pass_score:
#     ...
#     show_mission_pdf_download(...)
#
# 교체:


# 아래 코드는 show_integrated_quiz_tab 함수 내부에서 사용합니다.

        if score >= pass_score:
            st.success(f"통과했습니다! {len(questions)}문제 중 {score}문제를 맞혔습니다.")
            st.session_state[f"mission_{key_key}_lyrics_quiz"] = True
            st.session_state[f"mission_{key_key}_lyrics_quiz_detail"] = f"가사 이해도 퀴즈 완료 / 점수: {score}/{len(questions)}"
            st.balloons()
        else:
            st.warning(f"아직 통과 기준에 부족합니다. 통과 기준은 {pass_score}/{len(questions)} 이상입니다.")


# 그리고 show_integrated_quiz_tab 함수의 맨 끝, 즉 함수 종료 직전에 아래 코드를 추가하세요.
# 들여쓰기 4칸 유지가 중요합니다.

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


# =========================================================
# 3. check_target_grammar_sentence 함수 안 수정
# =========================================================
# 함수 초반의 raw/s/low 만드는 부분을 아래로 교체하세요.

    raw = str(sentence).strip()
    raw = raw.replace("’", "'").replace("‘", "'").replace("`", "'")
    s = re.sub(r"\s+", " ", raw)
    low = s.lower().strip()


# 그리고 target == "Let's + 동사" 부분을 아래로 교체하세요.

    if target == "Let's + 동사":
        if re.search(r"\b(let's|let us)\s+(?!to\b)[a-zA-Z']+", low):
            return ok("좋아요. 함께 하자고 제안하는 Let's + 동사 형태를 잘 썼습니다.")
        if re.search(r"\b(let's|let us)\s+to\s+[a-zA-Z']+", low):
            return no("Let's 뒤에는 to를 쓰지 않고 동사를 바로 씁니다. 예: Let's skip the club.")
        return no("Let's + 동사 구조를 써 보세요. 예: Let's study English. / Let's skip the club.")


# =========================================================
# 4. show_song_grammar_tab 함수 안 Controlled Practice 수정
# =========================================================
# 기존 코드:
# if st.button("정답 확인", key=f"{prefix}cp_check_btn_{i}"):
#     if check_key not in st.session_state:
#         st.session_state[check_key] = choice == answer
#
# 아래로 교체하세요.

        if st.button("정답 확인", key=f"{prefix}cp_check_btn_{i}"):
            st.session_state[check_key] = choice == answer


# =========================================================
# 5. show_song_grammar_tab 함수 맨 아래 Grammar 인증서 부분 교체
# =========================================================
# 기존:
# if grammar_complete:
#     st.session_state[f"mission_{grammar_key}_grammar"] = True
#
# if st.session_state.get(f"mission_{grammar_key}_grammar"):
#     show_mission_pdf_download(...)
#
# 아래로 교체하세요.

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


# =========================================================
# 6. 문장 매칭 게임 탭 맨 아래 수정
# =========================================================
# elif selected_tab == "🧩 문장 매칭 게임": 안의 맨 아래에서
# 기존 완료 버튼 구간 전체를 아래 코드로 교체하세요.
#
# 기존 구간:
# st.markdown("---")
# st.markdown("### 📄 문장 매칭 게임 완료 인증")
# st.info(...)
# if st.button("문장 매칭을 모두 끝냈습니다", ...):
#     ...
# if st.session_state.get(...):
#     show_mission_pdf_download(...)
#
# 교체:

    st.markdown("---")
    st.markdown("## 📄 문장 매칭 게임 PDF 인증서")

    show_mission_pdf_download(
        song_choice,
        "문장 매칭 게임",
        f"{match_key}_matching_direct",
        "문장 매칭 게임 활동 완료",
        big=True,
        show_message=False
    )


# =========================================================
# 적용 후 확인할 것
# =========================================================
# requirements.txt에 아래가 들어 있어야 PDF 저장이 됩니다.
#
# reportlab>=4.0.0
# gTTS
# deep-translator
#
# 문장 매칭은 Streamlit이 JS 컴포넌트 내부 완료 상태를 직접 알 수 없으므로,
# "정말 완료했는지 자동 감지"는 현재 구조에서는 어렵습니다.
# 대신 버튼을 누르지 않아도 PDF 인증서 버튼이 바로 보이도록 수정했습니다.
#
# Grammar 인증서가 안 뜨던 문제는 대부분 정답 확인 상태가 갱신되지 않아서 생긴 문제입니다.
# st.session_state[check_key] = choice == answer 로 바꾸면,
# 처음 틀린 뒤 다시 맞혀도 점수가 갱신됩니다.
