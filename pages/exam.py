import streamlit as st
from pathlib import Path
from gtts import gTTS
import io
import base64
import random
import json
import re
import uuid
from urllib.parse import quote
import streamlit.components.v1 as components

1.  weekly plan : 주간 계획표
2. there are no breaks : 계획표에 쉬는 시간이 없다
3. Let me take a look: 내가 한 번 살펴볼게
4. you will get tired and give up: 너는 피곤해지고 포기하게 될 것이다
5. I will do my best: 최선을 다할 것이다
6. You are not an early bird: 너는 아침형 인간이 아니다
7. You need to make a realistic plan: 너는 현실적인 계획을 세워야 한다
8. That makes sense: 네 말이 일리가 있다
9. I will delete the morning jog and concentrate on the afternoon workout : 나는 아침 조깅을 없애고 오후 근력 운동에 집중하겠다
10. quality is more important than quantity: 양보다 질이 중요하다
11. I am out of time: 나는 이미 늦어버렸다
12. you begged me with the drowning eyes to stay: 너는 간절한 눈빛으로 나에게 머물러 달라고 말했다.
13. say goodbye: 작별인사하다
14. survive 살아남다
15. follow 따라가다
16. last 마지막
17. tomorrow 내일
18. I am going to love you every night like it is the last night: 오늘밤이 마지막 인 것처럼 오늘 밤 너를 사랑하겠다
19. if the world was ending 세상이 끝난다면
20. if the party was over and our time on earth was through : 파티가 끝나고 지구에서의 우리의 시간이 끝난다면