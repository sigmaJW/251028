import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------
# 1. 페이지 설정
# -----------------------------
st.set_page_config(page_title="MBTI by Country", page_icon="🌎", layout="centered")

# -----------------------------
# 2. 제목 및 설명
# -----------------------------
st.title("🌎 MBTI Type Distribution by Country")
st.markdown(
    """
    이 앱은 **MBTI 유형이 높은 국가 TOP 10**을 시각적으로 보여줍니다.  
    아래에서 `countriesMBTI_16types.csv` 파일을 업로드하고,  
    분석할 MBTI 유형을 선택해보세요.
    """
)

# -----------------------------
# 3. 파일 업로드
# -----------------------------
uploaded = st.file_uploader("📂 CSV 파일 업로드 (예: countriesMBTI_16types.csv)", type=["csv"])

if uploaded is None:
    st.info("⬆️ 파일을 업로드하면 분석이 시작됩니다.")
    st.stop()

# -----------------------------
# 4. 데이터 불러오기
# -----------------------------
try:
    df = pd.read_csv(uploaded)
except Exception as e:
    st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# 데이터 기본 검증
if "Country" not in df.columns:
    st.error("❌ CSV에 'Country' 열이 없습니다. 올바른 파일을 업로드하세요.")
    st.stop()

# -----------------------------
# 5. 사용자 입력 (MBTI 유형 선택)
# -----------------------------
mbti_types = [col for col in df.columns if col != "Country"]
selected_type = st.selectbox("분석할 MBTI 유형을 선택하세요:", mbti_types, index=0)

# -----------------------------
# 6. 상위 10개국 계산
# -----------------------------
top10 = df.nlargest(10, selected_type)[["Country", selected_type]].copy()
top10[selected_type] = (top10[selected_type] * 100).round(2)  # 퍼센트로 변환

# -----------------------------
# 7. Altair 시각화
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

st.altair_chart(chart, use_container_width=True)

# -----------------------------
# 8. 테이블 및 요약
# -----------------------------
st.subheader("📊 Top 10 데이터")
st.dataframe(top10.set_index("Country"), use_container_width=True)

max_country = top10.iloc[0]["Country"]
max_value = top10.iloc[0][selected_type]
st.success(f"**{selected_type}** 유형이 가장 높은 국가는 **{max_country}**, 비율은 **{max_value}%** 입니다.")
