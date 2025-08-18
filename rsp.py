# app.py
import streamlit as st
import random
from collections import defaultdict, Counter

st.set_page_config(page_title="AI 가위바위보 하나빼기", page_icon="✌️", layout="centered")

# ---------------------------
# 기본 데이터 & 유틸
# ---------------------------
HANDS = ["가위", "바위", "보"]
EMOJI = {"가위": "✌️", "바위": "✊", "보": "✋"}
# 승부 결과: user 기준
def judge(user, ai):
    if user == ai:
        return 0
    if (user, ai) in [("가위","보"), ("바위","가위"), ("보","바위")]:
        return 1
    return -1

def best_response(ai_candidates, target_user_hand):
    # 유저 손에 가장 유리한 AI 손을 선택 (이기기>비기기>지기)
    ranked = sorted(ai_candidates, key=lambda h: (-judge(h, target_user_hand), random.random()))
    return ranked[0]

def weighted_choice(weights_dict):
    # {"가위":w1, "바위":w2, "보":w3} -> 확률 선택
    total = sum(weights_dict.values())
    r = random.random() * total
    upto = 0
    for k, w in weights_dict.items():
        upto += w
        if upto >= r:
            return k
    return random.choice(HANDS)

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "score" not in st.session_state:
    st.session_state.score = {"user": 0, "ai": 0, "draw": 0}
if "round" not in st.session_state:
    st.session_state.round = 1
if "phase" not in st.session_state:
    # phases: "pick_two" -> "reveal" -> "keep_one" -> "result"
    st.session_state.phase = "pick_two"
if "user_two" not in st.session_state:
    st.session_state.user_two = ["가위", "바위"]
if "ai_two" not in st.session_state:
    st.session_state.ai_two = ["가위", "바위"]
if "ai_precommit" not in st.session_state:
    st.session_state.ai_precommit = None
if "history" not in st.session_state:
    # 라운드별 기록 저장
    st.session_state.history = []
if "user_keep_history" not in st.session_state:
    st.session_state.user_keep_history = []  # 유저가 마지막에 남긴 손들의 기록

# ---------------------------
# 사이드바 설정
# ---------------------------
st.sidebar.title("⚙️ 설정")
mode = st.sidebar.radio("모드 선택", ["공정 모드(동시 선택)", "도전 모드(AI 최적 반응)"], index=0)
level = st.sidebar.select_slider("난이도", options=["초급","중급","고급"], value="중급")
if st.sidebar.button("🔄 전체 리셋"):
    st.session_state.score = {"user": 0, "ai": 0, "draw": 0}
    st.session_state.round = 1
    st.session_state.phase = "pick_two"
    st.session_state.history = []
    st.session_state.user_keep_history = []
    st.session_state.ai_precommit = None
    st.rerun()

# ---------------------------
# AI 초기 두 손 선택 전략
# ---------------------------
def ai_pick_two(level:str):
    # 유저의 과거 '남긴 손' 히스토리를 이용해 카운터 전략
    counts = Counter(st.session_state.user_keep_history)
    # 기본 가중치
    if level == "초급":
        # 거의 랜덤
        base = {"가위":1, "바위":1, "보":1}
    elif level == "중급":
        # 최근 경향을 약간 반영
        base = {"가위":1.0, "바위":1.0, "보":1.0}
        # 유저가 자주 남기는 손을 이기는 손 쪽 가중치 소폭 증가
        if counts:
            most = counts.most_common(1)[0][0]
            counter = {"가위":"바위", "바위":"보", "보":"가위"}[most]
            base[counter] += 0.7
    else: # 고급
        # 과거 분포 기반 확률적 대응
        total = sum(counts.values()) if counts else 0
        if total == 0:
            base = {"가위":1.2, "바위":1.2, "보":1.2}
        else:
            # 유저 분포를 이길 확률 극대화: P(ai=h) ∝ ∑_u P(user_keep=u) * 𝟙(judge(h,u)==1) + 0.5*𝟙(draw)
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
# 헤더 & 점수판
# ---------------------------
st.title("✌️ AI와 가위바위보 하나빼기")
st.caption("둘이 각각 **두 손**을 내고, 공개 후 **하나를 빼서** 최종 한 손으로 승부!")

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
# 1) 두 손 선택 단계
# ---------------------------
if st.session_state.phase == "pick_two":
    st.subheader("1) 두 손을 선택하세요")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**내 두 손**")
        u1 = st.selectbox("첫 번째 손", HANDS, index=HANDS.index(st.session_state.user_two[0]), key="u1")
        u2 = st.selectbox("두 번째 손", HANDS, index=HANDS.index(st.session_state.user_two[1]), key="u2")
        st.session_state.user_two = [u1, u2]
    with c2:
        st.markdown("**AI는 비공개로 두 손을 선택 중…**")

    if st.button("🔍 공개하기"):
        # AI 두 손 확정
        st.session_state.ai_two = ai_pick_two(level)
        # 공정 모드면, AI가 남길 한 손도 미리 비밀리에 확정(동시 선택 가정)
        if "공정" in mode:
            # 유저가 무엇을 남길지 예측 어려우므로, AI는 자기 두 손 중 무작위 or 간단한 휴리스틱
            # 휴리스틱: 서로 다른 손이라면 '가위<바위<보' 순으로 균형있게 랜덤
            st.session_state.ai_precommit = random.choice(st.session_state.ai_two)
        else:
            st.session_state.ai_precommit = None
        st.session_state.phase = "reveal"
        st.rerun()

