import streamlit as st
from config.settings import PAGE_TITLE, LOGO_PATH, LAYOUT, SIDEBAR_STATE, CSS_PATH, MENU
from streamlit_option_menu import option_menu
from pages.dashboard import run_dashboard
from pages.about import run_about

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=str(LOGO_PATH),
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

# ── CSS ─────────────────────────────────────────────────────────────────────
@st.cache_data
def get_css():
    return CSS_PATH.read_text()
try:
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.warning(f"CSS failed: {e}")

# ── Navigation ───────────────────────────────────────────────────────────────
handlers = {
    "dashboard": run_dashboard,
    "about": run_about,
}

choice = option_menu(
    PAGE_TITLE,
    options=list(MENU.keys()),
    icons=[item["icon"] for item in MENU.values()],
    orientation="horizontal",
    menu_icon="dice-4-fill",
    default_index=0,
    styles={
        "nav-link": {"font-size": "12px"},
        "nav-link-selected": {"background-color": "green"},
    }
)

handler_key = MENU[choice]["handler_name"]
handler = handlers.get(handler_key)

if handler:
    handler()
else:
    st.error(f"No handler found for {choice}")