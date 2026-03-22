import streamlit as st

def load_css():
    """Injects the core Dark Fantasy visual engine CSS into the Streamlit app.
    Call this at the very top of each page below st.set_page_config.
    """
    st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Lato:wght@400;700&display=swap');

    /* --- VARIABLES --- */
    :root {
        --stone-bg: #111;
        --emerald-glow: #50c878;
        --emerald-bright: #66ff99;
        --emerald-dim: #1e3a2a;
        --destruct-red: #8b0000;
        --destruct-bright: #ff4500;
        --nav-gold: #d4af37; 
        --gold-glow: rgba(212, 175, 55, 0.6);
        
        /* Balanced Text Colors */
        --text-stone: #888;      /* Warm Matte Grey */
        --text-metal: #8a9ba8;   /* Cool Steel Grey */
    }

    /* --- GLOBAL BACKGROUND --- */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000 80%);
    }

    /* --- SIDEBAR STYLING --- */
    [data-testid="stSidebar"] { 
        background-color: #080808; 
        border-right: 1px solid #1e3a2a; 
    }
    
    .sidebar-header {
        font-family: 'Cinzel', serif;
        color: var(--emerald-bright);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        margin-top: 2rem;
        border-bottom: 1px solid var(--emerald-dim);
        padding-bottom: 0.5rem;
        text-align: center;
        text-shadow: 0 0 10px var(--emerald-dim);
    }

    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #111 !important;
        border: 1px solid #333 !important;
        color: #ddd !important;
        font-family: 'Cinzel', serif !important;
        border-radius: 0px !important; 
    }

    /* Sidebar Navigation Links */
    [data-testid="stSidebarNav"] a {
        font-family: 'Cinzel', serif !important;
        color: #888 !important;
        transition: color 0.3s ease;
    }
    [data-testid="stSidebarNav"] a:hover {
        color: var(--nav-gold) !important;
        text-shadow: 0 0 10px var(--gold-glow);
    }

    header[data-testid="stHeader"] { background: transparent; }

    /* --- AGGRESSIVE INPUT OVERRIDE (THE FIX) --- */
    /* This targets every possible layer of the input box to kill the Navy Blue */
    
    /* 1. The Outer Wrapper */
    div[data-baseweb="input"] {
        background-color: #0e0e0e !important;
        border: 1px solid #333 !important;
        border-radius: 0px !important;
        padding: 5px;
    }

    /* 2. The Inner Container (Base Input) */
    div[data-baseweb="base-input"] {
        background-color: #0e0e0e !important;
        border: none !important;
        border-radius: 0px !important;
    }

    /* 3. The Input Element Itself */
    input.st-ai, input.st-ah, input[type="text"] {
        background-color: transparent !important;
        color: #e0e0e0 !important;
        font-family: 'Cinzel', serif !important;
        text-align: left !important; /* Force Left Alignment */
    }

    /* 4. Focus State */
    div[data-baseweb="input"]:focus-within {
        border-color: var(--emerald-glow) !important;
        box-shadow: 0 0 8px var(--emerald-dim) !important;
    }
    
    /* --- POPOVER MENU CONTAINER --- */
    div[data-testid="stPopoverBody"] {
        background-color: #080808 !important; /* Pitch Black */
        border: 1px solid #444 !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.9);
        border-radius: 0px; 
    }

    /* --- TOAST STYLING --- */
    div[data-testid="stToast"] {
        background-color: #0e0e0e !important;
        border: 1px solid #333 !important;
        border-left: 4px solid var(--emerald-glow) !important;
        color: #eee !important;
        font-family: 'Cinzel', serif !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.8);
        border-radius: 0px;
    }

    /* --- MAIN HEADER --- */
    h1 {
        font-family: 'Cinzel', serif !important;
        text-transform: uppercase;
        letter-spacing: 12px;
        font-size: 3rem !important;
        color: var(--emerald-bright) !important;
        text-shadow: 0 0 30px rgba(102, 255, 153, 0.4);
        margin-bottom: 0 !important;
        text-align: center;
        margin-top: 5vh !important;
    }
    .subtext {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.5rem;
        color: #888;
        font-style: italic;
        margin-bottom: 3rem;
    }

    /* --- PAGE LINKS / NAVIGATION CARDS (Vault/Index specific) --- */
    a[data-testid="stPageLink-NavLink"] {
        background: transparent !important; border: none !important;
    }

    /* Allow .vault-link-card to target index specific large cards */
    .vault-link-card {
        background: linear-gradient(145deg, #151515, #0a0a0a) !important;
        border: 1px solid #333 !important;
        border-left: 4px solid var(--emerald-dim) !important;
        padding: 3rem 2rem !important;
        border-radius: 2px !important;
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8) !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        height: 200px !important; /* Fixed Height for consistency */
    }

    .vault-link-card:hover {
        background: linear-gradient(145deg, #1a1a1a, #111) !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 20px 50px rgba(0,0,0,1), 0 0 30px rgba(80, 200, 120, 0.1) !important;
        border-color: var(--emerald-glow) !important;
        border-left: 4px solid var(--emerald-bright) !important;
    }

    .vault-link-card p {
        font-family: 'Cinzel', serif !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #e0e0e0 !important;
        letter-spacing: 4px !important;
        margin: 0 !important;
        text-transform: uppercase !important;
        text-shadow: 0 2px 5px #000 !important;
        transition: color 0.3s ease !important;
    }

    .vault-link-card:hover p {
        color: var(--emerald-bright) !important;
        text-shadow: 0 0 15px var(--emerald-glow) !important;
    }

    /* Standard Navlink styling */
    a[data-testid="stPageLink-NavLink"]:not(.vault-link-card) p { 
        color: #666; font-family: 'Cinzel', serif; font-size: 0.9rem; transition: color 0.3s; 
    }
    a[data-testid="stPageLink-NavLink"]:not(.vault-link-card):hover p { 
        color: var(--nav-gold) !important; text-shadow: 0 0 10px var(--gold-glow); 
    }

    [data-testid="stPageLink-NavLink"] img { display: none; }


    /* --- PROCEDURAL PILLS --- */
    .pill-container {
        display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; width: 100%;
        margin-top: 0.5rem;
    }

    .pill-base {
        display: inline-block;
        font-family: 'Lato', sans-serif;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 2px; 
        padding: 6px 14px;
        border-radius: 4px;
        border: 1px solid transparent; 
        min-width: 70px;
    }

    /* STONE */
    .pill-stone {
        background-color: #151515;
        background-image: radial-gradient(#000 15%, transparent 16%), radial-gradient(#000 15%, transparent 16%);
        background-size: 4px 4px;
        color: var(--text-stone);
        border: 1px solid #333;
        box-shadow: inset 0 0 4px #000; 
    }

    /* METAL */
    .pill-metal {
        background-color: #151515; 
        background-image: repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px);
        color: var(--text-metal);
        border: 1px solid #4a5568; 
        box-shadow: inset 0 0 4px #000; 
    }

    /* --- BUTTONS --- */
    button[kind="primary"] {
        background: transparent !important; border: none !important; color: #555 !important;
        font-family: 'Cinzel', serif !important; font-size: 1.1rem !important; padding: 0 !important;
        height: 60px !important; width: 100% !important; transition: all 0.3s ease !important;
        box-shadow: none !important;
        border-radius: 0px !important;
    }
    button[kind="primary"]:hover {
        color: var(--emerald-bright) !important; text-shadow: 0 0 15px var(--emerald-glow);
        transform: scale(1.05); background: transparent !important;
    }

    button[kind="secondaryFormSubmit"] {
        width: 100% !important;
        border-radius: 0px !important;
        background: transparent !important;
        border: 1px solid #444 !important;
        color: #888 !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        letter-spacing: 6px !important;
        font-size: 1.2rem !important;
        height: 70px !important;
        transition: all 0.5s ease !important;
        margin-top: 1rem;
    }
    button[kind="secondaryFormSubmit"]:hover {
        border-color: var(--emerald-bright) !important;
        color: var(--emerald-bright) !important;
        text-shadow: 0 0 15px var(--emerald-glow);
        background: rgba(80, 200, 120, 0.05) !important;
    }

    button[kind="secondary"] {
        background: transparent !important; 
        border: 1px solid #333 !important; 
        color: #555 !important;
        font-family: 'Cinzel', serif !important; 
        font-size: 0.8rem !important;
        border-radius: 0px !important;
        height: auto !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        transition: all 0.4s ease !important; 
        box-shadow: none !important;
    }
    button[kind="secondary"]:hover {
        color: var(--destruct-bright) !important;
        text-shadow: 0 0 10px var(--destruct-red) !important;
        border-color: var(--destruct-bright) !important;
    }

    /* DIVINE (POPOVER) */
    div[data-testid="stPopover"] button {
        color: var(--nav-gold) !important;
        border-color: transparent !important;
        background: transparent !important;
    }
    div[data-testid="stPopover"] button:hover {
        color: var(--nav-gold) !important;
        text-shadow: 0 0 10px var(--gold-glow) !important;
        transform: scale(1.2) !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    div[data-testid="stPopover"] button svg {
        fill: var(--nav-gold) !important;
        color: var(--nav-gold) !important;
    }

    /* --- MODAL STYLING --- */
    div[role="dialog"] {
        background-color: #0e0e0e !important;
        border: 1px solid #333 !important;
        box-shadow: 0 0 50px rgba(0,0,0,0.9);
        border-radius: 0px;
    }

    .modal-header { border-bottom: 1px solid #333; padding-bottom: 1rem; margin-bottom: 1rem; }
    .modal-name { font-family: 'Cinzel', serif; font-size: 2.5rem; color: #fff; line-height: 1.1; margin-bottom: 5px;}
    .modal-class { font-family: 'Cinzel', serif; font-size: 0.9rem; color: var(--emerald-bright); letter-spacing: 3px; text-transform: uppercase; }
    .modal-voice { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; color: #e0e0e0; font-style: italic; padding: 1.5rem; background: #0a0a0a; border-left: 2px solid var(--emerald-glow); margin-bottom: 1.5rem; }
    .modal-lore { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; color: #bbb; line-height: 1.7; text-align: justify; }
    .modal-visual { font-family: 'Cormorant Garamond', serif; font-size: 0.95rem; color: #666; font-style: italic; margin-top: 10px; border-top: 1px solid #222; padding-top: 10px; }
    .modal-meta { font-family: 'Lato', sans-serif; font-size: 0.7rem; color: #444; margin-top: 2rem; border-top: 1px solid #222; padding-top: 1rem; }

    /* --- RUNIC FOOTER --- */
    .footer-container { 
        display: flex; 
        justify-content: center; 
        gap: 2rem; 
        margin-top: 8rem; 
        padding-bottom: 2rem;
        opacity: 0.4;
    }

    .rune-span {
        font-size: 2rem; 
        color: var(--emerald-dim); 
        user-select: none; 
        cursor: default; 
        transition: all 0.5s ease; 
        animation: rune-glow 4s infinite ease-in-out;
    }

    @keyframes rune-glow {
        0%, 100% { color: var(--emerald-dim); text-shadow: none; transform: scale(1); }
        50% { color: var(--emerald-glow); text-shadow: 0 0 15px var(--emerald-dim); transform: scale(1.1); }
    }

    /* --- SPECIFIC TO THE VAULT/ARCHIVE CARDS --- */
    .archive-card {
        background: #0e0e0e;
        border: 1px solid #222;
        border-bottom: none; 
        border-top: 4px solid var(--emerald-dim);
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        display: flex;
        flex-direction: column;
        height: 640px !important; 
        margin-bottom: 0px !important;
        overflow: hidden;
    }
    .archive-card:hover {
        border-top: 4px solid var(--emerald-bright);
        box-shadow: 0 15px 50px rgba(0,0,0,1);
    }
    .img-frame { 
        width: 100%; height: 400px; overflow: hidden; 
        border-bottom: 1px solid #222; position: relative; flex-shrink: 0;
    }
    .img-frame img { 
        width: 100%; height: 100%; object-fit: cover; object-position: top center; 
        opacity: 0.95; transition: opacity 0.5s; 
    }
    .img-frame:hover img { opacity: 1; transform: scale(1.02); }

    .card-identity {
        padding: 1rem 0.5rem; text-align: center;
        background: linear-gradient(180deg, #111 0%, #0e0e0e 100%);
        flex-grow: 1; display: flex; flex-direction: column; 
        justify-content: space-between; align-items: center; gap: 0.5rem;
    }

    .identity-top { width: 100%; display: flex; flex-direction: column; gap: 0.2rem; }

    .card-name { 
        font-family: 'Cinzel', serif; font-size: 1.4rem; color: #fff; letter-spacing: 1px; 
        text-shadow: 0 4px 10px #000; line-height: 1.2;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
        min-height: 3.4rem; display: flex; align-items: center; justify-content: center;
    }

    .card-class { 
        font-family: 'Cinzel', serif; font-size: 0.8rem; color: var(--emerald-bright); 
        letter-spacing: 2px; text-transform: uppercase; opacity: 0.9;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    
    /* --- CHARACTER CARD (Forge Specific) --- */
    .character-card {
        background: #0e0e0e;
        border: 1px solid #222;
        border-top: 4px solid var(--emerald-dim);
        box-shadow: 0 20px 60px rgba(0,0,0,1);
        margin-top: 4rem;
        animation: fadein 1.5s;
    }
    .seam { height: 1px; background: radial-gradient(circle, #444 0%, transparent 90%); margin: 0; border: none; opacity: 0.6; }
    .character-card .card-header { background: #111; padding: 2rem 1rem; text-align: center; }
    .character-card .card-name { font-family: 'Cinzel', serif; font-size: 2.2rem; color: #fff; letter-spacing: 4px; margin-bottom: 0.5rem; min-height: unset; webkit-line-clamp: unset;}
    .character-card .card-class { font-family: 'Cinzel', serif; font-size: 0.9rem; color: var(--emerald-bright); letter-spacing: 3px; text-transform: uppercase; text-shadow: 0 0 10px rgba(102, 255, 153, 0.3); }

    .img-container { position: relative; overflow: hidden; }
    .img-container img { width: 100%; display: block; opacity: 0.9; transition: all 0.5s ease; cursor: zoom-in; }
    .img-container::after { content: ""; position: absolute; bottom: 0; left: 0; width: 100%; height: 80px; background: linear-gradient(to top, #0e0e0e, transparent); pointer-events: none; }
    .img-container img:hover { opacity: 1; transform: scale(1.02); }

    .visual-caption { background: #080808; padding: 2rem 3rem; font-family: 'Cormorant Garamond', serif; font-style: italic; color: #888; text-align: left; font-size: 1.15rem; line-height: 1.6; }
    .voice-section { padding: 2.5rem 3rem 1.5rem 3rem; background: radial-gradient(circle at 50% 50%, #111 0%, #0e0e0e 100%); text-align: center; }
    .voice-quote { font-family: 'Cormorant Garamond', serif; font-size: 1.5rem; color: #d0d0d0; font-style: italic; line-height: 1.4; }
    .voice-quote::before { content: "“"; font-size: 3rem; color: var(--emerald-dim); vertical-align: -1rem; margin-right: 10px; }
    .voice-quote::after { content: "”"; font-size: 3rem; color: var(--emerald-dim); vertical-align: -2rem; margin-left: 10px; }

    .lore-section { padding: 1.5rem 3rem 3rem 3rem; color: #b0b0b0; line-height: 1.7; font-size: 1.2rem; font-family: 'Cormorant Garamond', serif; background: #050505; text-align: left; }
    .lore-label { font-family: 'Cinzel', serif; font-size: 0.8rem; color: #666; letter-spacing: 2px; text-transform: uppercase; display: block; margin-bottom: 10px; text-align: center; opacity: 0.8; }

    @keyframes fadein { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

</style>
    """, unsafe_allow_html=True)
