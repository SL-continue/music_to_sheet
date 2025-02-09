from fastapi import FastAPI, UploadFile, File
import subprocess
import tempfile
import os
import shutil
from basic_pitch.inference import predict
from fastapi.responses import FileResponse

app = FastAPI()

def find_musescore():
    possible_executables = ["musescore", "musescore3", "musescore4"]
    for exe in possible_executables:
        path = shutil.which(exe)
        if path:
            print(f"Found MuseScore at: {path}")
            return path
    return "/usr/bin/musescore3"

@app.post("/convert/")
async def convert_file(file: UploadFile = File(...)):
    # Save uploaded file
    audio_path = f"/tmp/{file.filename}"
    file_name = file.filename.split(".")[0]

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate MIDI using Basic Pitch
    _, midi_data, _ = predict(audio_path)

    # Create a temporary MIDI file
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as tmp_midi:
        midi_path = tmp_midi.name
        midi_data.write(midi_path)

    # Define PDF output path
    pdf_path = os.path.join(tempfile.gettempdir(), f"{file_name}.pdf")

    # Convert MIDI to PDF using MuseScore CLI
    musescore_path = find_musescore()
    command = ["xvfb-run", musescore_path, "-o", pdf_path, midi_path]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        return {"error": f"MuseScore PDF export failed: {e}"}

    finally:
        os.remove(midi_path)

    return FileResponse(pdf_path, filename=f"{file_name}.pdf")
