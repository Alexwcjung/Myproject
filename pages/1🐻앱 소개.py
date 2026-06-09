import streamlit as st
import os

# =====================================================
# 재미있는 영어 놀이터 / 앱 소개 첫 페이지
# 앱 소개 + 소개 영상 1개
# =====================================================

st.set_page_config(
    page_title="재미있는 영어 놀이터",
    page_icon="🎡",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fff7fb 0%, #ffffff 55%, #f8fffb 100%);
    }

    .hero-box {
        background: linear-gradient(135deg, #ffffff 0%, #fff1f7 52%, #fce7f3 100%);
        padding: 44px 36px;
        border-radius: 32px;
        color: #1f2937;
        box-shadow: 0 12px 32px rgba(244, 114, 182, 0.18);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        border: 1px solid #fbcfe8;
    }

    .hero-box::after {
        content: "🌍";
        position: absolute;
        right: 28px;
        top: 16px;
        font-size: 96px;
        opacity: 0.14;
    }

    .hero-box::before {
        content: "🌸";
        position: absolute;
        right: 120px;
        bottom: 12px;
        font-size: 72px;
        opacity: 0.18;
    }

    .hero-title {
        font-size: 50px;
        font-weight: 1000;
        letter-spacing: -1px;
        margin-bottom: 10px;
        color: #0f172a;
        line-height: 1.15;
    }

    .hero-subtitle {
        font-size: 20px;
        line-height: 1.6;
        font-weight: 800;
        color: #475569;
    }

    .pill {
        display: inline-block;
        background: rgba(255,255,255,0.85);
        padding: 8px 15px;
        border-radius: 999px;
        font-size: 15px;
        font-weight: 900;
        margin-right: 8px;
        margin-top: 18px;
        color: #be185d;
        border: 1px solid #fbcfe8;
    }

    .section-title {
        font-size: 29px;
        font-weight: 1000;
        color: #0f172a;
        margin-top: 18px;
        margin-bottom: 14px;
    }

    .intro-box {
        background: white;
        padding: 28px 26px;
        border-radius: 28px;
        border: 1px solid #fbcfe8;
        box-shadow: 0 8px 24px rgba(244, 114, 182, 0.09);
        margin-bottom: 24px;
    }

    .intro-text {
        font-size: 17px;
        line-height: 1.85;
        color: #334155;
    }

    .card {
        background: white;
        padding: 24px 22px;
        border-radius: 26px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.07);
        height: 100%;
    }

    .card-icon {
        font-size: 36px;
        margin-bottom: 8px;
    }

    .card-title {
        font-size: 21px;
        font-weight: 1000;
        color: #0f172a;
        margin-bottom: 8px;
    }

    .card-text {
        font-size: 16px;
        line-height: 1.7;
        color: #475569;
    }

    .mini-box {
        background: linear-gradient(135deg, #ffffff 0%, #fff1f7 100%);
        padding: 22px;
        border-radius: 24px;
        border: 1px solid #fbcfe8;
        box-shadow: 0 8px 20px rgba(244, 114, 182, 0.1);
        height: 100%;
    }

    .mini-title {
        font-size: 22px;
        font-weight: 1000;
        color: #be185d;
        margin-bottom: 8px;
    }

    .mini-text {
        font-size: 17px;
        line-height: 1.8;
        color: #334155;
    }

    .flower-line {
        text-align: center;
        font-size: 25px;
        margin: 22px 0;
        opacity: 0.85;
    }

    .video-wrap {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 28px;
        padding: 22px 24px;
        margin-top: 12px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.07);
    }

    .video-title {
        font-size: 24px;
        font-weight: 1000;
        color: #0f172a;
        margin-bottom: 14px;
    }

    .missing-box {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 20px;
        padding: 16px 18px;
        color: #7c2d12;
        font-size: 15px;
        font-weight: 800;
        line-height: 1.7;
    }

    @media (max-width: 768px) {
        .hero-box {
            padding: 32px 22px;
            border-radius: 24px;
        }

        .hero-title {
            font-size: 35px;
        }

        .hero-subtitle {
            font-size: 17px;
        }

        .section-title {
            font-size: 23px;
        }

        .intro-box {
            padding: 22px 20px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Hero
# =========================
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🎡 재미있는 영어 놀이터</div>
        <div class="hero-subtitle">
            쉬운 영어를 먼저 듣고, 짧게 말하며 익히는 영어 학습 앱
        </div>
        <div>
            <span class="pill">🔊 듣기 먼저</span>
            <span class="pill">🗣️ 말하기 먼저</span>
            <span class="pill">🎵 노래와 영상</span>
            <span class="pill">🌸 쉬운 표현부터</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# Intro
# =========================
st.markdown(
    """
    <div class="intro-box">
        <div class="intro-text">
            <b>재미있는 영어 놀이터</b>는 영어를 처음부터 어렵게 공부하는 앱이 아닙니다.<br>
            학생들이 실제 생활에서 쓸 수 있는 쉬운 단어와 문장을
            <b>듣고, 따라 말하고, 다시 확인하면서</b> 영어에 익숙해지는 공간입니다.
            <br><br>
            영어는 소리에 익숙해지고, 입으로 짧은 표현을 말해 보는 것이 중요합니다.
            이 앱은 학생들이 부담 없이 영어를 듣고 말하며 자신감을 기를 수 있도록 설계되었습니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# Main Focus
# =========================
st.markdown('<div class="section-title">🌱 앱의 중심 활동</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🔊</div>
            <div class="card-title">듣기</div>
            <div class="card-text">
                단어와 문장을 반복해서 들으며 영어 소리에 익숙해집니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">🗣️</div>
            <div class="card-title">말하기</div>
            <div class="card-text">
                들은 표현을 직접 따라 말하며 영어를 입에 붙입니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="card">
            <div class="card-icon">📖</div>
            <div class="card-title">읽기와 확인</div>
            <div class="card-text">
                짧은 글과 간단한 활동으로 배운 표현을 다시 확인합니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="flower-line">🌸 🌿 🌸</div>', unsafe_allow_html=True)

# =========================
# Extra
# =========================
left, right = st.columns([1.1, 1])

with left:
    st.markdown(
        """
        <div class="mini-box">
            <div class="mini-title">🎵 노래와 영상도 함께</div>
            <div class="mini-text">
                영어 노래와 영상은 흥미를 높이기 위한 활동으로 활용합니다.
                익숙한 멜로디와 장면을 통해 표현을 더 자연스럽게 만날 수 있습니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        """
        <div class="mini-box">
            <div class="mini-title">💬 오늘의 메시지</div>
            <div class="mini-text">
                완벽하지 않아도 괜찮습니다.<br>
                두려움 없이 듣고 말해 봅시다.<br>
                한 단어, 한 문장씩 천천히 익히며
                영어를 사용할 수 있다는 자신감을 기릅니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# Video Section
# =========================
st.markdown('<div class="section-title">🎬 앱 소개 영상</div>', unsafe_allow_html=True) 

video_path = "videos/스마트폰_영어_아지트.mp4"

st.markdown("<div class='video-wrap'>", unsafe_allow_html=True)

if os.path.exists(video_path):
    st.video(video_path)
else:
    st.markdown(
        f"""
        <div class="missing-box">
            영상 파일을 찾을 수 없습니다.<br>
            현재 찾고 있는 경로:<br>
            <code>{video_path}</code><br><br>
            GitHub의 <b>videos</b> 폴더 안 파일명과 코드의 파일명이 정확히 같은지 확인하세요.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

st.caption("🌸 재미있는 영어 놀이터 · Listening and Speaking First")
