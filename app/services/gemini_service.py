
import re
from google import genai
from app.config import get_gemini_api_key
from google.genai.errors import ClientError

client = genai.Client(api_key=get_gemini_api_key())

chat_memory = []

MAX_HISTORY_MESSAGES = 6
MAX_INPUT_WORDS = 500
MAX_OUTPUT_WORDS = 10000

FORMAT_RULES = (
    "Formatting rules (STRICT):\n"
    "- Use plain text only\n"
    "- NEVER write everything in one paragraph\n"
    "- After every heading, add a blank line\n"
    "- After every emoji heading, start on a new line\n"
    "- Each idea must be on its own line\n"
    "- Separate sections with an empty line\n"
    "- Keep paragraphs max 2 lines\n"
    "- Make it easy to scan with eyes\n"
)

ROLE_PROMPTS = {
    "teacher": (
        "You are a friendly Teacher AI.\n"
        "Explain topics in a visually clean and engaging way.\n"
        "Structure answers like a modern learning blog or ChatGPT response.\n\n"

        "Response style rules:\n"
        "- Start with a short title using an emoji\n"
        "- Give a simple 2–3 line explanation\n"
        "- Show examples in separate lines\n"
        "- Use emojis for sections\n"
        "- Use numbered sections for use-cases\n"
        "- Keep spacing between sections\n"
        "- Avoid long paragraphs\n"
        "- Make it pleasant to read\n"
    )
,

    "interviewer": (
        "You are a professional AI Technical Interviewer.\n"
        "ONLY list questions.\n"
        "No introduction. No explanation.\n"
        "Use strict numbering format:\n"
        "1. Question\n"
        "2. Question\n"
    ),

    "debugger": (
        "You are an expert Python Debugger AI.\n"
        "Identify syntax or logical errors clearly.\n"
        "Explain what is wrong and show corrected code.\n\n"
        + FORMAT_RULES
    )
}

ALLOWED_TOPICS = [
    "python",
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "fastapi"
]

PYTHON_CODE_PATTERNS = [
    r"\bprint\s*\(",
    r"\bdef\s+\w+\(",
    r"\bclass\s+\w+",
    r"\bimport\s+\w+",
    r"\bfor\s+\w+\s+in\s+",
    r"\bif\s+.+:",
]

def looks_like_python_code(message: str) -> bool:
    return any(re.search(pattern, message) for pattern in PYTHON_CODE_PATTERNS)

def is_allowed_topic(message: str, role: str) -> bool:
    msg = message.lower()

    # Debugger always allows Python code
    if role == "debugger" and looks_like_python_code(message):
        return True

    return any(topic in msg for topic in ALLOWED_TOPICS)

def word_count(text: str) -> int:
    return len(text.split())

def clear_memory():
    chat_memory.clear()

def clean_output(text: str) -> str:
    """
    Removes unwanted markdown leftovers just in case
    """
    text = re.sub(r"\*{2,}", "", text)
    text = re.sub(r"#{2,}", "", text)
    return text.strip()

def get_gemini_response(user_message: str, role: str):
    input_words = word_count(user_message)

    if input_words > MAX_INPUT_WORDS:
        return (
            f"Input too long. Please stay within {MAX_INPUT_WORDS} words.",
            input_words,
            0
        )

    if not is_allowed_topic(user_message, role):
        return (
            "Sorry, this question is outside the allowed scope.\n"
            "Please ask only Python or AI related questions.",
            input_words,
            0
        )

    try:

        if role == "interviewer":
            prompt = (
                ROLE_PROMPTS["interviewer"]
                + "\nUser request:\n"
                + user_message
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            reply = clean_output(response.text)
            return reply, input_words, word_count(reply)

        # Teacher / Debugger with memory
        chat_memory.append(f"User: {user_message}")
        recent_history = chat_memory[-MAX_HISTORY_MESSAGES:]

        prompt = (
            ROLE_PROMPTS[role]
            + "\nConversation so far:\n"
            + "\n".join(recent_history)
            + f"\n\nKeep answer under {MAX_OUTPUT_WORDS} words."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        reply = clean_output(response.text)
        chat_memory.append(f"AI: {reply}")

        return reply, input_words, word_count(reply)

    except ClientError:
        return (
            "AI service limit reached. Please try again later.",
            input_words,
            0
        )

    except Exception:
        return (
            "Something went wrong. Please try again.",
            input_words,
            0
        )
