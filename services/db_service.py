import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd

# -----------------------------------------------------------------------------
# 1. AUTHENTICATION & CONNECTION (Memoized)
# -----------------------------------------------------------------------------
@st.cache_resource
def get_gspread_client():
    """Authenticates and returns the gspread client. Cached so we only connect once."""
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=SCOPES
        )
    else:
        creds = service_account.Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    
    return gspread.authorize(creds)

@st.cache_resource
def get_worksheet():
    """Returns the main NPC worksheet. Cached for performance."""
    gc = get_gspread_client()
    sh = gc.open("Masters_Vault_Db")
    return sh.worksheet("NPCs")

@st.cache_resource
def get_items_worksheet():
    """Returns the Magic Items worksheet. Cached for performance."""
    gc = get_gspread_client()
    sh = gc.open("Masters_Vault_Db")
    try:
        return sh.worksheet("Magic Items")
    except Exception as e:
        raise Exception(f"Could not find a tab named 'Magic Items' in your Google Sheet. Error: {e}")

# -----------------------------------------------------------------------------
# 2. READ OPERATIONS
# -----------------------------------------------------------------------------
@st.cache_data(ttl=60)
def get_all_records():
    """Fetches all records from the sheet as a Pandas DataFrame.
    Cached for 60 seconds to prevent rate-limiting, but auto-refreshes.
    """
    worksheet = get_worksheet()
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def clear_cache():
    """Manually invalidates the data cache (useful after writing data)."""
    get_all_records.clear()

@st.cache_data(ttl=60)
def get_all_items():
    """Fetches all records from the Items sheet as a Pandas DataFrame."""
    worksheet = get_items_worksheet()
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def clear_items_cache():
    """Manually invalidates the items cache."""
    get_all_items.clear()

# -----------------------------------------------------------------------------
# 3. WRITE OPERATIONS
# -----------------------------------------------------------------------------
def insert_character(row_data: list):
    """Inserts a new character row at the top of the sheet."""
    worksheet = get_worksheet()
    worksheet.insert_row(row_data, 2)
    clear_cache()

def insert_item(row_data: list):
    """Inserts a new item row at the top of the Items sheet."""
    worksheet = get_items_worksheet()
    worksheet.insert_row(row_data, 2)
    clear_items_cache()

def update_character_meta(sheet_row: int, campaign: str, faction: str):
    """Updates specific columns (Campaign, Faction) for a given row."""
    worksheet = get_worksheet()
    worksheet.update_cell(sheet_row, 8, campaign)
    worksheet.update_cell(sheet_row, 9, faction)
    clear_cache()

def update_character_image(sheet_row: int, new_image_url: str):
    """Updates only the Image_URL column (Column 6 in the sheet) for a given row."""
    worksheet = get_worksheet()
    worksheet.update_cell(sheet_row, 6, new_image_url)
    clear_cache()

def delete_character(sheet_row: int):
    """Deletes a specific row in the sheet."""
    worksheet = get_worksheet()
    worksheet.delete_rows(sheet_row)
    clear_cache()
