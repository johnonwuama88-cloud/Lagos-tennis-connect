import streamlit as st
import pandas as pd
import random
import string
import os

def generate_estate_code():
    """Generates a secure 6-character estate access code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Mapping venue options to your exact local images in the assets folder
VENUE_IMAGES = {
    "Lagos Lawn Tennis Club (TBS / Onikan)": "assets/lagos_lawn_tennis_club.jpg",
    "Ikoyi Club 1938 (Ikoyi)": "assets/Ikoyi_club.jpg",
    "Luik Tennis & Recreation Club (The Rock Drive, Lekki Phase 1)": "assets/Luik_tennis.jpg",
    "Lekki Tennis Club / Arena Court (Gbolahan Owolabi St, Lekki 1)": "assets/Lekki_tennis_club.jpg",
}

def render_booking_system():
    st.subheader("📅 Court Booking System & Gate Pass")
    st.caption("Reserve courts across Lagos, manage ball boy fees, and generate secure estate gate passes.")

    lagos_venues = [
        "--- 🏝️ Island Venues (Ikoyi, VI, Lekki & Ajah) ---",
        "Lagos Lawn Tennis Club (TBS / Onikan)",
        "Ikoyi Club 1938 (Ikoyi)",
        "Luik Tennis & Recreation Club (The Rock Drive, Lekki Phase 1)",
        "Lekki Tennis Club / Arena Court (Gbolahan Owolabi St, Lekki 1)",
        "Nicon Town Tennis Courts (Lekki Phase 1)",
        "VGC Recreation Club (Victoria Garden City, Ajah)",
        "Chevron Recreation Center (Lekki / Chevron Drive)",
        "Eko Hotels & Suites Tennis Court (Victoria Island)",
        "1004 Estate Tennis Courts (Victoria Island)",
        "Lagos Country Club Annex (Parkview Estate, Ikoyi)",
        "Banana Island Field & Tennis Courts (Ikoyi)",
        
        "--- 🏙️ Mainland Venues (Ikeja, Yaba, Surulere & Apapa) ---",
        "Ikeja Country Club / Lagos Country Club (Ikeja GRA)",
        "Dr. Philip Adegbile Sports Complex (Yabatech, Yaba)",
        "Unilag Tennis Courts (Akoka, Yaba)",
        "National Stadium Tennis Complex (Surulere)",
        "Apapa Club - Tennis Section (Park Lane, Apapa)",
        "Apapa City Club Tennis Court (Apapa)",
        "ISL Tennis Courts (Unilag Campus, Yaba)",
        "Civil Centre / Ikeja Recreation Club (GRA Ikeja)",
        "Gbagada Sports Club (Gbagada Phase 2)",
        "Command Day Secondary / Military Hospital Courts (Yaba/Ikeja)",
        "Eagle Club Tennis Section (Surulere)"
    ]

    col1, col2 = st.columns(2)
    
    with col1:
        venue = st.selectbox("Select Venue / Club in Lagos:", lagos_venues)
        booking_date = st.date_input("Select Booking Date")

    with col2:
        time_slot = st.selectbox(
            "Select Time Slot:",
            ["06:00 AM - 07:30 AM", "07:30 AM - 09:00 AM", "04:00 PM - 05:30 PM", "05:30 PM - 07:00 PM"]
        )
        court_num = st.selectbox("Court Number:", ["Court 1 (Center)", "Court 2", "Court 3", "Court 4"])

    # Interactive Venue Photo Preview
    if venue in VENUE_IMAGES:
        img_path = VENUE_IMAGES[venue]
        if os.path.exists(img_path):
            st.markdown("#### 🏟️ Court Facility Preview")
            st.image(img_path, caption=f"Photo: {venue}", use_container_width=True)
        else:
            st.warning(f"⚠️ Image file `{img_path}` not found in assets folder.")
    elif not venue.startswith("---"):
        st.info(f"📸 Image preview slot ready for **{venue}**. Add an image to `assets/` to display it here.")

    st.divider()

    # Payment & Fee Allocation
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
    
    if split_payment:
        st.caption(f"ℹ️ You will pay 50% now (₦{total_fee / 2:,.0f}), and a Paystack payment request will be sent to your opponent.")

    st.markdown("---")

    # Booking Confirmation & Gate Pass Generator
    if st.button("Confirm Booking & Generate Digital Gate Pass", type="primary"):
        if venue.startswith("---"):
            st.warning("Please select a valid venue from the list.")
        else:
            access_code = generate_estate_code()
            
            st.success("🎉 Booking Confirmed successfully!")
            
            with st.expander("🎫 View Digital Court & Estate Gate Pass", expanded=True):
                st.markdown(f"### 🎾 **{venue}**")
                st.write(f"**Date & Time:** {booking_date} | {time_slot}")
                st.write(f"**Court Assigned:** {court_num}")
                st.write(f"**Ball Boy Requested:** {'Yes' if include_ball_boy else 'No'}")
                
                st.info(f"🔑 **Estate / Security Gate Access Code:** `{access_code}`")
                st.caption("Show this code to security personnel at the estate gate for entry.")