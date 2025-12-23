import streamlit as st
import requests
import os
from dotenv import load_dotenv
from io import BytesIO
import random

# Load API key
load_dotenv()
API_KEY = os.getenv("CLIPDROP_API_KEY")

# Page config
st.set_page_config(
    page_title="AI Text to Image Generator",
    page_icon="🎨",
    layout="centered"
)

# Title
st.title("🎨 AI Text-to-Image Generator")
st.write("Generate images using **Clipdrop AI**")

# User input
prompt = st.text_input(
    "Image Description",
    placeholder="Describe the image you want..."
)

# Style selection
style = st.selectbox(
    "Select Style",
    ["Realistic", "Anime", "3D", "Digital Art"]
)

# Surprise prompts
surprise_prompts = [
    "Cyberpunk city at night",
    "Astronaut riding a horse",
    "AI robot painting art",
    "Futuristic Indian village",
    "Flying cars in the future"
]

if st.button("🎲 Surprise Me"):
    prompt = random.choice(surprise_prompts)
    st.experimental_rerun()

# Generate button
if st.button("✨ Generate Image"):
    if prompt == "":
        st.warning("Please enter a prompt")
    else:
        with st.spinner("Generating image..."):
            full_prompt = f"{style} style, {prompt}"

            response = requests.post(
                "https://clipdrop-api.co/text-to-image/v1",
                headers={
                    "x-api-key": API_KEY
                },
                files={
                    "prompt": (None, full_prompt)
                }
            )

            if response.status_code == 200:
                image_bytes = response.content
                st.image(image_bytes, caption="Generated Image", use_column_width=True)

                st.download_button(
                    label="⬇ Download Image",
                    data=image_bytes,
                    file_name="generated_image.png",
                    mime="image/png"
                )
            else:
                st.error("Image generation failed")
