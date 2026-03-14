import streamlit as st
from google import genai
from google.genai import types
import json

def get_gemini_client():
    """Initializes and returns the Gemini client."""
    return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def generate_npc_text(concept: str, tone: str) -> dict:
    """
    Generates the NPC text data and returns a structured dictionary.
    Handles JSON parsing and error checking locally.
    """
    # 1. DEFINE VIBES
    if tone == "Grim & Shadow":
        text_vibe = "themes include: Horror, the seedy underbelly, evil, malignant forces, nightmares, disturbing reality, messiness, visible violence, grime, and survival. Characters should feel dangerous, terrifying, or part of a ruthless dark-fantasy world."
    elif tone == "Noble & Bright":
        text_vibe = "themes include: High fantasy, heroic, hopeful, noble, absolute purity, celestial light, epic scale, righteousness, pristine appearances, and grand ideals. Characters should feel majestic, powerful, honorable, or divine."
    else:
        text_vibe = "themes include: strange, eerie, weird, dreamlike logic, mysterious, heavy folklore, unsettling phenomena, reality-bending, and the unknown. Characters should feel alien, ancient, esoteric, or tied to unnatural magics."

    text_prompt = f"""
    Role: Master Worldbuilder and Grounded Fantasy DM.
    Task: Create a vivid, highly believable, and realistic NPC based on: "{concept}".
    Rules: 
    1. Norse-inspired name (EASY to pronounce). 
    2. Tone: {text_vibe}
    3. Contextual realism: The setting is high-fantasy. Apply realism based on the subject's nature. Avoid cartoonish high-fantasy tropes. 
    4. MANDATORY COMPLIANCE: The Visual_Desc MUST be PG-13. 
    5. No Stats.
    Format: JSON with keys: Name, Class, Visual_Desc, Lore, Greeting.
    """
    
    client = get_gemini_client()
    text_response = client.models.generate_content(
        model='gemini-3-pro-preview',
        contents=text_prompt
    )
    
    raw_text = text_response.text.replace('```json', '').replace('```', '').strip()
    parsed_json = json.loads(raw_text)
    
    if isinstance(parsed_json, list):
        return parsed_json[0]
    return parsed_json

def _get_image_style(tone: str) -> str:
    """Helper to maintain a single source of truth for visual styles and tags."""
    base_style = "Award-winning National Geographic wildlife photography, hyper-realistic, 8k resolution, shot on 35mm lens, highly detailed, realistic textures, grounded, environmental storytelling, subject in their natural environment. ABSOLUTELY NO CGI, NO 3D RENDER, NO CARTOON, NO VIDEO GAME GRAPHICS."

    if tone == "Grim & Shadow":
        img_vibe = "Horror aesthetic, terrifying, evil presence, malignant, nightmare fuel, disturbing dark fantasy, gritty, low key lighting, heavy shadows, ominous mood, dirty and battle-worn equipment, muddy or dimly lit background."
    elif tone == "Noble & Bright":
        img_vibe = "Epic high fantasy style, vibrant saturated colors, golden hour lighting, radiant, glowing, majestic atmosphere, pristine, ethereal, sharp focus, beautiful epic landscape background, heavenly light shafts."
    else:
        img_vibe = "Weird surreal style, mist-filled atmosphere, strange unnatural colors, folklore aesthetic, hauntingly beautiful, eerie cinematic lighting, otherworldly natural background, anomalous phenomena."
    
    return f"{base_style} {img_vibe}"

def generate_npc_image(visual_desc: str, char_class: str, tone: str) -> bytes:
    """
    Generates an image of the NPC based on the text description and tone.
    Returns the raw image bytes.
    """
    full_style = _get_image_style(tone)
        
    image_prompt = (
        f"A hyper-realistic photograph of a {char_class}. "
        f"Description: {visual_desc}. "
        f"They MUST be placed in an environment that naturally fits them (do not use a plain studio background). "
        f"Style: {full_style}"
    )
    
    client = get_gemini_client()
    image_response = client.models.generate_images(
        model='imagen-4.0-ultra-generate-001',
        prompt=image_prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="3:4",
        )
    )
    
    # Return the raw image bytes
    return image_response.generated_images[0].image.image_bytes

