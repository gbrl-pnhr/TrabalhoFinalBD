import streamlit as st


def render_sidebar(page_name: str):
    """
    Renders the global sidebar content.
    """
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3448/3448609.png", width=50)
        st.title("Restaurant OS")
        st.markdown(f"**Current Page:** {page_name}")
        st.divider()
        st.subheader("System Status")
        st.caption("Backend API")
        st.success("● Online")
        st.caption("Database")
        st.success("● Connected")
        st.divider()
        st.info("💡 Tip: Use 'R' to refresh any page.")