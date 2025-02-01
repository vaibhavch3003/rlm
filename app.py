import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from models.imnci_llm import classify_symptoms  # Import function from imnci_llm.py
import tempfile

# Streamlit UI Setup
st.set_page_config(page_title="IMNCI AI Assistant", layout="wide")
st.title("👶 IMNCI AI Assistant for ANM / Field Worker")

st.write("""
### 🏥 Voice-Assisted IMNCI Classification
Simply **speak** or **type** the newborn's symptoms, and our AI will provide a structured IMNCI chart with **classification & treatment plans**.
""")

# Initialize session state for symptoms
if "symptoms_text" not in st.session_state:
    st.session_state["symptoms_text"] = ""

# Function to record audio using sounddevice
def record_audio(duration=5, fs=44100):
    st.info(f"🎙 Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    return recording, fs

# Function to convert recorded audio to text using SpeechRecognition
def get_voice_input():
    recording, fs = record_audio()
    
    # Save recording to a temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        wav.write(temp_wav.name, fs, recording)
        temp_wav_path = temp_wav.name

    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            st.success("✅ Voice input recorded successfully!")
            text = recognizer.recognize_google(audio_data)
            st.session_state["symptoms_text"] = text
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio. Please try again.")
        except sr.RequestError:
            st.error("❌ Could not request results from the speech recognition service.")

# User Input Section
st.subheader("🗣 Speak or 📝 Type Symptoms")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎙 Record Symptoms"):
        get_voice_input()

with col2:
    symptoms_input = st.text_area("Or type the symptoms here:", value=st.session_state["symptoms_text"])

# Process Symptoms and Display IMNCI Chart
if st.button("🔍 Analyze Symptoms"):
    if symptoms_input.strip() == "":
        st.warning("⚠️ Please provide symptoms via voice or text.")
    else:
        with st.spinner("Analyzing symptoms..."):
            result = classify_symptoms(symptoms_input)
            st.success("✅ Symptoms classified successfully!")
            st.write("### IMNCI Classification & Treatment Plan:")
            st.json(result)

