from pydantic import BaseModel


class AudioResponse(BaseModel):
    genre: str
    confidence: float
    