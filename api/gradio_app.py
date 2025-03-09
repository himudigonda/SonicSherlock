import gradio as gr
from fastapi import FastAPI, UploadFile, HTTPException
import uvicorn
import asyncio
from io import BytesIO  # Import BytesIO
import requests  # Import the requests library

from utils.logger import logger

# Create a FastAPI app instance
app = FastAPI()

# Define the Gradio interface
def recognize_audio_interface(audio_file):
    """Recognizes audio via Gradio, using direct POST to the /recognize endpoint."""
    logger.info("api.gradio_app.recognize_audio_interface :: Running Gradio interface")
    try:
        if not audio_file:
            return "Please provide an audio file."

        # Read the audio file into bytes
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()

        # Create a multipart form to send the file
        files = {"file": ("audio.wav", BytesIO(audio_bytes), "audio/wav")}  # Set content type to audio/wav

        # Make a POST request to the /recognize endpoint in FastAPI
        response = requests.post("http://localhost:8000/recognize/", files=files)  # Updated URL

        if response.status_code == 200:
            result = response.json()
            if result and result.get("song_id"):  # Safely check for song_id
                return f"Song ID: {result['song_id']}, Title: {result['title']}, Artist: {result['artist']}"
            else:
                return "No match found."
        else:
            logger.error(f"api.gradio_app.recognize_audio_interface :: Error from /recognize endpoint: {response.status_code} - {response.text}")
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        logger.error(f"api.gradio_app.recognize_audio_interface :: Error in Gradio interface: {e}")
        return f"Error: {str(e)}"

iface = gr.Interface(
    fn=recognize_audio_interface,
    inputs=gr.Audio(type="filepath"),
    outputs="text",
    title="SonicSherlock Audio Recognition",
    description="Upload an audio file or record from your microphone to identify the song."
)

# Launch the Gradio app (standalone - Uvicorn is NOT needed here)
iface.launch(server_name="0.0.0.0", server_port=8001)