def remix_npc_image(base_visual: str, char_class: str, tweak: str, tone: str) -> bytes:
    """
    Rerolls an image by combining the character's original visual description
    with a specific user tweak (e.g., 'give him a scar').
    """
    full_style = _get_image_style(tone)
        
    image_prompt = (
        f"A hyper-realistic photograph of a {char_class}. "
        f"Base Description: {base_visual}. "
        f"MANDATORY NEW DETAIL: {tweak}. "
        f"They MUST be placed in an environment that naturally fits them (do not use a plain studio background). "
        f"Style: {full_style}"
    )
    
    client = get_gemini_client()
    image_response = client.models.generate_images(
        model='imagen-4.0-ultra-generate-001',
        prompt=image_prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="3:4",
        )
    )
    return image_response.generated_images[0].image.image_bytes

# -----------------------------------------------------------------------------
# 3. MAGIC ITEM LOGIC
# -----------------------------------------------------------------------------
def generate_item_text(concept: str, rarity: str) -> dict:
    """
    Generates the Magic Item text data and returns a structured dictionary.
    Handles JSON parsing locally.
    """
    text_prompt = f"""
    Role: Master Worldbuilder and Grounded Fantasy DM.
    Task: Create a vivid, highly believable, and realistic Magic Item based on: "{concept}".
    Rules: 
    1. Tone: Mysterious, ancient, and grounded in a dark high-fantasy setting.
    2. Rarity: {rarity}
    3. MANDATORY COMPLIANCE: The Visual_Desc MUST be PG-13. 
    Format: JSON strictly with these exact keys: Name, Type, Rarity, Lore, Visual_Desc.
    """
    
    client = get_gemini_client()
    text_response = client.models.generate_content(
        model='gemini-3-pro-preview',
        contents=text_prompt
    )
    
    raw_text = text_response.text.replace('```json', '').replace('```', '').strip()
    parsed_json = json.loads(raw_text)
    
    if isinstance(parsed_json, list):
        return parsed_json[0]
    return parsed_json

def generate_item_image(visual_desc: str, item_type: str) -> bytes:
    """
    Generates an image of the Magic Item based on the text description.
    Returns the raw image bytes.
    """
    base_style = "Museum quality artifact macro photography, highly detailed, realistic textures, eerie cinematic lighting, 8k resolution, dramatic shadows, grounded. ABSOLUTELY NO CGI, NO 3D RENDER, NO CARTOON, NO VIDEO GAME GRAPHICS."
        
    image_prompt = (
        f"A hyper-realistic close-up photograph of a magical {item_type}. "
        f"Description: {visual_desc}. "
        f"The item MUST be placed naturally on a textured surface like worn leather, an ancient stone altar, or dark velvet. "
        f"Style: {base_style}"
    )
    
    client = get_gemini_client()
    image_response = client.models.generate_images(
        model='imagen-4.0-ultra-generate-001',
        prompt=image_prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",  # Items look great in square aspects
        )
    )
    
    return image_response.generated_images[0].image.image_bytes

def remix_item_image(base_visual: str, item_type: str, tweak: str) -> bytes:
    """
    Rerolls an item image by combining the artifact's original visual description
    with a specific user tweak (e.g., 'Make it glow blue').
    """
    base_style = "Museum quality artifact macro photography, highly detailed, realistic textures, eerie cinematic lighting, 8k resolution, dramatic shadows, grounded. ABSOLUTELY NO CGI, NO 3D RENDER, NO CARTOON, NO VIDEO GAME GRAPHICS."
        
    image_prompt = (
        f"A hyper-realistic close-up photograph of a magical {item_type}. "
        f"Base Description: {base_visual}. "
        f"MANDATORY NEW DETAIL: {tweak}. "
        f"The item MUST be placed naturally on a textured surface like worn leather, an ancient stone altar, or dark velvet. "
        f"Style: {base_style}"
    )
    
    client = get_gemini_client()
    image_response = client.models.generate_images(
        model='imagen-4.0-ultra-generate-001',
        prompt=image_prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
        )
    )
    
    return image_response.generated_images[0].image.image_bytes
