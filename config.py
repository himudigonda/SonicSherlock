import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True  # Enable debug logging


class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/sonic_sherlock"
    )
    # Sample rate for audio processing (Hz)
    SAMPLE_RATE = 44000
    # Frame length for FFT (samples)
    FFT_WINDOW_SIZE = 2048  # Reduced for faster processing
    # Hop length (samples)
    HOP_LENGTH = 1024  # Increased for faster processing
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
    # Number of Fingerprints to use
    NUM_FINGERPRINTS_TO_USE = 100


config = Config()
