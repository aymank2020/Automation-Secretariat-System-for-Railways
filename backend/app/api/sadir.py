from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import os
import uuid

from app.db.database import get_db
from app.models import Sadir, User
from app.schemas import SadirCreate, SadirUpdate, SadirResponse, SadirListResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/sadir", tags=["Sadir"])

UPLOAD_DIR = "uploads/sadir"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=SadirResponse)
async def create_sadir(
    sadir: SadirCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """إنشاء صادر جديد"""
    # التحقق من عدم تكرار رقم القيد
    existing = db.query(Sadir).filter(Sadir.qaid_number == sadir.qaid_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="رقم القيد موجود مسبقاً")
    
    db_sadir = Sadir(**sadir.model_dump(), created_by=current_user.id)
    db.add(db_sadir)
    db.commit()
    db.refresh(db_sadir)
    return db_sadir


@router.get("/", response_model=List[SadirListResponse])
async def list_sadir(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    qaid_number: Optional[str] = None,
    subject: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """قائمة الصادر مع إمكانية التصفية"""
    query = db.query(Sadir)
    
    if qaid_number:
        query = query.filter(Sadir.qaid_number.contains(qaid_number))
    if subject:
        query = query.filter(Sadir.subject.contains(subject))
    if date_from:
        query = query.filter(Sadir.qaid_date >= date_from)
    if date_to:
        query = query.filter(Sadir.qaid_date <= date_to)
    
    return query.order_by(Sadir.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/search", response_model=List[SadirListResponse])
async def search_sadir(
    q: str = Query(..., min_length=2, description="نص البحث"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """البحث في الصادر"""
    return db.query(Sadir).filter(
        (Sadir.qaid_number.contains(q)) |
        (Sadir.letter_number.contains(q)) |
        (Sadir.subject.contains(q)) |
        (Sadir.source_administration.contains(q)) |
        (Sadir.exported_to.contains(q))
    ).order_by(Sadir.created_at.desc()).limit(50).all()


@router.get("/{sadir_id}", response_model=SadirResponse)
async def get_sadir(
    sadir_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """الحصول على تفاصيل صادر"""
    sadir = db.query(Sadir).filter(Sadir.id == sadir_id).first()
    if not sadir:
        raise HTTPException(status_code=404, detail="الصادر غير موجود")
    return sadir


@router.put("/{sadir_id}", response_model=SadirResponse)
async def update_sadir(
    sadir_id: int,
    sadir_update: SadirUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """تحديث صادر"""
    db_sadir = db.query(Sadir).filter(Sadir.id == sadir_id).first()
    if not db_sadir:
        raise HTTPException(status_code=404, detail="الصادر غير موجود")
    
    update_data = sadir_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sadir, field, value)
    
    db.commit()
    db.refresh(db_sadir)
    return db_sadir


@router.delete("/{sadir_id}")
async def delete_sadir(
    sadir_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف صادر"""
    db_sadir = db.query(Sadir).filter(Sadir.id == sadir_id).first()
    if not db_sadir:
        raise HTTPException(status_code=404, detail="الصادر غير موجود")
    
    # حذف الملف المرفق إذا وجد
    if db_sadir.attachment_path and os.path.exists(db_sadir.attachment_path):
        os.remove(db_sadir.attachment_path)
    
    db.delete(db_sadir)
    db.commit()
    return {"message": "تم الحذف بنجاح"}


@router.post("/{sadir_id}/upload")
async def upload_attachment(
    sadir_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """رفع ملف مرفق للصادر"""
    db_sadir = db.query(Sadir).filter(Sadir.id == sadir_id).first()
    if not db_sadir:
        raise HTTPException(status_code=404, detail="الصادر غير موجود")
    
    # التحقق من نوع الملف
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="نوع الملف غير مسموح به")
    
    # إنشاء اسم فريد للملف
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # حفظ الملف
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # تحديث سجل الصادر
    db_sadir.attachment_path = file_path
    db_sadir.attachment_name = file.filename
    db.commit()
    db.refresh(db_sadir)
    
    return {
        "message": "تم رفع الملف بنجاح",
        "file_path": file_path,
        "file_name": file.filename
    }


@router.get("/stats/summary")
async def get_sadir_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """إحصائيات الصادر"""
    total = db.query(Sadir).count()
    pending = db.query(Sadir).filter(Sadir.signature_status == 'pending').count()
    saved = db.query(Sadir).filter(Sadir.signature_status == 'saved').count()
    needs_followup = db.query(Sadir).filter(Sadir.needs_followup == True).count()
    signed_by_chief = db.query(Sadir).filter(Sadir.signed_by_chief == True).count()
    
    return {
        "total": total,
        "pending": pending,
        "saved": saved,
        "needs_followup": needs_followup,
        "signed_by_chief": signed_by_chief
    }
