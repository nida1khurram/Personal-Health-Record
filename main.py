import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

from features.input_form.input_form import render_input_form
from features.visualization.visualization import render_visualization
from features.analytics.analytics import render_analytics
from features.reports.reports import render_reports
from features.recommendations.recommendations import render_recommendations
from features.introduction.introduction import render_introduction
from features.ui.ui import render_ui

def main():
    authenticator.login(location='main') # Call login with keyword argument for location

    if st.session_state["authentication_status"]: # Access status directly from session_state
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{st.session_state["name"]}*') # Access name from session_state
        
        # Original main content goes here
        page = render_ui()

        if page == "Introduction":
            render_introduction()
        elif page == "Input Form":
            render_input_form()
        elif page == "Visualization":
            render_visualization()
        elif page == "Analytics":
            render_analytics()
        elif page == "Reports":
            render_reports()
        elif page == "Recommendations":
            render_recommendations()

    elif st.session_state["authentication_status"] == False: # Access status directly
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] == None: # Access status directly
        st.warning('Please enter your username and password')

    # Registration form, only shown if not authenticated
    if st.session_state["authentication_status"] == False or st.session_state["authentication_status"] == None:
        with st.expander("Register New User"):
            try:
                            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                                location='main'
                            )
                            if email_of_registered_user:
                                st.success('User registered successfully! Please log in.')
                                # Save the updated config to the YAML file
                                with open('./config.yaml', 'w') as file:
                                    yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                st.error(e)
        
if __name__ == "__main__":
    main()
