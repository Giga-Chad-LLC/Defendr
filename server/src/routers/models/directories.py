from pydantic import BaseModel
from typing import List



class DirectoryDto(BaseModel):
    user_id: int
    title: str
    icon: str

# API route responses
class DirectoryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    icon: str


class DirectoriesResponse(BaseModel):
    directories: List[DirectoryResponse]
