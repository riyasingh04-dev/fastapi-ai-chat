import os
from dotenv import load_dotenv

load_dotenv()  

def get_groq_api_key() -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    return api_key

def get_google_client_id() -> str:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not client_id:
        raise ValueError("GOOGLE_CLIENT_ID not found in .env file")
    return client_id

def get_google_client_secret() -> str:
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    if not client_secret:
        raise ValueError("GOOGLE_CLIENT_SECRET not found in .env file")
    return client_secret

def get_secret_key() -> str:
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("SECRET_KEY not found in .env file")
    return secret_key

def get_db_url() -> str:
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")
    db = os.getenv("MYSQL_DB")
    if not all([user, password, host, port, db]):
        raise ValueError("MySQL configuration missing in .env file")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
