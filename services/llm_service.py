import google.generativeai as genai
import os
import streamlit as st
from config import logger, MODEL_NAME, GENERATION_CONFIG
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

def get_api_key() -> str:
    """API anahtarını .env dosyasından veya Streamlit secrets'tan alır."""
    # 1. Öncelik: .env içerisindeki sistem ortam değişkenleri
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key
        
    # 2. Öncelik: Streamlit secrets (Eğer secrets.toml varsa)
    try:
        # st.secrets'e doğrudan erişmek yerine hasattr gibi güvenli bir yöntem yok. 
        # Streamlit, dosya yoksa özel bir uyarı ('No secrets found...') verebilir.
        # Bu yüzden hata yakalama içine alıyoruz.
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
        
    return ""

API_KEY = get_api_key()

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    logger.error("API Anahtarı bulunamadı! Lütfen .env dosyasına veya .streamlit/secrets.toml içine ekleyin.")


def is_api_configured() -> bool:
    """API anahtarının tanımlı olup olmadığını döndürür."""
    return bool(API_KEY)


def get_gemini_response(prompt: str, is_json: bool = True) -> str:
    """Gemini modelinden yanıt alır."""
    if not is_api_configured():
        logger.error("API yapılandırılmamış şekilde çağrı denendi.")
        return "HATA: API Anahtarı eksik! Lütfen .env dosyanızı kontrol edin."
    
    try:
        logger.info(f"Gemini API çağrısı yapılıyor. Mod: {'JSON' if is_json else 'DÜZ METİN'}")
        if is_json:
            model = genai.GenerativeModel(model_name=MODEL_NAME, generation_config=GENERATION_CONFIG)
        else:
            # Düz metin için config olmaksızın varsayılan parametreler
            model = genai.GenerativeModel(model_name=MODEL_NAME)
            
        response = model.generate_content(prompt)
        logger.info("Gemini API çağrısı başarıyla tamamlandı.")
        return response.text
    except Exception as e:
        logger.exception("Gemini API isteği sırasında hata oluştu.")
        return f"Gemini API Hatası: {str(e)}"
