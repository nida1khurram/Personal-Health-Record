import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import os
from features.recommendations.recommendations import generate_daily_recommendation

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

class PDF(FPDF):
    def __init__(self, username=None):
        super().__init__()
        self.username = username

    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Personal Health Record Report', 0, 1, 'C')
        if self.username:
            self.set_font('Arial', '', 10)
            self.cell(0, 5, f'Report for: {self.username}', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln(5)

    def add_dataframe_as_table(self, df_to_print):
        # Use a smaller font for the table
        self.set_font('Arial', '', 8)
        
        # Set column widths to fit landscape page (approx. 277mm available)
        col_widths = {
            'date': 40, # Increased width for datetime
            'blood_pressure': 25,
            'sugar_level': 25,
            'pulse_rate': 25,
            'notes': 55,
            'recommendation': 105 # Adjusted to fit total width
        }
        
        # --- Table Header ---
        self.set_font('Arial', 'B', 9)
        header_labels = [h.replace('_', ' ').title() for h in df_to_print.columns]
        for i, header in enumerate(header_labels):
            self.cell(col_widths[df_to_print.columns[i]], 10, header, 1, 0, 'C')
        self.ln()

        # --- Table Body ---
        self.set_font('Arial', '', 8)
        for _, row in df_to_print.iterrows():
            # Use a fixed height for all cells in a row
            cell_height = 10
            
            # Truncate long text to prevent overflow
            notes = str(row['notes'])
            if len(notes) > 35: # Approx char limit for notes width
                notes = notes[:32] + '...'

            recommendation = str(row['recommendation'])
            if len(recommendation) > 80: # Approx char limit for recommendation width
                recommendation = recommendation[:77] + '...'

            # Create a dictionary of the potentially truncated values
            row_values = {
                'date': row['date'].strftime('%Y-%m-%d %H:%M:%S'), # Format date to include time
                'blood_pressure': str(row['blood_pressure']),
                'sugar_level': str(row['sugar_level']),
                'pulse_rate': str(row['pulse_rate']),
                'notes': notes,
                'recommendation': recommendation
            }

            for col_name in df_to_print.columns:
                self.cell(col_widths[col_name], cell_height, row_values[col_name], 1, 0, 'L')
            
            self.ln()
        self.ln(10)

def render_reports():
    st.header("Generate Health Reports")
    df = load_data()

    if df.empty:
        st.info("No data available to generate reports. Please add some health records first.")
        return

    st.subheader("Select Date Range for Report")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

    filtered_df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)].copy()

    if filtered_df.empty:
        st.warning("No data available for the selected date range to generate a report.")
        return

    if st.button("Generate PDF Report"):
        username = st.session_state["username"]
        pdf = PDF(username=username)
        pdf.alias_nb_pages()
        pdf.add_page(orientation='L') # Use landscape for more space

        # --- Summary Section ---
        pdf.chapter_title("Summary of Health Metrics")
        summary_text = f"Report Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        summary_text += f"Data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n\n"
        
        bp_split = filtered_df['blood_pressure'].astype(str).str.extract(r'(\d+)/(\d+)', expand=True)
        filtered_df['systolic'] = pd.to_numeric(bp_split[0], errors='coerce')
        filtered_df['diastolic'] = pd.to_numeric(bp_split[1], errors='coerce')

        if not filtered_df['sugar_level'].dropna().empty:
            summary_text += f"Average Sugar Level: {filtered_df['sugar_level'].mean():.2f} mg/dL\n"
        if not filtered_df['pulse_rate'].dropna().empty:
            summary_text += f"Average Pulse Rate: {filtered_df['pulse_rate'].mean():.2f} bpm\n"
        if not filtered_df['systolic'].dropna().empty:
            summary_text += f"Average Systolic BP: {filtered_df['systolic'].mean():.2f} mmHg\n"
        if not filtered_df['diastolic'].dropna().empty:
            summary_text += f"Average Diastolic BP: {filtered_df['diastolic'].mean():.2f} mmHg\n"
        pdf.chapter_body(summary_text)
        
        # --- Raw Data Table with Daily Recommendations ---
        pdf.chapter_title("Daily Health Records and Recommendations")
        
        # Generate daily recommendations and add as a new column
        filtered_df['recommendation'] = filtered_df.apply(generate_daily_recommendation, axis=1)
        
        report_df = filtered_df[['date', 'blood_pressure', 'sugar_level', 'pulse_rate', 'notes', 'recommendation']].copy()
        pdf.add_dataframe_as_table(report_df)

        # --- PDF Download ---
        pdf_output = bytes(pdf.output(dest='S'))
        st.success("PDF report generated successfully!")
        st.download_button(
            label="Download Report",
            data=pdf_output,
            file_name=f"health_report_{start_date}_{end_date}.pdf",
            mime="application/pdf"
        )
