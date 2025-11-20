# Personal Health Record Dashboard

## Project Overview
A health data tracking and visualization web app built with Python and Streamlit.  
Users can log daily vitals (BP, Sugar, Pulse), view health trends, and export professional PDF reports.

## Core Features
- Add daily health records  
- View trend charts over time  
- Automatic health insights  
- Export reports to PDF for doctors  
- Smart health recommendations  

## Tech Stack
- **Language:** Python 3.11+  
- **Framework:** Streamlit  
- **Data Handling:** Pandas  
- **Visualization:** Matplotlib / Seaborn  
- **PDF Generation:** FPDF2  

## Project Structure
health-dashboard/
├── main.py # Entry point
├── data/
│ └── health_records.csv # Saved vitals data
├── features/
│ ├── input_form/
│ │ ├── GEMINI.md
│ │ └── input_form.py
│ ├── visualization/
│ │ ├── GEMINI.md
│ │ └── visualization.py
│ ├── analytics/
│ │ ├── GEMINI.md
│ │ └── analytics.py
│ └── reports/
│ ├── GEMINI.md
│ └── reports.py
└── assets/
└── logo.png