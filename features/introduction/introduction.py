import streamlit as st

def render_introduction():
    st.header("🩺 Personal Health Record Dashboard — Your Digital Health Partner")
    st.write("""
        Take control of your health like never before!
        The Personal Health Record Dashboard is an intelligent health-tracking web app built with Python + Streamlit that helps you monitor, understand, and improve your health every single day.

        Record your Blood Pressure, Sugar Level, and Pulse Rate with just a few clicks — and instantly see your progress through beautiful charts, smart insights, and PDF health reports ready to share with your doctor.
    """)

    st.subheader("🌟 Key Features:")
    st.markdown("""
    -   **🧠 Smart Health Insights:** Get automatic alerts for abnormal readings.
    -   **📊 Visual Health Trends:** See your progress in interactive graphs.
    -   **🩸 Easy Data Entry:** Log your daily vitals in seconds.
    -   **📄 Export to PDF:** Generate professional reports for doctor visits.
    -   **💬 Smart Recommendations:** Personalized tips for better health.
    -   **☁️ No Setup Needed:** Runs instantly on any browser via Streamlit.
    """)

    st.subheader("💡 Why People Love It")
    st.write("""
        Unlike typical fitness apps, this dashboard gives real medical tracking power with clarity and control — making it perfect for:
        -   Diabetic or hypertension patients
        -   Families tracking elders’ health
        -   Clinics and health consultants
        -   Wellness coaches
    """)

    st.write("""
        Stay informed. Stay healthy.
        Transform your daily health data into a smart digital health diary — beautifully designed, medically useful, and easy to use.
    """)

    st.subheader("📊 Example Health Scenarios:")

    st.markdown("""
    **🩷 Example 1: Normal & Healthy Day**
    | Vital           | Reading         | Status      |
    | :-------------- | :-------------- | :---------- |
    | Blood Pressure  | 118 / 78 mmHg   | ✅ Normal   |
    | Pulse Rate      | 76 bpm          | ✅ Normal   |
    | Sugar Level     | 92 mg/dL        | ✅ Normal   |
    Notes: Slept well, light breakfast, morning walk done.
    """)

    st.markdown("""
    **💛 Example 2: Slightly High Sugar (After Lunch)**
    | Vital           | Reading         | Status          |
    | :-------------- | :-------------- | :-------------- |
    | Blood Pressure  | 125 / 82 mmHg   | ✅ Normal       |
    | Pulse Rate      | 84 bpm          | ✅ Normal       |
    | Sugar Level     | 148 mg/dL       | ⚠️ Slightly High |
    Notes: Had rice in lunch, plan evening walk.
    """)

    st.markdown("""
    **💜 Example 3: Mild Stress Day**
    | Vital           | Reading         | Status            |
    | :-------------- | :-------------- | :---------------- |
    | Blood Pressure  | 135 / 88 mmHg   | ⚠️ Mildly Elevated |
    | Pulse Rate      | 92 bpm          | ⚠️ Slightly High   |
    | Sugar Level     | 98 mg/dL        | ✅ Normal         |
    Notes: Slept late, felt stressed at work, skipped exercise.
    """)

    st.info("Your health data is stored locally on your system and is not shared externally.")
    st.markdown("---")
    st.write("Built with ❤️ by Nida Khurram")