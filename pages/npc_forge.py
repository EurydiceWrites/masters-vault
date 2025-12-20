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
st.set_page_config(page_title="The NPC Forge", layout="centered", page_icon="⚒️")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (Polished Obsidian)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Cormorant+Garamond:wght@400;600&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #111;
        --metal-dark: #1a1a1a;
        --emerald-glow: #50c878;
        --emerald-dim: #1e3a2a;
    }

    /* --- GLOBAL POLISH --- */
    /* Fixes the ugly blue highlight when selecting text */
    ::selection {
        background: var(--emerald-dim); 
        color: var(--emerald-glow);
    }
    
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1f2b24 0%, #000 80%);
    }

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 12px;
        font-size: 3.5rem !important;
        color: var(--emerald-glow) !important;
        text-shadow: 0 0 30px rgba(80, 200, 120, 0.4);
        margin-bottom: 0 !important;
        text-align: center;
    }
    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        color: #666;
        font-style: italic;
        margin-bottom: 3rem;
    }

    /* --- THE FORM CONTAINER (The Slab) --- */
    [data-testid="stForm"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #000 100%);
        border: 1px solid #333;
        box-shadow: 0 10px 40px rgba(0,0,0,0.9);
        padding: 0px !important; /* Critical for button alignment */
        border-radius: 4px;
        margin-bottom: 3rem;
        overflow: hidden; /* Keeps the button corners sharp */
    }

    /* --- CONTENT AREA (Inputs) --- */
    /* We add padding back to the top section only */
    [data-testid="stForm"] > div:nth-child(1) {
        padding: 3rem 2rem 2rem 2rem !important;
    }

    /* --- INPUT STYLING --- */
    .stTextInput > div > div > input {
        background-color: #080808 !important;
        border: 1px solid #333 !important;
        box-shadow: inset 0 2px 10px rgba(0,0,0,1) !important;
        color: #e0e0e0 !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.3rem;
        text-align: center;
        padding: 1.5rem;
    }
    
    /* GHOST TEXT LOGIC */
    .stTextInput input::placeholder { 
        color: transparent !important; 
        transition: color 0.5s; 
        font-style: italic;
    }
    .stTextInput:hover input::placeholder, .stTextInput input:focus::placeholder { 
        color: #444 !important; 
    }
    
    /* Remove Labels */
    .stTextInput label { display: none; }
    [data-testid="InputInstructions"] { display: none !important; }

    /* --- THE BUTTON (THE BASE) --- */
    /* Forces the button to be full width and attached to the bottom */
    .stButton {
        width: 100% !important;
        margin-top: 0rem !important;
        padding: 0 !important;
    }
    
    .stButton > button {
        width: 100% !important;
        border-radius: 0px !important; /* Square corners to fit the slab */
        background: linear-gradient(to bottom, #222, #000) !important;
        border: none !important;
        border-top: 1px solid #444 !important;
        color: #666 !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        letter-spacing: 4px !important;
        font-size: 1.1rem !important;
        height: 70px !important;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #0f1a15 !important;
        color: var(--emerald-glow) !important;
        border-top: 1px solid var(--emerald-glow) !important;
        text-shadow: 0 0 10px var(--emerald-glow);
    }
    
    .stButton > button:active {
        background: #000 !important;
        color: #333 !important;
    }

    /* --- RESULT CARD POLISH --- */
    .character-card {
        background: #0a0a0a;
        border: 1px solid #222;
        border-top: 3px solid var(--emerald-dim); /* Subtle color hint */
        box-shadow: 0 20px 50px rgba(0,0,0,1);
        margin-top: 2rem;
        animation: fadein 1s;
    }
    @keyframes fadein { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    
    .card-name {
        font-family: 'Cinzel', serif;
        font-size: 2rem;
        color: #fff;
        text-align: center;
        padding: 1.5rem;
        letter-spacing: 4px;
        background: #111;
        border-bottom: 1px solid #222;
    }
    
    /* Image Polish */
    .character-card img {
        width: 100%;
        display: block;
        opacity: 0.9;
        transition: opacity 0.5s;
    }
    .character-card img:hover { opacity: 1; }
    
    /* Text Polish */
    .visual-block {
        background: #050505;
        padding: 1.5rem 2rem; 
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        color: #888;
        text-align: center;
        border-bottom: 1px solid #222;
    }
    
    .lore-section {
        padding: 2.5rem; /* LUXURY SPACING */
        color: #aaa;
        line-height: 1.8; /* Easier to read */
        font-size: 1.1rem;
        font-family: 'Lato', sans-serif;
    }
    
    /* Footer Polish */
    .footer-container { opacity: 0.3; text-align: center; margin-top: 4rem; padding-bottom: 2rem;}
    .rune-span { margin: 0 10px; font-size: 1.2rem; color: #444; cursor: default; }

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
            return gc, True, "Success"
        return None, None, "Missing Google Secrets"
    except Exception as e:
        return None, False, str(e)

gc, auth_success, auth_msg = setup_auth()
if not auth_success:
    st.error(f"System Failure: {auth_msg}")
    st.stop()

# -----------------------------------------------------------------------------
# 4. LAYOUT
# -----------------------------------------------------------------------------
st.page_link("home.py", label="< RETURN TO VAULT", use_container_width=False)

st.markdown("<h1>THE NPC FORGE</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Inscribe the soul. Strike the iron.</div>", unsafe_allow_html=True)

# THE OBSIDIAN SLAB CONTAINER
with st.form("forge_form"):
    
    # 1. THE CALL (Label)
    st.markdown("""
        <p style='
            font-family: Cinzel; 
            color: #555; 
            text-align: center; 
            font-size: 1rem; 
            margin-bottom: 1rem; 
            letter-spacing: 4px; 
            text-transform: uppercase;
            opacity: 0.8;'>
            WHISPER THE DESIRE...
        </p>
    """, unsafe_allow_html=True)
    
    # 2. THE RESPONSE (Ghost Input)
    # The placeholder completes the sentence "Whisper the desire... and the void shall give it form."
    user_input = st.text_input("Concept", placeholder="...AND THE VOID SHALL GIVE IT FORM.")
    
    # 3. THE LEVER (Button)
    submitted = st.form_submit_button("STRIKE THE ANVIL")

# -----------------------------------------------------------------------------
# 5. GENERATION
# -----------------------------------------------------------------------------
if submitted and user_input:
    
    with st.spinner("Summoning the soul..."):
        try:
            if "GOOGLE_API_KEY" in st.secrets:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            text_model = genai.GenerativeModel('models/gemini-3-pro-preview')
            text_prompt = f"""
            Role: Dark Fantasy DM Assistant.
            Task: Create a detailed NPC based on: "{user_input}".
            Rules: Norse-inspired name (EASY to pronounce). Dark, gritty tone. No Stats.
            Format: JSON with keys: Name, Class, Visual_Desc, Lore, Greeting.
            """
            text_response = text_model.generate_content(text_prompt)
            clean_json = text_response.text.replace("```json", "").replace("```", "").strip()
            char_data = json.loads(clean_json)
        except Exception as e:
            st.error(f"Forging Failed: {e}")
            st.stop()

    with st.spinner("Conjuring the form..."):
        try:
            image_model = genai.GenerativeModel('models/gemini-3-pro-image-preview')
            img_prompt = f"Hyper-realistic photograph, dark fantasy, {char_data['Visual_Desc']}, Norse aesthetic, gritty, 8k, cinematic lighting."
            img_response = image_model.generate_content(img_prompt)
            
            if img_response.parts:
                img_bytes = img_response.parts[0].inline_data.data
                if "cloudinary" in st.secrets:
                    cloudinary.config(
                        cloud_name = st.secrets["cloudinary"]["cloud_name"],
                        api_key = st.secrets["cloudinary"]["api_key"],
                        api_secret = st.secrets["cloudinary"]["api_secret"],
                        secure = True
                    )
                    upload_result = cloudinary.uploader.upload(io.BytesIO(img_bytes), folder="masters_vault_npcs")
                    image_url = upload_result.get("secure_url")
                else:
                    image_url = "https://via.placeholder.com/500?text=Cloudinary+Missing"
            else:
                image_url = "https://via.placeholder.com/500?text=Manifestation+Failed"
        except Exception as e:
            st.error(f"Image Gen Failed: {e}")
            image_url = "https://via.placeholder.com/500?text=Error"

    try:
        sh = gc.open("Masters_Vault_Db")
        worksheet = sh.get_worksheet(0)
        row_data = [char_data['Name'], char_data['Class'], char_data['Lore'], char_data['Greeting'], char_data['Visual_Desc'], image_url, str(datetime.datetime.now())]
        worksheet.append_row(row_data)
        st.toast("Entity Forged.", icon="⚒️")
    except Exception as e:
        st.error(f"Save Failed: {e}")

    # RESULT CARD (Updated to match Slab Design with Padding)
    st.markdown(f"""
    <div class="character-card">
        <div class="card-name">{char_data['Name']}</div>
        <img src="{image_url}">
        <div class="visual-block">"{char_data['Visual_Desc']}"</div>
        <div class="lore-section">
            <strong style="color: #50c878; font-family: Cinzel; letter-spacing: 1px;">CLASS:</strong> <span style="color: #ccc;">{char_data['Class']}</span><br><br>
            <strong style="color: #50c878; font-family: Cinzel; letter-spacing: 1px;">GREETING:</strong> <span style="color: #ccc;">"{char_data['Greeting']}"</span><br><br>
            <strong style="color: #50c878; font-family: Cinzel; letter-spacing: 1px;">LORE:</strong><br>
            {char_data['Lore']}
        </div>
    </div>
    """, unsafe_allow_html=True)

# FOOTER
runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)