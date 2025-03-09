from config import config
from utils.logger import logger
import hashlib


def create_fingerprint(peaks, song_id):
    """Creates audio fingerprints from a list of peaks.

    Args:
        peaks (list): A list of (time, frequency) tuples.
        song_id (int): The ID of the song.

    Returns:
        list: A list of fingerprint hashes.
    """
    logger.debug(
        f"audio.fingerprinting.create_fingerprint :: Creating fingerprints for song ID {song_id} with {len(peaks)} peaks"
    )
    fingerprints = []
    try:
        for i in range(len(peaks)):
            anchor_time, anchor_freq = peaks[i]
            for j in range(1, min(config.TARGET_ZONE_SIZE + 1, len(peaks) - i)):
                target_time, target_freq = peaks[i + j]
                delta_time = target_time - anchor_time
                # Create a hash from the frequency and time differences
                hash_str = f"{anchor_freq}:{target_freq}:{delta_time}"
                # Use hashlib for a more robust and consistent hash (SHA-256)
                fingerprint_hash = hashlib.sha256(hash_str.encode()).hexdigest()
                fingerprints.append(
                    {
                        "hash": fingerprint_hash,
                        "song_id": song_id,
                        "offset": anchor_time,
                    }
                )
        logger.debug(
            f"audio.fingerprinting.create_fingerprint :: Created {len(fingerprints)} fingerprints."
        )
        return fingerprints
    except Exception as e:
        logger.error(
            f"audio.fingerprinting.create_fingerprint :: Error creating fingerprints: {e}"
        )
        return []
