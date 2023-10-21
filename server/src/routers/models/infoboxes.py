from pydantic import BaseModel
from typing import List


class InfoboxDto(BaseModel):
    user_id: int
    directory_id: int | None
    icon: str
    title: str
    layout: str


# API route response
class InfoboxResponse(BaseModel):
    id: int
    user_id: int
    directory_id: int | None
    icon: str
    title: str
    layout: str

class InfoboxesResponse(BaseModel):
    infoboxes: List[InfoboxResponse]
