import streamlit as st
from bookings import render_court_bookings
from referrals import get_or_set_referral_code, render_invite_friends_section
from spectators import render_spectator_hub
from ladder import render_ladder_hub

# Page Configuration
st.set_page_config(
    page_title="Lagos Tennis Connect",
    page_icon="🎾",
    layout="wide"
)

# Initialize referral check on application load
get_or_set_referral_code()

# App Header
st.title("🎾 Lagos Tennis Connect")
st.caption("Connecting players, courts, and coaches across Lagos")

# Sidebar Navigation
page = st.sidebar.radio("Navigation", [
    "Court Bookings", 
    "Matchmaking", 
    "Ladder & Rankings",
    "Match Spectators", 
    "Invite Friends", 
    "Profile"
])

# Page Routing
if page == "Court Bookings":
    render_court_bookings(current_user="John O.")

elif page == "Matchmaking":
    st.subheader("🎾 Player Matchmaking & Hitting Partners")
    st.markdown("Find hitting partners at your skill level across Lagos.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Search Location", value="Ikoyi / Victoria Island")
    with col2:
        st.select_slider("Skill Level (NTRP)", options=["2.5", "3.0", "3.5", "4.0", "4.5", "5.0"])
        
    st.success("Matches available in your area!")

elif page == "Ladder & Rankings":
    render_ladder_hub(current_user="John O.")

elif page == "Match Spectators":
    render_spectator_hub(current_user="John O.")

elif page == "Invite Friends":
    render_invite_friends_section(user_id="JOHN101", user_name="John")

elif page == "Profile":
    st.subheader("👤 Player Profile")
    st.write("**Name:** John Onwuama")
    st.write("**Location:** Lagos, Nigeria")
    st.write("**Reliability Score:** 98% (Trusted Member)")
    st.write("**No-Show Strikes:** 0 / 3")