import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Eco Reward",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Eco Reward")
st.subheader("쓰레기를 올바르게 버리고 포인트를 받아보세요!")

# 세션 상태 초기화
if "records" not in st.session_state:
    st.session_state.records = []

if "total_points" not in st.session_state:
    st.session_state.total_points = 0

# 포인트 정책
POINTS = {
    "플라스틱": 10,
    "종이": 8,
    "캔": 12,
    "유리": 15,
    "음식물쓰레기": 5,
    "일반쓰레기": 1
}


def get_rank(points):
    if points >= 1000:
        return "🌍 지구 수호자"
    elif points >= 500:
        return "🏆 환경 챔피언"
    elif points >= 100:
        return "🌱 새싹 환경지킴이"
    else:
        return "🙂 입문자"


# 사이드바
with st.sidebar:
    st.header("📊 나의 현황")

    rank = get_rank(st.session_state.total_points)

    st.metric(
        "총 포인트",
        f"{st.session_state.total_points:,}"
    )

    st.write(f"현재 등급: **{rank}**")

# 입력 영역
st.header("🗑️ 쓰레기 배출 등록")

with st.form("recycle_form"):

    waste_type = st.selectbox(
        "쓰레기 종류",
        list(POINTS.keys())
    )

    quantity = st.number_input(
        "수량",
        min_value=1,
        value=1,
        step=1
    )

    submitted = st.form_submit_button("포인트 받기")

    if submitted:
        try:
            earned = POINTS[waste_type] * quantity

            record = {
                "날짜": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "종류": waste_type,
                "수량": quantity,
                "획득포인트": earned
            }

            st.session_state.records.append(record)
            st.session_state.total_points += earned

            st.success(
                f"{earned} 포인트 획득! 🎉"
            )

        except Exception as e:
            st.error(f"오류 발생: {e}")

# 기록 데이터프레임
df = pd.DataFrame(st.session_state.records)

# 통계
st.header("📈 통계")

col1, col2, col3 = st.columns(3)

total_count = len(df)

if not df.empty:
    total_quantity = int(df["수량"].sum())
else:
    total_quantity = 0

with col1:
    st.metric(
        "총 배출 횟수",
        total_count
    )

with col2:
    st.metric(
        "총 배출 수량",
        total_quantity
    )

with col3:
    st.metric(
        "누적 포인트",
        st.session_state.total_points
    )

# 기록 조회
st.header("📋 배출 기록")

if not df.empty:
    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="⬇️ CSV 다운로드",
        data=csv,
        file_name="eco_reward_records.csv",
        mime="text/csv"
    )

else:
    st.info("아직 등록된 기록이 없습니다.")

# 포인트 정책
st.header("💰 포인트 정책")

policy_df = pd.DataFrame(
    {
        "종류": list(POINTS.keys()),
        "포인트": list(POINTS.values())
    }
)

st.table(policy_df)

# 랭크 안내
st.header("🏅 랭크 안내")

rank_df = pd.DataFrame(
    {
        "등급": [
            "🙂 입문자",
            "🌱 새싹 환경지킴이",
            "🏆 환경 챔피언",
            "🌍 지구 수호자"
        ],
        "조건": [
            "0점 이상",
            "100점 이상",
            "500점 이상",
            "1000점 이상"
        ]
    }
)

st.table(rank_df)

st.markdown("---")
st.caption("Eco Reward MVP")
