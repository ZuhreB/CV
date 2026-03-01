import streamlit as st

# Streamlit yapılandırması UYGULAMANIN EN BAŞINDA OLMALIDIR.
st.set_page_config(page_title="CareerAdaptive AI Pro", layout="wide", page_icon="🚀")

import json

# Yerel modüllerin içe aktarılması
from config import COUNTRY_RULES, LANGUAGES, logger
from services.llm_service import get_gemini_response, is_api_configured
from utils.pdf_handler import extract_text_from_pdf, generate_cv_pdf
from utils.text_utils import generate_html_diff

# --- STREAMLIT ARAYÜZÜ ---


st.title("🚀 CareerAdaptive AI: Profesyonel Kariyer Danışmanı")
st.markdown(
    "CV'nizi sadece düzenlemekle kalmaz, **teknik ve soyut (soft skills)** açıdan iş ilanına göre optimize eder.")

if not is_api_configured():
    st.error("⚠️ API Anahtarı Eksik! Lütfen `.env` dosyanıza veya `.streamlit/secrets.toml` içine `GEMINI_API_KEY` ekleyin.")
    logger.warning("Kullanıcı arayüzde API anahtarından yoksun giriş yaptı.")

# Session State Yönetimi
if 'step' not in st.session_state:
    st.session_state.step = 'input'
if 'analysis' not in st.session_state:
    st.session_state.analysis = None

# --- ADIM 1: GİRDİ AŞAMASI ---
if st.session_state.step == 'input':
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 Başvuru Bilgileri")
        target_country = st.selectbox("Hedef Ülke", list(COUNTRY_RULES.keys()))
        target_lang = st.selectbox("Hedef Dil", list(LANGUAGES.keys()))
        job_description = st.text_area("İş İlanı Metni:", height=200, placeholder="İş tanımını buraya yapıştırın...")

        with st.expander("✨ Ekstra Başarılar ve Belgeler (Opsiyonel)"):
            st.markdown("CV'nizde olmayan ama bu işe özel belirtmek istediğiniz seminer, sertifika veya projeler:")
            extra_info = st.text_area("Ek Bilgiler:",
                                      placeholder="Örn: Google AI Sertifikası aldım, XYZ seminerine katıldım...")

    with col2:
        st.subheader("📄 Mevcut CV'niz")
        uploaded_file = st.file_uploader("CV'nizi PDF formatında yükleyin", type="pdf")

    if st.button("Derin Analizi Başlat", use_container_width=True):
        if not is_api_configured():
            st.error("API Anahtarı bulunamadı. Lütfen sisteme tanımlayın.")
        elif job_description and uploaded_file:
            with st.spinner("Gemini teknik ve sosyal becerileri analiz ediyor..."):
                cv_text = extract_text_from_pdf(uploaded_file)
                
                if cv_text.startswith("PDF okuma hatası"):
                    st.error(cv_text)
                else:
                    analysis_prompt = f"""
                    You are an elite Senior HR Director and Technical Recruiter specializing in ATS (Applicant Tracking Systems).
                    TARGET COUNTRY: {target_country} | OUTPUT LANGUAGE: {target_lang}
                    JOB DESCRIPTION: {job_description}
                    CANDIDATE CV: {cv_text}
                    EXTRA ACHIEVEMENTS: {extra_info}

                    YOUR MISSION:
                    1. MATCH SCORE: Evaluate the overall match between the job description and the CV out of 100 (initial_score). Consider ATS keyword density.
                    2. SCORE REASONS: List 3 main reasons for this score, focusing on both ATS parsability and human readability (score_reasons).
                    3. TECHNICAL ANALYSIS: Evaluate hard skills, tools, and exact keyword matching required by the job against the CV.
                    4. SOFT SKILLS ANALYSIS: Analyze expectations like leadership, initiative, adaptation, and cultural fit.
                    5. GAP ANALYSIS: Identify the top 2 missing aspects or weaknesses (one technical, one soft skill) in the CV for this specific role.
                    6. INTERVIEW QUESTIONS: Ask exactly 2 very specific questions. The candidate will answer these to provide material to strengthen their CV (e.g., asking for a STAR method example for a missing skill).

                    CRITICAL INSTRUCTION: Your output MUST be in {target_lang} language and strictly formatted as valid JSON:
                    {{
                        "initial_score": 85,
                        "score_reasons": ["Reason 1", "Reason 2", "Reason 3"],
                        "tech_analysis": "Summary of technical fit",
                        "soft_analysis": "Summary of soft skills fit",
                        "questions": ["Technical Question", "Soft Skills Question"]
                    }}
                    """
                    result = get_gemini_response(analysis_prompt, is_json=True)
                    try:
                        # Gelen yanıtı sadece json olarak kalacak şekilde daha güçlü temizleyelim
                        import re
                        # Sadece "{ " ile başlayıp "} " ile biten kısmı (JSON objesini) bulalım
                        json_match = re.search(r'\{.*\}', result, re.DOTALL)
                        
                        if json_match:
                            clean_result = json_match.group(0)
                        else:
                            clean_result = result.replace("```json", "").replace("```", "").strip()
                            
                        st.session_state.analysis = json.loads(clean_result)
                        st.session_state.cv_text = cv_text
                        st.session_state.job_desc = job_description
                        st.session_state.extra_info = extra_info
                        st.session_state.country = target_country
                        st.session_state.lang = target_lang
                        st.session_state.step = 'interview'
                        logger.info("Analiz adımı başarıyla geçildi.")
                        st.rerun()
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON Çözümlenirken hata oluştu: {e}. Gemini yanıtı: {result}")
                        st.error("Yapay zeka analiz formatında bir sorun oluştu.")
                        with st.expander("Hatayı İncele (Gemini'den Gelen Ham Yanıt)"):
                            st.write("Aşağıdaki çıktı JSON formatına uymadığı için sistem çöktü:")
                            st.code(result)
                            st.info("Lütfen bu çıktıyı kopyalayıp geliştiriciye/bana iletin ki sorunu kalıcı olarak çözelim veya aynı verilerle tekrar deneyin.")
        else:
            st.warning("Lütfen iş ilanını ve CV'nizi eklediğinizden emin olun.")

