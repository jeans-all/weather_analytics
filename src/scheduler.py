import schedule
import time
from main import save_to_database, process_weather_data, collect_all_cities

def job():
    weather_data = collect_all_cities()
    df_weather = process_weather_data(weather_data)
    save_to_database(df_weather)
    print(f"Data collected at {time.strftime('%Y-%m-%d %H:%M:%S')}")

# 15분마다 데이터 수집
schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    print("Weather data collection started...")
    while True:
        schedule.run_pending()
        time.sleep(1)
