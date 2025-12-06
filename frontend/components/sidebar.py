import streamlit as st
from services.system import SystemService


@st.cache_data(ttl=30, show_spinner=False)
def get_api_status() -> bool:
    """
    Checks the API health status with a 30-second cache.
    Returns True if online, False otherwise.
    """
    service = SystemService()
    try:
        data = service.get_health_status()
        return data is not None and data.get("status") == "ok"
    except Exception:
        return False


def render_sidebar(page_name: str):
    """
    Renders the global sidebar content with real-time status checks.
    """
    is_online = get_api_status()
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3448/3448609.png", width=50)
        st.title("Restaurant OS")
        st.markdown(f"**Current Page:** {page_name}")
        st.divider()
        st.subheader("System Status")
        st.caption("Backend API")
        if is_online:
            st.success("● Online")
        else:
            st.error("● Offline")
        st.caption("Database")
        if is_online:
            st.success("● Connected")
        else:
            st.error("● Unreachable")
        st.divider()
        st.info("💡 Tip: Use 'R' to refresh any page.")