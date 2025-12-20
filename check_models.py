import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Model Checker", page_icon="🕵️‍♀️")
st.title("🕵️‍♀️ The Royal Model Roll Call")

# --- 1. Connect to the Vault ---
try:
    # Grab the key securely
    google_key = st.secrets["GOOGLE_API_KEY"]
    # Configure Google with the key
    genai.configure(api_key=google_key)
    st.success("Credentials accepted. Asking Google for the complete list...")
    st.divider()
except Exception as e:
    st.error("⚠️ Could not find Google Key in .streamlit/secrets.toml")
    st.stop()

# --- 2. The Roll Call Spell ---
st.subheader("Available Generation Models:")
st.write("Scanning the Imperial Registry for models that can create content...")

found_models = []

with st.spinner("Scanning..."):
    try:
        # Ask Google for the list of ALL models
        for model in genai.list_models():
            # We only want models that can "generateContent" (chat/text/images)
            if 'generateContent' in model.supported_generation_methods:
                found_models.append(model.name)
                
    except Exception as e:
        st.error(f"The scan failed: {e}")
        st.stop()

# --- 3. Display the Results ---
if found_models:
    st.write(f"Found {len(found_models)} capable models accessible with your key:")
    
    # Loop through the list and display them cleanly
    for model_name in found_models:
        # Let's highlight the Flash model we were planning to use
        if 'flash' in model_name and '1.5' in model_name:
             st.markdown(f"👉 **`{model_name}`** ✨ *(Our Current Best Option for Speed)*")
        # Let's highlight any potential "image" models if they appear
        elif 'image' in model_name or 'vision' in model_name:
             st.markdown(f"🎨 **`{model_name}`** 🕵️‍♀️ *(Potentially an Artist?)*")
        else:
             st.markdown(f"- `{model_name}`")
else:
    st.warning("Strange... no generation models were found for your key.")