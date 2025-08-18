# app.py
import streamlit as st
import random
import string

st.set_page_config(page_title="Word Guess (5-letter)", page_icon="🟩", layout="centered")

# ---------------------------
# 기본 색상 (Wordle 스타일)
# ---------------------------
COLOR_CORRECT = "#6aaa64"   # 초록: 위치/문자 정답
COLOR_PRESENT = "#c9b458"   # 노랑: 존재하나 위치 오답
COLOR_ABSENT  = "#787c7e"   # 회색: 없음
COLOR_EMPTY   = "#d3d6da"   # 빈칸 테두리

# ---------------------------
# 기본 5글자 단어 목록 (영문)
# 필요시 사이드바에서 교체 가능
# ---------------------------
DEFAULT_WORDS = [
    "APPLE","GRAPE","MANGO","BERRY","LEMON","PEACH","PEARL","OLIVE","MELON","GUAVA",
    "BASIC","STONE","BRICK","PLANT","CHAIR","TABLE","CLOUD","STORM","RIVER","MUSIC",
    "ROBOT","LASER","CABLE","BRAVE","SMART","HAPPY","SADLY","FUNNY","ANGEL","DEVIL",
    "DRIVE","TRAIN","PLANE","SPEED","SLOWO","LIGHT","DARKS","EARTH","WATER","FIREY",
    "NURSE","DOCTOR","TEACH","LEARN","WRITE","READS","SMILE","CRYED","POWER","MIGHT",
]
# (주의) 위엔 데모용이라 영어 규범에 어긋나는 단어도 포함될 수 있어요.
# 실제 플레이용으로는 사이드바에서 적절한 5글자 영단어 목록을 붙여넣어 사용하세요.

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
    """
    Wordle 규칙대로 타일 색을 결정.
    반환: 리스트[('A', 'correct'|'present'|'absent'), ...] 길이 5
    """
    result = ["absent"] * 5
    target_list = list(target)

    # 1) 위치 일치 먼저 처리 (correct)
    for i, ch in enumerate(guess):
        if target[i] == ch:
            result[i] = "correct"
            target_list[i] = None  # 소진

    # 2) 남은 글자로 present 처리
    for i, ch in enumerate(guess):
        if result[i] == "correct":
            continue
        if ch in target_list:
            result[i] = "present"
            target_list[target_list.index(ch)] = None
        else:
            result[i] = "absent"

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
    html = "".join(
        tile(letter, color_of(state)) for letter, state in letters_states
    )
    st.markdown(f"<div style='display:flex;justify-content:center'>{html}</div>", unsafe_allow_html=True)

def render_empty_row(current_text=""):
    cells = []
    for i in range(5):
        if i < len(current_text):
            # 입력 중인 글자는 빈 타일에까지만 표시
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
    st.session_state.guesses = []  # 각 원소는 ("APPLE", [("A","correct"),...]) 형태
if "current" not in st.session_state:
    st.session_state.current = ""
if "keyboard" not in st.session_state:
    # 키보드 상태: 'correct' > 'present' > 'absent'
    st.session_state.keyboard = {}

# ---------------------------
# 사이드바 (설정/새게임/커스텀 단어)
# ---------------------------
st.sidebar.header("⚙️ 설정")
custom_list = st.sidebar.text_area("커스텀 5글자 단어 목록 (영문, 줄바꿈 구분)", height=160, placeholder="APPLE\nGRAPE\n... (한 줄에 하나)")
col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    if st.button("새 게임"):
        st.session_state.target = pick_target(st.session_state.words)
        st.session_state.guesses = []
        st.session_state.current = ""
        st.session_state.keyboard = {}
        st.experimental_rerun()
with col_sb2:
    if st.button("목록 적용"):
        words = [w.strip().upper() for w in custom_list.splitlines() if len(w.strip())==5 and w.strip().isalpha()]
        if len(words) >= 10:
            st.session_state.words = list(dict.fromkeys(words))  # 중복 제거
            st.session_state.target = pick_target(st.session_state.words)
            st.session_state.guesses = []
            st.session_state.current = ""
            st.session_state.keyboard = {}
            st.sidebar.success(f"단어 {len(st.session_state.words)}개 적용됨")
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
# 상태 체크 (승/패)
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
# 입력 & 키보드
# ---------------------------
def commit_guess():
    text = normalize_guess(st.session_state.current)
    if len(text) != 5:
        st.warning("5글자 영단어를 입력하세요.")
        return
    # 단어 목록 검사 (옵션)
    if text not in st.session_state.words:
        st.info("단어 목록에 없는 단어예요. 사이드바에서 목록을 교체하거나 이대로 진행할 수 있어요.")
        # 통과 허용 (원한다면 return으로 막을 수 있음)
    scored = score_guess(text, st.session_state.target)

    # 키보드 상태 업데이트
    for letter, state in scored:
        prev = st.session_state.keyboard.get(letter)
        priority = {"correct": 3, "present": 2, "absent": 1, None: 0}
        if priority[state] > priority.get(prev, 0):
            st.session_state.keyboard[letter] = state

    st.session_state.guesses.append((text, scored))
    st.session_state.current = ""

def press_letter(ch):
    if game_over:
        return
    cur = st.session_state.current
    if len(cur) < 5:
        st.session_state.current = cur + ch

def press_backspace():
    if game_over:
        return
    st.session_state.current = st.session_state.current[:-1]

def press_enter():
    if game_over:
        return
    commit_guess()

# 텍스트 입력창
st.text_input("직접 입력 (영문 5글자)", key="current", max_chars=5, help="엔터를 눌러 제출할 수 있어요.", on_change=commit_guess)

# 화면 키보드
kb_rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
st.write("")  # 간격

for row in kb_rows:
    cols = st.columns(len(row) + (2 if row.startswith("Z") else 0))
    for i, ch in enumerate(row):
        state = st.session_state.keyboard.get(ch)
        style = {}
        if state:
            style = {"correct": COLOR_CORRECT, "present": COLOR_PRESENT, "absent": COLOR_ABSENT}[state]
        if cols[i].button(ch, key=f"kb_{row}_{ch}"):
            press_letter(ch)
    if row.startswith("Z"):
        # Backspace, Enter
        if cols[-2].button("⌫", key="kb_backspace"):
            press_backspace()
        if cols[-1].button("ENTER", key="kb_enter"):
            press_enter()

# ---------------------------
# 결과
# ---------------------------
if game_over:
    if win:
        st.success(f"정답! 🎉  단어: **{st.session_state.target}**")
    else:
        st.error(f"실패! 😵  정답은 **{st.session_state.target}** 였어요.")

    # 공유용 그리드(이모지)
    def emoji_grid():
        lines = []
        for _, scored in st.session_state.guesses:
            line = "".join("🟩" if s=="correct" else "🟨" if s=="present" else "⬛" for _, s in scored)
            lines.append(line)
        return "\n".join(lines)

    st.code(emoji_grid(), language="text")
    if st.button("🔁 새 게임 시작"):
        st.session_state.target = pick_target(st.session_state.words)
        st.session_state.guesses = []
        st.session_state.current = ""
        st.session_state.keyboard = {}
        st.experimental_rerun()
