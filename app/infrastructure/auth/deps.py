from fastapi import Header, Depends
from uuid import UUID
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from app.infrastructure.db.deps import get_db
from app.infrastructure.db.models.user_session_entity import UserSessionEntity

SESSION_EXPIRE_DAYS = 31

def get_current_user_id(
    x_user_id: UUID = Header(..., alias="X-User-Id"),
    db=Depends(get_db),
) -> UUID:
    session = (db.query(UserSessionEntity)
               .filter(UserSessionEntity.user_id == str(x_user_id))
               .first())

    now = datetime.now(timezone.utc)

    # 1️⃣ 최초 접속
    if not session:
        entity = UserSessionEntity(
            user_id=str(x_user_id),
            created_at=now,
            last_seen_at=now,
        )
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return x_user_id

    # 2️⃣ 만료 체크
    if session.last_seen_at < now - timedelta(days=SESSION_EXPIRE_DAYS):
        entity = (
            db.query(UserSessionEntity)
            .filter(UserSessionEntity.user_id == str(x_user_id))
            .first()
        )
        if entity:
            db.delete(entity)
            db.commit()
        raise HTTPException(status_code=401, detail="Session expired")

    # 3️⃣ 정상 → last_seen 갱신
    session.last_seen_at = now
    db.commit()

    return x_user_id