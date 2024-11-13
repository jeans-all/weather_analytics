import requests
import json
from datetime import datetime
import time


API_KEY = "364f04d5b65445901ca5805d4436638f"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

CITIES = [
    "Seoul,KR",
    "Busan,KR",
    "Incheon,KR",
    "Daegu,KR",
    "Daejeon,KR",
    "Gwangju,KR"
] 


def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # 섭씨온도 사용
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # 필요한 데이터만 추출
        weather_info = {
            'city': city.split(',')[0],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather_description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed']
        }
        return weather_info
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

# 모든 도시의 데이터 수집
def collect_all_cities():
    all_data = []
    for city in CITIES:
        weather_data = get_weather_data(city)
        if weather_data:
            all_data.append(weather_data)
        time.sleep(1)  # API 호출 제한 고려
    return all_data

weather_data = collect_all_cities()
# print(json.dumps(weather_data, indent=2))



import pandas as pd

def process_weather_data(weather_data):
    # JSON 데이터를 DataFrame으로 변환
    df = pd.DataFrame(weather_data)
    
    # timestamp 컬럼을 datetime 타입으로 변환
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 도시명을 인덱스로 설정
    df.set_index('city', inplace=True)
    
    # 컬럼명 한글로 변경 (선택사항)
    df.columns = ['측정시각', '기온', '습도', '날씨', '풍속']
    
    # 소수점 자릿수 조정
    df['기온'] = df['기온'].round(1)
    df['풍속'] = df['풍속'].round(1)
    
    return df

df_weather = process_weather_data(weather_data)
# print(df_weather)

import sqlite3

def create_database():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    query = '''
        CREATE TABLE IF NOT EXISTS weather_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            temperature FLOAT,
            humidity INTEGER,
            weather_description TEXT,
            wind_speed FLOAT
        )
    '''

    cursor.execute(query)

    conn.commit()
    return conn

def save_to_database(df):
    conn = create_database()

    # DataFrame을 SQLite DB에 저장
    # 한글 컬럼명을 다시 영어로 변환
    df_to_save = df.reset_index()
    df_to_save.columns = ['city', 'timestamp', 'temperature', 'humidity',
                         'weather_description', 'wind_speed']

    # DB에 데이터 저장
    df_to_save.to_sql('weather_records', conn,
                      if_exists='append',
                      index=False)

    conn.close()

# 데이터베이스 저장 실행
save_to_database(df_weather)

# 저장된 데이터 확인
def check_saved_data():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM weather_records ORDER BY timestamp DESC LIMIT 5")
    rows = cursor.fetchall()

    print("\n최근 저장된 5개 레코드:")
    for row in rows:
        print(row)

    conn.close()

check_saved_data()
