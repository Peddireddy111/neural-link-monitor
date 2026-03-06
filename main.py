import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# --- THE COORDINATE SWITCHBOARD ---
# Uncomment (remove the #) for the city you want to analyze
CITIES = {
    "Paris": {"lat": 48.85, "lon": 2.35},
    "London": {"lat": 51.50, "lon": -0.12},
    "New York": {"lat": 40.71, "lon": -74.00},
    "Tokyo": {"lat": 35.68, "lon": 139.65},
    "Mumbai": {"lat": 19.07, "lon": 72.87},
    "Pulivendula": {"lat": 14.422232, "lon": 78.226341}
}

# CHANGE THIS to any city name in the list above
SELECTED_CITY = "Pulivendula" 
LAT = CITIES[SELECTED_CITY]["lat"]
LON = CITIES[SELECTED_CITY]["lon"]

# 1. Calculate dates for the past 7 days
today = datetime.now()
week_ago = today - timedelta(days=7)
start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

# 2. Get weather data from Open-Meteo API
print(f"CONNECTING TO NEURAL BRIDGE... ANALYZING: {SELECTED_CITY}")
url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"

try:
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()

    # 3. Process with pandas
    df = pd.DataFrame({
        'date': pd.to_datetime(data['daily']['time']),
        'max_temp': data['daily']['temperature_2m_max'],
        'min_temp': data['daily']['temperature_2m_min']
    })

    # 4. Calculate average
    df['avg_temp'] = (df['max_temp'] + df['min_temp']) / 2

    # 5. Create visualization
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['max_temp'], 'r-o', label='Max Temp')
    plt.plot(df['date'], df['min_temp'], 'b-o', label='Min Temp')
    plt.plot(df['date'], df['avg_temp'], 'g--', label='Average')

    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f'{SELECTED_CITY} Weather Analysis - Past Week')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 6. Save results locally
    if not os.path.exists('data'):
        os.makedirs('data')
    
    filename_base = SELECTED_CITY.lower().replace(" ", "_")
    plt.savefig(f'data/{filename_base}_chart.png')
    df.to_csv(f'data/{filename_base}_weather.csv', index=False)

    print(f"\n--- {SELECTED_CITY.upper()} ANALYSIS COMPLETE ---")
    print(df)
    print(f"\nAverage temperature: {df['avg_temp'].mean():.1f}°C")
    print(f"Files saved in 'data/' as {filename_base}_weather.csv")
    
    # Keep the window open
    plt.show()

except Exception as e:
    print(f"LINK FAILURE: {e}")