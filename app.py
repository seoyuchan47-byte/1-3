import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 웹앱 제목 설정
st.title("📊 나만의 심플 데이터 대시보드")
st.write("오류 없이 작동하는 가장 간단한 스트림릿 앱입니다.")

# 웹앱 구분을 위한 구분선
st.markdown("---")

# 2. 사이드바 레이아웃 추가
st.sidebar.header("⚙️ 설정 변경")
user_name = st.sidebar.text_input("당신의 이름을 입력하세요", "홍길동")
sample_count = st.sidebar.slider("생성할 데이터 개수", min_value=10, max_value=100, value=50)

# 사이드바 입력값에 따른 환영 인사
st.subheader(f"👋 반갑습니다, {user_name}님!")

# 3. 간단한 샘플 데이터프레임 생성
# 데이터 개수를 슬라이더 값(sample_count)과 연동하여 동적으로 변하게 만듭니다.
data = {
    "점수": [i * 1.5 for i in range(sample_count)],
    "만족도": [i % 5 + 1 for i in range(sample_count)]
}
df = pd.DataFrame(data)

# 4. 데이터 및 차트 시각화
col1, col2 = st.columns(2)

with col1:
    st.write("### 📄 데이터 표")
    # 데이터프레임을 깔끔하게 보여줍니다.
    st.dataframe(df, use_container_width=True)

with col2:
    st.write("### 📈 데이터 차트")
    # matplotlib를 활용한 간단한 선 그래프
    fig, ax = plt.subplots()
    ax.plot(df["점수"], label="Score", color="dodgerblue")
    ax.set_title("Score Trend")
    ax.legend()
    
    # 스트림릿에 matplotlib 차트 전달
    st.pyplot(fig)

st.markdown("---")
st.success("🎉 앱이 성공적으로 실행되었습니다!")
