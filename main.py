import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="끝말잇기 게임", page_icon="🎮")

st.title("🎮 끝말잇기 게임")
st.write("마지막 글자에 맞춰 단어를 이어가세요!")

# 세션 상태 초기화
if "words" not in st.session_state:
    st.session_state.words = []
if "last_char" not in st.session_state:
    st.session_state.last_char = None

# 단어 입력 폼
with st.form("word_form"):
    user_word = st.text_input("단어 입력", "")
    submitted = st.form_submit_button("제출")

# 제출 처리
if submitted:
    if not user_word:
        st.warning("단어를 입력하세요.")
    else:
        # 1. 중복 단어 방지
        if user_word in st.session_state.words:
            st.error("이미 사용한 단어입니다.")
        # 2. 첫 단어이거나, 이전 단어 마지막 글자와 일치하는지 확인
        elif st.session_state.last_char and user_word[0] != st.session_state.last_char:
            st.error(f"첫 글자가 '{st.session_state.last_char}'로 시작해야 합니다.")
        else:
            st.session_state.words.append(user_word)
            st.session_state.last_char = user_word[-1]
            st.success(f"'{user_word}' 등록 완료!")

# 현재까지의 단어 기록
if st.session_state.words:
    st.subheader("📜 지금까지 나온 단어")
    st.write(" → ".join(st.session_state.words))

# 게임 리셋 버튼
if st.button("🔄 게임 리셋"):
    st.session_state.words = []
    st.session_state.last_char = None
    st.success("게임이 초기화되었습니다.")
