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
# 2. THE VISUAL ENGINE (The Iron Altar)
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
        --iron-gradient: linear-gradient(180deg, #444 0%, #222 50%, #111 100%);
        --text-main: #d0d0d0;
        --text-muted: #666; /* Darker placeholder */
    }

    /* --- BACKGROUND --- */
    .stApp {
        background-color: var(--stone-dark);
        background-image: radial-gradient(circle at 50% 10%, #1f2220 0%, #000 100%);
        color: var(--text-main);
        font-family: 'Lato', sans-serif;
    }

    /* --- NAVIGATION BACK LINK --- */
    a[data-testid="stPageLink-NavLink"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    
    a[data-testid="stPageLink-NavLink"] p {
        color: var(--text-muted);
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
        transition: color 0.3s;
    }
    
    a[data-testid="stPageLink-NavLink"]:hover p {
        color: var(--emerald-glow);
    }

    /* --- HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 10px;
        font-size: 3rem !important;
        color: var(--emerald-glow) !important;
        text-shadow: 0 0 20px rgba(80, 200, 120, 0.4);
        text-align: center;
        margin-top: -20px;
        margin-bottom: 0.5rem !important;
    }

    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        font-style: italic;
        color: var(--text-muted);
        letter-spacing: 2px;
        margin-bottom: 3rem; 
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 2rem;
    }

    /* --- THE ALTAR (The Form Container) --- */
    /* This grounds the input field so it's not floating */
    [data-testid="stForm"] {
        background-color: #111;
        border: 1px solid #333;
        border-top: 4px solid #444; /* Highlight on top edge */
        border-radius: 4px;
        padding: 2rem;
        box-shadow: 
            0 20px 50px rgba(0,0,0,0.8), /* Drop shadow */
            inset 0 0 100px rgba(0,0,0,0.8); /* Inner shadow for depth */
        position: relative;
    }
    
    /* Decorative Bolts on the Altar */
    [data-testid="stForm"]::before, [data-testid="stForm"]::after {
        content: '+';
        position: absolute;
        top: 10px;
        color: #333;
        font-family: 'Cinzel', serif;
    }
    [data-testid="stForm"]::before { left: 15px; }
    [data-testid="stForm"]::after { right: 15px; }

    /* --- INPUT AREA (Embedded in the Altar) --- */
    .stTextInput > div > div > input {
        background-color: #050505 !important; 
        border: 1px solid #222 !important;
        border-bottom: 1px solid #333 !important;
        color: #e0e0e0 !important;
        font-family: 'Lato', sans-serif;
        font-size: 1.1rem;
        padding: 1rem;
        box-shadow: inset 0 5px 10px rgba(0,0,0,0.9); /* Recessed look */
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--emerald-dim) !important;
        color: #fff !important;
    }

    /* DIM THE PLACEHOLDER TEXT */
    .stTextInput input::placeholder {
        color: #444 !important;
        font-style: italic;
    }
    
    .stTextInput label {
        display: none;
    }

    /* --- THE ANVIL BUTTON --- */
    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }

    .stButton > button {
        width: 100%;
        max-width: 300px;
        height: 80px; /* Tall button */
        background: var(--iron-gradient);
        color: #aaa;
        border: 1px solid #333;
        border-bottom: 6px solid #111; /* Thickness */
        font-family: 'Cinzel', serif;
        font-weight: 900;
        letter-spacing: 4px;
        font-size: 1.5rem;
        text-transform: uppercase;
        transition: all 0.1s ease;
        position: relative;
        
        /* TRAPEZOID SHAPE (The Striking Plate) */
        clip-path: polygon(
            10% 0, 90% 0,   /* Narrower top */
            100% 100%, 0% 100% /* Wider bottom base */
        );
        
        text-shadow: 0 -1px 0 #000;
    }

    .stButton > button:hover {
        background: linear-gradient(180deg, #555 0%, #333 100%);
        color: var(--emerald-glow);
        text-shadow: 0 0 10px rgba(80, 200, 120, 0.8);
        border-bottom: 6px solid #111;
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(4px); /* Heavy impact */
        border-bottom: 2px solid #111;
        background: #222;
    }

    /* --- THE RESULT CARD --- */
    .character-card {
        background: linear-gradient(145deg, #111, #0a0a0a);
        border: 1px solid #222;
        border-top: 3px solid var(--emerald-dim);
        padding: 2.5rem;
        margin-top: 4rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
        position: relative;
    }

    .card-name {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        color: #fff;
        text-align: center;
        border-bottom: 1px solid #222;
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
        letter-spacing: 3px;
        text-shadow: 0 0 10px rgba(80, 200, 120, 0.4);
    }

    .visual-block {
        background-color: #080808;
        border-left: 2px solid var(--emerald-dim);
        padding: 1.5rem;
        font-style: italic;
        color: #bbb;
        margin: 2rem 0;
        line-height: 1.6;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
    }
    
    .lore-section {
        margin-top: 2rem;
        border-top: 1px solid #222;
        padding-top: 1.5rem;
        color: #888;
        font-size: 0.95rem;
        line-height: 1.7;
    }

    /* --- FOOTER RUNES (Sequential Glow) --- */
    .footer-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 5rem;
        position: relative;
        z-index: 100;
    }

    .rune-span {
        font-size: 1.5rem;
        color: var(--emerald-dim);
        opacity: 0.3;
        user-select: none;
        cursor: default;
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
# 4. MAIN LAYOUT
# -----------------------------------------------------------------------------

# Back Navigation
st.page_link("home.py", label="< RETURN TO VAULT", use_container_width=False)

# Header
st.markdown("<h1>THE NPC FORGE</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Inscribe the core concept to manifest a soul.</div>", unsafe_allow_html=True)

# THE IRON ALTAR (Form)
with st.form("forge_form"):
    st.markdown("<p style='font-family: Cinzel; color: #50c878; letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 5px; text-align: center; opacity: 0.7;'>CORE CONCEPT INSCRIPTION</p>", unsafe_allow_html=True)
    
    # Text input with darker placeholder styling
    user_input = st.text_input("Concept", placeholder="e.g. A weary executioner who collects butterflies...")
    
    # The Anvil Button
    submitted = st.form_submit_button("FORGE")

# -----------------------------------------------------------------------------
# 5. GENERATION & DISPLAY
# -----------------------------------------------------------------------------
if submitted and user_input:
    
    # 1. Text Gen
    with st.spinner("Striking the anvil..."):
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

    # 2. Image Gen
    with st.spinner("Cooling the steel..."):
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
        <div class="card-name">{char_data['Name']}</div>
        <div style="border: 1px solid #333; padding: 5px; background: #000;">
            <img src="{image_url}" style="width: 100%; display: block; opacity: 1.0;">
        </div>
        <div class="visual-block">"{char_data['Visual_Desc']}"</div>
        <div class="lore-section">
            <strong style="color: #50c878; font-family: Cinzel;">CLASS:</strong> <span style="color: #ccc;">{char_data['Class']}</span><br><br>
            <strong style="color: #50c878; font-family: Cinzel;">GREETING:</strong> <span style="color: #ccc;">"{char_data['Greeting']}"</span><br><br>
            <strong style="color: #50c878; font-family: Cinzel;">LORE:</strong><br>
            {char_data['Lore']}
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