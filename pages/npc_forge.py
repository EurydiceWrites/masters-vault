import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from PIL import Image
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="NPC Forge", page_icon="🛡️", layout="wide")

st.title("🛡️ NPC Forge")
st.caption("The Character Foundry")

# --- AUTHENTICATION ---
try:
    if "gcp_service_account" in st.secrets:
        service_account_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(service_account_info)
    else:
        creds = service_account.Credentials.from_service_account_file("service_account.json")
except Exception as e:
    st.error(f"🚨 Auth Error: {e}")
    st.stop()

# --- AI CONFIGURATION ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing GOOGLE_API_KEY")
    st.stop()

# --- INTERFACE ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 1. The Concept")
    user_input = st.text_area("Describe the character:", height=150, placeholder="E.g., A paranoid alchemist with blue skin and a vest made of vials...")
    summon_btn = st.button("Manifest Character", type="primary", use_container_width=True)

if summon_btn and user_input:
    # --- 2. GENERATE TEXT (LORE) ---
    with col2:
        with st.spinner("Writing the saga..."):
            try:
                # Use the SMART model for text
                text_model = genai.GenerativeModel('models/gemini-3-pro-preview')
                
                text_prompt = f"""
                You are a dark fantasy writer. Create a character based on: "{user_input}".
                
                REQUIREMENTS:
                - Name: Norse-inspired.
                - Tone: Dark, fantasy.
                
                OUTPUT FORMAT:
                **Name:** [Name]
                **Class:** [Class]
                **Race:** [Race]
                
                **Appearance:** [Visual description]
                **Backstory:** [Short history]
                **Secret:** [Dark secret]
                """
                
                text_response = text_model.generate_content(text_prompt)
                
                st.subheader("📜 The Scroll")
                st.markdown(text_response.text)
                
            except Exception as e:
                st.error(f"Lore generation failed: {e}")

    # --- 3. GENERATE IMAGE (PORTRAIT) ---
    with col1:
        st.markdown("---")
        with st.spinner("Painting the portrait..."):
            try:
                # Use the ART model for the visual
                image_model = genai.GenerativeModel('models/gemini-3-pro-image-preview')
                
                # We enforce "Character Portrait" in the prompt so it doesn't make a landscape
                image_prompt = f"Dark fantasy photo realistic image, {user_input}, detailed face, upper body, photo realistic, suitable background, 8k."
                
                img_response = image_model.generate_content(image_prompt)
                
                if img_response.parts:
                    img_data = img_response.parts[0].inline_data.data
                    image = Image.open(io.BytesIO(img_data))
                    st.image(image, caption="The Manifestation", use_container_width=True)
                else:
                    st.warning("The spirit refused to take form.")
                    
            except Exception as e:
                st.error(f"Portrait generation failed: {e}")