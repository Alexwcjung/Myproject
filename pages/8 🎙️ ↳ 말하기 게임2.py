import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="말하면 터지는 문장 게임 2",
    page_icon="💥",
    layout="centered"
)

# =========================================================
# 제목
# =========================================================
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 50%, #f7fee7 100%);
        padding: 30px 24px;
        border-radius: 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 26px rgba(80, 80, 120, 0.12);
        text-align: center;
        border: 1.5px solid #e0f2fe;
    ">
        <h1 style="color:#334155; margin-bottom:10px; font-size:36px; font-weight:900;">
            💥 말하면 터지는 문장 게임 2
        </h1>
        <p style="color:#64748b; font-size:19px; margin:0; line-height:1.7;">
            한국어 상황을 보고 영어 문장으로 말해 보세요.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info("사용 방법: 문법 선택 → 게임 시작 → 한국어 상황을 영어로 말하기 → 맞으면 카드가 터지고 정답과 발음이 나옵니다. 다음 문제는 직접 넘깁니다.")

# =========================================================
# 말하기 문제 데이터
# - 일상단어 400 느낌의 어휘를 활용
# - 2문장 이상, 조금 더 길고 약간 복잡한 문장
# =========================================================
speaking_questions = [
    {
        "category": "🏫 학교생활",
        "korean": "나는 오늘 수학 과제가 있어. 그래서 도서관에서 교과서와 공책을 사용할 거야.",
        "sentence": "I have a math assignment today, so I will use my textbook and notebook in the library.",
        "hint": "math / assignment / textbook / notebook / library"
    },
    {
        "category": "🏫 학교생활",
        "korean": "우리 모둠은 과학 프로젝트를 준비하고 있어. 내일 발표가 있어서 조금 긴장돼.",
        "sentence": "Our group is preparing a science project, and I am a little nervous because we have a presentation tomorrow.",
        "hint": "science / project / nervous / presentation / tomorrow"
    },
    {
        "category": "🏫 학교생활",
        "korean": "나는 복도에서 친구를 만났어. 우리는 점심시간 전에 일정표를 확인했어.",
        "sentence": "I met my friend in the hallway, and we checked the schedule before lunch time.",
        "hint": "friend / hallway / schedule / lunch"
    },
    {
        "category": "✏️ 교실 활동",
        "korean": "문장을 공책에 베껴 쓰고 중요한 단어에 밑줄을 치세요. 그런 다음 답을 확인하세요.",
        "sentence": "Copy the sentence in your notebook and underline the important words. Then check your answer.",
        "hint": "copy / notebook / underline / check"
    },
    {
        "category": "✏️ 교실 활동",
        "korean": "선생님이 설명한 뒤에 우리는 예시를 비교했어. 그리고 짝과 답을 토론했어.",
        "sentence": "After the teacher explained it, we compared the examples and discussed the answer with a partner.",
        "hint": "teacher / explain / compare / discuss / partner"
    },
    {
        "category": "✏️ 교실 활동",
        "korean": "철자를 말하고 단어를 반복해 주세요. 발음이 어렵다면 천천히 다시 말해도 됩니다.",
        "sentence": "Please spell the word and repeat it. If the pronunciation is difficult, you can say it slowly again.",
        "hint": "spell / repeat / pronunciation / slowly / again"
    },
    {
        "category": "🏠 집과 생활",
        "korean": "나는 거실에서 텔레비전을 보고 있었어. 하지만 냉장고 안에 음식이 없어서 부엌으로 갔어.",
        "sentence": "I was watching television in the living room, but there was no food in the refrigerator, so I went to the kitchen.",
        "hint": "television / living room / refrigerator / kitchen"
    },
    {
        "category": "🏠 집과 생활",
        "korean": "내 방에는 담요와 베개가 있어. 나는 피곤해서 일찍 자고 싶어.",
        "sentence": "There is a blanket and a pillow in my bedroom, and I want to sleep early because I am tired.",
        "hint": "blanket / pillow / bedroom / sleep / tired"
    },
    {
        "category": "🏠 집과 생활",
        "korean": "쓰레기를 버리고 손을 비누로 씻어 주세요. 그런 다음 수건으로 손을 말리세요.",
        "sentence": "Please throw away the trash and wash your hands with soap. Then dry your hands with a towel.",
        "hint": "trash / wash / soap / towel"
    },
    {
        "category": "🌅 하루 일과",
        "korean": "나는 보통 아침에 일찍 일어나. 학교에 가기 전에 샤워하고 옷을 입어.",
        "sentence": "I usually get up early in the morning. I take a shower and get dressed before I go to school.",
        "hint": "usually / get up / morning / shower / school"
    },
    {
        "category": "🌅 하루 일과",
        "korean": "주말에는 늦게 일어나지만 평일에는 항상 일찍 출발해. 버스가 자주 붐비기 때문이야.",
        "sentence": "I wake up late on weekends, but I always leave early on weekdays because the bus is often crowded.",
        "hint": "weekend / always / leave / weekday / bus"
    },
    {
        "category": "🌅 하루 일과",
        "korean": "나는 숙제를 끝낸 뒤에 조금 쉬어. 가끔은 음악을 들으면서 긴장을 풀어.",
        "sentence": "After I finish my homework, I relax for a while. Sometimes I listen to music to feel calm.",
        "hint": "finish / homework / relax / music / calm"
    },
    {
        "category": "🎮 취미와 여가",
        "korean": "내 취미는 영화 보기야. 시간이 있으면 친구와 영화를 보고 감상에 대해 이야기해.",
        "sentence": "My hobby is watching movies. If I have free time, I watch a movie with my friend and talk about it.",
        "hint": "hobby / movie / free time / friend / talk"
    },
    {
        "category": "🎮 취미와 여가",
        "korean": "그녀는 사진 촬영을 좋아해. 그래서 주말마다 공원에서 사진을 찍어.",
        "sentence": "She likes photography, so she takes pictures in the park every weekend.",
        "hint": "photography / pictures / park / weekend"
    },
    {
        "category": "🎮 취미와 여가",
        "korean": "나는 캠핑을 좋아하지만 오늘은 날씨가 나빠. 그래서 집에서 소설을 읽을 거야.",
        "sentence": "I like camping, but the weather is bad today, so I will read a novel at home.",
        "hint": "camping / weather / bad / novel / home"
    },
    {
        "category": "⚽ 운동과 활동",
        "korean": "우리는 방과 후에 축구를 할 거야. 경기장에 늦지 않도록 제시간에 도착해야 해.",
        "sentence": "We will play soccer after school, and we should arrive at the field on time.",
        "hint": "soccer / after school / field / on time"
    },
    {
        "category": "⚽ 운동과 활동",
        "korean": "그는 농구 경기에 나가고 싶어 해. 하지만 무릎이 아파서 오늘은 쉬어야 해.",
        "sentence": "He wants to join the basketball match, but his knee hurts, so he should rest today.",
        "hint": "basketball / match / hurts / rest"
    },
    {
        "category": "⚽ 운동과 활동",
        "korean": "코치가 운동장에서 우리에게 설명했어. 우리는 다음 대회를 위해 매일 연습할 거야.",
        "sentence": "The coach explained it to us on the field, and we will practice every day for the next competition.",
        "hint": "coach / field / practice / competition"
    },
    {
        "category": "🌦️ 날씨와 계절",
        "korean": "오늘은 비가 오고 바람이 불어. 그래서 우산과 비옷이 필요해.",
        "sentence": "It is rainy and windy today, so I need an umbrella and a raincoat.",
        "hint": "rainy / windy / umbrella / raincoat"
    },
    {
        "category": "🌦️ 날씨와 계절",
        "korean": "겨울에는 날씨가 춥지만 나는 눈 오는 날을 좋아해. 눈사람을 만들 수 있기 때문이야.",
        "sentence": "It is cold in winter, but I like snowy days because I can make a snowman.",
        "hint": "winter / cold / snowy / because"
    },
    {
        "category": "🌦️ 날씨와 계절",
        "korean": "일기예보를 확인해 주세요. 오후에는 폭풍우가 올 수 있어서 밖에 나가면 조심해야 해요.",
        "sentence": "Please check the weather forecast. It may be stormy in the afternoon, so be careful outside.",
        "hint": "forecast / stormy / afternoon / careful"
    },
    {
        "category": "🍽️ 식당과 주문",
        "korean": "나는 식당에서 메뉴를 보고 있어. 매운 음식은 괜찮지만 너무 비싼 요리는 원하지 않아.",
        "sentence": "I am looking at the menu in the restaurant. Spicy food is okay, but I do not want an expensive dish.",
        "hint": "menu / restaurant / spicy / expensive / dish"
    },
    {
        "category": "🍽️ 식당과 주문",
        "korean": "계산서를 가져다 주세요. 영수증도 필요해요. 왜냐하면 비용을 확인해야 하기 때문이에요.",
        "sentence": "Please bring the bill and the receipt because I need to check the price.",
        "hint": "bill / receipt / check / price"
    },
    {
        "category": "🍽️ 식당과 주문",
        "korean": "그녀는 샐러드를 주문했고 나는 수프를 주문했어. 우리는 식사 후에 디저트를 먹을 거야.",
        "sentence": "She ordered a salad and I ordered soup. We will have dessert after the meal.",
        "hint": "salad / soup / dessert / meal"
    },
    {
        "category": "🛍️ 쇼핑과 가격",
        "korean": "이 재킷은 너무 비싸. 할인 쿠폰이 있으면 나는 그것을 살 수 있어.",
        "sentence": "This jacket is too expensive. If I have a discount coupon, I can buy it.",
        "hint": "jacket / expensive / discount / coupon / buy"
    },
    {
        "category": "🛍️ 쇼핑과 가격",
        "korean": "계산원이 거스름돈을 줬어. 나는 영수증을 확인하고 가방에 넣었어.",
        "sentence": "The cashier gave me change, and I checked the receipt before I put it in my bag.",
        "hint": "cashier / change / receipt / bag"
    },
    {
        "category": "🛍️ 쇼핑과 가격",
        "korean": "색깔은 좋지만 사이즈가 맞지 않아. 그래서 교환이나 환불을 요청할 거야.",
        "sentence": "The color is good, but the size is not right, so I will ask for an exchange or a refund.",
        "hint": "color / size / exchange / refund"
    },
    {
        "category": "🚇 교통과 길 찾기",
        "korean": "나는 길을 잃었어. 지하철역에 가려면 어느 방향으로 가야 하는지 알고 싶어.",
        "sentence": "I am lost, and I want to know which direction I should go to get to the subway station.",
        "hint": "lost / direction / subway station"
    },
    {
        "category": "🚇 교통과 길 찾기",
        "korean": "버스 정류장은 모퉁이 근처에 있어. 횡단보도를 건넌 뒤에 오른쪽으로 가세요.",
        "sentence": "The bus stop is near the corner. Cross the crosswalk and then go right.",
        "hint": "bus stop / corner / crosswalk / right"
    },
    {
        "category": "🚇 교통과 길 찾기",
        "korean": "공항에 가려면 터미널에서 갈아타야 해. 시간이 없으니 빨리 움직여야 해.",
        "sentence": "To get to the airport, you need to transfer at the terminal. We do not have much time, so we should move quickly.",
        "hint": "airport / transfer / terminal / quickly"
    },
    {
        "category": "🧳 여행과 숙박",
        "korean": "나는 호텔 예약을 확인하고 싶어. 여권과 짐은 내 배낭 안에 있어.",
        "sentence": "I want to check my hotel reservation. My passport and luggage are in my backpack.",
        "hint": "hotel / reservation / passport / luggage / backpack"
    },
    {
        "category": "🧳 여행과 숙박",
        "korean": "우리는 현지 박물관을 방문할 거야. 유명한 기념품도 사고 싶어.",
        "sentence": "We will visit a local museum, and I also want to buy a famous souvenir.",
        "hint": "local / museum / famous / souvenir"
    },
    {
        "category": "🧳 여행과 숙박",
        "korean": "체크인 시간이 늦었지만 직원이 우리를 도와줬어. 그래서 우리는 방에 들어갈 수 있었어.",
        "sentence": "The check-in time was late, but the staff helped us, so we could enter the room.",
        "hint": "check in / late / staff / helped / room"
    },
    {
        "category": "😊 감정 표현",
        "korean": "나는 발표 전에 긴장했지만 끝난 뒤에는 자랑스러웠어. 친구들이 내게 박수를 쳤기 때문이야.",
        "sentence": "I was nervous before the presentation, but I felt proud after it because my friends clapped for me.",
        "hint": "nervous / presentation / proud / friends"
    },
    {
        "category": "😊 감정 표현",
        "korean": "그는 시험 결과에 실망했어. 하지만 선생님의 조언을 듣고 다시 희망을 가졌어.",
        "sentence": "He was disappointed with the test result, but he felt hopeful again after listening to the teacher's advice.",
        "hint": "disappointed / test / hopeful / advice"
    },
    {
        "category": "😊 감정 표현",
        "korean": "나는 혼자 있어서 외로웠어. 그래서 친구에게 메시지를 보내고 함께 산책했어.",
        "sentence": "I felt lonely because I was alone, so I sent a message to my friend and walked together.",
        "hint": "lonely / alone / message / friend / together"
    },
    {
        "category": "📱 미디어와 스마트폰",
        "korean": "내 스마트폰 배터리가 거의 없어. 와이파이 비밀번호를 찾으면 친구에게 메시지를 보낼 수 있어.",
        "sentence": "My smartphone battery is almost dead. If I find the Wi-Fi password, I can send a message to my friend.",
        "hint": "smartphone / battery / Wi-Fi / password / message"
    },
    {
        "category": "📱 미디어와 스마트폰",
        "korean": "나는 웹사이트에서 뉴스를 검색했어. 그런 다음 중요한 게시물에 댓글을 달았어.",
        "sentence": "I searched for news on the website, and then I wrote a comment on an important post.",
        "hint": "search / news / website / comment / post"
    },
    {
        "category": "📱 미디어와 스마트폰",
        "korean": "영상 통화가 끊겼어. 화면이 멈췄고 인터넷 연결도 좋지 않았어.",
        "sentence": "The video call stopped. The screen froze, and the internet connection was not good.",
        "hint": "video call / screen / internet / connection"
    },
    {
        "category": "🌈 직업과 미래",
        "korean": "나는 미래에 기술자가 되고 싶어. 그래서 공장에서 필요한 기술과 경험을 배우고 있어.",
        "sentence": "I want to become an engineer in the future, so I am learning the skills and experience needed in a factory.",
        "hint": "engineer / future / skills / experience / factory"
    },
    {
        "category": "🌈 직업과 미래",
        "korean": "그녀는 요리사가 되는 것이 꿈이야. 면접 전에 자신의 목표를 분명하게 설명하려고 해.",
        "sentence": "Her dream is to become a chef, and she wants to explain her goal clearly before the interview.",
        "hint": "dream / chef / goal / interview"
    },
    {
        "category": "🌈 직업과 미래",
        "korean": "나는 소방관을 존경해. 위험한 상황에서도 사람들을 돕기 때문이야.",
        "sentence": "I respect firefighters because they help people even in dangerous situations.",
        "hint": "firefighters / help / people / dangerous"
    },
]

