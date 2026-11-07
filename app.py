import streamlit as st
import time



# =====================================
# 1. 페이지 기본 설정
# =====================================

st.set_page_config(
    page_title="마음 쉼터",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 마음 쉼터 대화방")

st.write(
    "편안하게 마음속 이야기를 나누고 "
    "잠시 숨을 고를 수 있는 공간입니다."
)

st.caption("🤖 이 대화방은 AI가 답변하는 공간입니다.")

# =====================================
# 2. API 설정
# =====================================

try:
    API_KEY = st.secrets.get("OPENAI_API_KEY", "")
    MODEL = st.secrets.get("OPENAI_MODEL", "gpt-5.5")
except Exception:
    API_KEY = ""
    MODEL = "gpt-5.5"

API_KEY = API_KEY or os.getenv("OPENAI_API_KEY", "")

# =====================================
# 3. AI 기본 설정
# =====================================

SYSTEM_PROMPT = """
너는 '마음 쉼터'라는 이름의 친절하고 따뜻한 AI 대화 도우미야.

[대화 원칙]

1. 사용자의 이야기를 주의 깊게 들어줘.
2. 자연스럽고 따뜻한 한국어를 사용해.
3. 기계적으로 같은 문장을 반복하지 마.
4. 사용자가 말한 내용을 기억하고 이어서 대화해.
5. 사용자의 감정을 함부로 판단하지 마.
6. 무조건 긍정적인 말만 하지 말고 진심으로 공감해.
7. 한 번에 너무 많은 질문을 하지 마.
8. 초등학생도 이해할 수 있는 쉬운 표현을 사용해.
9. AI라는 사실을 숨기거나 사람인 척하지 마.
10. 의료진이나 전문 상담사라고 주장하지 마.
11. 의학적 진단이나 치료를 대신하지 마.

[안전 원칙]

1. 사용자가 위험하거나 매우 힘든 상황이라면
   믿을 수 있는 어른에게 도움을 요청하도록 안내해.
2. 자신을 해치거나 생명을 위협하는 행동에 관한
   구체적인 방법이나 설명은 제공하지 마.
3. 긴급한 위험이 있다면 112 또는 119에 도움을
   요청하도록 안내해.
4. 한국의 자살예방상담전화 109도 안내할 수 있어.
5. 사용자를 비난하거나 부끄럽게 만들지 마.
6. AI와의 대화만으로 모든 문제를 해결할 수 있다고
   말하지 마.

[답변 스타일]

- 자연스러운 대화체
- 적당한 길이
- 필요할 때만 이모지 사용
- 사용자의 말에 맞는 질문
- 따뜻하고 편안한 분위기
"""

# =====================================
# 4. API 클라이언트
# =====================================

@st.cache_resource
def get_client(api_key):
    return OpenAI(api_key=api_key)


# =====================================
# 5. 대화 기록 초기화
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0


# =====================================
# 6. 대화 초기화 버튼
# =====================================

with st.sidebar:
    st.title("⚙️ 설정")

    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.rerun()

    st.divider()

    st.write("🌿 마음 쉼터")
    st.write("AI 대화 도우미")

    st.caption("대화 내용은 현재 세션에 보관됩니다.")


# =====================================
# 7. 이전 대화 출력
# =====================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =====================================
# 8. 위험 표현 확인
# =====================================

CRISIS_KEYWORDS = [
    "죽고 싶",
    "살기 싫",
    "사라지고 싶",
    "없어지고 싶",
    "자해",
    "스스로를 해치",
    "목숨을 끊",
    "죽이고 싶"
]


def check_crisis(text):
    text = text.replace(" ", "").lower()

    return any(
        keyword.replace(" ", "") in text
        for keyword in CRISIS_KEYWORDS
    )


# =====================================
# 9. 안전 안내
# =====================================

def safety_response():

    return """
많이 힘든 마음을 이야기해 줘서 고마워.

이런 마음을 혼자 감당하지 않았으면 좋겠어.

지금은 믿을 수 있는 부모님, 선생님 또는
가까운 어른에게 네 마음을 꼭 알려줘.

당장 위험한 상황이라면 혼자 있지 말고
112 또는 119에 도움을 요청해 줘.

한국에서는 자살예방상담전화 109에서도
도움을 받을 수 있어.

너의 이야기는 중요하고,
도움을 요청해도 괜찮아.
"""


# =====================================
# 10. 실제 AI 답변 생성
# =====================================

def generate_ai_response(user_text):

    if not API_KEY:
        return (
            "아직 AI API 키가 설정되지 않았어. 🌿\n\n"
            ".streamlit/secrets.toml 파일에 "
            "OPENAI_API_KEY를 설정해 줘."
        )

    client = get_client(API_KEY)

    # 최근 대화 12개를 문맥으로 전달
    history = [
        {
            "role": msg["role"],
            "content": msg["content"]
        }
        for msg in st.session_state.messages[-12:]
    ]

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=history,
        max_output_tokens=500,
        store=False
    )

    answer = response.output_text

    if not answer:
        return "미안해. 답변을 만드는 데 문제가 생겼어. 다시 이야기해 줄래?"

    return answer


