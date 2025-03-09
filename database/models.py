from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, Identity(), primary_key=True)
    title = Column(String)
    artist = Column(String)

    def __repr__(self):
        return f"<Song(title='{self.title}', artist='{self.artist}')>"


class Fingerprint(Base):
    __tablename__ = "fingerprints"

    id = Column(Integer, Identity(), primary_key=True)
    hash = Column(String)
    song_id = Column(Integer)
    offset = Column(Integer)

    def __repr__(self):
        return f"<Fingerprint(hash='{self.hash}', song_id={self.song_id}, offset={self.offset})>"
