import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The Hall of Souls", page_icon="📚", layout="wide")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #111;
        --emerald-glow: #50c878;
        --emerald-bright: #66ff99;
        --emerald-dim: #1e3a2a;
        --destruct-red: #8b0000;
        --destruct-bright: #ff4500;
        --nav-gold: #d4af37; /* Divine Gold */
        --gold-glow: rgba(212, 175, 55, 0.6);
    }

    /* --- GLOBAL --- */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000 80%);
    }

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] { background-color: #080808; border-right: 1px solid #1e3a2a; }
    [data-testid="stSidebarNav"] { font-family: 'Cinzel', serif; padding-top: 2rem; }
    header[data-testid="stHeader"] { background: transparent; }

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 12px;
        font-size: 3rem !important;
        color: var(--emerald-bright) !important;
        text-shadow: 0 0 30px rgba(102, 255, 153, 0.4);
        margin-bottom: 0 !important;
        text-align: center;
    }
    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        color: #888;
        font-style: italic;
        margin-bottom: 3rem;
    }

    /* --- NAVIGATION LINK --- */
    a[data-testid="stPageLink-NavLink"] { background: transparent !important; border: none !important; }
    a[data-testid="stPageLink-NavLink"] p { color: #666; font-family: 'Cinzel', serif; font-size: 0.9rem; transition: color 0.3s; }
    a[data-testid="stPageLink-NavLink"]:hover p { color: var(--nav-gold) !important; text-shadow: 0 0 10px var(--gold-glow); }

    /* --- SEARCH BAR --- */
    .stTextInput > div > div > input {
        background-color: #0a0a0a !important;
        border: 1px solid #333 !important;
        border-bottom: 2px solid var(--emerald-dim) !important;
        color: #e0e0e0 !important;
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        text-align: center;
        padding: 1.5rem;
        letter-spacing: 2px;
    }

    /* --- ARCHIVE CARD --- */
    .archive-card {
        background: #0e0e0e;
        border: 1px solid #222;
        border-bottom: none; 
        border-top: 4px solid var(--emerald-dim);
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        display: flex;
        flex-direction: column;
        height: 520px !important;
        margin-bottom: 0px !important;
        overflow: hidden;
    }
    .archive-card:hover {
        border-top: 4px solid var(--emerald-bright);
        box-shadow: 0 15px 50px rgba(0,0,0,1);
    }

    /* Image Frame */
    .img-frame { 
        width: 100%; height: 300px; overflow: hidden; 
        border-bottom: 1px solid #222; position: relative; flex-shrink: 0;
    }
    .img-frame img { 
        width: 100%; height: 100%; object-fit: cover; object-position: top center; 
        opacity: 0.95; transition: opacity 0.5s; 
    }
    .img-frame:hover img { opacity: 1; transform: scale(1.02); }

    /* Identity Section */
    .card-identity {
        padding: 1rem 0.5rem; text-align: center;
        background: linear-gradient(180deg, #111 0%, #0e0e0e 100%);
        flex-grow: 1; display: flex; flex-direction: column; 
        justify-content: space-between; align-items: center; gap: 0.5rem;
    }

    .identity-top { width: 100%; display: flex; flex-direction: column; gap: 0.2rem; }

    .card-name { 
        font-family: 'Cinzel', serif; font-size: 1.4rem; color: #fff; letter-spacing: 1px; 
        text-shadow: 0 4px 10px #000; line-height: 1.2;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
        min-height: 3.4rem; display: flex; align-items: center; justify-content: center;
    }

    .card-class { 
        font-family: 'Cinzel', serif; font-size: 0.8rem; color: var(--emerald-bright); 
        letter-spacing: 2px; text-transform: uppercase; opacity: 0.9;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    
    .tag-pill {
        display: inline-block; background: #1a1a1a; border: 1px solid #333; color: #666;
        font-family: 'Lato', sans-serif; font-size: 0.65rem; text-transform: uppercase;
        letter-spacing: 1px; padding: 4px 12px; border-radius: 12px; margin-top: 0.5rem;
    }

    /* --- BUTTON CLASS 1: PRIMARY (EMERALD) --- */
    button[kind="primary"] {
        background: transparent !important; border: none !important; color: #555 !important;
        font-family: 'Cinzel', serif !important; font-size: 1.1rem !important; padding: 0 !important;
        height: 60px !important; width: 100% !important; transition: all 0.3s ease !important;
        box-shadow: none !important;
    }
    button[kind="primary"]:hover {
        color: var(--emerald-bright) !important; text-shadow: 0 0 15px var(--emerald-glow);
        transform: scale(1.05); background: transparent !important;
    }

    /* --- BUTTON CLASS 2: SECONDARY (RED) --- */
    button[kind="secondary"] {
        background: transparent !important; border: none !important; color: #444 !important;
        font-size: 1.5rem !important; padding: 0 !important; height: 60px !important;
        width: 100% !important; transition: all 0.4s ease !important; box-shadow: none !important;
    }
    button[kind="secondary"]:hover {
        color: var(--destruct-bright) !important;
        transform: scale(1.2); background: transparent !important;
    }

    /* --- BUTTON CLASS 3: DIVINE (GOLD POPOVER) --- */
    /* Target the button inside the popover container */
    [data-testid="stPopover"] > button {
        background: transparent !important;
        border: none !important;
        color: #555 !important; /* Default Dim */
        height: 60px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    /* When Hovered: Turn Gold */
    [data-testid="stPopover"] > button:hover {
        color: var(--nav-gold) !important;
        text-shadow: 0 0 10px var(--gold-glow) !important;
        transform: scale(1.1) !important;
    }
    /* Force the SVG Icon (Arrow) to match text color */
    [data-testid="stPopover"] > button svg {
        fill: currentColor !important;
        stroke: currentColor !important;
    }

    /* --- MODAL STYLING --- */
    .modal-header { border-bottom: 1px solid #333; padding-bottom: 1rem; margin-bottom: 1rem; }
    .modal-name { font-family: 'Cinzel', serif; font-size: 2.5rem; color: #fff; line-height: 1.1; margin-bottom: 5px;}
    .modal-class { font-family: 'Cinzel', serif; font-size: 0.9rem; color: var(--emerald-bright); letter-spacing: 3px; text-transform: uppercase; }
    .modal-voice { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; color: #e0e0e0; font-style: italic; padding: 1.5rem; background: #0a0a0a; border-left: 2px solid var(--emerald-glow); margin-bottom: 1.5rem; }
    .modal-lore { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; color: #bbb; line-height: 1.7; text-align: justify; }
    .modal-visual { font-family: 'Cormorant Garamond', serif; font-size: 0.95rem; color: #666; font-style: italic; margin-top: 10px; border-top: 1px solid #222; padding-top: 10px; }
    .modal-meta { font-family: 'Lato', sans-serif; font-size: 0.7rem; color: #444; margin-top: 2rem; border-top: 1px solid #222; padding-top: 1rem; }

    /* Footer */
    .footer-container { opacity: 0.3; text-align: center; margin-top: 4rem; padding-bottom: 2rem;}
    .rune-span { margin: 0 10px; font-size: 1.2rem; color: #444; cursor: default; }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AUTHENTICATION
# -----------------------------------------------------------------------------
try:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=SCOPES
        )
        gc = gspread.authorize(creds)
    else:
        creds = service_account.Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
        gc = gspread.authorize(creds)
except Exception as e:
    st.error(f"🚨 Connection Error: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 4. FETCH DATA
# -----------------------------------------------------------------------------
try:
    sh = gc.open("Masters_Vault_Db")
    worksheet = sh.get_worksheet(0)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Could not read from Vault: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 5. THE MODAL (POP UP FUNCTION) - CLEAN
# -----------------------------------------------------------------------------
@st.dialog("The Archive Opens...", width="large")
def view_soul(row, index_in_sheet):
    """
    Shows pure details. Edits happen in the popover.
    """
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

# -----------------------------------------------------------------------------
# 6. LAYOUT & GRID
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO HALL", use_container_width=False)

st.markdown("<h1>THE ARCHIVES OF THE LOST</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>That which is remembered, lives forever.</div>", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
st.sidebar.header("📜 Filter Archives")

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
        filtered_df['Lore'].astype(str).str.contains(search_query, case=False)
    )
    filtered_df = filtered_df[mask]

# --- GRID ---
if not filtered_df.empty:
    cols = st.columns(3)
    for index, row in filtered_df.iloc[::-1].iterrows():
        col_index = index % 3
        img_src = row.get('Image_URL', '')
        if not str(img_src).startswith("http"):
            img_src = "https://via.placeholder.com/400x500?text=No+Visage"

        if "cloudinary" in img_src and "/upload/" in img_src:
            img_src = img_src.replace("/upload/", "/upload/c_fill,g_face,w_800,h_600/")

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
            
            if row.get('Campaign'):
                 html += f'<div class="tag-pill">{row["Campaign"]}</div>'
            else:
                 html += f'<div class="tag-pill" style="opacity:0;">EMPTY</div>'
            
            html += '</div>'
            html += '</div>' 
            st.markdown(html, unsafe_allow_html=True)
            
            # ACTIONS
            b_col1, b_col2, b_col3 = st.columns([0.6, 0.2, 0.2])
            
            with b_col1:
                # CLASS 1: PRIMARY (Inspect)
                if st.button(f"INSPECT ᛦ", key=f"inspect_{index}", type="primary", use_container_width=True):
                    view_soul(row, index)
            
            with b_col2:
                # CLASS 3: DIVINE (Gold Popover)
                with st.popover("✒️", use_container_width=True):
                    st.caption(f"Inscribe Tags: {row['Name']}")
                    p_campaign = st.text_input("Campaign", value=row.get('Campaign', ''), key=f"pc_{index}")
                    p_faction = st.text_input("Faction", value=row.get('Faction', ''), key=f"pf_{index}")
                    
                    if st.button("Save", key=f"psave_{index}", type="primary"):
                        try:
                            sheet_row = index + 2
                            worksheet.update_cell(sheet_row, 8, p_campaign)
                            worksheet.update_cell(sheet_row, 9, p_faction)
                            st.toast("Resonance Inscribed", icon="✒️")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

            with b_col3:
                # CLASS 2: SECONDARY (Burn)
                if st.button("ᚺ", key=f"burn_{index}", type="secondary", use_container_width=True, help="Burn Soul"):
                    try:
                        worksheet.delete_rows(index + 2)
                        st.toast(f"Severed.", icon="🔥")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
else:
    st.markdown("<p style='text-align:center; color:#666;'>No souls answer to that name.</p>", unsafe_allow_html=True)

# FOOTER
runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)