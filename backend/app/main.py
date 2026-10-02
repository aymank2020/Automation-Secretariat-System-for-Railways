from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.db.database import init_db, SessionLocal
from app.api import auth, documents, users, warid, sadir, import_excel
from app.core.config import settings

app = FastAPI(title="Railways HR System API", version="2.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# إنشاء مجلدات التحميل
os.makedirs("uploads/warid", exist_ok=True)
os.makedirs("uploads/sadir", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# تقديم الملفات المرفقة
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(users.router)
app.include_router(warid.router)
app.include_router(sadir.router)
app.include_router(import_excel.router)


@app.on_event("startup")
def startup_event():
    init_db()
    from app.models import User
    from app.core.security import hash_password
    db = SessionLocal()
    try:
        if db.query(User).count() == 0 and settings.INITIAL_ADMIN_PASSWORD:
            db.add(User(username=settings.INITIAL_ADMIN_USERNAME, full_name="المدير العام", seclevel="admin", password=hash_password(settings.INITIAL_ADMIN_PASSWORD)))
            db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Railways HR System API", "status": "running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}
