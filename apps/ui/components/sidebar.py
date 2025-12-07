import sys
from pathlib import Path
import streamlit as st
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
from apps.ui.services.system import SystemService


def get_api_status() -> bool:
    """
    Checks API health.
    Uses SystemService which is now internally cached.
    """
    service = SystemService()
    try:
        data = service.get_health_status()
        return data is not None and data.get("status") == "ok"
    except Exception:
        return False


def render_global_sidebar(pages_structure):
    """
    Renders the global application sidebar (Layout).

    Args:
        pages_structure: The dictionary or list of st.Page objects used in main.py
    """
    is_online = get_api_status()
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
    with st.sidebar:
        if logo_path.exists():
            st.image(str(logo_path), width=50)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/3448/3448609.png", width=50)
        st.title("Restaurant OS")
        with st.container(border=True):
            st.caption("System Status")
            col_icon, col_text = st.columns([1, 4])
            with col_icon:
                if is_online:
                    st.write("🟢")
                else:
                    st.write("🔴")
            with col_text:
                if is_online:
                    st.write("**Online**")
                else:
                    st.error("**Offline**")

        st.divider()
        st.subheader("Navigation")
        if isinstance(pages_structure, dict):
            for section_name, pages in pages_structure.items():
                st.caption(section_name.upper())
                for page in pages:
                    st.page_link(page)
        else:
            for page in pages_structure:
                st.page_link(page)
        st.divider()
        st.info("💡 Tip: Use 'R' to refresh.")