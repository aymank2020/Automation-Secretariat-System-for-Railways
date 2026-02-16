from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# ========== Warid Schemas ==========

class WaridBase(BaseModel):
    """النموذج الأساسي للوارد"""
    qaid_number: str = Field(..., description="رقم القيد")
    qaid_date: date = Field(..., description="تاريخ القيد")
    warid_number: str = Field(..., description="رقم الوارد")
    warid_date: date = Field(..., description="تاريخ الوارد")
    almawrid: Optional[str] = Field(None, description="الموارد")
    warid_from: Optional[str] = Field(None, description="وارد من")
    source_entity: Optional[str] = Field(None, description="الجهة الموقع منها الخطاب")
    letter_number: Optional[str] = Field(None, description="رقم الخطاب")
    letter_date: Optional[date] = Field(None, description="تاريخ الخطاب")
    page_count: int = Field(0, description="عدد أوراق الخطاب")
    letter_status: Optional[str] = Field(None, description="حالة الخطاب الوارد")
    subject: str = Field(..., description="الموضوع")
    signature_status: str = Field("pending", description="حالة التوقيع")
    signature_date: Optional[date] = Field(None, description="تاريخ التوقيع")
    needs_followup: bool = Field(False, description="يحتاج لمتابعة")
    recipient_1_name: Optional[str] = Field(None, description="اسم المستلم 1")
    recipient_1_delivery_date: Optional[date] = Field(None, description="تاريخ التسليم 1")
    recipient_2_name: Optional[str] = Field(None, description="اسم المستلم 2")
    recipient_2_delivery_date: Optional[date] = Field(None, description="تاريخ التسليم 2")
    recipient_3_name: Optional[str] = Field(None, description="اسم المستلم 3")
    recipient_3_delivery_date: Optional[date] = Field(None, description="تاريخ التسليم 3")
    file_name: Optional[str] = Field(None, description="اسم ملف الحفظ")
    delivery_letter_status: Optional[str] = Field(None, description="حالة خطاب التسليم")
    linked_to_another: bool = Field(False, description="مرتبط بخطاب آخر")
    letter_type: Optional[str] = Field(None, description="نوع الخطاب")
    other_letter_qaid: Optional[str] = Field(None, description="رقم قيد الخطاب الآخر")
    notes: Optional[str] = Field(None, description="ملاحظات")


class WaridCreate(WaridBase):
    """نموذج إنشاء وارد جديد"""
    pass


class WaridUpdate(BaseModel):
    """نموذج تحديث وارد"""
    qaid_number: Optional[str] = None
    qaid_date: Optional[date] = None
    warid_number: Optional[str] = None
    warid_date: Optional[date] = None
    almawrid: Optional[str] = None
    warid_from: Optional[str] = None
    source_entity: Optional[str] = None
    letter_number: Optional[str] = None
    letter_date: Optional[date] = None
    page_count: Optional[int] = None
    letter_status: Optional[str] = None
    subject: Optional[str] = None
    signature_status: Optional[str] = None
    signature_date: Optional[date] = None
    needs_followup: Optional[bool] = None
    recipient_1_name: Optional[str] = None
    recipient_1_delivery_date: Optional[date] = None
    recipient_2_name: Optional[str] = None
    recipient_2_delivery_date: Optional[date] = None
    recipient_3_name: Optional[str] = None
    recipient_3_delivery_date: Optional[date] = None
    file_name: Optional[str] = None
    delivery_letter_status: Optional[str] = None
    linked_to_another: Optional[bool] = None
    letter_type: Optional[str] = None
    other_letter_qaid: Optional[str] = None
    notes: Optional[str] = None


class WaridResponse(WaridBase):
    """نموذج استجابة الوارد"""
    id: int
    attachment_path: Optional[str] = None
    attachment_name: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class WaridListResponse(BaseModel):
    """نموذج قائمة الوارد"""
    id: int
    qaid_number: str
    qaid_date: date
    warid_number: str
    warid_date: date
    subject: str
    source_entity: Optional[str] = None
    signature_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Sadir Schemas ==========

