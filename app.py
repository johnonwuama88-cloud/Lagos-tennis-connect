import streamlit as st

# Import modular page functions
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

page = st.sidebar.selectbox(
    "Choose a Module:",
    [
        "📅 Court Bookings",
        "🏆 Ladder & Rankings",
        "👀 Match Spectators",
        "📰 Tennis News & Scores",
        "🎁 Referrals & Rewards"
    ]
)

st.sidebar.divider()
st.sidebar.info("👤 **Active User:** John O. | 📍 **Location:** Lekki, Lagos")

# Route selected module
if page == "📅 Court Bookings":
    render_booking_system()

elif page == "🏆 Ladder & Rankings":
    render_ladder()

elif page == "👀 Match Spectators":
    render_spectator_hub(current_user="John O.")

elif page == "📰 Tennis News & Scores":
    render_tennis_news_hub()

elif page == "🎁 Referrals & Rewards":
    render_referral_hub()