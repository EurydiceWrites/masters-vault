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
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;800&family=Lato:wght@300;400&display=swap');

    /* --- VARIABLES --- */
    :root {
        --void-bg: #020403;
        --obsidian-glass: rgba(10, 15, 13, 0.95); /* Slightly more opaque for readability */
        --emerald-glow: #50c878;
        --emerald-dim: #1a3c2f;
        --text-main: #e0e0e0;
    }

    /* --- THE VOID (Background) --- */
    .stApp {
        background-color: var(--void-bg);
        background-image: 
            radial-gradient(circle at 50% 30%, #0f1c15 0%, transparent 70%),
            linear-gradient(180deg, #000 0%, #050a07 100%);
        color: var(--text-main);
        font-family: 'Lato', sans-serif;
    }

    /* --- HEADERS & RUNES --- */
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 4px;
        color: var(--emerald-glow) !important;
        text-shadow: 0 0 15px rgba(80, 200, 120, 0.4);
        position: relative;
    }
    
    /* FIX: Runes are now Bright Green so you can actually see them */
    h1::after {
        content: 'ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ ᚺ ᚾ ᛁ ᛃ ᛇ ᛈ';
        display: block;
        font-family: sans-serif;
        font-size: 1.2rem;
        letter-spacing: 1rem;
        color: var(--emerald-glow); /* Changed from Dim to Glow */
        margin-top: 10px;
        opacity: 0.8;
        text-shadow: 0 0 10px rgba(80, 200, 120, 0.5);
        text-align: center;
    }

    /* Streamlit's default top padding removal */
    .block-container {
        padding-top: 2rem;
    }

    /* --- INPUT FIELDS --- */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid var(--emerald-dim) !important;
        border-left: 3px solid var(--emerald-glow) !important; /* Accent on left */
        border-radius: 4px !important;
        color: #fff !important;
        font-family: 'Lato', sans-serif;
        font-size: 1.1rem;
        padding: 12px 15px;
        box-shadow: inset 0 0 20px #000;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--emerald-glow) !important;
        box-shadow: 0 0 15px rgba(80, 200, 120, 0.2) !important;
        background-color: rgba(80, 200, 120, 0.05) !important;
    }

    .stTextInput label {
        color: var(--emerald-glow) !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }

    /* --- BUTTONS (Fixed the "Weird" Shape) --- */
    .stButton > button {
        width: 100%;
        background: #0b1a12; /* Dark Green Base */
        color: #fff;
        border: 1px solid var(--emerald-glow);
        padding: 0.8rem 1rem;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        border-radius: 4px; /* Standard rounded corners, no weird clipping */
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }

    .stButton > button:hover {
        background: var(--emerald-glow);
        color: #000;
        box-shadow: 0 0 20px rgba(80, 200, 120, 0.6);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }

    /* --- CHARACTER CARD --- */
    .character-card {
        margin-top: 3rem;
        position: relative;
        filter: drop-shadow(0 10px 30px rgba(0,0,0,0.9));
    }

    .card-inner {
        background: var(--obsidian-glass);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border: 1px solid var(--emerald-dim);
        border-top: 4px solid var(--emerald-glow); /* Strong top bar */
        border-radius: 2px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
    }

    /* Card Typography */
    .card-name {
        color: #fff;
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 10px rgba(80, 200, 120, 0.6);
        letter-spacing: 3px;
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 10px;
    }

    /* Image Frame */
    .image-frame {
        border: 1px solid var(--emerald-dim);
        padding: 5px;
        background: #000;
        margin-bottom: 1.5rem;
    }

    .visual-desc {
        background: rgba(0, 0, 0, 0.4);
        border-left: 3px solid var(--emerald-glow);
        padding: 1rem 1.5rem;
        margin: 1.5rem 0;
        color: #dcdcdc;
        font-style: italic;
        font-family: 'Lato', sans-serif;
        line-height: 1.6;
    }
    
    .lore-section {
        font-size: 0.95rem;
        color: #a0a0a0;
        margin-top: 2rem;
        border-top: 1px solid var(--emerald-dim);
        padding-top: 1rem;
    }
    
    /* Toast Styling */
    div[data-baseweb="toast"] {
        background-color: var(--emerald-dim) !important;
        color: white !important;
        border: 1px solid var(--emerald-glow);
        font-family: 'Cinzel', serif;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AUTH & BACKEND LOGIC
# -----------------------------------------------------------------------------
def setup_auth():
    try:
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        
        # Google Sheets
        if "gcp_service_account" in st.secrets:
            creds = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes=SCOPES
            )
            gc = gspread.authorize(creds)
        else:
            return None, None, "Missing Google Secrets"

        # Cloudinary
        if "cloudinary" in st.secrets:
            cloudinary.config(
                cloud_name = st.secrets["cloudinary"]["cloud_name"],
                api_key = st.secrets["cloudinary"]["api_key"],
                api_secret = st.secrets["cloudinary"]["api_secret"],
                secure = True
            )
        
        # Gemini
        if "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
        return gc, True, "Success"
    except Exception as e:
        return None, False, str(e)

# -----------------------------------------------------------------------------
# 4. MAIN APPLICATION
# -----------------------------------------------------------------------------
def main():
    gc, auth_success, auth_msg = setup_auth()

    if not auth_success:
        st.error(f"System Failure: {auth_msg}")
        st.stop()

    st.title("THE MASTER'S VAULT")
    st.markdown("<p style='text-align: center; color: #50c878; font-family: Cinzel; letter-spacing: 2px; font-size: 0.8rem; margin-top: -10px; opacity: 0.8;'>SYSTEM ONLINE // CONNECTED TO THE VOID</p>", unsafe_allow_html=True)

    # THE INPUT AREA
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        # Changed placeholder to simple, clear language
        user_input = st.text_input("ENTER CHARACTER CONCEPT", placeholder="e.g. A weary knight with a rusted shield...")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True) # Spacer
        # Changed Button text to be less weird
        generate_btn = st.button("MANIFEST")

    # THE GENERATION LOGIC
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
            st.toast("Saved to the Vault", icon="🔮")
        except Exception as e:
            st.error(f"Save Failed: {e}")

        # D. HTML Injection for the Card
        st.markdown(f"""
        <div class="character-card">
            <div class="card-inner">
                <div class="card-name">{char_data['Name']}</div>
                
                <div class="image-frame">
                    <img src="{image_url}" style="width: 100%; display: block; opacity: 0.9;">
                </div>
                
                <div class="visual-desc">
                    <span style="font-size: 0.7rem; color: #50c878; display: block; margin-bottom: 8px; font-family: Cinzel; letter-spacing: 2px;">👁️ VISUAL DESCRIPTION</span>
                    {char_data['Visual_Desc']}
                </div>
                
                <div class="lore-section">
                    <strong style="color: #50c878; text-transform: uppercase; font-family: Cinzel;">Class / Role:</strong> <span style="color: #ccc;">{char_data['Class']}</span><br><br>
                    <strong style="color: #50c878; text-transform: uppercase; font-family: Cinzel;">Greeting:</strong> <span style="color: #ccc;">"{char_data['Greeting']}"</span><br><br>
                    <strong style="color: #50c878; text-transform: uppercase; font-family: Cinzel;">📜 Lore:</strong><br>
                    <span style="color: #bbb; line-height: 1.6;">{char_data['Lore']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()