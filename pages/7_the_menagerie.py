import streamlit as st
import datetime
import base64
import html

import utils.styles as styles
from services import llm_service, storage_service, db_service

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The Menagerie", layout="centered", page_icon="🐉")

if "creature_data" not in st.session_state:
    st.session_state.creature_data = None
if "last_creature_concept" not in st.session_state:
    st.session_state.last_creature_concept = ""

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE
# -----------------------------------------------------------------------------
styles.load_css()

# -----------------------------------------------------------------------------
# 3. CORE LOGIC
# -----------------------------------------------------------------------------
def conjure_creature(concept: str, tone: str):
    """Concept in, creature out: the Vault's eye sharpens it, the image model
    renders it, and it is caged in the Vault. Returns the result, or None on failure.
    """
    with st.spinner("The Menagerie stirs..."):
        try:
            description = llm_service.enhance_prompt(concept, "creature", tone)
            image_bytes = llm_service.generate_image(description, "creature", tone)
        except Exception as e:
            st.error(f"The beast would not take form: {e}")
            return None

    try:
        b64_encoded = base64.b64encode(image_bytes).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{b64_encoded}"
        image_url = storage_service.upload_image_to_cdn(data_uri, folder="The_Menagerie")
    except Exception:
        image_url = "Image Upload Failed"

    try:
        db_service.insert_creature(
            [concept, tone, image_url, str(datetime.datetime.now())]
        )
        st.session_state.db_status = "Success! The beast was caged in the Vault."
    except Exception as e:
        st.session_state.db_status = f"Vault Exception: {str(e)}"

    return {"concept": concept, "image_url": image_url}


def build_creature_card(data: dict) -> str:
    """The framed presentation: the conjured image, the concept inscribed beneath."""
    concept = html.escape(str(data.get("concept", "")))
    image_url = str(data.get("image_url", ""))

    if image_url.startswith("http"):
        portrait = (
            f'<a href="{image_url}" target="_blank">'
            f'<img src="{image_url}" title="Click to Expand"></a>'
        )
    else:
        portrait = "<div class='portrait-missing'>No Visage Found</div>"

    return (
        '<div class="character-card">'
        f'<div class="img-container">{portrait}</div>'
        f'<div class="visual-caption">"{concept}"</div>'
        '</div>'
    )

# -----------------------------------------------------------------------------
# 4. LAYOUT
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO VAULT", use_container_width=False)

st.markdown("<h1>THE MENAGERIE</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Summon the beasts that prowl the edges of the world.</div>", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-header">The Menagerie</div>', unsafe_allow_html=True)

with st.form("menagerie_form"):
    user_input = st.text_input(
        label="DESCRIBE THE BEAST...",
        placeholder="e.g., a translucent slug the size of a horse, slow lightning coiling in its gut"
    )

    c_vibe, c_btn = st.columns([2, 1])

    with c_vibe:
        st.markdown("""
            <div style="font-family: 'Cinzel', serif; font-size: 14px; color: #a0a0a0; margin-bottom: 5px; display: block; text-transform: uppercase; letter-spacing: 1px;">
                Choose a Resonance
            </div>
        """, unsafe_allow_html=True)

        selected_vibe = st.selectbox(
            "CHOOSE A RESONANCE",
            ["Noble & Bright", "Grim & Shadow", "Mystic & Strange"],
            index=1,
            label_visibility="collapsed"
        )
    with c_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("SUMMON THE BEAST")

if submitted and user_input:
    st.session_state.last_creature_concept = user_input
    st.session_state.creature_data = conjure_creature(user_input, selected_vibe)

# -----------------------------------------------------------------------------
# 5. RESULT
# -----------------------------------------------------------------------------
if st.session_state.creature_data:
    data = st.session_state.creature_data
    if "db_status" in st.session_state:
        if "Success!" in st.session_state.db_status:
            st.success(st.session_state.db_status)
        else:
            st.warning(st.session_state.db_status)

    st.markdown(build_creature_card(data), unsafe_allow_html=True)
