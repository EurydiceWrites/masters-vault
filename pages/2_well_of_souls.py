import streamlit as st
import datetime
import base64

import utils.styles as styles
from services import llm_service, storage_service, db_service

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Well of Souls", layout="centered", page_icon="🔮")

# Initialize Session State
if "npc_data" not in st.session_state:
    st.session_state.npc_data = None
if "last_concept" not in st.session_state:
    st.session_state.last_concept = ""

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (The Void Theme)
# -----------------------------------------------------------------------------
styles.load_css()

# -----------------------------------------------------------------------------
# 3. CARD RENDERING
# -----------------------------------------------------------------------------
def build_npc_card(data: dict, forming: bool = False) -> str:
    """Builds the character-card HTML.

    forming=True renders a shimmering placeholder where the portrait will go,
    so the written details can be shown the instant they land while the image
    is still being generated.
    """
    name = data.get("Name", "Unknown")
    char_class = data.get("Class", "Unknown")
    visual = data.get("Visual_Desc", "")
    greeting = data.get("Greeting", "")
    lore = data.get("Lore", "")
    image_url = str(data.get("image_url", ""))

    if forming:
        portrait = "<div class='portrait-forming'>The form gathers...</div>"
    elif image_url.startswith("http"):
        portrait = (
            f'<a href="{image_url}" target="_blank">'
            f'<img src="{image_url}" title="Click to Expand">'
            f'</a>'
        )
    else:
        portrait = "<div class='portrait-missing'>No Visage Found</div>"

    return (
        '<div class="character-card">'
        '<div class="card-header">'
        f'<div class="card-name">{name}</div>'
        f'<div class="card-class">{char_class}</div>'
        '</div>'
        f'<div class="img-container">{portrait}</div>'
        f'<div class="visual-caption">"{visual}"</div>'
        '<hr class="seam">'
        '<div class="voice-section">'
        f'<div class="voice-quote">{greeting}</div>'
        '</div>'
        '<hr class="seam">'
        '<div class="lore-section">'
        '<span class="lore-label">Archive Record</span>'
        f'{lore}'
        '</div>'
        '</div>'
    )


def show_status(slot):
    """Renders the Vault save status into the given placeholder."""
    status = st.session_state.get("db_status")
    if not status:
        return
    if "Success!" in status:
        slot.success(status)
    else:
        slot.warning(status)


# -----------------------------------------------------------------------------
# 4. CORE LOGIC — PROGRESSIVE ("LIVE") GENERATION
# -----------------------------------------------------------------------------
def generate_live(card_slot, status_slot, concept: str, tone: str, fast: bool = True):
    """Generates an NPC and renders it progressively.

    The written details appear the moment the text lands, so the card is
    performable seconds sooner; the portrait fills into the same card once it
    is ready, and the Vault save happens last.

    fast=True  -> quick image model (live, mid-session use).
    fast=False -> high-fidelity image model (prep).
    """
    status_slot.empty()

    # Immediate feedback while the text is being written.
    card_slot.markdown(
        "<div class='summoning-state'>The Void stirs...</div>",
        unsafe_allow_html=True,
    )

    # 1. TEXT — the moment this lands, the card is performable.
    try:
        char_data = llm_service.generate_npc_text(concept, tone)
    except Exception as e:
        card_slot.empty()
        status_slot.error(f"Failed to commune with the Void: {e}")
        return None

    # 2. Render the card NOW — portrait still forming.
    card_slot.markdown(build_npc_card(char_data, forming=True), unsafe_allow_html=True)

    # 3. IMAGE — generated behind the already-visible text.
    try:
        image_bytes = llm_service.generate_npc_image(
            char_data.get("Visual_Desc", ""),
            char_data.get("Class", ""),
            tone,
            fast=fast,
        )
        b64_encoded = base64.b64encode(image_bytes).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{b64_encoded}"
        char_data["image_url"] = storage_service.upload_image_to_cdn(data_uri)
    except Exception:
        # Image is non-critical: the card still shows, with "No Visage Found".
        char_data["image_url"] = "Image Upload Failed"

    # 4. Swap the finished portrait into the same card.
    card_slot.markdown(build_npc_card(char_data, forming=False), unsafe_allow_html=True)

    # 5. Save to the Vault — last, after the card is already in hand.
    try:
        row_to_save = [
            char_data.get("Name", "Unknown"),
            char_data.get("Class", "Unknown"),
            char_data.get("Lore", ""),
            char_data.get("Greeting", ""),
            char_data.get("Visual_Desc", ""),
            char_data.get("image_url", ""),
            str(datetime.datetime.now()),
        ]
        db_service.insert_character(row_to_save)
        st.session_state.db_status = f"Success! {char_data.get('Name')} saved to Vault."
    except Exception as e:
        st.session_state.db_status = f"Vault Exception: {str(e)}"

    show_status(status_slot)
    return char_data


# -----------------------------------------------------------------------------
# 5. LAYOUT
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO VAULT", use_container_width=False)

st.markdown("<h1>THE WELL OF SOULS</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Conjure a form and inscribe the soul... </div>", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-header">Well of Souls</div>', unsafe_allow_html=True)

with st.form("forge_form"):
    user_input = st.text_input(
        label="WHISPER YOUR DESIRES...",
        placeholder="...and the void shall give it form."
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
            label_visibility="collapsed"
        )
    with c_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("INSCRIBE THE SOUL.")

# -----------------------------------------------------------------------------
# 6. RESULT — placeholders that the live generation renders into, in order
# -----------------------------------------------------------------------------
status_slot = st.empty()
card_slot = st.empty()

if submitted and user_input:
    st.session_state.last_concept = user_input
    st.session_state.npc_data = generate_live(card_slot, status_slot, user_input, selected_vibe)
elif st.session_state.npc_data:
    show_status(status_slot)
    card_slot.markdown(
        build_npc_card(st.session_state.npc_data, forming=False),
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 7. MODIFIERS (REROLL)
# -----------------------------------------------------------------------------
if st.session_state.npc_data:
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    reroll_tone = None

    with col1:
        if st.button("REROLL: GRIM", use_container_width=True, type="secondary"):
            reroll_tone = "Grim & Shadow"
    with col2:
        if st.button("REROLL: NOBLE", use_container_width=True, type="secondary"):
            reroll_tone = "Noble & Bright"
    with col3:
        if st.button("REROLL: STRANGE", use_container_width=True, type="secondary"):
            reroll_tone = "Mystic & Strange"

    if reroll_tone:
        st.session_state.npc_data = generate_live(
            card_slot, status_slot, st.session_state.last_concept, reroll_tone
        )

# -----------------------------------------------------------------------------
# 8. FOOTER
# -----------------------------------------------------------------------------
runes = ["ᚦ", "ᛖ", "᛫", "ᚾ", "ᛁ", "ᚷ", "ᚺ", "ᛏ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)
