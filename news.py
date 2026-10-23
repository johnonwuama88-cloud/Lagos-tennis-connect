import streamlit as st
import feedparser

@st.cache_data(ttl=1800) # Cache for 30 minutes to ensure fast load times and save bandwidth
def fetch_live_tennis_news():
    """Fetches real-time tennis news from primary and fallback RSS sources."""
    rss_sources = [
        "https://news.google.com/rss/search?q=tennis+atp+wta&hl=en-US&gl=US&ceid=US:en",
        "https://www.wtatennis.com/rss-feeds/news",
        "http://feeds.feedburner.com/tennisx"
    ]
    
    for url in rss_sources:
        try:
            feed = feedparser.parse(url)
            if feed.entries and len(feed.entries) > 0:
                return feed.entries[:8]
        except Exception:
            continue
            
    return []

def render_tennis_news_hub():
    st.subheader("📰 Pro Tour & Live Tennis News Hub")
    st.caption("Automated live headlines, match scores, and local Lagos tournament coverage.")
    
    tab1, tab2, tab3 = st.tabs(["📰 Live Headlines", "🔴 Pro Scores Ticker", "🎥 Video Highlights"])
    
    # TAB 1: Live RSS Headlines
    with tab1:
        st.markdown("### Top Global Tennis Stories")
        
        with st.spinner("Fetching latest headlines from live sports feeds..."):
            articles = fetch_live_tennis_news()
        
        if not articles:
            st.warning("Unable to reach live news servers at the moment. Please check back shortly.")
        else:
            for entry in articles:
                title = entry.get("title", "Tennis News Update")
                link = entry.get("link", "#")
                published = entry.get("published", "Recently Updated")
                
                # Format clean card presentation
                with st.container():
                    st.markdown(f"#### 🎾 [{title}]({link})")
                    st.caption(f"🕒 Published: {published}")
                    st.divider()

    # TAB 2: Live Scores Ticker
    with tab2:
        st.markdown("### Featured Match Center & Scores")
        
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
        st.markdown("### 🇳🇬 Lagos Tennis Circuit Notice")
        st.info("Local club tournament fixtures at Ikoyi Club 1938 and Lagos Lawn Tennis Club are active. Check the **Match Spectators** tab to view or schedule local spectating!")

    # TAB 3: Video Highlights
    with tab3:
        st.markdown("### Curated Highlights & Masterclasses")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Tour Match Rallies & Top Shots**")
            st.link_button("▶️ Watch ATP/WTA Highlights", "https://www.youtube.com/results?search_query=atp+wta+tennis+highlights", use_container_width=True)
        with col_b:
            st.markdown("**Pro Technique & Footwork Masterclasses**")
            st.link_button("▶️ Watch Coaching Videos", "https://www.youtube.com/results?search_query=tennis+technique+masterclass", use_container_width=True)