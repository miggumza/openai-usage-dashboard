import streamlit as st
import requests
import datetime

# 날짜 설정
today = datetime.date.today()
default_start = today - datetime.timedelta(days=7)

# UI 설정
st.set_page_config(page_title="OpenAI 사용량 대시보드", layout="centered")
st.title("📊 OpenAI API 사용량 대시보드")

start_date = st.date_input("시작 날짜", default_start)
end_date = st.date_input("종료 날짜", today)

# 날짜 유효성 검사
if start_date > end_date:
    st.warning("⚠️ 시작 날짜는 종료 날짜보다 이전이어야 합니다.")
    st.stop()

start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

# API 호출 시도
try:
    api_key = st.secrets["openai"]["api_key"]
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_str}&end_date={end_str}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        usage_usd = data.get("total_usage", 0) / 100  # 센트 → 달러
        st.metric(label="💰 총 사용 금액 (USD)", value=f"${usage_usd:.2f}")
    else:
        st.error("❌ 사용량 데이터를 불러올 수 없습니다.")
        st.code(f"응답 코드: {response.status_code}")
        st.code(response.text)

except KeyError as e:
    st.error("❌ API 키가 설정되어 있지 않습니다. Streamlit Secrets를 확인해 주세요.")
    st.code(str(e))

except Exception as e:
    st.error("❌ 예기치 못한 오류가 발생했습니다.")
    st.code(str(e))
