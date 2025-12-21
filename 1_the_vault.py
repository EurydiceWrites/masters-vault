import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The Master's Vault", page_icon="🗝️", layout="wide")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (PREMIUM CSS)
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

    /* --- GLOBAL BACKGROUND --- */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000 80%);
    }

    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] { 
        background-color: #080808; 
        border-right: 1px solid #1e3a2a; 
    }
    
    /* Custom Sidebar Header */
    .sidebar-header {
        font-family: 'Cinzel', serif;
        color: var(--emerald-bright);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        margin-top: 2rem;
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 0.5rem;
        text-align: center;
        text-shadow: 0 0 10px var(--emerald-dim);
    }

    /* Sidebar Navigation Links */
    [data-testid="stSidebarNav"] a {
        font-family: 'Cinzel', serif !important;
        color: #888 !important;
        transition: color 0.3s ease;
    }
    [data-testid="stSidebarNav"] a:hover {
        color: var(--nav-gold) !important;
        text-shadow: 0 0 10px var(--gold-glow);
    }

    /* --- MAIN HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 12px;
        font-size: 4rem !important;
        color: var(--emerald-bright) !important;
        text-shadow: 0 0 40px rgba(102, 255, 153, 0.4);
        margin-bottom: 0 !important;
        text-align: center;
        margin-top: 5vh !important;
    }
    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.5rem;
        color: #888;
        font-style: italic;
        margin-bottom: 5rem;
    }

    /* --- NAVIGATION CARDS (Restoring the Premium Look) --- */
    a[data-testid="stPageLink-NavLink"] {
        background: linear-gradient(145deg, #151515, #0a0a0a);
        border: 1px solid #333;
        border-left: 4px solid var(--emerald-dim);
        padding: 3rem 2rem;
        border-radius: 2px;
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 200px; /* Fixed Height for consistency */
    }

    /* Hover State */
    a[data-testid="stPageLink-NavLink"]:hover {
        background: linear-gradient(145deg, #1a1a1a, #111);
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0,0,0,1), 0 0 30px rgba(80, 200, 120, 0.1);
        border-color: var(--emerald-glow);
        border-left: 4px solid var(--emerald-bright);
    }

    /* The Text Inside the Link */
    a[data-testid="stPageLink-NavLink"] p {
        font-family: 'Cinzel', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #e0e0e0;
        letter-spacing: 4px;
        margin: 0;
        text-transform: uppercase;
        text-shadow: 0 2px 5px #000;
        transition: color 0.3s ease;
    }

    a[data-testid="stPageLink-NavLink"]:hover p {
        color: var(--emerald-bright);
        text-shadow: 0 0 15px var(--emerald-glow);
    }

    /* Hide default icons if they appear */
    [data-testid="stPageLink-NavLink"] img { display: none; }

    /* --- FOOTER RUNES --- */
    .footer-container { 
        display: flex; 
        justify-content: center; 
        gap: 2rem; 
        margin-top: 8rem; 
        padding-bottom: 2rem;
        opacity: 0.4;
    }

    .rune-span {
        font-size: 2rem; 
        color: var(--emerald-dim); 
        user-select: none; 
        cursor: default; 
        transition: all 0.5s ease; 
        animation: rune-glow 4s infinite ease-in-out;
    }

    @keyframes rune-glow {
        0%, 100% { color: var(--emerald-dim); text-shadow: none; transform: scale(1); }
        50% { color: var(--emerald-glow); text-shadow: 0 0 15px var(--emerald-dim); transform: scale(1.1); }
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. LAYOUT
# -----------------------------------------------------------------------------
st.markdown("<h1>THE MASTER'S VAULT</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Where imagination meets the void.</div>", unsafe_allow_html=True)

# Navigation Grid
col1, col2 = st.columns(2)

# Using st.page_link for the premium hover effect
with col1:
    st.page_link("pages/forge.py", label="THE FORGE", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>Strike the Iron</p>", unsafe_allow_html=True)

with col2:
    st.page_link("pages/library.py", label="THE ARCHIVES", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>View the Souls</p>", unsafe_allow_html=True)

# Footer
runes = ["ᚠ", "ᚢ", "ᚦ", "ᚨ", "ᚱ", "ᚲ", "ᚷ", "ᚹ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    delay = i * 0.3
    rune_html += f"<span class='rune-span' style='animation-delay: {delay}s'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)