import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="고민상담 챗봇",
    page_icon="💬",
)

st.title("💬 고민상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 상담 챗봇")

# API 키 불러오기
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("Secrets에 GOOGLE_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 오류: {e}")
    st.stop()

# 시스템 프롬프트
SYSTEM_PROMPT = """
너는 공감 능력이 뛰어난 고민상담 챗봇이다.

규칙:
- 사용자의 감정을 공감해라.
- 너무 딱딱하지 않게 대화해라.
- 해결책을 강요하지 마라.
- 위험하거나 극단적인 선택은 권장하지 마라.
- 간결하지만 따뜻하게 답변해라.
- 한국어로 답변해라.
"""

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("고민을 편하게 이야기해보세요")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Gemini용 대화 변환
            contents = []

            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"

                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg["content"])]
                    )
                )

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.8,
                    max_output_tokens=500,
                )
            )

            ai_response = response.text

            # 응답 출력
            message_placeholder.markdown(ai_response)

            # 채팅 기록 저장
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )

        except Exception as e:
            error_message = f"오류가 발생했습니다: {e}"
            message_placeholder.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "죄송해요. 잠시 후 다시 시도해주세요."
                }
            )
