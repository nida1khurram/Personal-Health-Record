# Day 3: Health Data Visualization

## Goal
Visualize daily health data to identify trends and patterns.

## Learning Focus
- Data loading and preprocessing with Pandas
- Streamlit charting components
- Interactive data display

## Features
1. Load data from `data/health_records.csv`.
2. Display line charts for:
    - Blood Pressure (Systolic and Diastolic)
    - Sugar Level
    - Pulse Rate
3. Allow selection of date range for visualization.
4. Display a table of the raw data.

## Streamlit Components
- `st.line_chart()`
- `st.selectbox()`
- `st.date_input()`
- `st.dataframe()`

## Success Criteria
✅ Charts display correctly for selected metrics.
✅ Date range filtering works.
✅ Raw data table is visible.
✅ User-friendly interface for visualization.