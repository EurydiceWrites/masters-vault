import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import time
import json  # Creates structure for the data
import cloudinary
import cloudinary.uploader
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(page_title="NPC Forge", page_icon="🛡️", layout="wide")

# Custom UI Styling (Dark Mode friendly)
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stButton>button { 
        background-color: #50C878; 
        color: #0E1117; 
        border: none; 
        font-weight: bold; 
        width: 100%;
    }
    .stTextInput>div>div>input {
        background-color: #262730;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CONNECTING THE TOOLS ---
# A. API Keys
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    cloudinary.config(cloudinary_url=st.secrets["CLOUDINARY_URL"])
except Exception as e:
    st.error(f"⚠️ Key Error: {e}")

# B. Google Sheets Connection
# REPLACE THIS WITH YOUR SHEET ID
SHEET_ID = "1mhKTWKjRfYIKEV9uyAIkHy6HYdqbBxsCsiGHODs1C0w"

try:
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', SCOPE)
    client = gspread.authorize(creds)
except Exception as e:
    st.error(f"⚠️ Sheets Connection Error: {e}")


# --- 3. THE BRAIN (Functions) ---

def get_npc_data(concept):
    """
    Asks Gemini for a character profile. 
    ADJUSTMENT: Enforces Norse Names, but allows broad Dark Fantasy concepts.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are a creative assistant for a Dark Fantasy RPG campaign.
    The setting is gritty, mysterious, and magical. It is NOT strictly historical Viking.
    
    Create a detailed NPC based on this concept: "{concept}"
    
    CRITICAL RULES:
    1. The NAME must be Norse/Scandinavian (e.g., Astrid, Bjorn, Thorfinn), regardless of the race/class.
    2. The character design should be Dark Fantasy (gritty, realistic, serious).
    
    RETURN ONLY A VALID JSON OBJECT with these exact keys:
    {{
        "Name": "Norse Name here",
        "Class": "Class or Role",
        "Lore": "3 sentences of dramatic, dark backstory",
        "Greeting": "A short, in-character introduction",
        "Visual": "A detailed visual description for an art generator (appearance, clothing, lighting)"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean the text to ensure it's pure JSON
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        # Fallback if the Brain gets confused
        return {
            "Name": "Ragnar the Unknown",
            "Class": "Wanderer",
            "Lore": f"The mists of Niflheim obscure this fate. (Error: {e})",
            "Greeting": "...",
            "Visual": "A figure shrouded in shadow"
        }

def get_npc_image(visual_desc):
    """Generates the image using Gemini Pro Vision."""
    model = genai.GenerativeModel('models/gemini-3-pro-image-preview')
    
    # ADJUSTMENT: Removed "Norse art" to avoid excessive viking helmets.
    # Added "Dark Fantasy" and "Cinematic" for that gritty campaign feel.
    style_prompt = f"{visual_desc}, dark fantasy art, photorealistic, cinematic lighting, 8k resolution, highly detailed, oil painting style"
    
    response = model.generate_content(style_prompt, generation_config={"candidate_count": 1})
    return Image.open(io.BytesIO(response.candidates[0].content.parts[0].inline_data.data))

def upload_and_save(image_obj, data):
    """Uploads to Cloudinary AND saves to Sheets."""
    
    # 1. Upload to Cloudinary
    img_byte_arr = io.BytesIO()
    image_obj.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    public_id = f"npc_{data['Name'].replace(' ', '_')}_{int(time.time())}"
    upload_resp = cloudinary.uploader.upload(img_byte_arr, public_id=public_id)
    image_url = upload_resp['secure_url']
    
    # 2. Save to Sheets
    sheet = client.open_by_key(SHEET_ID).sheet1
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    row = [
        data['Name'], 
        data['Class'], 
        data['Lore'], 
        data['Greeting'], 
        data['Visual'], 
        image_url, 
        timestamp
    ]
    sheet.append_row(row)
    return image_url

# --- 4. THE UI (The Interface) ---
st.title("🛡️ NPC Forge")
st.caption("Summon Dark Fantasy characters with Norse names.")

# A. Input Section
with st.container():
    c1, c2 = st.columns([3, 1])
    with c1:
        concept = st.text_input("Who shall we summon?", placeholder="E.g., A paranoid alchemist with blue skin...")
    with c2:
        st.write("") # Spacer
        st.write("") # Spacer
        manifest_btn = st.button("Manifest NPC", type="primary")

# B. Results Section
if manifest_btn and concept:
    with st.spinner("Weaving fate..."):
        try:
            # Step 1: Generate Data
            npc_data = get_npc_data(concept)
            
            # Step 2: Generate Image
            npc_image = get_npc_image(npc_data['Visual'])
            
            # Step 3: Save Everything
            final_link = upload_and_save(npc_image, npc_data)
            
            # Success Message
            st.toast(f"{npc_data['Name']} has been saved to the Vault!", icon="✅")
            
            # Display Result
            st.divider()
            col_img, col_text = st.columns([1, 2])
            
            with col_img:
                st.image(npc_image, use_container_width=True)
                st.caption(f"Stored at: Cloudinary")
            
            with col_text:
                st.subheader(f"{npc_data['Name']}")
                st.markdown(f"**Class:** `{npc_data['Class']}`")
                st.markdown(f"**Greeting:** *\"{npc_data['Greeting']}\"*")
                st.info(npc_data['Lore'])

        except Exception as e:
            st.error(f"Something went wrong in the forge: {e}")