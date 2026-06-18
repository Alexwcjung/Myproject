# -*- coding: utf-8 -*-
"""
Pop Song Master Class 전체 txt 자동 수정기

사용법
1. 이 파일을 기존 전체 txt 파일과 같은 폴더에 넣으세요.
2. 기존 전체 txt 파일 이름을 ORIGINAL_FILE에 적으세요.
3. 실행하면 수정된 전체 txt 파일이 OUTPUT_FILE 이름으로 생성됩니다.

수정 내용
- 문장 매칭 게임: 완료 버튼 없이 PDF 인증서 버튼 바로 표시
- Grammar: 완료 시 큰 PDF 인증서 버튼 표시
- 가사와 이해도 퀴즈: 통과 후 제일 밑에 큰 PDF 버튼 표시
- Let's / Let’s / Let us 인식 오류 수정
- Grammar Practice에서 틀린 뒤 다시 맞히면 점수 갱신
"""

from pathlib import Path
import re

ORIGINAL_FILE = "pop_song_master_class_every_breath_you_take_21_forever_young_added (1).txt"
OUTPUT_FILE = "pop_song_master_class_every_breath_you_take_21_forever_young_FIXED_FULL.txt"

NEW_SHOW_MISSION_PDF_DOWNLOAD = '''def show_mission_pdf_download(song_choice, activity_name, mission_key, detail_text="", big=False, show_message=True):
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
'''


def replace_function(text, func_name, new_func):
    start = text.find(f"def {func_name}(")
    if start == -1:
        raise ValueError(f"{func_name} 함수를 찾지 못했습니다.")

    # 다음 top-level def/class 또는 큰 데이터 블록 시작 전까지 교체
    next_candidates = []
    for pat in ["\ndef ", "\nclass ", "\nGRAMMAR_POINTS", "\nSONGS", "\nBACKGROUND_CONTENT"]:
        idx = text.find(pat, start + 1)
        if idx != -1:
            next_candidates.append(idx)
    if not next_candidates:
        end = len(text)
    else:
        end = min(next_candidates)

    return text[:start] + new_func.rstrip() + "\n\n" + text[end:].lstrip("\n")


def patch_show_integrated_quiz_tab(text):
    old = '''        if score >= pass_score:
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
            st.warning(f"아직 통과 기준에 부족합니다. 통과 기준은 {pass_score}/{len(questions)} 이상입니다.")'''

    new = '''        if score >= pass_score:
            st.success(f"통과했습니다! {len(questions)}문제 중 {score}문제를 맞혔습니다.")
            st.session_state[f"mission_{key_key}_lyrics_quiz"] = True
            st.session_state[f"mission_{key_key}_lyrics_quiz_detail"] = f"가사 이해도 퀴즈 완료 / 점수: {score}/{len(questions)}"
            st.balloons()
        else:
            st.warning(f"아직 통과 기준에 부족합니다. 통과 기준은 {pass_score}/{len(questions)} 이상입니다.")'''

    if old in text:
        text = text.replace(old, new)

    bottom_block = '''
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
'''

    if 'f"{key_key}_lyrics_quiz_bottom"' not in text:
        marker = "\n\ndef check_target_grammar_sentence"
        if marker in text:
            text = text.replace(marker, bottom_block + marker, 1)
        else:
            raise ValueError("show_integrated_quiz_tab 끝 위치를 찾지 못했습니다.")

    return text


def patch_check_target_grammar_sentence(text):
    text = text.replace(
        '''    raw = str(sentence).strip()
    s = re.sub(r"\\s+", " ", raw)
    low = s.lower().strip()''',
        '''    raw = str(sentence).strip()
    raw = raw.replace("’", "'").replace("‘", "'").replace("`", "'")
    s = re.sub(r"\\s+", " ", raw)
    low = s.lower().strip()'''
    )

    old = '''    if target == "Let's + 동사":
        if re.search(r"\\blet's\\s+(?!to\\b)\\w+", low) or re.search(r"\\blet\\s+us\\s+(?!to\\b)\\w+", low):
            return ok("좋아요. 함께 하자고 제안하는 Let's + 동사 형태를 잘 썼습니다.")
        if re.search(r"\\blet's\\s+to\\s+\\w+", low):
            return no("Let's 뒤에는 to를 쓰지 않고 동사를 바로 씁니다. 예: Let's skip the club.")
        return no("Let's + 동사 구조를 써 보세요. 예: Let's study English.")'''

    new = '''    if target == "Let's + 동사":
        if re.search(r"\\b(let's|let us)\\s+(?!to\\b)[a-zA-Z']+", low):
            return ok("좋아요. 함께 하자고 제안하는 Let's + 동사 형태를 잘 썼습니다.")
        if re.search(r"\\b(let's|let us)\\s+to\\s+[a-zA-Z']+", low):
            return no("Let's 뒤에는 to를 쓰지 않고 동사를 바로 씁니다. 예: Let's skip the club.")
        return no("Let's + 동사 구조를 써 보세요. 예: Let's study English. / Let's skip the club.")'''

    if old in text:
        text = text.replace(old, new)
    else:
        pattern = r'''    if target == "Let's \+ 동사":.*?\n\n    if target == "gonna be \+ 형용사":'''
        text = re.sub(pattern, new + '\n\n    if target == "gonna be + 형용사":', text, flags=re.S)

    return text


