from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    seclevel = Column(String(20), nullable=False, default="user")
    full_name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)


class Warid(Base):
    """نموذج الوارد"""
    __tablename__ = "warid"
    id = Column(Integer, primary_key=True, index=True)
    
    # قيد
    qaid_number = Column(String(50), nullable=False, index=True)
    qaid_date = Column(Date, nullable=False)
    
    # الوارد
    warid_number = Column(String(50), nullable=False, index=True)
    warid_date = Column(Date, nullable=False)
    almawrid = Column(String(200), nullable=True)
    warid_from = Column(String(200), nullable=True)
    
    # الخطاب
    source_entity = Column(String(200), nullable=True)  # الجهة الموقع منها الخطاب
    letter_number = Column(String(50), nullable=True)
    letter_date = Column(Date, nullable=True)
    page_count = Column(Integer, default=0)
    letter_status = Column(String(50), nullable=True)
    
    # الموضوع
    subject = Column(Text, nullable=False)
    
    # التوقيع
    signature_status = Column(String(50), default='pending')  # pending, saved
    signature_date = Column(Date, nullable=True)
    needs_followup = Column(Boolean, default=False)
    
    # صادر إلى (3 مستلمين)
    recipient_1_name = Column(String(200), nullable=True)
    recipient_1_delivery_date = Column(Date, nullable=True)
    recipient_2_name = Column(String(200), nullable=True)
    recipient_2_delivery_date = Column(Date, nullable=True)
    recipient_3_name = Column(String(200), nullable=True)
    recipient_3_delivery_date = Column(Date, nullable=True)
    
    # ملف الحفظ
    file_name = Column(String(255), nullable=True)
    delivery_letter_status = Column(String(50), nullable=True)
    
    # الارتباط
    linked_to_another = Column(Boolean, default=False)
    letter_type = Column(String(50), nullable=True)
    other_letter_qaid = Column(String(50), nullable=True)
    
    # ملاحظات وملف
    notes = Column(Text, nullable=True)
    attachment_path = Column(String(500), nullable=True)
    attachment_name = Column(String(255), nullable=True)
    
    # metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    creator = relationship("User", backref="warid_documents")


class Sadir(Base):
    """نموذج الصادر"""
    __tablename__ = "sadir"
    id = Column(Integer, primary_key=True, index=True)
    
    # قيد
    qaid_number = Column(String(50), nullable=False, index=True)
    qaid_date = Column(Date, nullable=False)
    
    # الإدارة الوارد منها
    source_administration = Column(String(200), nullable=True)
    letter_number = Column(String(50), nullable=True)
    letter_date = Column(Date, nullable=True)
    attachment_count = Column(Integer, default=0)
    
    # الموضوع
    subject = Column(Text, nullable=False)
    
    # التوقيع
    signature_status = Column(String(50), default='pending')
    signature_date = Column(Date, nullable=True)
    
    # صادر إلى (3 مستلمين)
    recipient_1_name = Column(String(200), nullable=True)
    recipient_1_delivery_date = Column(Date, nullable=True)
    recipient_2_name = Column(String(200), nullable=True)
    recipient_2_delivery_date = Column(Date, nullable=True)
    recipient_3_name = Column(String(200), nullable=True)
    recipient_3_delivery_date = Column(Date, nullable=True)
    
    # الوزارة/الهيئة/جهة أخرى
    is_ministry = Column(Boolean, default=False)
    is_authority = Column(Boolean, default=False)
    is_other = Column(Boolean, default=False)
    
    # ملف الحفظ
    file_name = Column(String(255), nullable=True)
    needs_followup = Column(Boolean, default=False)
    
    # التوقيع من رئيس الهيئة
    signed_by_chief = Column(Boolean, default=False)
    exported_to = Column(String(200), nullable=True)
    export_date = Column(Date, nullable=True)
    
    # الارتباط
    letter_type = Column(String(50), nullable=True)
    linked_to_another = Column(Boolean, default=False)
    attachment_path = Column(String(500), nullable=True)
    attachment_name = Column(String(255), nullable=True)
    other_letter_qaid = Column(String(50), nullable=True)
    
    # ملاحظات
    notes = Column(Text, nullable=True)
    
    # metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    creator = relationship("User", backref="sadir_documents")


class DocumentHistory(Base):
    __tablename__ = "document_history"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, nullable=False, index=True)
    document_type = Column(String(20), nullable=False)  # 'warid' or 'sadir'
    action = Column(String(50), nullable=False)
    action_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    actor = relationship("User")
