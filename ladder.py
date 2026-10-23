import streamlit as st
import pandas as pd

def render_ladder():
    st.subheader("🏆 Lagos Tennis Challenge Ladder & Rankings")
    st.caption("Track player ratings, view local rankings, and issue formal match challenges.")

    # Top Rankings Table
    data = {
        "Rank": [1, 2, 3, 4, 5],
        "Player Name": ["Segun A.", "Chidi O.", "John O.", "Tunde B.", "Emeka K."],
        "Location": ["Ikoyi", "Victoria Island", "Lekki Phase 1", "Ikeja GRA", "VGC"],
        "UTR Rating": [8.4, 8.1, 7.8, 7.5, 7.2],
        "Matches Played": [14, 12, 10, 8, 9],
        "Status": ["Defending Champion", "Active", "Challenging", "Active", "Active"]
    }
    
    df = pd.DataFrame(data)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Challenge System
    st.markdown("### ⚔️ Issue a Ladder Challenge")
    
    col1, col2 = st.columns(2)
    with col1:
        target_player = st.selectbox("Select Player to Challenge:", [p for p in df["Player Name"] if p != "John O."])
        preferred_venue = st.selectbox("Preferred Venue:", ["Ikoyi Club 1938", "Lagos Lawn Tennis Club", "VGC Recreation Club"])
    
    with col2:
        proposed_date = st.date_input("Proposed Match Date")
        proposed_time = st.time_input("Proposed Time")
        
    if st.button("Send Formal Match Challenge", type="primary"):
        st.success(f"🎉 Challenge request sent to **{target_player}** for {proposed_date} at {proposed_time}!")
        st.info("They will receive an automated notification to accept or propose an alternative time.")