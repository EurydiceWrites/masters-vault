import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The Master's Vault", page_icon="🗝️", layout="wide")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (GLOBAL CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #111;
        --emerald-glow: #50c878;
        --emerald-bright: #66ff99;
        --emerald-dim: #1e3a2a;
        --nav-gold: #d4af37; 
        --gold-glow: rgba(212, 175, 55, 0.6);
    }

    /* --- GLOBAL --- */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000 80%);
    }

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] { background-color: #080808; border-right: 1px solid #1e3a2a; }
    
    /* Sidebar Links */
    [data-testid="stSidebarNav"] a {
        font-family: 'Cinzel', serif !important;
        color: #888 !important;
        transition: color 0.3s ease;
    }
    [data-testid="stSidebarNav"] a:hover {
        color: var(--nav-gold) !important;
        text-shadow: 0 0 10px var(--gold-glow);
    }

    /* --- HEADERS --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 12px;
        font-size: 3.5rem !important;
        color: var(--emerald-bright) !important;
        text-shadow: 0 0 30px rgba(102, 255, 153, 0.4);
        text-align: center;
        margin-top: 2rem !important;
    }
    h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: #ddd !important;
        text-align: center;
    }

    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.4rem;
        color: #888;
        font-style: italic;
        margin-bottom: 4rem;
    }

    /* --- BUTTONS (BIG NAVIGATION) --- */
    .nav-card {
        background: #0e0e0e;
        border: 1px solid #333;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border-radius: 2px;
    }
    .nav-card:hover {
        border-color: var(--emerald-glow);
        box-shadow: 0 0 20px rgba(80, 200, 120, 0.2);
        transform: translateY(-5px);
    }
    .nav-title {
        font-family: 'Cinzel', serif;
        font-size: 1.8rem;
        color: #fff;
        margin-bottom: 1rem;
    }
    .nav-desc {
        font-family: 'Lato', sans-serif;
        font-size: 1rem;
        color: #888;
    }
    
    /* --- FOOTER --- */
    .footer-container { opacity: 0.3; text-align: center; margin-top: 6rem; padding-bottom: 2rem;}
    .rune-span { margin: 0 10px; font-size: 1.2rem; color: #444; cursor: default; }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. LAYOUT
# -----------------------------------------------------------------------------
st.markdown("<h1>THE MASTER'S VAULT</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>The gateway to worlds unborn and souls remembered.</div>", unsafe_allow_html=True)

# Navigation Grid
col1, col2 = st.columns(2)

with col1:
    if st.button("THE FORGE \n(Create New Souls)", type="primary", use_container_width=True):
        st.switch_page("pages/forge.py")

with col2:
    if st.button("THE ARCHIVES \n(View The Lost)", type="primary", use_container_width=True):
        st.switch_page("pages/library.py")

# Footer
runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)