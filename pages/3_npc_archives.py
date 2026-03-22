import streamlit as st
import pandas as pd
import base64

import utils.styles as styles
from services import db_service, llm_service, storage_service

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="NPC Archives", page_icon="📚", layout="wide")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (CSS)
# -----------------------------------------------------------------------------
styles.load_css()

# -----------------------------------------------------------------------------
# 3. FETCH DATA
# -----------------------------------------------------------------------------
try:
    df = db_service.get_all_records()
except Exception as e:
    st.error(f"Could not read from Vault: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 5. THE MODAL (POP UP FUNCTION) - CLEAN
# -----------------------------------------------------------------------------
@st.dialog("The Archive Opens...", width="large")
def view_soul(row, index_in_sheet):
    img_src = row.get('Image_URL', '')
    if not str(img_src).startswith("http"):
        img_src = "https://via.placeholder.com/800x400?text=No+Visage"

    col1, col2 = st.columns([1, 1.4])
    with col1:
        st.markdown(f"""
        <style>
            .img-zoom-container {{ position: relative; overflow: hidden; border: 1px solid #333; border-radius: 2px; transition: border-color 0.3s; }}
            .img-zoom-container:hover {{ border-color: #50c878; }}
            .overlay-icon {{ position: absolute; bottom: 10px; right: 10px; background: rgba(0,0,0,0.7); color: #fff; padding: 4px 8px; font-size: 0.8rem; border-radius: 4px; pointer-events: none; }}
        </style>
        <div class="img-zoom-container">
            <a href="{img_src}" target="_blank" title="Open High-Res Version">
                <img src="{img_src}" style="width: 100%; display: block;">
                <div class="overlay-icon">⤢ ENLARGE</div>
            </a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='modal-visual'>{row['Visual_Desc']}</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="modal-header">
            <div class="modal-name">{row['Name']}</div>
                <div class="modal-class">{row['Class']}</div>
            </div>
            <div class="modal-voice">“{row['Greeting']}”</div>
            <div class="modal-lore">{row['Lore']}</div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 1px solid #222; margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-family:Cinzel; color:#95b4a7; margin-bottom:8px;'>✨ Reforge Visage (Fast Lane)</div>", unsafe_allow_html=True)
        
        preview_key = f"pending_npc_preview_{index_in_sheet}"
        
        tweak_prompt = st.text_input("Tweak visual details", placeholder="e.g., 'Make it snowing', 'Give them a scar'", label_visibility="collapsed", key=f"tweak_{index_in_sheet}")
        tweak_tone = st.selectbox("Resonance", ["Noble & Bright", "Grim & Shadow", "Mystic & Strange"], key=f"tweak_tone_{index_in_sheet}")
        
        if st.button("REFORGE IMAGE", type="primary", use_container_width=True, key=f"btn_reforge_{index_in_sheet}"):
            if not tweak_prompt:
                st.warning("Please enter a tweak description.")
            else:
                with st.spinner("The Weave shifts..."):
                    try:
                        new_img_bytes = llm_service.remix_npc_image(
                            base_visual=row['Visual_Desc'],
                            char_class=row['Class'],
                            tweak=tweak_prompt,
                            tone=tweak_tone
                        )
                        # Store preview in session state — do NOT st.rerun() here,
                        # because that closes the dialog before the preview can render.
                        st.session_state[preview_key] = {
                            "bytes": new_img_bytes,
                            "original_url": img_src,
                        }
                    except Exception as e:
                        st.error(f"Failed to reforge image: {e}")
        
        # --- PREVIEW: Accept or Keep Original ---
        if preview_key in st.session_state:
            st.markdown("<div style='font-family:Cinzel; color:#c9a347; margin: 12px 0 6px;'>⚖️ Compare Visages</div>", unsafe_allow_html=True)
            prev_col1, prev_col2 = st.columns(2)
            with prev_col1:
                st.markdown("<div style='text-align:center; color:#888; font-size:0.75rem; font-family:Cinzel; letter-spacing:1px;'>ORIGINAL</div>", unsafe_allow_html=True)
                st.image(st.session_state[preview_key]["original_url"], use_container_width=True)
            with prev_col2:
                st.markdown("<div style='text-align:center; color:#50c878; font-size:0.75rem; font-family:Cinzel; letter-spacing:1px;'>NEW VISAGE</div>", unsafe_allow_html=True)
                st.image(st.session_state[preview_key]["bytes"], use_container_width=True)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("↩ KEEP ORIGINAL", use_container_width=True, key=f"keep_{index_in_sheet}"):
                    del st.session_state[preview_key]
                    st.rerun()
            with btn_col2:
                if st.button("✅ ACCEPT NEW", type="primary", use_container_width=True, key=f"accept_{index_in_sheet}"):
                    with st.spinner("Inscribing new visage..."):
                        try:
                            img_bytes = st.session_state[preview_key]["bytes"]
                            b64_encoded = base64.b64encode(img_bytes).decode("utf-8")
                            data_uri = f"data:image/jpeg;base64,{b64_encoded}"
                            new_image_url = storage_service.upload_image_to_cdn(data_uri)
                            db_service.update_character_image(index_in_sheet + 2, new_image_url)
                            del st.session_state[preview_key]
                            st.session_state["show_success_toast"] = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to save: {e}")

# -----------------------------------------------------------------------------
# 6. LAYOUT & GRID
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO HALL", use_container_width=False)

st.markdown("<h1>NPC ARCHIVES</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>That which is remembered, lives forever.</div>", unsafe_allow_html=True)

if st.session_state.get("show_success_toast"):
    st.toast("Visage reforged successfully.", icon="✨")
    st.session_state["show_success_toast"] = False

# --- SIDEBAR FILTERS ---
st.sidebar.markdown('<div class="sidebar-header">Filter Archives</div>', unsafe_allow_html=True)

if not df.empty:
    campaigns = ["All"]
    if 'Campaign' in df.columns:
        unique_cams = sorted([str(x) for x in df['Campaign'].unique() if str(x).strip() != "" and str(x).lower() != "nan"])
        campaigns.extend(unique_cams)
    sel_campaign = st.sidebar.selectbox("Campaign", campaigns)
    
    factions = ["All"]
    if 'Faction' in df.columns:
        unique_facs = sorted([str(x) for x in df['Faction'].unique() if str(x).strip() != "" and str(x).lower() != "nan"])
        factions.extend(unique_facs)
    sel_faction = st.sidebar.selectbox("Faction", factions)
else:
    sel_campaign = "All"
    sel_faction = "All"

# --- SEARCH & FILTER LOGIC ---
search_query = st.text_input("Search the Archives", placeholder="Speak the name, class, or secret...")

filtered_df = df.copy()

if sel_campaign != "All":
    filtered_df['Campaign'] = filtered_df['Campaign'].astype(str)
    filtered_df = filtered_df[filtered_df['Campaign'] == sel_campaign]

if sel_faction != "All":
    filtered_df['Faction'] = filtered_df['Faction'].astype(str)
    filtered_df = filtered_df[filtered_df['Faction'] == sel_faction]

if search_query:
    mask = (
        filtered_df['Name'].astype(str).str.contains(search_query, case=False) |
        filtered_df['Class'].astype(str).str.contains(search_query, case=False) |
        filtered_df['Lore'].astype(str).str.contains(search_query, case=False) |
        filtered_df['Campaign'].astype(str).str.contains(search_query, case=False) |
        filtered_df['Faction'].astype(str).str.contains(search_query, case=False)
    )
    filtered_df = filtered_df[mask]

# --- GRID ---
MAX_DISPLAY = 30

if not filtered_df.empty:
    
    # 1. SORTING LOGIC: Latest First
    if 'Timestamp' in filtered_df.columns:
        filtered_df['Timestamp_Temp'] = pd.to_datetime(filtered_df['Timestamp'], errors='coerce')
        filtered_df = filtered_df.sort_values(by='Timestamp_Temp', ascending=False)
    else:
        filtered_df = filtered_df.iloc[::-1]

    # Cap displayed entries
    display_df = filtered_df.head(MAX_DISPLAY)

    cols = st.columns(3)
    
    for i, (index, row) in enumerate(display_df.iterrows()): 
        col_index = i % 3
        img_src = row.get('Image_URL', '')
        if not str(img_src).startswith("http"):
            img_src = "https://via.placeholder.com/400x533?text=No+Visage"

        # PERFORMANCE FIX: Cloudinary optimized thumbnails (3:4 aspect ratio)
        if "cloudinary" in img_src and "/upload/" in img_src:
            img_src = img_src.replace("/upload/", "/upload/c_fill,g_face,w_400,h_533,q_auto,f_auto/")

        with cols[col_index]:
            html = ""
            html += '<div class="archive-card">'
            html += '<div class="img-frame">'
            html += f'<img src="{img_src}" loading="lazy">'
            html += '</div>'
            html += '<div class="card-identity">'
            
            html += '<div class="identity-top">'
            html += f'<div class="card-name">{row["Name"]}</div>'
            html += f'<div class="card-class">{row["Class"]}</div>'
            html += '</div>'
            
            # --- PILLS ---
            html += '<div class="pill-container">'
            if row.get('Campaign'):
                 html += f'<div class="pill-base pill-stone">{row["Campaign"]}</div>'
            if row.get('Faction'):
                 html += f'<div class="pill-base pill-metal">{row["Faction"]}</div>'
            if not row.get('Campaign') and not row.get('Faction'):
                 html += f'<div class="pill-base pill-stone" style="opacity:0;">EMPTY</div>'
            html += '</div>'
            
            html += '</div>'
            html += '</div>' 
            st.markdown(html, unsafe_allow_html=True)
            
            # ACTIONS
            b_col1, b_col2, b_col3 = st.columns([0.6, 0.2, 0.2])
            
            with b_col1:
                if st.button(f"INSPECT ᛦ", key=f"inspect_{index}", type="primary", use_container_width=True):
                    view_soul(row, index)
            
            # QUICK EDIT (Quill)
            with b_col2:
                with st.popover("✒️", use_container_width=True):
                    st.markdown("<span style='color:#888; font-size:0.8rem; font-family:Cinzel; letter-spacing:1px; border-bottom:1px solid #333; display:block; margin-bottom:4px;'>CAMPAIGN</span>", unsafe_allow_html=True)
                    p_campaign = st.text_input("Campaign", value=row.get('Campaign', ''), key=f"pc_{index}", label_visibility="collapsed")
                    
                    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True) 

                    st.markdown("<span style='color:#8a9ba8; font-size:0.8rem; font-family:Cinzel; letter-spacing:1px; border-bottom:1px solid #4a5568; display:block; margin-bottom:4px;'>FACTION</span>", unsafe_allow_html=True)
                    p_faction = st.text_input("Faction", value=row.get('Faction', ''), key=f"pf_{index}", label_visibility="collapsed")
                    
                    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True) 

                    if st.button("Save", key=f"psave_{index}", type="primary"):
                        try:
                            sheet_row = index + 2
                            db_service.update_character_meta(sheet_row, p_campaign, p_faction)
                            st.toast("Resonance Inscribed", icon="✒️")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            with b_col3:
                if st.button("ᚺ", key=f"burn_{index}", type="secondary", use_container_width=True, help="Burn Soul"):
                    try:
                        db_service.delete_character(index + 2)
                        st.toast(f"Severed.", icon="🔥")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")