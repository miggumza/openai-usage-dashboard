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

# 날짜 포맷 맞추기
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

# API Key는 secrets.toml에 저장
api_key = st.secrets["openai"]["api_key"]

# API 호출
headers = {
    "Authorization": f"Bearer {api_key}"
}
url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_str}&end_date={end_str}"

response = requests.get(url, headers=headers)

# 결과 표시
if response.status_code == 200:
    data = response.json()
    usage_usd = data.get("total_usage", 0) / 100  # 센트 → 달러
    st.metric(label="💰 총 사용 금액 (USD)", value=f"${usage_usd:.2f}")
else:
    st.error("❌ 사용량 데이터를 불러올 수 없습니다.")