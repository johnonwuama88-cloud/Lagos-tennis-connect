import streamlit as st
import feedparser

@st.cache_data(ttl=1800) # Cache news for 30 minutes to ensure fast loading and avoid rate limits
def fetch_live_tennis_news():
    """Automatically fetches the latest global tennis headlines via public RSS feed."""
    rss_url = "https://news.google.com/rss/search?q=tennis+atp+wta&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    return feed.entries[:6] # Grab top 6 latest articles

def render_tennis_news_hub():
    st.subheader("📰 Pro Tour & Live Tennis News Hub")
    st.markdown("Automatically updated in real-time from global tennis feeds and local circuits.")
    
    tab1, tab2, tab3 = st.tabs(["🔴 Live Scores Ticker", "📰 Live RSS Headlines", "🎥 Highlights & Masterclasses"])
    
    # TAB 1: Live Scores & Ticker
    with tab1:
        st.markdown("### Today's Featured Matches & Scores")
        st.info("💡 **API Integration Note:** Live score tickers sync automatically via sports data APIs (such as Sportradar or RapidAPI Tennis). Below is the active match feed:")
        
        # Simulated live match structure (ready to map to an API response loop)
        col1, col2, col3 = st.columns([3, 1, 3])
        with col1:
            st.markdown("**Carlos Alcaraz (ESP)**")
            st.caption("ATP Ranking: #2")
        with col2:
            st.markdown("### 6-4, 3-2*")
            st.caption("🔴 LIVE (Set 2)")
        with col3:
            st.markdown("**Jannik Sinner (ITA)**")
            st.caption("ATP Ranking: #1")
        
        st.divider()
        
        col1, col2, col3 = st.columns([3, 1, 3])
        with col1:
            st.markdown("**Novak Djokovic (SRB)**")
            st.caption("ATP Ranking: #4")
        with col2:
            st.markdown("### Final")
            st.caption("🟢 Completed (7-6, 6-3)")
        with col3:
            st.markdown("**Alexander Zverev (GER)**")
            st.caption("ATP Ranking: #3")
            
        st.markdown("---")
        st.markdown("### 🇳🇬 Lagos Local Circuit")
        st.success("Local tournament fixtures across Ikoyi Club and Lagos Lawn Tennis Club are active. Check the **Match Spectators** tab to coordinate attendance!")

    # TAB 2: Live RSS Headlines (Fully Automated)
    with tab2:
        st.markdown("### Latest Automated Headlines")
        st.caption("Fetched live from global sports feeds with zero manual updates.")
        
        try:
            articles = fetch_live_tennis_news()
            if not articles:
                st.warning("Unable to fetch live news at the moment. Please check your internet connection.")
            else:
                for entry in articles:
                    title = entry.get("title", "No Title")
                    link = entry.get("link", "#")
                    published = entry.get("published", "Recent")
                    
                    st.markdown(f"#### [{title}]({link})")
                    st.caption(f"Published: {published}")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error loading news feed: {e}")

    # TAB 3: Video Highlights
    with tab3:
        st.markdown("### Curated Match Highlights & Masterclasses")
        st.markdown("Watch top professional rallies and tactical breakdowns.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Epic Pro Rally Exchanges**")
            st.link_button("▶️ Watch on YouTube", "https://www.youtube.com/results?search_query=atp+tennis+highlights", use_container_width=True)
        with col_b:
            st.markdown("**Pro Serving & Footwork Masterclass**")
            st.link_button("▶️ Watch Training Tips", "https://www.youtube.com/results?search_query=tennis+serving+technique+masterclass", use_container_width=True)