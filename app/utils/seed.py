"""
Seed the database with demo users.
Run from repo root: python -m app.utils.seed
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.database import SessionLocal, engine
from app.core.security import hash_password
from app.models import User, Subscription, Chat, Message
from app.core.database import Base


def seed():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Admin user
        if not db.query(User).filter(User.email == "admin@studyhub.com").first():
            admin = User(
                email="admin@studyhub.com",
                password=hash_password("Admin123"),
                name="Admin",
                is_admin=True,
                is_active=True,
            )
            db.add(admin)
            db.flush()
            db.add(Subscription(user_id=admin.id, plan="free", status="active"))
            print("✓ Admin: admin@studyhub.com / Admin123")

        # Demo user
        if not db.query(User).filter(User.email == "demo@studyhub.com").first():
            demo = User(
                email="demo@studyhub.com",
                password=hash_password("Demo1234"),
                name="Demo Student",
                is_active=True,
            )
            db.add(demo)
            db.flush()
            db.add(Subscription(user_id=demo.id, plan="free", status="active"))

            for tool, q, a in [
                ("study_assistant", "Can you explain photosynthesis?",
                 "Photosynthesis converts light energy into chemical energy stored in glucose..."),
                ("plagiarism", "Check my essay for plagiarism.",
                 "**Originality Score: 92%** — Your writing is highly original!"),
                ("cv_generator", "Help me create a CV.",
                 "**Professional CV Generated** — See the full CV below..."),
            ]:
                chat = Chat(user_id=demo.id, tool=tool, title=q[:50])
                db.add(chat)
                db.flush()
                db.add(Message(chat_id=chat.id, user_id=demo.id, role="user", content=q))
                db.add(Message(chat_id=chat.id, user_id=demo.id, role="assistant", content=a))

            print("✓ Demo: demo@studyhub.com / Demo1234")

        db.commit()
        print("\n✅ Seeding complete!")
    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
