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

# Entrance styling: themed doors, hall headers, and door captions.
st.markdown("""
<style>
    section[data-testid="stMain"] a[data-testid="stPageLink-NavLink"] {
        display: flex !important;
        justify-content: center !important;
        text-decoration: none !important;
    }
    section[data-testid="stMain"] a[data-testid="stPageLink-NavLink"] p {
        font-family: 'Cinzel', serif !important;
        font-size: 1.3rem !important;
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
    .hall-header {
        font-family: 'Cinzel', serif;
        color: #66ff99;
        text-transform: uppercase;
        letter-spacing: 5px;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 0.8rem;
        padding-bottom: 0.7rem;
        border-bottom: 1px solid #1e3a2a;
    }
    .door-caption {
        text-align: center;
        color: #666;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        margin-top: -15px;
        margin-bottom: 1.4rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. THE HALLS — each pairs a maker with its archive
# -----------------------------------------------------------------------------
hall_souls, hall_armory, hall_wilds = st.columns(3)

with hall_souls:
    st.markdown("<div class='hall-header'>The Souls</div>", unsafe_allow_html=True)
    st.page_link("pages/2_well_of_souls.py", label="THE WELL OF SOULS", use_container_width=True)
    st.markdown("<p class='door-caption'>Conjure an NPC</p>", unsafe_allow_html=True)
    st.page_link("pages/3_npc_archives.py", label="NPC ARCHIVES", use_container_width=True)
    st.markdown("<p class='door-caption'>View the Souls</p>", unsafe_allow_html=True)

with hall_armory:
    st.markdown("<div class='hall-header'>The Armory</div>", unsafe_allow_html=True)
    st.page_link("pages/4_the_forge.py", label="THE FORGE", use_container_width=True)
    st.markdown("<p class='door-caption'>Forge an Artifact</p>", unsafe_allow_html=True)
    st.page_link("pages/5_item_archives.py", label="THE RELIQUARY", use_container_width=True)
    st.markdown("<p class='door-caption'>Inspect the Reliquary</p>", unsafe_allow_html=True)

with hall_wilds:
    st.markdown("<div class='hall-header'>The Wilds</div>", unsafe_allow_html=True)
    st.page_link("pages/7_the_menagerie.py", label="THE MENAGERIE", use_container_width=True)
    st.markdown("<p class='door-caption'>Summon a Creature</p>", unsafe_allow_html=True)
    st.page_link("pages/8_the_bestiary.py", label="THE BESTIARY", use_container_width=True)
    st.markdown("<p class='door-caption'>Catalogue of Beasts</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# The Pitch stands alone
col_l, col_c, col_r = st.columns([1, 1, 1])
with col_c:
    st.page_link("pages/6_the_pitch.py", label="THE PITCH", use_container_width=True)
    st.markdown("<p class='door-caption'>The Vision</p>", unsafe_allow_html=True)

# Footer
runes = ["ᚹ", "ᚺ", "ᚨ", "ᛏ", "᛫", "ᚹ", "ᛖ", "ᚱ", "ᛖ", "᛫", "ᚹ", "ᛖ", "᛫", "ᚹ", "ᛖ", "ᚨ", "ᚱ", "ᛁ", "ᚾ", "ᚷ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    delay = i * 0.3
    rune_html += f"<span class='rune-span' style='animation-delay: {delay}s'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)
