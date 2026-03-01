import os
import logging

# Set up global logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CV_Changer")

# Model ayarları
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

MODEL_NAME = "gemini-2.5-flash"

# --- ÜLKE VE DİL BAZLI KURALLAR ---
COUNTRY_RULES = {
    "ABD": "Kesinlikle 1 sayfa olmalı. Fotoğraf, doğum tarihi ve medeni durum asla ekleme. Sadece üniversite düzeyindeki eğitimleri yaz, dili çok kısa ve doğrudan, sonuç odaklı kurgula.",
    "İngiltere": "1-2 sayfa olmalı. Fotoğraf ve iletişim bilgisi dışındaki kişisel bilgileri kesinlikle ekleme. Sade ve resmi bir üslup kullan.",
    "Almanya": "2 sayfa olmalı ve üstte profesyonel fotoğraf yeri bulunmalı. Eğitim bilgilerini iş deneyiminin üstüne koy. İş tecrübelerinde kesinlikle ay ve yıl belirt ve eğer CV'de tarihsel bir boşluk varsa bunu açıklayan bir not ekle. CV'nin en altına tarih ve imza alanı ekle.",
    "Fransa": "Dili kesinlikle Fransızca kurgula (şirket uluslararası olsa bile). Doğum tarihi yerine sadece 'Yaş' bilgisi ekle. CV'ye mutlaka 'Projet Professionnel' (kariyer hedeflerinin, yeteneklerin ve beklentilerin anlatıldığı bölüm) adlı bir başlık ekle.",
    "İtalya": "Dili resmi 'Siz' (Lei) formuyla İtalyanca yaz. Adayın ismini CV'nin en tepesine başlık olarak koy. Doğum tarihi ve mezuniyet derecesini/notunu kesinlikle ekle. Hobi ve ilgi alanlarını tamamen CV'den çıkar.",
    "Avustralya": "Max 2 sayfa olmalı, fotoğraf ekleme. İletişim bilgilerinin hemen altına 'Kariyer Hedefi' (Career Objective) bölümü aç. Adayın sahip olduğu yetenekleri işe göre kurgulayarak 'Employment Skills' başlığı altında vurgula.",
    "Japonya": "'Rirekisho' formatını baz al. (Yalın, sadece gerçeklerin olduğu, abartısız bir metin olarak hazırla). Yaş, cinsiyet ve milliyet bilgilerini ekle. Eklenecek referansların adayı en az 2 yıldır tanıyan kişiler olduğunu belirten bir not düş.",
    "Hollanda ve Belçika": "Profesyonel fotoğraf alanı ekle. Eğer aday deneyimsizse eğitimi iş tecrübesinden önce yaz, deneyimliyse iş tecrübesini en üste al.",
    "İspanya, Yunanistan, Portekiz": "Sağ üst köşeye fotoğraf alanı ekle, ikna edici bir dil kullan ve eğitim bilgilerini iş deneyiminden önce ver.",
    "Türkiye": "Sade arka planlı bir fotoğraf beklentisi olduğunu göz önünde bulundur. CV, kısa, net ve özel sektör için mutlaka 1 sayfa olmalı."
}

LANGUAGES = {
    "Türkçe": "Turkish",
    "İngilizce": "English",
    "Almanca": "German",
    "Fransızca": "French"
}
