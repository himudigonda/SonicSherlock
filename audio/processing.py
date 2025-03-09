import librosa
import librosa.display
import numpy as np
from scipy.ndimage import maximum_filter

from config import config
from utils.logger import logger


def load_audio(file_path):
    """Loads an audio file using librosa.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        tuple: A tuple containing the audio data as a numpy array and the sample rate.
               Returns None, None if loading fails.
    """
    logger.debug(f"audio.processing.load_audio :: Loading audio from {file_path}")
    try:
        audio, sr = librosa.load(file_path, sr=config.SAMPLE_RATE, mono=True)
        logger.debug(
            f"audio.processing.load_audio :: Audio loaded successfully. Sample rate: {sr}, Length: {len(audio)}"
        )
        return audio, sr
    except Exception as e:
        logger.error(f"audio.processing.load_audio :: Error loading audio: {e}")
        return None, None


def normalize_audio(audio):
    """Normalizes the audio data to the range -1 to 1.

    Args:
        audio (np.ndarray): The audio data.

    Returns:
        np.ndarray: The normalized audio data.
    """
    logger.debug("audio.processing.normalize_audio :: Normalizing audio")
    try:
        max_amplitude = np.max(np.abs(audio))
        normalized_audio = audio / max_amplitude
        logger.debug(
            f"audio.processing.normalize_audio :: Audio normalized. Max amplitude: {max_amplitude}"
        )
        return normalized_audio
    except Exception as e:
        logger.error(
            f"audio.processing.normalize_audio :: Error normalizing audio: {e}"
        )
        return audio  # Return the original audio in case of error


def create_spectrogram(audio):
    """Creates a spectrogram from the audio data.

    Args:
        audio (np.ndarray): The audio data.
        sr (int): The sample rate of the audio.

    Returns:
        np.ndarray: The spectrogram as a numpy array.
    """
    logger.debug("audio.processing.create_spectrogram :: Creating spectrogram")
    try:
        spectrogram = librosa.stft(
            audio, n_fft=config.FFT_WINDOW_SIZE, hop_length=config.HOP_LENGTH
        )
        spectrogram_db = librosa.amplitude_to_db(np.abs(spectrogram), ref=np.max)
        logger.debug(
            f"audio.processing.create_spectrogram :: Spectrogram created. Shape: {spectrogram_db.shape}"
        )
        return spectrogram_db
    except Exception as e:
        logger.error(
            f"audio.processing.create_spectrogram :: Error creating spectrogram: {e}"
        )
        return None


def extract_peaks(spectrogram):
    """Extracts peaks from the spectrogram using a maximum filter.

    Args:
        spectrogram (np.ndarray): The spectrogram data.

    Returns:
        list: A list of (time, frequency) tuples representing the peak locations.
    """
    logger.debug("audio.processing.extract_peaks :: Extracting peaks from spectrogram")
    try:
        # Apply maximum filter to find local maxima
        peaks = maximum_filter(spectrogram, size=10) == spectrogram
        # Get the indices of the peaks
        rows, cols = np.where(peaks)
        # Filter peaks based on the threshold
        peaks_db = [
            (col, row)
            for col, row in zip(cols, rows)
            if spectrogram[row, col] > config.PEAK_THRESHOLD
        ]
        logger.debug(f"audio.processing.extract_peaks :: Found {len(peaks_db)} peaks.")
        return peaks_db
    except Exception as e:
        logger.error(f"audio.processing.extract_peaks :: Error extracting peaks: {e}")
        return []
