import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# ============================================
# ۱. بارگذاری ایجنت (همان استپ ۶)
# ============================================
@st.cache_resource
def load_agent():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    class SimpleAgent:
        def __init__(self):
            self.history = []
            self.last_question = ""

        def ask(self, question: str) -> str:
            if len(question.split()) < 4 and self.last_question:
                combined = f"{self.last_question} {question}"
                question_to_search = combined
            else:
                question_to_search = question

            results = vector_store.similarity_search(question_to_search, k=1)
            answer = results[0].page_content if results else "اطلاعاتی در این زمینه ندارم."

            self.history.append(f"سوال: {question} → پاسخ: {answer}")
            self.last_question = question
            return answer

    return SimpleAgent()


# ============================================
# ۲. رابط کاربری Streamlit
# ============================================
st.set_page_config(
    page_title="🏋️ مشاور ورزشی هوشمند",
    page_icon="🏋️",
    layout="centered"
)

st.title("🏋️ مشاور ورزشی هوشمند")
st.markdown("به یک ایجنت هوشمند برای پاسخ به سوالات ورزشی خوش آمدید.")

# بارگذاری ایجنت
agent = load_agent()

# نمایش تاریخچه
if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش پیام‌های قبلی
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ورودی کاربر
if prompt := st.chat_input("سوال خود را بپرسید..."):
    # نمایش سوال کاربر
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # دریافت پاسخ از ایجنت
    with st.chat_message("assistant"):
        with st.spinner("در حال فکر کردن..."):
            response = agent.ask(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# دکمه‌ی پاک کردن تاریخچه
if st.button("🗑️ پاک کردن تاریخچه"):
    st.session_state.messages = []
    st.rerun()
