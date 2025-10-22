# 👨‍💻 Endüstri Mühendisliği Öğrenci Asistanı (Gemini RAG Chatbot)
**Akbank GenAI Bootcamp Projesi**

## 🎯 1. PROJENİN AMACI
[cite_start]Bu proje, Endüstri Mühendisliği ders notlarına (Yöneylem, Üretim vb.) dayanarak, öğrencilerin sorularına akademik doğrulukta yanıtlar sunan, RAG (Retrieval Augmented Generation) temelli bir chatbot geliştirmeyi amaçlar[cite: 9].

## 📄 2. VERİ SETİ HAKKINDA BİLGİ
* **İçerik:** Endüstri Mühendisliği ders konularını kapsayan PDF ders notları ve akademik kaynaklar kullanılmıştır (Toplam ~981 sayfa).
* [cite_start]**Hazırlık:** Dökümanlar `pypdf` ile yüklendi, `RecursiveCharacterTextSplitter` ile bölündü ve Google Embedding Modeli kullanılarak vektörleştirilip **Chroma DB**'ye kaydedildi. [cite: 10]

## 🛠️ 3. KULLANILAN YÖNTEMLER ve MİMARİ
[cite_start]Proje, sorgunun bağlamsal doğrulukla yanıtlanması için RAG mimarisini kullanır[cite: 11].

| Bileşen | Teknoloji | Görev |
| :--- | :--- | :--- |
| **Generation Model** | [cite_start]Gemini 2.5 Flash API [cite: 42] | Nihai akademik cevabı üretir. |
| **Embedding Model** | [cite_start]Google Embedding [cite: 43] | Ders notlarını vektörlere dönüştürür. |
| **Vektör Database** | [cite_start]Chroma DB [cite: 43] | Vektörleştirilmiş bilgileri saklar. |
| **RAG Pipeline** | [cite_start]LangChain [cite: 44] | Bileşenleri yöneten ve sorguyu işleyen ana çerçevedir. |
| **Arayüz** | Streamlit | Chatbot'u web üzerinden sunar. |

## 📊 4. ELDE EDİLEN SONUÇLAR
[cite_start]Chatbot, yüklenen Endüstri Mühendisliği ders notlarına dayanarak sorulara doğru ve hedefe yönelik cevaplar üretebilmektedir[cite: 12]. [cite_start]Web arayüzü üzerinden sorunsuz çalışır durumdadır[cite: 24].

---

### 🌐 5. PROJE WEB UYGULAMASI (DEPLOY LINKI)
https://endustrimuhendisligirasistani-qgxiebdvftpncz5tzcavw9.streamlit.app
Projenin canlı, çalışan web linki aşağıdadır:

[cite_start]**Canlı Uygulama Linki:** https://endustrimuhendisligirasistani-qgxiebdvftpncz5tzcavw9.streamlit.app [cite: 13]
