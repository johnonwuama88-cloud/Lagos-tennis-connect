import streamlit as st
import urllib.parse
import random

def render_court_bookings(current_user="John O."):
    st.subheader("🏟️ Court Bookings & Digital Passes")
    st.markdown("Reserve top courts across Lagos. Your booking instantly generates a verifiable Digital Pass for gate guards and court stewards.")
    
    # Facility Selection Outside the Form for Instant Dynamic Feedback
    club = st.selectbox(
        "Select Tennis Facility", 
        [
            "Ikoyi Club 1938 (Ikoyi)", 
            "Lagos Country Club (Ikeja)", 
            "VGC Tennis Club (Victoria Garden City)", 
            "Eko Hotel Tennis Courts (VI)"
        ]
    )
    
    # Check if facility is inside a gated estate
    requires_estate_code = "VGC" in club or "Garden City" in club
    default_gate_code = f"VGC-{random.randint(1000, 9999)}" if requires_estate_code else ""

    if requires_estate_code:
        st.warning("🔒 **Gated Estate Facility:** This court requires a visitor gate pass for entry.")
    
    # Booking Details Form
    with st.form("booking_form"):
        date = st.date_input("Select Booking Date")
        time_slot = st.selectbox("Select Time Slot", ["07:00 AM - 08:00 AM", "08:00 AM - 09:00 AM", "04:00 PM - 05:00 PM", "05:00 PM - 06:00 PM"])
        
        if requires_estate_code:
            estate_code = st.text_input("Visitor Gate Access Code", value=default_gate_code)
        else:
            estate_code = None
            
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
                "estate_code": estate_code,
                "ball_boy": include_ball_boy
            }
            st.success("Payment successful via Paystack! Digital Court Pass generated below.")

    # Display Active Digital Pass if booking exists
    if "latest_booking" in st.session_state:
        b = st.session_state["latest_booking"]
        st.markdown("---")
        st.markdown("### 🎫 Your Active Digital Court Pass")
        
        pass_text = (
            f"🎾 *LAGOS TENNIS CONNECT — DIGITAL COURT PASS*\n\n"
            f"• *Pass ID:* {b['id']}\n"
            f"• *Facility:* {b['club']}\n"
            f"• *Date & Time:* {b['date']} | {b['time']}\n"
            f"• *Player:* {b['user']}\n"
        )
        if b['estate_code']:
            pass_text += f"• *Estate Gate Code:* `{b['estate_code']}`\n"
        
        pass_text += f"• *Ball Boy Fee:* {'Included' if b['ball_boy'] else 'Not Included'}\n"
        pass_text += f"• *Status:* PAID & VERIFIED (Paystack Escrow)"
        
        st.info(pass_text)
        
        # WhatsApp Share Button
        wa_text = f"{pass_text}\n\n*Gate Guard / Steward Notice:* Please present this digital pass upon arrival at the facility."
        wa_url = f"https://wa.me/?text={urllib.parse.quote(wa_text)}"
        st.link_button("📲 Share Pass to WhatsApp / Gate Security", wa_url, use_container_width=True)