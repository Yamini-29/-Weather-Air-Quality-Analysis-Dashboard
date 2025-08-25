import pandas as pd

def transform_data(weather_df, air_df):

    weather_df['temperature'].fillna(weather_df['temperature'].mean(), inplace=True)
    weather_df['humidity'].fillna(weather_df['humidity'].mean(), inplace=True)
    weather_df['wind_speed'].fillna(weather_df['wind_speed'].mean(), inplace=True)

    air_df['pm25'].fillna(air_df['pm25'].mean(), inplace=True)
    air_df['pm10'].fillna(air_df['pm10'].mean(), inplace=True)

    weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
    air_df['datetime'] = pd.to_datetime(air_df['datetime'])

    merged_df = pd.merge(weather_df, air_df, on='datetime', how='inner')

    T = merged_df['temperature']
    RH = merged_df['humidity']
    W = merged_df['wind_speed']
    merged_df['feels_like'] = T + 0.33*RH - 0.7*W - 4.0

    return merged_df
