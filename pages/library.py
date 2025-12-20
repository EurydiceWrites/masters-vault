import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIG ---
st.set_page_config(page_title="The Library", page_icon="📚", layout="wide")
st.markdown("""<style>.stApp { background-color: #0E1117; color: #FAFAFA; } .stContainer { background-color: #262730; border: 1px solid #444; border-radius: 10px; padding: 10px; }</style>""", unsafe_allow_html=True)

# --- CONNECT ---
SHEET_ID = "1mhKTWKjRfYIKEV9uyAIkHy6HYdqbBxsCsiGHODs1C0w"

@st.cache_data(ttl=10) # Updates every 10s
def get_library():
    try:
        SCOPE = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        # This function relies on Row 1 being HEADERS
        return sheet.get_all_records() 
    except Exception as e:
        return []

# --- UI ---
st.title("📚 The Masters Vault")

# 1. Get Data
data = get_library()

if not data:
    st.warning("The Library is empty! (Or connection failed). Make sure Row 1 of your Sheet has headers: Name, Class, Lore, Greeting, Visual, Image_URL")
    st.stop()

# 2. Search
search = st.text_input("🔍 Search...", placeholder="Find a character...").lower()
if search:
    data = [d for d in data if search in str(d).lower()]

# 3. Grid Display
cols = st.columns(3) # 3 columns wide

for i, npc in enumerate(data):
    with cols[i % 3]: # Cycles 0, 1, 2, 0, 1, 2...
        with st.container(border=True):
            # Image (We look for the key 'Image_URL' - MAKE SURE YOUR HEADER MATCHES THIS)
            # If you named your header "Link" or "Url", change this word below!
            img_link = npc.get('Image_URL') or npc.get('image_url') or npc.get('Link')
            
            if img_link and str(img_link).startswith("http"):
                st.image(img_link, use_container_width=True)
            else:
                st.warning("No Image")
            
            st.subheader(npc.get('Name', 'Unknown'))
            st.caption(f"**Class:** {npc.get('Class', '?')}")
            with st.expander("Read Lore"):
                st.write(npc.get('Lore', '...'))
            with st.expander("Greeting"):
                st.info(f"\"{npc.get('Greeting', '...')}\"")