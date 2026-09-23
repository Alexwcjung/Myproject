 import streamlit as st

st.set_page_config(
    page_title="Fun English",
    page_icon="📚",
    layout="centered"
)

expressions = [
    ("weekly plan", "주간 계획표"),
    ("there are no breaks", "계획표에 쉬는 시간이 없다"),
    ("Let me take a look", "내가 한 번 살펴볼게"),
    ("you will get tired and give up", "너는 피곤해지고 포기하게 될 것이다"),
    ("I will do my best", "최선을 다할 것이다"),
    ("You are not an early bird", "너는 아침형 인간이 아니다"),
    ("You need to make a realistic plan", "너는 현실적인 계획을 세워야 한다"),
    ("That makes sense", "네 말이 일리가 있다"),
    ("I will delete the morning jog and concentrate on the afternoon workout", "나는 아침 조깅을 없애고 오후 근력 운동에 집중하겠다"),
    ("quality is more important than quantity", "양보다 질이 중요하다"),
    ("I am out of time", "나는 이미 늦어버렸다"),
    ("you begged me with drowning eyes to stay", "너는 간절한 눈빛으로 나에게 머물러 달라고 말했다."),
    ("say goodbye", "작별 인사하다"),
    ("survive", "살아남다"),
    ("follow", "따라가다"),
    ("last", "마지막"),
    ("tomorrow", "내일"),
    ("I am going to love you every night like it is the last night", "오늘 밤이 마지막인 것처럼 매일 밤 너를 사랑하겠다"),
    ("if the world was ending", "세상이 끝난다면"),
    ("if the party was over and our time on earth was through", "파티가 끝나고 지구에서의 우리의 시간이 끝난다면")
]

st.title("📚 Fun English")

for i, (english, korean) in enumerate(expressions, start=1):
    st.markdown(f"**{i}. {english}**")
    st.write(korean)