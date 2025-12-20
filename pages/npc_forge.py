import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from PIL import Image
import io
import gspread
import json
import datetime
import cloudinary
import cloudinary.uploader
import pandas as pd # Included per your requirements list

# --- PAGE CONFIG ---
st.set_page_config(page_title="NPC Forge", page_icon="🛡️", layout="wide")
st.title("🛡️ NPC Forge")
st.caption("The Character Foundry (Gemini 3 Pro)")

# --- 1. AUTHENTICATION & SETUP ---
try:
    # Google Sheets Auth
    if "gcp_service_account" in st.secrets:
        service_account_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/cloud-platform"]
        )
        gc = gspread.authorize(creds)
    else:
        st.error("🚨 Service Account Secrets missing.")
        st.stop()

    # Cloudinary Auth
    if "cloudinary" in st.secrets:
        cloudinary.config(
            cloud_name = st.secrets["cloudinary"]["cloud_name"],
            api_key = st.secrets["cloudinary"]["api_key"],
            api_secret = st.secrets["cloudinary"]["api_secret"],
            secure = True
        )
    else:
        st.error("🚨 Cloudinary Secrets missing.")
        st.stop()

    # Gemini API Auth
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("🚨 Google API Key missing.")
        st.stop()
        
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# --- INTERFACE ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 1. The Concept")
    user_input = st.text_area("Describe the character:", height=150, placeholder="E.g., A paranoid alchemist...")
    summon_btn = st.button("Manifest Character", type="primary", use_container_width=True)

if summon_btn and user_input:
    
    character_data = None
    image_url = "No Image"

    # --- A. GENERATE TEXT (Gemini 3 Pro) ---
    with col2:
        with st.spinner("Weaving the soul (Gemini 3 Pro)..."):
            try:
                # STRICT MODEL SELECTION: Gemini 3 Pro Preview
                text_model = genai.GenerativeModel('models/gemini-3-pro-preview')
                
                text_prompt = f"""
                You are a dark fantasy writer. Create a character based on: "{user_input}".
                Return ONLY a raw JSON object with these keys:
                "Name", "Class", "Lore", "Greeting", "Visual_Desc"
                """
                text_response = text_model.generate_content(text_prompt)
                clean_json = text_response.text.replace("```json", "").replace("```", "").strip()
                character_data = json.loads(clean_json)
                
                st.subheader(f"📜 {character_data['Name']}")
                st.caption(f"Class: {character_data['Class']}")
                st.write(f"**Lore:** {character_data['Lore']}")
                st.info(f"**Greeting:** \"{character_data['Greeting']}\"")
            except Exception as e:
                st.error(f"Lore Generation Failed: {e}")
                st.stop()

    # --- B. GENERATE & UPLOAD IMAGE (Gemini 3 Pro Image) ---
    with col1:
        st.markdown("---")
        with st.spinner("Painting & Archiving..."):
            try:
                # STRICT MODEL SELECTION: Gemini 3 Pro Image
                image_model = genai.GenerativeModel('models/gemini-3-pro-image-preview')
                
                desc = character_data.get("Visual_Desc", user_input)
                image_prompt = f"Dark fantasy character portrait, {desc}, oil painting style, 8k."
                
                img_response = image_model.generate_content(image_prompt)
                
                if img_response.parts:
                    # 1. Get Data
                    img_data = img_response.parts[0].inline_data.data
                    
                    # 2. Upload to Cloudinary
                    upload_result = cloudinary.uploader.upload(io.BytesIO(img_data), folder="masters_vault_npcs")
                    image_url = upload_result.get("secure_url")
                    
                    # 3. Show
                    st.image(image_url, caption=character_data['Name'], use_container_width=True)
                else:
                    st.warning("Visual manifestation failed.")
            except Exception as e:
                st.error(f"Image Error: {e}")

    # --- C. SAVE TO DB ---
    if character_data:
        try:
            sh = gc.open("Masters_Vault_Db")
            worksheet = sh.get_worksheet(0)
            
            row_data = [
                character_data['Name'],
                character_data['Class'],
                character_data['Lore'],
                character_data['Greeting'],
                character_data['Visual_Desc'],
                image_url,
                str(datetime.datetime.now())
            ]
            worksheet.append_row(row_data)
            st.toast("Saved to Vault!", icon="💾")
        except Exception as sheet_error:
            st.error(f"Database Error: {sheet_error}")