class SadirBase(BaseModel):
    """النموذج الأساسي للصادر"""
    qaid_number: str = Field(..., description="رقم القيد")
    qaid_date: date = Field(..., description="تاريخ القيد")
    source_administration: Optional[str] = Field(None, description="الإدارة الوارد منها")
    letter_number: Optional[str] = Field(None, description="رقم الخطاب")
    letter_date: Optional[date] = Field(None, description="تاريخ الخطاب")
    attachment_count: int = Field(0, description="عدد المرفقات")
    subject: str = Field(..., description="الموضوع")
    signature_status: str = Field("pending", description="حالة التوقيع")
    signature_date: Optional[date] = Field(None, description="تاريخ التوقيع")
    recipient_1_name: Optional[str] = Field(None, description="اسم المستلم 1")
    recipient_1_delivery_date: Optional[date] = Field(None, description="تاريخ التسليم 1")
    recipient_2_name: Optional[str] = Field(None, description="اسم المستلم 2")
    recipient_2_delivery_date: Optional[date] = Field(None, description="تاريخ التسليم 2")
    recipient_3_name: Optional[str] = Field(None, description="اسم المستلم 3")
    recipient_3_delivery_date: Optional[date] = Field(None, description="تاريخ التسليم 3")
    is_ministry: bool = Field(False, description="الوزارة")
    is_authority: bool = Field(False, description="الهيئة")
    is_other: bool = Field(False, description="جهة أخرى")
    file_name: Optional[str] = Field(None, description="اسم ملف الحفظ")
    needs_followup: bool = Field(False, description="يحتاج لمتابعة")
    signed_by_chief: bool = Field(False, description="تم التوقيع من رئيس الهيئة")
    exported_to: Optional[str] = Field(None, description="تم تصديرها إلى")
    export_date: Optional[date] = Field(None, description="تاريخ التصدير")
    letter_type: Optional[str] = Field(None, description="نوع الخطاب")
    linked_to_another: bool = Field(False, description="مرتبط بخطاب آخر")
    other_letter_qaid: Optional[str] = Field(None, description="رقم قيد الخطاب الآخر")
    notes: Optional[str] = Field(None, description="ملاحظات")


class SadirCreate(SadirBase):
    """نموذج إنشاء صادر جديد"""
    pass


class SadirUpdate(BaseModel):
    """نموذج تحديث صادر"""
    qaid_number: Optional[str] = None
    qaid_date: Optional[date] = None
    source_administration: Optional[str] = None
    letter_number: Optional[str] = None
    letter_date: Optional[date] = None
    attachment_count: Optional[int] = None
    subject: Optional[str] = None
    signature_status: Optional[str] = None
    signature_date: Optional[date] = None
    recipient_1_name: Optional[str] = None
    recipient_1_delivery_date: Optional[date] = None
    recipient_2_name: Optional[str] = None
    recipient_2_delivery_date: Optional[date] = None
    recipient_3_name: Optional[str] = None
    recipient_3_delivery_date: Optional[date] = None
    is_ministry: Optional[bool] = None
    is_authority: Optional[bool] = None
    is_other: Optional[bool] = None
    file_name: Optional[str] = None
    needs_followup: Optional[bool] = None
    signed_by_chief: Optional[bool] = None
    exported_to: Optional[str] = None
    export_date: Optional[date] = None
    letter_type: Optional[str] = None
    linked_to_another: Optional[bool] = None
    other_letter_qaid: Optional[str] = None
    notes: Optional[str] = None


class SadirResponse(SadirBase):
    """نموذج استجابة الصادر"""
    id: int
    attachment_path: Optional[str] = None
    attachment_name: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SadirListResponse(BaseModel):
    """نموذج قائمة الصادر"""
    id: int
    qaid_number: str
    qaid_date: date
    letter_number: Optional[str] = None
    letter_date: Optional[date] = None
    subject: str
    signature_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Search Schemas ==========

class WaridSearchParams(BaseModel):
    """معاملات البحث في الوارد"""
    qaid_number: Optional[str] = None
    warid_number: Optional[str] = None
    subject: Optional[str] = None
    source_entity: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    signature_status: Optional[str] = None


class SadirSearchParams(BaseModel):
    """معاملات البحث في الصادر"""
    qaid_number: Optional[str] = None
    letter_number: Optional[str] = None
    subject: Optional[str] = None
    source_administration: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    signature_status: Optional[str] = None


# ========== Import Schemas ==========

class ImportResponse(BaseModel):
    """نموذج استجابة الاستيراد"""
    success: bool
    imported_count: int
    errors: List[dict]
    message: str


class ImportPreview(BaseModel):
    """نموذج معاينة الاستيراد"""
    total_rows: int
    preview_data: List[dict]
    columns: List[str]
