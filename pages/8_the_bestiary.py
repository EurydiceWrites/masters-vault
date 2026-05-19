import streamlit as st
import pandas as pd
import html

import utils.styles as styles
from services import db_service

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The Bestiary", page_icon="📖", layout="wide")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE
# -----------------------------------------------------------------------------
styles.load_css()

# -----------------------------------------------------------------------------
# 3. FETCH DATA
# -----------------------------------------------------------------------------
try:
    df = db_service.get_all_creatures()
except Exception as e:
    st.error(f"Could not read from the Vault: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 4. LAYOUT
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO VAULT", use_container_width=False)

st.markdown("<h1>THE BESTIARY</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Every beast ever summoned — caged, catalogued, kept.</div>", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-header">Filter the Bestiary</div>', unsafe_allow_html=True)

# --- FILTERS ---
if not df.empty and 'Tone' in df.columns:
    unique_tones = sorted([str(x) for x in df['Tone'].unique() if str(x).strip() and str(x).lower() != "nan"])
    sel_tone = st.sidebar.selectbox("Resonance", ["All"] + unique_tones)
else:
    sel_tone = "All"

search_query = st.text_input("Search the Bestiary", placeholder="Search by description...")

filtered_df = df.copy()
if sel_tone != "All" and 'Tone' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Tone'].astype(str) == sel_tone]
if search_query and 'Concept' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Concept'].astype(str).str.contains(search_query, case=False, na=False)]

# --- GRID ---
MAX_DISPLAY = 30

if filtered_df.empty:
    st.markdown(
        "<div class='subtext'>The Bestiary is empty. Summon your first beast in The Menagerie.</div>",
        unsafe_allow_html=True,
    )
else:
    if 'Timestamp' in filtered_df.columns:
        filtered_df['_ts'] = pd.to_datetime(filtered_df['Timestamp'], errors='coerce')
        filtered_df = filtered_df.sort_values(by='_ts', ascending=False)
    else:
        filtered_df = filtered_df.iloc[::-1]

    display_df = filtered_df.head(MAX_DISPLAY)
    cols = st.columns(3)

    for i, (_, row) in enumerate(display_df.iterrows()):
        original = str(row.get('Image_URL', ''))
        if original.startswith("http"):
            thumb = original
            if "cloudinary" in thumb and "/upload/" in thumb:
                thumb = thumb.replace("/upload/", "/upload/c_fill,g_auto,w_400,h_533,q_auto,f_auto/")
        else:
            original = "https://via.placeholder.com/400x533?text=No+Visage"
            thumb = original

        raw_concept = str(row.get('Concept', ''))
        if len(raw_concept) > 75:
            raw_concept = raw_concept[:72] + "..."
        concept = html.escape(raw_concept)
        tone = html.escape(str(row.get('Tone', '')))

        with cols[i % 3]:
            card = (
                '<div class="archive-card">'
                '<div class="img-frame">'
                f'<a href="{original}" target="_blank" style="display:block; width:100%; height:100%;">'
                f'<img src="{thumb}" loading="lazy"></a>'
                '</div>'
                '<div class="card-identity">'
                '<div class="identity-top">'
                '<div style="font-family:Cormorant Garamond,serif; font-style:italic; '
                f'color:#aaa; font-size:1.05rem; line-height:1.4; text-align:center; padding:0 0.6rem;">{concept}</div>'
                '</div>'
                '<div class="pill-container">'
                f'<div class="pill-base pill-metal">{tone}</div>'
                '</div>'
                '</div>'
                '</div>'
            )
            st.markdown(card, unsafe_allow_html=True)
