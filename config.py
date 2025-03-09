import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True  # Enable debug logging


class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/sonic_sherlock"
    )
    # Sample rate for audio processing (Hz)
    SAMPLE_RATE = 8000
    # Frame length for FFT (samples)
    FFT_WINDOW_SIZE = 4096
    # Hop length (samples)
    HOP_LENGTH = 2048
    # Threshold for peak detection (dB)
    PEAK_THRESHOLD = -20  # Increased sensitivity significantly
    # Size of the maximum filter for peak detection
    MAX_FILTER_SIZE = 7  # Increased sensitivity significantly

    # Target zone size for fingerprinting
    TARGET_ZONE_SIZE = 10
    # Number of parallel processes to use
    NUM_PROCESSES = os.cpu_count()
    # Min hashes required to be a match
    MIN_HASHES = 5
    # Time to live for fingerprint caching
    FINGERPRINT_CACHE_TTL = 60 * 60  # 1 hour
    LOG_FILE = "log"


config = Config()
