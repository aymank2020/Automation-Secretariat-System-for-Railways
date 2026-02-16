from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import pandas as pd
import os

from app.db.database import get_db
from app.models import Warid, Sadir, User
from app.schemas import ImportResponse, ImportPreview
from app.core.security import get_current_user

router = APIRouter(prefix="/import", tags=["Import"])


@router.post("/warid/preview", response_model=ImportPreview)
async def preview_warid_excel(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """معاينة بيانات ملف Excel قبل الاستيراد"""
    
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="يجب أن يكون الملف بصيغة Excel أو CSV")
    
    try:
        # قراءة ملف Excel
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
        
        # تحويل الأعمدة إلى نص
        df.columns = [str(col).strip() for col in df.columns]
        
        # عرض أول 5 صفوف فقط
        preview_data = df.head(5).fillna('').to_dict('records')
        
        return ImportPreview(
            total_rows=len(df),
            preview_data=preview_data,
            columns=df.columns.tolist()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في قراءة الملف: {str(e)}")


@router.post("/warid", response_model=ImportResponse)
async def import_warid_excel(
    file: UploadFile = File(...),
    column_mapping: Optional[str] = Query(None, description="JSON mapping للأعمدة"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """استيراد بيانات الوارد من ملف Excel"""
    
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="يجب أن يكون الملف بصيغة Excel أو CSV")
    
    try:
        # قراءة ملف Excel
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
        
        # تحويل الأعمدة إلى نص
        df.columns = [str(col).strip() for col in df.columns]
        
        # تعيين الأعمدة الافتراضية
        default_mapping = {
            'م': 'serial',
            'النائب': 'deputy',
            'الوزارة': 'ministry',
            ' الوزارة': 'ministry',
            'الجهه': 'entity',
            'الجهة': 'entity',
            'الإسم': 'person_name',
            'الاسم': 'person_name',
            'الموضوعات': 'subject',
            'الموضوع': 'subject',
            'المستلم': 'recipient',
            'رقم السجل': 'register_number',
            'التاريخ': 'date',
            'التاريخ ': 'date'
        }
        
        imported_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # استخراج البيانات من الصف
                serial = str(row.get('م', row.get('serial', index + 1)))
                ministry = str(row.get('الوزارة', row.get(' ministry', row.get('ministry', ''))))
                entity = str(row.get('الجهه', row.get('الجهة', row.get('entity', ''))))
                person_name = str(row.get('الإسم', row.get('الاسم', row.get('person_name', ''))))
                subject = str(row.get('الموضوعات', row.get('الموضوع', row.get('subject', ''))))
                recipient = str(row.get('المستلم', row.get('recipient', '')))
                register_number = str(row.get('رقم السجل', row.get('register_number', serial)))
                
                # معالجة التاريخ
                date_value = row.get('التاريخ', row.get('التاريخ ', row.get('date', datetime.now())))
                if pd.isna(date_value):
                    date_value = datetime.now()
                elif isinstance(date_value, str):
                    try:
                        date_value = pd.to_datetime(date_value)
                    except:
                        date_value = datetime.now()
                
                # إنشاء سجل جديد
                warid = Warid(
                    qaid_number=register_number,
                    qaid_date=date_value.date() if hasattr(date_value, 'date') else datetime.now().date(),
                    warid_number=serial,
                    warid_date=date_value.date() if hasattr(date_value, 'date') else datetime.now().date(),
                    almawrid=ministry,
                    warid_from=entity,
                    source_entity=entity,
                    subject=subject if subject and subject != 'nan' else 'بدون موضوع',
                    recipient_1_name=recipient if recipient and recipient != 'nan' else None,
                    created_by=current_user.id
                )
                
                db.add(warid)
                imported_count += 1
                
                # حفظ كل 100 سجل
                if imported_count % 100 == 0:
                    db.commit()
                
            except Exception as e:
                errors.append({
                    'row': index + 2,  + 1 لأن الصف الأول هو العناوين
                    'error': str(e),
                    'data': row.to_dict()
                })
        
        # حفظ السجلات المتبقية
        db.commit()
        
        return ImportResponse(
            success=True,
            imported_count=imported_count,
            errors=errors,
            message=f"تم استيراد {imported_count} سجل بنجاح من أصل {len(df)}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في استيراد الملف: {str(e)}")


@router.post("/sadir/preview", response_model=ImportPreview)
async def preview_sadir_excel(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """معاينة بيانات ملف Excel قبل الاستيراد (للصادر)"""
    
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="يجب أن يكون الملف بصيغة Excel أو CSV")
    
    try:
        # قراءة ملف Excel
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
        
        # تحويل الأعمدة إلى نص
        df.columns = [str(col).strip() for col in df.columns]
        
        # عرض أول 5 صفوف فقط
        preview_data = df.head(5).fillna('').to_dict('records')
        
        return ImportPreview(
            total_rows=len(df),
            preview_data=preview_data,
            columns=df.columns.tolist()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في قراءة الملف: {str(e)}")


@router.post("/sadir", response_model=ImportResponse)
async def import_sadir_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """استيراد بيانات الصادر من ملف Excel"""
    
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="يجب أن يكون الملف بصيغة Excel أو CSV")
    
    try:
        # قراءة ملف Excel
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
        
        # تحويل الأعمدة إلى نص
        df.columns = [str(col).strip() for col in df.columns]
        
        imported_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # استخراج البيانات من الصف
                serial = str(row.get('م', row.get('serial', index + 1)))
                register_number = str(row.get('رقم القيد', row.get('register_number', serial)))
                subject = str(row.get('الموضوع', row.get('subject', 'بدون موضوع')))
                
                # معالجة التاريخ
                date_value = row.get('التاريخ', row.get('date', datetime.now()))
                if pd.isna(date_value):
                    date_value = datetime.now()
                elif isinstance(date_value, str):
                    try:
                        date_value = pd.to_datetime(date_value)
                    except:
                        date_value = datetime.now()
                
                # إنشاء سجل جديد
                sadir = Sadir(
                    qaid_number=register_number,
                    qaid_date=date_value.date() if hasattr(date_value, 'date') else datetime.now().date(),
                    subject=subject if subject and subject != 'nan' else 'بدون موضوع',
                    created_by=current_user.id
                )
                
                db.add(sadir)
                imported_count += 1
                
                # حفظ كل 100 سجل
                if imported_count % 100 == 0:
                    db.commit()
                
            except Exception as e:
                errors.append({
                    'row': index + 2,
                    'error': str(e),
                    'data': row.to_dict()
                })
        
        # حفظ السجلات المتبقية
        db.commit()
        
        return ImportResponse(
            success=True,
            imported_count=imported_count,
            errors=errors,
            message=f"تم استيراد {imported_count} سجل بنجاح من أصل {len(df)}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في استيراد الملف: {str(e)}")


@router.get("/templates/warid")
async def download_warid_template(
    current_user: User = Depends(get_current_user)
):
    """تحميل قالب Excel للوارد"""
    # إنشاء DataFrame فارغة بالأعمدة المطلوبة
    df = pd.DataFrame(columns=[
        'م', 'النائب', 'الوزارة', 'الجهه', 'الإسم', 
        'الموضوعات', 'المستلم', 'رقم السجل', 'التاريخ'
    ])
    
    # حفظ الملف
    template_path = "templates/warid_template.xlsx"
    os.makedirs("templates", exist_ok=True)
    df.to_excel(template_path, index=False, engine='openpyxl')
    
    return {"template_path": template_path, "message": "تم إنشاء القالب بنجاح"}


@router.get("/templates/sadir")
async def download_sadir_template(
    current_user: User = Depends(get_current_user)
):
    """تحميل قالب Excel للصادر"""
    # إنشاء DataFrame فارغة بالأعمدة المطلوبة
    df = pd.DataFrame(columns=[
        'م', 'رقم القيد', 'التاريخ', 'الموضوع', 
        'الإدارة الوارد منها', 'الجهة المرسل إليها'
    ])
    
    # حفظ الملف
    template_path = "templates/sadir_template.xlsx"
    os.makedirs("templates", exist_ok=True)
    df.to_excel(template_path, index=False, engine='openpyxl')
    
    return {"template_path": template_path, "message": "تم إنشاء القالب بنجاح"}
