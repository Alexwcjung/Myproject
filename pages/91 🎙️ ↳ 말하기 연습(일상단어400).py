import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="일상 문장구조 말하기 훈련",
    page_icon="🎙️",
    layout="wide"
)

# =========================================================
# 데이터
# - 일상단어 400 느낌의 어휘를 활용
# - 각 문제를 2문장 중심으로 짧게 조정
# - 기능은 생존 문장 말하기 훈련 형태
# =========================================================
PRACTICE_ITEMS = [{'cat': '🏫 학교생활',
  'ko': '나는 오늘 수학 과제가 있어. 도서관에서 교과서를 볼 거야.',
  'blank': 'I have a ______ assignment today. I will read my ______ in the library.',
  'answer': 'I have a math assignment today. I will read my textbook in the library.',
  'hint': 'math / textbook',
  'emoji': '📚'},
 {'cat': '🏫 학교생활',
  'ko': '우리는 과학 프로젝트를 준비하고 있어. 내일 발표가 있어서 조금 긴장돼.',
  'blank': 'We are preparing a ______ project. I am a little ______ because we have a presentation tomorrow.',
  'answer': 'We are preparing a science project. I am a little nervous because we have a presentation tomorrow.',
  'hint': 'science / nervous',
  'emoji': '🧪'},
 {'cat': '🏫 학교생활',
  'ko': '나는 복도에서 친구를 만났어. 우리는 일정표를 확인했어.',
  'blank': 'I met my ______ in the hallway. We checked the ______ together.',
  'answer': 'I met my friend in the hallway. We checked the schedule together.',
  'hint': 'friend / schedule',
  'emoji': '🏫'},
 {'cat': '✏️ 교실 활동',
  'ko': '문장을 공책에 베껴 쓰세요. 중요한 단어에 밑줄을 치세요.',
  'blank': '______ the sentence in your notebook. ______ the important words.',
  'answer': 'Copy the sentence in your notebook. Underline the important words.',
  'hint': 'Copy / Underline',
  'emoji': '✏️'},
 {'cat': '✏️ 교실 활동',
  'ko': '선생님이 예시를 설명했어. 우리는 답을 짝과 토론했어.',
  'blank': 'The teacher ______ the example. We ______ the answer with a partner.',
  'answer': 'The teacher explained the example. We discussed the answer with a partner.',
  'hint': 'explained / discussed',
  'emoji': '🧑\u200d🏫'},
 {'cat': '✏️ 교실 활동',
  'ko': '단어의 철자를 말해 주세요. 어려우면 천천히 반복해도 됩니다.',
  'blank': 'Please ______ the word. If it is difficult, you can ______ it slowly.',
  'answer': 'Please spell the word. If it is difficult, you can repeat it slowly.',
  'hint': 'spell / repeat',
  'emoji': '🔁'},
 {'cat': '🏠 집과 생활',
  'ko': '나는 거실에서 텔레비전을 보고 있었어. 음식이 없어서 부엌으로 갔어.',
  'blank': 'I was watching ______ in the living room. There was no food, so I went to the ______.',
  'answer': 'I was watching television in the living room. There was no food, so I went to the kitchen.',
  'hint': 'television / kitchen',
  'emoji': '🏠'},
 {'cat': '🏠 집과 생활',
  'ko': '내 방에는 담요와 베개가 있어. 나는 피곤해서 일찍 자고 싶어.',
  'blank': 'There is a ______ and a pillow in my bedroom. I want to sleep ______ because I am tired.',
  'answer': 'There is a blanket and a pillow in my bedroom. I want to sleep early because I am tired.',
  'hint': 'blanket / early',
  'emoji': '🛏️'},
 {'cat': '🏠 집과 생활',
  'ko': '쓰레기를 버려 주세요. 손을 비누로 씻어 주세요.',
  'blank': 'Please throw away the ______. Please wash your hands with ______.',
  'answer': 'Please throw away the trash. Please wash your hands with soap.',
  'hint': 'trash / soap',
  'emoji': '🧼'},
 {'cat': '🌅 하루 일과',
  'ko': '나는 보통 아침에 일찍 일어나. 학교에 가기 전에 샤워해.',
  'blank': 'I usually ______ early in the morning. I take a ______ before I go to school.',
  'answer': 'I usually get up early in the morning. I take a shower before I go to school.',
  'hint': 'get up / shower',
  'emoji': '🌅'},
 {'cat': '🌅 하루 일과',
  'ko': '주말에는 늦게 일어나. 평일에는 항상 일찍 출발해.',
  'blank': 'I wake up late on ______. I always leave early on ______.',
  'answer': 'I wake up late on weekends. I always leave early on weekdays.',
  'hint': 'weekends / weekdays',
  'emoji': '🚌'},
 {'cat': '🌅 하루 일과',
  'ko': '나는 숙제를 끝낸 뒤에 쉬어. 가끔 음악을 들으면서 긴장을 풀어.',
  'blank': 'After I finish my ______, I relax. Sometimes I listen to ______ to feel calm.',
  'answer': 'After I finish my homework, I relax. Sometimes I listen to music to feel calm.',
  'hint': 'homework / music',
  'emoji': '🎧'},
 {'cat': '🎮 취미와 여가',
  'ko': '내 취미는 영화 보기야. 시간이 있으면 친구와 영화를 봐.',
  'blank': 'My ______ is watching movies. If I have free time, I watch a movie with my ______.',
  'answer': 'My hobby is watching movies. If I have free time, I watch a movie with my friend.',
  'hint': 'hobby / friend',
  'emoji': '🎬'},
 {'cat': '🎮 취미와 여가',
  'ko': '그녀는 사진 촬영을 좋아해. 주말마다 공원에서 사진을 찍어.',
  'blank': 'She likes ______. She takes pictures in the ______ every weekend.',
  'answer': 'She likes photography. She takes pictures in the park every weekend.',
  'hint': 'photography / park',
  'emoji': '📷'},
 {'cat': '🎮 취미와 여가',
  'ko': '나는 캠핑을 좋아해. 오늘은 날씨가 나빠서 집에서 소설을 읽을 거야.',
  'blank': 'I like ______. The weather is bad today, so I will read a ______ at home.',
  'answer': 'I like camping. The weather is bad today, so I will read a novel at home.',
  'hint': 'camping / novel',
  'emoji': '🏕️'},
 {'cat': '⚽ 운동과 활동',
  'ko': '우리는 방과 후에 축구를 할 거야. 경기장에 제시간에 도착해야 해.',
  'blank': 'We will play ______ after school. We should arrive at the ______ on time.',
  'answer': 'We will play soccer after school. We should arrive at the field on time.',
  'hint': 'soccer / field',
  'emoji': '⚽'},
 {'cat': '⚽ 운동과 활동',
  'ko': '그는 농구 경기에 나가고 싶어 해. 하지만 무릎이 아파서 쉬어야 해.',
  'blank': 'He wants to join the ______ match. His knee hurts, so he should ______ today.',
  'answer': 'He wants to join the basketball match. His knee hurts, so he should rest today.',
  'hint': 'basketball / rest',
  'emoji': '🏀'},
 {'cat': '⚽ 운동과 활동',
  'ko': '코치가 우리에게 설명했어. 우리는 대회를 위해 매일 연습할 거야.',
  'blank': 'The ______ explained it to us. We will ______ every day for the competition.',
  'answer': 'The coach explained it to us. We will practice every day for the competition.',
  'hint': 'coach / practice',
  'emoji': '🏟️'},
 {'cat': '🌦️ 날씨와 계절',
  'ko': '오늘은 비가 오고 바람이 불어. 그래서 우산이 필요해.',
  'blank': 'It is ______ and windy today. I need an ______.',
  'answer': 'It is rainy and windy today. I need an umbrella.',
  'hint': 'rainy / umbrella',
  'emoji': '🌧️'},
 {'cat': '🌦️ 날씨와 계절',
  'ko': '겨울에는 날씨가 추워. 하지만 나는 눈 오는 날을 좋아해.',
  'blank': 'It is cold in ______. But I like ______ days.',
  'answer': 'It is cold in winter. But I like snowy days.',
  'hint': 'winter / snowy',
  'emoji': '⛄'},
 {'cat': '🌦️ 날씨와 계절',
  'ko': '일기예보를 확인해 주세요. 오후에는 폭풍우가 올 수 있어요.',
  'blank': 'Please check the weather ______. It may be ______ in the afternoon.',
  'answer': 'Please check the weather forecast. It may be stormy in the afternoon.',
  'hint': 'forecast / stormy',
  'emoji': '🌩️'},
 {'cat': '🍽️ 식당과 주문',
  'ko': '나는 식당에서 메뉴를 보고 있어. 너무 비싼 요리는 원하지 않아.',
  'blank': 'I am looking at the ______ in the restaurant. I do not want an expensive ______.',
  'answer': 'I am looking at the menu in the restaurant. I do not want an expensive dish.',
  'hint': 'menu / dish',
  'emoji': '🍽️'},
 {'cat': '🍽️ 식당과 주문',
  'ko': '계산서를 가져다 주세요. 영수증도 필요해요.',
  'blank': 'Please bring the ______. I also need the ______.',
  'answer': 'Please bring the bill. I also need the receipt.',
  'hint': 'bill / receipt',
  'emoji': '🧾'},
 {'cat': '🍽️ 식당과 주문',
  'ko': '그녀는 샐러드를 주문했어. 우리는 식사 후에 디저트를 먹을 거야.',
  'blank': 'She ordered a ______. We will have ______ after the meal.',
  'answer': 'She ordered a salad. We will have dessert after the meal.',
  'hint': 'salad / dessert',
  'emoji': '🥗'},
 {'cat': '🛍️ 쇼핑과 가격',
  'ko': '이 재킷은 너무 비싸. 할인 쿠폰이 있으면 살 수 있어.',
  'blank': 'This jacket is too ______. If I have a discount ______, I can buy it.',
  'answer': 'This jacket is too expensive. If I have a discount coupon, I can buy it.',
  'hint': 'expensive / coupon',
  'emoji': '🛍️'},
 {'cat': '🛍️ 쇼핑과 가격',
  'ko': '계산원이 거스름돈을 줬어. 나는 영수증을 확인했어.',
  'blank': 'The ______ gave me change. I checked the ______.',
  'answer': 'The cashier gave me change. I checked the receipt.',
  'hint': 'cashier / receipt',
  'emoji': '💵'},
 {'cat': '🛍️ 쇼핑과 가격',
  'ko': '색깔은 좋아. 하지만 사이즈가 맞지 않아서 교환하고 싶어.',
  'blank': 'The color is good. But the ______ is not right, so I want an ______.',
  'answer': 'The color is good. But the size is not right, so I want an exchange.',
  'hint': 'size / exchange',
  'emoji': '👕'},
 {'cat': '🚇 교통과 길 찾기',
  'ko': '나는 길을 잃었어. 지하철역에 가는 방향을 알고 싶어.',
  'blank': 'I am ______. I want to know the direction to the ______ station.',
  'answer': 'I am lost. I want to know the direction to the subway station.',
  'hint': 'lost / subway',
  'emoji': '🚇'},
 {'cat': '🚇 교통과 길 찾기',
  'ko': '버스 정류장은 모퉁이 근처에 있어. 횡단보도를 건너서 오른쪽으로 가세요.',
  'blank': 'The bus stop is near the ______. Cross the crosswalk and go ______.',
  'answer': 'The bus stop is near the corner. Cross the crosswalk and go right.',
  'hint': 'corner / right',
  'emoji': '🚏'},
 {'cat': '🚇 교통과 길 찾기',
  'ko': '공항에 가려면 터미널에서 갈아타야 해. 시간이 없으니 빨리 움직여야 해.',
  'blank': 'To get to the ______, you need to transfer at the terminal. We should move ______.',
  'answer': 'To get to the airport, you need to transfer at the terminal. We should move quickly.',
  'hint': 'airport / quickly',
  'emoji': '✈️'},
 {'cat': '🧳 여행과 숙박',
  'ko': '나는 호텔 예약을 확인하고 싶어. 여권은 내 배낭 안에 있어.',
  'blank': 'I want to check my hotel ______. My passport is in my ______.',
  'answer': 'I want to check my hotel reservation. My passport is in my backpack.',
  'hint': 'reservation / backpack',
  'emoji': '🧳'},
 {'cat': '🧳 여행과 숙박',
  'ko': '우리는 현지 박물관을 방문할 거야. 유명한 기념품도 사고 싶어.',
  'blank': 'We will visit a local ______. I also want to buy a famous ______.',
  'answer': 'We will visit a local museum. I also want to buy a famous souvenir.',
  'hint': 'museum / souvenir',
  'emoji': '🏛️'},
 {'cat': '🧳 여행과 숙박',
  'ko': '체크인 시간이 늦었어. 하지만 직원이 우리를 도와줬어.',
  'blank': 'The check-in time was ______. But the staff ______ us.',
  'answer': 'The check-in time was late. But the staff helped us.',
  'hint': 'late / helped',
  'emoji': '🏨'},
 {'cat': '😊 감정 표현',
  'ko': '나는 발표 전에 긴장했어. 끝난 뒤에는 자랑스러웠어.',
  'blank': 'I was ______ before the presentation. I felt ______ after it.',
  'answer': 'I was nervous before the presentation. I felt proud after it.',
  'hint': 'nervous / proud',
  'emoji': '👏'},
 {'cat': '😊 감정 표현',
  'ko': '그는 시험 결과에 실망했어. 하지만 조언을 듣고 다시 희망을 가졌어.',
  'blank': 'He was ______ with the test result. But he felt ______ again after the advice.',
  'answer': 'He was disappointed with the test result. But he felt hopeful again after the advice.',
  'hint': 'disappointed / hopeful',
  'emoji': '😊'},
 {'cat': '😊 감정 표현',
  'ko': '나는 혼자 있어서 외로웠어. 그래서 친구에게 메시지를 보냈어.',
  'blank': 'I felt ______ because I was alone. So I sent a ______ to my friend.',
  'answer': 'I felt lonely because I was alone. So I sent a message to my friend.',
  'hint': 'lonely / message',
  'emoji': '💬'},
 {'cat': '📱 미디어와 스마트폰',
  'ko': '내 스마트폰 배터리가 거의 없어. 와이파이 비밀번호가 필요해.',
  'blank': 'My smartphone ______ is almost dead. I need the Wi-Fi ______.',
  'answer': 'My smartphone battery is almost dead. I need the Wi-Fi password.',
  'hint': 'battery / password',
  'emoji': '📱'},
 {'cat': '📱 미디어와 스마트폰',
  'ko': '나는 웹사이트에서 뉴스를 검색했어. 중요한 게시물에 댓글을 달았어.',
  'blank': 'I searched for ______ on the website. I wrote a ______ on an important post.',
  'answer': 'I searched for news on the website. I wrote a comment on an important post.',
  'hint': 'news / comment',
  'emoji': '🌐'},
 {'cat': '📱 미디어와 스마트폰',
  'ko': '영상 통화가 끊겼어. 화면이 멈췄어.',
  'blank': 'The video call stopped. The ______ froze.',
  'answer': 'The video call stopped. The screen froze.',
  'hint': 'screen',
  'emoji': '📹'},
 {'cat': '🌈 직업과 미래',
  'ko': '나는 미래에 기술자가 되고 싶어. 그래서 필요한 경험을 배우고 있어.',
  'blank': 'I want to become an ______ in the future. So I am learning useful ______.',
  'answer': 'I want to become an engineer in the future. So I am learning useful experience.',
  'hint': 'engineer / experience',
  'emoji': '🛠️'},
 {'cat': '🌈 직업과 미래',
  'ko': '그녀의 꿈은 요리사가 되는 거야. 면접 전에 목표를 설명하려고 해.',
  'blank': 'Her dream is to become a ______. She wants to explain her ______ before the interview.',
  'answer': 'Her dream is to become a chef. She wants to explain her goal before the interview.',
  'hint': 'chef / goal',
  'emoji': '👩\u200d🍳'},
 {'cat': '🌈 직업과 미래',
  'ko': '나는 소방관을 존경해. 그들은 위험한 상황에서도 사람들을 도와줘.',
  'blank': 'I respect ______. They help people even in ______ situations.',
  'answer': 'I respect firefighters. They help people even in dangerous situations.',
  'hint': 'firefighters / dangerous',
  'emoji': '🚒'}]
