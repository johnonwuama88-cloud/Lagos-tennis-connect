import streamlit as st

def init_spectators_db():
    """Guarantees that matches_db is initialized in session state."""
    if "matches_db" not in st.session_state or not st.session_state["matches_db"]:
        st.session_state["matches_db"] = [
            {
                "id": "M101",
                "players": "Chidi M. vs Sola A.",
                "court": "Ikoyi Club 1938",
                "date": "2026-10-25",
                "time": "04:00 PM",
                "ntrp": "4.0 - 4.5 (High Level)",
                "allow_spectators": True,
                "spectators": ["John O.", "Emeka N."]
            },
            {
                "id": "M102",
                "players": "Fatima K. vs Tunde B.",
                "court": "Lagos Country Club",
                "date": "2026-10-26",
                "time": "08:00 AM",
                "ntrp": "3.5",
                "allow_spectators": True,
                "spectators": []
            }
        ]

def render_spectator_hub(current_user="John O."):
    # Always ensure matches database is initialized safely
    init_spectators_db()
    
    st.subheader("👀 Match Spectators & Fan Hub")
    st.markdown("Catch exciting local matches across Lagos, support fellow club members, or open your upcoming matches to spectators.")
    
    tab1, tab2 = st.tabs(["🏟️ Upcoming Matches to Watch", "📣 List Your Match for Spectators"])
    
    # TAB 1: Watch Matches
    with tab1:
        st.markdown("### Open Matches Inviting Spectators")
        
        open_matches = [m for m in st.session_state["matches_db"] if m["allow_spectators"]]
        
        if not open_matches:
            st.info("No public matches listed for spectators right now. Check back soon or list your own match!")
        else:
            for match in open_matches:
                with st.expander(f"🎾 {match['players']} — {match['court']} ({match['date']} @ {match['time']})"):
                    st.write(f"**Level:** NTRP {match['ntrp']}")
                    st.write(f"**Spectators Attending:** {len(match['spectators'])} ({', '.join(match['spectators']) if match['spectators'] else 'Be the first!'})")
                    
                    if current_user in match["spectators"]:
                        st.success("✅ You are on the spectator list for this match!")
                    else:
                        if st.button(f"RSVP as Spectator for {match['id']}", key=f"btn_{match['id']}"):
                            match["spectators"].append(current_user)
                            st.rerun()

    # TAB 2: List Match
    with tab2:
        st.markdown("### Invite Spectators to Your Match")
        with st.form("spectator_form"):
            court = st.selectbox("Court Location", ["Ikoyi Club 1938", "Lagos Country Club", "VGC Tennis Club", "Eko Hotel Courts"])
            match_date = st.date_input("Match Date")
            match_time = st.selectbox("Match Time", ["07:00 AM", "08:00 AM", "04:00 PM", "05:00 PM", "06:00 PM"])
            opponent = st.text_input("Opponent Name")
            ntrp = st.selectbox("Estimated Match NTRP Level", ["3.0", "3.5", "4.0", "4.5", "5.0"])
            
            submit = st.form_submit_button("Publish Match to Spectator Hub")
            if submit:
                new_match = {
                    "id": f"M{len(st.session_state['matches_db']) + 101}",
                    "players": f"{current_user} vs {opponent if opponent else 'TBD'}",
                    "court": court,
                    "date": str(match_date),
                    "time": match_time,
                    "ntrp": ntrp,
                    "allow_spectators": True,
                    "spectators": []
                }
                st.session_state["matches_db"].append(new_match)
                st.success("Your match has been published to the Spectator Hub!")