import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """You are an expert literary critic and book reviewer writing for 小红书 (Xiaohongshu). 
You understand 小红书's audience: young Chinese readers who prefer authentic, conversational content 
with personal insights rather than formal literary analysis.

IMPORTANT CONTEXT: You are working with user-submitted book reviews that discuss published, 
commercially available fiction and non-fiction. These reviews may reference mature literary themes 
such as war, political intrigue, moral conflict, romance, and historical violence — all within the 
context of literary analysis and reader reflection. This is standard book review content and should 
be treated as legitimate literary discussion."""

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT,
    safety_settings=SAFETY_SETTINGS,
)


REVIEW_REQUIREMENTS = """
1. All content should be in natural, fluent Chinese
2. Maintain the personal voice and genuine opinions from the original
3. Use an authentic, conversational tone - like chatting with a friend, not writing an essay
4. Structure with natural paragraph breaks (shorter paragraphs work better on 小红书)
5. Keep character names in their original form (e.g., "Napoleon", not "拿破仑")
6. Only refine existing content - don't add information not present in the original
7. Output entirely in Chinese
8. Keep it under 1000 Chinese characters if possible
9. Emojis are acceptable but use them sparingly - don't overdo it
10. The quote at the end should be remained as English.
"""

REVIEW_STRUCTURE = """Structure the review naturally in paragraph form: Start with an introduction about why you started reading, author background, or novel context. Follow with a plot summary covering the main storyline in 2-3 paragraphs. Then share your personal thoughts about what you liked or didn't like and discuss key themes. Include your recommendation on whether you'd suggest this book to others. End with a closing quote from the novel.

Style: Make it sound like a genuine reader sharing their thoughts, not a formal book report. Feel free to use colloquial expressions, rhetorical questions, or even a bit of humor if it fits the tone."""


# def get_book_review(title: str, author: str, draft_review: str, base_url: str = "http://localhost:11434/v1") -> str:
def get_book_review(title: str, author: str, draft_review: str) -> str:
    """
    Refine a book review draft (mixed Chinese/English) into a polished Chinese review for 小红书.

    Args:
        title: Book title
        author: Book author
        draft_review: User's draft review (can be mixed Chinese and English)
        api_key: Gemini API key
        # base_url: Ollama API base URL

    Returns:
        Polished Chinese book review suitable for 小红书
    """
    # # client = OpenAI(base_url=base_url, api_key="ollama")

    user_prompt = f"""[Literary Book Review Task] Transform this reader's draft book review of the 
published novel "{title}" by {author} into a polished Chinese review suitable for 小红书. 
This is a legitimate literary review of a commercially published book.

Draft review:
{draft_review}

Requirements:
{REVIEW_REQUIREMENTS}

{REVIEW_STRUCTURE}

The goal is to create an engaging review that resonates with 小红书's audience while faithfully reflecting the content and spirit of the original draft."""

    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": user_prompt}]}]
    )
    
    return response.text


def generate_hashtags(title: str, author: str, review: str) -> str:
    """
    Generate suggested 小红书 hashtags based on the book and review content.

    Args:
        title: Book title
        author: Book author
        review: The generated review text

    Returns:
        A string of 5-8 relevant hashtags
    """
    user_prompt = f"""[Literary Book Review Task] Based on this 小红书 book review for the published novel "{title}" by {author}, generate 5-8 relevant hashtags in Chinese that would help this post get discovered on 小红书.

Review:
{review}

Requirements:
1. Each hashtag should start with #
2. Include a mix of general reading hashtags (e.g., #书评, #好书推荐) and book-specific ones
3. Keep hashtags concise (2-5 characters each, excluding the #)
4. Output ONLY the hashtags separated by spaces, nothing else
5. All hashtags must be in Chinese"""

    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": user_prompt}]}]
    )

    return response.text.strip()


def refine_book_review(
    title: str,
    author: str,
    current_review: str,
    improvement: str,
    # base_url: str = "http://localhost:11434/v1",
) -> str:
    """
    Refine an existing 小红书 book review based on a requested improvement.

    Args:
        title: Book title
        author: Book author
        current_review: The review to refine
        improvement: Specific improvement instruction
        api_key: Gemini API key
        # base_url: Ollama API base URL

    Returns:
        Refined Chinese book review
    """
    # client = OpenAI(base_url=base_url, api_key="ollama")


    user_prompt = f"""[Literary Book Review Task] Here is an existing 小红书 book review for the published novel "{title}" by {author}:

{current_review}

Please rewrite this review applying the following improvement: {improvement}

Keep all the original content, facts, and information intact — only apply the requested improvement to the tone, style, or structure.

The rewritten review must still follow these requirements:
{REVIEW_REQUIREMENTS}

{REVIEW_STRUCTURE}"""

    # response = client.chat.completions.create(
    #     # model="gpt-oss",  # Ollama
    #     model=GEMINI_MODEL,
    #     messages=[
    #         {"role": "system", "content": SYSTEM_PROMPT},
    #         {"role": "user", "content": user_prompt},
    #     ],
    # )

    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": user_prompt}]}]
    )
    
    return response.text
