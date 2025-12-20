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
    ::selection { background: var(--emerald-dim); color: var(--emerald-bright); }
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000 80%);
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
    .stTextInput input::placeholder { color: #444 !important; font-style: italic; }
    .stTextInput:hover input { border-color: var(--emerald-glow) !important; }
    .stTextInput label { display: none; }

    /* --- ARCHIVE CARD (PREVIEW) --- */
    /* This wraps the HTML part of the card (Image + Title) */
    .archive-card {
        background: #0e0e0e;
        border: 1px solid #222;
        border-bottom: none; /* Button creates the bottom border */
        border-top: 4px solid var(--emerald-dim);
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        transition: transform 0.3s ease;
        display: flex;
        flex-direction: column;
        height: 600px; /* Fixed height for alignment */
        margin-bottom: 0px !important; /* Touch the button below */
        border-radius: 4px 4px 0 0;
    }
    .archive-card:hover {
        border-top: 4px solid var(--emerald-bright);
        box-shadow: 0 15px 50px rgba(0,0,0,1);
    }

    /* 1. IMAGE */
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

    /* 2. IDENTITY */
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
        font-size: 1.5rem; /* Reduced to prevent breaking */
        color: #fff; 
        letter-spacing: 1px; 
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 10px #000;
        line-height: 1.2;
        word-wrap: break-word;
    }
    .card-class { 
        font-family: 'Cinzel', serif; 
        font-size: 0.8rem; 
        color: var(--emerald-bright); 
        letter-spacing: 2px; 
        text-transform: uppercase; 
        opacity: 0.9;
    }

    /* --- THE INSPECT BUTTON (Seamless Integration) --- */
    /* We style the Streamlit button to look like the card footer */
    div.stButton > button {
        width: 100%;
        background-color: #080808;
        color: #666;
        border: 1px solid #222;
        border-top: none;
        border-radius: 0 0 4px 4px;
        font-family: 'Cinzel', serif;
        letter-spacing: 3px;
        font-size: 0.9rem;
        padding: 1rem;
        margin-top: 0px;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        color: var(--emerald-bright);
        background-color: #151515;
        border-color: #333;
        box-shadow: 0 5px 15px rgba(80, 200, 120, 0.1);
        text-shadow: 0 0 8px var(--emerald-dim);
    }
    div.stButton > button:focus {
        border-color: var(--emerald-glow);
        color: var(--emerald-glow);
    }

    /* --- DIALOG / MODAL STYLING --- */
    /* Styling the content INSIDE the pop-up */
    .modal-header { text-align: center; border-bottom: 1px solid #333; padding-bottom: 1rem; margin-bottom: 1rem; }
    .modal-name { font-family: 'Cinzel', serif; font-size: 2.5rem; color: var(--emerald-bright); margin: 0; }
    .modal-class { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; color: #888; font-style: italic; }
    
    .modal-voice { 
        font-family: 'Cormorant Garamond', serif; 
        font-size: 1.4rem; 
        color: #e0e0e0; 
        text-align: center; 
        padding: 2rem; 
        border-left: 2px solid var(--emerald-dim);
        background: #111;
        margin: 1.5rem 0;
        font-style: italic;
    }
    
    .modal-lore { 
        font-family: 'Cormorant Garamond', serif; 
        font-size: 1.2rem; 
        color: #bbb; 
        line-height: 1.8; 
        text-align: left; 
        padding: 1rem;
    }
    
    .modal-meta { font-family: 'Lato', sans-serif; font-size: 0.8rem; color: #444; text-align: center; margin-top: 2rem; }

    /* Footer Runes */
    .footer-container { opacity: 0.3; text-align: center; margin-top: 4rem; padding-bottom: 2rem;}
    .rune-span { margin: 0 10px; font-size: 1.2rem; color: #444; cursor: default; }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AUTHENTICATION
# -----------------------------------------------------------------------------
try:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    if "gcp_service_account" in st.secrets:
        service_account_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
        gc = gspread.authorize(creds)
    else:
        creds = service_account.Credentials.from_service_account_file(
            "service_account.json",
            scopes=SCOPES
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
# 5. THE MODAL (POP UP FUNCTION)
# -----------------------------------------------------------------------------
@st.dialog("The Soul Revealed", width="large")
def view_soul(row):
    """
    This function renders the pop-up modal content when a card is clicked.
    """
    # Safe Image Handling
    img_src = row.get('Image_URL', '')
    if not str(img_src).startswith("http"):
        img_src = "https://via.placeholder.com/800x400?text=No+Visage"

    # 1. Large Header Image
    st.image(img_src, use_container_width=True)
    
    # 2. Title Section
    st.markdown(f"""
        <div class="modal-header">
            <div class="modal-name">{row['Name']}</div>
            <div class="modal-class">{row['Class']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 3. Voice (Quote)
    st.markdown(f"""
        <div class="modal-voice">“{row['Greeting']}”</div>
    """, unsafe_allow_html=True)
    
    # 4. Lore (Full Text)
    st.markdown(f"""
        <div class="modal-lore">{row['Lore']}</div>
    """, unsafe_allow_html=True)
    
    # 5. Metadata
    st.markdown(f"""
        <div class="modal-meta">
            VISUAL: {row['Visual_Desc']}<br>
            ACCESSION: {row.get('Timestamp', 'Unknown')}
        </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 6. LAYOUT & GRID
# -----------------------------------------------------------------------------
st.page_link("home.py", label="< RETURN TO HALL", use_container_width=False)

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
    
    for index, row in filtered_df.iloc[::-1].iterrows():
        col_index = index % 3
        
        img_src = row.get('Image_URL', '')
        if not str(img_src).startswith("http"):
            img_src = "https://via.placeholder.com/400x500?text=No+Visage"

        with cols[col_index]:
            # 1. THE VISUAL CARD (HTML)
            # No interaction here, just display
            html = ""
            html += '<div class="archive-card">'
            html += '<div class="img-frame">'
            html += f'<img src="{img_src}" loading="lazy">'
            html += '</div>'
            html += '<div class="card-identity">'
            html += f'<div class="card-name">{row["Name"]}</div>'
            html += f'<div class="card-class">{row["Class"]}</div>'
            html += '</div>'
            html += '</div>' # End Card
            
            st.markdown(html, unsafe_allow_html=True)
            
            # 2. THE TRIGGER BUTTON (Streamlit)
            # Placed immediately below to look like the footer
            if st.button(f"INSPECT SOUL ᛦ", key=f"btn_{index}"):
                view_soul(row)

else:
    st.markdown("<p style='text-align:center; color:#666;'>No souls answer to that name.</p>", unsafe_allow_html=True)

# FOOTER
runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)