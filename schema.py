from pydantic import BaseModel
from typing import Optional
class Message(BaseModel):
    msg: str
    socket_id: Optional[str] = None 