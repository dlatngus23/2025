import streamlit as st
import random

st.title("🤖 AI와 가위바위보 게임")

options = ["가위", "바위", "보"]
user_choice = st.radio("가위, 바위, 보 중에서 선택하세요:", options)

if st.button("결과 확인"):
    ai_choice = random.choice(options)
    st.write(f"당신: {user_choice}")
    st.write(f"AI: {ai_choice}")

    if user_choice == ai_choice:
        st.info("무승부!")
    elif (user_choice == "가위" and ai_choice == "보") or \
         (user_choice == "바위" and ai_choice == "가위") or \
         (user_choice == "보" and ai_choice == "바위"):
        st.success("당신이 이겼습니다! 🎉")
    else:
        st.error("AI가 이겼습니다! 😢")
