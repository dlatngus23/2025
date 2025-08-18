# app.py
import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="AI 가위바위보 하나빼기", page_icon="✌️", layout="centered")

HANDS = ["가위", "바위", "보"]
EMOJI = {"가위": "✌️", "바위": "✊", "보": "✋"}

def judge(user, ai):
    if user == ai:
        return 0
    if (user, ai) in [("가위","보"), ("바위","가위"), ("보","바위")]:
        return 1
    return -1

def best_response(ai_candidates, target_user_hand):
    ranked = sorted(ai_candidates, key=lambda h: (-judge(h, target_user_hand), random.random()))
    return ranked[0]

def weighted_choice(weights_dict):
    total = sum(weights_dict.values())
    r = random.random() * total
    upto = 0
    for k, w in weights_dict.items():
        upto += w
        if upto >= r:
            return k
    return random.choice(HANDS)

# ---------------------------
# 세션 상태
# ---------------------------
if "score" not in st.session_state:
    st.session_state.score = {"user": 0, "ai": 0, "draw": 0}
if "round" not in st.session_state:
    st.session_state.round = 1
if "phase" not in st.session_state:
    st.session_state.phase = "pick_two"
if "user_two" not in st.session_state:
    st.session_state.user_two = ["가위", "바위"]
if "ai_two" not in st.session_state:
    st.session_state.ai_two = ["가위", "바위"]
if "ai_precommit" not in st.session_state:
    st.session_state.ai_precommit = None
if "history" not in st.session_state:
    st.session_state.history = []
if "user_keep_history" not in st.session_state:
    st.session_state.user_keep_history = []
if "pending_choice" not in st.session_state:
    st.session_state.pending_choice = None

# ---------------------------
# 사이드바
# ---------------------------
st.sidebar.title("⚙️ 설정")
mode = st.sidebar.radio("모드 선택", ["공정 모드(동시 선택)", "도전 모드(AI 최적 반응)"], index=0)
level = st.sidebar.select_slider("난이도", options=["초급","중급","고급"], value="중급")
if st.sidebar.button("🔄 전체 리셋"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ---------------------------
# AI 초기 두 손 선택 전략
# ---------------------------
def ai_pick_two(level:str):
    counts = Counter(st.session_state.user_keep_history)
    if level == "초급":
        base = {"가위":1, "바위":1, "보":1}
    elif level == "중급":
        base = {"가위":1.0, "바위":1.0, "보":1.0}
        if counts:
            most = counts.most_common(1)[0][0]
            counter = {"가위":"바위", "바위":"보", "보":"가위"}[most]
            base[counter] += 0.7
    else:
        total = sum(counts.values()) if counts else 0
        if total == 0:
            base = {"가위":1.2, "바위":1.2, "보":1.2}
        else:
            dist = {h: counts[h]/total for h in HANDS}
            score_map = {}
            for h in HANDS:
                win_prob = sum(p for u,p in dist.items() if judge(h,u)==1)
                draw_prob = sum(p for u,p in dist.items() if judge(h,u)==0)
                score_map[h] = 1e-6 + win_prob + 0.5*draw_prob
            base = score_map
    first = weighted_choice(base)
    second = weighted_choice(base)
    return [first, second]

# ---------------------------
# 헤더
# ---------------------------
st.title("✌️ AI와 가위바위보 하나빼기")
col_s, col_r = st.columns([2,1])
with col_s:
    st.subheader("📊 점수")
    c1, c2, c3 = st.columns(3)
    c1.metric("나", st.session_state.score["user"])
    c2.metric("AI", st.session_state.score["ai"])
    c3.metric("무승부", st.session_state.score["draw"])
with col_r:
    st.subheader("라운드")
    st.metric("Round", st.session_state.round)

st.divider()

# ---------------------------
# 단계별 화면
# ---------------------------
if st.session_state.phase == "pick_two":
    st.subheader("1) 두 손을 선택하세요")
    u1 = st.selectbox("첫 번째 손", HANDS, index=HANDS.index(st.session_state.user_two[0]), key="u1")
    u2 = st.selectbox("두 번째 손", HANDS, index=HANDS.index(st.session_state.user_two[1]), key="u2")
    st.session_state.user_two = [u1, u2]

    if st.button("🔍 공개하기"):
        st.session_state.ai_two = ai_pick_two(level)
        if "공정" in mode:
            st.session_state.ai_precommit = random.choice(st.session_state.ai_two)
        else:
            st.session_state.ai_precommit = None
        st.session_state.phase = "reveal"
        st.rerun()

elif st.session_state.phase == "reveal":
    st.subheader("2) 양측 두 손 공개!")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"내: {EMOJI[st.session_state.user_two[0]]} {EMOJI[st.session_state.user_two[1]]}")
    with c2:
        st.markdown(f"AI: {EMOJI[st.session_state.ai_two[0]]} {EMOJI[st.session_state.ai_two[1]]}")

    if st.button("🖐 하나 빼러 가기"):
        st.session_state.phase = "keep_one"
        st.session_state.pending_choice = None
        st.rerun()

elif st.session_state.phase == "keep_one":
    st.subheader("3) 어떤 손을 남길까요?")
    user_choice = st.radio(
        "내가 남길 손 선택",
        options=[f"{EMOJI[h]} {h}" for h in st.session_state.user_two],
        horizontal=True,
    )
    user_keep = user_choice.split()[-1]

    if st.button("✅ 선택 확정"):
        st.session_state.pending_choice = user_keep
        st.session_state.phase = "result"
        st.rerun()

elif st.session_state.phase == "result":
    user_keep = st.session_state.pending_choice
    if "공정" in mode:
        ai_keep = st.session_state.ai_precommit
    else:
        ai_keep = best_response(st.session_state.ai_two, user_keep)

    st.subheader("4) 최종 결과")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"내 최종: {EMOJI[user_keep]} {user_keep}")
    with c2:
        st.markdown(f"AI 최종: {EMOJI[ai_keep]} {ai_keep}")

    result = judge(user_keep, ai_keep)
    if result == 1:
        st.success("🎉 승리!")
    elif result == 0:
        st.warning("🤝 무승부")
    else:
        st.error("😵 패배…")

    if st.button("다음 라운드 ▶"):
        if result == 1:
            st.session_state.score["user"] += 1
        elif result == 0:
            st.session_state.score["draw"] += 1
        else:
            st.session_state.score["ai"] += 1

        st.session_state.user_keep_history.append(user_keep)
        st.session_state.history.append({
            "round": st.session_state.round,
            "user_two": tuple(st.session_state.user_two),
            "ai_two": tuple(st.session_state.ai_two),
            "mode": mode,
            "level": level,
            "user_keep": user_keep,
            "ai_keep": ai_keep,
            "result": "승" if result==1 else ("무" if result==0 else "패"),
        })

        st.session_state.round += 1
        st.session_state.phase = "pick_two"
        st.session_state.ai_precommit = None
        st.session_state.pending_choice = None
        st.rerun()

# ---------------------------
# 기록
# ---------------------------
st.divider()
with st.expander("📜 전판 기록"):
    for h in reversed(st.session_state.history[-50:]):
        st.write(f"R{h['round']} | {h['user_two']}→{h['user_keep']} vs {h['ai_two']}→{h['ai_keep']} ⇒ {h['result']}")
