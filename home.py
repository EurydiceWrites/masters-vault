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
st.set_page_config(page_title="Master's Vault", layout="centered", page_icon="⚔️")

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (CSS INJECTION)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;800&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #1c1c1c; /* Solid Dark Stone */
        --stone-dark: #111111;
        --emerald-glow: #50c878;
        --emerald-dim: #2e5a44;
        --text-main: #d0d0d0;
        --border-color: #3a3a3a;
    }

    /* --- BACKGROUND (Solid Stone, No Sci-Fi Stars) --- */
    .stApp {
        background-color: var(--stone-dark);
        background-image: radial-gradient(circle at center, #252525 0%, #0a0a0a 100%);
        color: var(--text-main);
        font-family: 'Lato', sans-serif;
    }

    /* --- HEADER (The Inscription) --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 8px;
        font-size: 3.5rem !important;
        color: var(--emerald-glow) !important;
        text-shadow: 0 5px 15px rgba(0,0,0,0.8);
        text-align: center;
        margin-bottom: 2rem !important; /* SEPARATION */
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 2rem;
    }

    /* --- THE RUNES (Decorative Separation) --- */
    .rune-divider {
        font-size: 1.2rem;
        color: #444; /* Darker, etched look */
        text-align: center;
        letter-spacing: 2rem;
        margin-bottom: 4rem; /* MASSIVE SPACE HERE */
        font-family: sans-serif;
        text-shadow: 0 1px 0 rgba(255,255,255,0.1);
    }

    /* --- SUBTEXT (Fantasy Flavor) --- */
    .subtext {
        text-align: center;
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
        color: #666;
        letter-spacing: 3px;
        margin-bottom: 3rem; 
        text-transform: uppercase;
    }

    /* --- INPUT FIELDS (Carved Stone Block) --- */
    .stTextInput > div > div > input {
        background-color: #222 !important; 
        border: 2px solid #333 !important; /* Physical border, not glowing */
        border-top: 4px solid #111 !important; /* Shadow effect */
        color: #e0e0e0 !important;
        font-family: 'Lato', sans-serif;
        font-size: 1.1rem;
        padding: 15px;
        border-radius: 4px;
        box-shadow: inset 0 5px 10px rgba(0,0,0,0.5); /* Inner shadow for depth */
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--emerald-dim) !important;
        background-color: #252525 !important;
    }

    /* Label Styling */
    .stTextInput label {
        color: #888 !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 1px;
        margin-bottom: 15px;
    }

    /* --- BUTTONS (Physical Tablet) --- */
    .stButton > button {
        width: 100%;
        background-color: #1a2e25; /* Dark Emerald Stone */
        color: #ccc;
        border: 1px solid #2e5a44;
        border-bottom: 4px solid #11221a; /* 3D Effect */
        padding: 1rem;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        letter-spacing: 3px;
        transition: all 0.2s ease;
        border-radius: 4px;
        margin-top: 29px; /* Aligns with input box */
        text-transform: uppercase;
    }

    .stButton > button:hover {
        background-color: #2e5a44;
        color: #fff;
        transform: translateY(2px); /* Physical press effect */
        border-bottom: 2px solid #11221a;
    }
    
    /* --- CHARACTER CARD (Parchment/Stone Style) --- */
    .character-card {
        background-color: #181818;
        border: 1px solid #333;
        padding: 40px;
        margin-top: 5rem; /* DISTANCE from input */
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        border-radius: 4px;
    }
    
    .card-name {
        font-family: 'Cinzel', serif;
        font-size: 2.5rem;
        color: #e0e0e0;
        text-align: center;
        border-bottom: 1px solid #333;
        padding-bottom: 20px;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }
    
    .visual-block {
        background-color: #111;
        border-left: 4px solid var(--emerald-dim);
        padding: 20px;
        font-style: italic;
        color: #bbb;
        margin: 20px 0;
        line-height: 1.6;
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
    # 1. The Title
    st.markdown("<h1>THE MASTER'S VAULT</h1>", unsafe_allow_html=True)
    
    # 2. The Subtext (Now Fantasy Themed)
    st.markdown("<div class='subtext'>THE FORGE AWAITS YOUR COMMAND</div>", unsafe_allow_html=True)

    # 3. The Divider (Visual separation)
    st.markdown("<div class='rune-divider'>ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈ</div>", unsafe_allow_html=True)

    # --- INPUT SECTION ---
    col1, col2 = st.columns([3, 1])
    
    # Fix for the Indentation Error: Ensure everything inside 'with' is indented
    with col1:
        user_input = st.text_input("CORE CONCEPT", placeholder="e.g. A weary knight with a rusted shield...")
    
    with col2:
        # Button text updated to "SUMMON CREATION"
        generate_btn = st.button("SUMMON CREATION")

    # --- GENERATION LOGIC ---
    if generate_btn and user_input:
        
        # A. Text Generation
        with st.spinner("Forging..."):
            try:
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
                st.error(f"Text Gen Failed: {e}")
                st.stop()

        # B. Image Generation
        with st.spinner("Summoning Visuals..."):
            try:
                image_model = genai.GenerativeModel('models/gemini-3-pro-image-preview')
                img_prompt = f"Hyper-realistic photograph, dark fantasy, {char_data['Visual_Desc']}, Norse aesthetic, gritty, 8k, cinematic lighting."
                img_response = image_model.generate_content(img_prompt)
                
                if img_response.parts:
                    img_bytes = img_response.parts[0].inline_data.data
                    upload_result = cloudinary.uploader.upload(io.BytesIO(img_bytes), folder="masters_vault_npcs")
                    image_url = upload_result.get("secure_url")
                else:
                    image_url = "https://via.placeholder.com/500?text=Manifestation+Failed"
            except Exception as e:
                st.error(f"Image Gen Failed: {e}")
                image_url = "https://via.placeholder.com/500?text=Error"

        # C. Save to DB
        try:
            sh = gc.open("Masters_Vault_Db")
            worksheet = sh.get_worksheet(0)
            row_data = [char_data['Name'], char_data['Class'], char_data['Lore'], char_data['Greeting'], char_data['Visual_Desc'], image_url, str(datetime.datetime.now())]
            worksheet.append_row(row_data)
            st.toast("Saved to the Vault", icon="⚔️")
        except Exception as e:
            st.error(f"Save Failed: {e}")

        # D. HTML Injection for the Card
        st.markdown(f"""
        <div class="character-card">
            <div class="card-name">{char_data['Name']}</div>
            
            <div style="border: 4px solid #111; padding: 0; margin-bottom: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
                <img src="{image_url}" style="width: 100%; display: block; opacity: 1.0;">
            </div>
            
            <div class="visual-block">
                <span style="font-size: 0.7rem; color: #50c878; display: block; margin-bottom: 8px; font-family: Cinzel; letter-spacing: 2px;">VISUAL DESCRIPTION</span>
                {char_data['Visual_Desc']}
            </div>
            
            <div style="margin-top: 30px; font-size: 0.95rem; line-height: 1.6; color: #aaa;">
                <strong style="color: #50c878; font-family: Cinzel;">CLASS:</strong> {char_data['Class']}<br><br>
                <strong style="color: #50c878; font-family: Cinzel;">GREETING:</strong> "{char_data['Greeting']}"<br><br>
                <strong style="color: #50c878; font-family: Cinzel;">LORE:</strong><br>
                {char_data['Lore']}
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()