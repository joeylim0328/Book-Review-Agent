import os

from dotenv import load_dotenv
import streamlit as st
from review_agent import get_book_review, refine_book_review

load_dotenv()

st.set_page_config(
    page_title="Joey's Book Review Agent",
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


# --- Ollama (local) ---
# default_ollama_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
# ollama_url = st.sidebar.text_input(
#     "Ollama Base URL",
#     value=default_ollama_url,
#     help="URL of your Ollama instance. Set the OLLAMA_BASE_URL env var to change the default.",
# )


generate = st.button("Generate Review", type="primary")

if generate:
    missing_fields = []
    if not title.strip():
        missing_fields.append("**Book Title**")
    if not author.strip():
        missing_fields.append("**Author**")
    if not draft.strip():
        missing_fields.append("**Draft Review**")

    if missing_fields:
        st.warning(f"Please fill in the following field(s): {', '.join(missing_fields)}")
    else:
        with st.spinner("Generating your review..."):
            try:
                # st.session_state.review = get_book_review(title, author, draft, base_url=ollama_url)
                st.session_state.review = get_book_review(title, author, draft)
                st.session_state.review_title = title
                st.session_state.review_author = author
            except Exception as e:
                st.error(f"Failed to generate review: {e}")

if st.session_state.get("review"):
    st.divider()
    st.subheader("Your 小红书 Review")
    st.markdown(st.session_state.review)

    st.divider()
    st.markdown("**Not satisfied? Click what you'd like to improve:**")

    IMPROVEMENT_OPTIONS = {
        "✨ More Engaging": "Make it more captivating and lively, with stronger hooks and more compelling language to draw readers in. Use more emojis to add visual flair and energy",
        "✂️ More Concise": "Make it tighter and more concise, removing any redundancy while keeping all key insights",
        "❤️ More Emotional": "Make it more heartfelt and emotionally resonant, with deeper reflection on how the book made you feel",
        "😄 Add Humor": "Weave in wit and light humor to make the review more entertaining and fun to read. Sprinkle in more emojis to amplify the playful tone",
        "📐 Better Structure": "Improve the overall structure and paragraph flow for smoother, easier readability",
    }

    cols = st.columns(3)
    for i, (label, instruction) in enumerate(IMPROVEMENT_OPTIONS.items()):
        with cols[i % 3]:
            if st.button(label, key=f"improve_{label}", use_container_width=True):
                with st.spinner(f"Refining your review..."):
                    try:
                        # st.session_state.review = refine_book_review(
                        #     st.session_state.review_title,
                        #     st.session_state.review_author,
                        #     st.session_state.review,
                        #     instruction,
                        #     base_url=ollama_url,
                        # )
                        st.session_state.review = refine_book_review(
                            st.session_state.review_title,
                            st.session_state.review_author,
                            st.session_state.review,
                            instruction,
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to refine review: {e}")
