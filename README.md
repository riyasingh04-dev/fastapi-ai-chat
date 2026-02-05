# FastAPI AI Chat with Golden Ratio UI 

A modern, classy AI chat application built with **FastAPI**, **Groq (Llama 3)**, and a **Golden Ratio** inspired design.

## Features

-   **Premium UI**: Light, classy theme designed with Golden Ratio (1.618) proportions.
-   **Multi-Role AI**:
    -    **Teacher AI**: Explains concepts clearly with structured formatting.
    -    **Interviewer AI**: Conducts technical interviews (questions only).
    -    **Debugger AI**: Analyzes and fixes code snippets.
-   **High-Performance Backend**: Powered by **FastAPI**.
-   **Fast Inference**: Uses **Groq** API (Llama 3 70b) for lightning-fast responses.
-   **Conversation Memory**: Remembers context within the session.

## Tech Stack

-   **Backend**: Python, FastAPI, Uvicorn
-   **AI Engine**: Groq (Llama 3)
-   **Frontend**: HTML, CSS (Golden Ratio Design), JavaScript
-   **Styling**: Custom CSS (No frameworks)

##  Getting Started

### Prerequisites

-   Python 3.8+
-   A [Groq API Key](https://console.groq.com/keys)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/riyasingh04-dev/fastapi-ai-chat
    cd fastapi-ai-chat
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    
    # Windows
    venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Create a `.env` file in the root directory and add your API Key:
    ```env
    GROQ_API_KEY=gsk_your_groq_api_key_here
    ```

5.  **Run the Application**
    ```bash
    uvicorn app.main:app --reload
    ```

6.  **Open in Browser**
    Visit `http://127.0.0.1:8000` to start chatting!

##  Project Structure

```
├── app/
│   ├── main.py              # Entry point
│   ├── config.py            # Environment config
│   ├── routers/             # API endpoints
│   ├── services/            # AI logic (Groq)
│   ├── static/              # CSS & Assets
│   └── templates/           # HTML templates
├── requirements.txt         # Dependencies
├── .env                     # API Keys (Excluded from git)
└── README.md                # Documentation
```

## License

This project is open-source and available under the MIT License.
