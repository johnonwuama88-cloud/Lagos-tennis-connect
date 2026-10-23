import streamlit as st
from referrals import get_or_set_referral_code, render_invite_friends_section
from spectators import render_spectator_hub

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
    "Match Spectators", 
    "Invite Friends", 
    "Profile"
])

# Page Routing
if page == "Court Bookings":
    st.subheader("🏟️ Court Bookings & Reservations")
    st.markdown("Reserve slots at top tennis facilities across Lagos.")
    
    court = st.selectbox("Select Tennis Club", ["Ikoyi Club 1938", "Lagos Country Club", "VGC Tennis Club", "Eko Hotel Tennis Courts"])
    date = st.date_input("Select Date")
    time_slot = st.selectbox("Select Time Slot", ["07:00 AM - 08:00 AM", "08:00 AM - 09:00 AM", "04:00 PM - 05:00 PM", "05:00 PM - 06:00 PM"])
    
    if st.button("Proceed to Paystack Checkout"):
        st.info(f"Booking {court} for {date} at {time_slot}. Initializing Paystack Split Payment...")

elif page == "Matchmaking":
    st.subheader("🎾 Player Matchmaking & Ladder")
    st.markdown("Find hitting partners at your skill level across Lagos.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Search Location", value="Ikoyi / Victoria Island")
    with col2:
        st.select_slider("Skill Level (NTRP)", options=["2.5", "3.0", "3.5", "4.0", "4.5", "5.0"])
        
    st.success("Matches available in your area!")

elif page == "Match Spectators":
    render_spectator_hub(current_user="John O.")

elif page == "Invite Friends":
    render_invite_friends_section(user_id="JOHN101", user_name="John")

elif page == "Profile":
    st.subheader("👤 Player Profile")
    st.write("**Name:** John Onwuama")
    st.write("**Location:** Lagos, Nigeria")
    st.write("**Preferred Hand:** Right-handed")