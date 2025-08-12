import streamlit as st

# MBTI 궁합 데이터 (예시)
compatibility_data = {
    "INTJ": ["ENFP", "ENTP"],
    "INTP": ["ENTJ", "ESTJ"],
    "ENTJ": ["INTP", "ISTP"],
    "ENTP": ["INFJ", "INTJ"],
    "INFJ": ["ENFP", "ENTP"],
    "INFP": ["ENFJ", "ENTJ"],
    "ENFJ": ["INFP", "ISFP"],
    "ENFP": ["INFJ", "INTJ"],
    "ISTJ": ["ESFP", "ESTP"],
    "ISFJ": ["ESFP", "ESTP"],
    "ESTJ": ["ISTP", "INTP"],
    "ESFJ": ["ISFP", "INFP"],
    "ISTP": ["ESTJ", "ENTJ"],
    "ISFP": ["ESFJ", "ENFJ"],
    "ESTP": ["ISFJ", "INFJ"],
    "ESFP": ["ISFJ", "ISTJ"]
}

st.set_page_config(page_title="MBTI 궁합 추천", page_icon="💡")

st.title("💡 MBTI 궁합 추천기")
st.write("당신의 MBTI를 선택하면 잘 맞는 MBTI를 추천해드립니다!")

# MBTI 선택
user_mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(compatibility_data.keys()))

# 결과 표시
if user_mbti:
    matches = compatibility_data.get(user_mbti, [])
    if matches:
        st.success(f"✅ {user_mbti}와(과) 잘 맞는 MBTI는: **{', '.join(matches)}** 입니다!")
    else:
        st.warning("해당 MBTI의 궁합 정보가 없습니다.")

