from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import os
import uuid

from app.db.database import get_db
from app.models import Warid, User
from app.schemas import WaridCreate, WaridUpdate, WaridResponse, WaridListResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/warid", tags=["Warid"])

UPLOAD_DIR = "uploads/warid"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=WaridResponse)
async def create_warid(
    warid: WaridCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """إنشاء وارد جديد"""
    # التحقق من عدم تكرار رقم القيد
    existing = db.query(Warid).filter(Warid.qaid_number == warid.qaid_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="رقم القيد موجود مسبقاً")
    
    db_warid = Warid(**warid.model_dump(), created_by=current_user.id)
    db.add(db_warid)
    db.commit()
    db.refresh(db_warid)
    return db_warid


@router.get("/", response_model=List[WaridListResponse])
async def list_warid(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    qaid_number: Optional[str] = None,
    subject: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """قائمة الوارد مع إمكانية التصفية"""
    query = db.query(Warid)
    
    if qaid_number:
        query = query.filter(Warid.qaid_number.contains(qaid_number))
    if subject:
        query = query.filter(Warid.subject.contains(subject))
    if date_from:
        query = query.filter(Warid.qaid_date >= date_from)
    if date_to:
        query = query.filter(Warid.qaid_date <= date_to)
    
    return query.order_by(Warid.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/search", response_model=List[WaridListResponse])
async def search_warid(
    q: str = Query(..., min_length=2, description="نص البحث"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """البحث في الوارد"""
    return db.query(Warid).filter(
        (Warid.qaid_number.contains(q)) |
        (Warid.warid_number.contains(q)) |
        (Warid.subject.contains(q)) |
        (Warid.source_entity.contains(q)) |
        (Warid.warid_from.contains(q))
    ).order_by(Warid.created_at.desc()).limit(50).all()


@router.get("/{warid_id}", response_model=WaridResponse)
async def get_warid(
    warid_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """الحصول على تفاصيل وارد"""
    warid = db.query(Warid).filter(Warid.id == warid_id).first()
    if not warid:
        raise HTTPException(status_code=404, detail="الوارد غير موجود")
    return warid


@router.put("/{warid_id}", response_model=WaridResponse)
async def update_warid(
    warid_id: int,
    warid_update: WaridUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """تحديث وارد"""
    db_warid = db.query(Warid).filter(Warid.id == warid_id).first()
    if not db_warid:
        raise HTTPException(status_code=404, detail="الوارد غير موجود")
    
    update_data = warid_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_warid, field, value)
    
    db.commit()
    db.refresh(db_warid)
    return db_warid


@router.delete("/{warid_id}")
async def delete_warid(
    warid_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """حذف وارد"""
    db_warid = db.query(Warid).filter(Warid.id == warid_id).first()
    if not db_warid:
        raise HTTPException(status_code=404, detail="الوارد غير موجود")
    
    # حذف الملف المرفق إذا وجد
    if db_warid.attachment_path and os.path.exists(db_warid.attachment_path):
        os.remove(db_warid.attachment_path)
    
    db.delete(db_warid)
    db.commit()
    return {"message": "تم الحذف بنجاح"}


@router.post("/{warid_id}/upload")
async def upload_attachment(
    warid_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """رفع ملف مرفق للوارد"""
    db_warid = db.query(Warid).filter(Warid.id == warid_id).first()
    if not db_warid:
        raise HTTPException(status_code=404, detail="الوارد غير موجود")
    
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
    
    # تحديث سجل الوارد
    db_warid.attachment_path = file_path
    db_warid.attachment_name = file.filename
    db.commit()
    db.refresh(db_warid)
    
    return {
        "message": "تم رفع الملف بنجاح",
        "file_path": file_path,
        "file_name": file.filename
    }


@router.get("/stats/summary")
async def get_warid_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """إحصائيات الوارد"""
    total = db.query(Warid).count()
    pending = db.query(Warid).filter(Warid.signature_status == 'pending').count()
    saved = db.query(Warid).filter(Warid.signature_status == 'saved').count()
    needs_followup = db.query(Warid).filter(Warid.needs_followup == True).count()
    
    return {
        "total": total,
        "pending": pending,
        "saved": saved,
        "needs_followup": needs_followup
    }
