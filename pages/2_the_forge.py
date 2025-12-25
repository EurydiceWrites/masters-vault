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
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="The NPC Forge", layout="centered", page_icon="⚒️")

# Initialize Session State
if "npc_data" not in st.session_state:
    st.session_state.npc_data = None
if "last_concept" not in st.session_state:
    st.session_state.last_concept = ""

# -----------------------------------------------------------------------------
# 2. THE VISUAL ENGINE (The Void Theme)
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

    /* --- GLOBAL BACKGROUND --- */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 30%, #1a1a1a 0%, #000 80%);
    }

    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] { 
        background-color: #080808; 
        border-right: 1px solid #1e3a2a; 
    }
    .sidebar-header {
        font-family: 'Cinzel', serif;
        color: var(--emerald-bright);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        margin-top: 2rem;
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 0.5rem;
        text-align: center;
        text-shadow: 0 0 10px var(--emerald-dim);
    }
    header[data-testid="stHeader"] { background: transparent; }

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 12px;
        font-size: 3.5rem !important;
        color: var(--emerald-bright) !important;
        text-shadow: 0 0 40px rgba(102, 255, 153, 0.4);
        margin-bottom: 0 !important;
        text-align: center;
        margin-top: 10vh !important;
    }
    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.4rem;
        color: #888;
        font-style: italic;
        margin-bottom: 4rem;
    }

    /* --- NAVIGATION LINK --- */
    a[data-testid="stPageLink-NavLink"] { background: transparent !important; border: none !important; }
    a[data-testid="stPageLink-NavLink"] p { color: #666; font-family: 'Cinzel', serif; font-size: 0.9rem; transition: color 0.3s; }
    a[data-testid="stPageLink-NavLink"]:hover p { color: var(--nav-gold) !important; text-shadow: 0 0 10px var(--emerald-glow); }

    /* --- THE VOID INPUT (Specific Overrides) --- */
    
    /* 1. Target the Outer Container */
    div[data-baseweb="input"] {
        background-color: #000000 !important; /* PITCH BLACK */
        border: 1px solid #333 !important;
        border-radius: 0px !important;
        padding: 10px;
    }

    /* 2. Target the Inner 'Base Input' */
    div[data-baseweb="base-input"] {
        background-color: transparent !important;
        border: none !important;
    }

    /* 3. Target the Text Itself */
    input.st-ai, input.st-ah, input[type="text"] {
        background-color: transparent !important;
        color: #e0e0e0 !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.5rem !important;
        text-align: center !important; 
        font-style: italic;
    }
    
    /* 4. THE GHOST PLACEHOLDER (Hidden until hover) */
    input::placeholder {
        color: transparent !important; /* Invisible by default */
        transition: color 0.5s ease-in-out;
        font-family: 'Cinzel', serif !important;
        font-size: 1rem !important;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Reveal on Hover or Focus */
    div[data-baseweb="input"]:hover input::placeholder {
        color: #444 !important; /* Faint grey on hover */
    }
    div[data-baseweb="base-input"]:focus-within input::placeholder {
        color: #333 !important;
    }

    /* 5. REMOVE "PRESS ENTER" Instructions */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }

    /* 6. The Label (The "Call") */
    label p {
        font-family: 'Cinzel', serif !important;
        font-size: 1.2rem !important;
        color: #888 !important;
        text-align: center !important;
        letter-spacing: 2px !important;
        width: 100%;
        margin-bottom: 10px !important;
    }

    /* Focus Glow */
    div[data-baseweb="input"]:focus-within {
        border-color: var(--emerald-glow) !important;
        box-shadow: 0 0 20px rgba(80, 200, 120, 0.2) !important;
    }

    /* --- BUTTONS --- */
    button[kind="secondaryFormSubmit"] {
        width: 100% !important;
        border-radius: 0px !important;
        background: transparent !important;
        border: 1px solid #444 !important;
        color: #888 !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        letter-spacing: 6px !important;
        font-size: 1.2rem !important;
        height: 70px !important;
        transition: all 0.5s ease !important;
        margin-top: 1rem;
    }
    button[kind="secondaryFormSubmit"]:hover {
        border-color: var(--emerald-bright) !important;
        color: var(--emerald-bright) !important;
        text-shadow: 0 0 15px var(--emerald-glow);
        background: rgba(80, 200, 120, 0.05) !important;
    }
    
    /* Resonance Buttons */
    button[kind="secondary"] {
        background: transparent !important; 
        border: 1px solid #333 !important; 
        color: #555 !important;
        font-family: 'Cinzel', serif !important; 
        font-size: 0.8rem !important;
        border-radius: 0px !important;
    }
    button[kind="secondary"]:hover {
        color: var(--emerald-bright) !important;
        border-color: var(--emerald-dim) !important;
    }

    /* --- CARD STYLING --- */
    .character-card {
        background: #0e0e0e;
        border: 1px solid #222;
        border-top: 4px solid var(--emerald-dim);
        box-shadow: 0 20px 60px rgba(0,0,0,1);
        margin-top: 4rem;
        animation: fadein 1.5s;
    }
    .seam { height: 1px; background: radial-gradient(circle, #444 0%, transparent 90%); margin: 0; border: none; opacity: 0.6; }
    
    .card-header { background: #111; padding: 2rem 1rem; text-align: center; }
    .card-name { font-family: 'Cinzel', serif; font-size: 2.2rem; color: #fff; letter-spacing: 4px; margin-bottom: 0.5rem; }
    .card-class { font-family: 'Cinzel', serif; font-size: 0.9rem; color: var(--emerald-bright); letter-spacing: 3px; text-transform: uppercase; text-shadow: 0 0 10px rgba(102, 255, 153, 0.3); }

    .img-container { position: relative; overflow: hidden; }
    .img-container img { width: 100%; display: block; opacity: 0.9; transition: all 0.5s ease; cursor: zoom-in; }
    .img-container::after { content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 80px; background: linear-gradient(to top, #0e0e0e, transparent); pointer-events: none; }
    .img-container img:hover { opacity: 1; transform: scale(1.02); }

    .visual-caption { background: #080808; padding: 2rem 3rem; font-family: 'Cormorant Garamond', serif; font-style: italic; color: #888; text-align: left; font-size: 1.15rem; line-height: 1.6; }
    .voice-section { padding: 2.5rem 3rem 1.5rem 3rem; background: radial-gradient(circle at 50% 50%, #111 0%, #0e0e0e 100%); text-align: center; }
    .voice-quote { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; color: #d0d0d0; font-style: italic; line-height: 1.4; }
    .voice-quote::before { content: "“"; font-size: 3rem; color: var(--emerald-dim); vertical-align: -1rem; margin-right: 10px; }
    .voice-quote::after { content: "”"; font-size: 3rem; color: var(--emerald-dim); vertical-align: -2rem; margin-left: 10px; }

    .lore-section { padding: 1.5rem 3rem 3rem 3rem; color: #b0b0b0; line-height: 1.7; font-size: 1.2rem; font-family: 'Cormorant Garamond', serif; background: #050505; text-align: left; }
    .lore-label { font-family: 'Cinzel', serif; font-size: 0.8rem; color: #666; letter-spacing: 2px; text-transform: uppercase; display: block; margin-bottom: 10px; text-align: center; opacity: 0.8; }

    @keyframes fadein { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    /* Footer */
    .footer-container { opacity: 0.3; text-align: center; margin-top: 4rem; padding-bottom: 2rem;}
    .rune-span { margin: 0 10px; font-size: 1.2rem; color: #444; cursor: default; }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. CORE LOGIC (Gemini & GSheets)
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

def forge_npc(concept, tone):
    # 1. DEFINE VIBES
    if tone == "Grim & Shadow":
        text_vibe = "Dark fantasy, gritty, morally ambiguous, dangerous tone."
        img_vibe = "photo realistic, dark fantasy, gritty, low key lighting, shadow heavy, ominous"
    elif tone == "Noble & Bright":
        text_vibe = "High fantasy, heroic, hopeful, noble, clean and elegant tone."
        img_vibe = "photo realistic, high fantasy, vibrant, golden hour lighting, majestic, clean, ethereal"
    else: # Mystic & Strange
        text_vibe = "Eldritch, strange, dreamlike, mysterious, folklore-heavy tone."
        img_vibe = "photo realistic, surreal, mist-filled, cinematic, strange colors, folklore aesthetic"

    # 2. GENERATE TEXT
    with st.spinner(f"The Void answers..."):
        try:
            if "GOOGLE_API_KEY" in st.secrets:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            text_model = genai.GenerativeModel('models/gemini-3-pro-preview')
            text_prompt = f"""
            Role: Fantasy DM Creative Archivist.
            Task: Create a vivid, fully realized description in a fantasy style of an NPC based on: "{concept}".
            Rules: Norse-inspired name (EASY to pronounce). {text_vibe}. No Stats.
            Format: JSON with keys: Name, Class, Visual_Desc, Lore, Greeting.
            """
            text_response = text_model.generate_content(text_prompt)
            clean_json = text_response.text.replace("```json", "").replace("```", "").strip()
            char_data = json.loads(clean_json)
        except Exception as e:
            st.error(f"The whisper was lost: {e}")
            return None

    # 3. GENERATE IMAGE
    with st.spinner("Conjuring the form..."):
        try:
            image_model = genai.GenerativeModel('models/gemini-3-pro-image-preview') 
            img_prompt = f"{img_vibe}, {char_data['Visual_Desc']}, Norse aesthetic, 8k, cinematic lighting."
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

    # 4. SAVE
    try:
        gc, auth_success, auth_msg = setup_auth()
        if auth_success:
            sh = gc.open("Masters_Vault_Db")
            worksheet = sh.get_worksheet(0)
            # Simple save: Name, Class, Lore, Greeting, Visual, Image, Time
            row_data = [
                char_data['Name'], 
                char_data['Class'], 
                char_data['Lore'], 
                char_data['Greeting'], 
                char_data['Visual_Desc'], 
                image_url, 
                str(datetime.datetime.now()),
                "", "" # Empty Campaign/Faction
            ]
            worksheet.append_row(row_data)
    except Exception as e:
        st.warning(f"Vault closed (Local mode): {e}")

    char_data['image_url'] = image_url
    return char_data

# -----------------------------------------------------------------------------
# 4. LAYOUT
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO VAULT", use_container_width=False)

st.markdown("<h1>THE NPC FORGE</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Inscribe the soul. Strike the iron.</div>", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
st.sidebar.markdown('<div class="sidebar-header">The Forge</div>', unsafe_allow_html=True)

# --- THE INPUT (Z-PATTERN & CALL/RESPONSE) ---
with st.form("forge_form"):
    
    # 1. The Call (Label)
    # The placeholder acts as the response (hidden until hover/focus)
    user_input = st.text_input(
        label="WHISPER YOUR DESIRES...", 
        placeholder="...and the void shall give it form."
    )
    
    # 2. Layout for Button (Z-Pattern Alignment)
    # We use columns to push the button to the right side
    c_spacer, c_btn = st.columns([2, 1])
    
    with c_btn:
        submitted = st.form_submit_button("STRIKE THE ANVIL")

# --- HANDLING SUBMISSION ---
if submitted and user_input:
    st.session_state.last_concept = user_input
    # CHANGE: DEFAULT IS NOW NOBLE & BRIGHT
    st.session_state.npc_data = forge_npc(user_input, "Noble & Bright") 

# -----------------------------------------------------------------------------
# 5. RESULT & MODIFIERS
# -----------------------------------------------------------------------------
if st.session_state.npc_data:
    data = st.session_state.npc_data
    
    # --- RENDER CARD ---
    card_html = ""
    card_html += f'<div class="character-card">'
    card_html += f'  <div class="card-header">'
    card_html += f'    <div class="card-name">{data["Name"]}</div>'
    card_html += f'    <div class="card-class">{data["Class"]}</div>'
    card_html += f'  </div>'
    card_html += f'  <div class="img-container">'
    card_html += f'    <a href="{data["image_url"]}" target="_blank">'
    card_html += f'      <img src="{data["image_url"]}" title="Click to Expand">'
    card_html += f'    </a>'
    card_html += f'  </div>'
    card_html += f'  <div class="visual-caption">"{data["Visual_Desc"]}"</div>'
    card_html += f'  <hr class="seam">'
    card_html += f'  <div class="voice-section">'
    card_html += f'    <div class="voice-quote">{data["Greeting"]}</div>'
    card_html += f'  </div>'
    card_html += f'  <hr class="seam">'
    card_html += f'  <div class="lore-section">'
    card_html += f'    <span class="lore-label">Archive Record</span>'
    card_html += f'    {data["Lore"]}'
    card_html += f'  </div>'
    card_html += f'</div>'
    st.markdown(card_html, unsafe_allow_html=True)

    # --- RESONANCE MODIFIERS ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("REROLL: GRIM", use_container_width=True, type="secondary"):
            st.session_state.npc_data = forge_npc(st.session_state.last_concept, "Grim & Shadow")
            st.rerun()
            
    with col2:
        if st.button("REROLL: NOBLE", use_container_width=True, type="secondary"):
            st.session_state.npc_data = forge_npc(st.session_state.last_concept, "Noble & Bright")
            st.rerun()
            
    with col3:
        if st.button("REROLL: STRANGE", use_container_width=True, type="secondary"):
            st.session_state.npc_data = forge_npc(st.session_state.last_concept, "Mystic & Strange")
            st.rerun()

# FOOTER
runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)