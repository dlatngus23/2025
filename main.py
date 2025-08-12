import streamlit as st
import random

# 단어 목록 불러오기 (UTF-8 txt 파일, 한 줄에 한 단어)
@st.cache_data
def load_words():
    with open("korean_words.txt", "r", encoding="utf-8") as f:
        words = [w.strip() for w in f if len(w.strip()) > 1]  # 한 글자 단어 제외
    return words

word_bank = load_words()

st.title("📚 AI 백과사전 끝말잇기")

if "words" not in st.session_state:
    st.session_state.words = []
if "last_char" not in st.session_state:
    st.session_state.last_char = None

user_word = st.text_input("당신의 단어:")

if st.button("제출"):
    if not st.session_state.words:
        st.session_state.words.append(user_word)
        st.session_state.last_char = user_word[-1]
    else:
        if user_word[0] != st.session_state.last_char:
            st.error(f"'{st.session_state.last_char}'로 시작해야 합니다!")
        elif user_word not in word_bank:
            st.error("백과사전 단어 목록에 없는 단어입니다!")
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
