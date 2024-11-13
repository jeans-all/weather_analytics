import schedule
import time
from main import collect_all_cities
from data_processing import process_weather_data
from database import save_to_database

def job():
    weather_data = collect_all_cities()
    df_weather = process_weather_data(weather_data)
    save_to_database(df_weather)
    print(f"Data collected at {time.strftime('%Y-%m-%d %H:%M:%S')}")

# 15분마다 데이터 수집
schedule.every(15).minutes.do(job)

if __name__ == "__main__":
    print("Weather data collection started...")
    while True:
        schedule.run_pending()
        time.sleep(1)
