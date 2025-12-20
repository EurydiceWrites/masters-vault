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
# 1. CONFIGURATION & CSS (The Visual Engine)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Master's Vault",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def inject_custom_css():
    st.markdown("""
    <style>
        /* --- FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Lato:wght@300;400;700&display=swap');

        /* --- GLOBAL APP CONTAINER (The Void) --- */
        .stApp {
            background-color: #050505;
            background-image: radial-gradient(circle at 50% 0%, #111e17 0%, #050505 70%);
            color: #dcdcdc;
            font-family: 'Lato', sans-serif;
        }

        /* --- TYPOGRAPHY --- */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Cinzel', serif;
            color: #50c878; /* Emerald Green */
            text-shadow: 0 0 10px rgba(80, 200, 120, 0.3);
            font-weight: 700;
        }
        
        /* --- INPUT FIELDS (Obsidian Tablets) --- */
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea {
            background-color: #0a0a0a; 
            color: #50c878;
            border: 1px solid #1f3a2d;
            border-radius: 4px;
            font-family: 'Lato', sans-serif;
            box-shadow: inset 0 0 10px #000;
        }
        .stTextInput > div > div > input:focus, 
        .stTextArea > div > div > textarea:focus {
            border-color: #50c878;
            box-shadow: 0 0 15px rgba(80, 200, 120, 0.2);
        }

        /* --- BUTTONS (The Gems/Runes) --- */
        .stButton > button {
            width: 100%;
            background: linear-gradient(145deg, #0f241a, #050505);
            color: #50c878;
            border: 1px solid #1f3a2d;
            font-family: 'Cinzel', serif;
            font-weight: 700;
            letter-spacing: 2px;
            padding: 0.75rem 1rem;
            text-transform: uppercase;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.5);
        }
        .stButton > button:hover {
            color: #fff;
            border-color: #50c878;
            box-shadow: 0 0 20px rgba(80, 200, 120, 0.4);
            text-shadow: 0 0 8px #50c878;
        }

        /* --- THE CHARACTER SHEET CARD --- */
        .char-sheet {
            background: rgba(10, 10, 10, 0.9);
            border: 1px solid #1f3a2d;
            padding: 2rem;
            border-radius: 2px;
            box-shadow: 0 0 30px rgba(0,0,0,0.8);
            margin-top: 2rem;
        }
        
        /* Cinematic Image Border */
        .cinematic-frame {
            border: 2px solid #3d2b1f; /* Dark Bronze/Iron */
            border-image: linear-gradient(to bottom, #50c878, #0f241a, #50c878) 1;
            padding: 5px;
            background: #000;
            box-shadow: 0 0 15px rgba(80, 200, 120, 0.1);
            margin-bottom: 1.5rem;
        }
        .cinematic-frame img {
            display: block; width: 100%; height: auto;
            filter: contrast(1.1) saturate(0.9);
        }

        /* Visual Description Highlight Box */
        .visual-desc-box {
            background-color: #0f1612;
            border-left: 3px solid #50c878;
            padding: 1rem;
            margin: 1rem 0;
            color: #e0e0e0;
            font-style: italic;
            font-family: 'Lato', sans-serif;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #080808;
            border-right: 1px solid #1f3a2d;
        }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. THE LOGIC (Authentication & Functions)
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
# 3. MAIN APP
# -----------------------------------------------------------------------------
def main():
    inject_custom_css()
    gc, auth_success, auth_msg = setup_auth()

    if not auth_success:
        st.error(f"System Failure: {auth_msg}")
        st.stop()

    # --- SIDEBAR NAV ---
    with st.sidebar:
        st.header("THE NEXUS")
        mode = st.radio("Select Module", ["NPC Forge", "Art Studio", "The Vault"])
        st.markdown("---")
        st.caption("v2.4.0 // STABLE")

    # --- HEADER ---
    st.markdown("<h1>THE MASTER'S VAULT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-family: Cinzel;'>SYSTEM ONLINE // CONNECTED TO THE VOID</p>", unsafe_allow_html=True)
    st.markdown("---")

    # --- MODE: NPC FORGE ---
    if mode == "NPC Forge":
        st.markdown("## ⚒️ The NPC Forge")
        
        # Input Section
        with st.container():
            col1, col2 = st.columns([2, 1])
            with col1:
                user_input = st.text_area("Input Core Concept", height=100, placeholder="E.g., A weary Norse shield-maiden who runs a tavern in the underworld...")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                ignite_btn = st.button("IGNITE FORGE", type="primary")

        if ignite_btn and user_input:
            
            # 1. Text Gen
            with st.spinner("Forging soul and story..."):
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

            # 2. Image Gen
            with st.spinner("Manifesting visual form..."):
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

            # 3. Save to DB
            try:
                sh = gc.open("Masters_Vault_Db")
                worksheet = sh.get_worksheet(0)
                row_data = [char_data['Name'], char_data['Class'], char_data['Lore'], char_data['Greeting'], char_data['Visual_Desc'], image_url, str(datetime.datetime.now())]
                worksheet.append_row(row_data)
                st.toast("Character Saved to Vault", icon="💾")
            except Exception as e:
                st.error(f"Save Failed: {e}")

            # 4. Render The Cinematic Card (Using the new HTML Design)
            st.markdown("---")
            html_content = f"""
            <div class="char-sheet">
                <h2 style="margin-top: 0; color: #50c878; font-size: 2.5rem; text-align: center;">{char_data['Name']}</h2>
                <p style="text-align: center; color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem;">{char_data['Class']}</p>
                
                <div class="cinematic-frame">
                    <img src="{image_url}" alt="Character Portrait">
                </div>
                
                <div class="visual-desc-box">
                    <strong>👁️ SIGHT:</strong> {char_data['Visual_Desc']}
                </div>
                
                <div style="margin-top: 1.5rem;">
                    <p><strong style="color: #50c878;">🗣️ Greeting:</strong> "{char_data['Greeting']}"</p>
                    <hr style="border-color: #1f3a2d; opacity: 0.5;">
                    <p style="font-size: 0.95rem; color: #aaa;"><strong>📜 Lore:</strong> {char_data['Lore']}</p>
                </div>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)

    # --- MODE: OTHER ---
    elif mode == "Art Studio":
        st.markdown("## 🎨 Art Studio")
        st.info("Module Offline: Recalibrating Neural Runes.")
        
    elif mode == "The Vault":
        st.markdown("## 🔒 The Vault")
        st.text("Accessing secured memories...")

if __name__ == "__main__":
    main()