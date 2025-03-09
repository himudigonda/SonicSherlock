from pydantic import BaseModel


class SongCreate(BaseModel):
    title: str
    artist: str


class SongResponse(BaseModel):
    id: int
    title: str
    artist: str


class RecognitionResponse(BaseModel):
    song_id: int | None
    title: str | None
    artist: str | None
