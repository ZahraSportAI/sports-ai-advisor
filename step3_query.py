from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# بارگذاری پایگاه داده
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# چند سوال نمونه
questions = [
    "تمرین برای سرعت در تکواندو؟",
    "پروتئین بعد از تمرین بدنسازی؟",
    "تمرین برای مبتدیان؟"
]

print("🧪 جستجوی ساده\n")
for q in questions:
    print(f"❓ {q}")
    results = vector_store.similarity_search(q, k=1)  # فقط یک نتیجه
    print(f"✅ {results[0].page_content}\n")