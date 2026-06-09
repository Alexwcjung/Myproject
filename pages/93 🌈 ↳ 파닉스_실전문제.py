import streamlit as st
from gtts import gTTS
import io
import html

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="Phonics Speaking Practice",
    page_icon="🗣️",
    layout="wide"
)

st.title("🗣️ Phonics Speaking Practice")
st.caption("스펠링을 보고 먼저 말한 뒤, 원어민 발음을 듣고, 단어의 소리를 이해해 봅시다.")

# =========================
# CSS
# =========================
st.markdown(
    """
    <style>
    .guide-box {
        border-left: 7px solid #ff9f1c;
        background: linear-gradient(135deg, #fff7e6, #fff0f5);
        padding: 18px 20px;
        border-radius: 18px;
        margin-bottom: 24px;
        line-height: 1.8;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .mini-card {
        background: linear-gradient(135deg, #f8fbff, #ffffff);
        border: 1px solid #dbeafe;
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 12px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
    }

    .pattern-title {
        font-size: 24px;
        font-weight: 900;
        color: #1e3a8a;
        margin-bottom: 4px;
    }

    .sound-text {
        font-size: 15px;
        font-weight: 800;
        color: #475569;
        margin-bottom: 8px;
    }

    .word-wrap {
        line-height: 2.3;
        margin-top: 4px;
        margin-bottom: 6px;
    }

    .word-pill {
        display: inline-block;
        background: #eef2ff;
        color: #111827;
        font-size: 22px;
        font-weight: 900;
        padding: 6px 13px;
        border-radius: 999px;
        margin: 4px 4px;
        border: 1px solid #c7d2fe;
    }

    .explain-box {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #7c2d12;
        border-radius: 14px;
        padding: 10px 12px;
        font-size: 15px;
        line-height: 1.6;
        margin-top: 8px;
    }

    .category-guide {
        background-color:#f8fbff;
        border:1px solid #dbeafe;
        border-radius:16px;
        padding:14px 16px;
        margin-bottom:18px;
        line-height:1.7;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 800;
        padding: 0.35rem 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 안내 박스
# =========================
st.markdown(
    """
    <div class="guide-box">
        <div style="font-size:22px; font-weight:900; margin-bottom:10px;">
            📌 연습 방법
        </div>
        <div>👀 화면에 보이는 <b>영어 단어</b>를 먼저 큰 소리로 읽습니다.</div>
        <div>🔊 <b>원어민 발음 듣기</b> 버튼을 눌러 실제 발음을 확인합니다.</div>
        <div>💡 설명을 보며 <b>글자와 소리의 관계</b>를 이해해 봅니다.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# TTS 함수
# =========================
@st.cache_data
def make_tts_audio(text, lang="en", tld="com"):
    fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


def play_audio(text, key):
    if st.button("🔊 발음 듣기", key=key):
        audio_bytes = make_tts_audio(text)
        st.audio(audio_bytes, format="audio/mp3")


# =========================
# 연습 데이터
# =========================
practice_sets = {
    "① 자음 소리": [
        {"pattern": "B b", "sound": "/b/", "words": ["bat", "bus", "ball", "bed", "big"], "explain": "B는 /b/ 소리입니다. 입술을 붙였다가 떼며 '브'에 가깝게 소리 냅니다."},
        {"pattern": "C c", "sound": "/k/", "words": ["cat", "cup", "can", "cot", "cap"], "explain": "C는 기본적으로 /k/ 소리로 나는 경우가 많습니다."},
        {"pattern": "D d", "sound": "/d/", "words": ["dog", "desk", "dad", "duck", "day"], "explain": "D는 /d/ 소리입니다. 혀끝을 윗잇몸 근처에 대었다가 떼며 소리 냅니다."},
        {"pattern": "F f", "sound": "/f/", "words": ["fish", "fan", "fox", "fun", "five"], "explain": "F는 /f/ 소리입니다. 윗니를 아랫입술에 가볍게 대고 바람을 냅니다."},
        {"pattern": "G g", "sound": "/g/", "words": ["goat", "gum", "girl", "game", "gas"], "explain": "G는 기본적으로 /g/ 소리로 납니다."},
        {"pattern": "H h", "sound": "/h/", "words": ["hat", "hen", "hot", "home", "hand"], "explain": "H는 숨을 내보내는 /h/ 소리입니다."},
        {"pattern": "J j", "sound": "/dʒ/", "words": ["jam", "jet", "jump", "job", "jelly"], "explain": "J는 /dʒ/ 소리입니다. '즈'와 '쥬' 사이처럼 들립니다."},
        {"pattern": "K k", "sound": "/k/", "words": ["kite", "king", "key", "kid", "kick"], "explain": "K는 /k/ 소리입니다."},
        {"pattern": "L l", "sound": "/l/", "words": ["lion", "leg", "leaf", "lamp", "lake"], "explain": "L은 혀끝을 윗잇몸에 대며 내는 소리입니다."},
        {"pattern": "M m", "sound": "/m/", "words": ["moon", "man", "milk", "map", "mom"], "explain": "M은 입술을 붙이고 코로 울리며 내는 소리입니다."},
        {"pattern": "N n", "sound": "/n/", "words": ["nest", "nose", "nine", "net", "name"], "explain": "N은 혀끝을 윗잇몸에 대고 코로 울리며 내는 소리입니다."},
        {"pattern": "P p", "sound": "/p/", "words": ["pig", "pen", "pot", "park", "pet"], "explain": "P는 입술을 붙였다가 터뜨리듯 내는 소리입니다."},
        {"pattern": "Q q", "sound": "/kw/", "words": ["queen", "quick", "quiz", "quiet", "quilt"], "explain": "Q는 보통 qu로 쓰이며 /kw/ 소리로 납니다."},
        {"pattern": "R r", "sound": "/r/", "words": ["red", "run", "rabbit", "rain", "rice"], "explain": "R은 혀를 뒤로 살짝 당겨 내는 영어식 r 소리입니다."},
        {"pattern": "S s", "sound": "/s/", "words": ["sun", "sit", "sad", "six", "sock"], "explain": "S는 바람이 새어 나가는 /s/ 소리입니다."},
        {"pattern": "T t", "sound": "/t/", "words": ["top", "ten", "tiger", "tap", "toy"], "explain": "T는 혀끝을 윗잇몸 근처에 대었다가 떼며 내는 소리입니다."},
        {"pattern": "V v", "sound": "/v/", "words": ["van", "vet", "vest", "vase", "very"], "explain": "V는 /v/ 소리입니다. F와 달리 목소리가 울립니다."},
        {"pattern": "W w", "sound": "/w/", "words": ["window", "wet", "win", "water", "walk"], "explain": "W는 입술을 둥글게 모아 시작하는 소리입니다."},
        {"pattern": "X x", "sound": "/ks/", "words": ["fox", "box", "six", "taxi", "mix"], "explain": "X는 /ks/ 소리로 나는 경우가 많습니다."},
        {"pattern": "Y y", "sound": "/j/", "words": ["yes", "yellow", "yo-yo", "yard", "young"], "explain": "Y는 단어 앞에서 /j/ 소리로 납니다."},
        {"pattern": "Z z", "sound": "/z/", "words": ["zebra", "zip", "zero", "zoo", "zigzag"], "explain": "Z는 목소리가 울리는 /z/ 소리입니다."},
    ],

    "② 짧은 모음": [
        {"pattern": "short a", "sound": "/æ/", "words": ["cat", "bat", "hat", "map", "bag", "fan", "jam", "sad"], "explain": "짧은 a는 /æ/ 소리입니다. '애'에 가까운 소리입니다."},
        {"pattern": "short e", "sound": "/e/", "words": ["bed", "pen", "egg", "ten", "red", "hen", "desk", "pet"], "explain": "짧은 e는 /e/ 소리입니다. '에'에 가까운 소리입니다."},
        {"pattern": "short i", "sound": "/ɪ/", "words": ["sit", "pig", "fish", "six", "milk", "big", "win", "kid"], "explain": "짧은 i는 /ɪ/ 소리입니다. 한국어 '이'보다 짧고 힘을 빼서 냅니다."},
        {"pattern": "short o", "sound": "/ɑ/", "words": ["hot", "dog", "box", "fox", "pot", "top", "cot", "rock"], "explain": "짧은 o는 /ɑ/ 계열 소리로 나는 경우가 많습니다."},
        {"pattern": "short u", "sound": "/ʌ/", "words": ["cup", "bus", "sun", "run", "fun", "duck", "gum", "jump"], "explain": "짧은 u는 /ʌ/ 소리입니다. 짧은 '어'에 가깝습니다."},
    ],

    "③ 긴 모음": [
        {"pattern": "long a", "sound": "/eɪ/", "words": ["cake", "name", "make", "lake", "game", "rain", "day", "play"], "explain": "긴 a는 /eɪ/ 소리입니다. gTTS 오류를 줄이기 위해 단어로 듣는 방식이 안정적입니다."},
        {"pattern": "long e", "sound": "/iː/", "words": ["see", "tree", "green", "bee", "feet", "eat", "sea", "teach"], "explain": "긴 e는 /iː/ 소리입니다. 길고 선명한 '이' 소리입니다."},
        {"pattern": "long i", "sound": "/aɪ/", "words": ["bike", "five", "kite", "time", "line", "ride", "like", "nine"], "explain": "긴 i는 /aɪ/ 소리입니다. '아이'에 가깝습니다."},
        {"pattern": "long o", "sound": "/oʊ/", "words": ["home", "rope", "hope", "nose", "boat", "goat", "snow", "yellow"], "explain": "긴 o는 /oʊ/ 소리입니다. '오우'에 가깝습니다."},
        {"pattern": "long u", "sound": "/juː/", "words": ["cube", "cute", "use", "music", "student", "tube", "mule", "huge"], "explain": "긴 u는 /juː/ 소리로 나는 경우가 많습니다. '유'에 가깝습니다."},
    ],

    "④ 모음 예외": [
        {"pattern": "al / all", "sound": "/ɔː/", "words": ["ball", "call", "tall", "wall", "fall", "small"], "explain": "all은 기본 short a가 아니라 '올'에 가까운 소리로 납니다."},
        {"pattern": "ar / a", "sound": "/ɑː/", "words": ["car", "park", "star", "far", "father", "start"], "explain": "ar 또는 father의 a는 '아' 계열 소리로 나는 경우가 있습니다."},
        {"pattern": "weak a", "sound": "/ə/", "words": ["about", "ago", "again", "away", "around", "banana"], "explain": "강세가 약한 a는 /ə/처럼 약한 '어' 소리로 납니다."},
        {"pattern": "o as /ʌ/", "sound": "/ʌ/", "words": ["love", "come", "son", "some", "done", "money"], "explain": "o가 /o/가 아니라 /ʌ/ 소리로 나는 예외 단어들입니다."},
        {"pattern": "o as /uː/", "sound": "/uː/", "words": ["do", "to", "who", "move", "lose", "prove"], "explain": "o가 긴 /uː/ 소리로 나는 경우입니다."},
        {"pattern": "oo", "sound": "/ʊ/ or /uː/", "words": ["book", "good", "look", "cook", "moon", "spoon", "food", "school"], "explain": "oo는 짧은 /ʊ/ 소리도 나고 긴 /uː/ 소리도 납니다."},
        {"pattern": "ea as /e/", "sound": "/e/", "words": ["bread", "head", "dead", "ready", "heavy", "weather"], "explain": "ea가 긴 e가 아니라 /e/ 소리로 나는 예외입니다."},
        {"pattern": "ou as /ʌ/", "sound": "/ʌ/", "words": ["country", "young", "touch", "double", "trouble", "cousin"], "explain": "ou가 /aʊ/가 아니라 /ʌ/ 소리로 나는 경우입니다."},
    ],

    "⑤ 자음 이어 읽기": [
        {"pattern": "bl", "sound": "blend", "words": ["black", "blue", "block", "blow", "blank"], "explain": "bl은 b와 l 소리가 이어져 납니다."},
        {"pattern": "br", "sound": "blend", "words": ["brown", "bread", "brush", "bring", "break"], "explain": "br은 b와 r 소리가 이어져 납니다."},
        {"pattern": "cl", "sound": "blend", "words": ["clock", "class", "clap", "clean", "cloud"], "explain": "cl은 c/k 소리와 l 소리가 이어져 납니다."},
        {"pattern": "cr", "sound": "blend", "words": ["crab", "cry", "crown", "cream", "cross"], "explain": "cr은 c/k 소리와 r 소리가 이어져 납니다."},
        {"pattern": "dr", "sound": "blend", "words": ["drum", "dress", "drink", "drive", "dream"], "explain": "dr은 d와 r 소리가 이어져 납니다."},
        {"pattern": "fl", "sound": "blend", "words": ["flag", "fly", "flame", "floor", "flower"], "explain": "fl은 f와 l 소리가 이어져 납니다."},
        {"pattern": "fr", "sound": "blend", "words": ["frog", "free", "fruit", "friend", "from"], "explain": "fr은 f와 r 소리가 이어져 납니다."},
        {"pattern": "gl", "sound": "blend", "words": ["glass", "glad", "globe", "glue", "glove"], "explain": "gl은 g와 l 소리가 이어져 납니다."},
        {"pattern": "gr", "sound": "blend", "words": ["green", "grass", "grape", "gray", "grow"], "explain": "gr은 g와 r 소리가 이어져 납니다."},
        {"pattern": "pl", "sound": "blend", "words": ["plane", "play", "plug", "plant", "please"], "explain": "pl은 p와 l 소리가 이어져 납니다."},
        {"pattern": "pr", "sound": "blend", "words": ["present", "price", "print", "proud", "pray"], "explain": "pr은 p와 r 소리가 이어져 납니다."},
        {"pattern": "sk", "sound": "blend", "words": ["skate", "sky", "skill", "skin", "skip"], "explain": "sk는 s와 k 소리가 이어져 납니다."},
        {"pattern": "sl", "sound": "blend", "words": ["sleep", "slow", "slide", "slim", "slice"], "explain": "sl은 s와 l 소리가 이어져 납니다."},
        {"pattern": "sm", "sound": "blend", "words": ["smile", "small", "smell", "smoke", "smart"], "explain": "sm은 s와 m 소리가 이어져 납니다."},
        {"pattern": "sn", "sound": "blend", "words": ["snake", "snow", "snack", "snail", "snap"], "explain": "sn은 s와 n 소리가 이어져 납니다."},
        {"pattern": "sp", "sound": "blend", "words": ["spoon", "space", "speak", "spin", "sport"], "explain": "sp는 s와 p 소리가 이어져 납니다."},
        {"pattern": "st", "sound": "blend", "words": ["star", "stop", "student", "stone", "stick"], "explain": "st는 s와 t 소리가 이어져 납니다."},
        {"pattern": "tr", "sound": "blend", "words": ["tree", "train", "truck", "trip", "true"], "explain": "tr은 t와 r 소리가 이어져 납니다."},
    ],

    "⑥ 두 글자 한 소리": [
        {"pattern": "ch", "sound": "/tʃ/", "words": ["chair", "cheese", "chicken", "child", "watch", "lunch"], "explain": "ch는 /tʃ/ 소리입니다. '치'에 가깝습니다."},
        {"pattern": "sh", "sound": "/ʃ/", "words": ["ship", "shop", "fish", "shoe", "sheep", "wash"], "explain": "sh는 /ʃ/ 소리입니다. '쉬'에 가깝습니다."},
        {"pattern": "th", "sound": "/θ/", "words": ["three", "thin", "bath", "thank", "think", "teeth"], "explain": "th는 혀를 살짝 내밀고 바람을 내는 /θ/ 소리가 납니다."},
        {"pattern": "th", "sound": "/ð/", "words": ["this", "that", "mother", "father", "they", "there"], "explain": "th는 목소리가 울리는 /ð/ 소리로도 납니다."},
        {"pattern": "wh", "sound": "/w/", "words": ["whale", "white", "wheel", "when", "what", "where"], "explain": "wh는 보통 /w/ 소리로 납니다."},
        {"pattern": "ph", "sound": "/f/", "words": ["phone", "photo", "graph", "dolphin", "elephant", "alphabet"], "explain": "ph는 f와 같은 /f/ 소리로 납니다."},
        {"pattern": "ck", "sound": "/k/", "words": ["duck", "clock", "black", "back", "neck", "rock"], "explain": "ck는 /k/ 소리로 납니다."},
    ],

    "⑦ 모음 두 글자 소리": [
        {"pattern": "ai", "sound": "/eɪ/", "words": ["rain", "train", "paint", "mail", "tail", "wait"], "explain": "ai는 보통 단어 중간에서 /eɪ/ 소리로 납니다."},
        {"pattern": "ay", "sound": "/eɪ/", "words": ["day", "play", "say", "way", "stay", "gray"], "explain": "ay는 보통 단어 끝에서 /eɪ/ 소리로 납니다."},
        {"pattern": "ee", "sound": "/iː/", "words": ["see", "tree", "green", "bee", "feet", "sleep"], "explain": "ee는 긴 /iː/ 소리입니다."},
        {"pattern": "ea", "sound": "/iː/", "words": ["eat", "sea", "teach", "read", "meat", "team"], "explain": "ea는 보통 긴 /iː/ 소리로 납니다."},
        {"pattern": "oa", "sound": "/oʊ/", "words": ["boat", "goat", "coat", "road", "soap", "toast"], "explain": "oa는 보통 /oʊ/ 소리로 납니다."},
        {"pattern": "ow", "sound": "/oʊ/", "words": ["snow", "window", "yellow", "slow", "grow", "show"], "explain": "ow는 /oʊ/ 소리로 나는 경우가 있습니다."},
        {"pattern": "ow", "sound": "/aʊ/", "words": ["cow", "now", "brown", "down", "town", "flower"], "explain": "ow는 /aʊ/ 소리로 나는 경우도 있습니다."},
        {"pattern": "ou", "sound": "/aʊ/", "words": ["house", "mouth", "cloud", "loud", "out", "round"], "explain": "ou는 /aʊ/ 소리로 나는 경우가 많습니다."},
        {"pattern": "oi", "sound": "/ɔɪ/", "words": ["coin", "oil", "join", "boil", "soil", "point"], "explain": "oi는 보통 단어 중간에서 /ɔɪ/ 소리로 납니다."},
        {"pattern": "oy", "sound": "/ɔɪ/", "words": ["boy", "toy", "joy", "enjoy", "royal", "oyster"], "explain": "oy는 보통 단어 끝에서 /ɔɪ/ 소리로 납니다."},
    ],

    "⑧ r이 붙은 모음": [
        {"pattern": "ar", "sound": "/ɑːr/", "words": ["car", "star", "park", "far", "arm", "farm", "dark"], "explain": "ar은 r의 영향을 받아 /ɑːr/ 소리로 납니다."},
        {"pattern": "er", "sound": "/ɜːr/", "words": ["her", "teacher", "sister", "father", "mother", "water", "paper"], "explain": "er은 /ɜːr/ 또는 약한 /ər/ 소리로 납니다."},
        {"pattern": "ir", "sound": "/ɜːr/", "words": ["bird", "girl", "shirt", "first", "third", "circle", "dirty"], "explain": "ir은 /ɜːr/ 소리로 나는 경우가 많습니다."},
        {"pattern": "or", "sound": "/ɔːr/", "words": ["corn", "fork", "horse", "short", "sport", "morning", "story"], "explain": "or은 /ɔːr/ 소리로 나는 경우가 많습니다."},
        {"pattern": "ur", "sound": "/ɜːr/", "words": ["turn", "burn", "nurse", "hurt", "purple", "turtle", "church"], "explain": "ur은 /ɜːr/ 소리로 나는 경우가 많습니다."},
    ],

    "⑨ 소리 안 나는 e": [
        {"pattern": "a_e", "sound": "/eɪ/", "words": ["cake", "name", "make", "lake", "game", "same", "take", "wave"], "explain": "끝의 e는 소리 나지 않고 앞의 a를 긴 /eɪ/ 소리로 만듭니다."},
        {"pattern": "i_e", "sound": "/aɪ/", "words": ["bike", "five", "kite", "time", "line", "ride", "like", "smile"], "explain": "끝의 e는 소리 나지 않고 앞의 i를 긴 /aɪ/ 소리로 만듭니다."},
        {"pattern": "o_e", "sound": "/oʊ/", "words": ["home", "rope", "hope", "nose", "stone", "phone", "note", "bone"], "explain": "끝의 e는 소리 나지 않고 앞의 o를 긴 /oʊ/ 소리로 만듭니다."},
        {"pattern": "u_e", "sound": "/juː/", "words": ["cube", "cute", "use", "tube", "huge", "mule", "June", "rule"], "explain": "끝의 e는 소리 나지 않고 앞의 u를 긴 소리로 만듭니다."},
    ],

    "⑩ 자음 예외": [
        {"pattern": "c + e", "sound": "/s/", "words": ["cent", "cell", "ice", "face", "dance", "nice"], "explain": "c 뒤에 e가 오면 c가 /s/ 소리로 나는 경우가 많습니다."},
        {"pattern": "c + i", "sound": "/s/", "words": ["city", "circle", "pencil", "cinema", "rice", "decide"], "explain": "c 뒤에 i가 오면 c가 /s/ 소리로 나는 경우가 많습니다."},
        {"pattern": "c + y", "sound": "/s/", "words": ["cycle", "cymbal", "fancy", "spicy", "icy", "mercy"], "explain": "c 뒤에 y가 오면 c가 /s/ 소리로 나는 경우가 있습니다."},
        {"pattern": "g + e", "sound": "/dʒ/", "words": ["gem", "gentle", "page", "large", "orange", "cage"], "explain": "g 뒤에 e가 오면 /dʒ/ 소리로 나는 경우가 있습니다."},
        {"pattern": "g + i", "sound": "/dʒ/", "words": ["giant", "giraffe", "magic", "engine", "energy", "imagine"], "explain": "g 뒤에 i가 오면 /dʒ/ 소리로 나는 경우가 있습니다."},
        {"pattern": "g + y", "sound": "/dʒ/", "words": ["gym", "energy", "biology", "allergy", "technology"], "explain": "g 뒤에 y가 오면 /dʒ/ 소리로 나는 경우가 있습니다."},
        {"pattern": "kn", "sound": "/n/", "words": ["knee", "know", "knife", "knock", "knot", "kneel"], "explain": "kn으로 시작하는 단어에서 k는 소리 나지 않습니다."},
        {"pattern": "wr", "sound": "/r/", "words": ["write", "wrong", "wrap", "wrist", "wreck", "writer"], "explain": "wr로 시작하는 단어에서 w는 소리 나지 않습니다."},
        {"pattern": "mb", "sound": "/m/", "words": ["lamb", "comb", "climb", "thumb", "bomb", "dumb"], "explain": "단어 끝 mb에서 b는 소리 나지 않는 경우가 많습니다."},
        {"pattern": "x", "sound": "/gz/", "words": ["exam", "example", "exist", "exact", "exit"], "explain": "x가 /gz/ 소리로 나는 경우입니다."},
    ],
}

# =========================
# 출력 함수
# =========================
def show_speaking_practice(tab_name, groups):
    st.subheader(tab_name)

    st.markdown(
        """
        <div class="category-guide">
            👀 <b>단어들을 먼저 직접 읽어 보세요.</b><br>
            🔊 그 다음 <b>발음 듣기</b>를 눌러 여러 단어를 한 번에 들어 봅니다.<br>
            💡 설명을 보고 어떤 글자가 어떤 소리로 나는지 확인합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    for i, item in enumerate(groups):
        pattern = item["pattern"]
        sound = item["sound"]
        words = item["words"]
        explain = item["explain"]

        # ✅ 단어 사이 발음 간격을 조금 더 늘림
        # 예: gem.               gentle.               page.               large.               orange.               cage.
        words_audio = ".               ".join(words) + "."

        words_html = "".join(
            [f"<span class='word-pill'>{html.escape(word)}</span>" for word in words]
        )

        st.markdown('<div class="mini-card">', unsafe_allow_html=True)

        col1, col2 = st.columns([1.3, 4])

        with col1:
            st.markdown(
                f"""
                <div class="pattern-title">{html.escape(pattern)}</div>
                <div class="sound-text">{html.escape(sound)}</div>
                """,
                unsafe_allow_html=True
            )
            play_audio(words_audio, key=f"{tab_name}_{i}_audio")

        with col2:
            st.markdown(
                f"""
                <div class="word-wrap">
                    {words_html}
                </div>
                <div class="explain-box">
                    💡 {html.escape(explain)}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 탭 구성
# =========================
tabs = st.tabs(list(practice_sets.keys()))

for tab, tab_name in zip(tabs, practice_sets.keys()):
    with tab:
        show_speaking_practice(tab_name, practice_sets[tab_name])