# ---------------------------
# 2) 양측 두 손 공개
# ---------------------------
elif st.session_state.phase == "reveal":
    st.subheader("2) 양측 두 손 공개!")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**나**")
        st.markdown(f"{EMOJI[st.session_state.user_two[0]]}  {EMOJI[st.session_state.user_two[1]]} "
                    f"({st.session_state.user_two[0]}, {st.session_state.user_two[1]})")
    with c2:
        st.markdown("**AI**")
        st.markdown(f"{EMOJI[st.session_state.ai_two[0]]}  {EMOJI[st.session_state.ai_two[1]]} "
                    f"({st.session_state.ai_two[0]}, {st.session_state.ai_two[1]})")

    st.info("이제 각자 한 손을 **빼고** 하나만 남깁니다.")
    if st.button("🖐 하나 빼러 가기"):
        st.session_state.phase = "keep_one"
        st.rerun()

# ---------------------------
# 3) 하나 빼기(최종 한 손 선택)
# ---------------------------
elif st.session_state.phase == "keep_one":
    st.subheader("3) 어떤 손을 남길까요?")
    user_keep = st.radio(
        "내가 남길 손 선택",
        options=[f"{EMOJI[h]} {h}" for h in st.session_state.user_two],
        horizontal=True,
    )
    user_keep = user_keep.split()[-1]  # 텍스트에서 손 이름 추출

    # AI의 남길 손 결정
    if "공정" in mode:
        ai_keep = st.session_state.ai_precommit
    else:
        # 도전 모드: 유저 선택을 보고 최적 반응
        ai_keep = best_response(st.session_state.ai_two, user_keep)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**내 최종 손**")
        st.markdown(f"{EMOJI[user_keep]}  {user_keep}")
    with c2:
        st.markdown("**AI 최종 손**")
        st.markdown(f"{EMOJI[ai_keep]}  {ai_keep}")

    result = judge(user_keep, ai_keep)
    if result == 1:
        st.success("🎉 승리!")
    elif result == 0:
        st.warning("🤝 무승부")
    else:
        st.error("😵 패배…")

    # 완료 처리 버튼
    if st.button("✅ 결과 확정"):
        # 점수 반영
        if result == 1:
            st.session_state.score["user"] += 1
        elif result == 0:
            st.session_state.score["draw"] += 1
        else:
            st.session_state.score["ai"] += 1

        # 기록 저장
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

        # 다음 라운드 준비
        st.session_state.round += 1
        st.session_state.phase = "pick_two"
        st.session_state.ai_precommit = None
        st.rerun()

# ---------------------------
# 히스토리 & 도움말
# ---------------------------
st.divider()
with st.expander("📜 전판 기록 보기", expanded=False):
    if st.session_state.history:
        for h in reversed(st.session_state.history[-50:]):  # 최근 50판까지만 표시
            st.write(
                f"R{h['round']} | 모드:{h['mode']} | 난이도:{h['level']} | "
                f"내:{h['user_two']}→{h['user_keep']}  vs  AI:{h['ai_two']}→{h['ai_keep']} "
                f"⇒ **{h['result']}**"
            )
    else:
        st.caption("아직 기록이 없습니다.")

with st.expander("ℹ️ 규칙 / 팁", expanded=False):
    st.markdown("""
- **규칙**: 각자 **두 손**(가위/바위/보)을 낸 뒤, 공개 후 **하나를 빼서** 최종 한 손으로 승부합니다.  
- **공정 모드**: AI도 어떤 손을 남길지 **미리 비공개로 확정**합니다(동시 선택 가정).  
- **도전 모드**: 당신이 남긴 손을 보고 **AI가 유리한 손으로 대응**합니다.  
- **난이도**: AI의 **초기 두 손 선택** 전략에 영향을 줍니다.
    - *초급*: 거의 랜덤  
    - *중급*: 당신이 자주 남기는 손을 **이기는 손** 가중치 ↑  
    - *고급*: 과거 분포를 분석해 **이길 확률**을 통계적으로 높이려 합니다.
""")