def patch_grammar_practice_and_certificate(text):
    text = text.replace(
        '''        if st.button("정답 확인", key=f"{prefix}cp_check_btn_{i}"):
            if check_key not in st.session_state:
                st.session_state[check_key] = choice == answer''',
        '''        if st.button("정답 확인", key=f"{prefix}cp_check_btn_{i}"):
            st.session_state[check_key] = choice == answer'''
    )

    old = '''    if grammar_complete:
        st.session_state[f"mission_{grammar_key}_grammar"] = True

    if st.session_state.get(f"mission_{grammar_key}_grammar"):
        show_mission_pdf_download(
            song_choice,
            "Grammar",
            f"{grammar_key}_grammar",
            f"Grammar 활동 완료 / Grammar Practice 점수: {score}/{len(questions)}"
        )'''

    new = '''    if grammar_complete:
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
        )'''

    if old in text:
        text = text.replace(old, new)
    else:
        pattern = r'''    if grammar_complete:\n        st\.session_state\[f"mission_\{grammar_key\}_grammar"\] = True\n\n    if st\.session_state\.get\(f"mission_\{grammar_key\}_grammar"\):\n        show_mission_pdf_download\(\n            song_choice,\n            "Grammar",\n            f"\{grammar_key\}_grammar",\n            f"Grammar 활동 완료 / Grammar Practice 점수: \{score\}/\{len\(questions\)\}"\n        \)'''
        text = re.sub(pattern, new, text)

    return text


def patch_matching_certificate(text):
    old = '''    st.markdown("---")
    st.markdown("### 📄 문장 매칭 게임 완료 인증")
    st.info("문장 매칭 게임을 모두 끝낸 뒤 아래 버튼을 눌러 PDF 인증서를 저장하세요.")

    if st.button("문장 매칭을 모두 끝냈습니다", key=f"matching_done_{match_key}", use_container_width=True):
        st.session_state[f"mission_{match_key}_matching"] = True

    if st.session_state.get(f"mission_{match_key}_matching"):
        show_mission_pdf_download(
            song_choice,
            "문장 매칭 게임",
            f"{match_key}_matching",
            "문장 매칭 게임 활동 완료"
        )'''

    new = '''    st.markdown("---")
    st.markdown("## 📄 문장 매칭 게임 PDF 인증서")

    show_mission_pdf_download(
        song_choice,
        "문장 매칭 게임",
        f"{match_key}_matching_direct",
        "문장 매칭 게임 활동 완료",
        big=True,
        show_message=False
    )'''

    if old in text:
        return text.replace(old, new)

    pattern = r'''    st\.markdown\("---"\)\n    st\.markdown\("### 📄 문장 매칭 게임 완료 인증"\).*?show_mission_pdf_download\(\n            song_choice,\n            "문장 매칭 게임",\n            f"\{match_key\}_matching",\n            "문장 매칭 게임 활동 완료"\n        \)'''
    return re.sub(pattern, new, text, flags=re.S)


def main():
    src = Path(ORIGINAL_FILE)
    if not src.exists():
        raise FileNotFoundError(
            f"원본 파일을 찾지 못했습니다: {ORIGINAL_FILE}\n"
            "이 수정기 파일과 같은 폴더에 원본 전체 txt 파일을 넣거나, ORIGINAL_FILE 값을 실제 파일명으로 바꾸세요."
        )

    text = src.read_text(encoding="utf-8")

    text = replace_function(text, "show_mission_pdf_download", NEW_SHOW_MISSION_PDF_DOWNLOAD)
    text = patch_show_integrated_quiz_tab(text)
    text = patch_check_target_grammar_sentence(text)
    text = patch_grammar_practice_and_certificate(text)
    text = patch_matching_certificate(text)

    out = Path(OUTPUT_FILE)
    out.write_text(text, encoding="utf-8")
    print(f"완료: {out.resolve()}")


if __name__ == "__main__":
    main()
