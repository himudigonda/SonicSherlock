from fastapi import FastAPI, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
import io  # ADDED
import random

from audio import processing
from audio import fingerprinting
from database.database_manager import DatabaseManager
from api import schemas
from matching import matcher
from utils.logger import logger
from config import config

app = FastAPI()
db_manager = DatabaseManager()


@app.post(
    "/songs/", response_model=schemas.SongResponse, status_code=status.HTTP_201_CREATED
)
async def create_song(song: schemas.SongCreate):
    """Adds a new song to the database."""
    logger.info(f"api.app.create_song :: Received request to add song: {song}")
    song_id = db_manager.add_song(song.title, song.artist)
    if song_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add song",
        )
    created_song = db_manager.get_song_by_id(song_id)
    return created_song


@app.post("/recognize/", response_model=schemas.RecognitionResponse)
async def recognize_audio(file: UploadFile):
    """Recognizes the audio and returns song information."""
    logger.info("api.app.recognize_audio :: Received audio recognition request")
    try:
        # Load audio
        import io  # ADDED

        audio_bytes = await file.read()  # Read audio bytes from SpooledTemporaryFile
        audio, sr = processing.load_audio(io.BytesIO(audio_bytes))
        if audio is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid audio file"
            )

        # Create spectrogram
        spectrogram = processing.create_spectrogram(audio)
        if spectrogram is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create spectrogram",
            )

        # Extract peaks
        peaks = processing.extract_peaks(spectrogram)

        # Create fingerprints
        fingerprints = fingerprinting.create_fingerprint(
            peaks, song_id=0
        )  # Use a dummy song_id for recognition

        # Limit the number of fingerprints to use for matching
        if len(fingerprints) > config.NUM_FINGERPRINTS_TO_USE:
            fingerprints = random.sample(fingerprints, config.NUM_FINGERPRINTS_TO_USE)
            logger.debug(
                f"api.app.recognize_audio :: Limited fingerprints to {config.NUM_FINGERPRINTS_TO_USE}"
            )

        # Match fingerprints
        matches = matcher.match_fingerprints(fingerprints)
        best_song_id, offset = matcher.get_best_match(matches)

        if best_song_id is None:
            return schemas.RecognitionResponse(song_id=None, title=None, artist=None)

        song = db_manager.get_song_by_id(best_song_id)

        if song is None:
            logger.error(
                f"api.app.recognize_audio :: Song ID not found: {best_song_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Song not found"
            )

        return schemas.RecognitionResponse(
            song_id=song.id, title=song.title, artist=song.artist
        )

    except Exception as e:
        logger.error(f"api.app.recognize_audio :: Error during recognition: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
