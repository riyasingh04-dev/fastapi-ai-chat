from pydantic import BaseModel
from typing import Literal

class ChatRequest(BaseModel):
    message: str
    role: Literal["teacher", "interviewer", "debugger"]

class ChatResponse(BaseModel):
    reply: str
    input_words: int
    output_words: int
