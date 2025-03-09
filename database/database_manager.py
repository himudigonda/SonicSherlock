from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config
from utils.logger import logger
from database.models import Base, Song, Fingerprint


class DatabaseManager:
    def __init__(self):
        logger.debug(
            "database.database_manager.DatabaseManager :: Initializing DatabaseManager"
        )
        try:
            self.engine = create_engine(config.DATABASE_URL)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            logger.debug(
                "database.database_manager.DatabaseManager :: Database connection established"
            )
        except Exception as e:
            logger.critical(
                f"database.database_manager.DatabaseManager :: Failed to connect to database: {e}"
            )
            raise  # Re-raise the exception to prevent the application from starting

    def add_song(self, title, artist):
        """Adds a new song to the database.

        Args:
            title (str): The title of the song.
            artist (str): The artist of the song.

        Returns:
            int: The ID of the newly added song.
        """
        logger.debug(
            f"database.database_manager.DatabaseManager :: Adding song: Title={title}, Artist={artist}"
        )
        session = self.Session()
        try:
            song = Song(title=title, artist=artist)
            session.add(song)
            session.commit()
            logger.debug(
                f"database.database_manager.DatabaseManager :: Song added successfully. Song ID: {song.id}"
            )
            return song.id
        except Exception as e:
            session.rollback()
            logger.error(
                f"database.database_manager.DatabaseManager :: Error adding song: {e}"
            )
            return None
        finally:
            session.close()

    def store_fingerprints(self, fingerprints):
        """Stores a list of fingerprints in the database.

        Args:
            fingerprints (list): A list of fingerprint dictionaries.
        """
        logger.debug(
            f"database.database_manager.DatabaseManager :: Storing {len(fingerprints)} fingerprints"
        )
        session = self.Session()
        try:
            for fingerprint_data in fingerprints:
                # Convert 'offset' to a standard Python integer
                fingerprint_data["offset"] = int(fingerprint_data["offset"])
                fingerprint = Fingerprint(**fingerprint_data)
                session.add(fingerprint)
            session.commit()
            logger.debug(
                "database.database_manager.DatabaseManager :: Fingerprints stored successfully"
            )
        except Exception as e:
            session.rollback()
            logger.error(
                f"database.database_manager.DatabaseManager :: Error storing fingerprints: {e}"
            )
        finally:
            session.close()

    def get_song_by_id(self, song_id):
        """Retrieves a song from the database by its ID.

        Args:
            song_id (int): The ID of the song to retrieve.

        Returns:
            Song: The Song object if found, None otherwise.
        """
        logger.debug(
            f"database.database_manager.DatabaseManager :: Retrieving song with ID: {song_id}"
        )
        session = self.Session()
        try:
            song = session.query(Song).filter(Song.id == song_id).first()
            if song:
                logger.debug(
                    f"database.database_manager.DatabaseManager :: Song found: {song}"
                )
            else:
                logger.debug(
                    f"database.database_manager.DatabaseManager :: Song with ID {song_id} not found"
                )
            return song
        except Exception as e:
            logger.error(
                f"database.database_manager.DatabaseManager :: Error retrieving song: {e}"
            )
            return None
        finally:
            session.close()

    def get_fingerprints_by_hash(self, hash_value):
        """Retrieves fingerprints from the database by their hash value.

        Args:
            hash_value (str): The hash value to search for.

        Returns:
            list: A list of Fingerprint objects matching the hash value.
        """
        logger.debug(
            f"database.database_manager.DatabaseManager :: Retrieving fingerprints with hash: {hash_value}"
        )
        session = self.Session()
        try:
            fingerprints = (
                session.query(Fingerprint).filter(Fingerprint.hash == hash_value).all()
            )
            logger.debug(
                f"database.database_manager.DatabaseManager :: Found {len(fingerprints)} fingerprints with hash {hash_value}"
            )
            return fingerprints
        except Exception as e:
            logger.error(
                f"database.database_manager.DatabaseManager :: Error retrieving fingerprints: {e}"
            )
            return []
        finally:
            session.close()