# =========================================================
# 디자인
# =========================================================
st.markdown(
    """
    <style>
    @media (max-width: 640px) {
        #speaking-app {
            padding: 10px !important;
            border-radius: 20px !important;
        }
        #speaking-app #blankSentence {
            font-size: 20px !important;
            padding: 13px 12px !important;
            margin-bottom: 8px !important;
            line-height: 1.45 !important;
        }
        #speaking-app #koPrompt {
            font-size: 19px !important;
            margin-bottom: 8px !important;
            line-height: 1.35 !important;
        }
        #speaking-app #transcriptBox {
            font-size: 17px !important;
            line-height: 1.45 !important;
        }
        #speaking-app #micBtn {
            width: 78px !important;
            height: 78px !important;
            font-size: 27px !important;
        }
        #speaking-app #hintBtn,
        #speaking-app #answerBtn,
        #speaking-app #listenBtn,
        #speaking-app #nextBtn {
            padding: 13px 8px !important;
            min-height: 58px !important;
            font-size: 17px !important;
        }
        #speaking-app #hintBox {
            font-size: 13px !important;
            padding: 6px 8px !important;
            line-height: 1.25 !important;
            max-width: 100% !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
            white-space: normal !important;
            box-sizing: border-box !important;
        }
    }
    

        #speaking-app #hintBtn:hover,
        #speaking-app #answerBtn:hover,
        #speaking-app #listenBtn:hover,
        #speaking-app #nextBtn:hover {
            border-color: #22c55e !important;
            color: #22c55e !important;
        }

        @media (max-width: 640px) {
            #speaking-app div[style*="grid-template-columns:repeat(3"] {
                grid-template-columns: repeat(1, minmax(0, 1fr)) !important;
            }
        }

</style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 말하기 훈련 컴포넌트
# =========================================================
def speaking_practice_component(items):
    items_json = json.dumps(items, ensure_ascii=False)

    html = r"""
    <div id="speaking-app" style="
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #eff6ff 0%, #fdf4ff 35%, #fff7ed 68%, #f0fdf4 100%);
        border: 2px solid #c4b5fd;
        border-radius: 34px;
        padding: 24px;
        box-shadow: 0 12px 28px rgba(124,58,237,0.12);
    ">
        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:18px;">
            <label style="font-weight:900; color:#334155;">문장 범위 선택</label>
            <select id="categorySelect" style="
                padding: 10px 14px;
                border-radius: 999px;
                border: 1.5px solid #bae6fd;
                font-size: 15px;
                font-weight: 800;
                color: #0f172a;
                background: white;
            "></select>

            <button id="randomBtn" style="
                border: 1.5px solid #c7d2fe;
                background: white;
                color: #3730a3;
                border-radius: 999px;
                padding: 10px 15px;
                font-weight: 900;
                cursor: pointer;
            ">🎲 이 범위 섞기</button>

            <button id="resetBtn" style="
                border: 1.5px solid #fed7aa;
                background: #fff7ed;
                color: #9a3412;
                border-radius: 999px;
                padding: 10px 15px;
                font-weight: 900;
                cursor: pointer;
            ">🔄 점수 초기화</button>
        </div>

        <div style="
            background:white;
            border-radius:26px;
            padding:24px;
            border:1.5px solid #e0f2fe;
            box-shadow:0 5px 16px rgba(0,0,0,0.055);
        ">
            <div style="display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <div id="categoryLabel" style="
                    display:inline-block;
                    background:linear-gradient(135deg,#dbeafe,#ede9fe);
                    color:#3730a3;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1.5px solid #c4b5fd;
                "></div>

                <div id="scoreLabel" style="
                    display:inline-block;
                    background:linear-gradient(135deg,#dcfce7,#fef9c3);
                    color:#166534;
                    border-radius:999px;
                    padding:8px 14px;
                    font-size:15px;
                    font-weight:900;
                    border:1.5px solid #86efac;
                ">정답 0개</div>
            </div>

            <div style="
                font-size: 26px;
                font-weight: 900;
                color: #111827;
                line-height: 1.35;
                margin-bottom: 10px;
            " id="koPrompt">
                한국어 상황
            </div>

            <div style="
                background: linear-gradient(135deg, #ffffff 0%, #eff6ff 45%, #fdf4ff 100%);
                border: 2px solid #c4b5fd;
                border-radius: 24px;
                padding: 18px 16px;
                margin-bottom: 12px;
                font-size: 28px;
                font-weight: 900;
                color: #1f2937;
                line-height: 1.55;
                box-shadow: 0 6px 16px rgba(99,102,241,0.08);
                word-break: break-word;
            " id="blankSentence">
                I am ______.
            </div>

            <div style="
                background:linear-gradient(135deg,#eef2ff,#fdf2f8);
                border:1.5px solid #c4b5fd;
                border-radius:20px;
                padding:14px 16px;
                margin-bottom:12px;
                min-height:52px;
                box-shadow: 0 4px 12px rgba(124,58,237,0.08);
            ">
                <div id="transcriptBox" style="
                    font-size:23px;
                    font-weight:900;
                    color:#4c1d95;
                    line-height:1.6;
                    min-height:32px;
                    word-break: break-word;
                "></div>
            </div>

            <div style="display:flex; flex-direction:column; gap:12px; align-items:center; justify-content:center; margin-bottom:12px;">
                <button id="micBtn" style="
                    border:4px solid rgba(255,255,255,0.95);
                    background: linear-gradient(135deg, #8b5cf6, #ec4899);
                    color:white;
                    border-radius:999px;
                    width:108px;
                    height:108px;
                    font-weight:1000;
                    cursor:pointer;
                    font-size:38px;
                    box-shadow:0 12px 26px rgba(124,58,237,0.26);
                    flex: 0 0 auto;
                ">🎙️</button>

                <div style="display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:10px; width:100%; max-width:760px;">
                    <button id="hintBtn" style="
                        border:1.5px solid #bbf7d0;
                        background:white;
                        color:#111827;
                        border-radius:999px;
                        padding:18px 14px;
                        min-height:72px;
                        font-size:22px;
                        font-weight:1000;
                        cursor:pointer;
                        box-shadow:0 6px 16px rgba(34,197,94,0.16);
                    ">💡 힌트</button>

                    <button id="answerBtn" style="
                        display:inline-block;
                        border:1.5px solid #bbf7d0;
                        background:white;
                        color:#111827;
                        border-radius:999px;
                        padding:18px 14px;
                        min-height:72px;
                        font-size:22px;
                        font-weight:1000;
                        cursor:pointer;
                        box-shadow:0 6px 16px rgba(34,197,94,0.16);
                    ">👀🔊 정답 보기·듣기</button>

                    <button id="listenBtn" style="display:none;">🔊 듣기</button>

                    <button id="nextBtn" style="
                        display:inline-block;
                        border:1.5px solid #bbf7d0;
                        background:white;
                        color:#111827;
                        border-radius:999px;
                        padding:18px 14px;
                        min-height:72px;
                        font-size:22px;
                        font-weight:1000;
                        cursor:pointer;
                        box-shadow:0 6px 16px rgba(34,197,94,0.16);
                    ">➡️ 다음</button>
                </div>
            </div>

            <div id="hintBox" style="
                display:none;
                background:linear-gradient(135deg,#fff7ed,#fffbeb);
                border:1.5px solid #fbbf24;
                color:#92400e;
                border-radius:14px;
                padding:7px 10px;
                margin-top:6px;
                margin-bottom:6px;
                font-size:16px;
                font-weight:900;
                line-height:1.25;
                word-break:break-word;
                overflow-wrap:anywhere;
                white-space:normal;
                max-width:100%;
                box-sizing:border-box;
                box-shadow: 0 3px 8px rgba(251,191,36,0.10);
            "></div>

            <div id="answerBox" style="display:none;"></div>

            <div id="resultBox" style="
                display:none;
                margin-top:8px;
                font-size:15px;
                font-weight:800;
                color:#64748b;
            "></div>
        </div>

        <div style="
            margin-top:14px;
            color:#64748b;
            font-size:13px;
            line-height:1.6;
            font-weight:700;
        ">
            ※ Chrome 계열 브라우저에서 음성 인식이 가장 잘 작동합니다.<br>
            ※ 문장은 말해야 합니다. 다만 발음 시험은 아니므로 빈칸 핵심 단어와 문장 흐름을 관대하게 봅니다.<br>
            ※ 마이크 권한 요청이 나오면 허용을 눌러 주세요.
        </div>
    </div>

    <script>
    const ITEMS = __ITEMS_JSON__;

    let currentList = [];
    let currentIndex = 0;
    let currentItem = null;
    let score = 0;
    let alreadyCorrect = false;
    let isListening = false;
    let recognitionTimeout = null;
    let speechCheckTimeout = null;
    let finalSpeechBuffer = "";
    let lastCheckedSpeech = "";
    let lastCheckAt = 0;
    let isCheckingSpeech = false;
    let hasSubmittedSpeech = false;

    const categorySelect = document.getElementById("categorySelect");
    const randomBtn = document.getElementById("randomBtn");
    const resetBtn = document.getElementById("resetBtn");
    const categoryLabel = document.getElementById("categoryLabel");
    const scoreLabel = document.getElementById("scoreLabel");
    const koPrompt = document.getElementById("koPrompt");
    const blankSentence = document.getElementById("blankSentence");
    const hintBox = document.getElementById("hintBox");
    const hintBtn = document.getElementById("hintBtn");
    const listenBtn = document.getElementById("listenBtn");
    const answerBtn = document.getElementById("answerBtn");
    const micBtn = document.getElementById("micBtn");
    const nextBtn = document.getElementById("nextBtn");
    const transcriptBox = document.getElementById("transcriptBox");
    const resultBox = document.getElementById("resultBox");

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    function uniqueCategories() {
        const ranges = [];
        const chunkSize = 50;

        for (let start = 0; start < ITEMS.length; start += chunkSize) {
            const end = Math.min(start + chunkSize, ITEMS.length);
            ranges.push((start + 1) + "~" + end);
        }

        return ranges;
    }

    function initCategories() {
        const cats = uniqueCategories();
        categorySelect.innerHTML = "";
        cats.forEach(cat => {
            const option = document.createElement("option");
            option.value = cat;
            option.innerText = cat;
            categorySelect.appendChild(option);
        });
    }

    function getFilteredItems() {
        const selected = categorySelect.value;
        const chunkSize = 50;

        if (!selected || selected.indexOf("~") === -1) {
            return ITEMS.slice(0, chunkSize);
        }

        const parts = selected.split("~");
        const start = parseInt(parts[0], 10) - 1;
        const end = parseInt(parts[1], 10);

        return ITEMS.slice(start, end);
    }

    function shuffleArray(arr) {
        const copied = arr.slice();
        for (let i = copied.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copied[i], copied[j]] = [copied[j], copied[i]];
        }
        return copied;
    }

    function normalizeText(text) {
        return String(text || "")
            .toLowerCase()
            .replace(/\bi'm\b/g, "i am")
            .replace(/\bim\b/g, "i am")
            .replace(/\byou're\b/g, "you are")
            .replace(/\bhe's\b/g, "he is")
            .replace(/\bshe's\b/g, "she is")
            .replace(/\bit's\b/g, "it is")
            .replace(/\bwe're\b/g, "we are")
            .replace(/\bthey're\b/g, "they are")
            .replace(/\bdon't\b/g, "do not")
            .replace(/\bdoesn't\b/g, "does not")
            .replace(/\bdidn't\b/g, "did not")
            .replace(/\bcan't\b/g, "cannot")
            .replace(/\bcant\b/g, "cannot")
            .replace(/\bi'll\b/g, "i will")
            .replace(/\byou'll\b/g, "you will")
            .replace(/\bhe'll\b/g, "he will")
            .replace(/\bshe'll\b/g, "she will")
            .replace(/\bok\b/g, "okay")
            .replace(/\bo k\b/g, "okay")
            .replace(/\bwanna\b/g, "want")
            .replace(/\bgonna\b/g, "going to")
            .replace(/\bgotta\b/g, "have to")
            .replace(/\bp\.e\.\b/g, "pe")
            .replace(/\bwi fi\b/g, "wifi")
            .replace(/\bwi-fi\b/g, "wifi")
            .replace(/\bt shirt\b/g, "tshirt")
            .replace(/\btee shirt\b/g, "tshirt")
            .replace(/[.,!?;:'"’‘“”]/g, "")
            .replace(/-/g, " ")
            .replace(/\s+/g, " ")
            .trim();
    }

    function wordsOnly(text) {
        return normalizeText(text).split(" ").filter(w => w.length > 0);
    }

    function editDistance(a, b) {
        a = String(a || "");
        b = String(b || "");
        const dp = Array.from({ length: a.length + 1 }, () => Array(b.length + 1).fill(0));

        for (let i = 0; i <= a.length; i++) dp[i][0] = i;
        for (let j = 0; j <= b.length; j++) dp[0][j] = j;

        for (let i = 1; i <= a.length; i++) {
            for (let j = 1; j <= b.length; j++) {
                const cost = a[i - 1] === b[j - 1] ? 0 : 1;
                dp[i][j] = Math.min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + cost
                );
            }
        }
        return dp[a.length][b.length];
    }

    function wordSimilarity(a, b) {
        if (!a || !b) return 0;
        if (a === b) return 1;
        const dist = editDistance(a, b);
        return 1 - (dist / Math.max(a.length, b.length));
    }

    function soundKey(text) {
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
            .replace(/(.)\1+/g, "$1");
    }

    function vowelLooseKey(text) {
        return normalizeText(text)
            .replace(/[^a-z]/g, "")
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
            .replace(/[aeiouy]+/g, "v")
            .replace(/(.)\1+/g, "$1");
    }

    function hasSharedBigram(a, b) {
        a = String(a || "");
        b = String(b || "");
        if (a.length < 2 || b.length < 2) return false;

        for (let i = 0; i < a.length - 1; i++) {
            if (b.includes(a.slice(i, i + 2))) return true;
        }

        return false;
    }

    function aliasMatch(spokenWord, answerWord) {
        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        const aliases = {
            "i": ["i", "eye", "hi", "ai", "a"],
            "am": ["am", "im", "i'm", "em"],
            "have": ["have", "haf", "hub"],
            "a": ["a", "uh", "an"],
            "the": ["the", "da", "d"],
            "my": ["my", "mai"],
            "we": ["we", "wee", "wi"],
            "are": ["are", "r", "our"],
            "was": ["was", "wuz"],
            "will": ["will", "wheel", "well"],
            "is": ["is", "iz", "his"],
            "to": ["to", "too", "two"],
            "in": ["in", "inn"],
            "on": ["on", "an"],
            "at": ["at", "art"],
            "with": ["with", "wid"],
            "because": ["because", "becuz", "cause"],
            "and": ["and", "an", "en"],
            "but": ["but", "bat"],
            "so": ["so", "sew"],
            "it": ["it", "eat"],

            "math": ["math", "mat", "mass", "meth", "matt"],
            "science": ["science", "sience", "signs"],
            "textbook": ["textbook", "text book"],
            "friend": ["friend", "frend", "freind"],
            "schedule": ["schedule", "skedule"],
            "copy": ["copy", "coffee"],
            "underline": ["underline", "under line"],
            "explained": ["explained", "explain", "explane"],
            "discussed": ["discussed", "discuss"],
            "repeat": ["repeat", "repeet"],
            "television": ["television", "tv", "televison"],
            "kitchen": ["kitchen", "kichen"],
            "blanket": ["blanket", "blankit"],
            "early": ["early", "erly"],
            "soap": ["soap", "soup"],
            "shower": ["shower", "shaur"],
            "weekends": ["weekends", "weekend"],
            "weekdays": ["weekdays", "weekday"],
            "homework": ["homework", "home work"],
            "music": ["music", "musick"],
            "hobby": ["hobby", "habi"],
            "photography": ["photography", "fotography"],
            "camping": ["camping", "campin"],
            "soccer": ["soccer", "soker"],
            "basketball": ["basketball", "basket ball"],
            "coach": ["coach", "couch"],
            "rainy": ["rainy", "raining"],
            "umbrella": ["umbrella", "umbreller"],
            "winter": ["winter", "winner"],
            "snowy": ["snowy", "snowing"],
            "forecast": ["forecast", "forcast"],
            "stormy": ["stormy", "storm"],
            "restaurant": ["restaurant", "resturant"],
            "menu": ["menu", "manu"],
            "dish": ["dish", "this"],
            "bill": ["bill", "빌"],
            "receipt": ["receipt", "receit", "reseat"],
            "salad": ["salad", "saled"],
            "dessert": ["dessert", "desert"],
            "expensive": ["expensive", "expencive"],
            "coupon": ["coupon", "cupon"],
            "cashier": ["cashier", "casher"],
            "size": ["size", "sides"],
            "exchange": ["exchange", "ex change"],
            "lost": ["lost", "last"],
            "subway": ["subway", "sub way"],
            "corner": ["corner", "coroner"],
            "right": ["right", "write", "light"],
            "airport": ["airport", "air port"],
            "quickly": ["quickly", "quickli"],
            "reservation": ["reservation", "reserbation"],
            "backpack": ["backpack", "back pack"],
            "museum": ["museum", "museam"],
            "souvenir": ["souvenir", "suvener"],
            "late": ["late", "let"],
            "helped": ["helped", "help"],
            "nervous": ["nervous", "nervus"],
            "proud": ["proud", "prout"],
            "disappointed": ["disappointed", "disapointed"],
            "hopeful": ["hopeful", "hopful"],
            "lonely": ["lonely", "lonli"],
            "message": ["message", "messege"],
            "battery": ["battery", "batery"],
            "password": ["password", "pass word"],
            "news": ["news", "new"],
            "comment": ["comment", "coment"],
            "screen": ["screen", "스크린"],
            "engineer": ["engineer", "enginier"],
            "experience": ["experience", "experiance"],
            "chef": ["chef", "shef"],
            "goal": ["goal", "go"],
            "firefighters": ["firefighters", "fire fighter", "firefighters"],
            "dangerous": ["dangerous", "dangrous"]
        };

        if (!aliases[aw]) return false;
        return aliases[aw].includes(sw);
    }

    function isUnderstandableWord(spokenWord, answerWord) {
        const sw = normalizeText(spokenWord).replace(/\s+/g, "");
        const aw = normalizeText(answerWord).replace(/\s+/g, "");

        if (!sw || !aw) return false;
        if (sw === aw) return true;
        if (aliasMatch(sw, aw)) return true;

        const dist = editDistance(sw, aw);
        const sim = wordSimilarity(sw, aw);

        const soundSw = soundKey(sw);
        const soundAw = soundKey(aw);
        const soundDist = editDistance(soundSw, soundAw);
        const soundSim = wordSimilarity(soundSw, soundAw);

        const vowelSw = vowelLooseKey(sw);
        const vowelAw = vowelLooseKey(aw);
        const vowelSim = wordSimilarity(vowelSw, vowelAw);

        const sameFirst = sw.charAt(0) === aw.charAt(0);
        const sameLast = sw.charAt(sw.length - 1) === aw.charAt(aw.length - 1);
        const sameFirstTwo = sw.slice(0, 2) === aw.slice(0, 2);
        const sameFirstThree = sw.slice(0, 3) === aw.slice(0, 3);
        const sameLastTwo = sw.slice(-2) === aw.slice(-2);

        const soundSameFirst =
            soundSw && soundAw && soundSw.charAt(0) === soundAw.charAt(0);
        const soundSameLast =
            soundSw && soundAw &&
            soundSw.charAt(soundSw.length - 1) === soundAw.charAt(soundAw.length - 1);

        const hasAnyClue =
            sameFirst ||
            sameLast ||
            sameFirstTwo ||
            sameLastTwo ||
            soundSameFirst ||
            soundSameLast ||
            hasSharedBigram(sw, aw) ||
            sim >= 0.28 ||
            soundSim >= 0.20 ||
            vowelSim >= 0.23;

        if (!hasAnyClue) return false;

        // 일부만 인식되거나 붙어서 인식된 경우 허용
        if (aw.length >= 4 && sw.length >= 2 && (aw.includes(sw) || sw.includes(aw))) {
            return true;
        }

        // 자음 뼈대가 같거나 거의 같으면 통과
        if (soundSw && soundAw && soundSw === soundAw) return true;
        if (soundSw && soundAw && soundDist <= 2 && soundSim >= 0.20) return true;

        // 짧은 단어도 너무 엄격하지 않게 처리
        if (aw.length <= 2) {
            return (
                sim >= 0.48 ||
                soundSim >= 0.25 ||
                sameFirst ||
                sameLast ||
                soundSameFirst ||
                soundSameLast
            );
        }

        // 3~4글자 단어: 한 단어 인식 관대하게
        if (aw.length <= 4) {
            return (
                dist <= 2 ||
                sim >= 0.28 ||
                soundSim >= 0.18 ||
                vowelSim >= 0.22 ||
                sameFirst ||
                sameLast ||
                soundSameFirst ||
                soundSameLast ||
                hasSharedBigram(sw, aw)
            );
        }

        // 5~6글자 단어
        if (aw.length <= 6) {
            return (
                dist <= 4 ||
                sim >= 0.30 ||
                soundSim >= 0.20 ||
                vowelSim >= 0.23 ||
                sameFirst ||
                sameFirstTwo ||
                sameLast ||
                sameLastTwo ||
                hasSharedBigram(sw, aw)
            );
        }

        // 긴 단어
        return (
            dist <= 6 ||
            sim >= 0.26 ||
            soundSim >= 0.18 ||
            vowelSim >= 0.20 ||
            sameFirst ||
            sameFirstTwo ||
            sameFirstThree ||
            sameLast ||
            sameLastTwo ||
            hasSharedBigram(sw, aw)
        );
    }

    function getCoreHintWords() {
        if (!currentItem || !currentItem.hint) return [];
        return String(currentItem.hint || "")
            .split("/")
            .map(x => normalizeText(x).trim())
            .filter(x => x.length > 0);
    }

    function removeFillerWords(words) {
        return words.filter(w =>
            !["a", "an", "the", "uh", "um", "please", "yes", "no"].includes(w)
        );
    }

    function isCloseEnough(spoken, answer) {
        const s = normalizeText(spoken);
        const a = normalizeText(answer);

        if (!s || !a) return false;
        if (s === a) return true;

        const spokenWords = wordsOnly(s);
        const answerWords = wordsOnly(a);

        if (spokenWords.length === 0 || answerWords.length === 0) return false;

        // 문장 말하기 활동이므로 빈칸 단어만 말하면 오답입니다.
        // 다만 2문장 전체에서 기능어 몇 개, 관사 몇 개가 빠지는 것은 허용합니다.
        const minWordsNeeded = Math.max(4, Math.ceil(answerWords.length * 0.45));
        if (spokenWords.length < minWordsNeeded) {
            return false;
        }

        // 첫 단어는 문장 시작 골격이므로 비슷해야 함
        if (!isUnderstandableWord(spokenWords[0], answerWords[0])) {
            return false;
        }

        // 모든 빈칸 핵심 정답은 반드시 말해야 함
        const blankAnswers = getCoreHintWords();

        for (const blankAnswer of blankAnswers) {
            const blankWords = wordsOnly(blankAnswer);
            const joinedBlank = blankWords.join("");
            let foundBlank = false;

            if (blankWords.length === 1) {
                const target = blankWords[0];

                for (const sw of spokenWords) {
                    if (isUnderstandableWord(sw, target)) {
                        foundBlank = true;
                        break;
                    }
                }

                if (!foundBlank) {
                    const joinedSpoken = spokenWords.join("");
                    if (isUnderstandableWord(joinedSpoken, target)) {
                        foundBlank = true;
                    }
                }
            } else {
                const joinedSpoken = spokenWords.join("");
                if (isUnderstandableWord(joinedSpoken, joinedBlank)) {
                    foundBlank = true;
                } else {
                    let pos = 0;
                    for (const sw of spokenWords) {
                        const target = blankWords[pos];
                        if (!target) break;
                        if (isUnderstandableWord(sw, target)) pos += 1;
                        if (pos >= blankWords.length) break;
                    }
                    if (pos >= blankWords.length) foundBlank = true;
                }
            }

            if (!foundBlank) {
                return false;
            }
        }

        // 문장 전체 흐름을 순서대로 관대하게 매칭
        let answerPos = 0;
        let matched = 0;

        for (let i = 0; i < spokenWords.length; i++) {
            const sw = spokenWords[i];
            const target = answerWords[answerPos];

            if (!target) break;

            if (isUnderstandableWord(sw, target)) {
                matched += 1;
                answerPos += 1;
                continue;
            }

            // filler는 건너뜀
            if (["a", "an", "the", "uh", "um", "please", "yes", "no"].includes(sw)) {
                continue;
            }

            // 정답 쪽 짧은 기능어 하나가 빠진 경우 허용
            const nextTarget = answerWords[answerPos + 1];
            if (
                target &&
                target.length <= 3 &&
                nextTarget &&
                isUnderstandableWord(sw, nextTarget)
            ) {
                matched += 1;
                answerPos += 2;
                continue;
            }

            // 정답 두 단어가 붙어서 인식된 경우
            if (
                nextTarget &&
                isUnderstandableWord(sw, target + nextTarget)
            ) {
                matched += 2;
                answerPos += 2;
                continue;
            }
        }

        // 긴 2문장이라 완벽한 단어 수를 요구하지 않음
        const requiredMatches = Math.max(4, Math.ceil(answerWords.length * 0.48));
        if (matched >= requiredMatches) return true;

        // 빈칸을 모두 맞히고, 문장 길이와 첫 단어 조건을 만족하면 통과
        // 긴 문장에서 ASR이 중간을 많이 흘려도 학습 목적상 인정
        if (
            blankAnswers.length > 0 &&
            spokenWords.length >= minWordsNeeded &&
            isUnderstandableWord(spokenWords[0], answerWords[0])
        ) {
            return true;
        }

        return false;
    }

    function isCorrectSpeech(spoken, answer) {
        return isCloseEnough(spoken, answer);
    }

    function escapeHtml(text) {
        return String(text || "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function makeTwoLetterHint(answerWord) {
        if (!answerWord) return "";

        return String(answerWord).split("/").map(part => {
            return part.trim().split(" ").map(word => {
                const clean = word.trim();
                if (clean.length <= 2) return clean;
                return clean.slice(0, 2) + "_".repeat(Math.min(clean.length - 2, 6));
            }).join(" ");
        }).join(" / ");
    }

    function makeBlankSentenceHtml(blankText) {
        const parts = String(blankText || "").split(/(______)/g);

        return parts.map(part => {
            if (part === "______") {
                return "<span style='display:inline-block; min-width:120px; height:42px; vertical-align:middle; background:#e0f2fe; border-radius:14px; margin:0 6px; border:1.5px solid #bae6fd;'></span>";
            }

            return escapeHtml(part);
        }).join("");
    }

    function makeFilledBlankSentenceHtml(blankText, hintText) {
        const answers = String(hintText || "")
            .split("/")
            .map(x => x.trim())
            .filter(x => x.length > 0);

        let blankIndex = 0;
        const parts = String(blankText || "").split(/(______)/g);

        return parts.map(part => {
            if (part === "______") {
                const fill = answers[blankIndex] || "";
                blankIndex += 1;

                return "<span style='display:inline-block; min-width:96px; vertical-align:middle; background:#dcfce7; color:#166534; border-radius:14px; margin:0 6px; padding:4px 12px; border:1.5px solid #86efac; font-weight:900; box-shadow:0 3px 8px rgba(34,197,94,0.10);'>"
                    + escapeHtml(fill) +
                    "</span>";
            }

            return escapeHtml(part);
        }).join("");
    }

    function updateScore() {
        scoreLabel.innerText = "정답 " + score + "개";
    }

    function resetMicState() {
        isListening = false;
        if (recognitionTimeout) {
            clearTimeout(recognitionTimeout);
            recognitionTimeout = null;
        }
        if (speechCheckTimeout) {
            clearTimeout(speechCheckTimeout);
            speechCheckTimeout = null;
        }
        micBtn.disabled = false;
        micBtn.style.opacity = "1";
        micBtn.style.pointerEvents = "auto";
        micBtn.innerText = "🎙️";
    }

    function stopRecognition() {
        if (recognitionTimeout) {
            clearTimeout(recognitionTimeout);
            recognitionTimeout = null;
        }
        if (recognition) {
            try { recognition.onresult = null; } catch (e) {}
            try { recognition.onerror = null; } catch (e) {}
            try { recognition.onend = null; } catch (e) {}
            try { recognition.stop(); } catch (e) {}
            try { recognition.abort(); } catch (e) {}
            recognition = null;
        }
        resetMicState();
    }

    function speak(text) {
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        utterance.rate = 0.82;
        utterance.pitch = 1.05;

        const voices = window.speechSynthesis.getVoices();
        const preferred = voices.find(v =>
            v.lang && v.lang.toLowerCase().startsWith("en") &&
            /(samantha|jenny|aria|zira|google us english|karen|victoria|female)/i.test(v.name)
        );
        if (preferred) utterance.voice = preferred;

        window.speechSynthesis.speak(utterance);
    }

    function loadQuestion(index = 0) {
        if (currentList.length === 0) {
            currentList = getFilteredItems();
        }

        if (index >= currentList.length) index = 0;
        if (index < 0) index = currentList.length - 1;

        currentIndex = index;
        currentItem = currentList[currentIndex];
        alreadyCorrect = false;

        categoryLabel.innerText = "문장 " + categorySelect.value + " · " + (currentIndex + 1) + " / " + currentList.length;
        const emoji = currentItem.emoji || "🎙️";
        koPrompt.innerHTML =
            "<span style='font-size:42px; margin-right:10px; vertical-align:middle;'>" + emoji + "</span>" +
            "<span style='vertical-align:middle;'>" + currentItem.ko + "</span>";

        blankSentence.innerHTML = makeBlankSentenceHtml(currentItem.blank);
        hintBox.style.display = "none";
        if (typeof answerBox !== "undefined" && answerBox) answerBox.style.display = "none";
        hintBox.innerText = "";
        if (typeof answerBox !== "undefined" && answerBox) answerBox.innerText = "";
        transcriptBox.innerText = "";
        finalSpeechBuffer = "";
        lastCheckedSpeech = "";
        isCheckingSpeech = false;

        resetMicState();
        hintBtn.style.display = "inline-block";
        micBtn.style.display = "inline-block";
        answerBtn.style.display = "inline-block";
        listenBtn.style.display = "none";
        nextBtn.style.display = "inline-block";

        resultBox.style.display = "none";
        resultBox.innerText = "";
        updateScore();
    }

    function goNextQuestion() {
        stopRecognition();
        window.speechSynthesis.cancel();
        loadQuestion(currentIndex + 1);
    }

    function checkSpeech(spokenText) {
        if (!currentItem) return;

        const recognized = String(spokenText || "").trim();
        const recognizedKey = normalizeText(recognized);
        if (!recognizedKey) return;

        // 같은 결과가 아주 짧은 시간 안에 중복으로 들어오는 경우만 막습니다.
        // 학생이 다시 말했을 때는 같은 문장도 다시 채점될 수 있어야 합니다.
        const now = Date.now();
        if (recognizedKey === lastCheckedSpeech && now - lastCheckAt < 1200) return;
        lastCheckedSpeech = recognizedKey;
        lastCheckAt = now;
        isCheckingSpeech = false;

        if (isCorrectSpeech(recognized, currentItem.answer)) {
            if (!alreadyCorrect) {
                score += 1;
                alreadyCorrect = true;
            }

            updateScore();

            transcriptBox.innerHTML =
                "<span style='color:#4c1d95;'>" + escapeHtml(recognized || currentItem.answer) + "</span> " +
                "<span style='color:#166534;'>✅ 정답입니다</span>";

            blankSentence.innerHTML = makeFilledBlankSentenceHtml(currentItem.blank, currentItem.hint);

            hintBox.style.display = "none";
            answerBtn.style.display = "none";
            listenBtn.style.display = "inline-block";
            nextBtn.style.display = "inline-block";

            resultBox.style.display = "none";
            resultBox.innerText = "";

            speak(currentItem.answer);
        } else {
            transcriptBox.innerHTML =
                "<span style='color:#92400e;'>" + escapeHtml(recognized || "조금 더 크게 말해 보세요") + "</span> " +
                "<span style='color:#92400e;'>💬 다시 한 번 말해 보세요</span>";

            hintBox.style.display = "block";
            hintBox.innerText = "힌트: " + makeTwoLetterHint(currentItem.hint);

            answerBtn.style.display = "inline-block";
            listenBtn.style.display = "none";
            nextBtn.style.display = "inline-block";

            resultBox.style.display = "block";
            resultBox.style.color = "#92400e";
            resultBox.innerText = "문장은 말해야 합니다. 다만 발음 시험은 아니므로, 문장 흐름과 빈칸 핵심 단어가 맞으면 관대하게 정답으로 인정됩니다.";
        }
        isCheckingSpeech = false;
    }

    async function startRecognition() {
        // 듣는 중에 다시 누르면 현재 인식을 정리하고 새로 시작합니다.
        if (isListening) {
            stopRecognition();
            setTimeout(function() {
                startRecognition();
            }, 160);
            return;
        }

        if (!SpeechRecognition) {
            transcriptBox.innerText = "Chrome에서 열어 주세요.";
            return;
        }

        if (!currentItem || alreadyCorrect) return;

        stopRecognition();

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                stream.getTracks().forEach(track => track.stop());
            } catch (err) {
                transcriptBox.innerText = "마이크 허용 후 다시 눌러 주세요.";
                resetMicState();
                return;
            }
        }

        window.speechSynthesis.cancel();

        try {
            recognition = new SpeechRecognition();
            recognition.lang = "en-US";
            recognition.interimResults = true;
            recognition.continuous = true;
            recognition.maxAlternatives = 8;

            isListening = true;
            hasSubmittedSpeech = false;
            micBtn.disabled = false;
            micBtn.style.opacity = "0.9";
            micBtn.style.pointerEvents = "auto";
            micBtn.innerText = "👂";
            resultBox.style.display = "none";
            resultBox.innerText = "";
            transcriptBox.innerText = "듣는 중입니다. 한 문장씩 천천히 말해 보세요.";
            finalSpeechBuffer = "";
            lastCheckedSpeech = "";
            lastCheckAt = 0;
            isCheckingSpeech = false;

            const finalSegments = {};
            let liveInterimText = "";

            function cleanDuplicateWords(text) {
                const words = normalizeText(text).split(" ").filter(Boolean);
                if (words.length < 4) return String(text || "").trim();

                // 같은 문장이 두 번 붙는 경우를 줄입니다.
                const half = Math.floor(words.length / 2);
                const first = words.slice(0, half).join(" ");
                const second = words.slice(half, half * 2).join(" ");
                if (first && first === second) {
                    return words.slice(0, half).join(" ");
                }

                return String(text || "").replace(/\s+/g, " ").trim();
            }

            function getFinalText() {
                const keys = Object.keys(finalSegments).map(Number).sort((a, b) => a - b);
                const joined = keys.map(k => finalSegments[k]).filter(Boolean).join(" ");
                return cleanDuplicateWords(joined || finalSpeechBuffer || transcriptBox.innerText || "");
            }

            function pickBestTranscript(result) {
                let piece = result[0].transcript.trim();
                for (let j = 0; j < result.length; j++) {
                    const alt = result[j].transcript.trim();
                    if (isCorrectSpeech(alt, currentItem.answer)) {
                        piece = alt;
                        break;
                    }
                }
                return piece;
            }

            function finishAndCheck(textToCheck) {
                const finalText = cleanDuplicateWords(textToCheck || getFinalText());

                if (hasSubmittedSpeech) return;
                hasSubmittedSpeech = true;

                if (recognitionTimeout) {
                    clearTimeout(recognitionTimeout);
                    recognitionTimeout = null;
                }
                if (speechCheckTimeout) {
                    clearTimeout(speechCheckTimeout);
                    speechCheckTimeout = null;
                }

                if (recognition) {
                    try { recognition.onresult = null; } catch (e) {}
                    try { recognition.onerror = null; } catch (e) {}
                    try { recognition.onend = null; } catch (e) {}
                    try { recognition.stop(); } catch (e) {}
                    try { recognition.abort(); } catch (e) {}
                    recognition = null;
                }

                resetMicState();

                if (finalText.trim() && finalText !== "듣는 중입니다 한 문장씩 천천히 말해 보세요") {
                    checkSpeech(finalText);
                } else {
                    transcriptBox.innerText = "소리가 잘 들어오지 않았습니다. 마이크를 조금 가까이 두고 다시 눌러 말해 보세요.";
                    resultBox.style.display = "none";
                }
            }

            function scheduleFinalCheck() {
                if (speechCheckTimeout) {
                    clearTimeout(speechCheckTimeout);
                    speechCheckTimeout = null;
                }

                // 긴 문장 2개를 말할 수 있도록 마지막 최종 인식 뒤 3초 기다립니다.
                speechCheckTimeout = setTimeout(function() {
                    finishAndCheck(getFinalText());
                }, 3000);
            }

            recognitionTimeout = setTimeout(function() {
                if (isListening) {
                    finishAndCheck(getFinalText() || liveInterimText || "");
                }
            }, 16000);

            recognition.onresult = function(event) {
                let interimText = "";
                let hasFinal = false;

                // event.resultIndex부터 새로 들어온 결과만 처리해서 중복 인식을 막습니다.
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const piece = pickBestTranscript(event.results[i]);
                    if (!piece) continue;

                    if (event.results[i].isFinal) {
                        finalSegments[i] = piece;
                        hasFinal = true;
                    } else {
                        interimText += (interimText ? " " : "") + piece;
                    }
                }

                finalSpeechBuffer = getFinalText();
                liveInterimText = cleanDuplicateWords((finalSpeechBuffer ? finalSpeechBuffer + " " : "") + interimText);

                const displayText = (liveInterimText || finalSpeechBuffer || "").trim();
                if (displayText) {
                    transcriptBox.innerText = displayText;
                }

                if (hasFinal) {
                    scheduleFinalCheck();
                }
            };

            recognition.onerror = function(event) {
                if (event.error === "not-allowed" || event.error === "service-not-allowed") {
                    finishAndCheck("");
                    transcriptBox.innerText = "마이크 허용 후 다시 눌러 주세요.";
                    return;
                }

                // no-speech는 실제 수업에서 자주 뜨므로 오류로 크게 띄우지 않습니다.
                if (event.error === "no-speech" || event.error === "audio-capture" || event.error === "network") {
                    finishAndCheck(getFinalText() || liveInterimText || "");
                    return;
                }

                finishAndCheck(getFinalText() || liveInterimText || "");
            };

            recognition.onend = function() {
                if (!hasSubmittedSpeech && (getFinalText() || liveInterimText || "").trim()) {
                    scheduleFinalCheck();
                } else if (!hasSubmittedSpeech) {
                    resetMicState();
                }
            };

            recognition.start();
        } catch (err) {
            stopRecognition();
            transcriptBox.innerText = "다시 눌러 주세요.";
        }
    }

    categorySelect.addEventListener("change", function() {
        stopRecognition();
        currentList = getFilteredItems();
        currentIndex = 0;
        loadQuestion(0);
    });

    randomBtn.addEventListener("click", function() {
        stopRecognition();
        currentList = shuffleArray(getFilteredItems());
        loadQuestion(0);
    });

    resetBtn.addEventListener("click", function() {
        stopRecognition();
        score = 0;
        alreadyCorrect = false;
        updateScore();
        resultBox.style.display = "none";
        resultBox.innerText = "";
        loadQuestion(0);
    });

    hintBtn.addEventListener("click", function() {
        hintBox.style.display = "block";
        hintBox.innerText = makeTwoLetterHint(currentItem.hint);
    });

    listenBtn.addEventListener("click", function() {
        speak(currentItem.answer);
    });

    answerBtn.addEventListener("click", function() {
        if (!currentItem) return;
        if (typeof answerBox !== "undefined" && answerBox) answerBox.style.display = "none";
        blankSentence.innerHTML = makeFilledBlankSentenceHtml(currentItem.blank, currentItem.hint);
        transcriptBox.innerHTML = "<span style='color:#166534;'>" + escapeHtml(currentItem.answer) + "</span>";
        listenBtn.style.display = "none";
        nextBtn.style.display = "inline-block";
        speak(currentItem.answer);

        resultBox.style.display = "block";
        resultBox.style.color = "#166534";
        resultBox.innerText = "정답을 보고 들은 뒤, 다시 말하면 정답으로 인정됩니다.";
    });

    micBtn.addEventListener("click", startRecognition);

    nextBtn.addEventListener("click", function() {
        goNextQuestion();
    });

    initCategories();
    currentList = getFilteredItems();
    updateScore();
    loadQuestion(0);
    </script>
    """

    html = html.replace("__ITEMS_JSON__", items_json)
    components.html(html, height=880, scrolling=True)


speaking_practice_component(PRACTICE_ITEMS)
