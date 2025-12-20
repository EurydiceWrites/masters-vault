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
# 1. CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Master's Vault",
    page_icon="🐉",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (CSS INJECTION)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;800&family=Lato:wght@300;400&display=swap');

    /* --- VARIABLES --- */
    :root {
        --void-bg: #030303;
        --emerald-glow: #50c878;
        --emerald-dim: #1e4a3b;
        --text-main: #c0c0c0;
    }

    /* --- THE VOID (Background) --- */
    .stApp {
        background-color: var(--void-bg);
        background-image: 
            radial-gradient(circle at 50% 0%, #1a2e25 0%, transparent 60%),
            linear-gradient(0deg, #000 0%, #080808 100%);
        color: var(--text-main);
        font-family: 'Lato', sans-serif;
    }

    /* --- HEADERS --- */
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 4px;
        color: var(--emerald-glow) !important;
        text-shadow: 0 0 20px rgba(80, 200, 120, 0.4);
    }
    
    /* Streamlit's default top padding removal */
    .block-container {
        padding-top: 2rem;
    }

    /* --- INPUT FIELDS (The Command Line Look) --- */
    /* We remove the box and make it a sleek underline */
    .stTextInput > div > div > input {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid var(--emerald-dim) !important;
        color: #fff !important;
        font-family: 'Lato', sans-serif;
        font-size: 1.1rem;
        padding: 10px 0;
        border-radius: 0;
    }

    .stTextInput > div > div > input:focus {
        border-bottom-color: var(--emerald-glow) !important;
        box-shadow: 0 10px 20px -10px rgba(80, 200, 120, 0.2) !important;
    }

    .stTextInput label {
        color: var(--emerald-dim) !important;
        font-family: 'Cinzel', serif !important;
        letter-spacing: 2px;
        font-size: 0.8rem;
    }

    /* --- BUTTONS (The Rune Key) --- */
    .stButton > button {
        width: 100%;
        background-color: var(--emerald-dim);
        color: #fff;
        border: none;
        padding: 0.75rem 1rem;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        letter-spacing: 3px;
        transition: all 0.3s ease;
        
        /* The Sci-Fi Cut Corner */
        clip-path: polygon(10% 0, 100% 0, 100% 100%, 0% 100%);
    }

    .stButton > button:hover {
        background-color: var(--emerald-glow);
        color: #000;
        padding-left: 2rem; /* Slide effect */
        text-shadow: 0 0 10px rgba(255,255,255,0.5);
    }
    
    /* --- TOAST ALERTS --- */
    div[data-baseweb="toast"] {
        background-color: #0b3d26 !important;
        color: white !important;
        border: 1px solid #50c878;
        font-family: 'Cinzel', serif;
    }

    /* --- CUSTOM ARTIFACT CARD --- */
    .character-card {
        background: #080a09;
        position: relative;
        padding: 2px; /* Gradient border width */
        margin-top: 2rem;
        
        /* Angled Corners */
        clip-path: polygon(
            20px 0, 100% 0, 
            100% calc(100% - 20px), calc(100% - 20px) 100%, 
            0 100%, 0 20px
        );
    }

    .card-inner {
        background: #080a09;
        padding: 2rem;
        /* Match outer clip */
        clip-path: polygon(
            20px 0, 100% 0, 
            100% calc(100% - 20px), calc(100% - 20px) 100%, 
            0 100%, 0 20px
        );
    }
    
    /* Glowing Border Pseudo-element */
    .character-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, var(--emerald-dim), #000 40%, #000 60%, var(--emerald-dim));
        z-index: 0;
    }
    
    .card-content {
        position: relative;
        z-index: 1;
    }

    /* Card Typography */
    .card-name {
        color: #fff;
        font-family: 'Cinzel', serif;
        font-size: 2rem;
        text-align: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 0.5rem;
    }

    .visual-desc {
        background: rgba(80, 200, 120, 0.05);
        border-left: 2px solid var(--emerald-glow);
        padding: 1rem;
        margin: 1.5rem 0;
        color: #e0e0e0;
        font-style: italic;
    }
    
    .lore-section {
        font-size: 0.85rem;
        color: #666;
        margin-top: 1.5rem;
        border-top: 1px solid #1a1a1a;
        padding-top: 1rem;
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
# 4. MAIN APP
# -----------------------------------------------------------------------------
def main():
    gc, auth_success, auth_msg = setup_auth()

    if not auth_success:
        st.error(f"System Failure: {auth_msg}")
        st.stop()

    st.title("THE MASTER'S VAULT")
    st.markdown("<p style='text-align: center; color: #444; font-family: Cinzel; margin-top: -20px;'>SYSTEM ONLINE // CONNECTED TO THE VOID</p>", unsafe_allow_html=True)

    # THE INPUT (Styled as a command line)
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input("CORE CONCEPT", placeholder="Type your vision here...")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True) # Spacer
        generate_btn = st.button("IGNITE")

    # THE GENERATION LOGIC
    if generate_btn and user_input:
        
        # A. Text Generation
        with st.spinner("Forging soul..."):
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
        with st.spinner("Manifesting form..."):
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
            st.toast("Saved to Archives", icon="💾")
        except Exception as e:
            st.error(f"Save Failed: {e}")

        # D. HTML Injection for the Card (Using REAL Data)
        st.markdown(f"""
        <div class="character-card">
            <div class="card-inner">
                <div class="card-content">
                    <div class="card-name">{char_data['Name']}</div>
                    
                    <div style="border: 1px solid #1a2e25; padding: 2px; margin-bottom: 1.5rem;">
                        <img src="{image_url}" style="width: 100%; display: block; opacity: 0.9;">
                    </div>
                    
                    <div class="visual-desc">
                        <span style="font-size: 0.6rem; color: #50c878; display: block; margin-bottom: 5px; font-family: Cinzel;">VISUAL SCAN</span>
                        {char_data['Visual_Desc']}
                    </div>
                    
                    <div class="lore-section">
                        <strong style="color: #444; text-transform: uppercase; font-family: Cinzel;">Class / Role:</strong> <span style="color: #888;">{char_data['Class']}</span><br><br>
                        <strong style="color: #444; text-transform: uppercase; font-family: Cinzel;">Greeting:</strong> <span style="color: #888;">"{char_data['Greeting']}"</span><br><br>
                        <strong style="color: #333; text-transform: uppercase;">Archive Data:</strong><br>
                        {char_data['Lore']}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()