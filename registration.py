# Save this file as registration.py
import streamlit as st

def render_registration():
    st.header("👤 New Player Registration")
    st.write("Join the Lagos tennis network to book courts, enter ladder rankings, and find hitting partners.")
    
    with st.form("player_registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", placeholder="e.g. John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            phone = st.text_input("Phone / WhatsApp Number *", placeholder="+234...")
            
        with col2:
            location = st.selectbox(
                "Primary Location in Lagos *",
                ["Lekki / Victoria Island / Ikoyi", "Ikeja / Maryland", "Surulere / Yaba", "Ajah / Sangotedo", "Festac / Mile 2", "Other"]
            )
            skill_level = st.selectbox(
                "NTRP / Skill Level *",
                ["Beginner (1.0 - 2.5)", "Intermediate (3.0 - 3.5)", "Advanced (4.0 - 4.5)", "Pro / Semi-Pro (5.0+)"]
            )
            play_style = st.multiselect(
                "Preferred Play Types",
                ["Singles", "Doubles", "Casual Hitting", "Competitive / Ladder"]
            )
            
        submitted = st.form_submit_button("Register Player Profile 🚀", type="primary")
        
        if submitted:
            if full_name and email:
                st.session_state["user_name"] = full_name
                st.session_state["user_location"] = location
                st.success(f"Welcome to Lagos Tennis Connect, {full_name}! Your profile is active.")
                st.balloons()
            else:
                st.error("Please complete all required fields (*).")