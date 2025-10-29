
from sqlmodel import Session, select
from .db import engine, init_db
from .models import User, Role
from .auth import get_password_hash

def ensure_user(session: Session, email: str, password: str, role: str, full_name: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        user = User(email=email, hashed_password=get_password_hash(password), role=role, full_name=full_name)
        session.add(user)
        session.commit()
        print(f"Created user: {email} ({role})")
    else:
        print(f"User exists: {email}")
    return user

def main():
    init_db()
    with Session(engine) as session:
        ensure_user(session, "admin2@example.com", "admin2", Role.ADMIN_2, "Admin Dos")
        ensure_user(session, "admin1@example.com", "admin1", Role.ADMIN_1, "Admin Uno")
        ensure_user(session, "cliente@example.com", "cliente", Role.CLIENTE, "Cliente Demo")

if __name__ == "__main__":
    main()
