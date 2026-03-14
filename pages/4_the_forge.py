import streamlit as st
import datetime
import base64

import utils.styles as styles
from services import llm_service, storage_service, db_service

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The Forge", layout="centered", page_icon="⚒️")

# Initialize Session State
if "item_data" not in st.session_state:
    st.session_state.item_data = None
if "last_item_concept" not in st.session_state:
    st.session_state.last_item_concept = ""

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE
# -----------------------------------------------------------------------------
styles.load_css()

# -----------------------------------------------------------------------------
# 3. CORE LOGIC
# -----------------------------------------------------------------------------
def forge_item(concept, rarity):
    # 1. GENERATE TEXT
    with st.spinner(f"The Anvil rings..."):
        try:
            item_data = llm_service.generate_item_text(concept, rarity)
        except Exception as e:
            st.error(f"Failed to forge item text: {e}")
            return None

    # 2. GENERATE IMAGE
    with st.spinner("Enchanting the Form..."):
        try:
            image_bytes = llm_service.generate_item_image(
                item_data.get('Visual_Desc', ''), 
                item_data.get('Type', 'Wondrous Item')
            )
            
            b64_encoded = base64.b64encode(image_bytes).decode("utf-8")
            data_uri = f"data:image/jpeg;base64,{b64_encoded}"
            
            # ---> UPLOAD TO CLOUDINARY <---
            item_data["image_url"] = storage_service.upload_image_to_cdn(data_uri, folder="The_Forge")
        except Exception as e:
            st.warning(f"Could not forge visual form: {e}")
            item_data["image_url"] = "Image Upload Failed"

        # ---> 3. SAVE TO GOOGLE SHEETS <---
        try:
            current_time = str(datetime.datetime.now())
            row_to_save = [
                item_data.get("Name", "Unknown Artifact"), 
                item_data.get("Type", "Unknown"),
                rarity,
                item_data.get("Lore", ""),             
                item_data.get("Visual_Desc", ""),  
                item_data.get("image_url", ""),    
                current_time                       
            ]
            
            db_service.insert_item(row_to_save)
            st.session_state.db_status = f"Success! {item_data.get('Name')} saved to the Armory."
        except Exception as e:
            st.session_state.db_status = f"Armory Exception: {str(e)}"

        return item_data

# -----------------------------------------------------------------------------
# 4. LAYOUT
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO VAULT", use_container_width=False)

st.markdown("<h1>THE FORGE</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Forge artifacts of power and ruin...</div>", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-header">The Forge</div>', unsafe_allow_html=True)

with st.form("armory_form"):
    user_input = st.text_input(
        label="DESCRIBE THE ARTIFACT...", 
        placeholder="e.g., A cursed dagger made of black glass that murmurs secrets"
    )
    
    c_rarity, c_btn = st.columns([2, 1])
 
    with c_rarity:
        st.markdown("""
            <div style="font-family: 'Cinzel', serif; font-size: 14px; color: #a0a0a0; margin-bottom: 5px; display: block; text-transform: uppercase; letter-spacing: 1px;">
                Choose Rarity
            </div>
        """, unsafe_allow_html=True)
        
        selected_rarity = st.selectbox(
            "CHOOSE RARITY", 
            ["Common", "Uncommon", "Rare", "Very Rare", "Legendary", "Artifact"],
            index=2, # Default to Rare
            label_visibility="collapsed"
        )
    with c_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("STRIKE THE ANVIL")

if submitted and user_input:
    st.session_state.last_item_concept = user_input
    st.session_state.item_data = forge_item(user_input, selected_rarity) 
    st.rerun()

# -----------------------------------------------------------------------------
# 5. RESULT & MODIFIERS
# -----------------------------------------------------------------------------
if st.session_state.item_data:
    data = st.session_state.item_data
    if "db_status" in st.session_state:
        # If success, show green. If error, show yellow.
        if "Success!" in st.session_state.db_status:
            st.success(st.session_state.db_status)
        else:
            st.warning(st.session_state.db_status)
    
    card_html = ""
    card_html += f'<div class="character-card">'
    card_html += f'  <div class="card-header">'
    card_html += f'    <div class="card-name">{data.get("Name", "Unknown Artifact")}</div>'
    card_html += f'    <div class="card-class" style="color:#c9a347;">{data.get("Type", "Wondrous Item")} • {selected_rarity}</div>'
    card_html += f'  </div>'
    card_html += f'  <div class="img-container">'
    if data.get("image_url", "").startswith("http"):
        card_html += f'    <a href="{data["image_url"]}" target="_blank">'
        card_html += f'      <img src="{data["image_url"]}" title="Click to Expand">'
        card_html += f'    </a>'
    else:
        card_html += f'    <div style="height:400px; display:flex; align-items:center; justify-content:center; color:#555;">No Visage Found</div>'
    card_html += f'  </div>'
    card_html += f'  <div class="visual-caption">"{data.get("Visual_Desc", "")}"</div>'
    card_html += f'  <hr class="seam">'
    card_html += f'  <div class="lore-section">'
    card_html += f'    <span class="lore-label">Lore</span>'
    card_html += f'    {data.get("Lore", "")}'
    card_html += f'  </div>'
    card_html += f'</div>'
    st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("REROLL ARTIFACT", use_container_width=True, type="secondary"):
        st.session_state.item_data = forge_item(st.session_state.last_item_concept, selected_rarity)
        st.rerun()

runes = ["ᚹ", "ᛊ", "ᛟ", "ᚾ", "ᚷ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)
