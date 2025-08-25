import requests
import pandas as pd

def fetch_weather_data(city, start_date, end_date, api_key):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}?unitGroup=metric&key={api_key}&contentType=json"
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()
    
    weather_df = pd.json_normalize(data, record_path=['days'])
    weather_df = weather_df[['datetime', 'temp', 'humidity', 'windspeed', 'conditions']]
    weather_df.rename(columns={'temp':'temperature', 'windspeed':'wind_speed'}, inplace=True)
    
    T = weather_df['temperature']
    RH = weather_df['humidity']
    weather_df['feels_like'] = T + 0.33*RH - 0.7*weather_df['wind_speed'] - 4.0
    
    return weather_df
