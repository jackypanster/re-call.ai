from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    email: str
    created_at: datetime
    settings: Optional[Dict] = {}
