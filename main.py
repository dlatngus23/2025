import streamlit as st

# MBTI별 귀여운 동물 데이터 (이미지 + 이름)
mbti_animals = {
    "INTJ": {"name": "고양이", "img": "https://images.unsplash.com/photo-1518791841217-8f162f1e1131"},
    "INTP": {"name": "부엉이", "img": "https://images.unsplash.com/photo-1501706362039-c6e80948f162"},
    "ENTJ": {"name": "사자", "img": "https://images.unsplash.com/photo-1552410260-0fd40f1e8a3d"},
    "ENTP": {"name": "원숭이", "img": "https://images.unsplash.com/photo-1574158622682-e40e69881006"},
    "INFJ": {"name": "사슴", "img": "https://images.unsplash.com/photo-1501706362039-c6e80948f162"},
    "INFP": {"name": "토끼", "img": "https://images.unsplash.com/photo-1547394765-185e1e68f34e"},
    "ENFJ": {"name": "강아지", "img": "https://images.unsplash.com/photo-1507149833265-60c372daea22"},
    "ENFP": {"name": "코알라", "img": "https://images.unsplash.com/photo-1575548641098-f2a94b79fe66"},
    "ISTJ": {"name": "거북이", "img": "https://images.unsplash.com/photo-1505843293017-71cb1a4e68b9"},
    "ISFJ": {"name": "펭귄", "img": "https://images.unsplash.com/photo-1504292004442-f3866f0e9c9e"},
    "ESTJ": {"name": "독수리", "img": "https://images.unsplash.com/photo-1572044162444-ad60f128bdea"},
    "ESFJ": {"name": "카피바라", "img": "https://images.unsplash.com/photo-1624896877888-1739b9e8f5f5"},
    "ISTP": {"name": "여우", "img": "https://images.unsplash.com/photo-1546182990-dffeafbe841d"},
    "ISFP": {"name": "고슴도치", "img": "https://images.unsplash.com/photo-1601758124279-0c3f31a1127a"},
    "ESTP": {"name": "돌고래", "img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"},
    "ESFP": {"name": "햄스터", "img": "https://images.unsplash.com/photo-1618847880473-029d8ab0f8d4"},
}

# 페이지 설정
st.set_page_config(page_title="MBTI 동물 매칭", page_icon="🐾")

st.title("🐾 MBTI 동물 매칭")
st.write("당신의 MBTI에 어울리는 귀여운 동물을 찾아보세요!")

# MBTI 선택
user_mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(mbti_animals.keys()))

# 결과 표시
if user_mbti:
    animal = mbti_animals[user_mbti]
    st.success(f"{user_mbti}와 어울리는 귀여운 동물은 **{animal['name']}** 입니다!")
    st.image(animal["img"], caption=f"{animal['name']} 🐾", use_column_width=True)
