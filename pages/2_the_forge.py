import streamlit as st
from google import genai
from google.oauth2 import service_account
from google.genai import types
import gspread
import json
import datetime
import cloudinary
import cloudinary.uploader
import base64
import os

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Well of Souls", layout="centered", page_icon="⚒️")

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
    div[data-baseweb="input"] {
        background-color: #000000 !important;
        border: 1px solid #333 !important;
        border-radius: 0px !important;
        padding: 10px;
    }
    div[data-baseweb="base-input"] {
        background-color: transparent !important;
        border: none !important;
    }
    input.st-ai, input.st-ah, input[type="text"] {
        background-color: transparent !important;
        color: #e0e0e0 !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.5rem !important;
        text-align: center !important; 
        font-style: italic;
    }
    input::placeholder {
        color: transparent !important;
        transition: color 0.5s ease-in-out;
        font-family: 'Cinzel', serif !important;
        font-size: 1rem !important;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    div[data-baseweb="input"]:hover input::placeholder {
        color: #444 !important;
    }
    div[data-baseweb="base-input"]:focus-within input::placeholder {
        color: #333 !important;
    }
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    label p {
        font-family: 'Cinzel', serif !important;
        font-size: 1.2rem !important;
        color: #888 !important;
        text-align: center !important;
        letter-spacing: 2px !important;
        width: 100%;
        margin-bottom: 10px !important;
    }
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

    .footer-container { opacity: 0.3; text-align: center; margin-top: 4rem; padding-bottom: 2rem;}
    .rune-span { margin: 0 10px; font-size: 1.2rem; color: #444; cursor: default; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. CORE LOGIC
# -----------------------------------------------------------------------------
def setup_auth():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=SCOPES
        )
    else:
        creds = service_account.Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
        
    gc = gspread.authorize(creds)
    sh = gc.open("Masters_Vault_Db")
    
    # Return JUST the worksheet to make saving simple
    return sh.get_worksheet(0)

def forge_npc(concept, tone):
    # 1. DEFINE VIBES
    if tone == "Grim & Shadow":
        text_vibe = "may contain themes including: Dark fantasy, gritty, morally ambiguous, dangerous tone. Focus on survival, visible scars, and heavily weathered gear."
        img_vibe = "ultra-realistic cinematic movie still, dark fantasy, gritty, low key lighting, heavy shadows, ominous, battle-worn, stark realism, deeply weathered"
    elif tone == "Noble & Bright":
        text_vibe = "may contain themes including: High fantasy, heroic, hopeful, noble, clean and elegant tone. Focus on grand ideals and pristine appearance."
        img_vibe = "ultra-realistic cinematic movie still, high fantasy, vibrant, golden hour lighting, majestic, clean, ethereal, sharp focus, majestic"
    else:
        text_vibe = "may contain themes including: eldritch, strange, dreamlike, mysterious, folklore-heavy tone. Focus on unsettling but beautiful, unnatural details."
        img_vibe = "ultra-realistic cinematic movie still, surreal, mist-filled, strange colors, folklore aesthetic, hauntingly beautiful, eerie cinematic lighting"

    # 2. GENERATE TEXT
    with st.spinner(f"The Void answers..."):
        client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

        text_prompt = f"""
        Role: Master Worldbuilder and Grounded Fantasy DM.
        Task: Create a vivid, highly believable, and realistic NPC based on: "{concept}".
        Rules: 
        1. Norse-inspired name (EASY to pronounce). 
        2. Tone: {text_vibe}
        3. Contextual realism: The setting is high-fantasy. Apply realism based on the subject's nature. Avoid cartoonish high-fantasy tropes. 
        4. MANDATORY COMPLIANCE: The Visual_Desc MUST be PG-13. 
        5. No Stats.
        Format: JSON with keys: Name, Class, Visual_Desc, Lore, Greeting.
        """
        
        text_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=text_prompt
        )
        
        raw_text = text_response.text.replace('```json', '').replace('```', '').strip()
        parsed_json = json.loads(raw_text)
        
        if isinstance(parsed_json, list):
            char_data = parsed_json[0]
        else:
            char_data = parsed_json

    # 3. GENERATE IMAGE
    with st.spinner("Conjuring the Form..."):
        image_prompt = f"An ultra-realistic, cinematic 8K movie still of a {char_data.get('Class')}. {char_data.get('Visual_Desc')}. {img_vibe}"
        
        image_response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=image_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="3:4",
            )
        )
        
        generated_image = image_response.generated_images[0].image.image_bytes
        b64_encoded = base64.b64encode(generated_image).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{b64_encoded}"
        
        # ---> UPLOAD TO CLOUDINARY <---
        try:
            # Use the exact format you have in your Streamlit secrets
            cloudinary.config(
                cloud_name = st.secrets["cloudinary"]["cloud_name"],
                api_key = st.secrets["cloudinary"]["api_key"],
                api_secret = st.secrets["cloudinary"]["api_secret"],
                secure = True
            )
            upload_result = cloudinary.uploader.upload(data_uri, folder="Well_of_Souls")
            char_data["image_url"] = upload_result["secure_url"]
        except Exception as e:
            st.warning(f"Cloudinary Error: {e}")
            # CRITICAL FIX: Do NOT save the raw data_uri to the spreadsheet. 
            char_data["image_url"] = "Image Upload Failed - See Cloudinary"

        # ---> 4. SAVE TO GOOGLE SHEETS <---
        try:
            # We now just grab the worksheet directly. No unpacking. No messages.
            worksheet = setup_auth()
            
            current_time = str(datetime.datetime.now())
            row_to_save = [
                char_data.get("Name", "Unknown"), 
                char_data.get("Class", "Unknown"),
                char_data.get("Lore", ""),         
                char_data.get("Greeting", ""),     
                char_data.get("Visual_Desc", ""),  
                char_data.get("image_url", ""),    
                current_time                       
            ]
            
            worksheet.insert_row(row_to_save, 2)
            st.session_state.db_status = f"Success! {char_data.get('Name')} saved to Vault."
        except Exception as e:
            st.session_state.db_status = f"Vault Exception: {str(e)}"

        return char_data

