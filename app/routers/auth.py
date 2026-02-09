from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from app.config import get_google_client_id, get_google_client_secret
from app.database import get_db
from app.models import User
from app.utils import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel, EmailStr
import random
from datetime import datetime, timedelta
from app.services.email_service import send_otp_email

router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()

def register_oauth():
    oauth.register(
        name='google',
        client_id=get_google_client_id(),
        client_secret=get_google_client_secret(),
        authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
        access_token_url='https://oauth2.googleapis.com/token',
        access_token_params=None,
        authorize_params=None,
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
        client_kwargs={
            'scope': 'openid email profile',
            'timeout': 30.0
        }
    )

register_oauth()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class EmailLoginRequest(BaseModel):
    email: EmailStr

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str

@router.post("/signup")
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=get_password_hash(user_data.password),
        auth_provider="local"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/token")
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/email-login")
async def email_login(login_data: EmailLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    if user.auth_provider != "google":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password required for this account")
    
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    user.otp = otp
    user.otp_expiry = datetime.now() + timedelta(minutes=5)
    db.commit()
    print(f"DEBUG: OTP for {user.email} is {otp}, expires at {user.otp_expiry}")
    
    # Send email
    if send_otp_email(user.email, otp):
        return {"message": "OTP sent to your email"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send OTP email")

@router.post("/verify-otp")
async def verify_otp(verify_data: OTPVerifyRequest, db: Session = Depends(get_db)):
    email = verify_data.email.strip()
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        print(f"DEBUG: User not found for email: '{email}'")
        raise HTTPException(status_code=400, detail="User not found")
        
    if not user.otp or not user.otp_expiry:
        print(f"DEBUG: No OTP record found for {email}")
        raise HTTPException(status_code=400, detail="No OTP requested")
    
    print(f"DEBUG: Verifying OTP for {email}. Stored: '{user.otp}', Received: '{verify_data.otp}'")
    
    if user.otp != verify_data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    now = datetime.now()
    if now > user.otp_expiry:
        print(f"DEBUG: OTP expired for {email}. Now: {now}, Expiry: {user.otp_expiry}")
        user.otp = None
        user.otp_expiry = None
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")
    
    # Valid OTP
    user.otp = None
    user.otp_expiry = None
    db.commit()
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/google")
async def login_google(request: Request):
    google = oauth.create_client('google')
    redirect_uri = request.url_for('auth_callback')
    return await google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        google = oauth.create_client('google')
        token = await google.authorize_access_token(request)
        user_info = token.get('userinfo')
        if not user_info: 
            user_info = await google.userinfo(token=token)
            
        email = user_info.get('email')
        google_id = user_info.get('sub')
        name = user_info.get('name')

        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            db_user = User(
                email=email,
                google_id=google_id,
                name=name,
                auth_provider="google"
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        elif not db_user.google_id:
            db_user.google_id = google_id
            db_user.auth_provider = "google" 
            db.commit()

        access_token = create_access_token(data={"sub": db_user.email})
        
        request.session['user'] = {
            "email": db_user.email, 
            "name": db_user.name,
            "picture": user_info.get('picture')
        }
        request.session['token'] = access_token
        
        return RedirectResponse(url='/')
    except Exception as e:
        print(f"OAuth Error details: {repr(e)}")
        raise HTTPException(status_code=400, detail=f"OAuth failed: {repr(e)}")

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
async def login_page(request: Request):
    if request.session.get('user'):
        return RedirectResponse(url="/")
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/set_session")
async def set_session(request: Request, token: str, email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    request.session['user'] = {"email": user.email, "name": user.name}
    request.session['token'] = token
    return RedirectResponse(url='/')

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url='/auth/login')
