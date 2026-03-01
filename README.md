# 🚀 CareerAdaptive AI Pro

**CareerAdaptive AI Pro**, sadece sıradan bir CV düzenleyici veya şablon doldurucu değildir; gücünü en modern Büyük Dil Modellerinden (LLM - Google Gemini 2.5) alan, stratejik bir **İnsan Kaynakları ve Kariyer Danışmanı** simülasyonudur. 

Bu projenin temel amacı; adayların mevcut pozisyonlarına, hedefledikleri sektöre ve başvurdukları ülkenin işe alım standartlarına **%100 uyumlu, ATS (Aday Takip Sistemi) dostu ve mülakata çağrılma oranını maksimize eden** profesyonel özgeçmişler üretmektir.

---

## ✨ Neyi Farklı ve Kaliteli Yapıyor?

Sıradan CV hazırlama araçlarının aksine, CareerAdaptive AI Pro bir "önce anla, sonra dönüştür" felsefesiyle çalışır:

1. **Stratejik Uyum Analizi (Derinlemesine İnceleme):**
   - Mevcut CV'nizi ve başvurmak istediğiniz iş ilanının metnini yan yana koyarak sadece anahtar kelime eşleştirmesi yapmaz; **bağlamsal uyumu** ölçer.
   - Size 100 üzerinden net bir "Uyum Puanı" verir ve bu puanın perde arkasındaki temel 3 nedeni şeffafça açıklar.
   - İlanın **Hard Skills (Teknik Yetkinlikler)** ve **Soft Skills (Soyut/Sosyal Yetenekler)** beklentilerini ayrı ayrı analiz eder ve mevcut CV'nizdeki "Gap" (Eksiklik) tespiti yapar.

2. **İnteraktif "Akıllı" Mülakat:**
   - CV'nizdeki eksikleri gördükten sonra yapay zeka size, tıpkı gerçek bir İK uzmanı gibi, o ilana özel 2 spesifik soru yöneltir. (Örn: *"İlanda takım liderliği tecrübesi isteniyor, geçmişte kriz anında inisiyatif aldığınız bir anıyı anlatır mısınız?"*)
   - Verdiğiniz bu değerli cevapları alıp, sanki en başından beri CV'nizde varmış gibi profesyonel bir üslupla (Action Verbs - Etken Fiiller kullanarak) iş tecrübelerinizin arasına stratejik bir şekilde yedirir.

3. **Ülke ve Kültür Odaklı Dinamik Format (Yerelleştirme):**
   - Bir CV'nin Almanya, ABD veya İngiltere'deki standartları birbirinden tamamen farklıdır. 
   - Proje; **ABD başvuruları için** 1 sayfalık, fotoğrafsız, sonuç odaklı; **Almanya için** tarih detaylı ve fotoğraflı; **Japonya için** geleneksel "Rirekisho" formatını, **Fransa için** ise *Projet Professionnel* bölümünü hesaba katarak *hedef ülkenin İK kültürüne özel* kalıplarda çıktılar üretir.

4. **Sektörel Zeka:**
   - Finans sektörüne başvuran bir aday için dil son derece ciddi ve matematiksel başarılarla (kâr oranları, optimize edilen bütçeler vb.) bezenirken, Pazarlama veya Tasarım başvurularında daha yenilikçi ve vizyoner bir dil kurgulanır.

5. **Görsel "Neler Değişti?" Fark Ekranı (HTML Diff):**
   - Eski CV'niz ile yenisi arasındaki farkı (neler silindi, neler eklendi) yeşil ve kırmızı işaretlemelerle size sunar. Böylece yapay zekanın nerelere sihirli bir dokunuş yaptığını şeffafça görebilirsiniz.

6. **ATS Dostu, Temiz PDF Çıktısı (ReportLab):**
   - İK yazılımlarının (ATS) en büyük düşmanı karmaşık tablolar, okunmayan fontlar ve iki sütunlu tasarımlardır. 
   - Sistem, arka planda dinamik olarak **Markdown başlıklarını okuyup ReportLab ile sıfırdan, %100 temiz, tek sayfaya optimize edilmiş ve makine okunabilirliği en yüksek seviyede olan** PDF'ler inşa eder.

---

## 🛠️ Sistem Mimarisi ve Nasıl Çalışır?

Proje, gücünü modern web yetenekleri ve ileri düzey yapay zeka işleme yeteneklerinin entegrasyonundan alır:

1. **Girdi (Input) Katmanı (Streamlit UI + PyPDF2):** 
   - Kullanıcı, hedef ülke, hedef dil, iş ilanı metni, varsa ek proje/sertifika bilgilerini girer ve mevcut PDF CV'sini yükler. PyPDF2 ile dosyadan saf metin çıkarılır.
2. **Değerlendirme Katmanı (Gemini 2.5 Flash + JSON Parsing):** 
   - Gemini API, bu büyük veriyi işleyip JSON formatında yapılandırılmış bir "Skor ve Analiz Raporu" döner.
3. **Akıllı Mülakat Katmanı (Etkileşim):** 
   - Uygulama, kullanıcının eksik yönlerini kapatmak için iki soruluk bir mini mülakat ekranı çıkartır.
4. **Jenerasyon Katmanı (Strict Prompting):** 
   - Kullanıcının verdiği mülakat cevapları ve eski veriler birleştirilerek katı Prompt Engineering kurallarıyla ("Ben" dilini kullanma, tek sayfa yap, klişelerden kaçın, aktif fiiller kullan vb.) yeni ve ikna edici özgeçmişin Markdown hali yaratılır.
5. **Geri Bildirim & Render Katmanı (PDF Generation & Diff):** 
   - Oluşturulan yeni CV'nin, eskiye göre ne kadar performans artışı sağladığı (Örn: Puan %60'tan %95'e çıktı) ölçülür.  
   - Hazırlanan Markdown metni, ReportLab algoritmasından geçirilerek şık bir PDF dokümanına dönüştürülür ve kullanıcıya indirmesi için sunulur.

---

## 💻 Teknoloji Yığını (Tech Stack)

* **Arayüz Framework'ü:** Streamlit (Hızlı, Verimli, Pythonik UI)
* **Yapay Zeka Zekası:** Google Generative AI (Gemini 2.5 Flash)
* **Doküman İşleme (PDF):** 
  - `PyPDF2` (Okuma & Parse)
  - `ReportLab` (Sıfırdan ATS uyumlu ve font yerleşimleri hesaplanan PDF Yaratma)
* **Metin Farkı Saptama:** `difflib` (Özel HTML Diff Üretici)
* **Ortam & Değişken Yönetimi:** `python-dotenv`, `Config yapıları`

---

## 🎯 Vizyon (Sonuç)

**CareerAdaptive AI Pro** bir "metin değiştirici" (Text Changer) değil, bir "kader değiştiricidir" (Life Changer). İnsan Kaynakları bariyerlerini ve algoritmik ATS duvarlarını yıkarak, donanımlı yeteneklerin tam da hak ettikleri mülakat masalarına oturmalarını sağlamak için yaratılmış, son derece kaliteli ve bütünsel bir mühendislik ürünüdür.
