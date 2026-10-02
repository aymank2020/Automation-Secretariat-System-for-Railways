import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from app.db.database import SessionLocal, init_db
from app.models import User
from app.core.security import hash_password
from app.core.config import settings

init_db()
db = SessionLocal()
if db.query(User).count() == 0 and settings.INITIAL_ADMIN_PASSWORD:
    db.add(User(username=settings.INITIAL_ADMIN_USERNAME, full_name="المدير العام", seclevel="admin", password=hash_password(settings.INITIAL_ADMIN_PASSWORD)))
    db.commit()
    print("Configured initial administrator created")
else:
    print("No user added: users exist or INITIAL_ADMIN_PASSWORD is not configured")
db.close()
