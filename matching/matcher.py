from collections import defaultdict
from config import config
from utils.logger import logger
from database.database_manager import DatabaseManager


def match_fingerprints(query_fingerprints):
    """Matches query fingerprints against the database.

    Args:
        query_fingerprints (list): A list of fingerprint hashes from the query audio.

    Returns:
        dict: A dictionary mapping song IDs to match counts.
    """
    logger.debug(
        f"matching.matcher.match_fingerprints :: Matching {len(query_fingerprints)} query fingerprints"
    )
    db_manager = DatabaseManager()
    matches = defaultdict(int)
    try:
        for fingerprint_data in query_fingerprints:
            fingerprint_hash = fingerprint_data["hash"]
            database_fingerprints = db_manager.get_fingerprints_by_hash(
                fingerprint_hash
            )

            if database_fingerprints:
                logger.debug(
                    f"matching.matcher.match_fingerprints :: Found {len(database_fingerprints)} matching fingerprints for hash {fingerprint_hash}"
                )
                for db_fingerprint in database_fingerprints:
                    # Calculate the offset difference
                    offset_difference = (
                        db_fingerprint.offset - fingerprint_data["offset"]
                    )
                    # Combine song ID and offset difference to identify a match
                    match_key = (db_fingerprint.song_id, offset_difference)
                    matches[match_key] += 1
            else:
                logger.debug(
                    f"matching.matcher.match_fingerprints :: No matching fingerprints found for hash {fingerprint_hash}"
                )

        logger.debug(
            f"matching.matcher.match_fingerprints :: Found matches for song IDs: {matches.keys()}"
        )
        return matches
    except Exception as e:
        logger.error(
            f"matching.matcher.match_fingerprints :: Error matching fingerprints: {e}"
        )
        return {}


def get_best_match(matches):
    """Determines the best match from the matches dictionary.

    Args:
        matches (dict): A dictionary mapping (song_id, offset_difference) tuples to match counts.

    Returns:
        tuple: A tuple containing the song ID and the offset difference of the best match,
               or (None, None) if no match is found.
    """
    logger.debug("matching.matcher.get_best_match :: Determining the best match")
    try:
        if not matches:
            logger.info("matching.matcher.get_best_match :: No matches found")
            return None, None

        # Sort the matches by count (number of matching fingerprints)
        best_match_key = max(matches, key=matches.get)
        song_id, offset_difference = best_match_key

        # Filter matches based on a minimum number of matching fingerprints
        if matches[best_match_key] < config.MIN_HASHES:
            logger.info(
                f"matching.matcher.get_best_match :: Best match count ({matches[best_match_key]}) is less than the minimum required ({config.MIN_HASHES})"
            )
            return None, None

        logger.info(
            f"matching.matcher.get_best_match :: Best match found: Song ID={song_id}, Offset Difference={offset_difference}, Count={matches[best_match_key]}"
        )
        return song_id, offset_difference
    except Exception as e:
        logger.error(
            f"matching.matcher.get_best_match :: Error determining best match: {e}"
        )
        return None, None
