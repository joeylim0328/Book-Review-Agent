from openai import OpenAI


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

    system_prompt = """You are an expert at writing engaging book reviews for 小红书 (Xiaohongshu). 
You understand 小红书's audience: young Chinese readers who prefer authentic, conversational content 
with personal insights rather than formal literary analysis."""

    user_prompt = f"""Transform this draft book review of "{title}" by {author} into a polished 
Chinese review suitable for 小红书.

Draft review:
{draft_review}

Requirements:
1. Translate all English content into natural, fluent Chinese
2. Maintain the personal voice and genuine opinions from the original
3. Use an authentic, conversational tone - like chatting with a friend, not writing an essay
4. Structure with natural paragraph breaks (shorter paragraphs work better on 小红书)
5. Keep character names in their original form (e.g., "Napoleon", not "拿破仑")
6. Only refine existing content - don't add information not present in the draft
7. Output entirely in Chinese
8. Keep it under 1000 Chinese characters if possible
9. Emojis are acceptable but use them sparingly - don't overdo it
10. The quote at the end should be remained as English.

Structure the review naturally in paragraph form: Start with an introduction about why you started reading, author background, or novel context. Follow with a plot summary covering the main storyline in 2-3 paragraphs. Then share your personal thoughts about what you liked or didn't like and discuss key themes. Include your recommendation on whether you'd suggest this book to others. End with a closing quote from the novel.

Style: Make it sound like a genuine reader sharing their thoughts, not a formal book report. Feel free to use colloquial expressions, rhetorical questions, or even a bit of humor if it fits the tone. The goal is to create an engaging review that resonates with 小红书's audience while faithfully reflecting the content and spirit of the original draft."""

    response = client.chat.completions.create(
        model="gpt-oss",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content
