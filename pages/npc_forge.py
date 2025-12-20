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
# 2. THE VISUAL ENGINE (The Furnace & Anvil)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;800&family=Cormorant+Garamond:wght@400;600&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #1c1c1c;
        --stone-dark: #0e0e0e;
        --emerald-glow: #50c878;
        --emerald-dim: #2e5a44;
        --iron-plate: #1a1a1a;
        --furnace-glow: rgba(80, 200, 120, 0.1);
    }

    /* --- BACKGROUND --- */
    .stApp {
        background-color: var(--stone-dark);
        background-image: 
            radial-gradient(circle at 50% 0%, #1f2220 0%, transparent 60%),
            url("https://www.transparenttextures.com/patterns/black-felt.png"); /* Subtle noise texture */
        color: #d0d0d0;
        font-family: 'Lato', sans-serif;
    }

    /* --- NAVIGATION --- */
    a[data-testid="stPageLink-NavLink"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    a[data-testid="stPageLink-NavLink"] p {
        color: #666;
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
    }
    a[data-testid="stPageLink-NavLink"]:hover p { color: var(--emerald-glow); }

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 12px;
        font-size: 3.5rem !important;
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
        margin-bottom: 4rem; 
        border-bottom: 1px solid #333;
        padding-bottom: 2rem;
    }

    /* --- THE IRON ALTAR (Form Container) --- */
    [data-testid="stForm"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
        border: 1px solid #333;
        border-top: 1px solid #555; /* Top highlight */
        border-bottom: 5px solid #000; /* Heavy base */
        border-radius: 6px;
        padding: 3rem 2rem 2rem 2rem;
        box-shadow: 
            0 20px 50px rgba(0,0,0,0.9),
            inset 0 0 60px rgba(0,0,0,0.8); /* Inner depth */
        position: relative;
    }

    /* THE BOLTS (Pseudo-elements) */
    [data-testid="stForm"]::before {
        content: '';
        position: absolute;
        top: 15px; left: 15px;
        width: 10px; height: 10px;
        background: #000;
        border-radius: 50%;
        box-shadow: 0 1px 0 #333;
    }
    [data-testid="stForm"]::after {
        content: '';
        position: absolute;
        top: 15px; right: 15px;
        width: 10px; height: 10px;
        background: #000;
        border-radius: 50%;
        box-shadow: 0 1px 0 #333;
    }

    /* --- THE "MOULD" (Input Field) --- */
    .stTextInput > div > div > input {
        background-color: #050505 !important; 
        border: 1px solid #222 !important;
        border-top: 3px solid #000 !important; /* Deep shadow top */
        border-bottom: 1px solid #333 !important;
        color: #e0e0e0 !important;
        font-family: 'Lato', sans-serif;
        font-size: 1.2rem;
        padding: 1.5rem;
        box-shadow: inset 0 0 20px #000;
        border-radius: 4px;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--emerald-dim) !important;
        background-color: #080a09 !important;
        color: #fff !important;
    }

    .stTextInput input::placeholder {
        color: #444 !important;
        font-style: italic;
        letter-spacing: 1px;
    }
    
    .stTextInput label { display: none; }

    /* --- THE HAMMER (Button) --- */
    /* This targets the button container to ensure full width */
    .stButton {
        width: 100%;
        margin-top: 2rem;
    }

    .stButton > button {
        width: 100%;
        background: radial-gradient(circle at center, #2e3b33 0%, #0e1210 100%);
        color: #888;
        border: 1px solid #2e5a44;
        border-bottom: 4px solid #000;
        padding: 1.5rem;
        font-family: 'Cinzel', serif;
        font-weight: 800;
        letter-spacing: 6px;
        font-size: 1.4rem;
        text-transform: uppercase;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        text-shadow: 0 -1px 0 #000;
        position: relative;
        overflow: hidden;
    }

    /* Hover: The Metal heats up */
    .stButton > button:hover {
        background: radial-gradient(circle at center, #3a5c4a 0%, #15221c 100%);
        color: #fff;
        border-color: var(--emerald-glow);
        text-shadow: 0 0 15px var(--emerald-glow);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(80, 200, 120, 0.1);
    }

    .stButton > button:active {
        transform: translateY(2px);
        border-bottom: 1px solid #000;
        box-shadow: inset 0 0 20px #000;
    }

    /* --- THE ARTIFACT (Result Card) --- */
    .character-card {
        background: #080808;
        border: 1px solid #222;
        padding: 0; /* Image touches edges */
        margin-top: 4rem;
        box-shadow: 0 0 60px rgba(0,0,0,1);
        position: relative;
    }
    
    .card-header {
        background: #0f1210;
        padding: 1.5rem;
        border-bottom: 1px solid #222;
        text-align: center;
    }
    
    .card-name {
        font-family: 'Cinzel', serif;
        font-size: 2rem;
        color: #fff;
        letter-spacing: 3px;
        margin: 0;
        text-shadow: 0 0 10px rgba(80, 200, 120, 0.5);
    }
    
    .card-body {
        padding: 2rem;
    }

    .visual-block {
        background-color: #0c0c0c;
        border-left: 2px solid var(--emerald-dim);
        padding: 1.5rem;
        font-style: italic;
        color: #ccc;
        margin-bottom: 2rem;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
    }
    
    /* --- FOOTER RUNES (Consistent) --- */
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
# 3. LOGIC
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
st.markdown("<div class='subtext'>The anvil awaits your hammer. Strike true.</div>", unsafe_allow_html=True)

# THE IRON ALTAR
with st.form("forge_form"):
    st.markdown("<p style='font-family: Cinzel; color: #555; letter-spacing: 2px; font-size: 0.8rem; text-align: center; margin-bottom: 10px;'>INSCRIPTION</p>", unsafe_allow_html=True)
    
    user_input = st.text_input("Concept", placeholder="Describe the soul you wish to forge...")
    
    # The massive button
    submitted = st.form_submit_button("STRIKE THE ANVIL")

# -----------------------------------------------------------------------------
# 5. GENERATION
# -----------------------------------------------------------------------------
if submitted and user_input:
    
    # 1. Text
    with st.spinner("The hammers are ringing..."):
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

    # 2. Image
    with st.spinner("Quenching the steel..."):
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

    # 3. Save
    try:
        sh = gc.open("Masters_Vault_Db")
        worksheet = sh.get_worksheet(0)
        row_data = [char_data['Name'], char_data['Class'], char_data['Lore'], char_data['Greeting'], char_data['Visual_Desc'], image_url, str(datetime.datetime.now())]
        worksheet.append_row(row_data)
        st.toast("Entity Forged.", icon="⚒️")
    except Exception as e:
        st.error(f"Save Failed: {e}")

    # 4. Render
    st.markdown(f"""
    <div class="character-card">
        <div class="card-header">
            <div class="card-name">{char_data['Name']}</div>
            <div style="color: #50c878; font-family: Cinzel; font-size: 0.9rem; margin-top: 5px;">{char_data['Class']}</div>
        </div>
        
        <img src="{image_url}" style="width: 100%; display: block; opacity: 1.0; border-bottom: 1px solid #222;">
        
        <div class="card-body">
            <div class="visual-block">"{char_data['Visual_Desc']}"</div>
            
            <div style="color: #aaa; line-height: 1.6; font-size: 0.95rem;">
                <strong style="color: #50c878; font-family: Cinzel;">GREETING:</strong> <span style="color: #ddd;">"{char_data['Greeting']}"</span><br><br>
                <strong style="color: #50c878; font-family: Cinzel;">LORE:</strong><br>
                {char_data['Lore']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
runes = ["ᚦ", "ᚱ", "ᛁ", "ᛉ", "ᛉ", "ᚨ", "ᚱ"]
rune_html = "<div class='footer-container'>"
for i, rune in enumerate(runes):
    delay = i * 0.3
    rune_html += f"<span class='rune-span' style='animation-delay: {delay}s'>{rune}</span>"
rune_html += "</div>"
st.markdown(rune_html, unsafe_allow_html=True)