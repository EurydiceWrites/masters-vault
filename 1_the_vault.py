import streamlit as st

import utils.styles as styles

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The Master's Vault", page_icon="🗝️", layout="wide")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (PREMIUM CSS)
# -----------------------------------------------------------------------------
styles.load_css()

# -----------------------------------------------------------------------------
# 3. LAYOUT
# -----------------------------------------------------------------------------
st.markdown("<h1>THE MASTER'S VAULT</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Where imagination meets the void.</div>", unsafe_allow_html=True)

# CSS to fix the left-alignment of st.page_link and make them look like headers
st.markdown("""
<style>
    section[data-testid="stMain"] a[data-testid="stPageLink-NavLink"] {
        display: flex !important;
        justify-content: center !important;
        text-decoration: none !important;
    }
    section[data-testid="stMain"] a[data-testid="stPageLink-NavLink"] p {
        font-family: 'Cinzel', serif !important;
        font-size: 1.6rem !important;
        color: #e0e0e0 !important;
        letter-spacing: 3px !important;
        text-transform: uppercase !important;
        text-align: center !important;
        transition: color 0.3s ease !important;
    }
    section[data-testid="stMain"] a[data-testid="stPageLink-NavLink"]:hover p {
        color: #50c878 !important;
        text-shadow: 0 0 15px rgba(80, 200, 120, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Grid
col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/2_well_of_souls.py", label="THE WELL OF SOULS", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>Conjure an NPC</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.page_link("pages/4_the_forge.py", label="THE FORGE", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>Forge an Artifact</p>", unsafe_allow_html=True)

with col2:
    st.page_link("pages/3_npc_archives.py", label="NPC ARCHIVES", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>View the Souls</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.page_link("pages/5_item_archives.py", label="THE RELIQUARY", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cormorant Garamond; font-size: 1rem; margin-top: -15px;'>Inspect the Reliquary</p>", unsafe_allow_html=True)

# Footer
runes = ["ᚠ", "ᚢ", "ᚦ", "ᚨ", "ᚱ", "ᚲ", "ᚷ", "ᚹ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    delay = i * 0.3
    rune_html += f"<span class='rune-span' style='animation-delay: {delay}s'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)