from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserSession:
    user_id: UUID
    created_at: datetime
    last_seen_at: datetime
