import streamlit as st

# MBTI별 귀여운 동물 데이터 (이미지 + 이름)
mbti_animals = {
    "INTJ": {"name": "고양이", "img": "https://i.imgur.com/QZ8jZrD.jpg"},
    "INTP": {"name": "부엉이", "img": "https://i.imgur.com/Y9Y4Y7Q.jpg"},
    "ENTJ": {"name": "사자", "img": "https://i.imgur.com/kGr3K7m.jpg"},
    "ENTP": {"name": "원숭이", "img": "https://i.imgur.com/WQq5w5v.jpg"},
    "INFJ": {"name": "사슴", "img": "https://i.imgur.com/Z6F4d0q.jpg"},
    "INFP": {"name": "토끼", "img": "https://i.imgur.com/Gf1B1hs.jpg"},
    "ENFJ": {"name": "강아지", "img": "https://i.imgur.com/0zQF4uO.jpg"},
    "ENFP": {"name": "코알라", "img": "https://i.imgur.com/lqQz7Zf.jpg"},
    "ISTJ": {"name": "거북이", "img": "https://i.imgur.com/BIRbYdN.jpg"},
    "ISFJ": {"name": "펭귄", "img": "https://i.imgur.com/mbx2Qzk.jpg"},
    "ESTJ": {"name": "독수리", "img": "https://i.imgur.com/wQ9Cqja.jpg"},
    "ESFJ": {"name": "카피바라", "img": "https://i.imgur.com/8BYc7X2.jpg"},
    "ISTP": {"name": "여우", "img": "https://i.imgur.com/YWBo4w3.jpg"},
    "ISFP": {"name": "고슴도치", "img": "https://i.imgur.com/X1j7zEo.jpg"},
    "ESTP": {"name": "돌고래", "img": "https://i.imgur.com/RcH6Whv.jpg"},
    "ESFP": {"name": "햄스터", "img": "https://i.imgur.com/fgLQ3Ov.jpg"},
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
