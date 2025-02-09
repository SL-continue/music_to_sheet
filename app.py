import tempfile
import streamlit as st
import os
from music_to_midi import generate_sheet_from_audio

# Supported file types
VALID_EXTENSIONS = ["mp3", "ogg", "wav", "flac", "m4a"]

st.title("🎵 AI-Powered Music Transcription")
st.write("Upload an audio file (.mp3, .ogg, .wav, .flac, .m4a), and we'll generate a **music sheet (PDF)** for you!")

uploaded_file = st.file_uploader("Upload an audio file", type=VALID_EXTENSIONS)

# Check if a file is uploaded
if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]
    file_name = uploaded_file.name.split('.')[0]
    if (file_type not in VALID_EXTENSIONS):
        st.error(f"Invalid file type: {file_type}. Please upload a file with one of the following extensions: {', '.join(VALID_EXTENSIONS)}")

    # Check if PDF is already stored in session state
    if "pdf_output_path" not in st.session_state or st.session_state["last_uploaded"] != uploaded_file.name:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_audio:
            tmp_audio.write(uploaded_file.read())
            tmp_audio_path = tmp_audio.name

        # Generate the sheet music
        with st.spinner("🎼 Processing your file... Please wait."):
            pdf_output_path = generate_sheet_from_audio(tmp_audio_path, file_name)

        os.remove(tmp_audio_path)

        if pdf_output_path:
            st.session_state["pdf_output_path"] = pdf_output_path  # ✅ Store in session state
            st.session_state["last_uploaded"] = uploaded_file.name  # Track last uploaded file
        else:
            st.error("❌ Failed to generate the music sheet.")

    # Show download button only if PDF exists
    if "pdf_output_path" in st.session_state:
        st.success("✅ Music sheet generated successfully!")
        with open(st.session_state["pdf_output_path"], "rb") as pdf_file:
            st.download_button(
                label="📥 Download Transcribed Sheet Music",
                data=pdf_file,
                file_name=f"{file_name}.pdf",
                mime="application/pdf"
            )
