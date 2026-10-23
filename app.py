import streamlit as st

# Import all modular page functions
from bookings import render_booking_system
from ladder import render_ladder
from spectators import render_spectator_hub
from news import render_tennis_news_hub
from referrals import render_referral_hub

# Page Configuration
st.set_page_config(
    page_title="Lagos Tennis Connect",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS Injection)
st.markdown("""
<style>
    /* Main Background & Font Tweaks */
    .stApp {
        background-color: #0e1117;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hero Banner Styling */
    .hero-container {
        background: linear-gradient(135deg, #0d3b66 0%, #001f3f 50%, #004d40 100%);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .hero-title {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        color: #00e676;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0px;
    }
    
    /* Custom Badge Indicator */
    .status-badge {
        background-color: rgba(0, 230, 118, 0.15);
        color: #00e676;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(0, 230, 118, 0.3);
        display: inline-block;
    }
    
    /* Card Container for Venue Photos & Components */
    .court-card {
        background-color: #1a1f2c;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #2d3748;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Metric Card Polish */
    [data-testid="stMetricValue"] {
        font-weight: 700 !important;
        color: #00e676 !important;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header Component
st.markdown("""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div class="hero-title">🎾 Lagos Tennis Connect</div>
            <div class="hero-subtitle">The premier digital hub for tennis players across Lagos, Nigeria</div>
        </div>
        <div style="margin-top: 10px;">
            <span class="status-badge">● Active Season 2026</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Styling & Navigation
st.sidebar.image("https://img.icons8.com/color/96/tennis-.png", width=65)
st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Choose a Module:",
    [
        "📅 Court Bookings",
        "🏆 Ladder & Rankings",
        "👀 Match Spectators",
        "📰 Tennis News & Scores",
        "🎁 Referrals & Rewards"
    ]
)

st.sidebar.divider()

# User Profile Card in Sidebar
with st.sidebar.container():
    st.markdown("### 👤 Player Profile")
    st.caption("**John O.** | Rating: **7.8 UTR**")
    st.caption("📍 Home Club: *Nicon Town Courts, Lekki*")

st.sidebar.divider()
st.sidebar.caption("⚡ Powered by Streamlit & Paystack Engine")

# Route Selected Module
if page == "📅 Court Bookings":
    render_booking_system()

elif page == "🏆 Ladder & Rankings":
    render_ladder()

elif page == "👀 Match Spectators":
    render_spectator_hub(current_user="John O.")

elif page == "📰 Tennis News & Scores":
    render_tennis_news_hub()

elif page == "🎁 Referrals & Rewards":
    render_referral_hub()