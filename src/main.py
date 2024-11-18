import os 
import pandas as pd
import requests
import json
import time
import sqlite3

from datetime import datetime
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env

API_KEY = os.environ.get('OPENWEATHER_API_KEY')
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
            'temperature_feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'weather_description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed']
        }
        
        # data['timestamp'] = weather_info['timestamp']
        # data['city'] = weather_info['city']
        # print(weather_info)
        # return (weather_info, data)
        return weather_info
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

# 모든 도시의 데이터 수집
def collect_all_cities():
    all_data = []
    all_fullData = []
    for city in CITIES:
        # (weather_data, fullData) = get_weather_data(city)
        weather_data = get_weather_data(city)
        # print(weather_data)
        if weather_data:
            all_data.append(weather_data)
            # all_fullData.append(fullData)
        time.sleep(1)  # API 호출 제한 고려
    # print(all_data)
    # print()
    # print(all_fullData)
    # return (all_data, all_fullData)
    return all_data

# (weather_data, weather_fullData) = collect_all_cities()
weather_data = collect_all_cities()
# print(json.dumps(weather_data, indent=2))




def process_weather_data(weather_data):
    # JSON 데이터를 DataFrame으로 변환

    print(weather_data)
    print()
    df = pd.DataFrame(weather_data)
    

    # timestamp 컬럼을 datetime 타입으로 변환
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    except:
        print(df)
        print(df.columns)
        exit()

    # 도시명을 인덱스로 설정
    df.set_index('city', inplace=True)
    
    # 컬럼명 한글로 변경 (선택사항)
    # print(df.columns)
    # df.columns = ['측정시각', '기온', '체감기온', '습도', '날씨', '풍속']
    # 소수점 자릿수 조정
    # df['기온'] = df['기온'].round(1)
    # df['풍속'] = df['풍속'].round(1)
    
    return df

def process_weather_dataFull(weather_fullData):
    df = pd.DataFrame(weather_fullData)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('city', inplace = True)
    
    return df


df_weather = process_weather_data(weather_data)
# df_weather_fullData = process_weather_dataFull(weather_fullData)
# print(df_weather_fullData['main'])


def create_database():
    conn = sqlite3.connect('data/weather_data.db')
    cursor = conn.cursor()
    
    query = '''
        CREATE TABLE IF NOT EXISTS weather_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            temperature FLOAT,
            temperature_feels_like, FLOAT,
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
    # print(df_to_save)
    df_to_save.columns = ['city', 'timestamp', 'temperature', 'temperature_feels_like', 'humidity',
                         'weather_description', 'wind_speed']

    # DB에 데이터 저장
    df_to_save.to_sql('weather_records', conn,
                      if_exists='append',
                      index=False)

    conn.close()

# 데이터베이스 저장 실행
save_to_database(df_weather)
# save_to_databaseFull(df_weather_fullData)
# 저장된 데이터 확인
def check_saved_data():
    conn = sqlite3.connect('data/weather_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM weather_records ORDER BY timestamp DESC LIMIT 5")
    rows = cursor.fetchall()

    print("\n최근 저장된 5개 레코드:")
    for row in rows:
        print(row)

    conn.close()

check_saved_data()
