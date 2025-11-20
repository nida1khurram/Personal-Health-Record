import streamlit as st
import pandas as pd
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

def render_analytics():
    st.header("Health Analytics")

    df = load_data()

    if not df.empty:
        st.subheader("Key Statistics")

        # Convert blood pressure to numeric for statistics
        # Ensure 'blood_pressure' column is string type and handle potential non-string entries
        df['blood_pressure'] = df['blood_pressure'].astype(str)
        
        # Use a regex to split only valid blood pressure strings (e.g., "120/80")
        # Non-matching entries will result in NaN for systolic and diastolic
        bp_split = df['blood_pressure'].str.extract(r'(\d+)/(\d+)', expand=True)
        df['systolic'] = pd.to_numeric(bp_split[0], errors='coerce')
        df['diastolic'] = pd.to_numeric(bp_split[1], errors='coerce')

        metrics = {
            "Sugar Level (mg/dL)": df['sugar_level'],
            "Pulse Rate (bpm)": df['pulse_rate'],
            "Systolic BP": df['systolic'],
            "Diastolic BP": df['diastolic']
        }

        for name, series in metrics.items():
            if not series.dropna().empty:
                st.write(f"#### {name}")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Mean", f"{series.mean():.2f}")
                col2.metric("Median", f"{series.median():.2f}")
                col3.metric("Min", f"{series.min():.2f}")
                col4.metric("Max", f"{series.max():.2f}")
            else:
                st.write(f"#### {name}")
                st.info("No data available for this metric.")

        st.subheader("Normal Health Ranges (General Guidelines)")
        st.write("Blood Sugar: 70 - 100 mg/dL (Fasting)")
        st.write("Pulse Rate: 60 - 100 bpm (At rest)")
        st.write("Blood Pressure: Less than 120/80 mmHg (Ideal)")

        st.subheader("Body Mass Index (BMI) Calculation")
        height_m = st.number_input("Enter your height in meters:", min_value=0.0, format="%.2f", key="bmi_height")
        weight_kg = st.number_input("Enter your weight in kilograms:", min_value=0.0, format="%.2f", key="bmi_weight")
        
        if st.button("Calculate BMI", key="calculate_bmi_button"):
            if height_m > 0 and weight_kg > 0:
                bmi = weight_kg / (height_m ** 2)
                st.metric(label="Your BMI is", value=f"{bmi:.2f}")
                if bmi < 18.5:
                    st.warning("Underweight: Consider consulting a healthcare professional for advice on healthy weight gain.")
                elif 18.5 <= bmi < 25:
                    st.success("Normal weight: Keep up the good work!")
                elif 25 <= bmi < 30:
                    st.warning("Overweight: Consider a balanced diet and regular exercise.")
                else:
                    st.error("Obesity: It is recommended to consult a healthcare professional for a personalized plan.")
            else:
                st.error("Please enter valid height and weight.")

        st.subheader("Out-of-Range Values (Basic Check)")
        st.write("This section highlights values that might be outside typical healthy ranges. Consult a doctor for accurate interpretation.")

        # Define some arbitrary healthy ranges for demonstration
        # These should ideally come from medical guidelines or user-defined preferences
        healthy_ranges = {
            'sugar_level': {'min': 70, 'max': 140}, # mg/dL
            'pulse_rate': {'min': 60, 'max': 100}, # bpm
            'systolic': {'min': 90, 'max': 120}, # mmHg
            'diastolic': {'min': 60, 'max': 80} # mmHg
        }

        out_of_range_found = False
        for col, ranges in healthy_ranges.items():
            if col in df.columns and not df[col].dropna().empty:
                outliers = df[(df[col] < ranges['min']) | (df[col] > ranges['max'])]
                if not outliers.empty:
                    st.write(f"##### {col.replace('_', ' ').title()} Outliers:")
                    st.dataframe(outliers[['date', col]])
                    out_of_range_found = True
        
        if not out_of_range_found:
            st.info("No significant out-of-range values detected based on basic checks.")

    else:
        st.info("No data available for analytics. Please add some health records first.")
