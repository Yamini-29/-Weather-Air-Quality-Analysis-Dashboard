import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from main import run_pipeline

st.set_page_config(page_title="Weather + Air Quality Analysis", layout="wide")
st.title("🌤️ Weather + Air Quality Analysis Dashboard")

city = st.text_input("Enter City:")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Run Analysis"):
    if city:
        with st.spinner("Fetching data and running pipeline..."):
            merged_df, daily_avg, corr_matrix = run_pipeline(city, str(start_date), str(end_date))
        
        st.success(f"Pipeline completed! Showing results for {city} from {start_date} to {end_date}.")

        st.subheader("📊 Daily Average Temperature & Air Quality")
        st.dataframe(daily_avg)

        fig, ax = plt.subplots(figsize=(10,5))
        daily_avg.plot(x='datetime', y=['temperature','pm25','pm10'], kind='line', marker='o', ax=ax)
        ax.set_title("Daily Temperature & Air Quality (PM2.5 & PM10)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Values")
        st.pyplot(fig)

        st.subheader("🔗 Correlation Between Weather & Air Quality Metrics")
        fig2, ax2 = plt.subplots(figsize=(8,6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax2)
        st.pyplot(fig2)

        if st.checkbox("Show Full Merged DataFrame"):
            st.dataframe(merged_df)
    else:
        st.error("Please enter a city name to run the analysis.")
