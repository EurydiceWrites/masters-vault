import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="The Master's Vault",
    page_icon="🗝️",
    layout="centered"
)

# --- DESIGN & UX OVERRIDES (EMERALD THEME) ---
st.markdown("""
<style>
    /* 1. IMPORTS: CINZEL (Fantasy Header Font) */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Roboto:wght@300;400&display=swap');

    /* 2. BACKGROUND: The Void */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at center, #111e17 0%, #050505 100%);
        color: #dcdcdc;
    }

    /* 3. HEADERS: Norse/Emerald Style */
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: #50c878 !important; /* Emerald Green Text */
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0px 0px 10px rgba(80, 200, 120, 0.3);
    }

    /* 4. INFO BOXES (System Status) */
    .stAlert {
        background-color: #0b3d26;
        color: #e8f5e9;
        border: 1px solid #50c878;
    }

    /* 5. BUTTONS/LINKS: The Emerald Gem */
    /* This targets the page_link buttons specifically */
    button[kind="secondary"] {
        background-color: #0b3d26 !important;
        color: #e8f5e9 !important;
        font-family: 'Cinzel', serif !important;
        border: 1px solid #145235 !important;
        transition: all 0.3s ease;
    }
    button[kind="secondary"]:hover {
        background-color: #145235 !important;
        border-color: #50c878 !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(80, 200, 120, 0.5);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN CONTENT ---
st.title("🗝️ The Master's Vault")

# The info box will now look like a magical HUD element due to the CSS above
st.info("System Status: Online | Welcome, Master.")

st.markdown("---")

# Use Columns to create a side-by-side layout for your buttons
col1, col2 = st.columns(2)

with col1:
    st.header("🛡️ NPC Forge")
    st.write("Generate complete characters: Name, Class, Backstory, and Visuals.")
    # This creates the button
    st.page_link("pages/npc_forge.py", label="Enter the Forge", icon="🔥", use_container_width=True)

with col2:
    st.header("🎨 Art Studio")
    st.write("Generate high-fidelity visuals: Landscapes, Items, and Monsters.")
    # This creates the button
    st.page_link("pages/art_studio.py", label="Enter the Studio", icon="🎨", use_container_width=True)

st.markdown("---")
st.caption("© 2025 Project Mind's Eye | Operational Guide v1.0")