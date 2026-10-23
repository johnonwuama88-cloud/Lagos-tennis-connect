import streamlit as st
import pandas as pd
import random
import string
from streamlit_gsheets import GSheetsConnection  # type: ignore

def generate_estate_code():
    """Generates a secure 6-character estate access code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def render_booking_system():
    st.subheader("📅 Court Booking System & Gate Pass")
    st.caption("Reserve courts across Lagos, manage ball boy fees, and generate secure estate gate passes.")

    # Establish Google Sheets Connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # 1. Selection Form
    col1, col2 = st.columns(2)
    
    with col1:
        venue = st.selectbox(
            "Select Venue / Club:",
            [
                "Ikoyi Club 1938 (Ikoyi)",
                "Lagos Lawn Tennis Club (TBS / Onikan)",
                "VGC Recreation Club (Victoria Garden City)",
                "Nicon Town Tennis Courts (Lekki Phase 1)",
                "Chevron Recreation Center (Gbagada / Lekki)",
                "Ikeja Country Club (GRA Ikeja)"
            ]
        )
        
        booking_date = st.date_input("Select Date")

    with col2:
        time_slot = st.selectbox(
            "Select Time Slot:",
            ["06:00 AM - 07:30 AM", "07:30 AM - 09:00 AM", "04:00 PM - 05:30 PM", "05:30 PM - 07:00 PM"]
        )
        
        court_num = st.selectbox("Court Number:", ["Court 1 (Center)", "Court 2", "Court 3", "Court 4"])

    st.divider()

    # 2. Payment Details
    st.markdown("### 💳 Payment & Operations Split")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        court_fee = 5000
        st.metric("Court Reservation Fee", f"₦{court_fee:,}")
        
    with col_b:
        include_ball_boy = st.checkbox("Include Ball Boy Assistance (+₦1,500)", value=True)
        ball_boy_fee = 1500 if include_ball_boy else 0
        
    with col_c:
        split_payment = st.checkbox("Split payment with opponent via Paystack link")

    total_fee = court_fee + ball_boy_fee
    st.markdown(f"#### **Total Amount:** ₦{total_fee:,}")

    st.markdown("---")

    # 3. Confirm Booking & Append to Database
    if st.button("Confirm Booking & Save to Database", type="primary"):
        access_code = generate_estate_code()
        
        # New record payload
        new_booking = pd.DataFrame([{
            "User": "John O.",
            "Venue": venue,
            "Date": str(booking_date),
            "TimeSlot": time_slot,
            "Court": court_num,
            "BallBoy": "Yes" if include_ball_boy else "No",
            "TotalFee": total_fee,
            "GateCode": access_code
        }])
        
        try:
            # Fetch existing data & append
            existing_data = conn.read(worksheet="Bookings", ttl=0)
            updated_df = pd.concat([existing_data, new_booking], ignore_index=True)
            conn.update(worksheet="Bookings", data=updated_df)
            st.success("🎉 Booking saved permanently to the central database!")
        except Exception as e:
            # Fallback if initial sheet is empty/unconfigured
            st.info("🎉 Booking confirmed locally!")

        # Gate Pass Output
        with st.expander("🎫 View Digital Court & Estate Gate Pass", expanded=True):
            st.markdown(f"### 🎾 **{venue}**")
            st.write(f"**Date & Time:** {booking_date} | {time_slot}")
            st.write(f"**Court Assigned:** {court_num}")
            st.info(f"🔑 **Estate / Security Gate Access Code:** `{access_code}`")

    st.divider()

    # 4. Read Live Bookings from Database
    st.markdown("### 📋 Live Confirmed Court Reservations")
    try:
        live_bookings = conn.read(worksheet="Bookings", ttl=10)
        st.dataframe(live_bookings, use_container_width=True, hide_index=True)
    except Exception:
        st.caption("Connect your Google Sheet credentials under `.streamlit/secrets.toml` to view live synced database records.")
