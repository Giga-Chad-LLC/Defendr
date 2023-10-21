from pydantic import BaseModel
from typing import List


class UserDto(BaseModel):
    email: str
    password: str


# API route responses
class UserResponse(BaseModel):
    id: int
    email: str

class UsersResponse(BaseModel):
    users: List[UserResponse]
