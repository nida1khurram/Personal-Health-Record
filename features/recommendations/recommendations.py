import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import re

def load_data():
    # Get the current username from session state
    username = st.session_state["username"]
    
    # Construct user-specific file path
    user_data_dir = os.path.join("data", username)
    file_path = os.path.join(user_data_dir, "health_records.csv")
    
    # Ensure the user-specific directory exists (though input_form should create it)
    os.makedirs(user_data_dir, exist_ok=True)
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            df = pd.read_csv(file_path)
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df.dropna(subset=['date'], inplace=True) # Drop rows where date could not be parsed
            df = df.sort_values(by='date')
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    else:
        pd.DataFrame(columns=['date', 'blood_pressure', 'sugar_level', 'pulse_rate', 'notes']).to_csv(file_path, index=False)
        return pd.DataFrame()

def get_recent_data(df, days=30):
    if df.empty:
        return pd.DataFrame()
    latest_date = df['date'].max()
    start_date = latest_date - timedelta(days=days)
    return df[df['date'] >= start_date]

def generate_daily_recommendation(row):
    recs = []
    
    # Blood Pressure
    bp = row['blood_pressure']
    if isinstance(bp, str):
        match = re.match(r'(\d+)/(\d+)', bp)
        if match:
            systolic, diastolic = int(match.group(1)), int(match.group(2))
            bp_val = f"{systolic}/{diastolic} mmHg"
            if systolic > 130 or diastolic > 85:
                recs.append(f"BP ({bp_val}) is high.")
            elif systolic < 90 or diastolic < 60:
                recs.append(f"BP ({bp_val}) is low.")
            else:
                recs.append(f"BP ({bp_val}) is healthy.")
        else:
            recs.append("BP data format invalid.")
    else:
        recs.append("BP data missing.")
    
    # Sugar Level
    sugar = row['sugar_level']
    if pd.notna(sugar):
        sugar_val = f"{sugar:.0f} mg/dL"
        if sugar > 140:
            recs.append(f"Sugar ({sugar_val}) is high.")
        elif sugar < 70:
            recs.append(f"Sugar ({sugar_val}) is low.")
        else:
            recs.append(f"Sugar ({sugar_val}) is healthy.")
    else:
        recs.append("Sugar data missing.")

    # Pulse Rate
    pulse = row['pulse_rate']
    if pd.notna(pulse):
        pulse_val = f"{pulse:.0f} bpm"
        if pulse > 100:
            recs.append(f"Pulse ({pulse_val}) is high.")
        elif pulse < 60:
            recs.append(f"Pulse ({pulse_val}) is low.")
        else:
            recs.append(f"Pulse ({pulse_val}) is healthy.")
    else:
        recs.append("Pulse data missing.")

    if all("healthy" in rec.lower() for rec in recs if "data missing" not in rec.lower() and "data format invalid" not in rec.lower()):
        return "All recorded metrics are within the healthy range. Keep it up!"
    
    return " ".join(recs)

def generate_recommendations_text(df):
    if df.empty:
        return ["Not enough recent data to generate specific recommendations."]

    # For overall summary, we still use averages
    recommendations = []
    df['blood_pressure'] = df['blood_pressure'].astype(str)
    bp_split = df['blood_pressure'].str.extract(r'(\d+)/(\d+)', expand=True)
    df['systolic'] = pd.to_numeric(bp_split[0], errors='coerce')
    df['diastolic'] = pd.to_numeric(bp_split[1], errors='coerce')

    # Blood Pressure Recommendations
    if not df['systolic'].dropna().empty:
        avg_systolic = df['systolic'].mean()
        avg_diastolic = df['diastolic'].mean()
        bp_rec = f"Avg BP ({avg_systolic:.0f}/{avg_diastolic:.0f}): "
        if avg_systolic > 130 or avg_diastolic > 85:
            bp_rec += "Elevated. Consider reducing sodium and consulting your doctor."
        elif avg_systolic < 90 or avg_diastolic < 60:
            bp_rec += "Low. Ensure hydration and discuss with your doctor if symptomatic."
        else:
            bp_rec += "Healthy range."
        recommendations.append(bp_rec)

    # Other metrics can be added here if needed for summary
    return recommendations

def render_recommendations():
    st.header("Smart Health Recommendations")
    df = load_data()

    if df.empty:
        st.info("No health records found. Add data to get recommendations.")
        return

    st.subheader("Recommendations based on your last 30 days")
    recent_df = get_recent_data(df, days=30)
    
    # We can show both a summary and daily highlights
    summary_recs = generate_recommendations_text(recent_df.copy())
    st.write("#### Overall Summary:")
    for rec in summary_recs:
        if "Elevated" in rec or "High" in rec:
            st.warning(rec)
        elif "Low" in rec:
            st.info(rec)
        else:
            st.success(rec)

    st.write("#### Daily Highlights:")
    # Show recommendations for the last 5 days as highlights
    daily_highlights_df = recent_df.tail(5)
    if daily_highlights_df.empty:
        st.write("No recent entries for daily highlights.")
    else:
        for _, row in daily_highlights_df.iterrows():
            daily_rec = generate_daily_recommendation(row)
            date_str = row['date'].strftime('%Y-%m-%d')
            st.write(f"**{date_str}:** {daily_rec}")

    st.markdown("---")
    st.info("These recommendations are for informational purposes only.")

