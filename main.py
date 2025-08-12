import streamlit as st
import random

# 단어 목록 (예시: 실제로는 수천 개 가능)
word_bank = [
    "사과", "과자", "자동차", "차표", "표범", "범고래", "래미안", "안경", "경찰", "찰흙",
    "흙집", "집게", "게장", "장갑", "갑옷", "옷장", "장난감", "감자", "자전거",
    "거북이", "이발소", "소방서", "서랍", "랍스터", "터미널", "널빤지", "지구", "구름"
]

st.title("📚 AI 끝말잇기")

if "words" not in st.session_state:
    st.session_state.words = []
if "last_char" not in st.session_state:
    st.session_state.last_char = None

user_word = st.text_input("당신의 단어:")

if st.button("제출"):
    if not st.session_state.words:
        if user_word in word_bank:
            st.session_state.words.append(user_word)
            st.session_state.last_char = user_word[-1]
        else:
            st.error("단어 목록에 없는 단어입니다!")
    else:
        if user_word[0] != st.session_state.last_char:
            st.error(f"'{st.session_state.last_char}'로 시작해야 합니다!")
        elif user_word not in word_bank:
            st.error("단어 목록에 없는 단어입니다!")
        else:
            st.session_state.words.append(user_word)
            st.session_state.last_char = user_word[-1]

            # AI 차례
            candidates = [w for w in word_bank if w[0] == st.session_state.last_char and w not in st.session_state.words]
            if candidates:
                ai_word = random.choice(candidates)
                st.session_state.words.append(ai_word)
                st.session_state.last_char = ai_word[-1]
                st.info(f"AI: {ai_word}")
            else:
                st.success("AI가 단어를 못 찾았습니다. 당신의 승리!")

if st.session_state.words:
    st.write(" → ".join(st.session_state.words))

if st.button("게임 리셋"):
    st.session_state.words = []
    st.session_state.last_char = None
