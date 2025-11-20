import streamlit as st
import pandas as pd
from datetime import datetime
import os

def render_input_form():
    st.header("Daily Health Data Entry")

    with st.form(key='health_input_form'):
        entry_date = st.date_input("Date", datetime.now())
        entry_time = st.time_input("Time", datetime.now().time())
        
        # Combine date and time
        entry_datetime = datetime.combine(entry_date, entry_time)
        
        st.subheader("Blood Pressure")
        col1, col2 = st.columns(2)
        with col1:
            systolic_bp = st.number_input("Systolic (mmHg)", min_value=0, max_value=300, value=120)
        with col2:
            diastolic_bp = st.number_input("Diastolic (mmHg)", min_value=0, max_value=200, value=80)
        
        sugar_level = st.number_input("Sugar Level (mg/dL)", min_value=0)
        pulse_rate = st.number_input("Pulse Rate (bpm)", min_value=0)
        notes = st.text_area("Notes")

        submit_button = st.form_submit_button(label='Save Record')

        if submit_button:
            if not all([entry_date, systolic_bp, diastolic_bp, sugar_level, pulse_rate]):
                st.error("Please fill all required fields.")
            else:
                blood_pressure_combined = f"{systolic_bp}/{diastolic_bp}"
                new_record = {
                    "date": [entry_datetime],
                    "blood_pressure": [blood_pressure_combined],
                    "sugar_level": [sugar_level],
                    "pulse_rate": [pulse_rate],
                    "notes": [notes]
                }
                new_df = pd.DataFrame(new_record)

                # Get the current username from session state
                username = st.session_state["username"]
                
                # Construct user-specific file path
                user_data_dir = os.path.join("data", username)
                file_path = os.path.join(user_data_dir, "health_records.csv")
                
                # Ensure the user-specific directory exists
                os.makedirs(user_data_dir, exist_ok=True)
                
                if os.path.exists(file_path):
                    try:
                        existing_df = pd.read_csv(file_path)
                        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                    except pd.errors.EmptyDataError:
                        updated_df = new_df
                else:
                    updated_df = new_df
                
                updated_df.to_csv(file_path, index=False)
                st.success("Health record saved successfully!")
