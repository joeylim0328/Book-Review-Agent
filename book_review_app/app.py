import streamlit as st
from review_agent import get_book_review

st.set_page_config(
    page_title="📚 Joey's Book Review Agent",
    page_icon="📚",
    layout="centered",
)

st.title("📚 Joey's Book Review Agent")
st.caption("Transform your draft book review into a polished 小红书-style Chinese review.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Book Title", placeholder="e.g. Animal Farm")
with col2:
    author = st.text_input("Author", placeholder="e.g. George Orwell")

draft = st.text_area(
    "Draft Review",
    placeholder="Paste your draft review here (English, Chinese, or mixed)...",
    height=300,
)


ollama_url = st.sidebar.text_input(
    "Book Review",
    value="http://localhost:11434/v1",
    help="URL of your local Ollama instance.",
)

generate = st.button("Generate Review", type="primary", disabled=not (title and author and draft))

if generate:
    with st.spinner("Generating your review..."):
        try:
            review = get_book_review(title, author, draft, base_url=ollama_url)
            st.divider()
            st.subheader("Your 小红书 Review")
            st.markdown(review)
        except Exception as e:
            st.error(f"Failed to generate review: {e}")
