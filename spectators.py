import streamlit as st
import urllib.parse

APP_BASE_URL = "https://lagostennisconnect-app-72g48ltuk8.streamlit.app"

# In-memory session state initialization for active match fixtures
if "matches_db" not in st.session_state:
    st.session_state["matches_db"] = [
        {
            "id": "MATCH-101",
            "player1": "John O.",
            "player2": "Chidi M.",
            "court": "Ikoyi Club (Court 2)",
            "date_time": "Today, 4:00 PM",
            "allow_spectators": True,
            "spectators": ["Sola A.", "Fatima K."]
        }
    ]

def render_spectator_hub(current_user="John O."):
    st.subheader("🏟️ Match Spectator Center")
    
    tab1, tab2 = st.tabs(["🔥 Upcoming Matches to Watch", "🎾 Host / Invite Spectators"])
    
    # TAB 1: Browse & RSVP to matches
    with tab1:
        st.markdown("### Public Fixtures Open for Spectators")
        open_matches = [m for m in st.session_state["matches_db"] if m["allow_spectators"]]
        
        if not open_matches:
            st.info("No spectator matches scheduled right now. Check back later!")
        else:
            for match in open_matches:
                with st.expander(f"⚔️ {match['player1']} vs {match['player2']} — {match['court']}", expanded=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"⏰ **Time:** {match['date_time']}")
                        st.write(f"👥 **Attending Spectators ({len(match['spectators'])}):** {', '.join(match['spectators']) if match['spectators'] else 'None yet'}")
                    
                    with col2:
                        if current_user not in match["spectators"]:
                            if st.button("🎟️ RSVP to Watch", key=f"rsvp_{match['id']}"):
                                match["spectators"].append(current_user)
                                st.success("RSVP Confirmed!")
                                st.rerun()
                        else:
                            st.success("You're Attending!")
                    
                    with col3:
                        invite_text = (
                            f"🎾 *Match Alert!* Come watch {match['player1']} vs {match['player2']} "
                            f"at {match['court']} ({match['date_time']}). "
                            f"RSVP on Lagos Tennis Connect: {APP_BASE_URL}/?match_id={match['id']}"
                        )
                        wa_match_url = f"https://wa.me/?text={urllib.parse.quote(invite_text)}"
                        st.link_button("📲 Invite Spectators", wa_match_url)

    # TAB 2: Post match fixtures for spectator invites
    with tab2:
        st.markdown("### Invite Spectators to Your Match")
        with st.form("create_spectator_match_form"):
            opponent = st.text_input("Opponent Name", placeholder="e.g. Chidi M.")
            court_location = st.selectbox("Court Location", ["Ikoyi Club", "Lagos Country Club", "Eko Hotel Courts", "VGC Tennis Club"])
            match_time = st.text_input("Match Date & Time", value="Tomorrow, 5:00 PM")
            allow_specs = st.checkbox("Allow registered players to come and watch", value=True)
            
            submit = st.form_submit_button("Publish Match Fixture")
            if submit and opponent:
                new_match = {
                    "id": f"MATCH-{len(st.session_state['matches_db']) + 101}",
                    "player1": current_user,
                    "player2": opponent,
                    "court": court_location,
                    "date_time": match_time,
                    "allow_spectators": allow_specs,
                    "spectators": []
                }
                st.session_state["matches_db"].append(new_match)
                st.success("Match posted! Other players can now see it and RSVP to watch.")
                st.rerun()