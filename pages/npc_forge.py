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
# 2. THE VISUAL ENGINE (Obsidian Slab & Split-Sentence Interaction)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Cormorant+Garamond:wght@400;600&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #111;
        --metal-dark: #1a1a1a;
        --metal-light: #2d2d2d;
        --emerald-glow: #50c878;
        --emerald-dim: #1e3a2a;
    }

    /* --- PAGE BACKGROUND --- */
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

    /* --- THE IRON FORGE CONTAINER --- */
    [data-testid="stForm"] {
        background: linear-gradient(135deg, var(--metal-dark) 0%, #000 100%);
        border: 1px solid #333;
        box-shadow: 
            inset 1px 1px 0px rgba(255,255,255,0.1), 
            inset -1px -1px 0px rgba(0,0,0,0.5),      
            0 0 0 4px #0a0a0a,                        
            0 10px 30px rgba(0,0,0,0.9);              
            
        padding: 0px !important; 
        border-radius: 4px;
        margin-bottom: 2rem;
    }

    /* --- CONTENT PADDING --- */
    [data-testid="stForm"] > div:nth-child(1) {
        padding: 3rem 2rem 2rem 2rem !important;
    }

    /* --- GHOST INPUT FIELDS --- */
    .stTextInput > div > div > input {
        background-color: #050505 !important;
        border: 1px solid #333 !important;
        border-bottom: 1px solid #444 !important;
        box-shadow: inset 0 5px 15px rgba(0,0,0,1) !important;
        color: #d0d0d0 !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.4rem;
        text-align: center;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }

    /* GHOST TEXT LOGIC: Hidden by default */
    .stTextInput input::placeholder {
        color: transparent !important;
        transition: color 0.5s ease-in-out;
        font-style: italic;
        letter-spacing: 1px;
    }

    /* REVEAL LOGIC: Visible on Hover or Focus */
    .stTextInput:hover input::placeholder, 
    .stTextInput input:focus::placeholder {
        color: #444 !important; /* Ghostly Grey */
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--emerald-glow) !important;
        box-shadow: inset 0 5px 10px rgba(0,0,0,1), 0 0 15px rgba(80, 200, 120, 0.1) !important;
    }
    
    .stTextInput label { display: none; }
    [data-testid="InputInstructions"] { display: none !important; }

    /* --- THE PRESSURE PLATE (Button) --- */
    .stButton {
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .stButton > button {
        width: 100% !important;
        margin: 0 !important;
        border-radius: 0 0 4px 4px !important;
        background: linear-gradient(to bottom, #1a1a1a, #000) !important;
        border: none !important;
        border-top: 1px solid #333 !important;
        
        font-family: 'Cinzel', serif !important;
        font-weight: 800 !important;
        letter-spacing: 6px !important;
        font-size: 1.2rem !important;
        color: #555 !important;
        
        height: 80px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(to bottom, #0f2e1d, #05140d) !important;
        color: var(--emerald-glow) !important;
        border-top: 1px solid var(--emerald-glow) !important;
        text-shadow: 0 0 15px var(--emerald-glow);
    }
    
    .stButton > button:active {
        background: #000 !important;
        color: #333 !important;
        transform: translateY(2px);
    }

    /* --- RESULT CARD --- */
    .character-card {
        background: #080808;
        border: 1px solid #222;
        box-shadow: 0 0 40px rgba(0,0,0,0.8);
        border-left: 2px solid var(--emerald-dim);
        padding-bottom: 1rem;
    }
    .card-name {
        background: #111;
        color: #eee;
        font-family: 'Cinzel', serif;
        font-size: 1.8rem;
        padding: 1rem;
        text-align: center;
        border-bottom: 1px solid #222;
    }
    
    /* --- NAVIGATION & FOOTER --- */
    a[data-testid="stPageLink-NavLink"] { display: none; }
    
    .footer-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 4rem;
        opacity: 0.4;
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
    # This is always visible. It starts the sentence.
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
    
    # 2. THE RESPONSE (Ghost Text)
    # This is invisible until hover. It completes the sentence.
    user_input = st.text_input("Concept", placeholder="...AND THE VOID SHALL GIVE IT FORM.")
    
    # The Rune Button
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

    # RESULT CARD
    st.markdown(f"""
    <div class="character-card">
        <div class="card-name">{char_data['Name']}</div>
        <img src="{image_url}" style="width: 100%; display: block; border-bottom: 1px solid #222;">
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