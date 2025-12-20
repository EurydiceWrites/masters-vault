import streamlit as st

# -----------------------------------------------------------------------------
# 1. SETUP & CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Master's Vault", layout="centered", page_icon="⚔️")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (Refined Ancient Stone)
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

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 12px; /* Wider for more epic feel */
        font-size: 3.8rem !important;
        color: var(--emerald-glow) !important;
        text-shadow: 0 0 20px rgba(80, 200, 120, 0.2);
        text-align: center;
        margin-bottom: 1rem !important;
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 2rem;
    }

    /* --- SUBTEXT --- */
    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif; /* More book-like font */
        font-size: 1.3rem;
        font-style: italic;
        color: var(--text-muted);
        letter-spacing: 2px;
        margin-bottom: 5rem; 
    }

    /* --- STONE TABLET NAVIGATION (No Emojis) --- */
    /* We style the link container to look like a heavy slab */
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
    }

    /* Hover State: The Emerald Awakening */
    a[data-testid="stPageLink-NavLink"]:hover {
        background: linear-gradient(145deg, #252b27, #1a1a1a);
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 30px rgba(0,0,0,0.8), 0 0 15px rgba(80, 200, 120, 0.1);
        border-color: var(--emerald-glow);
        border-left: 3px solid var(--emerald-glow);
    }

    /* The Title Text inside the Tablet */
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
    }

    /* Hiding the default Streamlit Icon to remove "Amateur" feel */
    [data-testid="stPageLink-NavLink"] img {
        display: none;
    }
    
    /* --- CUSTOM ICON REPLACEMENT (Pseudo-elements) --- */
    /* We can't easily inject icons via CSS into Streamlit links, 
       so we rely on the clean typography and borders. */

    /* --- FOOTER RUNES --- */
    .footer-runes {
        text-align: center;
        opacity: 0.2;
        letter-spacing: 1.5rem;
        color: var(--emerald-glow);
        font-size: 1.2rem;
        margin-top: 5rem;
        user-select: none;
        cursor: default;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. MAIN LAYOUT
# -----------------------------------------------------------------------------

# HEADER
st.markdown("<h1>THE MASTER'S VAULT</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Where imagination meets the void.</div>", unsafe_allow_html=True)

# NAVIGATION COLUMNS
col1, col2 = st.columns(2)

with col1:
    # Notice: No icon="..." parameter. We are letting the CSS do the work.
    st.page_link("pages/npc_forge.py", label="NPC FORGE", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>Soul & Story</p>", unsafe_allow_html=True)

with col2:
    st.page_link("pages/art_studio.py", label="ART STUDIO", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>Visuals & Items</p>", unsafe_allow_html=True)

# FOOTER DECORATION
st.markdown("<div class='footer-runes'>ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ</div>", unsafe_allow_html=True)