import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta

# Basic Page Setting
st.set_page_config(
    page_title="날씨 모니터링 대시보드",
    layout="wide"
)

# Title
st.title("실시간 날씨 모니터링 대시보드")

# Retrive latest data from database
def get_latest_weather():
    conn = sqlite3.connect('data/weather_data.db')
    query = """
    SELECT city, temperature, humidity, weather_description, wind_speed, timestamp
    FROM weather_records
    WHERE timestamp = (SELECT MAX(timestamp) FROM weather_records)
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Retrieve data of last 24 hours 
def get_historical_data():
    conn = sqlite3.connect('data/weather_data.db')
    query = """
    SELECT city, temperature, humidity, timestamp
    FROM weather_records
    WHERE timestamp >= datetime('now', '-1 day')
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

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

# Time-series graph
st.subheader("지역별 기온 변화")
historical_data = get_historical_data()
fig = px.line(
    historical_data,
    x='timestamp',
    y='temperature',
    color='city',
    title='Temperature Change Per City'
)
st.plotly_chart(fig, use_container_width=True)

# Humidity Distribution Graph
st.subheader("Current Humidity Distribution")
fig_humidity = px.bar(
    latest_data,
    x='city',
    y='humidity',
    title='Humidity Per City'
)
st.plotly_chart(fig_humidity, use_container_width=True)

# 데이터 업데이트 시간 표시
st.sidebar.write("Last Updated:", latest_data['timestamp'].iloc[0])
