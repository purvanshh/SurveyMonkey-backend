"""
Pydantic schemas for Collectors.
"""

from pydantic import BaseModel
from typing import List


class CollectorResponse(BaseModel):
    collector_name: str
    share_url: str
    status: str
    responses: int
    date_modified: str


class CollectorListResponse(BaseModel):
    collectors: List[CollectorResponse]
    total_responses: int
