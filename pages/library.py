import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="The Library", page_icon="📚", layout="wide")
st.title("📚 The Master's Library")
st.caption("The archives of the Masters_Vault_Db")

# --- AUTHENTICATION ---
# (We reuse the exact same auth block that works in the Forge)
try:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    if "gcp_service_account" in st.secrets:
        service_account_info = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
        gc = gspread.authorize(creds)
    else:
        # Local fallback
        creds = service_account.Credentials.from_service_account_file(
            "service_account.json",
            scopes=SCOPES
        )
        gc = gspread.authorize(creds)
        
except Exception as e:
    st.error(f"🚨 Connection Error: {e}")
    st.stop()

# --- FETCH DATA ---
try:
    sh = gc.open("Masters_Vault_Db")
    worksheet = sh.get_worksheet(0)
    
    # Get all records as a list of dictionaries
    data = worksheet.get_all_records()
    
    # Convert to Pandas DataFrame for easier handling
    df = pd.DataFrame(data)

    if df.empty:
        st.info("The Library is empty. Go to the Forge to summon new souls.")
        st.stop()

except Exception as e:
    st.error(f"Could not read from Vault: {e}")
    st.stop()

# --- DISPLAY OPTIONS ---
# Allow filtering by Class
all_classes = ["All"] + list(df['Class'].unique())
selected_class = st.selectbox("Filter by Class:", all_classes)

if selected_class != "All":
    df = df[df['Class'] == selected_class]

st.markdown("---")

# --- DISPLAY CARDS ---
# We iterate through the rows and display them
for index, row in df.iterrows():
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        # COLUMN 1: IMAGE
        with col1:
            if row['Image_URL'] and str(row['Image_URL']).startswith("http"):
                st.image(row['Image_URL'], use_container_width=True)
            else:
                st.info("No Image")
                
        # COLUMN 2: STATS & LORE
        with col2:
            st.subheader(row['Name'])
            st.caption(f"**Class:** {row['Class']} | **Summoned:** {row['Timestamp']}")
            
            st.markdown(f"**🗣️ Greeting:** *\"{row['Greeting']}\"*")
            
            with st.expander("Read Full Lore"):
                st.write(row['Lore'])
                st.markdown(f"**Visual Notes:** {row['Visual_Desc']}")
                
        st.markdown("---")