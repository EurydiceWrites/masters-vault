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
# 2. THE VISUAL ENGINE
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Cormorant+Garamond:wght@400;600&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #1c1c1c;
        --stone-dark: #0e0e0e;
        --emerald-glow: #50c878;
        --emerald-dim: #2e5a44;
        --iron-gradient: linear-gradient(180deg, #2b2b2b 0%, #1a1a1a 40%, #000 100%);
    }

    /* --- BACKGROUND --- */
    .stApp {
        background-color: var(--stone-dark);
        background-image: radial-gradient(circle at 50% 10%, #252b27 0%, #000 90%);
        color: #d0d0d0;
        font-family: 'Lato', sans-serif;
    }

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 10px;
        font-size: 3rem !important;
        color: var(--emerald-glow) !important;
        text-shadow: 0 0 25px rgba(80, 200, 120, 0.3);
        text-align: center;
        margin-top: -10px;
        margin-bottom: 0 !important;
    }

    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        font-style: italic;
        color: #888;
        letter-spacing: 2px;
        margin-bottom: 3rem; 
    }

    /* --- NAVIGATION --- */
    a[data-testid="stPageLink-NavLink"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    a[data-testid="stPageLink-NavLink"] p { color: #666; font-family: 'Cinzel', serif; font-size: 0.9rem; }
    a[data-testid="stPageLink-NavLink"]:hover p { color: var(--emerald-glow); }

    /* --- THE ANVIL CONTAINER (The Form) --- */
    [data-testid="stForm"] {
        background: var(--iron-gradient);
        /* CRITICAL FIX: 0 padding on sides/bottom so button hits the edge */
        padding: 4rem 0rem 0rem 0rem !important; 
        border: none;
        
        /* THE ANVIL SHAPE */
        clip-path: polygon(
            0% 0%, 100% 0%,      /* Top Face (Wide) */
            90% 35%, 90% 65%,    /* Right Waist (Deep pinch) */
            100% 100%, 0% 100%,  /* Base (Wide) */
            10% 65%, 10% 35%     /* Left Waist (Deep pinch) */
        );
        
        filter: drop-shadow(0 0 30px rgba(0,0,0,0.9));
        margin-bottom: 2rem;
    }

    /* --- INPUT FIELD --- */
    /* Because parent has 0 padding, we must manually center this and give it width */
    .stTextInput {
        width: 80% !important;
        margin: 0 auto !important; /* Centers the input block */
    }

    .stTextInput > div > div > input {
        background-color: #080808 !important; 
        border: 1px solid #333 !important;
        border-top: 4px solid #000 !important;
        color: #e0e0e0 !important;
        font-family: 'Lato', sans-serif;
        font-size: 1.2rem;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 3rem; 
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--emerald-dim) !important;
    }
    .stTextInput label { display: none; }
    [data-testid="InputInstructions"] { display: none !important; }

    /* --- THE BUTTON FIX --- */
    
    /* 1. Reset the container margins */
    .stButton {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 2. The Button Itself - NO ROUNDING, FULL WIDTH */
    .stButton > button {
        width: 100% !important;
        border-radius: 0px !important; /* Sharp corners are essential */
        background-color: #000 !important; 
        color: #666 !important;
        border: none !important;
        border-top: 2px solid #333 !important; 
        padding: 2rem !important; 
        font-family: 'Cinzel', serif !important;
        font-weight: 900 !important;
        letter-spacing: 8px !important;
        font-size: 1.5rem !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }

    /* 3. Hover Effects */
    .stButton > button:hover {
        color: #fff !important;
        background-color: #0a1f14 !important; 
        text-shadow: 0 0 15px var(--emerald-glow) !important;
        border-top: 2px solid var(--emerald-glow) !important;
        box-shadow: inset 0 0 50px var(--emerald-glow) !important;
    }
    
    .stButton > button:active {
        background-color: #000 !important;
        transform: translateY(2px);
    }

    /* --- RESULT CARD --- */
    .character-card {
        background: #0a0a0a;
        border: 1px solid #222;
        margin-top: 4rem;
        box-shadow: 0 0 50px #000;
        animation: fadein 1s;
    }
    @keyframes fadein { from { opacity: 0; } to { opacity: 1; } }

    .card-name {
        font-family: 'Cinzel', serif;
        font-size: 2rem;
        color: #fff;
        text-align: center;
        padding: 1.5rem;
        border-bottom: 1px solid #222;
        letter-spacing: 3px;
    }
    .visual-block {
        background-color: #080808;
        border-left: 2px solid var(--emerald-dim);
        padding: 1.5rem;
        font-style: italic;
        color: #ccc;
        margin: 1.5rem;
        font-family: 'Cormorant Garamond', serif;
    }
    .lore-section {
        padding: 0 1.5rem 1.5rem 1.5rem;
        color: #888;
        line-height: 1.6;
    }

    /* --- FOOTER RUNES --- */
    .footer-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 5rem;
    }
    .rune-span {
        font-size: 1.5rem;
        color: var(--emerald-dim);
        opacity: 0.3;
        animation: rune-glow 4s infinite ease-in-out;
    }
    @keyframes rune-glow {
        0%, 100% { color: var(--emerald-dim); opacity: 0.3; text-shadow: none; }
        50% { color: var(--emerald-glow); opacity: 0.8; text-shadow: 0 0 10px var(--emerald-dim); }
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

# THE ANVIL CONTAINER
with st.form("forge_form"):
    st.markdown("<p style='font-family: Cinzel; color: #444; text-align: center; font-size: 0.8rem; margin-bottom: 5px; opacity: 0.5;'>INSCRIPTION SURFACE</p>", unsafe_allow_html=True)
    
    # Input Area
    user_input = st.text_input("Concept", placeholder="e.g. A weary executioner who collects butterflies...")
    
    # The Black Button (Base of Anvil)
    submitted = st.form_submit_button("FORGE")

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

    st.markdown(f"""
    <div class="character-card">
        <div class="card-name">{char_data['Name']}</div>
        <img src="{image_url}" style="width: 100%; display: block; border-bottom: 1px solid #222;">
        <div class="visual-block">"{char_data['Visual_Desc']}"</div>
        <div class="lore-section">
            <strong style="color: #50c878; font-family: Cinzel;">CLASS:</strong> {char_data['Class']}<br><br>
            <strong style="color: #50c878; font-family: Cinzel;">GREETING:</strong> "{char_data['Greeting']}"<br><br>
            <strong style="color: #50c878; font-family: Cinzel;">LORE:</strong><br>
            {char_data['Lore']}
        </div>
    </div>
    """, unsafe_allow_html=True)

runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    delay = i * 0.3
    rune_html += f"<span class='rune-span' style='animation-delay: {delay}s'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)