import streamlit as st
import random
from google.oauth2 import service_account
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="NPC Forge", page_icon="🛡️")

st.title("🛡️ NPC Forge")
st.write("Summon Dark Fantasy characters with Norse names.")

# --- AUTHENTICATION (The Fix) ---
try:
    # Check if we are on the Cloud (Secrets exist)
    if "gcp_service_account" in st.secrets:
        service_account_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(service_account_info)
    # If not, fall back to local file (Computer mode)
    else:
        creds = service_account.Credentials.from_service_account_file("service_account.json")
except Exception as e:
    st.error(f"🚨 Authentication Error: {e}")
    st.stop()

# --- AI SETUP ---
# Grab the API Key from secrets
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# --- THE APP LOGIC ---
user_input = st.text_input("Who shall we summon?", placeholder="E.g., A paranoid alchemist with blue skin...")

if st.button("Manifest NPC"):
    if not user_input:
        st.warning("Please describe the entity you wish to summon.")
    else:
        with st.spinner("Weaving fate..."):
            try:
                # 1. Create the Prompt
                prompt = f"""
                Generate a dark fantasy NPC based on this description: "{user_input}".
                
                The NPC must have a Norse-inspired name.
                Provide the output in this specific format:
                
                **Name:** [Name]
                **Class:** [Class]
                **Race:** [Race]
                
                **Appearance:**
                [2-3 sentences describing them visually]
                
                **Backstory:**
                [Short paragraph about their dark past]
                
                **Secret:**
                [One dark secret they are hiding]
                """

                # 2. Call the AI
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                
                # 3. Show the Result
                st.markdown("### 📜 The Scroll Unfurls")
                st.markdown(response.text)
                
                st.success("Summoning Complete.")

            except Exception as e:
                st.error(f"The ritual failed: {e}")