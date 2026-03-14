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
# 3. CORE LOGIC
# -----------------------------------------------------------------------------
def forge_npc(concept, tone):
    # 1. GENERATE TEXT
    with st.spinner(f"The Void answers..."):
        try:
            char_data = llm_service.generate_npc_text(concept, tone)
        except Exception as e:
            st.error(f"Failed to commune with the Void: {e}")
            return None

    # 2. GENERATE IMAGE
    with st.spinner("Conjuring the Form..."):
        try:
            image_bytes = llm_service.generate_npc_image(
                char_data.get('Visual_Desc', ''), 
                char_data.get('Class', ''), 
                tone
            )
            
            b64_encoded = base64.b64encode(image_bytes).decode("utf-8")
            data_uri = f"data:image/jpeg;base64,{b64_encoded}"
            
            # ---> UPLOAD TO CLOUDINARY <---
            char_data["image_url"] = storage_service.upload_image_to_cdn(data_uri)
        except Exception as e:
            st.warning(f"Could not forge visgae: {e}")
            char_data["image_url"] = "Image Upload Failed"

        # ---> 3. SAVE TO GOOGLE SHEETS <---
        try:
            current_time = str(datetime.datetime.now())
            row_to_save = [
                char_data.get("Name", "Unknown"), 
                char_data.get("Class", "Unknown"),
                char_data.get("Lore", ""),         
                char_data.get("Greeting", ""),     
                char_data.get("Visual_Desc", ""),  
                char_data.get("image_url", ""),    
                current_time                       
            ]
            
            db_service.insert_character(row_to_save)
            st.session_state.db_status = f"Success! {char_data.get('Name')} saved to Vault."
        except Exception as e:
            st.session_state.db_status = f"Vault Exception: {str(e)}"

        return char_data

# -----------------------------------------------------------------------------
# 4. LAYOUT
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

if submitted and user_input:
    st.session_state.last_concept = user_input
    st.session_state.npc_data = forge_npc(user_input, selected_vibe) 
    st.rerun()

# -----------------------------------------------------------------------------
# 5. RESULT & MODIFIERS
# -----------------------------------------------------------------------------
if st.session_state.npc_data:
    data = st.session_state.npc_data
    if "db_status" in st.session_state:
        # If success, show green. If error, show yellow.
        if "Success!" in st.session_state.db_status:
            st.success(st.session_state.db_status)
        else:
            st.warning(st.session_state.db_status)
    
    card_html = ""
    card_html += f'<div class="character-card">'
    card_html += f'  <div class="card-header">'
    card_html += f'    <div class="card-name">{data["Name"]}</div>'
    card_html += f'    <div class="card-class">{data["Class"]}</div>'
    card_html += f'  </div>'
    card_html += f'  <div class="img-container">'
    card_html += f'    <a href="{data["image_url"]}" target="_blank">'
    card_html += f'      <img src="{data["image_url"]}" title="Click to Expand">'
    card_html += f'    </a>'
    card_html += f'  </div>'
    card_html += f'  <div class="visual-caption">"{data["Visual_Desc"]}"</div>'
    card_html += f'  <hr class="seam">'
    card_html += f'  <div class="voice-section">'
    card_html += f'    <div class="voice-quote">{data["Greeting"]}</div>'
    card_html += f'  </div>'
    card_html += f'  <hr class="seam">'
    card_html += f'  <div class="lore-section">'
    card_html += f'    <span class="lore-label">Archive Record</span>'
    card_html += f'    {data["Lore"]}'
    card_html += f'  </div>'
    card_html += f'</div>'
    st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("REROLL: GRIM", use_container_width=True, type="secondary"):
            st.session_state.npc_data = forge_npc(st.session_state.last_concept, "Grim & Shadow")
            st.rerun()
            
    with col2:
        if st.button("REROLL: NOBLE", use_container_width=True, type="secondary"):
            st.session_state.npc_data = forge_npc(st.session_state.last_concept, "Noble & Bright")
            st.rerun()
            
    with col3:
        if st.button("REROLL: STRANGE", use_container_width=True, type="secondary"):
            st.session_state.npc_data = forge_npc(st.session_state.last_concept, "Mystic & Strange")
            st.rerun()

runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)