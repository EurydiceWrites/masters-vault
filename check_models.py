import streamlit as st
from google import genai

st.set_page_config(page_title="Model Checker", page_icon="🕵️‍♀️")
st.title("🕵️‍♀️ The Royal Model Roll Call")

# --- 1. Connect to the Vault ---
try:
    # Grab the key securely
    google_key = st.secrets["GOOGLE_API_KEY"]
    
    # NEW WAY: Create the Keymaster (Client) instead of configuring globally
    client = genai.Client(api_key=google_key)
    
    st.success("Credentials accepted. Asking Google for the complete list...")
    st.divider()
except Exception as e:
    st.error(f"⚠️ Could not connect: {e}")
    st.stop()

# --- 2. The Roll Call Spell ---
st.subheader("Available Generation Models:")
st.write("Scanning the Imperial Registry for models that can create content...")

found_models = []

with st.spinner("Scanning..."):
    try:
        # NEW WAY: Ask the Keymaster for the list of models
        for model in client.models.list():
            # Grab the name of every model returned
            found_models.append(model.name)
                
    except Exception as e:
        st.error(f"The scan failed: {e}")
        st.stop()

# --- 3. Display the Results ---
if found_models:
    st.write(f"Found {len(found_models)} capable models accessible with your key:")
    
    # Loop through the list and display them cleanly
    for model_name in found_models:
        # Highlight the Flash model
        if 'flash' in model_name and '1.5' in model_name:
             st.markdown(f"👉 **`{model_name}`** ✨ *(Our Current Best Option for Speed)*")
        # Highlight any potential "image" models
        elif 'image' in model_name or 'vision' in model_name:
             st.markdown(f"🎨 **`{model_name}`** 🕵️‍♀️ *(Potentially an Artist?)*")
        else:
             st.markdown(f"- `{model_name}`")
else:
    st.warning("Strange... no generation models were found for your key.")