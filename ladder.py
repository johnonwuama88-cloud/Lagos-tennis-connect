import streamlit as st

def init_ladder_db():
    """Ensures ladder_db is always initialized in session state."""
    if "ladder_db" not in st.session_state or not st.session_state["ladder_db"]:
        st.session_state["ladder_db"] = [
            {"rank": 1, "name": "Chidi M.", "ntrp": "4.5", "points": 1250, "record": "14-2"},
            {"rank": 2, "name": "John O.", "ntrp": "4.0", "points": 1120, "record": "12-4"},
            {"rank": 3, "name": "Sola A.", "ntrp": "4.0", "points": 980, "record": "10-5"},
            {"rank": 4, "name": "Fatima K.", "ntrp": "3.5", "points": 850, "record": "9-6"},
            {"rank": 5, "name": "Emeka N.", "ntrp": "3.5", "points": 720, "record": "7-8"}
        ]

def render_ladder_hub(current_user="John O."):
    # Always ensure database initialization
    init_ladder_db()
    
    st.subheader("🏆 Lagos Tennis Connect — Official Ladder")
    st.markdown("Climb the ranks by challenging players above you and logging match results.")
    
    tab1, tab2 = st.tabs(["📊 Leaderboard Standings", "⚔️ Issue a Ladder Challenge"])
    
    # TAB 1: Leaderboard Table
    with tab1:
        st.markdown("### Current Singles Rankings")
        
        for player in sorted(st.session_state["ladder_db"], key=lambda x: x["rank"]):
            is_me = (player["name"] == current_user)
            
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            with col1:
                st.markdown(f"### #{player['rank']}")
            with col2:
                st.markdown(f"**{player['name']}** {'*(You)*' if is_me else ''}")
                st.caption(f"NTRP: {player['ntrp']}")
            with col3:
                st.write(f"🌟 **{player['points']} pts**")
            with col4:
                st.write(f"📈 Record: {player['record']}")
                
    # TAB 2: Issue a Challenge
    with tab2:
        st.markdown("### Challenge a Player")
        st.markdown("Rule: You can challenge any player ranked up to **2 spots above you**.")
        
        user_rank = next((p["rank"] for p in st.session_state["ladder_db"] if p["name"] == current_user), 2)
        eligible_opponents = [p["name"] for p in st.session_state["ladder_db"] if p["rank"] < user_rank and p["rank"] >= max(1, user_rank - 2)]
        
        if not eligible_opponents:
            st.info("You are currently near the top of your bracket! Defend your rank against incoming challengers.")
        else:
            with st.form("challenge_form"):
                opponent = st.selectbox("Select Opponent to Challenge", eligible_opponents)
                match_date = st.date_input("Proposed Match Date")
                court = st.selectbox("Preferred Court", ["Ikoyi Club", "Lagos Country Club", "VGC Tennis Club"])
                
                submit_challenge = st.form_submit_button("Send Official Challenge")
                if submit_challenge:
                    st.success(f"Challenge successfully sent to **{opponent}** for {match_date} at {court}! They have 48 hours to accept.")