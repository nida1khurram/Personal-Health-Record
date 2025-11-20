import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os

def load_data():
    # Get the current username from session state
    username = st.session_state["username"]
    
    # Construct user-specific file path
    user_data_dir = os.path.join("data", username)
    file_path = os.path.join(user_data_dir, "health_records.csv")
    
    # Ensure the user-specific directory exists (though input_form should create it)
    os.makedirs(user_data_dir, exist_ok=True)

    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df.dropna(subset=['date'], inplace=True) # Drop rows where date could not be parsed
            df = df.sort_values(by='date')
            return df
        except pd.errors.EmptyDataError:
            st.warning("No health records found. Please add some data using the 'Input Form'.")
            return pd.DataFrame()
    else:
        # If the file doesn't exist, create an empty one with the correct headers
        pd.DataFrame(columns=['date', 'blood_pressure', 'sugar_level', 'pulse_rate', 'notes']).to_csv(file_path, index=False)
        st.warning("No health records file found. A new one has been created. Please add some data.")
        return pd.DataFrame()

def render_visualization():
    st.header("Health Data Visualization")

    df = load_data()

    if not df.empty:
        st.sidebar.subheader("Filter Data")
        
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()

        start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
        end_date = st.sidebar.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

        filtered_df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]

        if filtered_df.empty:
            st.warning("No data available for the selected date range.")
            return

        st.subheader("Trends Over Time")

        # Blood Pressure
        st.write("#### Blood Pressure")
        bp_df = filtered_df.copy()
        
        # Ensure 'blood_pressure' column is string type and handle potential non-string entries
        bp_df['blood_pressure'] = bp_df['blood_pressure'].astype(str)
        
        # Use a regex to split only valid blood pressure strings (e.g., "120/80")
        # Non-matching entries will result in NaN for systolic and diastolic
        bp_split = bp_df['blood_pressure'].str.extract(r'(\d+)/(\d+)', expand=True)
        bp_df['systolic'] = pd.to_numeric(bp_split[0], errors='coerce')
        bp_df['diastolic'] = pd.to_numeric(bp_split[1], errors='coerce')
        
        # Drop rows where both systolic and diastolic are NaN, as they can't be plotted
        bp_plot_df = bp_df.dropna(subset=['systolic', 'diastolic'])

        if not bp_plot_df.empty:
            fig_bp = px.line(bp_plot_df, x='date', y=['systolic', 'diastolic'], title='Blood Pressure Trend')
            st.plotly_chart(fig_bp, use_container_width=True)
        else:
            st.info("No valid blood pressure data to display for the selected period.")

        # Sugar Level
        st.write("#### Sugar Level")
        fig_sugar = px.line(filtered_df, x='date', y='sugar_level', title='Sugar Level Trend')
        st.plotly_chart(fig_sugar, use_container_width=True)

        # Pulse Rate
        st.write("#### Pulse Rate")
        fig_pulse = px.line(filtered_df, x='date', y='pulse_rate', title='Pulse Rate Trend')
        st.plotly_chart(fig_pulse, use_container_width=True)

        st.subheader("Raw Data")
        st.dataframe(filtered_df)
