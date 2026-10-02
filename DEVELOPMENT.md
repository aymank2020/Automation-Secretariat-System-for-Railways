# دليل التطوير - نظام إدارة المراسلات

## التطويرات الجديدة

### 1. شاشة رئيسية جديدة (Home.vue)
- تصميم مطابق للصور المرفقة
- شعار الهيئة القومية لسكك حديد مصر
- أزرار: أدخال الوارد/الصادر، بحث في الوارد/الصادر، استعلام في الوارد/الصادر
- زر خروج

### 2. نماذج الوارد والصادر المنفصلة

#### WaridForm.vue - نموذج الوارد
يحتوي على الحقول التالية:
- رقم القيد وتاريخ القيد
- رقم الوارد وتاريخ الوارد والموارد ووارد من
- الجهة الموقع منها الخطاب ورقم الخطاب وتاريخ الخطاب
- عدد أوراق الخطاب وحالة الخطاب الوارد
- الموضوع
- حالة التوقيع (انتظار/حفظ) وتاريخ التوقيع
- يحتاج لمتابعة
- صادر إلى (3 مستلمين مع تواريخ التسليم)
- اسم ملف الحفظ وحالة خطاب التسليم
- مرتبط بخطاب آخر ونوع الخطاب ورقم قيد الخطاب الآخر
- ملاحظات وصورة الخطاب

#### SadirForm.vue - نموذج الصادر
يحتوي على الحقول التالية:
- رقم القيد وتاريخ القيد
- الإدارة الوارد منها ورقم الخطاب وتاريخ الخطاب
- عدد المرفقات والموضوع
- حالة التوقيع وتاريخ التوقيع
- صادر إلى (3 مستلمين مع تواريخ التسليم)
- الوزارة/الهيئة/جهة أخرى
- اسم ملف الحفظ ويحتاج لمتابعة
- تم التوقيع من رئيس الهيئة وتم تصديرها إلى وتاريخ التصدير
- نوع الخطاب ومرتبط بخطاب آخر
- صورة الخطاب ورقم قيد الخطاب الآخر وملاحظات

### 3. صفحات البحث

#### WaridSearch.vue - البحث في الوارد
- حقول البحث: رقم القيد، رقم الوارد، الموضوع، الجهة، التاريخ، حالة التوقيع
- جدول النتائج مع إمكانية التعديل والحذف

#### SadirSearch.vue - البحث في الصادر
- حقول البحث: رقم القيد، رقم الخطاب، الموضوع، الإدارة، التاريخ، حالة التوقيع
- جدول النتائج مع إمكانية التعديل والحذف

### 4. صفحات الاستعلام

#### WaridQuery.vue - استعلام الوارد
- بحث سريع
- إحصائيات (إجمالي، انتظار، حفظ، يحتاج متابعة)
- جدول النتائج مع عرض التفاصيل

#### SadirQuery.vue - استعلام الصادر
- بحث سريع
- إحصائيات (إجمالي، انتظار، حفظ، يحتاج متابعة، موقع من الرئيس)
- جدول النتائج مع عرض التفاصيل

### 5. استيراد من Excel

#### ExcelImport.vue - مكون استيراد Excel
- اختيار نوع البيانات (وارد/صادر)
- رفع ملف Excel/CSV
- معاينة البيانات قبل الاستيراد
- استيراد البيانات إلى قاعدة البيانات

#### API Endpoints للاستيراد
- `POST /import/warid/preview` - معاينة بيانات الوارد
- `POST /import/warid` - استيراد بيانات الوارد
- `POST /import/sadir/preview` - معاينة بيانات الصادر
- `POST /import/sadir` - استيراد بيانات الصادر
- `GET /import/templates/warid` - تحميل قالب الوارد
- `GET /import/templates/sadir` - تحميل قالب الصادر

## الملفات المضافة/المعدلة

### Backend
```
backend/app/models/__init__.py          # إضافة نماذج Warid و Sadir
backend/app/schemas/__init__.py         # إضافة المخططات
backend/app/api/warid.py                # API الوارد الجديد
backend/app/api/sadir.py                # API الصادر الجديد
backend/app/api/import_excel.py         # API استيراد Excel
backend/app/main.py                     # تحديث المسارات
```

### Frontend
```
frontend/src/pages/Home.vue             # الشاشة الرئيسية الجديدة
frontend/src/pages/WaridForm.vue        # نموذج الوارد
frontend/src/pages/SadirForm.vue        # نموذج الصادر
frontend/src/pages/WaridSearch.vue      # البحث في الوارد
frontend/src/pages/SadirSearch.vue      # البحث في الصادر
frontend/src/pages/WaridQuery.vue       # استعلام الوارد
frontend/src/pages/SadirQuery.vue       # استعلام الصادر
frontend/src/components/ExcelImport.vue # مكون استيراد Excel
frontend/src/router/index.js            # تحديث التوجيهات
frontend/src/pages/Login.vue            # تحديث إعادة التوجيه
```

## قاعدة البيانات

