# Day 5: Health Report Generation

## Goal
Generate professional PDF reports summarizing the user's health data.

## Learning Focus
- PDF generation with `fpdf2`
- Integrating data and visualizations into a PDF
- Streamlit download functionality

## Features
1. Load data from `data/health_records.csv`.
2. Allow selection of a date range for the report.
3. Generate a PDF report that includes:
    - Patient information (if available, or a generic placeholder)
    - Summary of key health metrics (e.g., average BP, sugar, pulse for the period)
    - A table of the raw data for the selected period.
    - (Optional, for later) Embed simple charts or trends.
4. Provide a download button for the generated PDF.

## Streamlit Components
- `st.button()`
- `st.download_button()`
- `st.date_input()`

## External Libraries
- `fpdf2`

## Success Criteria
✅ PDF report is generated with selected data.
✅ Report includes a summary and raw data.
✅ PDF is downloadable.
✅ Report is well-formatted and professional-looking.