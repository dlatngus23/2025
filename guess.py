# app.py
import streamlit as st
import random
import string

st.set_page_config(page_title="Word Guess (5-letter)", page_icon="🟩", layout="centered")

# ---------------------------
# 색상
# ---------------------------
COLOR_CORRECT = "#6aaa64"   # 초록: 위치/문자 정답
COLOR_PRESENT = "#c9b458"   # 노랑: 존재하나 위치 오답
COLOR_ABSENT  = "#787c7e"   # 회색: 없음
COLOR_EMPTY   = "#d3d6da"   # 빈칸 테두리

# ---------------------------
# 기본 단어 목록
# ---------------------------
DEFAULT_WORDS = [
    "APPLE","GRAPE","MANGO","BERRY","LEMON","PEACH","OLIVE","MELON","GUAVA",
    "BASIC","STONE","PLANT","CHAIR","TABLE","CLOUD","STORM","RIVER","MUSIC",
    "ROBOT","LASER","CABLE","BRAVE","SMART","HAPPY","FUNNY","ANGEL","DEVIL",
]

# ---------------------------
# 유틸
# ---------------------------
def normalize_guess(s: str) -> str:
    s = (s or "").strip().upper()
    s = "".join(ch for ch in s if ch in string.ascii_uppercase)
    return s[:5]

def pick_target(words):
    return random.choice(words).upper()

def score_guess(guess: str, target: str):
    result = ["absent"] * 5
    target_list = list(target)
    # correct
    for i, ch in enumerate(guess):
        if target[i] == ch:
            result[i] = "correct"
            target_list[i] = None
    # present
    for i, ch in enumerate(guess):
        if result[i] == "correct": continue
        if ch in target_list:
            result[i] = "present"
            target_list[target_list.index(ch)] = None
    return list(zip(list(guess), result))

def color_of(state: str):
    return {"correct": COLOR_CORRECT, "present": COLOR_PRESENT, "absent": COLOR_ABSENT}[state]

def tile(letter: str, bg: str | None, border_only=False):
    if border_only:
        style = f"""
        display:inline-flex;justify-content:center;align-items:center;
        width:56px;height:56px;margin:3px;font-weight:800;font-size:24px;
        border:2px solid {COLOR_EMPTY}; border-radius:6px; text-transform:uppercase;
        """
        return f"<div style='{style}'></div>"
    else:
        style = f"""
        display:inline-flex;justify-content:center;align-items:center;
        width:56px;height:56px;margin:3px;font-weight:800;font-size:24px;
        background:{bg}; color:white; border-radius:6px; text-transform:uppercase;
        """
        return f"<div style='{style}'>{letter}</div>"

def render_row(letters_states):
    html = "".join(tile(letter, color_of(state)) for letter, state in letters_states)
    st.markdown(f"<div style='display:flex;justify-content:center'>{html}</div>", unsafe_allow_html=True)

def render_empty_row(current_text=""):
    cells = []
    for i in range(5):
        if i < len(current_text):
            cells.append(
                f"<div style='display:inline-flex;justify-content:center;align-items:center;"
                f"width:56px;height:56px;margin:3px;font-weight:800;font-size:24px;"
                f"border:2px solid {COLOR_EMPTY}; border-radius:6px; text-transform:uppercase;'>{current_text[i]}</div>"
            )
        else:
            cells.append(tile("", bg=None, border_only=True))
    st.markdown(f"<div style='display:flex;justify-content:center'>{''.join(cells)}</div>", unsafe_allow_html=True)

# ---------------------------
# 세션 상태
# ---------------------------
if "words" not in st.session_state:
    st.session_state.words = DEFAULT_WORDS[:]
if "target" not in st.session_state:
    st.session_state.target = pick_target(st.session_state.words)
if "guesses" not in st.session_state:
    st.session_state.guesses = []
if "current" not in st.session_state:
    st.session_state.current = ""

# ---------------------------
# 사이드바 (새 게임/목록 교체)
# ---------------------------
st.sidebar.header("⚙️ 설정")
custom_list = st.sidebar.text_area("커스텀 5글자 단어 목록 (영문, 줄바꿈 구분)", height=160)
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("새 게임"):
        st.session_state.target = pick_target(st.session_state.words)
        st.session_state.guesses = []
        st.session_state.current = ""
        st.experimental_rerun()
with col2:
    if st.button("목록 적용"):
        words = [w.strip().upper() for w in custom_list.splitlines() if len(w.strip())==5 and w.strip().isalpha()]
        if len(words) >= 10:
            st.session_state.words = list(dict.fromkeys(words))
            st.session_state.target = pick_target(st.session_state.words)
            st.session_state.guesses = []
            st.session_state.current = ""
            st.sidebar.success(f"{len(words)}개 단어 적용됨")
        else:
            st.sidebar.error("최소 10개 이상의 5글자 영단어를 넣어주세요.")

# ---------------------------
# 헤더
# ---------------------------
st.title("🟩 Word Guess – 5글자")
st.caption("6번 안에 5글자 단어를 맞혀보세요!")

# ---------------------------
# 보드 렌더링
# ---------------------------
MAX_TRIES = 6
for i in range(MAX_TRIES):
    if i < len(st.session_state.guesses):
        render_row(st.session_state.guesses[i][1])
    elif i == len(st.session_state.guesses):
        render_empty_row(st.session_state.current)
    else:
        render_empty_row("")

# ---------------------------
# 상태 체크
# ---------------------------
game_over = False
win = False
if st.session_state.guesses:
    last_word, last_states = st.session_state.guesses[-1]
    if all(state == "correct" for _, state in last_states):
        game_over, win = True, True
if len(st.session_state.guesses) >= MAX_TRIES and not win:
    game_over = True

# ---------------------------
# 입력
# ---------------------------
def commit_guess():
    text = normalize_guess(st.session_state.current)
    if len(text) != 5:
        st.warning("5글자 영단어를 입력하세요.")
        return
    scored = score_guess(text, st.session_state.target)
    st.session_state.guesses.append((text, scored))
    st.session_state.current = ""

st.text_input("영문 5글자 입력 후 Enter", key="current", max_chars=5, on_change=commit_guess)

# ---------------------------
# 결과
# ---------------------------
if game_over:
    if win:
        st.success(f"정답! 🎉  단어: **{st.session_state.target}**")
    else:
        st.error(f"실패! 😵  정답은 **{st.session_state.target}** 였어요.")
    if st.button("🔁 새 게임 시작"):
        st.session_state.target = pick_target(st.session_state.words)
        st.session_state.guesses = []
        st.session_state.current = ""
        st.experimental_rerun()
