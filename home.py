import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
import io
import gspread
import json
import datetime
import cloudinary
import cloudinary.uploader

# -----------------------------------------------------------------------------
# 1. SETUP & CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Master's Vault", layout="centered", page_icon="🔮")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (CSS INJECTION)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;800&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --void-bg: #050505;
        --stone-bg: #0f1110; /* Dark Stone */
        --emerald-glow: #50c878;
        --emerald-dim: #1e3a2f;
        --text-main: #d0d0d0;
        --border-color: #2a4035;
    }

    /* --- THE VOID (Background) --- */
    .stApp {
        background-color: var(--void-bg);
        /* Subtle texture instead of sci-fi gradient */
        background-image: url("https://www.transparenttextures.com/patterns/black-scales.png"); 
        color: var(--text-main);
        font-family: 'Lato', sans-serif;
    }

    /* --- HEADER (The Inscription) --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 6px;
        color: var(--emerald-glow) !important;
        text-shadow: 0 0 10px rgba(80, 200, 120, 0.3);
        text-align: center;
        margin-bottom: 0.5rem !important; /* Tight to the runes below */
    }

    /* --- THE RUNES (Decorative Separation) --- */
    .rune-divider {
        font-size: 1.5rem;
        color: var(--emerald-dim);
        text-align: center;
        letter-spacing: 1.5rem;
        margin-bottom: 3rem; /* MASSIVE SPACE HERE helps remove sci-fi feel */
        opacity: 0.7;
        font-family: sans-serif;
    }

    /* --- SUBTEXT (Status) --- */
    .subtext {
        text-align: center;
        font-family: 'Cinzel', serif;
        font-size: 0.8rem;
        color: #666;
        letter-spacing: 2px;
        margin-bottom: 4rem; /* SEPARATION */
        border-bottom: 1px solid var(--emerald-dim);
        display: inline-block;
        padding-bottom: 10px;
    }
    
    /* Center the subtext container */
    .subtext-container {
        display: flex;
        justify-content: center;
        width: 100%;
    }

    /* --- INPUT FIELDS (Dark Stone Block) --- */
    /* No transparency, no blur. Solid stone. */
    .stTextInput > div > div > input {
        background-color: var(--stone-bg) !important; 
        border: 1px solid var(--border-color) !important;
        color: #fff !important;
        font-family: 'Lato', sans-serif;
        font-size: 1.1rem;
        padding: 15px;
        border-radius: 2px; /* Slight rounding, stone-like */
        box-shadow: inset 0 0 10px #000;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--emerald-glow) !important;
        box-shadow: 0 0 15px rgba(80, 200, 120, 0.1) !important;
    }

    /* Label Styling */
    .stTextInput label {
        color: var(--emerald-glow) !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    /* --- BUTTONS (Physical Tablet) --- */
    .stButton > button {
        width: 100%;
        background-color: #0f1613; /* Dark green-black */
        color: #fff;
        border: 1px solid var(--emerald-dim);
        padding: 1rem;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        letter-spacing: 3px;
        transition: all 0.3s ease;
        border-radius: 2px;
        margin-top: 29px; /* Aligns with input box */
    }

    .stButton > button:hover {
        background-color: var(--emerald-dim);
        border-color: var(--emerald-glow);
        box-shadow: 0 0 15px rgba(80, 200, 120, 0.2);
        color: #fff;
    }
    
    /* --- CHARACTER CARD (Parchment/Stone Style) --- */
    .character-card {
        background-color: #0a0a0a;
        border: 1px solid var(--emerald-dim);
        padding: 40px;
        margin-top: 4rem; /* DISTANCE from input */
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
    }
    
    .card-name {
        font-family: 'Cinzel', serif;
        font-size: 2.5rem;
        color: #fff;
        text-align: center;
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 20px;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }
    
    .visual-block {
        background-color: #0e1210;
        border-left: 4px solid var(--emerald-dim);
        padding: 20px;
        font-style: italic;
        color: #ccc;
        margin: 20px 0;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AUTH & LOGIC
# -----------------------------------------------------------------------------
def setup_auth():
    try:
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        
        if "gcp_service_account" in st.secrets:
            creds = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes=SCOPES
            )
            gc = gspread.authorize(creds)
        else:
            return None, None, "Missing Google Secrets"

        if "cloudinary" in st.secrets:
            cloudinary.config(
                cloud_name = st.secrets["cloudinary"]["cloud_name"],
                api_key = st.secrets["cloudinary"]["api_key"],
                api_secret = st.secrets["cloudinary"]["api_secret"],
                secure = True
            )
        
        if "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
        return gc, True, "Success"
    except Exception as e:
        return None, False, str(e)

# -----------------------------------------------------------------------------
# 4. MAIN LAYOUT
# -----------------------------------------------------------------------------
def main():
    gc, auth_success, auth_msg = setup_auth()

    if not auth_success:
        st.error(f"System Failure: {auth_msg}")
        st.stop()

    # --- HEADER SECTION ---
    st.markdown("<h1>THE MASTER'S VAULT</h1>", unsafe_allow_html=True)
    # The Runes are now their own div, separated by CSS margins
    st.markdown("<div class='rune-divider'>ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈ</div>", unsafe_allow_html=True)
    
    # The Subtext is visually distinct and pushed down
    st.markdown("<div class='subtext-container'><div class='subtext'>SYSTEM ONLINE // CONNECTED TO THE VOID</div></div>", unsafe_allow_html=True)

    # --- INPUT SECTION ---
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input("CORE CONCEPT", placeholder="e.g. A weary knight with a rusted shield...")
    with col2: