import streamlit as st

# -----------------------------------------------------------------------------
# 1. SETUP & CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Master's Vault", layout="centered", page_icon="🗝️")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (Ancient Stone Theme)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;800&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #1c1c1c;
        --stone-dark: #111111;
        --emerald-glow: #50c878;
        --emerald-dim: #2e5a44;
        --text-main: #d0d0d0;
    }

    /* --- BACKGROUND --- */
    .stApp {
        background-color: var(--stone-dark);
        background-image: radial-gradient(circle at center, #252525 0%, #0a0a0a 100%);
        color: var(--text-main);
        font-family: 'Lato', sans-serif;
    }

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 8px;
        font-size: 3.5rem !important;
        color: var(--emerald-glow) !important;
        text-shadow: 0 5px 15px rgba(0,0,0,0.8);
        text-align: center;
        margin-bottom: 2rem !important;
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 2rem;
    }

    /* --- SUBTEXT --- */
    .subtext {
        text-align: center;
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        color: #888;
        letter-spacing: 4px;
        margin-bottom: 4rem; 
        text-transform: uppercase;
    }

    /* --- NAVIGATION TABLETS (Styling the Links) --- */
    /* This targets the page_link buttons to make them look like stone slabs */
    a[data-testid="stPageLink-NavLink"] {
        background-color: #1a2e25;
        border: 1px solid #2e5a44;
        border-left: 4px solid var(--emerald-glow); /* Accent on left */
        padding: 2rem;
        border-radius: 4px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }

    a[data-testid="stPageLink-NavLink"]:hover {
        background-color: #2e5a44;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.7);
        border-color: var(--emerald-glow);
    }

    /* Text inside the links */
    a[data-testid="stPageLink-NavLink"] p {
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #e0e0e0;
        letter-spacing: 2px;
    }
    
    /* Remove default Streamlit icons/decorations if any */
    [data-testid="stPageLink-NavLink"] img {
        filter: grayscale(100%) brightness(1.2);
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. MAIN LAYOUT
# -----------------------------------------------------------------------------

# HEADER
st.markdown("<h1>THE MASTER'S VAULT</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>SELECT YOUR MODULE</div>", unsafe_allow_html=True)

# NAVIGATION COLUMNS
col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/npc_forge.py", label="THE NPC FORGE", icon="⚒️", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 10px;'>Summon Characters & Lore</p>", unsafe_allow_html=True)

with col2:
    st.page_link("pages/art_studio.py", label="THE ART STUDIO", icon="🎨", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 10px;'>Manifest Visuals & items</p>", unsafe_allow_html=True)

# FOOTER DECORATION
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; opacity: 0.3; letter-spacing: 1rem; color: #50c878;'>ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ</div>", unsafe_allow_html=True)