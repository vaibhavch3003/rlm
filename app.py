import streamlit as st
from models.imnci_llm import classify_symptoms  # Import function from imnci_llm.py

# Streamlit UI Setup
st.set_page_config(page_title="IMNCI AI Assistant", layout="wide")
st.title("👶 IMNCI AI Assistant for ANM / Field Worker")

st.write("""
### 🏥 IMNCI Classification
Type the newborn's symptoms below, and our AI will provide a structured IMNCI chart with **classification & treatment plans**.
""")

# Initialize session state for symptoms
if "symptoms_text" not in st.session_state:
    st.session_state["symptoms_text"] = ""

# Text Input for Symptoms
symptoms_text = st.text_area("Enter the symptoms of the newborn (0-2 months) or child (2 months-5 years):", 
                             value=st.session_state["symptoms_text"], height=150)

# Button to classify symptoms
if st.button("Classify and Generate IMNCI Chart"):
    if symptoms_text.strip():
        st.session_state["symptoms_text"] = symptoms_text  # Save input in session state
        result = classify_symptoms(symptoms_text)  # Call the LLM model for classification

        st.subheader("📝 IMNCI Classification & Treatment Plan")
        st.write(result)  # Display the output from the model
    else:
        st.warning("Please enter symptoms to proceed with classification.")
