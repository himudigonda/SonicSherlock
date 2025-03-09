import os
import re  # Import the regular expression module
import click
from audio import processing
from audio import fingerprinting
from database.database_manager import DatabaseManager
from database.models import Song
from sqlalchemy import func
from utils.logger import logger


def extract_artist_title(filename):
    """Extracts the artist and title from the filename.
    Assumes the filename is in the format "Artist - Title.mp3" or "Artist, Title.mp3".
    Handles filenames with multiple hyphens or commas.

    Args:
        filename (str): The name of the audio file.

    Returns:
        tuple: A tuple containing the artist and title, or (None, None) if extraction fails.
    """
    try:
        # Use regex to split the filename by either " - " or ", "
        match = re.split(r" - |, ", filename, maxsplit=1)

        if len(match) == 2:
            artist = match[0].strip()
            title = match[1].replace(".mp3", "").strip()  # Remove the .mp3 extension
            return artist, title
        else:
            logger.warning(f"Could not split filename {filename} into artist and title")
            return None, None

    except Exception as e:
        logger.error(f"Error extracting artist and title from filename: {e}")
        return None, None


@click.command()
@click.option(
    "--songs-dir", default="songs", help="Path to the directory containing the songs."
)
def add_and_fingerprint_songs(songs_dir):
    """Adds songs from the specified directory to the database and fingerprints them."""
    logger.info(f"Adding and fingerprinting songs from directory: {songs_dir}")
    db_manager = DatabaseManager()
    session = db_manager.Session()  # Get the session here

    song_files = [f for f in os.listdir(songs_dir) if f.endswith(".mp3")]

    if not song_files:
        logger.warning(f"No .mp3 files found in the directory: {songs_dir}")
        click.echo(f"No .mp3 files found in the directory: {songs_dir}")
        return

    for song_file in song_files:
        # Split the filename to extract the artist and song title
        file_path = os.path.join(songs_dir, song_file)
        artist, title = extract_artist_title(song_file)

        if artist and title:
            logger.info(f"Processing song: {title} - {artist}")

            # Check if the song already exists in the database based on title and artist
            existing_song = (
                session.query(Song)
                .filter(
                    func.lower(Song.title) == title.lower(),
                    func.lower(Song.artist) == artist.lower(),
                )
                .first()
            )

            if existing_song:
                logger.info(
                    f"Song '{title}' by '{artist}' already exists in the database with ID: {existing_song.id}. Skipping."
                )
                click.echo(
                    f"Song '{title}' by '{artist}' already exists in the database. Skipping."
                )
                continue  # Skip to the next song

            # Add the song to the database
            song_id = db_manager.add_song(title, artist)
            if song_id:
                logger.info(
                    f"Added song '{title}' by '{artist}' to the database with ID: {song_id}"
                )

                # Fingerprint the song
                # Load the audio
                audio, sr = processing.load_audio(file_path)
                if audio is None:
                    logger.error(f"Failed to load audio for {file_path}")
                    click.echo(f"Failed to load audio for {file_path}")
                    continue

                # Create spectrogram
                spectrogram = processing.create_spectrogram(audio)
                if spectrogram is None:
                    logger.error(f"Failed to create spectrogram for {file_path}")
                    click.echo(f"Failed to create spectrogram for {file_path}")
                    continue

                # Extract peaks
                peaks = processing.extract_peaks(spectrogram)

                # Create fingerprints
                fingerprints = fingerprinting.create_fingerprint(peaks, song_id)

                # Store the fingerprints
                db_manager.store_fingerprints(fingerprints)
                logger.info(f"Fingerprinted {len(fingerprints)} for song ID {song_id}")
                click.echo(f"Fingerprinted {len(fingerprints)} for song ID {song_id}")

            else:
                logger.error(
                    f"Failed to add song '{title}' by '{artist}' to the database."
                )
                click.echo(
                    f"Failed to add song '{title}' by '{artist}' to the database."
                )
        else:
            logger.warning(
                f"Could not extract artist and title from filename: {song_file}"
            )
            click.echo(f"Could not extract artist and title from filename: {song_file}")
    session.close()  # Close the session


if __name__ == "__main__":
    add_and_fingerprint_songs()
