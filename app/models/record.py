from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class Record(BaseModel):
    id: str
    content: str
    summary: Optional[str] = None
    keywords: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    embedding_id: Optional[str] = None
    user_id: str
    created_at: datetime
    updated_at: datetime