# --- ADIM 2: AKILLI MÜLAKAT ---
elif st.session_state.step == 'interview':
    st.subheader(f"🧐 Stratejik Değerlendirme ({st.session_state.lang})")

    initial_score = st.session_state.analysis.get('initial_score', 0)
    st.metric(label="Mevcut CV'nizin İş İlanı ile Uyum Puanı", value=f"%{initial_score}")
    
    reasons = st.session_state.analysis.get('score_reasons', [])
    if reasons:
        st.write("**Puanlama Nedenleri:**")
        for r in reasons:
            st.markdown(f"- {r}")
            
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**💻 Teknik Analiz:**\n{st.session_state.analysis.get('tech_analysis', 'Bulunamadı.')}")
    with c2:
        st.success(f"**🤝 Sosyal/Soyut Analiz:**\n{st.session_state.analysis.get('soft_analysis', 'Bulunamadı.')}")

    st.divider()
    st.write("### CV'nizi Bir Adım Öne Taşıyalım")
    st.write("Yapay zeka, mülakat şansınızı artırmak için şu detayları CV'nize eklemeyi öneriyor:")

    questions = st.session_state.analysis.get('questions', ["", ""])
    ans1 = st.text_area(questions[0] if len(questions) > 0 else "Soru 1",
                        help="Teknik bir detay veya başarı hikayesi ekleyin.")
    ans2 = st.text_area(questions[1] if len(questions) > 1 else "Soru 2",
                        help="İnisiyatif aldığınız veya bir sorunu çözdüğünüz anı anlatın.")

    if st.button("Optimize Edilmiş CV'yi Üret", use_container_width=True):
        if ans1 and ans2:
            st.session_state.user_answers = f"Teknik Yanıt: {ans1}\nSosyal Yanıt: {ans2}"
            st.session_state.step = 'result'
            st.rerun()
        else:
            st.warning("Lütfen her iki soruyu da yanıtlayarak CV'nize güç katın.")

