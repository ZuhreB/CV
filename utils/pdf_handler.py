import PyPDF2
import io
import typing
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from config import logger

import os

# Font dosyalarının güvenli yolu (Proje içindeki assets/fonts klasörü)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(BASE_DIR, "assets", "fonts")

# TR/UTF-8 desteği için TTF fontları kaydediyoruz (Örn: Arial)
try:
    pdfmetrics.registerFont(TTFont('Arial', os.path.join(FONT_DIR, 'arial.ttf')))
    pdfmetrics.registerFont(TTFont('Arial-Bold', os.path.join(FONT_DIR, 'arialbd.ttf')))
    FONT_NORMAL = 'Arial'
    FONT_BOLD = 'Arial-Bold'
    logger.info("Arial TTF fontları klasörden başarıyla yüklendi (Türkçe karakter desteği aktif).")
except Exception as e:
    logger.warning(f"Arial TTF fontu bulunamadı, varsayılan fonta dönülüyor. (Türkçe harflerde sorun olabilir): {e}")
    FONT_NORMAL = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'

def extract_text_from_pdf(file: typing.Any) -> str:
    """Yüklenen PDF dosyasından metin çıkarır. Streamlit UploadedFile objesini destekler."""
    try:
        # file nesnesinden adı okumayı deniyoruz
        file_name = file.name if hasattr(file, 'name') else 'Bilinmeyen Dosya'
        logger.info(f"PDF'ten metin çıkarma başlatıldı - Dosya: {file_name}")
        
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
                
        logger.info(f"PDF'ten metin başarıyla çıkarıldı. Karakter sayısı: {len(text)}")
        return text
    except Exception as e:
        logger.exception("PDF okunurken bir hata oluştu.")
        return f"PDF okuma hatası: {str(e)}"

def generate_cv_pdf(cv_text: str) -> bytes:
    """Metin tabanlı CV verisini ReportLab ile daha gelişmiş PDF formatına dönüştürür."""
    logger.info("Yeniden oluşturulan CV için PDF doküman çıkarma işlemi başlatıldı.")
    try:
        buffer = io.BytesIO()
        # Kenar boşluklarını daraltıp A4 formatını kullanıyoruz ki 1 sayfaya daha fazla sığsın
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=36, 
            leftMargin=36, 
            topMargin=36, 
            bottomMargin=36
        )
        styles = getSampleStyleSheet()
        
        # 1 sayfaya sığması için font boyutları ve boşlukları optimize edildi
        style = ParagraphStyle(
            'Normal_CV',
            parent=styles["Normal"],
            fontName=FONT_NORMAL,
            fontSize=10,
            leading=14,
            spaceAfter=4
        )

        heading_style = ParagraphStyle(
            'Heading_CV',
            parent=styles['Heading2'],
            fontName=FONT_BOLD,
            fontSize=13,
            textColor='#1a202c', # Koyu gri renk
            spaceAfter=6,
            spaceBefore=10
        )

        flowables = []
        for line in cv_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Markdown formatındaki başlıkları algılama
            is_heading = False
            if line.startswith('###') or line.startswith('##') or line.startswith('#'):
                line = line.replace('#', '').strip()
                is_heading = True
            
            # Kalınlaştırılmış yerleri temizleyip normal gösterim için düzenliyoruz. 
            # ReportLab desteklediği <b> html elementini de kullanabilirdik ama metin yapısı çok karışık olabiliyor.
            clean_line = line.replace('**', '').replace('*', '-')
            
            if is_heading:
                # Başlıklarda ReportLab'ın bold yeteneğini kullanıyoruz
                p = Paragraph(f"<b>{clean_line}</b>", heading_style)
            else:
                p = Paragraph(clean_line, style)
                
            flowables.append(p)

        doc.build(flowables)
        pdf_bytes = buffer.getvalue()
        logger.info("PDF doküman başarıyla oluşturuldu ve belleğe yazıldı.")
        return pdf_bytes
    except Exception as e:
        logger.exception("PDF oluşturma sırasında hata.")
        raise e
