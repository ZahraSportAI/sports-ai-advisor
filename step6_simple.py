from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ============================================
# ۱. بارگذاری پایگاه داده
# ============================================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


# ============================================
# ۲. تابع جستجوی هوشمند (با حافظه ساده)
# ============================================
class SimpleAgent:
    def __init__(self):
        self.history = []  # تاریخچه مکالمه
        self.last_question = ""  # آخرین سوال پرسیده شده

    def ask(self, question):
        # ۱. آیا سوال جدید، ادامه‌ی سوال قبلی است؟
        if len(question.split()) < 4 and self.last_question:
            # ترکیب سوال جدید با سوال قبلی
            combined = f"{self.last_question} {question}"
            print(f"🔗 سوال مبهم: '{question}' → ترکیب با قبلی: '{combined}'")
            question_to_search = combined
        else:
            question_to_search = question

        # ۲. جستجو در پایگاه داده
        results = vector_store.similarity_search(question_to_search, k=3)
        answer = results[0].page_content if results else "اطلاعاتی ندارم."

        # ۳. ذخیره در تاریخچه
        self.history.append(f"سوال: {question} → پاسخ: {answer}")
        self.last_question = question  # ذخیره برای سوال بعدی

        return answer


# ============================================
# ۳. تست
# ============================================
print("\n🧪 تست ایجنت ساده با حافظه:\n")

agent = SimpleAgent()

conversation = ["بهترین تمرین برای افزایش استقامت چیست؟",
"چند بار در هفته باید تمرین استقامتی انجام داد؟",
"آیا پروتئین برای بدنسازی لازم است؟",
"چطور می‌توان از آسیب‌های ورزشی پیشگیری کرد؟"
]

for q in conversation:
    print(f"\n❓ سوال: {q}")
    answer = agent.ask(q)
    print(f"✅ پاسخ: {answer}")
    print("-" * 50)

print("\n📝 تاریخچه مکالمه:")
for item in agent.history:
    print(f"  • {item}")
