# Real-time Weather Monitoring System

## About the Project
- Collect weather data using OpenWeatherMap API
- Monitor weathers in major cities in Korea
- Provide data visualization on dashboard

## Key Features
- Real-time data collection
- Current weather status per city
- Time-series graph of change in temperature
- Humidity distribution chart

## Project Structure
```bash
 project/
 |-- data/
 |--  |-- weather_data.db   # Collected data
 |-- src/
 |--  |-- main.py           # Processing data
 |--  |-- scheduler.py      # Collecting data
 |--  |-- app.py            # Visualizing data
 |-- tests/
 |-- requirements.txt       # List of dependent packages
 |-- README.md
```

## How to Install & Run the Project
### 1. Clone the repository
```bash
   git clone https://github.com/jeans-all/weather_analytics.git
   cd weather_analytics
```   

### 2. Create and activate a python virtual environment
``` bash
   python -m venv venv
   source venv/bin/activate
```

### 3. Install dependent packages
``` bash
   pip install -r requirements.txt
```

### 4. Set up API key
Register in https://openweathermap.org and then write the issued API key into file '.env' 
   ``` bash
      echo 'OPENWEATHER_API_KEY=your_api_key' > .env      
   ```

### 5. Run the Application
``` bash
   # Collect data (Every 15 minutes) 
   python src/scheduler.py

   # Open the dashboard
   streamlit run src/app.py
```

## Technology Stack
- Python
- SQLite
- Streamlit
- Plotly
