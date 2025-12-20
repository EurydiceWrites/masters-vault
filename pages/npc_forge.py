import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NPC Forge",
    page_icon="⚒️",
    layout="centered"
)

# --- CSS STYLING (THE ANVIL FIX) ---
st.markdown("""
<style>
    /* IMPORTS (Matching home.py) */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;800&family=Cormorant+Garamond:wght@400;600&family=Lato:wght@400;700&display=swap');

    /* VARIABLES */
    :root {
        --stone-bg: #1c1c1c; 
        --stone-dark: #0e0e0e; 
        --emerald-glow: #50c878;
        --iron-grey: #2a2a2a;
        --iron-light: #3d3d3d;
    }

    /* GENERAL PAGE BG */
    .stApp {
        background-color: var(--stone-dark);
        background-image: radial-gradient(circle at 50% 10%, #252525 0%, #000 100%);
    }

    /* --- THE ANVIL CONTAINER (THE FORM) --- */
    [data-testid="stForm"] {
        background: linear-gradient(180deg, var(--iron-light) 0%, var(--iron-grey) 80%);
        border: 1px solid #555;
        border-bottom: none; /* The button becomes the bottom */
        
        /* THE SHAPE: A subtle Anvil silhouette using clip-path */
        /* Note: We keep the bottom flat (0% and 100% x at 100% y) for the button base */
        clip-path: polygon(
            5% 0%, 95% 0%,       /* Top width */
            100% 10%, 100% 60%,  /* Right side flares */
            90% 85%, 90% 100%,   /* Taper in to base */
            10% 100%, 10% 85%,   /* Left side taper */
            0% 60%, 0% 10%       /* Left side flares */
        );
        
        /* CRITICAL FIX: Remove default Streamlit padding so button hits edges */
        padding: 0px !important; 
    }

    /* --- THE INPUT AREA (Top part of Anvil) --- */
    /* We target the first div inside the form to add padding BACK to the inputs */
    [data-testid="stForm"] > div:nth-child(1) {
        padding: 3rem 4rem 1rem 4rem !important;
        gap: 1.5rem !important; /* Spacing between input fields */
    }

    /* LABEL STYLING (Diegetic Text) */
    .stTextInput label, .stSelectbox label, .stTextArea label {
        font-family: 'Cinzel', serif !important;
        color: #aaa !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.9rem;
    }

    /* INPUT BOX STYLING (Engraved look) */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea {
        background-color: rgba(0,0,0,0.3) !important;
        border: 1px solid #444 !important;
        border-radius: 2px !important;
        color: var(--emerald-glow) !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.1rem;
    }

    /* --- THE BUTTON (THE ANVIL BASE) --- */
    /* Target the container of the button to remove margins */
    .stButton {
        margin-top: 0px !important;
        padding-bottom: 0px !important;
        width: 100%;
    }

    /* Target the actual button element */
    .stButton > button {
        width: 100% !important;
        border-radius: 0px !important; /* Square block */
        height: 80px !important; /* Thick base */
        background: #000 !important; /* Solid Black Iron */
        border: none !important;
        border-top: 2px solid #555 !important; /* Separator from form */
        
        font-family: 'Cinzel', serif !important;
        font-weight: 800 !important;
        letter-spacing: 5px !important;
        font-size: 1.5rem !important;
        color: #666 !important; /* Dormant state */
        
        transition: all 0.3s ease !important;
    }

    /* HOVER STATE (Heating up) */
    .stButton > button:hover {
        background: linear-gradient(to top, #000, #1a0505) !important;
        color: #ff4500 !important; /* Molten Orange text */
        text-shadow: 0 0 20px #ff4500;
        border-top: 2px solid #ff4500 !important;
    }
    
    /* REMOVE STREAMLIT BRANDING/HEADER SPACE */
    header {visibility: hidden;}
    .block-container {padding-top: 2rem;}

</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center; font-family: Cinzel; color: #50c878; font-size: 3rem;'>THE NPC FORGE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-family: Cormorant Garamond; color: #888; margin-bottom: 2rem; font-style: italic;'>Strike the iron while it is hot.</p>", unsafe_allow_html=True)

# --- THE ANVIL FORM ---
# We use a standard form, but the CSS above transforms it into the Anvil shape.
with st.form("anvil_form"):
    
    # -- TOP SECTION: IDENTITY --
    col1, col2 = st.columns(2)
    with col1:
        name_input = st.text_input("True Name", placeholder="e.g. Valerius the Grim")
    with col2:
        role_input = st.selectbox("Archetype", ["Soldier", "Merchant", "Noble", "Cultist", "Beggar", "Mage"])

    # -- MIDDLE SECTION: DETAILS --
    quirk_input = st.text_input("Defining Quirk", placeholder="e.g. Speaks in whispers, missing left ear...")
    
    # -- BOTTOM SECTION: SECRET --
    secret_input = st.text_area("Dark Secret", placeholder="What are they hiding from the party?", height=100)

    # -- THE BASE (SUBMIT BUTTON) --
    # The CSS targets this specific button to become the black base of the anvil
    submitted = st.form_submit_button("FORGE NPC")

# --- LOGIC HANDLING ---
if submitted:
    if not name_input:
        st.error(" The iron is too cold. You must provide a Name.")
    else:
        # Success Animation / Output
        st.markdown(f"""
        <div style="background: rgba(80, 200, 120, 0.1); border-left: 4px solid #50c878; padding: 20px; margin-top: 30px; border-radius: 4px;">
            <h3 style="font-family: Cinzel; color: #50c878; margin:0;">{name_input} Created</h3>
            <p style="font-family: Cormorant Garamond; font-size: 1.2rem; color: #ddd;">
                An {role_input} who {quirk_input.lower() if quirk_input else "is unremarkable"}.
            </p>
        </div>
        """, unsafe_allow_html=True)