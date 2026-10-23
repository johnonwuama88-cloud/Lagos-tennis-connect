import streamlit as st
import urllib.parse

APP_BASE_URL = "https://lagostennisconnect-app-72g48ltuk8.streamlit.app"

def get_or_set_referral_code():
    """Detects if a new user visited using a referral link."""
    query_params = st.query_params
    if "ref" in query_params:
        referred_by = query_params["ref"]
        st.session_state["referred_by_code"] = referred_by
        st.toast(f"🎾 Joined via referral code: **{referred_by}**!", icon="🎉")

def render_invite_friends_section(user_id="JOHN101", user_name="John"):
    """Renders the Invite Friends hub inside the app."""
    st.subheader("🤝 Invite Friends & Earn Perks")
    
    # Generate unique referral link
    referral_link = f"{APP_BASE_URL}/?ref={user_id}"
    
    # Pre-filled WhatsApp message
    whatsapp_message = (
        f"Hey! Join me on Lagos Tennis Connect to book courts, find hitting partners, "
        f"and track local ladder rankings. Download/join here: {referral_link}"
    )
    encoded_message = urllib.parse.quote(whatsapp_message)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"
    
    st.markdown("""
    Invite local players to *Lagos Tennis Connect*. When they sign up using your link, 
    you both get priority placement on matchmaking boards!
    """)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.text_input("Your Personal Invite Link", value=referral_link, disabled=True)
    with col2:
        st.write(" ")  # Vertical spacing
        st.link_button("📲 Share on WhatsApp", whatsapp_url, use_container_width=True)
        
    st.caption("Tip: You can also copy your link above and paste it directly into your local tennis club group chat.")