import os
# LANGCHAIN 1.x UYUMLU İMPORT YOLLARI (Modül Hatasını Çözmek İçin Nihai Versiyon)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# ----------------- YAPILANDIRMA -----------------
PERSIST_DIR = "./chroma_db_ai" # Vektör veritabanının kaydedileceği klasör

def create_vector_store(pdf_folder_path: str = "./"):
    """
    Belirtilen klasördeki PDF'leri yükler, böler ve Chroma DB'ye kaydeder.
    """
    # API Anahtarını Ortam Değişkeninden Çekme (GOOGLE_API_KEY olarak çekilmeli)
    gemini_api_key = os.environ.get("GOOGLE_API_KEY") 

    if not gemini_api_key:
        print("HATA: GOOGLE_API_KEY ortam değişkeni ayarlanmamış. Lütfen CMD'de set GOOGLE_API_KEY=... komutuyla ayarlayın.")
        return

    print("1. Adım: PDF'ler Yükleniyor...")
    documents = []
    # Klasördeki tüm PDF'leri yükle
    for filename in os.listdir(pdf_folder_path):
        if filename.endswith(".pdf"):
            print(f"   -> {filename} yükleniyor...")
            # PyPDFLoader kullanarak PDF'leri yükle
            try:
                loader = PyPDFLoader(os.path.join(pdf_folder_path, filename))
                documents.extend(loader.load())
            except Exception as e:
                print(f"UYARI: {filename} yüklenemedi: {e}")

    if not documents:
        print("\nUYARI: Klasörde (./) hiç PDF makalesi bulunamadı. Lütfen ders notlarını buraya kopyalayın.")
        return

    print(f"Toplam {len(documents)} sayfa yüklendi.")
    
    # 2. Metin Parçalama (Chunking)
    print("2. Adım: Metin Parçalara Ayrılıyor (Chunking)...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    texts = text_splitter.split_documents(documents)
    print(f"Toplam {len(texts)} adet metin parçası (chunk) oluşturuldu.")

    # 3. Gömme Modeli Seçimi (Embedding)
    print("3. Adım: Google Embedding Modeli Yükleniyor...")
    # API anahtarını model başlatılırken zorla geçiriyoruz
    embeddings = GoogleGenerativeAIEmbeddings(
        model="text-embedding-004",
        api_key=gemini_api_key  
    )

    # 4. Vektör Veritabanına Kayıt (Chroma DB)
    print(f"4. Adım: Vektörler Chroma DB'ye Kaydediliyor... Konum: {PERSIST_DIR}")
    
    # Veritabanını oluştur ve kaydet
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=PERSIST_DIR 
    )
    vectorstore.persist()
    print("\n✅ Vektör Veritabanı başarıyla oluşturuldu ve kaydedildi!")

if __name__ == "__main__":
    create_vector_store(pdf_folder_path="./")