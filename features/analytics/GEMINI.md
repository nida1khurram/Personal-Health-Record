# Day 4: Health Data Analytics

## Goal
Provide analytical insights and key statistics from the recorded health data.

## Learning Focus
- Data aggregation and statistical analysis with Pandas
- Conditional logic for health recommendations
- Displaying metrics and summaries in Streamlit

## Features
1. Load data from `data/health_records.csv`.
2. Display key statistics (mean, median, min, max) for Blood Pressure, Sugar Level, and Pulse Rate.
3. Implement Body Mass Index (BMI) calculation based on user input (height, weight).
4. Provide basic health recommendations based on BMI.
5. Identify and highlight any out-of-range values for BP, Sugar, or Pulse.

## Streamlit Components
- `st.metric()`
- `st.dataframe()`
- `st.write()` for text-based insights
- `st.expander()` for detailed statistics

## Success Criteria
✅ Key statistics are accurately calculated and displayed.
✅ BMI calculation is functional and provides recommendations.
✅ Out-of-range values are flagged.
✅ Analytics are clear and easy to understand.