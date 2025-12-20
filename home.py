import streamlit as st

st.set_page_config(
    page_title="The Master's Vault",
    page_icon="🗝️",
    layout="centered"
)

st.title("🗝️ The Master's Vault")

st.info("System Status: Online | Welcome, Master.")

st.markdown("---")

# Use Columns to create a side-by-side layout for your buttons
col1, col2 = st.columns(2)

with col1:
    st.header("🛡️ NPC Forge")
    st.write("Generate complete characters: Name, Class, Backstory, and Stats.")
    # This creates the button
    st.page_link("pages/npc_forge.py", label="Enter the Forge", icon="🔥", use_container_width=True)

with col2:
    st.header("🎨 Art Studio")
    st.write("Generate high-fidelity visuals: Landscapes, Items, and Monsters.")
    # This creates the button
    st.page_link("pages/art_studio.py", label="Enter the Studio", icon="🎨", use_container_width=True)

st.markdown("---")
st.caption("© 2025 Project Mind's Eye | Operational Guide v1.0")