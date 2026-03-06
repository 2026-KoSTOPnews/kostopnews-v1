from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

class UserSession(BaseModel):
    user_id: UUID
    created_at: datetime
    last_seen_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2용 (v1은 orm_mode=True)
