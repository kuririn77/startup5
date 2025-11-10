import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt

# 💩 스마트 화장실 앱 — 한국어 버전
st.set_page_config(page_title="스마트 화장실 💧", layout='wide')

# ------------------------------ 초기 설정 ------------------------------
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'profile' not in st.session_state:
    st.session_state.profile = {}

# ------------------------------ 1️⃣ 사용자 기본 프로필 ------------------------------
st.title("🚽 스마트 화장실 건강 관리 앱 💩")
st.markdown("### 🧍‍♀️ 사용자 기본 프로필")

닉네임 = st.text_input("닉네임을 입력하세요 ✏️")
나이 = st.number_input("나이", 1, 120, 25)
성별 = st.selectbox("성별", ["선택 안 함", "남성", "여성", "기타"])

건강특이사항 = st.multiselect(
    "건강 특이사항을 선택하세요 💊",
    ["없음", "고혈압", "당뇨", "임신 중", "신장 질환", "소화 문제", "기타"]
)

검사동의 = st.radio("AI 건강 분석을 허용하시겠습니까? 🤖", ["예", "아니오"])

if st.button("프로필 저장하기 💾"):
    st.session_state.profile = {
        '닉네임': 닉네임,
        '나이': 나이,
        '성별': 성별,
        '건강특이사항': 건강특이사항,
        '검사동의': 검사동의
    }
    st.success(f"✅ {닉네임}님의 프로필이 저장되었습니다!")

st.divider()

# ------------------------------ 2️⃣ 화장실 방문 기록 ------------------------------
st.header("🚻 화장실 방문 기록")

if st.button("지문 인식으로 방문하기 🖐️"):
    now = datetime.datetime.now()
    st.session_state.data = pd.concat([
        st.session_state.data,
        pd.DataFrame([{'날짜': now, 'pH': np.nan, '단백질': np.nan, '당': np.nan, '색상': np.nan, '온도': np.nan}])
    ], ignore_index=True)
    st.success(f"🚽 {now.strftime('%Y-%m-%d %H:%M')} 방문이 기록되었습니다!")

st.divider()

# ------------------------------ 3️⃣ AI 건강 분석 ------------------------------
st.header("🧠 내 똥 건강 분석 (AI 센서 기반)")

if 검사동의 == "예":
    if st.button("AI 센서 데이터 분석하기 ⚙️"):
        # 더미 센서 데이터 생성
        df = pd.DataFrame({
            '날짜': pd.date_range(datetime.date.today() - datetime.timedelta(days=6), periods=7),
            'pH': np.random.uniform(5.5, 8.0, 7),
            '단백질': np.random.uniform(0.1, 2.0, 7),
            '당': np.random.uniform(0.1, 1.0, 7),
            '색상': np.random.uniform(1, 10, 7),
            '온도': np.random.uniform(35, 38, 7)
        })

        df['장건강'] = 100 - abs(df['pH'] - 6.8) * 10
        df['수분'] = 100 - (df['색상'] - 1) * 8
        df['영양'] = 100 - abs(df['단백질'] - 1.0) * 20

        st.session_state.data = df
        st.success("🧬 AI 분석 완료! 결과를 아래에서 확인하세요 ⬇️")
else:
    st.warning("⚠️ 사용자가 AI 검사에 동의하지 않았습니다. 프로필에서 변경하세요.")

st.divider()

# ------------------------------ 4️⃣ 건강 변화 그래프 ------------------------------
st.header("📈 내 똥 건강 변화 그래프")

if not st.session_state.data.empty:
    view = st.session_state.data.melt('날짜', ['장건강', '수분', '영양'], var_name='지표', value_name='점수')
    chart = alt.Chart(view).mark_line(point=True).encode(
        x='날짜:T', y='점수:Q', color='지표:N', tooltip=['날짜:T', '지표:N', '점수:Q']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("아직 데이터가 없습니다. 분석을 먼저 진행하세요! 💩")

st.divider()

# ------------------------------ 5️⃣ 성취 시스템 ------------------------------
st.header("🏅 건강 뱃지 시스템")

if not st.session_state.data.empty:
    recent = st.session_state.data.tail(1).iloc[0]
    badges = []

    if recent['장건강'] > 80:
        badges.append('💪 장 튼튼왕')
    if recent['수분'] > 80:
        badges.append('💧 수분왕')
    if recent['영양'] > 80:
        badges.append('🍎 영양만점')

    if badges:
        st.success("🎉 새로 획득한 뱃지:")
        for b in badges:
            st.write(b)
    else:
        st.info("아직 획득한 뱃지가 없습니다 😅 꾸준히 노력해봐요!")
else:
    st.info("데이터가 없어요. 먼저 분석을 진행해주세요!")

st.divider()

st.caption("⚠️ 본 앱은 건강 참고용이며, 의료 진단을 대체하지 않습니다.")
