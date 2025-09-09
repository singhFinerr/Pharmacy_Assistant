from pydantic import BaseModel
from typing import Optional, Dict

class Query(BaseModel):
    text: str

class Response(BaseModel):
    response: str
    patient: Optional[Dict] = None
