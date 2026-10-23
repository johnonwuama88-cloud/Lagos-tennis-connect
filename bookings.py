import streamlit as st
import pandas as pd
import random
import string
from streamlit_gsheets import GSheetsConnection  # type: ignore

def generate_estate_code():
    """Generates a secure 6-character estate access code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def render_booking_system():
    st.subheader("📅 Court Reservation & Security Gate Pass")
    st.caption("Browse top courts in Lagos, schedule court slots, pay ball boy fees, and issue estate passes.")

    # 1. Authentic Lagos & African Tennis Player Showcase
    st.markdown("### 🏟️ Featured Lagos Tennis Clubs & Active Players")
    
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    
    with col_v1:
        st.image(
            "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=600&q=80",
            caption="Ikoyi Club 1938 (Center Court)",
            use_container_width=True
        )
        st.caption("🎾 **Ikoyi Club 1938** | 9 Hard Courts")
        
    with col_v2:
        st.image(
            "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?auto=format&fit=crop&w=600&q=80",
            caption="Lagos Lawn Tennis Club (Onikan)",
            use_container_width=True
        )
        st.caption("🎾 **LLTC Onikan** | Historic Clay/Hard")
        
    with col_v3:
        st.image(
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=600&q=80",
            caption="Lekki Phase 1 / Nicon Town Match",
            use_container_width=True
        )
        st.caption("🎾 **Nicon Town Courts** | Private Member Session")
        
    with col_v4:
        st.image(
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=600&q=80",
            caption="VGC Recreation Club",
            use_container_width=True
        )
        st.caption("🎾 **VGC Recreation Club** | Floodlit Evening Play")

    st.divider()

    # 2. Reservation Form
    st.markdown("### 📝 Reserve Your Slot")
    
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
        booking_date = st.date_input("Select Booking Date")

    with col2:
        time_slot = st.selectbox(
            "Select Time Slot:",
            ["06:00 AM - 07:30 AM", "07:30 AM - 09:00 AM", "04:00 PM - 05:30 PM", "05:30 PM - 07:00 PM"]
        )
        court_num = st.selectbox("Select Court:", ["Court 1 (Center)", "Court 2", "Court 3", "Court 4"])

    st.divider()

    # 3. Operations & Fee Breakdown
    st.markdown("### 💳 Fee Allocation")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        court_fee = 5000
        st.metric("Court Reservation Fee", f"₦{court_fee:,}")
        
    with col_b:
        include_ball_boy = st.checkbox("Include Ball Boy (+₦1,500)", value=True)
        ball_boy_fee = 1500 if include_ball_boy else 0
        
    with col_c:
        split_payment = st.checkbox("Split fee 50/50 with opponent")

    total_fee = court_fee + ball_boy_fee
    st.markdown(f"#### **Total Payment:** ₦{total_fee:,}")

    # 4. Confirmation Action
    if st.button("Confirm Reservation & Generate Gate Pass", type="primary", use_container_width=True):
        access_code = generate_estate_code()
        
        st.success("🎉 Court booked successfully!")
        
        with st.expander("🎫 Digital Security Gate & Court Pass", expanded=True):
            st.markdown(f"### 🎾 **{venue}**")
            st.write(f"**Date & Time:** {booking_date} | {time_slot}")
            st.write(f"**Court Assigned:** {court_num}")
            st.write(f"**Ball Boy Requested:** {'Yes' if include_ball_boy else 'No'}")
            
            st.info(f"🔑 **Security Access Code:** `{access_code}`")
            st.caption("Present this 6-digit access code at the security gate upon arrival.")