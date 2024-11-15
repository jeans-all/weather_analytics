# 실시간 날씨 모니터링 시스템

## 프로젝트 개요
- OpenWeatherMap API를 활용한 실시간 날씨 데이터 수집
- 한국 주요 도시의 날씨 정보 모니터링
- 데이터 시각화 대시보드 제공

## 주요 기능
- 실시간 날씨 데이터 수집
- 도시별 현재 날씨 현황
- 시계열 기온 변화 그래프
- 습도 분포 차트

## 프로젝트 구조
```bash
 project/
 |-- data/
 |--  |-- weather_data.db   # 수집 데이터
 |-- src/
 |--  |-- main.py           # 데이터 처리
 |--  |-- scheduler.py      # 데이터 수집
 |--  |-- app.py            # 시각화
 |-- tests/
 |-- requirements.txt       # 패키지 목록
 |-- README.md
```

## 설치 방법 및 실행
### 1. 저장소 클론
```bash
   git clone https://github.com/jeans-all/weather_analytics.git
   cd weather_analytics
```   

### 2. 가상환경 생성 및 활성화
``` bash
   python -m venv venv
   source venv/bin/activate
```

### 3. 필요 패키지 설치 
``` bash
   pip install -r requirements.txt
```

### 4. API KEY 설정
https://openweathermap.org 에서 API Key 값을 발급 받은 후 .env 에 저장
   ``` bash
      echo 'OPENWEATHER_API_KEY=your_api_key' > .env      
   ```

### 5. 어플리케이션 실행
``` bash
   # 데이터 수집
   python src/scheduler.py
   
   # 데쉬보드 실행
   streamlit run src/app.py
```

## 기술 스택
- Python
- SQLite
- Streamlit
- Plotly
