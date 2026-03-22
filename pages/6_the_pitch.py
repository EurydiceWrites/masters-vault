import streamlit as st
import streamlit.components.v1 as components
import os

import utils.styles as styles

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The Pitch", page_icon="🎮")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (CSS)
# -----------------------------------------------------------------------------
styles.load_css()

# -----------------------------------------------------------------------------
# 3. LAYOUT
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO HALL", use_container_width=False)

st.markdown("<h1>THE PITCH</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>A vision, forged in fire and code.</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. LOAD & EMBED THE PITCH HTML FILES
# -----------------------------------------------------------------------------
PITCH_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pitch")

def load_html(filename):
    """Reads a pitch HTML file and wraps it with a dark background for the iframe."""
    filepath = os.path.join(PITCH_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Wrap in a full HTML page with dark background to match the app theme
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0; padding:0; background:#0a0a0c; color:#c8c8c0;">
{content}
</body></html>"""

# Tabs for the two pitch boards
tab1, tab2 = st.tabs(["⚔️ THE SEVEN AGES", "🕳️ THE UNDERWORLD"])

with tab1:
    html_phases = load_html("ascension_seven_phases_green_red.html")
    components.html(html_phases, height=1800, scrolling=True)

with tab2:
    html_underworld = load_html("ascension_underworld_green_red.html")
    components.html(html_underworld, height=2200, scrolling=True)

# Footer
runes = ["ᚠ", "ᚢ", "ᚦ", "ᚨ", "ᚱ", "ᚲ", "ᚷ", "ᚹ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    delay = i * 0.3
    rune_html += f"<span class='rune-span' style='animation-delay: {delay}s'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)

