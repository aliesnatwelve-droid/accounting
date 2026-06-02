import streamlit as st
import sqlite3
from datetime import datetime
from database import init_db
import streamlit as st

# مخفی کردن سایدبار ناوبری پیش‌فرض
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* مخفی کردن منوی اصلی */
    #MainMenu {
        visibility: hidden;
    }
    
    /* مخفی کردن footer */
    footer {
        visibility: hidden;
    }
    
    /* مخفی کردن header */
    header {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)
# Initialize database
init_db()

st.set_page_config(page_title="Accounting Dashboard", layout="wide")

# Sidebar navigation
st.sidebar.title("ACCOUNTING DASHBOARD")
st.sidebar.markdown("---")

# Navigation buttons
pages = {
    " HOME": "home",
    " CALENDAR": "calendar", 
    " ANALYSIS": "analysis",
    " CATEGORIES": "categories"
}

for label, page in pages.items():
    if st.sidebar.button(label, use_container_width=True, key=f"nav_{page}"):
        st.session_state.current_page = page
        st.rerun()

st.sidebar.markdown("---")

# Show user info
st.sidebar.info("💡 Accounting Dashboard\n\nTrack your finances easily")

# Default page
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Page routing
if st.session_state.current_page == "home":
    import pages.home as home
    home.show()
elif st.session_state.current_page == "calendar":
    import pages.calender as calendar
    calendar.show()
elif st.session_state.current_page == "analysis":
    import pages.analysis as analysis
    analysis.show()
elif st.session_state.current_page == "categories":
    import pages.categories as categories
    categories.show()