# =========================================================
# 게임 설정
# =========================================================
categories = ["전체"] + list(dict.fromkeys([q["category"] for q in speaking_questions]))

selected_category = st.selectbox(
    "연습할 문법 / 주제를 고르세요.",
    categories
)

if selected_category == "전체":
    filtered_questions = speaking_questions
else:
    filtered_questions = [q for q in speaking_questions if q["category"] == selected_category]

col1, col2 = st.columns(2)

with col1:
    game_question_count = st.slider(
        "🎯 게임 문제 개수",
        min_value=1,
        max_value=len(filtered_questions),
        value=min(10, len(filtered_questions)),
        step=1
    )

with col2:
    pass_ratio = st.slider(
        "✅ 정답 인정 기준",
        min_value=45,
        max_value=95,
        value=65,
        step=5,
        help="낮을수록 학생 발음을 더 너그럽게 인정합니다. 기본값은 이전 코드보다 조금 관대하게 설정했습니다."
    )

show_first_hint = st.checkbox("처음부터 영어 첫 글자 힌트 보이기", value=False)
auto_sound = st.checkbox("맞히면 원어민 발음 자동 재생", value=True)

game_questions = filtered_questions[:game_question_count]

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #ffffff, #f8fbff);
        border-radius: 24px;
        padding: 20px 22px;
        margin: 16px 0 22px 0;
        box-shadow: 0 5px 16px rgba(0,0,0,0.055);
        border: 1.5px solid #edf2ff;
        font-size: 18px;
        line-height: 1.7;
        color: #374151;
    ">
        💡 <b>게임 시작</b>을 누른 뒤, 한국어 상황을 영어로 말하세요.<br>
        맞으면 카드가 <b>팡!</b> 터지고 정답 문장과 발음 버튼이 나옵니다.<br>
        틀리면 자동으로 힌트가 나타나며, 다음 문제는 직접 넘깁니다.
    </div>
    """,
    unsafe_allow_html=True
)

questions_json = json.dumps(game_questions, ensure_ascii=False)
hint_js = "true" if show_first_hint else "false"
auto_sound_js = "true" if auto_sound else "false"

# =========================================================
# 게임 HTML
# =========================================================
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        background: transparent;
    }}

    .game-wrap {{
        width: 100%;
        min-height: 700px;
        background: linear-gradient(135deg, #f0f9ff 0%, #fff7ed 50%, #f7fee7 100%);
        border: 4px solid #bfdbfe;
        border-radius: 32px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.12);
        padding: 24px;
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
    }}

    .top-bar {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-bottom: 18px;
    }}

    .badge {{
        background: rgba(255,255,255,0.95);
        border: 2px solid #dbeafe;
        border-radius: 20px;
        padding: 12px 8px;
        text-align: center;
        font-size: 19px;
        font-weight: 900;
        color: #334155;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        line-height: 1.4;
    }}

    .message {{
        background: linear-gradient(135deg, #fef3c7, #fed7aa);
        border: 3px solid #fb923c;
        border-radius: 24px;
        padding: 14px;
        text-align: center;
        font-size: 21px;
        font-weight: 900;
        color: #7c2d12;
        margin-bottom: 18px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        min-height: 34px;
        line-height: 1.4;
    }}

    .card-area {{
        width: 100%;
        min-height: 265px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }}

    .question-card {{
        width: 90%;
        min-height: 230px;
        background: linear-gradient(135deg, #ffffff, #fff7ed);
        border: 4px solid #fed7aa;
        border-radius: 34px;
        box-shadow: 0 12px 26px rgba(0,0,0,0.14);
        padding: 28px 24px;
        box-sizing: border-box;
        text-align: center;
        transition: all 0.25s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .question-card.pop {{
        animation: pop 0.55s forwards;
    }}

    @keyframes pop {{
        0% {{ transform: scale(1); opacity: 1; }}
        45% {{ transform: scale(1.18) rotate(2deg); opacity: 0.92; }}
        100% {{ transform: scale(0.08); opacity: 0; }}
    }}

    .category {{
        font-size: 19px;
        font-weight: 900;
        color: #9a3412;
        margin-bottom: 12px;
    }}

    .korean {{
        font-size: 29px;
        font-weight: 900;
        color: #111827;
        line-height: 1.5;
        word-break: keep-all;
    }}

    .hint {{
        display: none;
        margin-top: 14px;
        font-size: 18px;
        color: #92400e;
        font-weight: 900;
        background: #fff7ed;
        border: 2px solid #fed7aa;
        border-radius: 18px;
        padding: 10px 12px;
        line-height: 1.45;
    }}

    .answer-area {{
        display: none;
        width: 90%;
        margin: 18px auto 0 auto;
        background: rgba(255,255,255,0.96);
        border: 2px solid #dbeafe;
        border-radius: 26px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }}

    .answer-label {{
        font-size: 17px;
        font-weight: 900;
        color: #475569;
        margin-bottom: 8px;
    }}

    .answer-sentence {{
        font-size: 26px;
        font-weight: 900;
        color: #2563eb;
        line-height: 1.45;
        margin-bottom: 14px;
    }}

    .recognized {{
        width: 90%;
        margin: 14px auto 0 auto;
        text-align: center;
        font-size: 18px;
        font-weight: 900;
        color: #475569;
        min-height: 34px;
        line-height: 1.5;
        background: rgba(255,255,255,0.9);
        border: 1.5px solid #e2e8f0;
        border-radius: 18px;
        padding: 10px 12px;
        box-sizing: border-box;
    }}

    .btn-row {{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 18px;
    }}

    .btn {{
        border: none;
        border-radius: 999px;
        padding: 13px 24px;
        font-size: 19px;
        font-weight: 900;
        color: white;
        background: linear-gradient(135deg, #ff7eb3, #ffb86c);
        box-shadow: 0 8px 18px rgba(0,0,0,0.18);
        cursor: pointer;
    }}

    .sub-btn {{
        background: linear-gradient(135deg, #60a5fa, #93c5fd);
    }}

    .sound-btn {{
        background: linear-gradient(135deg, #34d399, #60a5fa);
        font-size: 17px;
        padding: 11px 20px;
    }}

    .btn:active {{
        transform: scale(0.96);
    }}

    .effect {{
        position: absolute;
        font-size: 44px;
        animation: floatUp 0.8s forwards;
        pointer-events: none;
        z-index: 30;
    }}

    @keyframes floatUp {{
        0% {{ opacity: 1; transform: translateY(0) scale(1); }}
        100% {{ opacity: 0; transform: translateY(-70px) scale(1.6); }}
    }}

    @media (max-width: 700px) {{
        .game-wrap {{
            padding: 12px;
            min-height: 690px;
            border-radius: 24px;
            border-width: 3px;
        }}

        .top-bar {{
            gap: 5px;
            margin-bottom: 12px;
        }}

        .badge {{
            font-size: 14px;
            padding: 9px 4px;
            border-radius: 14px;
            line-height: 1.3;
        }}

        .message {{
            font-size: 16px;
            padding: 10px 8px;
            border-radius: 18px;
            margin-bottom: 12px;
        }}

        .card-area {{
            min-height: 255px;
        }}

        .question-card {{
            width: 96%;
            min-height: 235px;
            padding: 22px 14px;
            border-radius: 24px;
        }}

        .category {{
            font-size: 16px;
        }}

        .korean {{
            font-size: 23px;
            line-height: 1.5;
        }}

        .hint {{
            font-size: 15px;
            padding: 8px 10px;
        }}

        .answer-area {{
            width: 96%;
            padding: 14px 12px;
            border-radius: 22px;
        }}

        .answer-sentence {{
            font-size: 20px;
        }}

        .recognized {{
            width: 96%;
            font-size: 14px;
            padding: 8px 10px;
        }}

        .btn {{
            font-size: 14px;
            padding: 10px 12px;
        }}

        .sound-btn {{
            font-size: 14px;
            padding: 10px 12px;
        }}

        .effect {{
            font-size: 34px;
        }}
    }}
</style>
</head>

<body>
<div class="game-wrap">
    <div class="top-bar">
        <div class="badge">문제<br><span id="qNum">0</span> / <span id="total">0</span></div>
        <div class="badge">정답<br><span id="score">0</span>개</div>
        <div class="badge">상태<br><span id="state">대기</span></div>
    </div>

    <div id="message" class="message">
        게임 시작을 누르고 한국어 상황을 영어로 말해 보세요!
    </div>

    <div class="card-area">
        <div id="questionCard" class="question-card">
            <div id="category" class="category">주제</div>
            <div id="korean" class="korean">게임 시작을 눌러 주세요 🎮</div>
            <div id="hint" class="hint"></div>
        </div>
    </div>

    <div id="recognized" class="recognized">
        Chrome에서 마이크 권한을 허용해 주세요.
    </div>

    <div id="answerArea" class="answer-area">
        <div class="answer-label">정답 문장</div>
        <div id="answerSentence" class="answer-sentence"></div>
        <button class="btn sound-btn" onclick="speakCurrentAnswer()">🔊 원어민 발음 듣기</button>
    </div>

    <div class="btn-row">
        <button id="startBtn" class="btn" onclick="startGame()">🎤 게임 시작</button>
        <button id="micBtn" class="btn" onclick="startOneRecognition()" style="display:none;">🎙️ 말하기</button>
        <button class="btn sub-btn" onclick="showAnswer()">👀 정답 보기</button>
        <button class="btn sub-btn" onclick="nextQuestion()">➡️ 다음</button>
        <button class="btn sub-btn" onclick="resetGame()">🔄 다시 시작</button>
    </div>
</div>

<script>
const questions = {questions_json};
const passRatio = {pass_ratio} / 100;
const showFirstHint = {hint_js};
const autoSound = {auto_sound_js};

let currentIndex = 0;
let score = 0;
let gameStarted = false;
let alreadyCorrect = false;
let recognition = null;
let isListening = false;

const qNum = document.getElementById("qNum");
const total = document.getElementById("total");
const scoreBox = document.getElementById("score");
const stateBox = document.getElementById("state");
const messageBox = document.getElementById("message");
const questionCard = document.getElementById("questionCard");
const categoryBox = document.getElementById("category");
const koreanBox = document.getElementById("korean");
const hintBox = document.getElementById("hint");
const answerArea = document.getElementById("answerArea");
const answerSentence = document.getElementById("answerSentence");
const recognizedBox = document.getElementById("recognized");
const startBtn = document.getElementById("startBtn");
const micBtn = document.getElementById("micBtn");

total.innerText = questions.length;

function normalizeText(text) {{
    return String(text || "")
        .toLowerCase()
        .replace(/\\bi'm\\b/g, "i am")
        .replace(/\\bim\\b/g, "i am")
        .replace(/\\byou're\\b/g, "you are")
        .replace(/\\bhe's\\b/g, "he is")
        .replace(/\\bshe's\\b/g, "she is")
        .replace(/\\bit's\\b/g, "it is")
        .replace(/\\bwe're\\b/g, "we are")
        .replace(/\\bthey're\\b/g, "they are")
        .replace(/\\bdon't\\b/g, "do not")
        .replace(/\\bdoesn't\\b/g, "does not")
        .replace(/\\bdidn't\\b/g, "did not")
        .replace(/\\bcan't\\b/g, "cannot")
        .replace(/\\bcant\\b/g, "cannot")
        .replace(/\\bi'll\\b/g, "i will")
        .replace(/\\byou'll\\b/g, "you will")
        .replace(/\\bhe'll\\b/g, "he will")
        .replace(/\\bshe'll\\b/g, "she will")
        .replace(/[.,!?;:'"’‘“”]/g, "")
        .replace(/-/g, " ")
        .replace(/\\s+/g, " ")
        .trim();
}}

function wordsOnly(text) {{
    return normalizeText(text).split(" ").filter(w => w.length > 0);
}}

function editDistance(a, b) {{
    a = String(a || "");
    b = String(b || "");
    const dp = Array.from({{ length: a.length + 1 }}, () => Array(b.length + 1).fill(0));

    for (let i = 0; i <= a.length; i++) dp[i][0] = i;
    for (let j = 0; j <= b.length; j++) dp[0][j] = j;

    for (let i = 1; i <= a.length; i++) {{
        for (let j = 1; j <= b.length; j++) {{
            const cost = a[i - 1] === b[j - 1] ? 0 : 1;
            dp[i][j] = Math.min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            );
        }}
    }}
    return dp[a.length][b.length];
}}

function similarity(a, b) {{
    if (!a || !b) return 0;
    if (a === b) return 1;
    const dist = editDistance(a, b);
    return 1 - dist / Math.max(a.length, b.length);
}}

function soundKey(text) {{
    return normalizeText(text)
        .replace(/[^a-z]/g, "")
        .replace(/tion/g, "shun")
        .replace(/sion/g, "shun")
        .replace(/th/g, "d")
        .replace(/ph/g, "f")
        .replace(/gh/g, "g")
        .replace(/ck/g, "k")
        .replace(/qu/g, "kw")
        .replace(/x/g, "ks")
        .replace(/c/g, "k")
        .replace(/q/g, "k")
        .replace(/z/g, "s")
        .replace(/v/g, "b")
        .replace(/r/g, "l")
        .replace(/ee/g, "i")
        .replace(/ea/g, "i")
        .replace(/ie/g, "i")
        .replace(/ei/g, "i")
        .replace(/oo/g, "u")
        .replace(/ou/g, "u")
        .replace(/ow/g, "o")
        .replace(/oa/g, "o")
        .replace(/ai/g, "e")
        .replace(/ay/g, "e")
        .replace(/[aeiouy]/g, "")
        .replace(/(.)\\1+/g, "$1");
}}

function aliasMatch(spokenWord, answerWord) {{
    const sw = normalizeText(spokenWord).replace(/\\s+/g, "");
    const aw = normalizeText(answerWord).replace(/\\s+/g, "");

    const aliases = {{
        "i": ["i", "eye", "ai"],
        "you": ["you", "u", "yew"],
        "he": ["he", "hi"],
        "she": ["she", "see", "sea"],
        "we": ["we", "wee"],
        "they": ["they", "day"],
        "one": ["one", "won"],
        "two": ["two", "to", "too"],
        "three": ["three", "tree"],
        "four": ["four", "for"],
        "eight": ["eight", "ate"],
        "here": ["here", "hear"],
        "there": ["there", "their"],
        "right": ["right", "write"],
        "wait": ["wait", "weight"],
        "know": ["know", "no"],
        "night": ["night", "knight"],
        "okay": ["okay", "ok"],
        "phone": ["phone", "fone"],
        "coffee": ["coffee", "coffe"],
        "please": ["please", "plz"]
    }};

    if (!aliases[aw]) return false;
    return aliases[aw].includes(sw);
}}

function isUnderstandableWord(spokenWord, answerWord) {{
    const sw = normalizeText(spokenWord).replace(/\\s+/g, "");
    const aw = normalizeText(answerWord).replace(/\\s+/g, "");
    if (!sw || !aw) return false;
    if (sw === aw) return true;
    if (aliasMatch(sw, aw)) return true;

    const dist = editDistance(sw, aw);
    const sim = similarity(sw, aw);

    const soundSw = soundKey(sw);
    const soundAw = soundKey(aw);

    const sameFirst = sw[0] === aw[0];
    const sameFirstTwo = sw.slice(0, 2) === aw.slice(0, 2);
    const soundSame = soundSw && soundAw && soundSw === soundAw;
    const soundSameFirst = soundSw && soundAw && soundSw[0] === soundAw[0];

    // 너무 다른 단어 방지: 첫소리도 다르고 유사도도 낮으면 오답
    if (!sameFirst && !soundSameFirst && sim < 0.78) return false;

    // 자음 뼈대가 같으면 발음/인식 차이로 허용
    if (soundSame) return true;

    // 짧은 기능어는 지나치게 관대하게 처리하지 않음
    if (aw.length <= 2) return sim >= 0.90;

    // 3~4글자 단어: 1글자 차이 또는 발음 유사 허용
    if (aw.length <= 4) {{
        return (sameFirst || soundSameFirst) && (dist <= 1 || sim >= 0.74);
    }}

    // 5~6글자 단어: 1~2글자 차이 또는 유사도 기준 허용
    if (aw.length <= 6) {{
        return (sameFirst || soundSameFirst || sameFirstTwo) && (dist <= 2 || sim >= 0.72);
    }}

    // 긴 단어는 좀 더 관대하게
    return (sameFirst || soundSameFirst || sameFirstTwo) && (dist <= 3 || sim >= 0.68);
}}

function sentenceMatch(spoken, target) {{
    const s = normalizeText(spoken);
    const t = normalizeText(target);
    if (!s || !t) return false;
    if (s === t) return true;
    if (s.includes(t) || t.includes(s)) {{
        const ratio = Math.min(s.length, t.length) / Math.max(s.length, t.length);
        if (ratio > 0.75) return true;
    }}

    const spokenWords = wordsOnly(s);
    const targetWords = wordsOnly(t);

    if (spokenWords.length === 0 || targetWords.length === 0) return false;

    let matched = 0;
    let used = new Array(spokenWords.length).fill(false);

    for (let tw of targetWords) {{
        let found = false;

        for (let i = 0; i < spokenWords.length; i++) {{
            if (used[i]) continue;
            if (isUnderstandableWord(spokenWords[i], tw)) {{
                used[i] = true;
                found = true;
                break;
            }}
        }}

        if (found) matched += 1;
    }}

    const ratio = matched / targetWords.length;

    // 긴 문장은 ASR이 중간을 누락할 수 있어 슬라이더 기준과 핵심어 기준을 함께 사용
    const minRequired = Math.max(passRatio, 0.55);
    return ratio >= minRequired;
}}

function makeFirstLetterHint(sentence) {{
    return normalizeText(sentence)
        .split(" ")
        .map(w => w ? w[0] + "_".repeat(Math.max(0, Math.min(w.length - 1, 4))) : "")
        .join(" ");
}}

function escapeHtml(text) {{
    return String(text || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}}

function stopRecognition() {{
    if (recognition) {{
        recognition.onend = null;
        recognition.onerror = null;
        recognition.onresult = null;
        try {{ recognition.abort(); }} catch(e) {{}}
        try {{ recognition.stop(); }} catch(e) {{}}
    }}
    recognition = null;
    isListening = false;
    micBtn.innerText = "🎙️ 말하기";
    micBtn.disabled = false;
    micBtn.style.opacity = "1";
}}

function showCurrentQuestion() {{
    if (currentIndex >= questions.length) {{
        endGame();
        return;
    }}

    stopRecognition();

    alreadyCorrect = false;
    questionCard.classList.remove("pop");
    questionCard.style.opacity = "1";
    questionCard.style.transform = "scale(1)";
    questionCard.style.display = "flex";

    answerArea.style.display = "none";
    recognizedBox.innerText = "";

    const q = questions[currentIndex];

    qNum.innerText = currentIndex + 1;
    categoryBox.innerText = q.category;
    koreanBox.innerText = q.korean;

    if (showFirstHint) {{
        hintBox.style.display = "block";
        hintBox.innerText = "힌트: " + makeFirstLetterHint(q.sentence);
    }} else {{
        hintBox.style.display = "none";
        hintBox.innerText = "";
    }}

    messageBox.innerText = "🎙️ 말하기 버튼을 누르고 영어로 말해 보세요.";
    stateBox.innerText = "대기";
    startBtn.style.display = "none";
    micBtn.style.display = "inline-block";
}}

function showHintAfterWrong() {{
    if (currentIndex >= questions.length) return;
    const q = questions[currentIndex];
    hintBox.style.display = "block";
    hintBox.innerText = "힌트: " + (q.hint || makeFirstLetterHint(q.sentence));
}}

function showAnswerArea() {{
    if (currentIndex >= questions.length) return;
    answerSentence.innerText = questions[currentIndex].sentence;
    answerArea.style.display = "block";
}}

function speakText(text) {{
    if (!("speechSynthesis" in window)) {{
        recognizedBox.innerText = "❌ 이 브라우저는 음성 재생을 지원하지 않습니다.";
        return;
    }}

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 0.85;
    utterance.pitch = 1.02;

    const voices = window.speechSynthesis.getVoices();
    const preferred = voices.find(v =>
        v.lang && v.lang.toLowerCase().startsWith("en") &&
        /(samantha|jenny|aria|zira|google us english|karen|victoria|female)/i.test(v.name)
    );
    if (preferred) utterance.voice = preferred;

    window.speechSynthesis.speak(utterance);
}}

function speakCurrentAnswer() {{
    if (currentIndex >= questions.length) return;
    speakText(questions[currentIndex].sentence);
}}

function showEffects() {{
    const wrap = document.querySelector(".game-wrap");
    const icons = ["💥", "✨", "🎉", "⭐", "👏", "🌟"];

    for (let i = 0; i < 12; i++) {{
        const e = document.createElement("div");
        e.className = "effect";
        e.innerText = icons[Math.floor(Math.random() * icons.length)];
        e.style.left = Math.random() * 80 + 10 + "%";
        e.style.top = Math.random() * 50 + 20 + "%";
        wrap.appendChild(e);

        setTimeout(() => {{
            e.remove();
        }}, 850);
    }}
}}

function correctAnswer(transcript) {{
    if (alreadyCorrect) return;

    alreadyCorrect = true;
    score++;
    scoreBox.innerText = score;

    recognizedBox.innerHTML = "🗣️ " + escapeHtml(transcript) + " <span style='color:#16a34a;'>✅ 정답입니다</span>";
    messageBox.innerText = "💥 정답! 다음 문제는 직접 넘기세요.";
    stateBox.innerText = "정답";

    showAnswerArea();

    questionCard.classList.add("pop");
    showEffects();

    stopRecognition();

    if (autoSound) {{
        setTimeout(() => {{
            speakCurrentAnswer();
        }}, 350);
    }}
}}

function checkSpeech(transcript) {{
    if (!gameStarted || alreadyCorrect || currentIndex >= questions.length) return;

    recognizedBox.innerText = "🗣️ 인식: " + transcript;

    const target = questions[currentIndex].sentence;

    if (sentenceMatch(transcript, target)) {{
        correctAnswer(transcript);
    }} else {{
        messageBox.innerText = "🍊 아직 정답으로 인식되지 않았습니다. 힌트를 보고 다시 말해 보세요.";
        stateBox.innerText = "다시";
        showHintAfterWrong();
        showAnswerButtonOnly();
    }}
}}

function showAnswerButtonOnly() {{
    // 버튼은 항상 보이므로 별도 처리 없음. 의미상 함수만 유지.
}}

async function requestMicPermission() {{
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {{
        try {{
            const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
            stream.getTracks().forEach(track => track.stop());
            return true;
        }} catch(e) {{
            recognizedBox.innerText = "마이크 허용 후 다시 눌러 주세요.";
            return false;
        }}
    }}
    return true;
}}

async function startOneRecognition() {{
    if (!gameStarted || currentIndex >= questions.length || alreadyCorrect) return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {{
        recognizedBox.innerText = "❌ 이 브라우저는 음성 인식을 지원하지 않습니다. Chrome으로 접속해 주세요.";
        return;
    }}

    if (isListening) {{
        stopRecognition();
        return;
    }}

    const micOK = await requestMicPermission();
    if (!micOK) return;

    stopRecognition();
    window.speechSynthesis.cancel();

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.maxAlternatives = 5;

    isListening = true;
    micBtn.innerText = "👂 듣는 중";
    micBtn.disabled = true;
    micBtn.style.opacity = "0.75";
    messageBox.innerText = "듣고 있습니다.";
    stateBox.innerText = "듣는 중";
    recognizedBox.innerText = "";

    let finalTranscript = "";
    let checked = false;

    recognition.onresult = function(event) {{
        let currentText = "";
        let hasFinal = false;

        for (let i = 0; i < event.results.length; i++) {{
            let best = event.results[i][0].transcript.trim();

            for (let j = 0; j < event.results[i].length; j++) {{
                const alt = event.results[i][j].transcript.trim();
                if (sentenceMatch(alt, questions[currentIndex].sentence)) {{
                    best = alt;
                    break;
                }}
            }}

            if (best) currentText += (currentText ? " " : "") + best;
            if (event.results[i].isFinal) hasFinal = true;
        }}

        if (currentText) {{
            finalTranscript = currentText;
            recognizedBox.innerText = "🗣️ 인식: " + currentText;
        }}

        if (hasFinal && !checked) {{
            checked = true;
            checkSpeech(finalTranscript);
        }}
    }};

    recognition.onerror = function(event) {{
        showHintAfterWrong();
        recognizedBox.innerText = event.error === "no-speech"
            ? "인식하지 못했습니다. 다시 눌러 주세요."
            : "마이크 오류가 났습니다. 다시 눌러 주세요.";
        messageBox.innerText = "다시 말하거나 정답을 확인할 수 있습니다.";
        stateBox.innerText = "오류";
        stopRecognition();
    }};

    recognition.onend = function() {{
        if (!checked && finalTranscript) {{
            checked = true;
            checkSpeech(finalTranscript);
        }}
        isListening = false;
        micBtn.innerText = "🎙️ 말하기";
        micBtn.disabled = false;
        micBtn.style.opacity = "1";
    }};

    try {{
        recognition.start();
    }} catch(e) {{
        recognizedBox.innerText = "마이크가 아직 준비되지 않았습니다. 다시 눌러 주세요.";
        stopRecognition();
    }}
}}

function startGame() {{
    gameStarted = true;
    currentIndex = 0;
    score = 0;
    alreadyCorrect = false;

    scoreBox.innerText = score;
    qNum.innerText = 1;
    total.innerText = questions.length;
    stateBox.innerText = "시작";

    showCurrentQuestion();
}}

function nextQuestion() {{
    if (!gameStarted) return;

    stopRecognition();
    window.speechSynthesis.cancel();

    currentIndex++;
    showCurrentQuestion();
}}

function showAnswer() {{
    if (!gameStarted || currentIndex >= questions.length) return;

    showAnswerArea();
    showHintAfterWrong();
    messageBox.innerText = "👀 정답을 확인하고 다시 말해 보세요. 맞히면 정답으로 인정됩니다.";
    stateBox.innerText = "정답 보기";
    speakCurrentAnswer();
}}

function resetGame() {{
    stopRecognition();
    window.speechSynthesis.cancel();

    gameStarted = false;
    currentIndex = 0;
    score = 0;
    alreadyCorrect = false;

    scoreBox.innerText = score;
    qNum.innerText = 0;
    stateBox.innerText = "대기";
    messageBox.innerText = "게임 시작을 누르고 한국어 상황을 영어로 말해 보세요!";
    categoryBox.innerText = "주제";
    koreanBox.innerText = "게임 시작을 눌러 주세요 🎮";
    hintBox.innerText = "";
    hintBox.style.display = "none";
    answerArea.style.display = "none";
    recognizedBox.innerText = "Chrome에서 마이크 권한을 허용해 주세요.";
    questionCard.classList.remove("pop");
    questionCard.style.opacity = "1";
    questionCard.style.transform = "scale(1)";
    questionCard.style.display = "flex";

    startBtn.style.display = "inline-block";
    micBtn.style.display = "none";
}}

function endGame() {{
    stopRecognition();
    window.speechSynthesis.cancel();

    gameStarted = false;
    alreadyCorrect = false;

    stateBox.innerText = "완료";
    messageBox.innerText = "🎉 게임 종료! 수고했습니다!";
    categoryBox.innerText = "최종 점수";
    koreanBox.innerText = score + " / " + questions.length;
    hintBox.style.display = "block";
    hintBox.innerText = "다시 하려면 다시 시작을 눌러 주세요.";
    answerArea.style.display = "none";
    recognizedBox.innerText = "최종 정답 개수: " + score + "개";

    startBtn.style.display = "inline-block";
    micBtn.style.display = "none";
}}
</script>
</body>
</html>
"""

components.html(game_html, height=760, scrolling=True)
