
def get_db():
    from database import SessionLocal
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def return_db():
    from database import SessionLocal
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()
