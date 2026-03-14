import streamlit as st
import cloudinary
import cloudinary.uploader

# Memoize the configuration so we only set it up once per session
@st.cache_resource
def setup_cloudinary():
    """Initializes and returns the Cloudinary configuration securely."""
    try:
        cloudinary.config(
            cloud_name = st.secrets["cloudinary"]["cloud_name"],
            api_key = st.secrets["cloudinary"]["api_key"],
            api_secret = st.secrets["cloudinary"]["api_secret"],
            secure = True
        )
        return True
    except Exception as e:
        print(f"Cloudinary Config Error: {e}")
        return False

def upload_image_to_cdn(data_uri: str, folder: str = "Well_of_Souls") -> str:
    """
    Uploads a Base64 encoded image string to Cloudinary.
    Returns the secure URL on success, or an error string on failure.
    """
    setup_cloudinary()
    
    try:
        upload_result = cloudinary.uploader.upload(data_uri, folder=folder)
        return upload_result.get("secure_url", "Upload Failed")
    except Exception as e:
        print(f"Cloudinary Upload Error: {e}")
        return f"Image Upload Failed: {e}"
