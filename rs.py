import streamlit as st

st.title("특정 단어 포함 문장 찾기")

# 1. 텍스트 입력 받기
text = st.text_area("텍스트를 입력하세요", height=200)

# 2. 키워드 입력 받기
keyword = st.text_input("찾고 싶은 단어를 입력하세요")

if st.button("검색"):
    if text.strip() == "" or keyword.strip() == "":
        st.write("텍스트와 단어를 모두 입력해주세요.")
    else:
        # 문장 분리 (마침표 기준)
        sentences = text.split('.')
        
        # 키워드 포함 문장 찾기 (대소문자 구분 없이)
        result = []
        for sentence in sentences:
            if keyword.lower() in sentence.lower():
                # 앞뒤 공백 제거 후 결과에 추가
                cleaned = sentence.strip()
                if cleaned != "":
                    result.append(cleaned)
        
        if result:
            st.write(f"'{keyword}'가 포함된 문장들:")
            for i, sent in enumerate(result, 1):
                st.write(f"{i}. {sent}.")
        else:
            st.write(f"'{keyword}'가 포함된 문장이 없습니다.")
