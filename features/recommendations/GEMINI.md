# Day 6: Smart Health Recommendations

## Goal
Provide personalized, data-driven health recommendations based on the user's recorded health data.

## Learning Focus
- Data analysis for pattern recognition
- Rule-based recommendation system
- Displaying actionable advice in Streamlit

## Features
1. Load data from `data/health_records.csv`.
2. Analyze recent trends (e.g., last 7 or 30 days) for Blood Pressure, Sugar Level, and Pulse Rate.
3. Implement rule-based recommendations:
    - **Blood Pressure:** If consistently high/low, suggest consulting a doctor, stress reduction, or dietary changes.
    - **Sugar Level:** If consistently high/low or erratic, suggest dietary adjustments, exercise, or medical consultation.
    - **Pulse Rate:** If consistently high/low, suggest exercise, relaxation techniques, or medical check-up.
    - **General:** Encourage consistent data entry.
4. Display recommendations clearly and concisely.

## Streamlit Components
- `st.expander()` for detailed recommendations
- `st.info()`, `st.warning()`, `st.success()` for different types of advice
- `st.write()` for general text

## Success Criteria
✅ Recommendations are relevant to the user's data.
✅ Advice is actionable and easy to understand.
✅ Different types of recommendations are provided based on data patterns.
✅ Encourages healthy habits and medical consultation when necessary.