### جدول Warid (الوارد)
| الحقل | النوع | الوصف |
|-------|-------|-------|
| id | Integer | المعرف |
| qaid_number | String | رقم القيد |
| qaid_date | Date | تاريخ القيد |
| warid_number | String | رقم الوارد |
| warid_date | Date | تاريخ الوارد |
| almawrid | String | الموارد |
| warid_from | String | وارد من |
| source_entity | String | الجهة الموقع منها |
| letter_number | String | رقم الخطاب |
| letter_date | Date | تاريخ الخطاب |
| page_count | Integer | عدد الأوراق |
| letter_status | String | حالة الخطاب |
| subject | Text | الموضوع |
| signature_status | String | حالة التوقيع |
| signature_date | Date | تاريخ التوقيع |
| needs_followup | Boolean | يحتاج متابعة |
| recipient_1_name | String | المستلم 1 |
| recipient_1_delivery_date | Date | تاريخ التسليم 1 |
| recipient_2_name | String | المستلم 2 |
| recipient_2_delivery_date | Date | تاريخ التسليم 2 |
| recipient_3_name | String | المستلم 3 |
| recipient_3_delivery_date | Date | تاريخ التسليم 3 |
| file_name | String | اسم ملف الحفظ |
| delivery_letter_status | String | حالة خطاب التسليم |
| linked_to_another | Boolean | مرتبط بخطاب آخر |
| letter_type | String | نوع الخطاب |
| other_letter_qaid | String | رقم قيد الخطاب الآخر |
| notes | Text | ملاحظات |
| attachment_path | String | مسار الملف المرفق |
| attachment_name | String | اسم الملف المرفق |
| created_by | Integer | أنشئ بواسطة |
| created_at | DateTime | تاريخ الإنشاء |
| updated_at | DateTime | تاريخ التحديث |

### جدول Sadir (الصادر)
| الحقل | النوع | الوصف |
|-------|-------|-------|
| id | Integer | المعرف |
| qaid_number | String | رقم القيد |
| qaid_date | Date | تاريخ القيد |
| source_administration | String | الإدارة الوارد منها |
| letter_number | String | رقم الخطاب |
| letter_date | Date | تاريخ الخطاب |
| attachment_count | Integer | عدد المرفقات |
| subject | Text | الموضوع |
| signature_status | String | حالة التوقيع |
| signature_date | Date | تاريخ التوقيع |
| recipient_1_name | String | المستلم 1 |
| recipient_1_delivery_date | Date | تاريخ التسليم 1 |
| recipient_2_name | String | المستلم 2 |
| recipient_2_delivery_date | Date | تاريخ التسليم 2 |
| recipient_3_name | String | المستلم 3 |
| recipient_3_delivery_date | Date | تاريخ التسليم 3 |
| is_ministry | Boolean | الوزارة |
| is_authority | Boolean | الهيئة |
| is_other | Boolean | جهة أخرى |
| file_name | String | اسم ملف الحفظ |
| needs_followup | Boolean | يحتاج متابعة |
| signed_by_chief | Boolean | موقع من الرئيس |
| exported_to | String | تم تصديرها إلى |
| export_date | Date | تاريخ التصدير |
| letter_type | String | نوع الخطاب |
| linked_to_another | Boolean | مرتبط بخطاب آخر |
| attachment_path | String | مسار الملف المرفق |
| attachment_name | String | اسم الملف المرفق |
| other_letter_qaid | String | رقم قيد الخطاب الآخر |
| notes | Text | ملاحظات |
| created_by | Integer | أنشئ بواسطة |
| created_at | DateTime | تاريخ الإنشاء |
| updated_at | DateTime | تاريخ التحديث |

## API Endpoints

### الوارد
- `GET /warid/` - قائمة الوارد
- `POST /warid/` - إنشاء وارد جديد
- `GET /warid/{id}` - الحصول على تفاصيل وارد
- `PUT /warid/{id}` - تحديث وارد
- `DELETE /warid/{id}` - حذف وارد
- `GET /warid/search` - البحث في الوارد
- `POST /warid/{id}/upload` - رفع ملف مرفق
- `GET /warid/stats/summary` - إحصائيات الوارد

### الصادر
- `GET /sadir/` - قائمة الصادر
- `POST /sadir/` - إنشاء صادر جديد
- `GET /sadir/{id}` - الحصول على تفاصيل صادر
- `PUT /sadir/{id}` - تحديث صادر
- `DELETE /sadir/{id}` - حذف صادر
- `GET /sadir/search` - البحث في الصادر
- `POST /sadir/{id}/upload` - رفع ملف مرفق
- `GET /sadir/stats/summary` - إحصائيات الصادر

## المسارات الجديدة

| المسار | الوصف |
|--------|-------|
| `/home` | الشاشة الرئيسية |
| `/warid/new` | إضافة وارد جديد |
| `/warid/:id/edit` | تعديل وارد |
| `/warid/search` | البحث في الوارد |
| `/warid/query` | استعلام الوارد |
| `/sadir/new` | إضافة صادر جديد |
| `/sadir/:id/edit` | تعديل صادر |
| `/sadir/search` | البحث في الصادر |
| `/sadir/query` | استعلام الصادر |

## طريقة التشغيل

### 1. تثبيت متطلبات Backend
```bash
cd backend
pip install -r requirements.txt
```

### 2. تشغيل Backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. تثبيت متطلبات Frontend
```bash
cd frontend
npm install
```

### 4. تشغيل Frontend
```bash
npm run dev
```

### 5. فتح التطبيق
```
http://localhost:5173
```

بيانات الدخول الافتراضية:
- **المدير الأول:** اضبط INITIAL_ADMIN_USERNAME وINITIAL_ADMIN_PASSWORD في البيئة.
- **بقية المستخدمين:** ينشئهم المدير بعد تسجيل الدخول؛ لا توجد كلمات مرور افتراضية.

## ملاحظات هامة

1. تم إضافة نماذج جديدة للوارد والصادر مع جميع الحقول المطلوبة
2. تم إنشاء صفحات منفصلة للوارد والصادر
3. تم إضافة خاصية استيراد البيانات من Excel
4. تم تحديث التوجيهات لتوجيه المستخدم إلى الشاشة الرئيسية بعد تسجيل الدخول
5. تم الحفاظ على الصفحات القديمة (Dashboard) للتوافق مع النظام القديم
