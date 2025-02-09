import streamlit as st
import requests
import tempfile
import os

# Replace with your actual EC2 Public IP
API_URL = "http://3.145.179.33:8000/convert/"

VALID_EXTENSIONS = ["mp3", "ogg", "wav", "flac", "m4a"]

st.title("🎵 AI-Powered Music Transcription")
st.write("Upload an audio file (.mp3, .ogg, .wav, .flac, .m4a), and we'll generate a **music sheet (PDF)** for you!")

# Initialize session state for file path
if "pdf_file_path" not in st.session_state:
    st.session_state.pdf_file_path = None

# File uploader
uploaded_file = st.file_uploader("Upload an audio file", type=VALID_EXTENSIONS)

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]
    file_name = uploaded_file.name.split('.')[0]
    if (file_type not in VALID_EXTENSIONS):
        st.error(f"Invalid file type: {file_type}. Please upload a file with one of the following extensions: {', '.join(VALID_EXTENSIONS)}")


    st.audio(uploaded_file, format="audio/wav")

    if st.button("Convert to Sheet Music 🎼"):
        with st.spinner("Processing... 🎵"):
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"{file_type}") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())  # Save uploaded file
                tmp_file_path = tmp_file.name  # Get the temporary file path

            # Send file to API
            with open(tmp_file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(API_URL, files=files)

            # Handle Response
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_pdf:
                    output_pdf.write(response.content)
                    output_pdf_path = output_pdf.name
                st.session_state.pdf_file_path = output_pdf_path
            else:
                st.error(f"❌ Error: {response.json()}")
                st.session_state.pdf_file_path = None
            try:
                os.remove(tmp_file_path)  # Remove temp audio file
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")

if st.session_state.pdf_file_path:
    st.success("✅ Conversion successful!")
    with open(st.session_state.pdf_file_path, "rb") as f:
        st.download_button(
            label="📥 Download Sheet Music",
            data=open(st.session_state.pdf_file_path,"rb"),
            file_name=f"{file_name}.pdf",
            mime="application/pdf",
        )
