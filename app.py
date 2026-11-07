
import streamlit as st
import random
import re

# =================================
# 1. 페이지 설정
# =================================

st.set_page_config(
    page_title="마음 쉼터",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 마음 쉼터 대화방")
st.write("편안하게 마음속 이야기를 나눠 보세요.")

# =================================
# 2. 세션 기록
# =================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "topics" not in st.session_state:
    st.session_state.topics = []

# =================================
# 3. 감정 분석
# =================================

emotions = {
    "기쁨": ["기뻐", "행복", "즐거워", "신나", "좋아"],
    "슬픔": ["슬퍼", "속상해", "울고 싶어", "우울", "외로워"],
    "걱정": ["걱정", "불안", "무서워", "두려워", "막막해"],
    "화남": ["화나", "짜증", "억울", "열받아"],
    "피곤": ["피곤", "지쳐", "힘들어", "졸려"]
}

def detect_emotion(text):
    for emotion, keywords in emotions.items():
        if any(word in text for word in keywords):
            return emotion
    return "일반"

# =================================
# 4. 위험 표현 확인
# =================================

def check_safety(text):
    keywords = [
        "죽고 싶",
        "살기 싫",
        "자해",
        "사라지고 싶",
        "스스로를 해치"
    ]

    return any(word in text for word in keywords)

# =================================
# 5. 대화 답변 생성
# =================================

def make_response(text):

    if check_safety(text):
        return (
            "이야기해 줘서 고마워.\n\n"
            "지금은 혼자 감당하지 않았으면 좋겠어. "
            "부모님이나 선생님처럼 믿을 수 있는 어른에게 "
            "지금 마음을 꼭 알려줘.\n\n"
            "당장 위험하다면 112 또는 119에 도움을 요청해 줘. "
            "한국 자살예방상담전화 109에서도 상담받을 수 있어."
        )

    emotion = detect_emotion(text)

    responses = {
        "기쁨": [
            "우와, 기쁜 일이 있었구나! 어떤 일이었는지 더 들려줄래?",
            "좋은 일이 생겼다니 반가워! 가장 좋았던 순간은 언제였어?",
            "그 기분을 함께 나눠줘서 고마워. 더 이야기해 줄래?"
        ],

        "슬픔": [
            "마음이 많이 속상했겠구나. 무슨 일이 있었는지 이야기해 줄래?",
            "그런 일이 있었다니 마음이 무겁겠다. 내가 이야기를 들어줄게.",
            "속상한 마음을 말해 줘서 고마워. 어떤 일이 가장 힘들었어?"
        ],

        "걱정": [
            "무엇이 가장 걱정되는지 천천히 이야기해 줄래?",
            "걱정이 많으면 마음이 복잡해질 수 있어. 하나씩 살펴보자.",
            "그 일이 신경 쓰이는구나. 어떤 부분이 가장 불안해?"
        ],

        "화남": [
            "정말 화가 날 만한 일이 있었나 봐. 무슨 일이었어?",
            "억울한 마음이 들었구나. 네 이야기를 들어볼게.",
            "짜증이 많이 났겠다. 어떤 상황이었는지 알려줄래?"
        ],

        "피곤": [
            "오늘 많이 지쳤구나. 잠깐 쉬어 가도 괜찮아.",
            "몸과 마음이 모두 피곤할 수 있지. 오늘 무슨 일이 있었어?",
            "조금 쉬면서 천천히 이야기해도 괜찮아."
        ],

        "일반": [
            "그렇구나! 조금 더 이야기해 줄래?",
            "그 이야기에 대해 더 알고 싶어. 어떤 일이 있었어?",
            "이야기해 줘서 고마워. 네 생각은 어때?",
            "그다음에는 어떻게 됐어?",
            "가장 기억에 남는 부분은 무엇이야?"
        ]
    }

    answer = random.choice(responses[emotion])

    # 이전 대화에서 언급한 주제 참고
    if len(st.session_state.messages) >= 2:
        answer += "\n\n아까 이야기했던 내용도 더 들려줘도 좋아."

    return answer

# =================================
# 6. 대화 기록 출력
# =================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =================================
# 7. 사이드바
# =================================

with st.sidebar:
    st.header("⚙️ 설정")

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.session_state.topics = []
        st.rerun()

    st.caption("🌿 마음 쉼터")
    st.caption("API 없이 작동하는 대화 프로그램")

# =================================
# 8. 사용자 입력
# =================================

prompt = st.chat_input("오늘 어떤 마음이 드시나요?")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("이야기를 생각하고 있어요..."):
            response_text = make_response(prompt)

        st.markdown(response_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })

# =================================
# 9. 호흡 쉼터
# =================================

with st.expander("🧘 잠깐 쉬어 가기"):
    st.write("1. 편안한 자세로 앉아 보세요.")
    st.write("2. 천천히 숨을 들이쉬세요.")
    st.write("3. 천천히 숨을 내쉬세요.")
    st.write("4. 편안한 속도로 반복해 보세요.")

st.divider()

st.caption(
    "🌿 이 프로그램은 전문 상담을 대신하지 않는 "
    "간단한 대화 도우미입니다."
)
