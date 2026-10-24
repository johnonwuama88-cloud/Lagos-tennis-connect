import streamlit as st

# Import modular page functions
from registration import render_registration  # <--- Make sure you have registration.py created!
from bookings import render_booking_system
from ladder import render_ladder
from spectators import render_spectator_hub
from news import render_tennis_news_hub
from referrals import render_referral_hub

# Page Configuration
st.set_page_config(
    page_title="Lagos Tennis Connect",
    page_icon="🎾",
    layout="wide"
)

# Main Title Header
st.title("🎾 Lagos Tennis Connect")
st.caption("The ultimate community platform for Lagos tennis players — book courts, join rankings, watch matches & get pro tour updates.")

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/tennis-.png", width=70)
st.sidebar.title("Navigation")

# Added 'Player Registration / Profile' as the first option
page = st.sidebar.selectbox(
    "Choose a Module:",
    [
        "👤 Player Registration / Profile",
        "📅 Court Bookings",
        "🏆 Ladder & Rankings",
        "👀 Match Spectators",
        "📰 Tennis News & Scores",
        "🎁 Referrals & Rewards"
    ]
)

st.sidebar.divider()

# Session State Check for Dynamic Active User Display
if "user_name" in st.session_state and st.session_state["user_name"]:
    active_user = st.session_state["user_name"]
    active_loc = st.session_state.get("user_location", "Lagos")
    st.sidebar.info(f"👤 **Active User:** {active_user} | 📍 **Location:** {active_loc}")
else:
    st.sidebar.warning("⚠️ **Status:** Guest (Please Register)")

# Route selected module
if page == "👤 Player Registration / Profile":
    render_registration()

elif page == "📅 Court Bookings":
    render_booking_system()

elif page == "🏆 Ladder & Rankings":
    render_ladder()

elif page == "👀 Match Spectators":
    render_spectator_hub(current_user=st.session_state.get("user_name", "John O."))

elif page == "📰 Tennis News & Scores":
    render_tennis_news_hub()

elif page == "🎁 Referrals & Rewards":
    render_referral_hub()