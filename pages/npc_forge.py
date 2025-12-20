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
# 2. THE VISUAL ENGINE (The Obsidian Slab)
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
        --text-main: #d0d0d0;
    }

    /* --- BACKGROUND --- */
    .stApp {
        background-color: var(--stone-dark);
        /* Deep vignette to focus center */
        background-image: radial-gradient(circle at 50% 30%, #222 0%, #000 90%);
        color: var(--text-main);
        font-family: 'Lato', sans-serif;
    }

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 8px;
        font-size: 3rem !important;
        color: var(--emerald-glow) !important;
        text-shadow: 0 0 20px rgba(80, 200, 120, 0.4);
        text-align: center;
        margin-bottom: 0 !important;
    }

    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        font-style: italic;
        color: #666;
        letter-spacing: 2px;
        margin-bottom: 3rem; 
    }

    /* --- NAVIGATION --- */
    a[data-testid="stPageLink-NavLink"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    a[data-testid="stPageLink-NavLink"] p { color: #555; font-family: 'Cinzel', serif; font-size: 0.9rem; transition: color 0.3s;}
    a[data-testid="stPageLink-NavLink"]:hover p { color: var(--emerald-glow); }

    /* --- THE OBSIDIAN SLAB (The Form Container) --- */
    [data-testid="stForm"] {
        background-color: #1a1a1a;
        /* Subtle grit texture */
        background-image: 
            linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), 
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: 20px 20px;
        
        /* The "Heavy Stone" Double Border */
        border: 2px solid #333;
        box-shadow: 
            0 0 0 6px #0e0e0e,           /* Outer black ring */
            0 0 30px rgba(0,0,0,0.8);    /* Deep drop shadow */
        
        border-radius: 4px; /* Slight rounding, not sharp */
        padding: 3rem 2.5rem !important; /* Luxury spacing */
    }

    /* --- INPUT FIELD (The Carved Inscription) --- */
    .stTextInput > div > div > input {
        background-color: #0b0b0b !important; 
        border: 1px solid #2a2a2a !important;
        border-top: 1px solid #000 !important; /* Deepen top edge */
        border-bottom: 1px solid #333 !important; /* Highlight bottom edge */
        
        /* INSET SHADOW makes it look carved into the stone */
        box-shadow: inset 0 4px 8px rgba(0,0,0,0.8) !important;
        
        color: #e0e0e0 !important;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.3rem;
        padding: 1.5rem;
        text-align: center;
        border-radius: 2px;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--emerald-dim) !important;
        color: var(--emerald-glow) !important;
        box-shadow: inset 0 4px 12px rgba(0,0,0,1), 0 0 10px rgba(80,200,120,0.1) !important;
    }
    .stTextInput label { display: none; } /* Hide default label */
    [data-testid="InputInstructions"] { display: none !important; }

    /* --- THE BUTTON (The Rune Activation) --- */
    /* Resetting the Anvil margins - we want a standard block now */
    .stButton {
        width: 100% !important;
        margin-top: 2rem !important;
    }

    .stButton > button {
        width: 100% !important;
        background: linear-gradient(180deg, #2a2a2a 0%, #151515 100%) !important;
        border: 1px solid #444 !important;
        border-bottom: 3px solid #000 !important; /* Heavy bottom for 3D feel */
        color: #888 !important;
        
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        letter-spacing: 4px !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }

    /* HOVER: The Rune Glows */
    .stButton > button:hover {
        background: linear-gradient(180deg, #1f2e25 0%, #0e1a14 100%) !important;
        border-color: var(--emerald-dim) !important;
        color: var(--emerald-glow) !important;
        text-shadow: 0 0 10px var(--emerald-glow) !important;
        box-shadow: 0 0 15px rgba(80, 200, 120, 0.2) !important;
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(2px);
        border-bottom: 1px solid #000 !important;
    }

    /* --- RESULT CARD --- */
    .character-card {
        background: #111;
        border: 1px solid #333;
        border-top: 3px solid var(--emerald-dim); /* Color accent on top only */
        margin-top: 4rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        animation: fadein 1s;
        position: relative;
    }
    @keyframes fadein { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    .card-name {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        color: #fff;
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        letter-spacing: 4px;
        text-shadow: 0 4px 10px #000;
    }
    .visual-block {
        background-color: #080808;
        border-top: 1px solid #222;
        border-bottom: 1px solid #222;
        padding: 1.5rem;
        text-align: center;
        font-style: italic;
        color: #666;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
    }
    .lore-section {
        padding: 2rem;
        color: #999;
        line-height: 1.8;
        font-size: 1.05rem;
    }

    /* --- FOOTER RUNES --- */
    .footer-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 6rem;
        padding-bottom: 2rem;
    }
    .rune-span {
        font-size: 1.5rem;
        color: #333;
        cursor: default;
        transition: color 0.5s;
    }
    .rune-span:hover {
        color: var(--emerald-glow);
        text-shadow: 0 0 10px var(--emerald-glow);
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
    st.markdown("<p style='font-family: Cinzel; color: #555; text-align: center; font-size: 0.9rem; margin-bottom: 1rem; letter-spacing: 2px;'>INSCRIPTION SURFACE</p>", unsafe_allow_html=True)
    
    # Input Area (Now visually 'Carved' into the slab)
    user_input = st.text_input("Concept", placeholder="e.g. A weary executioner who collects butterflies...")
    
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

    # RESULT CARD (Updated to match Slab Design)
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