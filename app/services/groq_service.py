import os
from groq import Groq
from app.config import get_groq_api_key

client = Groq(
    api_key=get_groq_api_key(),
)

chat_memory = []

MAX_HISTORY_MESSAGES = 10
MAX_INPUT_WORDS = 1000
MAX_OUTPUT_WORDS = 2000


FORMAT_RULES = (
    "formatting rules (STRICT):\n"
    "- Use plain text only (no markdown bold/italics unless necessary)\n"
    "- NEVER write everything in one huge paragraph\n"
    "- After every heading, add a blank line\n"
    "- After every emoji heading, start on a new line\n"
    "- Each idea must be on its own line\n"
    "- Separate sections with an empty line\n"
    "- Keep paragraphs to max 2 lines\n"
    "- Make it extremely easy to scan\n"
)

ROLE_PROMPTS = {
    "teacher": (
        "You are a friendly Teacher AI.\n"
        "Explain topics in a visually clean and engaging way.\n"
        "Structure answers like a modern learning blog.\n\n"
        "Response style rules:\n"
        "- Start with a short title using an emoji\n"
        "- Give a simple 2–3 line explanation\n"
        "- Show examples in separate lines\n"
        "- Use emojis for sections\n"
        "- Use numbered lists for steps/use-cases\n"
        "- Keep spacing between sections\n"
    ),

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
        "Explain what is wrong and show corrected code.\n"
    )
}

ALLOWED_TOPICS = [
    "python",
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "fastapi",
    "coding",
    "programming"
]

def is_allowed_topic(message: str, role: str) -> bool:
    msg = message.lower()
    if role == "debugger": 
        return True 
    return any(t in msg for t in ALLOWED_TOPICS)

def word_count(text: str) -> int:
    return len(text.split())

def clear_memory():
    chat_memory.clear()

def get_groq_response(user_message: str, role: str):
    input_words = word_count(user_message)

    if input_words > MAX_INPUT_WORDS:
        return (f"Input too long ({input_words} words). Limit is {MAX_INPUT_WORDS}.", input_words, 0)
    


    try:
        
        messages = []
        
      
        system_content = ROLE_PROMPTS.get(role, "You are a helpful AI assistant.") + "\n" + FORMAT_RULES
        messages.append({"role": "system", "content": system_content})

        
        recent_history_strs = chat_memory[-MAX_HISTORY_MESSAGES:]
        for h in recent_history_strs:
            if h.startswith("User: "):
                messages.append({"role": "user", "content": h.replace("User: ", "", 1)})
            elif h.startswith("AI: "):
                messages.append({"role": "assistant", "content": h.replace("AI: ", "", 1)})
        
        messages.append({"role": "user", "content": user_message})

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile", 
            max_tokens=MAX_OUTPUT_WORDS,
            temperature=0.7,
        )

        reply = chat_completion.choices[0].message.content
        
        chat_memory.append(f"User: {user_message}")
        chat_memory.append(f"AI: {reply}")

        return reply, input_words, word_count(reply)

    except Exception as e:
        print(f"Groq Error: {e}")
        return ("Sorry, I encountered an error with the AI service.", input_words, 0)
