FastAPI AI Chat with Golden Ratio UI

A modern, classy AI chat application built with FastAPI, Groq (Llama 3), and a Golden Ratio inspired design — now with secure multi-user authentication.
_______________________________________________________________________________________________________________________________________________
✨ Features
🎨 UI & Experience

Premium Golden Ratio UI: Light, minimal, and classy design (1.618 proportions).

Smooth Chat Experience: Clean layout with role-based responses.

🤖 AI Capabilities

Multi-Role AI

Teacher AI → Explains concepts clearly with structured formatting

Interviewer AI → Conducts technical interviews (questions only)

Debugger AI → Analyzes and fixes code snippets

Fast Inference: Powered by Groq (Llama 3 70B) for ultra-low latency responses

Conversation Memory: Maintains session context per user

🔐 Authentication & Users (NEW)

Multi-User Support

Email & Password Authentication

Google OAuth Login

Secure User Sessions

Protected Routes (Chat accessible only after login)

User-specific Chat Sessions
________________________________________________________________________________________________________________________________________________

🧠 Tech Stack

Backend: Python, FastAPI, Uvicorn

AI Engine: Groq (Llama 3 70B)

Auth: Email/Password + Google OAuth

Frontend: HTML, CSS, JavaScript

Styling: Custom CSS (Golden Ratio Design, no frameworks)
________________________________________________________________________________________________________________________________________________

🚀 Getting Started
Prerequisites

Python 3.8+

A Groq API Key

Google OAuth credentials (for Google login)
________________________________________________________________________________________________________________________________________________

Installation

Clone the repository

git clone https://github.com/riyasingh04-dev/fastapi-ai-chat
cd fastapi-ai-chat


Create & activate virtual environment

python -m venv venv

# Windows
venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


Configure Environment Variables
Create a .env file in the root directory:

GROQ_API_KEY=gsk_your_groq_api_key_here

# Auth
SECRET_KEY=your_secret_key
ALGORITHM=HS256

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret


Run the application

uvicorn app.main:app --reload


Open in browser

http://127.0.0.1:8000
________________________________________________________________________________________________________________________________________________

🔐 Authentication Flow

User can Sign Up using:

Email & Password

Google Account

On successful login:

User session is created

Access to chat interface is granted

Each user has:

Independent session

Isolated conversation context
________________________________________________________________________________________________________________________________________________

🗂️ Project Structure
├── app/
│   ├── main.py              # Application entry point
│   ├── config.py            # Environment & settings
│   ├── routers/
│   │   ├── auth.py          # Login / Signup / Google OAuth
│   │   └── chat.py          # AI chat endpoints
│   ├── services/            # AI & authentication logic
│   ├── static/              # CSS, JS, assets
│   └── templates/           # HTML templates
├── requirements.txt         # Dependencies
├── .env                     # Secrets (ignored by git)
├── .gitignore
└── README.md
________________________________________________________________________________________________________________________________________________

🛡️ Security Notes

.env file is excluded from Git

Passwords are securely hashed

OAuth tokens are handled server-side

Protected routes require authentication
________________________________________________________________________________________________________________________________________________

📌 Future Enhancements

Persistent chat history (DB)

JWT refresh tokens

Role-based access control

User profile & settings
________________________________________________________________________________________________________________________________________________
