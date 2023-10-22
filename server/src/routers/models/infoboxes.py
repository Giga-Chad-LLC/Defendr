from pydantic import BaseModel
from typing import List, Dict, Any, Union


class InfoboxDto(BaseModel):
    user_id: int
    directory_id: Union[int, None]
    fields: Dict[str, Any]


# API route response
class InfoboxResponse(BaseModel):
    id: int
    user_id: int
    directory_id: Union[int, None]
    icon: str
    title: str
    layout: str
    fields: Dict[str, dict]


class InfoboxesResponse(BaseModel):
    infoboxes: List[InfoboxResponse]
