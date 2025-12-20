import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The Masters Vault", page_icon="🗝️", layout="centered")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&display=swap');

    /* --- GLOBAL --- */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000 80%);
    }

    /* --- SIDEBAR STYLING (NEW) --- */
    /* 1. The Container */
    [data-testid="stSidebar"] {
        background-color: #080808; /* Darker than main content */
        border-right: 1px solid #1e3a2a; /* Dim Emerald Border */
    }

    /* 2. The Navigation Links */
    [data-testid="stSidebarNav"] {
        font-family: 'Cinzel', serif;
        padding-top: 2rem;
    }
    
    /* 3. Link Text (Normal State) */
    [data-testid="stSidebarNav"] span {
        color: #666;
        font-size: 1rem;
        letter-spacing: 2px;
        transition: color 0.3s;
    }

    /* 4. Link Text (Hover State) */
    [data-testid="stSidebarNav"] a:hover span {
        color: #50c878; /* Emerald Glow */
    }

    /* 5. Active Page (The one you are currently on) */
    [data-testid="stSidebarNav"] [aria-current="page"] span {
        color: #66ff99 !important;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(80, 200, 120, 0.4);
    }
    
    /* Hide the default top colored bar if present */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* --- HOME TITLE --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 8px;
        font-size: 3.5rem !important;
        color: #e0e0e0 !important;
        text-align: center;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        margin-top: 2rem;
    }
    
    .subtitle {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.4rem;
        color: #888;
        text-align: center;
        font-style: italic;
        margin-bottom: 4rem;
    }

    /* --- NAVIGATION CARDS --- */
    /* (Streamlit Native Link Styling) */
    div[data-testid="stPageLink-NavLink"] {
        background-color: #0e0e0e;
        border: 1px solid #333;
        border-radius: 4px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 150px; /* Fixed Height */
    }
    
    div[data-testid="stPageLink-NavLink"]:hover {
        border-color: #50c878;
        background-color: #111;
        transform: translateY(-5px);
        box-shadow: 0 0 30px rgba(80, 200, 120, 0.1);
    }
    
    /* Icon styling */
    div[data-testid="stPageLink-NavLink"] p {
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        letter-spacing: 2px;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. LAYOUT
# -----------------------------------------------------------------------------
st.markdown("<h1>THE MASTER'S VAULT</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A digital grimoire for the architect of worlds.</div>", unsafe_allow_html=True)

# Spacing
st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. NAVIGATION TILES
# -----------------------------------------------------------------------------
col1, col2 = st.columns(2)

# TILE 1: THE FORGE
with col1:
    # Ensure this string matches YOUR server filename exactly (1_The Forge.py or 1_the_forge.py)
    st.page_link("pages/1_the_forge.py", label="ENTER THE FORGE", icon="⚒️", use_container_width=True)
    st.markdown("""
        <div style="text-align: center; color: #666; font-family: 'Cormorant Garamond'; font-style: italic; margin-top: 10px;">
            Strike the iron. Breathe life into the void. <br>Create new souls for your world.
        </div>
    """, unsafe_allow_html=True)

# TILE 2: THE ARCHIVES
with col2:
    st.page_link("pages/2_library.py", label="OPEN THE ARCHIVES", icon="📜", use_container_width=True)
    st.markdown("""
        <div style="text-align: center; color: #666; font-family: 'Cormorant Garamond'; font-style: italic; margin-top: 10px;">
            That which is remembered, lives forever. <br>View and manage your creation.
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; opacity: 0.3;'>ᛯ</div>", unsafe_allow_html=True)