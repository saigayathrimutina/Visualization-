import streamlit as st
import random

st.title("🎨 AI Text-to-Image Generator (Demo)")

# User input
prompt = st.text_input("Describe the image you want...", "")

# Style selection
style = st.selectbox("Select Style", ["Realistic", "Anime", "3D", "Digital Art"])

# Surprise Me button
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

# Generate button (Demo)
if st.button("✨ Generate Image"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt!")
    else:
        # Instead of calling API, show a placeholder image
        st.image(
            "https://via.placeholder.com/512x512.png?text=AI+Image+Demo",
            caption=f"Demo Image for: {style} style, '{prompt}'",
            use_column_width=True
        )
        st.success("This is a demo. No API key is needed!")
