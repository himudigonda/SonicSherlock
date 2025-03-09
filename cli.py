import click
from audio import processing
from audio import fingerprinting
from database.database_manager import DatabaseManager
from utils.logger import logger

@click.group()
def cli():
    pass

@cli.command()
@click.argument('title')
@click.argument('artist')
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
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('song_id', type=int)
def fingerprint_song(file_path, song_id):
    """Fingerprints a song and stores the fingerprints in the database."""
    logger.info(f"cli.fingerprint_song :: Fingerprinting song: FilePath={file_path}, SongID={song_id}")
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


if __name__ == '__main__':
    cli()
