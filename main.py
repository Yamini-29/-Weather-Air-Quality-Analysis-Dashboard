import os
from dotenv import load_dotenv
import pandas as pd
from weather_extract import fetch_weather_data
from aqi_extract import fetch_air_quality
from transform import transform_data
from load import load_to_postgres
from sqlalchemy import create_engine

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
AIR_API_KEY = os.getenv("AIR_API_KEY")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

def run_pipeline(city: str, start_date: str, end_date: str):

    weather_df = fetch_weather_data(city, start_date, end_date, WEATHER_API_KEY)
    air_df = fetch_air_quality(city, start_date, end_date, AIR_API_KEY)

    merged_df = transform_data(weather_df, air_df)

    load_to_postgres(weather_df, air_df, merged_df, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    daily_avg = merged_df.groupby('datetime')[['temperature','pm25','pm10']].mean().reset_index()
    corr_matrix = merged_df[['temperature','humidity','wind_speed','pm25','pm10']].corr()

    return merged_df, daily_avg, corr_matrix

def fetch_merged_from_db():

    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    df = pd.read_sql("SELECT * FROM merged_data", engine)
    return df
