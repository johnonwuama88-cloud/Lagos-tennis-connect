import streamlit as st

def render_referral_hub():
    st.subheader("🎁 Referrals & Player Rewards")
    st.caption("Invite fellow Lagos tennis players to join the network and earn court credit vouchers.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔗 Your Personal Referral Link")
        referral_code = "LAGOS-TENNIS-JOHN2026"
        st.code(f"https://lagostennisconnect.streamlit.app/?ref={referral_code}", language="text")
        
        st.markdown("### 📊 Your Referral Stats")
        st.metric("Total Invited Players", "5 Players")
        st.metric("Earned Court Vouchers", "₦7,500 Credit")

    with col2:
        st.markdown("### 🏆 Reward Tiers")
        st.info("• **1 Referral:** ₦1,500 off your next court booking\n"
                "• **3 Referrals:** Free 1-hour ball boy session\n"
                "• **5 Referrals:** Free entry into the Quarterly Lagos Ladder Tournament")

    st.divider()
    
    st.markdown("### 📩 Invite via WhatsApp / Email")
    invite_phone = st.text_input("Enter Player's WhatsApp Number (+234):", placeholder="e.g. 08012345678")
    
    if st.button("Send Invitation Link", type="primary"):
        if invite_phone:
            st.success(f"🎉 Invitation generated for {invite_phone}!")
            st.caption("Share message: *Hey! Join me on Lagos Tennis Connect to book courts and join ladder rankings: https://lagostennisconnect.streamlit.app/?ref=" + referral_code + "*")
        else:
            st.warning("Please enter a phone number to generate the invitation.")