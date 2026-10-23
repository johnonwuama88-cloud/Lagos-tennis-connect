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

# High-Contrast Custom Styling (CSS Injection)
st.markdown("""
<style>
    /* Global App Background & High-Contrast Text */
    .stApp {
        background-color: #111827;
        color: #f9fafb !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Ensure all markdown text and paragraphs are bright and legible */
    p, span, label, .stMarkdown, div {
        color: #f3f4f6 !important;
    }
    
    /* Hero Banner Styling */
    .hero-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #111827 60%, #065f46 100%);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        border: 1px solid #374151;
    }
    
    .hero-title {
        color: #ffffff !important;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        color: #34d399 !important;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0px;
    }
    
    /* Custom Status Badge */
    .status-badge {
        background-color: rgba(52, 211, 153, 0.2);
        color: #34d399 !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        border: 1px solid #34d399;
        display: inline-block;
    }
    
    /* Metric Card Polish */
    [data-testid="stMetricValue"] {
        font-weight: 800 !important;
        color: #34d399 !important;
    }
    
    /* Sidebar Styling Override */
    [data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid #1f2937;
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

# Sidebar Navigation
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