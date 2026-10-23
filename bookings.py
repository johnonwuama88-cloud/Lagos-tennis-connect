import streamlit as st
import random
import string

def generate_estate_code():
    """Generates a secure 6-character estate access code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def render_booking_system():
    st.subheader("📅 Court Booking System & Gate Pass")
    st.caption("Reserve courts across Lagos, manage ball boy fees, and generate secure estate gate passes.")

    # Selection Layout
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

    # Split-Fee & Add-on Services
    st.markdown("### 💳 Payment & Operations Split (Paystack)")
    
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
    
    if split_payment:
        st.caption("ℹ️ You will pay 50% now (₦{:,.0f}), and a Paystack payment request will be sent to your opponent.".format(total_fee / 2))

    st.markdown("---")

    # Booking Confirmation Button
    if st.button("Confirm Booking & Generate Digital Gate Pass", type="primary"):
        access_code = generate_estate_code()
        
        st.success("🎉 Booking Confirmed successfully!")
        
        # Pass Presentation
        with st.expander("🎫 View Digital Court & Estate Gate Pass", expanded=True):
            st.markdown(f"### 🎾 **{venue}**")
            st.write(f"**Date & Time:** {booking_date} | {time_slot}")
            st.write(f"**Court Assigned:** {court_num}")
            st.write(f"**Ball Boy Requested:** {'Yes' if include_ball_boy else 'No'}")
            
            st.info(f"🔑 **Estate / Security Gate Access Code:** `{access_code}`")
            st.caption("Show this code to security personnel at the estate gate for entry.")
            
            # Simulated WhatsApp sharing
            whatsapp_msg = f"Lagos Tennis Connect Pass: Booking at {venue} on {booking_date} ({time_slot}). Gate Code: {access_code}"
            st.text_input("WhatsApp Ready Share Text:", value=whatsapp_msg)