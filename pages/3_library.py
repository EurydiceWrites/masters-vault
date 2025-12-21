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
    }

    /* --- GLOBAL --- */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000 80%);
    }

    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] {
        background-color: #080808; 
        border-right: 1px solid #1e3a2a;
    }
    [data-testid="stSidebarNav"] {
        font-family: 'Cinzel', serif;
        padding-top: 2rem;
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }

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

    /* --- ARCHIVE CARD (HTML Top Half) --- */
    .archive-card {
        background: #0e0e0e;
        border: 1px solid #222;
        border-bottom: none; /* Connects to button */
        border-top: 4px solid var(--emerald-dim);
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        display: flex;
        flex-direction: column;
        height: 600px; /* FIXED HEIGHT FOR ALIGNMENT */
        margin-bottom: 0px !important;
    }
    .archive-card:hover {
        border-top: 4px solid var(--emerald-bright);
        box-shadow: 0 15px 50px rgba(0,0,0,1);
    }

    .img-frame { 
        width: 100%; 
        height: 400px; 
        overflow: hidden; 
        border-bottom: 1px solid #222;
        position: relative;
        flex-shrink: 0;
    }
    .img-frame img { width: 100%; height: 100%; object-fit: cover; object-position: top; opacity: 0.95; transition: opacity 0.5s; }
    .img-frame:hover img { opacity: 1; transform: scale(1.02); }

    .card-identity {
        padding: 1rem;
        text-align: center;
        background: linear-gradient(180deg, #111 0%, #0e0e0e 100%);
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .card-name { 
        font-family: 'Cinzel', serif; 
        font-size: 1.5rem; 
        color: #fff; 
        letter-spacing: 1px; 
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 10px #000;
    }
    .card-class { 
        font-family: 'Cinzel', serif; 
        font-size: 0.8rem; 
        color: var(--emerald-bright); 
        letter-spacing: 2px; 
        text-transform: uppercase; 
        opacity: 0.9;
    }

    /* --- THE BUTTON OVERRIDE (Streamlit) --- */
    div.stButton > button {
        width: 100% !important;
        border-radius: 0px !important;
        background-color: #0e0e0e !important;
        color: #888 !important;
        border: 1px solid #222 !important;
        border-top: 1px solid #1a1a1a !important; 
        font-family: 'Cinzel', serif !important;
        font-size: 0.9rem !important;
        padding: 1rem !important;
        height: 60px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        color: var(--emerald-bright) !important;
        border-color: #333 !important;
        background-color: #151515 !important;
    }

    /* --- MODAL STYLING --- */
    .modal-header { border-bottom: 1px solid #333; padding-bottom: 1rem; margin-bottom: 1rem; }
    .modal-name { font-family: 'Cinzel', serif; font-size: 2.5rem; color: #fff; line-height: 1.1; margin-bottom: 5px;}
    .modal-class { font-family: 'Cinzel', serif; font-size: 0.9rem; color: var(--emerald-bright); letter-spacing: 3px; text-transform: uppercase; }
    
    .modal-voice { 
        font-family: 'Cormorant Garamond', serif; 
        font-size: 1.4rem; 
        color: #e0e0e0; 
        font-style: italic;
        padding: 1.5rem;
        background: #0a0a0a;
        border-left: 2px solid var(--emerald-glow);
        margin-bottom: 1.5rem;
    }
    
    .modal-lore { 
        font-family: 'Cormorant Garamond', serif; 
        font-size: 1.2rem; 
        color: #bbb; 
        line-height: 1.7; 
        text-align: justify; 
    }

    .modal-visual {
        font-family: 'Cormorant Garamond', serif; 
        font-size: 0.95rem; 
        color: #666; 
        font-style: italic; 
        margin-top: 10px;
        border-top: 1px solid #222;
        padding-top: 10px;
    }

    /* Footer Runes */
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
        # Fallback for local testing
        creds = service_account.Credentials.from_service_account_file(
            "service_account.json", scopes=SCOPES
        )
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

    if df.empty:
        st.info("The Library is empty.")
        st.stop()

except Exception as e:
    st.error(f"Could not read from Vault: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 5. THE MODAL (POP UP FUNCTION) - CLICKABLE IMAGE VERSION
# -----------------------------------------------------------------------------
@st.dialog("The Archive Opens...", width="large")
def view_soul(row):
    # Safe Image Handling
    img_src = row.get('Image_URL', '')
    if not str(img_src).startswith("http"):
        img_src = "https://via.placeholder.com/800x400?text=No+Visage"

    col1, col2 = st.columns([1, 1.4])
    
    with col1:
        # --- CLICKABLE IMAGE HACK ---
        # We use HTML to wrap the image in an anchor tag target="_blank"
        st.markdown(f"""
        <style>
            .img-zoom-container {{
                position: relative;
                overflow: hidden;
                border: 1px solid #333;
                border-radius: 2px;
                transition: border-color 0.3s;
            }}
            .img-zoom-container:hover {{
                border-color: #50c878;
            }}
            .overlay-icon {{
                position: absolute;
                bottom: 10px;
                right: 10px;
                background: rgba(0,0,0,0.7);
                color: #fff;
                padding: 4px 8px;
                font-size: 0.8rem;
                border-radius: 4px;
                pointer-events: none;
            }}
        </style>
        
        <div class="img-zoom-container">
            <a href="{img_src}" target="_blank" title="Open High-Res Version">
                <img src="{img_src}" style="width: 100%; display: block;">
                <div class="overlay-icon">⤢ ENLARGE</div>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Visual Description (Styled)
        st.markdown(f"<div class='modal-visual'>{row['Visual_Desc']}</div>", unsafe_allow_html=True)
        
    with col2:
        # Title Block
        st.markdown(f"""
            <div class="modal-header">
                <div class="modal-name">{row['Name']}</div>
                <div class="modal-class">{row['Class']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Voice Block
        st.markdown(f"""
            <div class="modal-voice">“{row['Greeting']}”</div>
        """, unsafe_allow_html=True)
        
        # Lore Block
        st.markdown(f"""
            <div class="modal-lore">{row['Lore']}</div>
        """, unsafe_allow_html=True)
        
        # Meta Block
        st.markdown(f"""
            <div class="modal-meta">ACCESSION: {row.get('Timestamp', 'Unknown')}</div>
        """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. LAYOUT & GRID
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO HALL", use_container_width=False)

st.markdown("<h1>THE ARCHIVES OF THE LOST</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>That which is remembered, lives forever.</div>", unsafe_allow_html=True)

# --- SEARCH ---
search_query = st.text_input("Search the Archives", placeholder="Speak the name, class, or secret...")

if search_query:
    mask = (
        df['Name'].astype(str).str.contains(search_query, case=False) |
        df['Class'].astype(str).str.contains(search_query, case=False) |
        df['Lore'].astype(str).str.contains(search_query, case=False)
    )
    filtered_df = df[mask]
else:
    filtered_df = df

# --- GRID ---
if not filtered_df.empty:
    cols = st.columns(3)
    
    # Reverse order to show newest first
    for index, row in filtered_df.iloc[::-1].iterrows():
        col_index = index % 3
        
        img_src = row.get('Image_URL', '')
        if not str(img_src).startswith("http"):
            img_src = "https://via.placeholder.com/400x500?text=No+Visage"

        with cols[col_index]:
            # 1. THE VISUAL CARD (Fixed Height HTML)
            html = ""
            html += '<div class="archive-card">'
            html += '<div class="img-frame">'
            html += f'<img src="{img_src}" loading="lazy">'
            html += '</div>'
            html += '<div class="card-identity">'
            html += f'<div class="card-name">{row["Name"]}</div>'
            html += f'<div class="card-class">{row["Class"]}</div>'
            html += '</div>'
            html += '</div>' 
            
            st.markdown(html, unsafe_allow_html=True)
            
            # 2. THE BUTTONS (Action Row)
            # We split the space: Big "Inspect" button, Small "Burn" button
            b_col1, b_col2 = st.columns([0.8, 0.2])
            
            with b_col1:
                # The Rune ᛦ (Yr) - Inspect
                if st.button(f"INSPECT ᛦ", key=f"inspect_{index}", use_container_width=True):
                    view_soul(row)
            
            with b_col2:
                # The Rune 🔥 - Burn
                if st.button("🔥", key=f"burn_{index}", use_container_width=True, help="Permanently Burn from Archives"):
                    try:
                        # Warning: This assumes the dataframe index matches the sheet order.
                        # Since we are using filtered_df, we must be careful.
                        # Ideally, find row by Unique ID. For now, we trust the index + 2 logic
                        # But since we reversed the list, index is still the ORIGINAL index from the full DF
                        # So this should work.
                        worksheet.delete_rows(index + 2)
                        st.toast(f"The soul of {row['Name']} has been severed.", icon="🔥")
                        # We must clear cache or rerun to see changes
                        st.rerun()
                    except Exception as e:
                        st.error(f"The soul resists: {e}")

else:
    st.markdown("<p style='text-align:center; color:#666;'>No souls answer to that name.</p>", unsafe_allow_html=True)

# FOOTER
runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)