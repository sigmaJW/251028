import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------
# 1. 데이터 로드
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -----------------------------
# 2. 페이지 제목 및 설명
# -----------------------------
st.title("🌎 MBTI Type Distribution by Country")
st.write(
    """
    특정 **MBTI 유형이 높은 국가 TOP 10**을 시각화합니다.  
    슬라이더나 셀렉트를 통해 원하는 MBTI 유형을 선택해보세요.
    """
)

# -----------------------------
# 3. 사용자 입력 (MBTI 타입 선택)
# -----------------------------
mbti_types = [col for col in df.columns if col != "Country"]
selected_type = st.selectbox("분석할 MBTI 유형을 선택하세요:", mbti_types, index=0)

# -----------------------------
# 4. 선택된 MBTI 유형 상위 10개국 추출
# -----------------------------
top10 = df.nlargest(10, selected_type)[["Country", selected_type]].copy()
top10[selected_type] = (top10[selected_type] * 100).round(2)  # 퍼센트 변환

# -----------------------------
# 5. Altair 시각화
# -----------------------------
chart = (
    alt.Chart(top10)
    .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
    .encode(
        x=alt.X("Country:N", sort='-y', title="국가"),
        y=alt.Y(f"{selected_type}:Q", title=f"{selected_type} 비율 (%)"),
        color=alt.Color(f"{selected_type}:Q", scale=alt.Scale(scheme='tealblues')),
        tooltip=["Country", f"{selected_type}"]
    )
    .properties(
        title=f"🏆 {selected_type} 유형이 높은 국가 TOP 10",
        width=700,
        height=400
    )
)

# -----------------------------
# 6. 결과 출력
# -----------------------------
st.altair_chart(chart, use_container_width=True)

# 테이블도 함께 표시
st.dataframe(top10.set_index("Country"), use_container_width=True)

# -----------------------------
# 7. 요약 텍스트
# -----------------------------
max_country = top10.iloc[0]["Country"]
max_value = top10.iloc[0][selected_type]
st.success(f"**{selected_type}** 유형이 가장 높은 국가는 **{max_country}**, 비율은 **{max_value}%** 입니다.")