# =====================================
# 11. 심호흡 쉼터
# =====================================

with st.expander("🧘 잠깐 쉬어 가기"):

    st.markdown("### 천천히 호흡하기")

    st.write("1. 편안한 자세로 앉아 봐.")
    st.write("2. 천천히 숨을 들이쉬어 봐.")
    st.write("3. 천천히 숨을 내쉬어 봐.")
    st.write("4. 편안해질 때까지 반복해 봐.")

    st.info("무리하지 말고 자연스럽게 호흡해 줘.")


# =====================================
# 12. 사용자 메시지 입력
# =====================================

prompt = st.chat_input(
    "오늘 어떤 마음이 드시나요? 편하게 적어주세요."
)

if prompt:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    st.session_state.chat_count += 1

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 답변 출력
    with st.chat_message("assistant"):

        with st.spinner("🌿 이야기를 듣고 있어요..."):

            try:

                # 위험 표현이 감지되면 안전 안내 우선
                if check_crisis(prompt):
                    response_text = safety_response()

                else:
                    response_text = generate_ai_response(prompt)

                st.markdown(response_text)

            except Exception:

                response_text = (
                    "미안해. 지금 AI 연결에 문제가 생겼어.\n\n"
                    "잠시 후 다시 시도해 줘. 🌿"
                )

                st.error("AI 연결 오류가 발생했습니다.")
                st.markdown(response_text)

    # AI 답변 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })


# =====================================
# 13. 하단 안내
# =====================================

st.divider()

st.caption(
    "🌿 마음 쉼터는 AI 대화 도우미입니다. "
    "전문적인 상담이나 긴급한 도움을 대신하지 않습니다."
)



# 1. 페이지 기본 설정
st.set_page_config(
    page_title="마음 쉼터",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 마음 쉼터 대화방")
st.write("편안하게 마음속 이야기를 나누고 잠시 숨을 고를 수 있는 공간입니다.")
st.write("편안하게 마음속 이야기를 나누고 잠시 숨을 고를 수 있는 공간입니다.")

# 2. 세션 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. 이전 대화 화면에 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. 사용자 입력 받기
if prompt := st.chat_input("오늘 어떤 마음이 드시나요? 편하게 적어주세요."):
    # 사용자 메시지 기록 및 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. 어시스턴트 응답 생성
    with st.chat_message("assistant"):
        # 지친 마음이나 위기가 감지되는 키워드 목록
        soothe_keywords = ["힘들다", "지친다", "막막해", "속상해", "불안해", "답답해", "울고 싶어", "죽고 싶다", "살기 싫다"]
        needs_soothing = any(kw in prompt for kw in soothe_keywords)
        
        if needs_soothing:
            # (1) 깊은 공감과 위로 메시지
            response_text = (
                "마음이 참 무겁고 지치셨겠어요. 그동안 그 무거운 마음을 혼자 견뎌내느라 애썼다는 말씀 꼭 드리고 싶어요.\n\n"
                "지금 이 순간만큼은 아무 걱정 말고, 잠시 숨을 깊게 고르며 마음을 내려놓아 보세요."
            )
            st.markdown(response_text)
            
            # (2) 마음을 진정시키는 인터랙티브 쉼터 (심호흡 가이드)
            st.markdown("---")
            st.markdown("### 🧘 잠시 숨을 고르는 1분 쉼터")
            st.write("화면을 보며 천천히 호흡을 따라 해 보세요.")
            
            if st.button("🫁 심호흡 시작하기 (들숨 4초 / 날숨 4초)"):
                with st.spinner("숨을 천천히 들이쉬고... 내쉬어 보세요..."):
                    time.sleep(2)
                st.success("참 잘하셨어요. 어깨와 목의 긴장을 살짝 풀어보세요.")
            
            # (3) 부담 없는 전문 상담 안내 (원터치 버튼)
            st.markdown("---")
            st.markdown(
                """
                <div style="background-color: #f7f9fa; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e1e4e8;">
                    <p style="margin-bottom: 10px; font-size: 14px; color: #555;">마음속 이야기를 더 깊게 털어놓고 싶다면, 언제든 열려 있는 따뜻한 손길을 만나보세요.</p>
                    <a href="tel:109" target="_self" style="text-decoration: none;">
                        <button style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 5px; font-weight: bold; cursor: pointer;">
                            📞 자살예방 상담전화 (109) 연결하기
                        </button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # 일반적인 대화 응답
            response_text = "그렇군요. 이야기해 주셔서 고마워요. 어떤 생각들이 스쳐 지나가는지 조금 더 들려주시겠어요?"
            st.markdown(response_text)
            
        # 대화 기록 저장
        st.session_state.messages.append({"role": "assistant", "content": response_text})
