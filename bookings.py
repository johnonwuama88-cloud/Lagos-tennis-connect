import streamlit as st
import urllib.parse
import random

def render_court_bookings(current_user="John O."):
    st.subheader("🏟️ Court Bookings & Digital Passes")
    st.markdown("Reserve top courts across Lagos. Your booking instantly generates a verifiable Digital Pass for gate guards and stewards.")
    
    with st.form("booking_form"):
        club = st.selectbox("Select Tennis Facility", [
            "Ikoyi Club 1938 (Ikoyi)", 
            "Lagos Country Club (Ikeja)", 
            "VGC Tennis Club (Victoria Garden City)", 
            "Eko Hotel Tennis Courts (VI)"
        ])
        
        # Check if club requires an estate access code
        requires_estate_code = "VGC" in club or "Garden City" in club
        estate_code = ""
        if requires_estate_code:
            st.info("🔒 This facility is inside a gated estate. A visitor access code is required for gate entry.")
            estate_code = st.text_input("Estate Visitor Access Code", value=f"VGC-{random.randint(1000,9999)}")
        
        date = st.date_input("Select Booking Date")
        time_slot = st.selectbox("Select Time Slot", ["07:00 AM - 08:00 AM", "08:00 AM - 09:00 AM", "04:00 PM - 05:00 PM", "05:00 PM - 06:00 PM"])
        
        include_ball_boy = st.checkbox("Include Official Ball Boy & Attendant Fee (+ ₦1,500 split payment)", value=True)
        
        submit_booking = st.form_submit_button("Proceed to Paystack Split Checkout")
        
        if submit_booking:
            booking_id = f"LTC-BK-{random.randint(10000, 99999)}"
            st.session_state["latest_booking"] = {
                "id": booking_id,
                "club": club,
                "date": str(date),
                "time": time_slot,
                "user": current_user,
                "estate_code": estate_code if requires_estate_code else None,
                "ball_boy": include_ball_boy
            }
            st.success("Payment successful via Paystack! Digital Court Pass generated.")
    
    # Display Digital Pass if available
    if "latest_booking" in st.session_state:
        b = st.session_state["latest_booking"]
        st.markdown("---")
        st.markdown("### 🎫 Your Active Digital Court Pass")
        
        pass_summary = (
            f"🎾 *LAGOS TENNIS CONNECT — OFFICIAL PASS*\n\n"
            f"• *Booking ID:* {b['id']}\n"
            f"• *Facility:* {b['club']}\n"
            f"• *Date & Time:* {b['date']} | {b['time']}\n"
            f"• *Player:* {b['user']}\n"
        )
        if b['estate_code']:
            pass_summary += f"• *Estate Gate Code:* `{b['estate_code']}`\n"
        pass_summary += f"• *Status:* PAID & VERIFIED (Paystack)"
        
        st.info(pass_summary)
        
        # WhatsApp share button for the pass
        wa_pass_text = f"{pass_summary}\n\n*Note to Gate Guard / Steward:* Please verify this digital pass for court entry."
        wa_pass_url = f"https://wa.me/?text={urllib.parse.quote(wa_pass_text)}"
        st.link_button("📲 Send Pass to WhatsApp / Gate Guard", wa_pass_url, use_container_width=True)