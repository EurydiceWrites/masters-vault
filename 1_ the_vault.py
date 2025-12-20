import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Master's Vault", layout="centered", page_icon="⚔️")

# -----------------------------------------------------------------------------
# 2. CSS STYLING (The Theme Engine)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;800&family=Cormorant+Garamond:wght@400;600&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #1c1c1c; 
        --stone-dark: #0e0e0e; 
        --emerald-glow: #50c878; 
        --emerald-dim: #2e5a44; 
        --text-main: #d0d0d0; 
        --text-muted: #888;
    }

    /* --- BACKGROUND --- */
    .stApp {
        background-color: var(--stone-dark);
        background-image: radial-gradient(circle at 50% 30%, #252525 0%, #000 100%);
        color: var(--text-main); 
        font-family: 'Lato', sans-serif;
    }

    /* --- SIDEBAR STYLING (ADDED) --- */
    [data-testid="stSidebar"] {
        background-color: #080808; 
        border-right: 1px solid #1e3a2a;
    }
    [data-testid="stSidebarNav"] {
        font-family: 'Cinzel', serif;
        padding-top: 2rem;
    }
    [data-testid="stSidebarNav"] span {
        color: #666;
        font-size: 1rem;
        letter-spacing: 2px;
        transition: color 0.3s;
    }
    [data-testid="stSidebarNav"] a:hover span {
        color: #50c878; /* Emerald Glow */
    }
    [data-testid="stSidebarNav"] [aria-current="page"] span {
        color: #66ff99 !important;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(80, 200, 120, 0.4);
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important; 
        text-transform: uppercase; 
        letter-spacing: 12px; 
        font-size: 3.8rem !important;
        color: var(--emerald-glow) !important; 
        text-shadow: 0 0 20px rgba(80, 200, 120, 0.2); 
        text-align: center;
        margin-bottom: 1rem !important; 
        border-bottom: 1px solid var(--emerald-dim); 
        padding-bottom: 2rem;
    }

    .subtext {
        text-align: center; 
        font-family: 'Cormorant Garamond', serif; 
        font-size: 1.3rem; 
        font-style: italic;
        color: var(--text-muted); 
        letter-spacing: 2px; 
        margin-bottom: 5rem; 
    }

    /* --- NAVIGATION CARDS --- */
    a[data-testid="stPageLink-NavLink"] {
        background: linear-gradient(145deg, #1f2220, #151515); 
        border: 1px solid #333; 
        border-left: 3px solid var(--emerald-dim);
        padding: 2.5rem 1.5rem; 
        border-radius: 2px; 
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        box-shadow: 0 10px 20px rgba(0,0,0,0.5); 
        text-align: center; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        z-index: 10; 
        position: relative;
    }

    a[data-testid="stPageLink-NavLink"]:hover {
        background: linear-gradient(145deg, #252b27, #1a1a1a); 
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 30px rgba(0,0,0,0.8), 0 0 25px rgba(80, 200, 120, 0.2); 
        border-color: var(--emerald-glow); 
        border-left: 3px solid var(--emerald-glow);
    }

    a[data-testid="stPageLink-NavLink"] p {
        font-family: 'Cinzel', serif; 
        font-size: 1.6rem; 
        font-weight: 700; 
        color: #e0e0e0; 
        letter-spacing: 3px; 
        margin: 0; 
        transition: color 0.3s ease;
    }

    a[data-testid="stPageLink-NavLink"]:hover p { 
        color: var(--emerald-glow); 
        text-shadow: 0 0 10px rgba(80, 200, 120, 0.6); 
    }

    /* Hide default icons in links if any appear */
    [data-testid="stPageLink-NavLink"] img { display: none; }

    /* --- FOOTER RUNES --- */
    .footer-container { 
        display: flex; 
        justify-content: center; 
        gap: 1.5rem; 
        margin-top: 5rem; 
        position: relative; 
        z-index: 999; 
    }

    .rune-span {
        font-size: 1.8rem; 
        color: var(--emerald-dim); 
        opacity: 0.3; 
        user-select: none; 
        cursor: pointer; 
        padding: 10px; 
        transition: all 0.1s ease; 
        animation: rune-glow 3s infinite ease-in-out;
    }

    .rune-span:hover {
        animation-play-state: paused; 
        color: var(--emerald-glow) !important; 
        opacity: 1 !important; 
        text-shadow: 0 0 10px var(--emerald-glow), 0 0 20px var(--emerald-glow), 0 0 40px var(--emerald-glow) !important; 
        transform: scale(1.3) !important;
    }

    @keyframes rune-glow {
        0%, 100% { color: var(--emerald-dim); opacity: 0.3; text-shadow: none; transform: scale(1); }
        50% { color: var(--emerald-glow); opacity: 0.8; text-shadow: 0 0 15px var(--emerald-dim); transform: scale(1.1); }
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

# --- THE FIX: Pointing to the CORRECT file paths you have now ---
with col1:
    st.page_link("pages/1_the_forge.py", label="THE FORGE", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>Strike the Iron</p>", unsafe_allow_html=True)

with col2:
    st.page_link("pages/2_library.py", label="THE ARCHIVES", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>View the Souls</p>", unsafe_allow_html=True)

# Footer
runes = ["ᚠ", "ᚢ", "ᚦ", "ᚨ", "ᚱ", "ᚲ", "ᚷ", "ᚹ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    delay = i * 0.2
    rune_html += f"<span class='rune-span' style='animation-delay: {delay}s'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)