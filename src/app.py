import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 기본 설정
st.set_page_config(
    page_title="Weather Monitoring Dashboard",
    layout="wide"
)

# 제목
st.title("Real Time Weather Monitoring Dashboard")

# DB에서 최신 데이터 조회
def get_latest_weather():
    conn = sqlite3.connect('data/weather_data.db')
    query = """
    SELECT city, temperature, temperature_feels_like, humidity, weather_description, wind_speed, timestamp  
    FROM weather_records  
    WHERE (city, timestamp) IN (SELECT city, MAX(timestamp) FROM weather_records GROUP BY city)
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 최근 24시간 데이터 조회
def get_historical_data():
    conn = sqlite3.connect('data/weather_data.db')
    query = """
    SELECT city, temperature, temperature_feels_like, humidity, timestamp, wind_speed
    FROM weather_records
    WHERE timestamp >= datetime('now', '-1 day')
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    # print(df)
    return df



# 최신 데이터 표시
latest_data = get_latest_weather()

# 도시별 현재 날씨 카드 표시
st.subheader("Current Weather Status", anchor="Section-1")
cols = st.columns(len(latest_data))
for idx, (_, row) in enumerate(latest_data.iterrows()):
    with cols[idx]:
        st.metric(
            label=row['city'],
            value=f"{row['temperature']}°C",
            delta=f"Humidity {row['humidity']}%"
        )
        st.write(f"Weather: {row['weather_description']}")
        st.write(f"Wind speed: {row['wind_speed']}m/s")


# 실제 온도 vs 체감 온도
st.subheader("Real Temperature vs Perceived Temperature", anchor="Section-2")
fig_feeling = go.Figure()
fig_feeling.add_trace(go.Bar(
    x=latest_data["city"], 
    y=latest_data["temperature"], 
    name="Real Temperature",
    marker=dict(
        color=latest_data['temperature'],
        colorscale='sunset_r',
        showscale=True,
        cmin=-10,
        cmax=10, 
        colorbar=dict(
            title="Temperature", 
            len=0.8,
            y = 0.38
        ) 
    )
    )
)
fig_feeling.add_trace(go.Bar(
    x=latest_data["city"], 
    y=latest_data["temperature_feels_like"], 
    name="Perceived Temperature", 
    marker=dict(
        color=latest_data['temperature_feels_like'],
        colorscale='sunset_r',
        cmin=-10,
        cmax=10,
        colorbar=dict(
            title="Temperature_feels_like", 
            len=0.8,
            y = 0.38
        ) 
    ))
)
fig_feeling.update_layout(barmode="group")

st.plotly_chart(fig_feeling, use_container_width=True)

# 시계열 그래프
st.subheader("Temperature Changes Over Time in Cities", anchor="Section-3")
historical_data = get_historical_data()
print(historical_data)
# exit()
fig = px.line(
    historical_data,
    x='timestamp',
    y='temperature',
    color='city'
    # title='Temperature Change in Cities'
)
st.plotly_chart(fig, use_container_width=True)


# 습도와 풍속과의 관계
st.subheader("Relation Between Humidity and Temperature", anchor="Section-4")
fig_scatter = px.scatter(historical_data.sort_values('humidity'), x="humidity", y="wind_speed", color="temperature", 
                         size="temperature", hover_data=["city"], labels={"humidity": "습도 (%)", "wind_speed": "풍속 (m/s)"})
st.plotly_chart(fig_scatter, use_container_width=True)


# 습도 분포 그래프
st.subheader("Current Humidity Distribution", anchor="Section-5")
fig_humidity = px.bar(
    latest_data,
    x='city',
    y='humidity',
    color = 'humidity',
    color_continuous_scale='bluyl',
    range_color = [0, 100],
    title='Humidity Per City'
)
st.plotly_chart(fig_humidity, use_container_width=True)


# sidebar 
st.sidebar.title("Contents")
st.sidebar.markdown("""
<ul>
    <li><a href='#Section-1'> Current Weather Status </a></li>
    <li><a href='#Section-2'> Real Temperature vs Perceived Temperature </a></li>
    <li><a href='#Section-3'> Temperature Changes Over Time in Cities </a></li>
    <li><a href='#Section-4'> Relation Between Humidity and Temperature </a></li>
    <li><a href='#Section-5'> Current Humidity Distribution </a></li>
</ul>
""", unsafe_allow_html=True)

st.sidebar.header("Information")
st.sidebar.metric("Last updated:", latest_data['timestamp'].iloc[0])

hottest = latest_data.loc[latest_data["temperature"] == latest_data["temperature"].max(), 'city'].iloc[0]
coolest = latest_data.loc[latest_data["temperature"] == latest_data["temperature"].min(), 'city'].iloc[0]
st.sidebar.metric("Hottest City", f'{hottest} at {latest_data["temperature"].max()}')
st.sidebar.metric("Coldest City", f'{coolest} at {latest_data["temperature"].min()}')
