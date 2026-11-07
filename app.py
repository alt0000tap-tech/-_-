import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_title("마음 쉼터")
import streamlit as st
import time

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
