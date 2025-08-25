import requests
import pandas as pd

def fetch_air_quality(city, start_date, end_date, token):
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    if data['status'] != 'ok':
        raise ValueError(f"API Error: {data}")
    
    pm25 = pd.DataFrame(data['data']['forecast']['daily']['pm25'])
    pm10 = pd.DataFrame(data['data']['forecast']['daily']['pm10'])
    
    air_df = pd.merge(pm25[['day','avg']], pm10[['day','avg']], on='day')
    air_df.rename(columns={'day':'datetime', 'avg_x':'pm25','avg_y':'pm10'}, inplace=True)
    
    air_df['datetime'] = pd.to_datetime(air_df['datetime'])
    mask = (air_df['datetime'] >= pd.to_datetime(start_date)) & (air_df['datetime'] <= pd.to_datetime(end_date))
    air_df = air_df.loc[mask]
    
    def aqi_category(pm25):
        if pm25 <= 50: return 'Good'
        elif pm25 <= 100: return 'Moderate'
        elif pm25 <= 150: return 'Unhealthy for Sensitive Groups'
        elif pm25 <= 200: return 'Unhealthy'
        elif pm25 <= 300: return 'Very Unhealthy'
        else: return 'Hazardous'
    
    air_df['aqi_category'] = air_df['pm25'].apply(aqi_category)
    
    return air_df
