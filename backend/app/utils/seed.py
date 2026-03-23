"""
Database seeder — run with:
    python -m app.utils.seed
from the backend/ directory.
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
        # ── Admin user ────────────────────────────────────────────────────────
        admin = db.query(User).filter(User.email == "admin@studyhub.com").first()
        if not admin:
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
            print("✓ Admin created: admin@studyhub.com / Admin123")
        else:
            print("  Admin already exists, skipping.")

        # ── Demo user ─────────────────────────────────────────────────────────
        demo = db.query(User).filter(User.email == "demo@studyhub.com").first()
        if not demo:
            demo = User(
                email="demo@studyhub.com",
                password=hash_password("Demo1234"),
                name="Demo Student",
                is_active=True,
            )
            db.add(demo)
            db.flush()
            db.add(Subscription(user_id=demo.id, plan="free", status="active"))

            # Sample chats
            for tool, sample_q, sample_a in [
                (
                    "study_assistant",
                    "Can you explain photosynthesis?",
                    "Photosynthesis is the process by which plants convert light energy into chemical energy...",
                ),
                (
                    "plagiarism",
                    "Please check my essay for plagiarism.",
                    "**Originality Score: 92%** — Your writing is highly original!",
                ),
                (
                    "cv_generator",
                    "Help me create a CV for a software engineering role.",
                    "**Professional CV Generated** — See the full CV below...",
                ),
            ]:
                chat = Chat(user_id=demo.id, tool=tool, title=sample_q[:50])
                db.add(chat)
                db.flush()
                db.add(Message(chat_id=chat.id, user_id=demo.id, role="user", content=sample_q))
                db.add(Message(chat_id=chat.id, user_id=demo.id, role="assistant", content=sample_a))

            print("✓ Demo user created: demo@studyhub.com / Demo1234")
        else:
            print("  Demo user already exists, skipping.")

        db.commit()
        print("\n✅ Seeding complete!")
        print("\nDemo credentials:")
        print("  Admin : admin@studyhub.com  /  Admin123")
        print("  User  : demo@studyhub.com   /  Demo1234")

    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
