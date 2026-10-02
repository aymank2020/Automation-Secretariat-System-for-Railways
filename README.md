# نظام إدارة المراسلات - السكك الحديدية
Railways Correspondence Management System

نظام متكامل لإدارة المراسلات الواردة والصادرة مع دعم OCR التلقائي لملفات PDF.

## 🚀 مميزات النظام

- ✅ إدارة المراسلات الواردة والصادرة
- ✅ نظام تسجيل دخول آمن
- ✅ **معالجة OCR تلقائية لملفات PDF** ⭐ *جديد*
- ✅ استخراج تلقائي للبيانات من المستندات (الموضوع، التاريخ، المصدر، المرسل إليه)
- ✅ نظام بحث شامل
- ✅ توثيق كامل لسجل التعديلات
- ✅ أذونات صلاحيات مستخدمين

---

## 📋 المتطلبات

- Python 3.8+
- Node.js 18+
- Git

---

## 🔧 التثبيت والتشغيل

### الطريقة 1: التشغيل السريع (موصى به)

```bash
# استنساخ الريبو
git clone https://github.com/aymank2020/Automation-Secretariat-System-for-Railways.git
cd Automation-Secretariat-System-for-Railways

# تشغيل كل شيء بسطر واحد
bash start.sh
```

السكربت يقوم تلقائياً بـ:
- تثبيت المكتبات
- إنشاء قاعدة البيانات والمستخدم الأول من إعدادات البيئة
- تشغيل Backend
- تشغيل Frontend

---

### الطريقة 2: التشغيل اليدوي

#### إعداد Backend

```bash
cd backend

# تثبيت المكتبات
pip install -r requirements.txt

# انسخ .env.example إلى .env واضبط SECRET_KEY فريدًا بطول 32 حرفًا على الأقل
# واضبط INITIAL_ADMIN_PASSWORD قويًا؛ لا توجد حسابات افتراضية منشورة

# ⭐ **هام جداً**: إنشاء قاعدة البيانات وتحميل المستخدمين
python seed_db.py

# تشغيل السيرفر
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend URL:** http://localhost:8000  
**API Documentation:** http://localhost:8000/docs

#### إعداد Frontend (في terminal جديد)

```bash
cd frontend

# تثبيت المكتبات
npm install

# تشغيل السيرفر
npm run dev -- --host
```

**Frontend URL:** http://localhost:5173

---

### الطريقة 3: Docker (للإنتاج)

```bash
# بناء وتشغيل الحاويات
docker-compose up --build
```

---

## 🔐 إعداد الدخول

يُنشأ المدير الأول فقط عند ضبط `INITIAL_ADMIN_PASSWORD` لقاعدة بيانات فارغة.
اضبط `SECRET_KEY` فريدًا بطول 32 حرفًا على الأقل واحتفظ به عبر إعادة التشغيل.
التسجيل عبر `/auth/register` يتطلب رمز مدير صالحًا؛ الحسابات الموجودة تظل محفوظة.

---

## 📤 رفع ملفات PDF مع OCR

### عبر API

```bash
curl -X POST "http://localhost:8000/documents/upload-pdf" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf" \
  -F "doc_type=وارد"
```

### الرد النموذجي

```json
{
  "id": 1,
  "doc_type": "وارد",
  "doc_number": "وارد_20240215_223000",
  "subject": "الاتفاقيات مع دولة السودان",
  "source": "وزارة الخارجية",
  "destination": "إدارة الشؤون القانونية",
  "date": "2026-02-15T22:30:00",
  "content": "نص المستند...",
  "file_path": "./uploads/1708037800000_document.pdf",
  "file_name": "document.pdf",
  "file_type": "pdf",
  "status": "new",
  "priority": "normal"
}
```

---

## 🗄️ قاعدة البيانات

النظام يستخدم SQLite افتراضياً. يمكن تغييرها إلى PostgreSQL عبر متغير البيئة `DATABASE_URL`.

### هيكل قاعدة البيانات

```sql
-- جدول المستخدمين
users (id, username, password, seclevel, full_name, is_active)

-- جدول المستندات
documents (id, doc_type, doc_number, subject, source, destination, date, content, file_path, file_name, file_type, status, priority, created_by)

-- جدول سجل التعديلات
document_history (id, document_id, action, action_by, action_at, old_value, new_value)
```

---

## 📂 هيكل المشروع

```
.
├── backend/
│   ├── app/
│   │   ├── api/           # API Endpoints
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   └── users.py
│   │   ├── services/      # ⭐ OCR Service (جديد)
│   │   │   └── ocr_service.py
│   │   ├── db/            # قاعدة البيانات
│   │   ├── models/        # SQLAlchemy Models
│   │   └── schemas/       # Pydantic Schemas
│   ├── requirements.txt
│   ├── seed_db.py         # تهيئة قاعدة البيانات
│   └── uploads/           # الملفات المرفوعة
├── frontend/
│   ├── src/
│   │   ├── components/    # Vue Components
│   │   ├── pages/         # الصفحات
│   │   ├── services/      # API Services
│   │   └── stores/        # State Management
│   └── package.json
├── docker-compose.yml
└── start.sh               # سكربت التشغيل السريع
```

---

## 🆚 التحديثات الجديدة (الإصدار 2.0)

- ✨ **معالجة OCR تلقائية** لملفات PDF
- ✅ استخراج ذكي للبيانات (الموضوع، التاريخ، المصدر، المرسل إليه)
- ✅ Endpoint `/documents/upload-pdf` لرفع الملفات
- ✅ دعم اللغة العربية في استخراج البيانات
- ✅ حفظ الملفات المرفوعة في مجلد `uploads/`
- 🔧 تحديث `requirements.txt` بالمكتبات الجديدة

---

## 🛠️ تطوير النظام

### إضافة ميزات OCR جديدة

تعديل `backend/app/services/ocr_service.py` لتخصيص استخراج البيانات.

### إضافة API Endpoints جديدة

تعديل `backend/app/api/` لإضافة نقاط النهاية المطلوبة.

---

## 📝 الأمان

- كلمات المرور مُشفرة باستخدام SHA-256 + salt
- استخدام JWT للمصادقة
- فصل الصلاحيات حسب المستخدم

---

## 🐛 حل المشاكل

### مشكلة: "اسم المستخدم أو كلمة المرور غير صحيحة"

**الحل:**
```bash
cd backend
python seed_db.py
```

ينشئ هذا الأمر قاعدة البيانات ويحمّل المستخدمين الافتراضيين.

---

## 📞 الدعم

للدعم والتواصل:
- GitHub Issues: https://github.com/aymank2020/Automation-Secretariat-System-for-Railways/issues

---

## 📄 الترخيص

MIT License

---

## 👨‍💻 التطوير بواسطة

- Ayman Kamel (@aymank2020)

---

**آخر تحديث:** فبراير 2026
**الإصدار:** 2.0.0
