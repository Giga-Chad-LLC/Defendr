from pydantic import BaseModel
from typing import List


class SearchResult(BaseModel):
    label: str
    value: str

# API route responses
class SearchResultsResponse(BaseModel):
    results: List[SearchResult]
