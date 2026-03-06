from app.infrastructure.db.session import SessionLocal

def get_db():
    db = SessionLocal()

    try:
        yield db  # <-- yield를 쓰면 generator를 반환
    finally:
        db.close()