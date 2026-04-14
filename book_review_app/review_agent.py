from openai import OpenAI

SYSTEM_PROMPT = """You are an expert at writing engaging book reviews for 小红书 (Xiaohongshu). 
You understand 小红书's audience: young Chinese readers who prefer authentic, conversational content 
with personal insights rather than formal literary analysis."""

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


def get_book_review(title: str, author: str, draft_review: str, base_url: str = "http://localhost:11434/v1") -> str:
    """
    Refine a book review draft (mixed Chinese/English) into a polished Chinese review for 小红书.

    Args:
        title: Book title
        author: Book author
        draft_review: User's draft review (can be mixed Chinese and English)
        base_url: Ollama API base URL

    Returns:
        Polished Chinese book review suitable for 小红书
    """
    client = OpenAI(base_url=base_url, api_key="ollama")

    user_prompt = f"""Transform this draft book review of "{title}" by {author} into a polished 
Chinese review suitable for 小红书.

Draft review:
{draft_review}

Requirements:
{REVIEW_REQUIREMENTS}

{REVIEW_STRUCTURE}

The goal is to create an engaging review that resonates with 小红书's audience while faithfully reflecting the content and spirit of the original draft."""

    response = client.chat.completions.create(
        model="gpt-oss",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content


def refine_book_review(
    title: str,
    author: str,
    current_review: str,
    improvement: str,
    base_url: str = "http://localhost:11434/v1",
) -> str:
    """
    Refine an existing 小红书 book review based on a requested improvement.

    Args:
        title: Book title
        author: Book author
        current_review: The review to refine
        improvement: Specific improvement instruction
        base_url: Ollama API base URL

    Returns:
        Refined Chinese book review
    """
    client = OpenAI(base_url=base_url, api_key="ollama")

    user_prompt = f"""Here is an existing 小红书 book review for "{title}" by {author}:

{current_review}

Please rewrite this review applying the following improvement: {improvement}

Keep all the original content, facts, and information intact — only apply the requested improvement to the tone, style, or structure.

The rewritten review must still follow these requirements:
{REVIEW_REQUIREMENTS}

{REVIEW_STRUCTURE}"""

    response = client.chat.completions.create(
        model="gpt-oss",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content
