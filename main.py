import streamlit as st

# MBTI 궁합 데이터 + 이유
compatibility_data = {
    "INTJ": {
        "matches": ["ENFP", "ENTP"],
        "reason": "서로의 부족한 부분을 채워주며 창의적 시너지를 발휘합니다.\n계획적인 성향과 자유로운 성향이 균형을 이룹니다."
    },
    "INTP": {
        "matches": ["ENTJ", "ESTJ"],
        "reason": "논리적인 분석가와 실행력이 강한 리더의 조합입니다.\n서로의 아이디어를 현실로 만드는 데 강점을 보입니다."
    },
    "ENTJ": {
        "matches": ["INTP", "ISTP"],
        "reason": "리더십과 전략이 조화를 이루는 관계입니다.\n결단력과 분석력이 균형을 잡아줍니다."
    },
    "ENTP": {
        "matches": ["INFJ", "INTJ"],
        "reason": "즉흥적인 발상과 깊이 있는 통찰력이 잘 어울립니다.\n서로에게 새로운 시각과 안정감을 제공합니다."
    },
    "INFJ": {
        "matches": ["ENFP", "ENTP"],
        "reason": "이상과 현실을 연결하는 조합입니다.\n서로에게 영감을 주고 정서적으로 지지합니다."
    },
    "INFP": {
        "matches": ["ENFJ", "ENTJ"],
        "reason": "이해심 깊은 이상가와 추진력 있는 리더의 조화입니다.\n서로의 가치관을 존중하며 성장합니다."
    },
    "ENFJ": {
        "matches": ["INFP", "ISFP"],
        "reason": "사람 중심의 가치관이 서로를 끌어당깁니다.\n감정적인 교감과 상호 성장이 강점입니다."
    },
    "ENFP": {
        "matches": ["INFJ", "INTJ"],
        "reason": "에너지와 영감을 주고받는 관계입니다.\n자유로움과 깊이가 공존합니다."
    },
    "ISTJ": {
        "matches": ["ESFP", "ESTP"],
        "reason": "책임감 있는 성향과 활동적인 성향이 균형을 이룹니다.\n서로의 삶에 활기를 불어넣습니다."
    },
    "ISFJ": {
        "matches": ["ESFP", "ESTP"],
        "reason": "세심한 배려와 활발한 성격이 어울립니다.\n서로의 장점을 인정하며 편안함을 줍니다."
    },
    "ESTJ": {
        "matches": ["ISTP", "INTP"],
        "reason": "체계적인 성향과 유연한 사고가 조화를 이룹니다.\n목표 달성에 있어 강력한 팀워크를 형성합니다."
    },
    "ESFJ": {
        "matches": ["ISFP", "INFP"],
        "reason": "따뜻한 배려와 자유로운 감성이 어우러집니다.\n서로의 일상에 안정감과 즐거움을 줍니다."
    },
    "ISTP": {
        "matches": ["ESTJ", "ENTJ"],
        "reason": "실용적인 문제 해결과 전략적 사고가 만나 강점을 발휘합니다.\n서로의 장점을 빠르게 인정합니다."
    },
    "ISFP": {
        "matches": ["ESFJ", "ENFJ"],
        "reason": "감성적인 교감과 실용성이 잘 어울립니다.\n서로의 가치관을 존중하며 편안함을 느낍니다."
    },
    "ESTP": {
        "matches": ["ISFJ", "INFJ"],
        "reason": "모험심과 안정감이 어우러지는 조합입니다.\n서로에게 새로운 경험과 안정을 동시에 제공합니다."
    },
    "ESFP": {
        "matches": ["ISFJ", "ISTJ"],
        "reason": "사교성과 책임감이 균형을 이루는 관계입니다.\n함께 있을 때 활력과 신뢰를 느낍니다."
    }
}

# 페이지 설정
st.set_page_config(page_title="MBTI 궁합 추천", page_icon="💡")

st.title("💡 MBTI 궁합 추천기")
st.write("당신의 MBTI를 선택하면 잘 맞는 MBTI와 그 이유를 알려드립니다!")

# MBTI 선택
user_mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(compatibility_data.keys()))

# 결과 표시
if user_mbti:
    data = compatibility_data.get(user_mbti)
    if data:
        matches = ", ".join(data["matches"])
        reason = data["reason"]
        st.success(f"✅ {user_mbti}와(과) 잘 맞는 MBTI는: **{matches}** 입니다!")
        st.info(reason)
    else:
        st.warning("해당 MBTI의 궁합 정보가 없습니다.")

