from sqlalchemy import create_engine

def load_to_postgres(weather_df, air_df, merged_df, db_user, db_password, db_host, db_port, db_name):

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    weather_df.to_sql('weather', engine, if_exists='replace', index=False)
    air_df.to_sql('air_quality', engine, if_exists='replace', index=False)
    merged_df.to_sql('merged_data', engine, if_exists='replace', index=False)

    print("Data loaded into PostgreSQL successfully!")
