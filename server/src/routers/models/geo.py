from pydantic import BaseModel


class GeoDto(BaseModel):
    latitude: float
    longitude: float

# API route responses
class GeoResponse(BaseModel):
    geo: GeoDto
    ip: str