# -----------------------------------------------------------------------------
# 4. LAYOUT
# -----------------------------------------------------------------------------
st.page_link("1_the_vault.py", label="< RETURN TO VAULT", use_container_width=False)

st.markdown("<h1>The WELL OF SOULS</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Conjure a form and inscribe the soul... </div>", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-header">The Well of Souls</div>', unsafe_allow_html=True)

with st.form("forge_form"):
    user_input = st.text_input(
        label="WHISPER YOUR DESIRES...", 
        placeholder="...and the void shall give it form."
    )
    
    c_vibe, c_btn = st.columns([2, 1])
 
    with c_vibe:
        st.markdown("""
            <div style="font-family: 'Cinzel', serif; font-size: 14px; color: #a0a0a0; margin-bottom: 5px; display: block; text-transform: uppercase; letter-spacing: 1px;">
                Choose a Resonance
            </div>
        """, unsafe_allow_html=True)
        
        selected_vibe = st.selectbox(
            "CHOOSE A RESONANCE", 
            ["Noble & Bright", "Grim & Shadow", "Mystic & Strange"],
            label_visibility="collapsed"
        )
    with c_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("INSCRIBE THE SOUL.")

if submitted and user_input:
    st.session_state.last_concept = user_input
    st.session_state.npc_data = forge_npc(user_input, selected_vibe) 
    st.rerun()

# -----------------------------------------------------------------------------
# 5. RESULT & MODIFIERS
# -----------------------------------------------------------------------------
if st.session_state.npc_data:
    data = st.session_state.npc_data
    if "db_status" in st.session_state:
        # If success, show green. If error, show yellow.
        if "Success!" in st.session_state.db_status:
            st.success(st.session_state.db_status)
        else:
            st.warning(st.session_state.db_status)
    
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

runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    rune_html += f"<span class='rune-span'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)