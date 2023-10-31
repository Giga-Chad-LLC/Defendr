from pydantic import BaseModel
from typing import List, Dict, Any, Union


available_infobox_layouts = {
    "ONLINE_SERVICE": 'ONLINE_SERVICE',
    "INTERNATIONAL_PASSPORT": 'INTERNATIONAL_PASSPORT',
    "BANK_CARD": 'BANK_CARD',
}

available_field_types = {
    "selection": "SELECTION",
    "text": "TEXT"
}


class InfoboxDto(BaseModel):
    user_id: int
    directory_id: Union[int, None]
    fields: Dict[str, Any]


# API route response
class InfoboxResponse(BaseModel):
    infobox_id: int
    infobox_user_id: int
    infobox_directory_id: Union[int, None]
    infobox_title: str
    infobox_icon: str
    infobox_layout: str
    field_id: int
    field_label: str
    field_type: str
    text_field_value: Union[str, None]
    selection_field_id: Union[int, None]
    option_label: Union[str, None]
    option_selected: Union[bool, None]



class InfoboxesResponse(BaseModel):
    infoboxes: List[InfoboxResponse]


