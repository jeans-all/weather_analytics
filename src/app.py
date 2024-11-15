import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta

# 페이지 기본 설정
st.set_page_config(
    page_title="날씨 모니터링 대시보드",
    layout="wide"
)

# 제목
st.title("실시간 날씨 모니터링 대시보드")

# DB에서 최신 데이터 조회
def get_latest_weather():
    conn = sqlite3.connect('weather_data.db')
    query = """
    SELECT city, temperature, humidity, weather_description, wind_speed, timestamp
    FROM weather_records
    WHERE timestamp = (SELECT MAX(timestamp) FROM weather_records)
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 최근 24시간 데이터 조회
def get_historical_data():
    conn = sqlite3.connect('weather_data.db')
    query = """
    SELECT city, temperature, humidity, timestamp
    FROM weather_records
    WHERE timestamp >= datetime('now', '-1 day')
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 최신 데이터 표시
latest_data = get_latest_weather()

# 도시별 현재 날씨 카드 표시
st.subheader("현재 날씨 현황")
cols = st.columns(len(latest_data))
for idx, (_, row) in enumerate(latest_data.iterrows()):
    with cols[idx]:
        st.metric(
            label=row['city'],
            value=f"{row['temperature']}°C",
            delta=f"습도 {row['humidity']}%"
        )
        st.write(f"날씨: {row['weather_description']}")
        st.write(f"풍속: {row['wind_speed']}m/s")

# 시계열 그래프
st.subheader("지역별 기온 변화")
historical_data = get_historical_data()
fig = px.line(
    historical_data,
    x='timestamp',
    y='temperature',
    color='city',
    title='도시별 기온 변화'
)
st.plotly_chart(fig, use_container_width=True)

# 습도 분포 그래프
st.subheader("현재 습도 분포")
fig_humidity = px.bar(
    latest_data,
    x='city',
    y='humidity',
    title='도시별 습도'
)
st.plotly_chart(fig_humidity, use_container_width=True)

# 데이터 업데이트 시간 표시
st.sidebar.write("최종 업데이트:", latest_data['timestamp'].iloc[0])
