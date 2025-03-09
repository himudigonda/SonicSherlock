import click
from audio import processing
from audio import fingerprinting
from database.database_manager import DatabaseManager
from database.models import Song, Fingerprint  # Import models
from utils.logger import logger


@click.group()
def cli():
    pass


@cli.command()
@click.argument("title")
@click.argument("artist")
def add_song(title, artist):
    """Adds a song to the database."""
    logger.info(f"cli.add_song :: Adding song: Title={title}, Artist={artist}")
    db_manager = DatabaseManager()
    song_id = db_manager.add_song(title, artist)
    if song_id:
        click.echo(f"Song added successfully with ID: {song_id}")
    else:
        click.echo("Failed to add song.")


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("song_id", type=int)
def fingerprint_song(file_path, song_id):
    """Fingerprints a song and stores the fingerprints in the database."""
    logger.info(
        f"cli.fingerprint_song :: Fingerprinting song: FilePath={file_path}, SongID={song_id}"
    )
    db_manager = DatabaseManager()
    # Load the audio
    audio, sr = processing.load_audio(file_path)
    if audio is None:
        click.echo("Failed to load audio.")
        return

    # Create spectrogram
    spectrogram = processing.create_spectrogram(audio)
    if spectrogram is None:
        click.echo("Failed to create spectrogram.")
        return

    # Extract peaks
    peaks = processing.extract_peaks(spectrogram)

    # Create fingerprints
    fingerprints = fingerprinting.create_fingerprint(peaks, song_id)

    # Store the fingerprints
    db_manager.store_fingerprints(fingerprints)
    click.echo(f"Fingerprinted {len(fingerprints)} for song ID {song_id}")


@cli.command()
def clear_database():
    """Clears all songs and fingerprints from the database."""
    logger.info(
        "cli.clear_database :: Clearing all songs and fingerprints from the database"
    )
    db_manager = DatabaseManager()
    session = db_manager.Session()  # Get a session
    try:
        # Delete all fingerprints
        num_fingerprints_deleted = session.query(Fingerprint).delete()
        logger.info(
            f"cli.clear_database :: Deleted {num_fingerprints_deleted} fingerprints"
        )
        # Delete all songs
        num_songs_deleted = session.query(Song).delete()
        logger.info(f"cli.clear_database :: Deleted {num_songs_deleted} songs")
        session.commit()
        click.echo("Successfully cleared all songs and fingerprints from the database.")
    except Exception as e:
        session.rollback()
        logger.error(f"cli.clear_database :: Error clearing database: {e}")
        click.echo(f"Error clearing database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    cli()
