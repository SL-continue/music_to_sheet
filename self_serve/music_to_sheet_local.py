import subprocess
import tempfile
import os
import shutil
from basic_pitch.inference import predict

def find_musescore():
    """Finds MuseScore 4 or 3 automatically."""
    possible_executables = ["MuseScore4.exe", "MuseScore3.exe", "musescore3", "musescore4"]

    for exe in possible_executables:
        path = shutil.which(exe)
        if path:
            print(f"✅ Found MuseScore at: {path}")
            return path

    raise FileNotFoundError("MuseScore3/4 not found")


#Transcribes an audio file to a sheet music PDF using Basic Pitch and MuseScore.
def generate_sheet_from_audio(audio_file_path, file_name):
    # Generate MIDI using Basic Pitch
    _, midi_data, _ = predict(audio_file_path)

    # Create a temporary MIDI file
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp_midi:
        midi_path = tmp_midi.name
        midi_data.write(midi_path)

    # Define PDF output path
    # pdf_path = os.path.join(tempfile.gettempdir(), f"{file_name}.pdf")
    pdf_path = f"{file_name}.pdf"

    # Convert MIDI to PDF using MuseScore CLI
    musescore_path = find_musescore()

    try:
        command = [
            musescore_path,
            "-o", pdf_path,
            midi_path  # Input MIDI file
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        print(f"❌ MuseScore PDF Export Failed: {e}")
        print(f"🔍 Error Output: {e.stderr}")
        return None

    finally:
        # Clean up temporary MIDI file
        if os.path.exists(midi_path):
            os.remove(midi_path)

    return pdf_path  # Return the generated PDF path