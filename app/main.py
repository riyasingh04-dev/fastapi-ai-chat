from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware
from app.config import get_secret_key
from app.database import engine, Base
from app.routers import chat, auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI AI Chat App")

app.add_middleware(SessionMiddleware, secret_key=get_secret_key())

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(chat.router)
app.include_router(auth.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = request.session.get('user')
    if not user:
        # Redirect to the new unified login page
        return RedirectResponse(url='/auth/login')
        
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": user,
            "token": request.session.get('token')
        }
    )
