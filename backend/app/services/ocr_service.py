import fitz  # PyMuPDF
import pandas as pd
import re
from typing import Dict, List, Optional
from datetime import datetime


class OCRService:
    def __init__(self):
        pass

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """
        استخراج النص من ملف PDF باستخدام PyMuPDF
        """
        doc = fitz.open(pdf_path)
        full_text = []
        
        for page_num, page in enumerate(doc, 1):
            text = page.get_text()
            full_text.append(f"--- صفحة {page_num} ---\n{text}")
        
        doc.close()
        return "\n\n".join(full_text)

    @staticmethod
    def clean_text(text: str) -> str:
        """
        تنظيف النص المستخرج
        """
        # إزالة الأسطر الفارغة المتكررة
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        return text.strip()

    @staticmethod
    def extract_document_data(text: str) -> Dict:
        """
        استخراج البيانات المنظمة من النص
        مثل: الموضوع، التاريخ، المصدر، المرسل إليه
        """
        data = {
            "subject": "",
            "date": "",
            "source": "",
            "destination": "",
            "content": text[:1000]  # أول 1000 حرف
        }

        # البحث عن الموضوع
        subject_patterns = [
            r'(?:موضوع|الموضوع|عنوان)\s*[:：]\s*(.+?)(?:\n|$)',
            r'(?:خطاب|رسالة|اتفاقية)\s+(.+?)(?:\n|$)',
        ]
        for pattern in subject_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["subject"] = match.group(1).strip(" :-،")
                break

        # البحث عن التاريخ
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                data["date"] = match.group(0)
                break

        # البحث عن المصدر
        source_patterns = [
            r'(?:من|صادر من|الجهة|المانحة)\s*[:：]\s*(.+?)(?:\n|$)',
        ]
        for pattern in source_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["source"] = match.group(1).strip(" :-،")
                break

        # البحث عن المرسل إليه
        dest_patterns = [
            r'(?:إلى|المرسل إليه|إدارة|قطاع)\s*[:：]\s*(.+?)(?:\n|$)',
        ]
        for pattern in dest_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["destination"] = match.group(1).strip(" :-،")
                break

        return data

    @staticmethod
    def process_pdf_document(pdf_path: str) -> Dict:
        """
        معالجة كاملة لملف PDF واستخراج البيانات
        """
        print(f"📄 جاري معالجة: {pdf_path}")

        # استخراج النص
        raw_text = OCRService.extract_text_from_pdf(pdf_path)
        
        # تنظيف النص
        cleaned_text = OCRService.clean_text(raw_text)
        
        # استخراج البيانات المنظمة
        doc_data = OCRService.extract_document_data(cleaned_text)
        
        # حفظ النص الكامل
        doc_data["full_text"] = cleaned_text
        doc_data["processed_at"] = datetime.utcnow().isoformat()
        
        print(f"✅ تم استخراج: الموضوع='{doc_data['subject'][:50]}...', التاريخ={doc_data['date']}")
        
        return doc_data

# الدالة الرئيسية للاستخدام الخارجي
def process_pdf_file(pdf_path: str) -> Dict:
    """
    معالجة ملف PDF واحد
    """
    return OCRService.process_pdf_document(pdf_path)


def batch_process_pdfs(pdf_paths: List[str]) -> List[Dict]:
    """
    معالجة مجموعة من ملفات PDF
    """
    results = []
    for i, pdf_path in enumerate(pdf_paths, 1):
        print(f"\n⚙️  معالجة ملف {i}/{len(pdf_paths)}...")
        try:
            result = process_pdf_file(pdf_path)
            result["file_path"] = pdf_path
            results.append(result)
        except Exception as e:
            print(f"❌ خطأ في معالجة {pdf_path}: {e}")
            results.append({
                "file_path": pdf_path,
                "error": str(e)
            })
    
    return results