# --- ADIM 3: SONUÇ VE PDF ---
elif st.session_state.step == 'result':
    st.subheader(f"✨ Yeni {st.session_state.lang} Özgeçmişiniz")

    with st.spinner("Kariyer mimarı CV'nizi son haline getiriyor..."):
        final_prompt = f"""
        ROLE & MISSION: You are an elite Executive Career Counselor and ATS (Applicant Tracking System) Optimization Expert. Your goal is to rewrite the candidate's CV/Resume to perfectly match the target role, sector, and target country's standards. It must achieve a 100% ATS parse rate while remaining highly persuasive to human recruiters.
        
        OUTPUT LANGUAGE: {st.session_state.lang} | TARGET COUNTRY: {st.session_state.country}
        JOB DESCRIPTION: {st.session_state.job_desc}
        CANDIDATE DATA: {st.session_state.cv_text}
        EXTRA ACHIEVEMENTS: {st.session_state.extra_info}
        INTERVIEW ANSWERS: {st.session_state.user_answers}

        INSTRUCTIONS:
        1. ATS Optimization (CRITICAL): Ensure perfect keyword density based on the job description. Do NOT use complex tables, columns, or graphics. Format strictly using standard Markdown headers ('#', '##') and bullet points. Use standard section headers (e.g., Professional Summary, Experience, Education, Skills).
        2. Content Integration: Professionally weave the 'Interview Answers' and 'Extra Achievements' into the work experience or summary using the STAR (Situation, Task, Action, Result) methodology.
        3. Professional Tone & Action Verbs: Never use first-person pronouns ("I", "me"). Start bullet points with strong Action Verbs (e.g., "Spearheaded", "Optimized", "Architected") and quantify achievements with metrics, percentages, and amounts wherever possible. Ensure perfect grammar and spelling.
        4. Length Constraint: For corporate roles, strictly limit to 1 page (max 250-300 words). Be perfectly concise. Remove outdated or irrelevant experiences. Academic applications can be 2 pages.
        5. Sector Nuance: Adapt the tone depending on the implied sector (e.g., highly conservative for Finance, innovative for Tech/Design).
        
        CV STRUCTURE & ORDER (Follow Exactly):
        - Personal Contact Info (Header): Name, Phone, Professional Email, LinkedIn/GitHub ONLY. Do not include Home Address, Marital Status, or ID numbers. Output MUST start with the candidate's name as a header (e.g., # Name Surname).
        - Professional Summary: 2-3 sentences summarizing core competencies relevant to the job and long-term goals.
        - Professional Experience: STRICTLY reverse chronological order (newest first). Include Company, Role, and exact Start/End dates. Focus purely on achievements and processes, eliminating irrelevant older duties.
        - Education: STRICTLY reverse chronological order. Remove high school if university is listed. Include GPA only for academic roles or if explicitly high/recent.
        - Projects & Portfolio Links: NEVER delete or omit any URLs, GitHub repos, or portfolio links provided by the candidate unless they are incredibly unprofessional or 100% irrelevant to the role. Embed them naturally within the experience or a separate 'Projects' section.
        - Skills (Hard & Soft): Categorize technical skills/tools clearly to match the JD's keywords.
        - Certifications & Courses: Only relevant industry-recognized certifications.
        - Languages: Honest proficiency levels.
        - Interests (Optional): Only if it adds professional value (e.g., Chess Club President). No cliches.
        - References: "Available upon request" for corporate; explicit contacts for academic.

        COUNTRY-SPECIFIC RULES (Enforce Strictly for {st.session_state.country}):
        {COUNTRY_RULES.get(st.session_state.country, "")}
        
        CRITICAL: Provide ONLY the raw Markdown text of the CV. Do NOT add conversational text like "Here is your CV" or "Sure!". Just output the CV text. Output content must be written in {st.session_state.lang}.
        """
        
        final_cv = get_gemini_response(final_prompt, is_json=False)
        
        if final_cv.startswith("Gemini API Hatası"):
            st.error("Özgeçmiş oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.")
        else:
            with st.spinner("Yeni CV'nizin performansı ölçülüyor..."):
                eval_prompt = f"""
                You are an impartial ATS Algorithm Evaluator and HR Documentation Expert.
                OUTPUT LANGUAGE: {st.session_state.lang}
                JOB DESCRIPTION: {st.session_state.job_desc}
                NEW CV TEXT: {final_cv}
                PREVIOUS SCORE: {st.session_state.analysis.get('initial_score', 0)}

                Evaluate the newly generated CV against the job description. Check for keyword density optimization, structural ATS clarity, the impact of Action Verbs, and persuasiveness of the content. Provide a new match score out of 100.
                
                CRITICAL INSTRUCTION: Your response MUST be valid JSON formatted exactly like this:
                {{
                    "new_score": 95,
                    "improvement_percentage": "+10%",
                    "evaluation_summary": "Summary of what was fixed and strengthened in the new CV for ATS..."
                }}
                """
                eval_result = get_gemini_response(eval_prompt, is_json=True)
                
                try:
                    import re
                    json_match = re.search(r'\{.*\}', eval_result, re.DOTALL)
                    if json_match:
                        clean_eval = json_match.group(0)
                    else:
                        clean_eval = eval_result.replace("```json", "").replace("```", "").strip()
                        
                    eval_data = json.loads(clean_eval)
                except json.JSONDecodeError:
                    eval_data = {
                        "new_score": "Hesaplanamadı",
                        "improvement_percentage": "-",
                        "evaluation_summary": "Değerlendirme özeti alınamadı."
                    }

            st.divider()
            st.subheader("📊 Performans Artışı")
            ec1, ec2, ec3 = st.columns(3)
            with ec1:
                st.metric(label="Önceki Uyum Puanı", value=f"%{st.session_state.analysis.get('initial_score', 0)}")
            with ec2:
                st.metric(label="Yeni Uyum Puanı", value=f"%{eval_data.get('new_score', 0)}", delta=eval_data.get('improvement_percentage', ''))
            with ec3:
                st.info(f"**Değerlendirme Özeti:**\n{eval_data.get('evaluation_summary', '')}")
            st.divider()

            # Sekmeler (Tabs) oluşturma
            tab1, tab2 = st.tabs(["✨ Yeni Özgeçmiş (Temiz Görünüm)", "🔍 Neler Neden Değişti? (Farkları Gör)"])
            
            with tab1:
                st.markdown(final_cv)
                
            with tab2:
                st.info("💡 **Açıklama:** Kırmızı (üstü çizili) olanlar eski/silinen/değiştirilen kısımlar, Yeşil olanlar Yapay Zekanın size özel sıfırdan yazdığı eklemelerdir.")
                # Orijinal PDF metni ile yeni oluşturulan ve biçimlendirilmiş markdown metni arasındaki farklar
                html_diff = generate_html_diff(st.session_state.cv_text, final_cv)
                # Güvenli HTML kullanımı için components.html de kullanılabilir ama markdown ile st.write(unsafe_allow_html) yeterlidir.
                st.write(html_diff, unsafe_allow_html=True)

            # Modülerleştirilmiş PDF Oluşturma 
            try:
                pdf_bytes = generate_cv_pdf(final_cv)
                st.download_button(
                    label="Profesyonel CV'yi PDF Olarak İndir", 
                    data=pdf_bytes,
                    file_name=f"Adaptive_CV_Pro_{st.session_state.lang}.pdf", 
                    mime="application/pdf"
                )
            except Exception as e:
                logger.error(f"PDF indirme butonu hazırlanırken hata: {str(e)}")
                st.error(f"PDF oluşturulamadı: {str(e)}")

    if st.button("🔄 Yeni Analiz"):
        logger.info("Kullanıcı yeni analiz başlattı, oturum sıfırlanıyor.")
        for key in list(st.session_state.keys()): 
            del st.session_state[key]
        st.rerun()