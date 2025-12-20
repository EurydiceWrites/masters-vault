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

    /* --- ARCHIVE CARD DESIGN --- */
    .archive-card {
        background: #0e0e0e;
        border: 1px solid #222;
        border-top: 2px solid var(--emerald-dim);
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
        height: 700px; /* Increased height for better visuals */
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    .archive-card:hover {
        transform: translateY(-5px);
        border-top: 2px solid var(--emerald-bright);
        box-shadow: 0 15px 40px rgba(0,0,0,1);
    }

    /* Card Components */
    .card-header { background: #111; padding: 1rem; text-align: center; border-bottom: 1px solid #222; }
    .card-name { font-family: 'Cinzel', serif; font-size: 1.6rem; color: #fff; letter-spacing: 2px; }
    .card-class { font-family: 'Cinzel', serif; font-size: 0.8rem; color: var(--emerald-bright); letter-spacing: 1px; text-transform: uppercase; text-shadow: 0 0 5px rgba(102, 255, 153, 0.3); }

    .img-frame { 
        width: 100%; 
        height: 250px; /* TALLER IMAGES */
        overflow: hidden; 
        border-bottom: 1px solid #222;
        position: relative;
    }
    .img-frame img { width: 100%; height: 100%; object-fit: cover; opacity: 0.9; transition: opacity 0.5s; }
    .img-frame:hover img { opacity: 1; transform: scale(1.05); }

    .voice-snippet {
        padding: 1.5rem;
        background: radial-gradient(circle at 50% 50%, #151515 0%, #0e0e0e 100%);
        text-align: center;
        border-bottom: 1px solid #222;
    }
    .quote-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.15rem;
        color: #d0d0d0;
        font-style: italic;
        line-height: 1.3;
    }

    .lore-scroll {
        padding: 1.5rem;
        color: #999;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.05rem;
        line-height: 1.6;
        overflow-y: auto; 
        flex-grow: 1;
        text-align: left; /* LEFT ALIGNED FOR READABILITY */
    }
    /* Custom Scrollbar */
    .lore-scroll::-webkit-scrollbar { width: 6px; }
    .lore-scroll::-webkit-scrollbar-track { background: #0e0e0e; }
    .lore-scroll::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
    .lore-scroll::-webkit-scrollbar-thumb:hover { background: var(--emerald-dim); }

    .footer-meta {
        padding: 0.5rem;
        background: #050505;
        text-align: center;
        font-family: 'Lato', sans-serif;
        font-size: 0.7rem;
        color: #444;
        border-top: 1px solid #222;
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
        # Local fallback
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
        st.info("The Library is empty. Go to the Forge to summon new souls.")
        st.stop()

except Exception as e:
    st.error(f"Could not read from Vault: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 5. LAYOUT & GRID DISPLAY
# -----------------------------------------------------------------------------
st.page_link("home.py", label="< RETURN TO HALL", use_container_width=False)

st.markdown("<h1>THE ARCHIVES OF THE LOST</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>That which is remembered, lives forever.</div>", unsafe_allow_html=True)

# --- SEARCH RUNE ---
search_query = st.text_input("Search the Archives", placeholder="Speak the name, class, or secret...")

# --- FILTER LOGIC ---
if search_query:
    mask = (
        df['Name'].astype(str).str.contains(search_query, case=False) |
        df['Class'].astype(str).str.contains(search_query, case=False) |
        df['Lore'].astype(str).str.contains(search_query, case=False)
    )
    filtered_df = df[mask]
else:
    filtered_df = df

# --- THE GRID OF SOULS ---
if not filtered_df.empty:
    cols = st.columns(3)
    
    # Reverse order to show newest characters first
    for index, row in filtered_df.iloc[::-1].iterrows():
        col_index = index % 3
        
        # Safe Image Handling
        img_src = row.get('Image_URL', '')
        if not str(img_src).startswith("http"):
            img_src = "https://via.placeholder.com/400x250?text=No+Visage"

        # --- NUCLEAR OPTION: Line-by-Line HTML Construction ---
        # This prevents Streamlit from interpreting indentation as a code block.
        card_html = ""
        card_html += f'<div class="archive-card">'
        card_html += f'  <div class="card-header">'
        card_html += f'    <div class="card-name">{row["Name"]}</div>'
        card_html += f'    <div class="card-class">{row["Class"]}</div>'
        card_html += f'  </div>'
        
        card_html += f'  <div class="img-frame">'
        card_html += f'    <a href="{img_src}" target="_blank">'
        card_html += f'      <img src="{img_src}" loading="lazy">'
        card_html += f'    </a>'
        card_html += f'  </div>'
        
        card_html += f'  <div class="voice-snippet">'
        card_html += f'    <div class="quote-text">“{row["Greeting"]}”</div>'
        card_html += f'  </div>'
        
        card_html += f'  <div class="lore-scroll">'
        card_html += f'    {row["Lore"]}'
        card_html += f'  </div>'
        
        card_html += f'  <div class="footer-meta">'
        card_html += f'    ACCESSION: {row.get("Timestamp", "Unknown")}'
        card_html += f'  </div>'
        card_html += f'</div>'
        
        with cols[col_index]:
            st.markdown(card_html, unsafe_allow_html=True)

else:
    st.markdown("<p style='text-align:center; color:#666;'>No souls answer to that name.</p>", unsafe_allow_html=True)

# FOOTER
runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)