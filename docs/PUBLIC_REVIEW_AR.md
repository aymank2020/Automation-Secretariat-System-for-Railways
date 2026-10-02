# مراجعة وتطوير Automation-Secretariat-System-for-Railways

التاريخ: 2026-10-02. [المستودع العام](https://github.com/aymank2020/Automation-Secretariat-System-for-Railways).
المصدر الذي بدأت منه المراجعة: `ec364b4f15fff4f2b9c4fc9f6f23707d0fbac713`. فرع التطوير: `codex/review-develop-2026-10-02`.

## وظيفة المشروع ونطاق المراجعة

نسخة أقدم تجمع وارد/صادر وواجهة مستندات قديمة ورفع PDF. المصدر العام لم يصل حتى إلى import app بسبب نموذج/schemas ناقصة واستيرادات auth خاطئة وسطر عربي غير معلق. أعدت عقد API الموجود دون إعادة تصميم بيانات وارد/صادر.

راجعت بنية الملفات بصورة متكررة، وتعليمات AGENTS المتاحة، وملفات التشغيل والتبعيات والاختبارات والمستهلكين المرتبطين بالتغييرات. جرى العمل في نسخة معزولة؛ لم تتصل هذه المراجعة بخادم إنتاج أو قاعدة بيانات مستخدم أو جلسة دراسة حقيقية. هذه نتائج تنفيذ محلي محدد، وليست ادعاء مراجعة كل سطر أو جاهزية إنتاج شاملة.

## نتائج موثقة

- P0: Document مستورد من routes وغير موجود؛ schemas User/Token/Document ناقصة. أضيف model التوافق: [backend/app/models/__init__.py:140](../backend/app/models/__init__.py#L140) وschemas المطابقة للاستهلاك الحالي.
- P0: get_current_user استورد من security بدل dependencies، وimport_excel يحوي SyntaxError؛ صُححا.
- P1: التسجيل العام ومفتاح قصير عام والحسابات الأولية الثابتة؛ أصبحت مفاتيح/تهيئة بيئية وتسجيل admin-only.
- P1: التاريخ يجمع أنواعًا مختلفة بالمعرف نفسه؛ writes/read/delete للمستند القديم تستخدم document_type=document: [backend/app/api/documents.py:153](../backend/app/api/documents.py#L153).
- P1: أسماء PDF أُنشئت من اسم المستخدم وdoc_number من ثانية واحدة؛ أصبحا UUID.

## خطة التغيير المنفذة

1. P0 — استعادة imports ونماذج/schema routes الموجودة وإزالة خطأ syntax: منفذ.
2. P1 — حارس التسجيل ورفض sub غير صالح/مستخدم معطل، مفتاح JWT إلزامي وseed من البيئة: منفذ.
3. P1 — عزل تاريخ المستندات حسب النوع وأسماء PDF/أرقام مستند فريدة: منفذ.
4. P2 — اختبارات HTTP للهوية والمستند وPDF وتحديث التشغيل، وstart.sh يفشل عند خطأ بدل متابعة زائفة: منفذ.

## التحقق الفعلي

`python -m compileall app` نجح. `python -m pytest tests -q` من backend: **10 passed**،10 تحذيرات deprecation لـPydantic/SQLAlchemy/lifespan. HTTP ينشئ ويعدل مستندًا ويقرأ history، ورفع ملفين بالاسم ../fixture.pdf يحفظهما باسمين مولدين وأرقام مختلفة. OCR نفسه mock خارجي، فلا دليل استخراج PDF فعلي. frontend npm ci/build: **نجح Vite،97 modules**.

## فحص التكامل والأثر

طُبقت مهارة Integration & Impact Review بعد مراجعة المصدر والاختبارات والفروق النهائية.

app.main يستورد6 routers ويسجلها → auth dependency → /documents/ → model/schema المستعادان → history response. /documents/upload-pdf → حفظ UUID → OCR boundary → المستند/التاريخ. المرجع التنفيذي: [backend/tests/test_documents.py:9](../backend/tests/test_documents.py#L9). صُححت أنواع history لتجنب حذف سجلات warid/sadir المجاورة، واختبار collision HTTP يثبت عدم ظهور سجل warid مماثل المعرف في history المستند وبقاءه بعد حذف المستند. تستمر endpoints الوارد والصادر والمستند القديم معًا؛ لا أزيلها بسبب التكرار. قاعدة fixture ذاكرة؛ لا ترحيل SQLite قائم.

## أولويات المتابعة والفجوات غير المنفذة

1. P1 — فصل تقديم uploads عن StaticFiles العام بمصادقة وأذونات وحجم محدود.
2. P1 — ترحيل SHA256، CORS محدد، ومعاملات ذرية للمستند وتاريخه.
3. P1 — migration واختبار ترقية قاعدة موجودة قبل تشغيل model المستعاد في الإنتاج.
4. P2 — OCR حقيقي لـPDF المصور واختبارات extraction على ملفات اصطناعية. جميعها غير منفذة؛ هذا إصلاح local runtime ولا يدعي جاهزية إنتاج.

## البحث المستخدم لاتخاذ القرار

- [FastAPI JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/): إعداد توقيع خاص وفحص هوية مركزية.
- [Python tempfile](https://docs.python.org/3/library/tempfile.html): عدم بناء تخزين مشترك من اسم غير موثوق.
- [SQLAlchemy declarative tables](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html): النموذج يجب أن يطابق consumer وschema قبل إنشاء metadata.

تستند نتائج الأعطال والإصلاح إلى ملفات هذا المستودع والاختبارات المحلية؛ توثيق المورد يشرح سبب اختيار التصميم ولا يثبت نجاح النشر.
