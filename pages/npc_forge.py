import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account

# --- PAGE CONFIG ---
st.set_page_config(page_title="NPC Forge", page_icon="🛡️")
st.title("🛡️ NPC Forge")
st.write("Summon Dark Fantasy characters with Norse names.")

# --- AUTHENTICATION ---
try:
    if "gcp_service_account" in st.secrets:
        # Cloud Mode
        service_account_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(service_account_info)
    else:
        # Local Mode
        creds = service_account.Credentials.from_service_account_file("service_account.json")
except Exception as e:
    st.error(f"🚨 Auth Error: {e}")
    st.stop()

# --- AI CONFIGURATION ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing GOOGLE_API_KEY in secrets.")
    st.stop()

# --- THE APP ---
user_input = st.text_input("Who shall we summon?", placeholder="E.g., A paranoid alchemist with blue skin...")

if st.button("Manifest NPC"):
    if not user_input:
        st.warning("Please describe the entity you wish to summon.")
    else:
        with st.spinner("Weaving fate..."):
            try:
                # 1. The Prompt
                prompt = f"""
                You are a creative writer for a dark fantasy RPG. 
                Generate a character based on this concept: "{user_input}".
                
                REQUIREMENTS:
                - Name: Must be Norse-inspired.
                - Tone: Dark, gritty, mysterious.
                
                OUTPUT FORMAT:
                **Name:** [Name]
                **Class:** [Class]
                **Race:** [Race]
                
                **Appearance:**
                [Visual description]
                
                **Backstory:**
                [A short, compelling history]
                
                **Secret:**
                [One hidden fact or weakness]
                """

                # 2. The Model (UPDATED TO GEMINI 3 PRO PREVIEW)
                model = genai.GenerativeModel('models/gemini-3-pro-preview')
                response = model.generate_content(prompt)
                
                # 3. Output
                st.markdown("### 📜 The Scroll Unfurls")
                st.markdown(response.text)
                st.success("Summoning Complete.")

            except Exception as e:
                st.error(f"The ritual failed: {e}")