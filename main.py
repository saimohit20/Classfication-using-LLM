import streamlit as st
from PIL import Image
from agents.gemma_agent import run_gemma_model
from agents.gemini_agent import run_gemini_model

st.set_page_config(page_title="Rare Object Detector", layout="centered")
st.title("🔍 Rare Class Detector")

# --- Upload image ---
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# --- Model selector ---
model_choice = st.selectbox("Select a model", ["gemini", "gemma"])

# --- Trigger detection ---
if uploaded_file is not None and model_choice:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("🔄 Processing...")

    if model_choice == "gemini":
        result = run_gemini_model(uploaded_file)
    elif model_choice == "gemma":
        result = run_gemma_model(uploaded_file)

    st.subheader("🎯 Detection Result")
    st.json(result)
