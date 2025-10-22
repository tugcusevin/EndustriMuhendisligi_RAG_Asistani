import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma 
from langchain.chains import RetrievalQA 
# ----------------- YAPILANDIRMA -----------------
PERSIST_DIR = "./chroma_db_ai" # Vektör veritabanı klasörünün konumu

# 1. Sayfa Ayarları (Web Arayüzü)
st.set_page_config(page_title="Endüstri Mühendisliği Asistanı (Gemini RAG)")
st.title("👨‍💻 Endüstri Mühendisliği Öğrenci Asistanı")
st.markdown("Ders notlarına dayalı Yöneylem, Üretim ve Ergonomi sorularını yanıtlar.")

# Hata Kontrolü (API Anahtarı)
gemini_api_key = os.environ.get("GOOGLE_API_KEY")
if not gemini_api_key:
    st.error("HATA: GOOGLE_API_KEY ortam değişkeni ayarlanmamış. CMD’de `set GOOGLE_API_KEY=...` komutuyla ayarlayın.")
    st.stop()

@st.cache_resource
def load_rag_chain(api_key):
    """RAG zincirinin bileşenlerini yükler."""
    if not os.path.isdir(PERSIST_DIR):
        st.error(f"HATA: Vektör veritabanı klasörü ({PERSIST_DIR}) bulunamadı. Lütfen önce 'python rag_pipeline.py' komutunu çalıştırın.")
        st.stop()

    # 1. Embedding ve Vector Store
    embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004", api_key=api_key)
    vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    
    # Retriever objesini alıyoruz (search_kwargs={"k": 4} varsayılabilir)
    retriever = vectorstore.as_retriever() 

    # 2. LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, api_key=api_key)

    # 3. Sorgu işleme fonksiyonu (RAG mantığını burada uyguluyoruz)
    def answer_question(question: str):
        # Düzeltme: Retriever'ı doğrudan çağrı (.invoke) olarak kullanıyoruz.
        docs = retriever.invoke(question) 
        
        # Alakalı dökümanların içeriğini birleştiriyoruz
        context = "\n\n".join([doc.page_content for doc in docs])

        # Nihai Prompt'u oluştur
        prompt_content = (
            "Sen bir Endüstri Mühendisliği öğrencisi asistanısın.\n"
            "Yalnızca sağlanan ders notlarına dayanarak soruları cevapla.\n"
            "Cevabın mantıklı, akademik ve kısa olsun.\n"
            "Eğer bilgi mevcut değilse, 'Elimdeki ders notlarında bu konu hakkında bilgi bulunmamaktadır.' diye yanıtla.\n\n"
            f"Context:\n{context}\n\n"
            f"Soru: {question}"
        )

        # Gemini LLM'e gönder ve cevabı al
        response = llm.invoke(prompt_content)
        return response.content

    # Zincir yerine, doğrudan sorgulama fonksiyonunu döndürüyoruz
    return answer_question 

# Zinciri yükle
try:
    qa_function = load_rag_chain(gemini_api_key)
    st.success("✅ Veritabanı ve Gemini bağlantısı başarılı!")
except Exception as e:
    st.error(f"RAG Zinciri Yüklenirken Hata: {e}")
    st.stop()

# --- Chatbot Arayüzü ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ders notlarınızla ilgili bir soru sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Ders notlarında arama yapılıyor..."):
            try:
                # Sorgulama fonksiyonunu doğrudan çağır
                assistant_response = qa_function(prompt)
            except Exception as e:
                assistant_response = f"⚠️ RAG Zinciri Çalışma Hatası: {e}"
            st.markdown(assistant_response)

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})