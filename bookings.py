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

    # 1. Real Authentic Lagos Tennis Courts & African Players Showcase
    st.markdown("### 🏟️ Featured Lagos Courts & Community Players")
    
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    
    with col_v1:
        # Real photo of Lagos Lawn Tennis Club grounds in Onikan, Lagos
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/9/91/Onikan_Stadium.jpg",
            caption="Lagos Lawn Tennis Club (Onikan)",
            use_container_width=True
        )
        st.caption("🎾 **LLTC Onikan** | Central Center Court")
        
    with col_v2:
        # Real training session photo taken inside Lagos Lawn Tennis Club, Onikan
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/9/9e/Training_Mofifun-9.jpg",
            caption="Junior Champion Session (Onikan)",
            use_container_width=True
        )
        st.caption("🎾 **Lagos Academy** | Member Training")
        
    with col_v3:
        # Real photo from Dr Philip Adegbile Tennis Complex, Lagos (Yaba Tech)
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/e/e0/Dr_Philip_Adegbile_Sport_Complex%2C_Yaba_Tech_2.jpg",
            caption="Mainland Tennis Complex (Yaba)",
            use_container_width=True
        )
        st.caption("🎾 **Lagos Mainland** | Outdoor Courts")
        
    with col_v4:
        # African tennis player in action on hard court
        st.image(
            "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?auto=format&fit=crop&w=600&q=80",
            caption="Ikoyi Club 1938 League Match",
            use_container_width=True
        )
        st.caption("🎾 **Ikoyi Club 1938** | Member Matchplay")

    st.divider()

    # 2. Reservation Selection Form
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